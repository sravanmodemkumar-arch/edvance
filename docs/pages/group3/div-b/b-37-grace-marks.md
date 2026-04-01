# B-37 — Grace Marks & Moderation Register

> **URL:** `/school/academic/results/grace-marks/`
> **File:** `b-37-grace-marks.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Exam Cell Head (S4) — full · HOD (S4) — view own dept · Principal (S6) — full · VP Academic (S5) — view

---

## 1. Purpose

Records and tracks all grace marks and moderation applied to student marks before result computation is finalised. In Indian education, grace marks are a formal mechanism with board-specific rules: CBSE allows "compensatory marks" to students who narrowly fail (pass-fail borderline), "Best of 5" computation where the lowest scoring subject is dropped, and subject-specific grace under special circulars. State boards have their own moderation schemes (Maharashtra famously does state-wide upward scaling; AP/TS boards have pass-granting grace). Every grace marks application must be documented — it cannot be arbitrary. This register is the legal audit trail showing why each student's marks were adjusted.

**CBSE grace marks rules:**
1. **Compensatory marks:** Student who fails by 1–4 marks in 1–2 subjects can receive compensatory marks to reach the pass threshold (33%), subject to guidelines
2. **Best of 5 (X only):** For Class X, the passing percentage is computed on the best 5 subjects out of 6 (if additional subject taken); the lowest mark subject is excluded
3. **Special grace circulars:** CBSE occasionally issues exam-specific circulars granting grace marks due to paper difficulty issues
4. **Condonation of absence:** Not a marks grace but allows absent-in-one-paper students a special consideration

---

## 2. Page Layout

### 2.1 Header
```
Grace Marks & Moderation Register                 [Apply Grace Marks]  [Export Register]
Exam: [Annual Exam 2025–26 ▼]  Class: [All ▼]
Grace Applied: 14 students  ·  Total Additional Marks: 48  ·  Board: CBSE
Status: ⬜ Not yet locked (open for additions)
```

---

## 3. Grace Marks Register

| # | Student | Class | Subject | Original Mark | Grace Applied | Final Mark | Rule Applied | Approved By | Date |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Vikram Singh | IX-A | Mathematics | 30 | +3 | 33 | CBSE Compensatory (borderline pass) | ECH + Principal | 28 Mar |
| 2 | Meena Devi | IX-B | Science | 29 | +4 | 33 | CBSE Compensatory (borderline pass) | ECH + Principal | 28 Mar |
| 3 | Arjun D | X-A | Hindi | 28 | +5 | 33 | CBSE Compensatory (max allowed 5m) | ECH + Principal | 28 Mar |
| 4 | Suresh K | X-B | Mathematics | 38 | Best of 5 applied | — | CBSE Best of 5 (Maths excluded) | ECH | 28 Mar |
| 5 | Priya M | XI-A | Chemistry | 55 | +2 | 57 | CBSE Special Circular No. 14/2025 | ECH | 28 Mar |

Notes:
- "Best of 5" is a computation method, not a marks addition — shown separately
- Grace is applied after all marks are entered and reviewed (B-17), but before result computation (B-18)

---

## 4. Apply Grace Marks Drawer (`grace-apply`, 480px)

[Apply Grace Marks] or click a student row:

```
Apply Grace Marks
Exam: Annual 2025–26

Student: [Search student ▼]
Class:   Auto-filled
Subject: [Select ▼]

Current Marks: 30 / 80
Rule to Apply: [Dropdown]
  → CBSE Compensatory (borderline pass — fail by ≤5 marks)
  → CBSE Best of 5 (Class X only)
  → CBSE Special Circular (requires circular reference)
  → State Board Moderation (state board only)
  → Manual Grace (Principal authorisation required)

Grace Marks Amount: [ 3 ]  (max 5 for compensatory; as per rule for others)

Final Marks (preview): 33 / 80  ✅ Will pass

Circular/Authority Reference: [CBSE Circular Date/No or Leave blank]

Reason Note (mandatory): [Student scored 30; borderline pass; applying max 3m compensatory marks as per CBSE guidelines]

[Apply & Log]  [Cancel]
```

---

## 5. Eligibility Filter

Before manually searching, the system shows students who are eligible for grace marks:

**Borderline Fail List (failed by ≤ 5 marks in any subject):**

| Student | Class | Subject | Score | Max | Pass Mark | Shortfall | Eligible Rule |
|---|---|---|---|---|---|---|---|
| Vikram Singh | IX-A | Mathematics | 30 | 80 | 33 | 3 marks | CBSE Compensatory |
| Meena Devi | IX-B | Science | 29 | 80 | 33 | 4 marks | CBSE Compensatory |
| Arjun D | X-A | Hindi | 28 | 80 | 33 | 5 marks | CBSE Compensatory |
| Ravi P | IX-C | Social Studies | 27 | 80 | 33 | 6 marks | ❌ Exceeds 5m limit |

This list makes it easy for the Exam Cell Head to identify and apply grace without manually searching each student.

---

## 6. Best of 5 Computation (Class X)

CBSE Class X: If a student takes 6 subjects (5 main + 1 additional), the passing percentage is computed on the best 5 scores. The additional/lowest subject is dropped from the percentage calculation (but still appears on the mark sheet).

| Student | S1 | S2 | S3 | S4 | S5 | S6 | Best 5 | Total | % |
|---|---|---|---|---|---|---|---|---|---|
| Suresh K | 72 | 65 | 58 | 70 | 74 | 38 | Drop S6 (38) | 339 | 67.8% |
| Priya L | 80 | 74 | 68 | 72 | 76 | 72 | Drop S1 (any 5) | 362 | 72.4% |

System automatically identifies which subject to drop for each student to maximise their percentage. This computation runs during B-18 (Result Computation) — the register here just documents the decision.

---

## 7. State Board Moderation (State Board Schools)

For schools affiliated with state boards that apply uniform moderation:
- Moderation percentage or marks addition per subject is entered by the Exam Cell Head (from the board's official moderation circular)
- Applied uniformly to all students in affected subjects
- Board circular number mandatory

Example: "AP Board has applied +8 marks moderation to Mathematics for Class X (Circular No. AP/EXAMS/2026/044)"

---

## 8. Lock Grace Register

[Lock Register] — same workflow as IA lock:
- After all grace marks applied, Exam Cell Head confirms and locks
- Locked register feeds into B-18 (Result Computation)
- Any further grace requires Principal + Platform Admin authorisation

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/` | Full grace register |
| 2 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/eligible/` | Borderline fail list |
| 3 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/` | Apply grace marks |
| 4 | `DELETE` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/{entry_id}/` | Reverse grace (before lock) |
| 5 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/lock/` | Lock grace register |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/grace-marks/export/` | Export register PDF |

---

## 10. Business Rules

- Grace marks can only be applied after all marks are reviewed and approved in B-17
- CBSE compensatory marks maximum: 5 marks per subject, maximum 2 subjects per student
- The system validates grace marks amounts against the selected rule — entering 6 marks for CBSE Compensatory rule is blocked
- "Manual Grace" (arbitrary grace not tied to a CBSE/board rule) requires Principal authorisation via A-23 — it is never applied silently
- Grace register is exported as part of the official result documentation for CBSE annual reporting
- Reversing grace marks (before lock) is possible with a reason; after lock it is impossible without Platform Admin

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
