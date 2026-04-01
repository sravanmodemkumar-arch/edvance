# B-18 — Result Computation

> **URL:** `/school/academic/results/<exam_id>/compute/`
> **File:** `b-18-result-computation.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Exam Cell Head (S4) — full · Principal (S6) — full

---

## 1. Purpose

Computes the final results for all students in an exam by combining theory marks (from B-16/B-17), internal assessment marks (from B-31), and grace marks (from B-37). Applies board-specific passing criteria, computes grades, ranks students within class and section, determines pass/fail/compartment status, and generates the result master. Result computation is run after all marks are approved and grace is applied. Once computed, results are reviewed before publication — publication triggers report card generation (B-19) and result analytics (B-20). The computation must be correct because it directly affects student promotion, CBSE board submission, and parent communication.

---

## 2. Page Layout

### 2.1 Header
```
Result Computation — Annual Exam 2025–26         [Run Computation]  [Preview Results]  [Publish Results]
Exam: Annual Exam 2025–26  ·  Classes: VI–XI (52 sections)
Pre-Computation Checklist: ⚠️ 2 items pending
Status: ⬜ Not yet computed
```

---

## 3. Pre-Computation Checklist

All items must be ✅ before computation can run:

| # | Check | Status |
|---|---|---|
| 1 | All marks entries submitted | ✅ 104/104 batches submitted |
| 2 | All marks approved by HODs | ✅ 104/104 approved |
| 3 | Internal Assessment marks locked | ✅ Locked (26 Mar) |
| 4 | Grace marks register locked | ⚠️ Not yet locked (3 pending entries) |
| 5 | Student eligibility list finalised | ✅ Done |
| 6 | Marks structure confirmed (pass criteria) | ✅ Done (from B-11) |

[Run Computation] is disabled until all 6 items are ✅.

---

## 4. Computation Configuration

| Setting | Value |
|---|---|
| Computation mode | Full (theory + IA + grace) |
| Grading scale | CBSE (A1/A2/B1/B2/C1/C2/D/E) |
| Class rank | Within section only / Across all sections of same class |
| Promotion criteria | Auto-promote students with overall pass; flag failures |
| Best of 5 (Class X) | Yes — drop lowest subject |
| CGPA computation | CBSE (Class X/XII: GPA based on grade points) |

---

## 5. Run Computation (Background Task)

[Run Computation] → launches background task:

```
Result Computation — In Progress
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Processing Class VI-A (42 students)...       ✅ Done
Processing Class VI-B (40 students)...       ✅ Done
Processing Class VI-C (38 students)...       ✅ Done
...
Processing Class XI-A (40 students)...       🔄 Running
Processing Class XI-B (38 students)...       ⏳ Pending
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Progress: 34 / 52 sections  ·  65.4%  ·  ~2 min remaining
[Cancel]
```

HTMX polling updates the progress bar every 5 seconds.

---

## 6. Computation Logic (per student, per subject)

```
Step 1: Theory Marks
  theory_marks = approved marks from B-16/B-17

Step 2: Apply Grace Marks (from B-37)
  theory_marks_final = theory_marks + grace_marks (if any)

Step 3: Add Internal Assessment (from B-31)
  For CBSE IX–X:  total_marks = theory_marks_final + ia_marks  (max: 80+20=100)
  For CBSE XI–XII: total_marks = theory_marks_final + ia_marks  (max: 70+30=100)
  For non-IA classes: total_marks = theory_marks_final

Step 4: Apply Best of 5 (CBSE Class X only)
  Identify the subject with lowest marks
  Exclude it from percentage computation (keep on mark sheet)

Step 5: Determine Pass/Fail per subject
  Pass criteria from B-11 config:
    CBSE IX–X: Theory ≥ 27/80 AND IA ≥ 6/20 AND Total ≥ 33/100
    CBSE XI–XII: Theory ≥ 23/70 AND IA ≥ 10/30 AND Total ≥ 33/100

Step 6: Determine Overall Result
  Pass: All subjects pass
  Compartment: Fail in 1–2 subjects (CBSE Class X/XII)
  Fail: Fail in 3+ subjects
  Absent: Marked absent in all/majority subjects

Step 7: Compute Percentage
  percentage = (sum of total_marks across subjects) / (total max marks) × 100

Step 8: Assign Grade (CBSE scale)
  91–100: A1 (10), 81–90: A2 (9), 71–80: B1 (8), 61–70: B2 (7)
  51–60: C1 (6), 41–50: C2 (5), 33–40: D (4), <33: E (Fail)

Step 9: Compute CGPA (Class X/XII)
  CGPA = sum of grade points (best 5) / 5

Step 10: Rank within section
  rank = position by percentage (descending)
  Ties = same rank, next rank skipped

Step 11: Flag for remedial (< 35% in any subject)
```

---

## 7. Post-Computation Preview

After computation, results are shown in preview mode (not yet published):

### 7.1 Summary Statistics

| Class | Section | Total | Pass | Pass % | Fail | Compartment | Avg % | Rank 1 |
|---|---|---|---|---|---|---|---|---|
| XI | A | 40 | 38 | 95.0% | 1 | 1 | 74.2% | Priya Sharma (91.4%) |
| XI | B | 38 | 35 | 92.1% | 2 | 1 | 70.8% | Rohit Kumar (88.2%) |
| IX | A | 42 | 40 | 95.2% | 2 | 0 | 72.6% | Anjali Das (89.4%) |

### 7.2 Failed / Compartment Students

| Student | Class | Failed Subjects | Compartment? | Eligible Remedial? |
|---|---|---|---|---|
| Deepak M | XI-A | Chemistry (29/80 theory) | Compartment (1 subject) | Yes — July supplementary |
| Arjun R | IX-A | Mathematics (25), Hindi (28) | Fail (2 subjects) | Remedial teaching + re-attempt |

### 7.3 Result Anomalies to Review

| Type | Description | Students |
|---|---|---|
| Result changed vs auto-computation | Grace marks pushed 3 students from Fail to Pass | Vikram, Meena, Arjun D |
| Student with 100% in a subject | Suresh K scored 80/80 theory + 20/20 IA in Maths | Verify data |
| Absent but has marks | Anjali Das marked absent but has Chemistry marks entered | Investigate |

[Review and Approve] → Exam Cell Head reviews anomaly list, approves computation.

---

## 8. Publish Results

[Publish Results] → requires Principal approval (via A-23 Approval Hub):
- Principal gets notification with summary
- Principal approves → results go live

**On publication:**
- Students and parents can see results in the Student/Parent portal
- Report cards become generatable (B-19)
- Result analytics are updated (B-20)
- Remedial teaching module (B-34) is notified of at-risk students

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/compute/status/` | Pre-computation checklist |
| 2 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/results/compute/` | Trigger computation (async) |
| 3 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/compute/progress/` | Computation progress |
| 4 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/preview/` | Preview summary |
| 5 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/preview/class/{class_id}/` | Class-level preview |
| 6 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/preview/anomalies/` | Anomaly list |
| 7 | `POST` | `/api/v1/school/{id}/exams/{exam_id}/results/publish/` | Publish results (Principal) |
| 8 | `GET` | `/api/v1/school/{id}/exams/{exam_id}/results/{student_id}/` | Individual student result |

---

## 10. Business Rules

- Computation is deterministic and idempotent — running it again with the same inputs produces the same result
- Re-computation is allowed if a correction is made (e.g., a marks correction approved after initial computation); it re-runs from scratch
- Results can be unpublished (by Principal) if a serious error is discovered — this revokes parent/student visibility but is logged
- CBSE board exam results (Class X/XII) are not computed here — they come from CBSE directly; this page handles internal/school exams only
- Computation for CBSE Class X/XII internal exams is still done here but does not include board theory marks

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division B*
