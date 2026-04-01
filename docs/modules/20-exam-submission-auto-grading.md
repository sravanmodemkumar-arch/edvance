# Module 20 — Exam Submission & Auto-Grading

## Purpose
Receive submitted exam answers from Module 19 (Exam Session & Proctoring), auto-grade
all objective question types instantly, manage the manual evaluation workflow for
descriptive questions, process physical OMR sheets via camera capture, calculate final
marks with grace marks and moderation, feed results to Module 21 (Results & Report Cards),
and generate all compliance-grade analytics for NAAC/NBA/board reporting.

---

## 1. Auto-Grading Engine

### 1.1 Trigger
- Auto-grading fires immediately on each student's submission (Module 19)
- No manual trigger required
- Objective questions: result available within seconds of submission
- Descriptive questions: queued for manual evaluation (Section 3)

### 1.2 MCQ Single Correct
- Student's selected option compared against answer key (per set code)
- Correct option: full marks awarded
- Wrong option: negative marks applied (from Module 18 marking scheme)
- No option selected: zero marks; negative NOT applied
- Per-set answer key: Set A student graded with Set A key; Set B with Set B key (etc.)
- Grace marks override: if HOD granted grace on this question, all students get full marks regardless

### 1.3 MCQ Multiple Correct (JEE Advanced Pattern)
Partial marking schema from Module 18:
```
All correct options selected, no wrong option: Full marks (+4)
3 of 3 correct options, no wrong option:       +3
2 of 3 correct options, no wrong option:       +2
1 of 3 correct options, no wrong option:       +1
Any wrong option included in selection:        −2
No option selected:                             0
```
Schema fully configurable per exam.

### 1.4 True / False
- Correct = full marks; Incorrect = negative marks (if configured); Unanswered = zero
- Justification field (if required): sent to manual evaluation queue separately

### 1.5 Fill in the Blank
- Per blank independently evaluated:
  - Text blanks: case-insensitive exact match; accepted synonyms list (teacher-configured per question in Module 17)
  - Numerical blanks: value within tolerance range (absolute or %)
  - Alternative spellings: common variants pre-loaded (e.g., "Sulphuric" = "Sulfuric")
- Partial marks: configurable — each correct blank = (total marks / number of blanks)
- All correct = full marks; all wrong = negative (if configured)

### 1.6 Numerical Answer Type
```
Student value vs correct value:
  Within tolerance (abs or %): full marks
  Outside tolerance:           zero marks
  Negative marking:            NOT applied for numerical (JEE Main / NEET pattern)
                               Applied for numerical (configurable for other exams)
  Unanswered:                  zero marks
```

### 1.7 Integer Type (0–9)
- Exact match: full marks
- Wrong digit: negative marks per configured scheme (JEE Advanced: −1)
- Unanswered: zero marks

### 1.8 Decimal Type (JEE Main)
- Student value matched to configured decimal places within tolerance
- No negative marking (JEE Main numerical section pattern)

### 1.9 Match the Following
- Per-pair scoring: each correctly matched pair = (total marks ÷ total pairs)
- All pairs correct = full marks
- Wrong pairs: negative per pair if configured
- Unanswered pair: zero for that pair

### 1.10 Matrix Match (JEE Advanced)
- Per-row scoring: each row evaluated independently
- Correct complete row mapping = row marks (+2 per row typically)
- Wrong row mapping = negative per row (−1 per row typically)
- Schema stored in Module 18 answer JSON; applied exactly

### 1.11 Assertion–Reason
- Option (A/B/C/D/E) exact match against per-set answer key
- Standard negative marking applied

### 1.12 Sequence / Arrangement
- Full credit: completely correct order = full marks
- Partial credit (configurable):
  - Each item in correct relative position to adjacent items = fractional mark
  - OR: each item in exact correct position = fractional mark
- Unanswered: zero marks

### 1.13 Diagram Label
- Each label independently evaluated
- Correct label (case-insensitive, accepted variants list) = (marks ÷ total labels)
- Partial scoring per label; no negative for diagram labels

### 1.14 Negative Marking Enforcement
- Negative marks applied only if student selected/entered a response
- Unattempted questions always = zero (never negative)
- Section total floor = 0: student cannot score negative in a section even if negative marks accumulate
- Overall total floor = 0 (configurable — some institutions allow overall negative)

### 1.15 Grace Marks Auto-Application
- If Module 18/19 grace marks granted on question Q:
  - Grace type FULL_ALL: all students get full marks for Q regardless of answer
  - Grace type FULL_ATTEMPTED: students who attempted Q get full marks
  - Grace type CORRECT_ONLY: students who answered correctly keep marks; others get full marks too
- Applied at time of result finalisation; audit entry per student
- Re-calculation triggered automatically when grace is granted after initial grading

---

## 2. OMR Processing (Physical Exams)

### 2.1 Camera Capture
- Invigilator opens EduForge app → "Scan OMR" → device camera activated
- Captures image of filled OMR sheet using camera (not file upload from device storage)
- Captured image processed in-app immediately; never stored to device gallery

### 2.2 Image Preprocessing (In-App)
- Auto-crop: detects OMR boundary; crops to sheet only
- Deskew: corrects tilt up to ±15 degrees
- Brightness / contrast normalisation: improves bubble visibility
- Resolution check: minimum 200 DPI equivalent; prompt re-capture if too low

### 2.3 Data Extraction

#### Roll Number Field
- Bubble matrix for roll number (10-digit) read
- Each digit's bubble column evaluated independently
- Confidence score per digit (0–100%)
- Low confidence (< 70%) on any digit → entire sheet flagged for manual verification

#### Set Code Field
- A / B / C / D bubbles read
- Set code validated against exam's registered sets; invalid set code → flagged

#### Response Fields (Per Question)
- Four-option bubble columns (A/B/C/D) scanned per question
- Confidence score per bubble per question
- Extraction result per question:

| Bubble State | Interpretation |
|---|---|
| One bubble filled, confidence ≥ 70% | Valid response — recorded |
| No bubble filled | Not attempted — zero marks |
| Two+ bubbles filled | Multiple response — flagged |
| All bubbles low confidence (< 50%) | Unreadable — flagged |

### 2.4 Batch Processing
- Invigilator scans all OMR sheets for a section/hall sequentially
- Each capture: immediate processing; running count shown (X processed / Y flagged)
- Batch summary at end: total processed, flagged count, roll numbers detected, missing roll numbers

### 2.5 Flagged Sheet Handling
- Multiple response: flagged — evaluator sees question number; manually confirms correct response or marks as incorrect
- Low confidence: flagged — evaluator views original capture image; manually enters response
- Wrong set code: flagged — admin corrects set code and re-grades
- Unreadable roll number: flagged — admin matches to student manually

### 2.6 Manual OMR Response Entry
- Fallback for: torn sheets, damaged OMR, non-OMR exams needing manual response entry
- Teacher enters responses question-by-question via numbered input interface
- Used for: offline exams where OMR was not pre-printed

### 2.7 OMR Re-Scan
- If result disputed: invigilator re-captures same OMR sheet
- New read compared with original; discrepancy shown question-by-question
- Discrepancy logged; HOD reviews and selects correct version

### 2.8 OMR Reconciliation
- Total OMR processed must match total students marked Present in Module 19 attendance
- Mismatch alert: "15 students marked present but only 14 OMR sheets processed — 1 missing"
- Admin resolves: missing sheet located or marked as "OMR not submitted" (zero score)

### 2.9 OMR Batch Analytics
- Confidence distribution: % of bubbles with > 90% confidence (quality metric for OMR sheet print)
- Common error patterns: students who didn't fill set code, students who left multiple sections blank
- Re-scan rate: % of sheets requiring re-scan (signal for OMR print quality improvement)

---

## 3. Manual Evaluation — Descriptive Questions

### 3.1 Evaluation Queue
- All Short Answer and Long Answer responses queued immediately after exam deadline
- Queue populated per evaluator assignment (from Module 19 multi-evaluator config)
- Queue view: subject / exam / assigned questions / student count / evaluated count / % complete

### 3.2 Evaluation Interface Layout
```
┌─────────────────────────────────┬──────────────────────────────────┐
│ Student Response (Left Panel)   │ Marking Scheme (Right Panel)     │
│                                 │                                  │
│ Q7: Derive expression for       │ Step 1: Definition        1 mark │
│ electric potential energy.      │ Step 2: Diagram           0.5 mk │
│                                 │ Step 3: Work done expr    1 mark │
│ [Student's typed answer here    │ Step 4: Integration       1.5 mk │
│ with equations rendered,        │ Step 5: Final expression  1 mark │
│ formatting preserved]           │ ─────────────────────────────── │
│                                 │ Total:                    5 marks │
│ [Evaluator annotation area]     │ [View Model Answer]              │
└─────────────────────────────────┴──────────────────────────────────┘
  Marks: [0][0.5][1][1.5][2][2.5][3][3.5][4][4.5][5]   [Save Draft] [Submit]
```

### 3.3 Rubric-Based Marking
- Each criterion in marking scheme shown as a row
- Evaluator clicks marks for each criterion (increment of 0.5 or 1 as configured)
- Sub-total auto-calculated per criterion; grand total auto-summed
- Cannot enter marks > criterion maximum (hard guard)
- Cannot enter negative per criterion (floor = 0)

### 3.4 Model Answer Reference
- "View Model Answer" expands full model answer (content blocks from Module 17/18)
- LaTeX equations rendered; diagrams shown; step-by-step visible
- Model answer panel scrollable independently of student response
- Side-by-side comparison: student answer and model answer in split view

### 3.5 Inline Annotation
- Evaluator selects text in student response → adds comment (tick ✓ / cross ✗ / text comment)
- Annotations appear as coloured highlights with tooltip
- Visible to student after result + evaluation release (configurable)
- Used for: "Correct definition ✓", "SI unit missing ✗", "Excellent example ✓"

### 3.6 Keyword Scoring Aid
- For theory questions: teacher pre-defined must-have keywords (Module 17 marking scheme)
- System auto-highlights keywords found (green) and missing (yellow) in student response
- Evaluator uses as aid; not a replacement for evaluator judgement
- Keyword presence count shown: "Found 3 of 5 expected keywords"

### 3.7 AI-Suggested Marks (Advisory)
- For short-answer questions: system calculates semantic similarity between student answer and model answer
- Similarity-based suggestion: "AI suggests: 2–3 marks out of 5"
- Shown as a range (not a single value) to avoid over-reliance
- Teacher always has final say; AI suggestion is advisory only; cannot auto-submit AI marks
- AI suggestion logged separately from teacher marks (for quality tracking)

### 3.8 Plagiarism Detection Within Exam
- For long-answer questions: responses compared across all students in same exam
- Near-identical responses (> 85% text similarity): both flagged
- HOD sees: side-by-side comparison of flagged pair with similarity score
- HOD action: Dismiss (coincidence) / Confirm (both get zero for that question with UFM log)
- Runs before evaluation queue opens (evaluators only see after HOD review of plagiarism flags)

### 3.9 Diagram Answer Evaluation
- Student's canvas drawing from exam rendered as-is for evaluator
- Evaluator sees: drawn diagram with all labels
- Marks labels individually: correct label (tick), wrong label (cross), missing label (noted)
- Marking scheme shows required elements and marks per element

### 3.10 Equation Answer Evaluation
- Student's LaTeX-typed equations rendered and displayed
- Mathematical correctness checked visually by evaluator
- Step marks awarded per marking scheme

### 3.11 Code Answer Evaluation
- Student's code displayed with syntax highlighting
- Evaluator assesses: logic correctness, output, syntax, efficiency per rubric
- Marks entered per rubric criterion

### 3.12 Evaluation Navigation
- Evaluator navigates: by student (evaluate all questions for one student) OR by question (evaluate one question for all students — recommended for consistency)
- Question-by-question mode recommended for fair evaluation
- Evaluator can switch mode at any time (pending answers preserved)

### 3.13 Save as Draft
- Evaluator saves partial evaluation mid-session; picks up from same point on next login
- Draft marks not finalised until evaluator clicks "Submit Question"
- Deadline reminder shown on draft save: "X hours remaining to complete evaluation"

### 3.14 Evaluation Lock
- Once evaluator submits marks for a question-student pair: locked
- Re-open: only via HOD unlock; reason required; re-opening logged
- Lock prevents accidental double-entry or retroactive changes

### 3.15 Evaluation Progress Tracker
- Per evaluator: X of Y students evaluated per question; % complete; estimated time remaining
- HOD dashboard: all evaluators' progress in one view
- Deadline alert to evaluator: at 50% of deadline if < 25% complete
- HOD alert: at 75% of deadline if evaluator < 50% complete

---

## 4. Blind Evaluation

### 4.1 Identity Masking
- In blind mode: evaluator sees Barcode ID only (e.g., "EXM-2025-0042") — not student name, roll number, section, or photo
- Student identifier never appears in evaluation interface
- Even the question paper set code hidden (evaluator sees questions in standard order)

### 4.2 Identity Reveal
- After all assigned evaluations submitted: HOD triggers "Reveal Identity"
- Barcode → student name/roll number mapping restored in marks tabulation
- Reveal is one-time, irreversible, and logged: who revealed, when
- Once revealed, marks sheet shows student names

### 4.3 Accidental Exposure Prevention
- System never renders student photo, name, or roll number in evaluation interface when blind mode active
- API response for evaluation interface: student_id replaced with barcode_id; all personal fields stripped

---

## 5. Double Evaluation & Reconciliation

### 5.1 Independent Evaluation
- Evaluator 1 and Evaluator 2 each evaluate same student responses independently
- Neither evaluator can see the other's marks during evaluation
- Both must complete evaluation before reconciliation runs

### 5.2 Automatic Comparison
After both submit:
```
For each question per student:
  Difference = |Eval1_marks − Eval2_marks|
  If Difference ≤ threshold (e.g., ≤ 1 mark per 5-mark question):
    Final = Average(Eval1, Eval2) rounded to nearest 0.5
  If Difference > threshold:
    → Sent to Head Examiner (HOD / Academic Director)
    → Third evaluator sees Eval1 and Eval2 marks; awards final marks
    → Third evaluator's marks are final
```
Threshold configurable per exam (default: 20% of question marks).

### 5.3 Evaluator Consistency Report
- HOD dashboard per subject:
  - Per question: Eval1 avg vs Eval2 avg; variance between evaluators
  - Per evaluator: overall leniency score (how far above/below class average)
  - Concordance rate: % of question-student pairs within threshold
- Used for: calibration training, identifying lenient/strict evaluators

### 5.4 Anchor Paper Calibration
- HOD sets 3–5 anchor responses per question before evaluation starts
- Anchor responses: pre-decided "correct marks" for each
- New evaluator must evaluate anchor papers first
- System compares evaluator's anchor marks vs preset marks:
  - Within ±10%: evaluator calibrated → proceed
  - > ±10%: evaluator shown discrepancy + model evaluation; must re-do anchors
- Prevents evaluator drift from start

### 5.5 Evaluator Score Drift Detection
- After every 20 student evaluations per question:
  - Evaluator's running average marks compared to overall class average for that question
  - Drift > 15% from class mean: auto-flag to HOD — "Evaluator X may be grading inconsistently on Q7"
- HOD reviews random sample; issues guidance

---

## 6. Marks Tabulation

### 6.1 Score Aggregation
```
Student Total = Objective_Auto_Marks
              + Descriptive_Manual_Marks
              + Practical_Marks (if applicable)
              + Internal_Assessment_Marks (CCE components, Module 15)
              + Project_Marks (Module 14, if applicable)
              ± Grace_Marks (if applied)
              ± Moderation (if applied)
```

### 6.2 Section-Wise Marks
- Marks calculated per section: Section A total, Section B total, etc.
- Sectional cutoff check: for exams with minimum per-section marks (banking/UPSC pattern):
  - Student below sectional cutoff → "Sectional Fail" even if overall total passes
  - All sectional cutoffs must be met for overall Pass

### 6.3 Grand Total Computation
- Sum across all sections
- Grace marks added
- Moderation applied (if configured)
- Rounded: nearest integer / nearest 0.5 per institution config

### 6.4 Percentage Calculation
```
Percentage = (Marks_Earned / Total_Marks) × 100
             Rounded to 2 decimal places
```

### 6.5 Grade Assignment

**CBSE Pattern (10-point grading):**

| Marks Range | Grade | Grade Point |
|---|---|---|
| 91–100 | A1 | 10 |
| 81–90 | A2 | 9 |
| 71–80 | B1 | 8 |
| 61–70 | B2 | 7 |
| 51–60 | C1 | 6 |
| 41–50 | C2 | 5 |
| 33–40 | D | 4 |
| 21–32 | E1 | — |
| 00–20 | E2 | — |

**UGC CGPA (7-point scale for degree colleges):**

| Marks Range | Grade | Grade Point |
|---|---|---|
| 90–100 | O (Outstanding) | 10 |
| 80–89 | A+ (Excellent) | 9 |
| 70–79 | A (Very Good) | 8 |
| 60–69 | B+ (Good) | 7 |
| 50–59 | B (Above Average) | 6 |
| 40–49 | C (Average) | 5 |
| 35–39 | P (Pass) | 4 |
| < 35 | F (Fail) | 0 |

**State Board Patterns:**
All 28 state board grading scales pre-loaded; institution selects on setup.

**Custom Grading Scale:**
Institution defines own grade boundaries; stored per academic year.

### 6.6 CGPA Calculation (College)
- Per semester: SGPA = Σ(Credit × Grade Point) / Σ(Credits)
- Cumulative CGPA = Σ(Semester Credits × SGPA) / Σ(Total Credits)
- Feeds Module 21 transcript generation

### 6.7 Pass / Fail Determination
- Pass condition: total marks ≥ passing marks threshold AND (all sectional cutoffs met, if applicable)
- Fail conditions: total < threshold / any sectional cutoff not met
- Special grades:
  - AB (Absent): student absent; total = 0; separate from zero-mark fail
  - UFM (Unfair Means): exam cancelled per Module 19 incident; marks voided
  - EX (Exempt): CWSN or medical exemption granted; not counted in average
  - INC (Incomplete): evaluation not yet complete; result pending

### 6.8 Detained Flag
- Applied when student fails annual exam AND does not meet board-specific promotion criteria
- Classes 9, 10, 11, 12 only — NOT Classes 1–8 (RTE no-detention mandate)
- CBSE: student fails if < 33% in any subject (theory + practical combined)
- State boards: per state pass criteria
- Detained status: blocks progression to next class; feeds Module 07 student profile

### 6.9 Rank Calculation
- Rank within: section / class / grade / batch
- Ties: same rank assigned; next rank skipped (1, 1, 3 — not 1, 1, 2)
- Rank calculated after all evaluations finalised and marks frozen

### 6.10 Percentile Calculation
- Within class: (students with marks ≤ candidate / total students) × 100
- Within institution: all students of same grade/subject
- EduForge cohort (anonymised): institution average vs platform cohort

---

## 7. Marks Imports from Other Modules

### 7.1 CCE Internal Assessment Components (CBSE)
Automatically pulled from Module 15 CCE allocation + teacher entries:
- Periodic Test 1 / 2 / 3 marks (teacher-entered per unit)
- Notebook assessment marks
- Subject enrichment activity marks
- Combined per CBSE scheme: (best 2 of 3 periodic tests × weight) + notebook + enrichment = 20 marks internal

### 7.2 Practical / Lab Marks
- CBSE practical exams (30 marks): practical exam marks from Module 19 practical exam type
- ITI trade practical: practical component marks
- College lab marks: sessional lab marks
- Combined with theory for subject total

### 7.3 Project / Assignment Marks
- Project marks from Module 14 (project assignment type)
- Tagged to specific subject + term + academic year
- Auto-pulled for subjects with project component
- Teacher confirms pull is correct before finalisation

### 7.4 Co-Curricular Marks
- Art / Music / Dance / PE: performance marks entered by subject teacher
- Module 21 includes in separate co-curricular section of report card
- Not included in academic aggregate (configurable per institution)

### 7.5 External Exam Marks (Board Results)
- For CBSE/state board official results: institution enters declared marks manually
- Theory + Practical marks entered separately per board result format
- Stored separately from internal marks; Module 21 tracks both for comparison
- External marks: read-only once entered and HOD-approved

---

## 8. Marks Moderation

### 8.1 Class-Level Moderation
- If class average < configured threshold (e.g., < 35%) after evaluation:
  - HOD prompted: "Class average is 28.4% — consider moderation"
  - Moderation types:
    - **Fixed addition**: add X marks to all students (e.g., +5 marks to all)
    - **Proportional scaling**: scale all marks by factor (e.g., × 1.15)
    - **Grace on specific question**: use Module 18/19 grace marks workflow
  - Moderation amount, type, and reason logged per exam
  - Before and after moderation: both score sets preserved

### 8.2 Question-Level Moderation Trigger
- If > 80% of class scored zero on a specific question:
  - HOD auto-prompted: "87% of students scored zero on Q7 — possible error in question or marking scheme"
  - HOD reviews: dismiss / grant grace / modify marking scheme
  - Grace marks auto-applied on confirmation (see Section 1.15)

### 8.3 Scaling (Percentile Preservation)
- Advanced moderation: adjust marks so class distribution matches target
- Used for: cross-section fairness (Section A and Section B taught by different teachers)
- Pre/post scaling: both preserved; Module 21 uses post-scaling marks for result; pre-scaling archived

### 8.4 Moderation Audit
- All moderation actions logged: who initiated, type, amount, reason, affected student count
- Moderation history per exam viewable by Principal and Admin
- Cannot be applied after marks sheet is Principal-signed

---

## 9. Marks Verification Workflow

### 9.1 Verification States
```
EVALUATED → TEACHER_SUBMITTED → VERIFIER_CHECKED → HOD_APPROVED
          → PRINCIPAL_SIGNED → PUBLISHED (feeds Module 21)
```

### 9.2 Teacher Submission
- Subject teacher reviews all marks; checks totals; submits marks sheet
- Submission timestamp recorded
- Teacher cannot change marks after submission without HOD unlock

### 9.3 Verifier Check (Second Teacher)
- Second teacher (verifier) re-totals all marks: confirms section totals sum correctly
- Verifier does NOT re-evaluate answer quality — marks addition check only
- Discrepancy: returns to teacher for correction; reason logged

### 9.4 HOD Approval
- HOD reviews: overall marks distribution, pass %, class average, any anomalies
- Approves: marks locked; no further edits without Principal override
- Returns: with specific note; teacher corrects and re-submits

### 9.5 Principal Sign-Off
- For annual exams, pre-boards, semester end: Principal reviews and signs marks sheet
- Digital sign-off: Principal clicks "Approve & Sign"; timestamp + name embedded
- Physical print: marks sheet PDF generated with Principal signature field for physical record

### 9.6 Result Publication
- After Principal sign-off: result published per Module 19 configured release timing
- Marks auto-pushed to Module 21 (Results & Report Cards) — no re-entry
- Module 23 (Leaderboard) receives top-performer data after publication

---

## 10. Re-Evaluation & Re-Totalling

### 10.1 Re-Totalling Request
- Student submits request within configurable window (default: 7 days from result publication)
- Process: system re-sums all marks entries for that student's exam
- Discrepancy found: corrected automatically; result updated; notification to student and parent
- No change found: original result confirmed; student notified
- All re-totalling outcomes logged: request date, original total, new total, difference

### 10.2 Full Re-Evaluation Request
- Student requests answer re-evaluation (answer re-read by new evaluator)
- Configurable per institution: allowed / not allowed
- Re-evaluation fee: institution configures (paid via Module 25); waived for CWSN students
- New evaluator assigned (different from original); blind mode applied
- Outcome: higher marks → result updated; same/lower → original retained OR higher taken (institution policy)
- Re-evaluation turnaround: institution sets SLA (default: 15 working days)

### 10.3 RTI-Based Photocopy Request (RTI Act 2005)
- Student / parent files RTI request for photocopy of evaluated answer sheet
- System generates printable version: student's response with evaluator annotations overlaid
- Admin fulfils within 15 working days per RTI timeline
- Fee: as per institution's RTI fee schedule (nominal — per RTI rules)
- All RTI requests logged; fulfilment status tracked

### 10.4 Re-Evaluation Analytics
- HOD sees: per subject per exam — total re-evaluation requests, % upheld, average marks change
- High re-evaluation rate on a subject = signal for evaluation quality review
- High uphold rate = evaluator calibration issue; HOD investigates

---

## 11. Special Cases Grading

### 11.1 CWSN Students
- Evaluated against CWSN-adapted marking scheme (Module 18 CWSN variant)
- Spelling errors not penalised (per CBSE CWSN guidelines)
- Simplified notation accepted for formulas
- Extended time already accounted in Module 19 (25% additional time)
- CWSN flag visible to evaluator; evaluator calibrated accordingly

### 11.2 Scribe-Written Responses
- Scribe flag from Module 19 visible to evaluator
- Language quality component not penalised (content evaluated only)
- Handwriting quality not relevant
- Evaluator notes "Scribe used" in evaluation record

### 11.3 Absent Students
- All questions: Not Attempted
- Total marks: 0
- Grade: AB (Absent) — not the same as "F" (Fail)
- Separate from zero-score students who appeared
- Absent flag: visible in all reports and Module 21 report card

### 11.4 Expelled (UFM) Students
- Marks: cancelled for that exam
- Grade: UFM (Unfair Means)
- Disciplinary record: linked to Module 19 incident report
- Module 21 report card: shows UFM for that exam; marks not included in aggregate
- HOD and Principal notified; further disciplinary action per institution policy

### 11.5 Late Submission (Grace Period)
- Answers submitted within grace period (Module 19): evaluated normally
- "Late Submission" flag in record; marks not deducted by default
- Penalty configurable: institutions can deduct X% for late submission (configurable; default: no deduction)

### 11.6 Open Book Exam
- Grading logic unchanged
- Evaluator calibration note displayed: "Open-book exam — higher accuracy expected on recall; focus evaluation on application and analysis quality"
- HOT question marks weighted contextually

### 11.7 Take-Home Exam
- Auto-plagiarism check (Module 14 engine) runs on all descriptive responses before evaluation opens
- Flagged pairs: HOD reviews before evaluator queue opens
- Evaluator sees: plagiarism flag status per student before evaluating
- Normal grading applies; plagiarism is separate academic integrity matter

### 11.8 Viva-Voce
- Examiner selects student → question-by-question from Module 17 viva bank
- Per question: rubric shown; examiner taps marks level per criterion
- Total calculated: linked to practical marks for CBSE 30-mark split
- Internal examiner + external examiner marks (if applicable): averaged

### 11.9 Project Defence Marks
- HOD or external examiner enters marks per rubric criterion
- Linked to Module 14 project assignment marks for combined project score
- CO attainment per project rubric criterion calculated

---

## 12. CO Attainment Calculation (NBA / NAAC)

### 12.1 Direct Attainment (Exam-Based)
For each question in exam:
- Question has CO tag(s) from Module 17
- Student's marks for that question contribute to CO attainment

```
CO1 Attainment (student) = Σ(marks earned on CO1-tagged questions)
                           / Σ(total marks of CO1-tagged questions)
                           × 100

CO1 Class Attainment = Average of all students' CO1 attainment
```

### 12.2 Attainment Levels
- Level 1: ≥ 40% students scored ≥ 40% on CO-mapped questions
- Level 2: ≥ 60% students scored ≥ 60%
- Level 3: ≥ 70% students scored ≥ 70%
Thresholds configurable per institution (above are UGC/NBA recommendations).

### 12.3 CO Attainment Report
- Per course per semester:
  - CO-wise attainment level (1/2/3)
  - Student-wise CO marks breakdown
  - Course average per CO
- Exported as NBA OBE Criterion 5 format
- Combined with indirect attainment (student feedback surveys — Module 47) for final CO attainment

### 12.4 PO Attainment Feed
- CO → PO mapping from Module 15 used
- Direct PO attainment calculated from CO attainment × CO-PO correlation strength
- Exported as NBA PO attainment table

---

## 13. Performance Analytics

### 13.1 Per-Question Class Analysis
For every question in the exam:
- % of class who answered correctly
- Average marks earned
- Most common wrong answer (MCQ): which distractor was most chosen
- Average time spent (online exams only)
- Feeds Module 17 item analysis update (difficulty index, discrimination index recalculated)

### 13.2 Class-Wide Weakness Report
- Top 10 questions where class average was lowest
- Topic-wise weak areas identified (based on question tags)
- Auto-feeds Module 15 re-teach flag for identified topics
- Teacher receives in-app: "Consider re-teaching: Electric Field (Q7, Q12 — class avg 28%)"

### 13.3 Bloom's Level Attainment
- Marks earned on L1–L2 (Recall) / L3 (Apply) / L4–L6 (HOTS) — per student and per class
- Shows: "Class average on HOTS questions: 34% — significantly below recall (72%)"
- Used in teaching strategy improvement discussions

### 13.4 Difficulty-Level Performance
- Class accuracy on Easy / Medium / Hard / Very Hard questions
- Cross-referencing: "Hard questions from Chapter 5 had 18% accuracy vs Hard questions from Chapter 3 at 52%"

### 13.5 Subject-Wise Multi-Exam Trend
- Per subject: class average trend across all exams this academic year
- Per student: individual score trend (links to Module 21 report card analytics)
- Feeds Module 47 (AI Performance Analytics) for predictive insights

### 13.6 Evaluator Quality Metrics
Per evaluator per subject (visible to HOD only):
- Average marks awarded per question vs class mean
- Re-evaluation request rate for that evaluator's students
- Double-evaluation concordance rate (if double evaluation used)
- Anchor paper calibration score
- Teacher evaluation quality score: composite of above metrics

### 13.7 Evaluation Turnaround Report
- Days taken from exam submission to marks finalisation, per subject per exam
- Target SLA: configurable (default: 7 working days for internal, 15 for semester-end)
- Breach report: exams where SLA was not met; teacher-wise breakdown
- Used in faculty performance review

---

## 14. Result Compilation & Release

### 14.1 Marks Finalisation
- After: all manual evaluations complete + verifier checked + HOD approved + Principal signed
- HOD triggers "Finalise Marks" — marks frozen for that exam
- Finalisation timestamp permanently stamped in exam record
- No changes possible without Principal override (with audit log)

### 14.2 Result Release
- Per Module 19 configured release timing (Immediate / Scheduled / Manual)
- Result feeds: Module 21 (Report Cards), Module 23 (Leaderboard)
- Student in-app notification: "Your [Exam Name] result is available"
- Parent in-app notification: school/minor students (Module 09)

### 14.3 Result Withhold
- Admin withholds individual student result: reason (fee pending / disciplinary / document pending)
- Student sees: "Your result is currently withheld. Please contact administration."
- HOD override: releases withheld result with documented reason
- DPDPA 2023: withhold reason logged but not shown to student (administrative use only)

### 14.4 Individual Marksheet View
Student sees (configurable what to show):
- Marks per section (or per question — institution choice)
- Total marks, percentage, grade
- Rank in class / batch
- Pass / Fail status
- Evaluator comments per question (if released)

### 14.5 Result Gazette
- Official institution-level result gazette PDF:
  - All students, all subjects, marks, grades, pass/fail, rank
  - Sorted by rank
  - Signed by: Subject Teacher + HOD + Principal (signature fields)
- Published to institution notice board (Module 34)
- Stored in Module 40 document vault

### 14.6 Marks Sheet PDF
- Subject-wise marks sheet: all students, marks per question group, total, percentage, grade
- Combined marks sheet: all subjects per student (final exam results)
- Bulk PDF generation per section/class/exam
- Watermarked: institution name + "OFFICIAL RESULT" + academic year

---

## 15. Data Architecture

### 15.1 Tenancy
- All evaluation data tagged with `tenant_id` (PostgreSQL RLS)
- Answer data stored in DB (not CDN — exam integrity requires DB)
- OMR captures: processed in-app; extracted responses stored in DB; raw image NOT stored after processing
- CO attainment data: tenant-scoped; shared to NAAC/NBA export only

### 15.2 Database Schema

```sql
-- Auto-grading results
auto_grade_results (
  result_id           UUID PK,
  session_id          UUID FK exam_sessions,
  question_id         UUID FK questions,
  tenant_id           UUID FK tenants,
  student_id          UUID FK users,
  set_code            VARCHAR(5),
  response_json       JSONB,
  correct_answer_json JSONB,
  is_correct          BOOLEAN,
  is_attempted        BOOLEAN,
  marks_earned        NUMERIC(4,1),
  negative_applied    NUMERIC(4,1) DEFAULT 0,
  grace_applied       NUMERIC(4,1) DEFAULT 0,
  graded_at           TIMESTAMPTZ
)

-- OMR scan records
omr_scans (
  scan_id             UUID PK,
  exam_id             UUID FK exams,
  tenant_id           UUID FK tenants,
  roll_number_raw     VARCHAR(20),
  roll_number_matched VARCHAR(30),
  student_id          UUID FK users NULL,
  set_code_raw        VARCHAR(5),
  set_code_confirmed  VARCHAR(5),
  confidence_avg      NUMERIC(4,3),
  flagged             BOOLEAN DEFAULT FALSE,
  flag_reasons        TEXT[],
  responses_json      JSONB,
  manually_overridden BOOLEAN DEFAULT FALSE,
  override_by         UUID FK users NULL,
  scanned_by          UUID FK users,
  scanned_at          TIMESTAMPTZ
)

-- Manual evaluation records
manual_evaluations (
  eval_id             UUID PK,
  session_id          UUID FK exam_sessions,
  question_id         UUID FK questions,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  evaluator_id        UUID FK users,
  evaluation_round    INTEGER DEFAULT 1,
  is_blind            BOOLEAN DEFAULT FALSE,
  barcode_id          VARCHAR(30) NULL,
  marks_earned        NUMERIC(4,1) NULL,
  criteria_marks_json JSONB,
  annotations_json    JSONB,
  overall_comment     TEXT NULL,
  ai_suggestion_min   NUMERIC(4,1) NULL,
  ai_suggestion_max   NUMERIC(4,1) NULL,
  keyword_found_count INTEGER NULL,
  keyword_total_count INTEGER NULL,
  plagiarism_flag     BOOLEAN DEFAULT FALSE,
  plagiarism_pair_id  UUID NULL,
  status              VARCHAR(20) DEFAULT 'PENDING',
  -- PENDING | DRAFT | SUBMITTED | LOCKED | REOPENED
  submitted_at        TIMESTAMPTZ NULL,
  created_at          TIMESTAMPTZ,
  updated_at          TIMESTAMPTZ
)

-- Double evaluation reconciliation
eval_reconciliation (
  recon_id            UUID PK,
  session_id          UUID FK exam_sessions,
  question_id         UUID FK questions,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  eval1_id            UUID FK manual_evaluations,
  eval2_id            UUID FK manual_evaluations,
  eval1_marks         NUMERIC(4,1),
  eval2_marks         NUMERIC(4,1),
  difference          NUMERIC(4,1),
  within_threshold    BOOLEAN,
  final_marks         NUMERIC(4,1) NULL,
  final_method        VARCHAR(20) NULL,
  -- AVERAGE | EVAL1 | EVAL2 | THIRD_EVALUATOR
  third_eval_id       UUID FK manual_evaluations NULL,
  resolved_at         TIMESTAMPTZ NULL
)

-- Marks tabulation per student per exam
exam_results (
  result_id           UUID PK,
  exam_id             UUID FK exams,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  roll_number         VARCHAR(30),
  objective_marks     NUMERIC(6,1) DEFAULT 0,
  descriptive_marks   NUMERIC(6,1) DEFAULT 0,
  practical_marks     NUMERIC(6,1) DEFAULT 0,
  internal_marks      NUMERIC(6,1) DEFAULT 0,
  project_marks       NUMERIC(6,1) DEFAULT 0,
  grace_marks         NUMERIC(5,1) DEFAULT 0,
  moderation_marks    NUMERIC(5,1) DEFAULT 0,
  total_marks         NUMERIC(6,1),
  max_marks           NUMERIC(6,1),
  percentage          NUMERIC(5,2),
  grade               VARCHAR(5),
  grade_point         NUMERIC(3,1) NULL,
  pass_status         VARCHAR(10),
  -- PASS | FAIL | AB | UFM | EX | INC | WITHHELD | SECTIONAL_FAIL
  section_marks_json  JSONB,
  rank_in_section     INTEGER NULL,
  rank_in_class       INTEGER NULL,
  rank_in_grade       INTEGER NULL,
  percentile_class    NUMERIC(5,2) NULL,
  percentile_inst     NUMERIC(5,2) NULL,
  is_detained         BOOLEAN DEFAULT FALSE,
  result_withheld     BOOLEAN DEFAULT FALSE,
  withhold_reason     TEXT NULL,
  verification_status VARCHAR(20) DEFAULT 'PENDING',
  -- PENDING | TEACHER_SUBMITTED | VERIFIED | HOD_APPROVED | PRINCIPAL_SIGNED | PUBLISHED
  teacher_submitted_at    TIMESTAMPTZ NULL,
  hod_approved_at         TIMESTAMPTZ NULL,
  principal_signed_at     TIMESTAMPTZ NULL,
  published_at            TIMESTAMPTZ NULL,
  created_at          TIMESTAMPTZ,
  updated_at          TIMESTAMPTZ
)

-- CO attainment per student per exam
co_attainment (
  attainment_id       UUID PK,
  exam_id             UUID FK exams,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  co_code             VARCHAR(20),
  total_co_marks      NUMERIC(6,1),
  earned_co_marks     NUMERIC(6,1),
  attainment_pct      NUMERIC(5,2),
  attainment_level    INTEGER NULL,               -- 1, 2, or 3
  calculated_at       TIMESTAMPTZ
)

-- Re-evaluation requests
reeval_requests (
  request_id          UUID PK,
  exam_id             UUID FK exams,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  request_type        VARCHAR(20),               -- RETOTALLING | FULL_REEVAL | RTI_COPY
  question_ids        UUID[] NULL,
  fee_paid            BOOLEAN DEFAULT FALSE,
  original_marks      NUMERIC(6,1),
  revised_marks       NUMERIC(6,1) NULL,
  outcome             VARCHAR(20) NULL,          -- INCREASED | SAME | DECREASED
  status              VARCHAR(20) DEFAULT 'PENDING',
  assigned_to         UUID FK users NULL,
  due_date            DATE NULL,
  resolved_at         TIMESTAMPTZ NULL,
  created_at          TIMESTAMPTZ
)

-- Marks moderation log
moderation_log (
  mod_id              UUID PK,
  exam_id             UUID FK exams,
  tenant_id           UUID FK tenants,
  moderation_type     VARCHAR(20),              -- FIXED_ADD | SCALING | GRACE_QUESTION
  question_id         UUID FK questions NULL,
  value               NUMERIC(5,2),
  reason              TEXT,
  applied_by          UUID FK users,
  affected_count      INTEGER,
  applied_at          TIMESTAMPTZ
)
```

### 15.3 Indexes
```sql
CREATE INDEX idx_auto_grade_session     ON auto_grade_results(session_id, question_id);
CREATE INDEX idx_manual_eval_queue      ON manual_evaluations(tenant_id, exam_id, evaluator_id, status);
CREATE INDEX idx_manual_eval_student    ON manual_evaluations(student_id, question_id, evaluation_round);
CREATE INDEX idx_results_exam           ON exam_results(exam_id, pass_status, verification_status);
CREATE INDEX idx_results_student        ON exam_results(student_id, exam_id);
CREATE INDEX idx_co_attainment_exam     ON co_attainment(exam_id, co_code);
CREATE INDEX idx_reeval_requests_status ON reeval_requests(tenant_id, status, due_date);
CREATE INDEX idx_omr_scans_exam         ON omr_scans(exam_id, flagged);
```

---

## 16. Roles & Permissions

| Action | Student | Teacher | HOD | Principal | Admin |
|---|---|---|---|---|---|
| View own result | ✅ | — | — | — | — |
| Evaluate descriptive questions | — | Assigned | Dept | View | — |
| Scan OMR sheets | — | ✅ | ✅ | — | ✅ |
| Verify marks totals | — | ✅ assigned | ✅ | — | ✅ |
| Apply grace marks | — | — | ✅ | ✅ | ✅ |
| Apply moderation | — | — | ✅ | ✅ | ✅ |
| Approve / freeze marks | — | — | ✅ | ✅ | ✅ |
| Sign marks sheet | — | — | — | ✅ | — |
| Publish results | — | — | ✅ | ✅ | ✅ |
| Withhold individual result | — | — | — | ✅ | ✅ |
| View evaluator analytics | — | Own | Dept | All | All |
| Request re-evaluation | ✅ | — | — | — | — |
| Process re-evaluation | — | — | ✅ | ✅ | ✅ |
| Export CO attainment (NBA) | — | — | ✅ | ✅ | ✅ |
| Export marks sheet PDF | — | Own subject | Dept | All | All |

---

## 17. Notifications (In-App Only)

| Trigger | Recipient |
|---|---|
| Evaluation queue assigned | Teacher (evaluator) |
| Evaluation deadline approaching (50%) | Teacher |
| Evaluation deadline breached | Teacher, HOD |
| Plagiarism flag raised in exam answers | HOD |
| Evaluator score drift detected | HOD |
| Anchor calibration failed | Teacher (evaluator) |
| Double evaluation sent to third evaluator | HOD, Academic Director |
| Grace marks applied | Teacher (confirmation), HOD |
| Moderation applied | Principal, HOD |
| Marks verified and submitted | HOD |
| HOD approval completed | Principal |
| Result published | Student, Parent (school/minor) |
| Result withheld | Student |
| Re-evaluation request received | HOD, Admin |
| Re-evaluation completed | Student |
| Re-totalling discrepancy found and corrected | Student, HOD |
| Class average below threshold (post-evaluation) | HOD |
| CO attainment report ready | HOD, Academic Director |

---

## 18. Compliance Summary

| Standard | Coverage |
|---|---|
| CBSE Examination Bye-Laws | Marks tabulation format, grace marks, UFM procedure, re-checking window, no-detention Classes 1–8 |
| CBSE CWSN Guidelines | Spelling not penalised, scribe accommodation noted, adapted marking scheme |
| UGC Examination Regulations | Double evaluation, moderation policy, CGPA calculation, result declaration timeline |
| AICTE OBE Guidelines | CO attainment calculation, PO attainment, direct + indirect attainment |
| NBA Criterion 5 | CO-wise question distribution, CO attainment report, PO attainment feed |
| NAAC SSR Criterion 2.5 & 2.6 | Evaluation process, student performance data, pass %, grade distribution |
| RTE Act 2009 | No-detention enforcement Classes 1–8; detained flag only Classes 9–12 |
| RPWD Act 2016 | CWSN evaluation accommodations, re-evaluation fee waiver |
| RTI Act 2005 | Evaluated answer sheet photocopy within 15 working days of request |
| DPDPA 2023 | Answer data 5-year retention; evaluator annotation access-controlled; no third-party sharing; deletion rights after statutory period |
| IT Act 2000 | Evaluation audit trail; marks finalisation timestamp; tamper detection |
| State Board Rules | All 28 state board grading scales, pass criteria, marks formats pre-loaded |
