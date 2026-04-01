# Module 14 — Homework & Assignments

## Purpose
Define how EduForge creates, distributes, submits, grades, and analyses homework and assignments for all institution types — school (CBSE and state board), college, coaching centre (JEE/NEET/UPSC/CA/Banking), and ITI — entirely within the platform, without any file uploads from device storage. All creation and submission is in-app using structured question types, rich-text editors, sketch canvases, and code editors.

---

## 1. Platform-Native Model — No File Upload

- All assignment creation and student submission happens **entirely within EduForge**
- **No file uploads permitted**: no Word (.docx), no PDF, no PPT, no ZIP, no image files from device storage
- Teacher types/builds questions in-app using question type tools
- Student types/draws/selects answers in-app
- Benefits:
  - Uniform access on any device (mobile, tablet, desktop)
  - Platform-level plagiarism detection possible
  - Consistent grading interface
  - No version mismatch or file corruption issues
  - DPDPA-compliant data handling (all data stays in platform)
- All assignment data stored in EduForge database; not on external file storage

---

## 2. Camera Capture — Only Permitted Exception

- Student can capture a photo **directly using device camera** within the app (not upload from device gallery or file system)
- Use cases: hand-drawn geometry diagram, handwritten rough work, science diagram sketch, map drawing
- Camera capture is an in-app action — device gallery/file browser never opened
- Teacher enables or disables camera capture per question (default: disabled)
- Captured image stored within platform; processed for display in submission view
- Image size limit: 2 MB per capture; up to 3 captures per question

---

## 3. MCQ — Multiple Choice Question

- Single correct answer or multiple correct answers (teacher configures)
- Up to 6 options per question
- Options entered as: plain text, equation (math editor), or image (camera-captured by teacher)
- Auto-graded immediately on submission
- For multiple-correct: marks awarded only if all correct options selected and no incorrect options selected (full credit); partial marking configurable
- Options randomised per student (teacher enables — prevents copying from neighbour)
- Student cannot change answer after time-limited assignment expires

---

## 4. Fill in the Blank

- Single or multiple blanks within a sentence or paragraph
- Exact text match or keyword match (teacher selects)
- Keyword match: teacher lists acceptable keywords; any matching word = correct
- Partial marks per blank (configurable)
- Auto-graded on submission
- Case-insensitive matching by default (configurable)
- Spelling tolerance: teacher can mark alternate spellings as acceptable answers

---

## 5. True / False

- Binary statement; student marks True or False
- Auto-graded
- Teacher adds "explanation" field: displayed to student after results published (builds understanding)
- Can be combined with justification: student must also type a one-line reason (manually graded separately)

---

## 6. Match the Following

- Two columns: Column A (items) and Column B (options)
- Student drags Column B items to match with Column A items
- Auto-graded; partial marks per correct pair configurable
- Column B options randomised per student
- Column size: up to 8 pairs per question
- Widely used in Biology (organisms–functions), History (events–dates), Geography (states–capitals)

---

## 7. Short Answer

- Student types answer up to 200 words using plain text input
- Manually graded by teacher
- Teacher adds text feedback per answer
- Word count shown to student in real-time
- Recommended word count range shown (teacher configures — e.g., 50–80 words)
- Auto-save every 60 seconds while student types

---

## 8. Long Answer

- Rich text editor: bold, italic, underline, tables, bullet points, numbered lists, headings
- Up to 1,000 words
- Recommended word count range shown (teacher configures — e.g., 300–500 words)
- Word count live counter with colour indicator: green (in range), yellow (±20%), red (significantly over/under)
- Manually graded using rubric or free scoring
- Teacher inline annotation on submitted answer (Point 88)
- Auto-save every 60 seconds

---

## 9. Numerical Answer

- Student enters a numerical value + selects unit from dropdown
- Teacher sets:
  - Expected answer (exact value)
  - Tolerance range (±): e.g., 9.8 ± 0.1 m/s²
  - Unit (mandatory or optional per question)
- Auto-graded: value within tolerance AND correct unit = full marks; correct value wrong unit = configurable partial marks
- Significant figures check: optional teacher config (e.g., answer must be to 2 decimal places)
- Used extensively in Physics, Chemistry, Mathematics, Engineering

---

## 10. Math / Equation Editor

- Visual equation keyboard embedded in answer input (MathJax / KaTeX rendering)
- Student builds equations using button palette: fractions, powers, roots, integrals, summations, matrices, Greek letters
- No LaTeX knowledge required — button-driven input
- Rendered as formatted mathematics in both input and submission view
- Teacher can also author questions using the same equation editor
- Supports: algebra, calculus, trigonometry, statistics, vectors, matrices
- Auto-graded if answer is an equation matching teacher's key (exact symbolic match or numerical evaluation)

---

## 11. Chemical Formula / Structure

- Embedded chemistry tools:
  - Periodic table reference (click element to insert symbol)
  - Formula builder: student constructs molecular formula using element tiles and subscript/superscript inputs (e.g., H₂SO₄, Ca(OH)₂)
  - Chemical equation balancer: student writes reactants and products; system checks if balanced
  - Structural formula: drawn on sketch canvas (Point 12) for structural diagrams (benzene ring, organic chains)
- Used for: Chemistry Classes 9–12, JEE/NEET Chemistry coaching
- Auto-graded for formula matching; structural diagrams manually reviewed

---

## 12. Diagram / Sketch Canvas

- Free-hand drawing tool embedded in app
- Student draws using:
  - Touch (finger or stylus on tablet)
  - Mouse (on desktop/laptop)
- Drawing tools: pen, eraser, straight line, circle, rectangle, colour palette, text label
- Use cases: geometry diagrams, biology diagrams (plant cell, heart, neuron), geography maps, circuit diagrams, ray diagrams, free-body diagrams, flowcharts
- Submitted drawing stored as vector within platform (not as an uploaded image file)
- Teacher views drawing in grading interface; adds sketch-level feedback by drawing on top of student's submission (annotation layer)

---

## 13. Code Editor

- Syntax-highlighted online code editor embedded in platform
- Supported languages: Python, C, C++, Java, HTML/CSS, JavaScript, SQL
- Features: line numbers, auto-indent, bracket matching, syntax error highlighting
- Optional sandboxed code execution (teacher enables per question):
  - Student's code runs in isolated environment
  - Output compared against teacher's expected output
  - Auto-graded on output match; partial credit for partial output match
- Used for: CS/IT Classes 11–12, BCA/MCA assignments, coding bootcamp batches
- No file upload; code written entirely in platform editor

---

## 14. Integer Type Question (JEE / Coaching)

- JEE Advanced and coaching pattern: answer is a non-negative integer
- Single-digit integers: 0–9 (JEE Advanced pattern)
- Double-digit integers: 0–99 (some coaching variants)
- Student enters number using numeric keypad within app
- Auto-graded: exact integer match required; no partial credit
- No negative marking for integer type (JEE pattern)
- Coaching centers: most commonly used for Mathematics, Physics problems

---

## 15. Assertion-Reason Question (NEET / JEE)

- Two statements presented: Assertion (A) and Reason (R)
- Student selects one of four standard options:
  1. Both A and R are true, and R is the correct explanation of A
  2. Both A and R are true, but R is not the correct explanation of A
  3. A is true, but R is false
  4. A is false, but R is true
- Auto-graded on selection
- Used extensively in: NEET Biology, NEET Chemistry, JEE Chemistry coaching
- Teacher marks which option is correct at question creation

---

## 16. Paragraph-Based / Comprehension Question Set

- A reading passage, data table, or experimental scenario presented at top
- 3–5 questions based on the same passage linked below
- Passage displayed alongside questions in split-screen view (student does not need to scroll back)
- Question types within the set: MCQ, short answer, numerical, true/false (mixed)
- Used in: JEE, NEET, UPSC, CAT, Bank PO, CUET, reading comprehension in language subjects
- Partial and full passage question sets supported

---

## 17. Matrix Match Question (JEE)

- Column I (typically 4 items) matched with Column II (typically 4–6 options)
- Multiple correct pairings per item (one item in Col I can match multiple in Col II)
- Student drags Col II options to match with each Col I item
- Partial marks per correct pair (configurable)
- Auto-graded
- Widely used in JEE Main/Advanced Physics, Chemistry, Mathematics problem sets

---

## 18. Statement-Based Question

- 3–5 statements listed (Statement I, II, III, IV, V)
- Student selects which statements are correct (single or multiple)
- Auto-graded
- Commonly used in: UPSC Prelims, Bank PO/Clerk, State PSC, SSC CGL/CHSL, CUET

---

## 19. Negative Marking Configuration

- Teacher configures negative marking per question (or per assignment):
  - JEE Main pattern: +4 for correct, −1 for wrong
  - JEE Advanced pattern: +4 correct, −2 wrong, 0 unattempted
  - NEET pattern: +4 correct, −1 wrong
  - Bank/UPSC: +1 correct, −0.25 or −0.33 wrong
  - Custom: any positive/negative combination configurable
- Student sees running score (with negatives) as they answer each question
- Warning prompt when student tries to change an already-answered MCQ: "Changing this answer may result in negative marks. Proceed?"
- Final score can be negative; displayed as 0 in student-visible result if institution configures floor-at-zero

---

## 20. Digital Lab Record Book

- Replaces physical lab record book entirely — no file upload required
- Structured assignment type with defined sections per lab experiment:
  1. **Aim** — text input
  2. **Apparatus / Materials Required** — checklist or text
  3. **Theory / Principle** — rich text
  4. **Procedure** — numbered steps (rich text)
  5. **Circuit Diagram / Setup Diagram** — sketch canvas (Point 12)
  6. **Observations Table** — structured table (Point 21)
  7. **Calculations** — math editor (Point 10)
  8. **Result** — short text
  9. **Precautions** — bullet list
  10. **Sources of Error** — bullet list
  11. **Conclusion** — short text
- Teacher grades each section independently with marks and feedback
- Final mark auto-summed; contributes to CBSE internal practical assessment
- CBSE Classes 11–12 Science: practical internal = 30 marks (lab record + viva + actual practical exam)
- ITI: trade practical record maintained in same format with trade-specific sections

---

## 21. Lab Observation Table

- Teacher defines table structure at assignment creation:
  - Number of rows and columns
  - Column headers (e.g., S.No., Length (cm), Mass (g), Trial 1, Trial 2, Average)
  - Read-only columns (pre-filled by teacher): S.No., given constants
  - Student-fill columns: observation values, calculated values
- System auto-calculates: averages, sums, standard deviation where teacher enables formula
- Student fills table row by row on device; mobile-friendly table interface
- Submitted table rendered cleanly in grading view; teacher checks values and adds feedback

---

## 22. Viva-Voce Preparation Assignment

- Teacher creates a set of expected viva questions before the actual viva examination
- Student answers each question within platform (text/equation/sketch as appropriate)
- Teacher reviews student's preparation level; uses responses to decide depth of actual viva questioning
- Student benefits: structured preparation before high-stress oral examination
- Marks from viva-prep assignment: optional (can be counted toward participation grade or left ungraded)
- Linked to specific experiment/lab record if applicable

---

## 23. Practice Assignment (Ungraded)

- Purpose: self-study and reinforcement
- Student sees correct answer immediately after submitting each question (or after submitting all — teacher config)
- No marks recorded in internal assessment
- No parent notification for practice assignments
- Can be attempted multiple times (each attempt tracked; student sees improvement)
- Teacher sees attempt count and score per student: gauge of engagement

---

## 24. Formative Assessment Assignment (Graded)

- Marks contribute to CCE / continuous internal assessment (configurable per subject per term)
- CBSE internal assessment breakdown (configurable):
  - Periodic Tests: 10 marks
  - Assignment / Portfolio: 5 marks
  - Subject Enrichment Activity: 5 marks
  - Total Internal: 20 marks
- Teacher marks which assignments count and their weightage in internal assessment
- Auto-fed to Module 21 Results when graded and published

---

## 25. Holiday Homework Pack

- Special assignment type given before: Diwali, Holi, Summer, Winter vacations
- Multiple subjects' holiday assignments bundled under one "Holiday Homework Pack" for the class
- Student opens pack → sees subject-wise assignments → submits each within platform
- Due date: first working day after vacation
- Parent-visible immediately on creation: parent sees all assigned work during vacation
- Late return from vacation: student selects "Returned late" reason; teacher decides penalty waiver case-by-case
- No auto-late penalty for genuine delayed vacation return (configurable)

---

## 26. Summer / Winter Project Assignment

- Extended multi-week project (2–8 weeks)
- Broken into milestones with individual due dates:
  - Milestone 1: Topic selection + outline (Week 1)
  - Milestone 2: Research notes (Week 2–3)
  - Milestone 3: Draft (Week 4–5)
  - Milestone 4: Final submission (Week 6)
- Student submits each milestone within platform
- Teacher grades each milestone separately
- Cumulative weighted score
- Teacher provides feedback at each milestone; student incorporates before next milestone

---

## 27. Group / Collaborative Assignment

- Team of 2–6 students works together
- Group composition: set by teacher OR self-selected by students (teacher enables self-selection)
- Shared workspace: all group members can edit answers simultaneously within platform
- One student submits final version on behalf of group; all members receive same grade
- Contribution tracking: system logs which group member contributed to which sections (based on edit timestamps)
- Teacher can see contribution log; differentiates effort if needed
- Used for: project work, debate preparation, group experiments

---

## 28. Differential Assignment

- Teacher creates 2–3 difficulty variants of the same assignment:
  - **Advanced**: additional HOTS (Higher Order Thinking Skills) questions, extended problems
  - **Standard**: NCERT-aligned, grade-appropriate
  - **Remedial**: simplified questions, step-by-step scaffolding
- Teacher assigns each variant to specific student groups within the class (groups defined by teacher)
- Student sees only their assigned variant; no awareness of other variants
- Teacher's analytics view: performance across all three groups; identifies whether differentiation is working
- Marks normalised for fair comparison across variants (configurable)

---

## 29. Peer Review Assignment

- Teacher assigns students to anonymously review each other's long answers
- Process:
  1. All students submit their answers
  2. Each student is assigned 2–3 peers' submissions to review (identity hidden)
  3. Reviewer uses teacher's rubric to assign marks and write comments
  4. Final score: teacher % + peer average % (configurable weighting, e.g., 70% teacher + 30% peers)
  5. Student receives: own score + anonymised peer feedback
- Pedagogical benefit: develops critical thinking, teaches evaluation skills
- Teacher sees all peer reviews; can override aberrant peer scores
- Builds skills aligned with NEP 2020's emphasis on peer learning

---

## 30. In-Class Timed Assignment

- Teacher activates a countdown timer (15 / 20 / 30 / 45 / 60 minutes configurable)
- Timer starts when each student opens the assignment
- Auto-submits student's current progress when timer expires
- Teacher monitors live: submission count, % completed in class in real-time
- Used for: surprise tests, class participation grade, in-class practice
- Students who joined late: timer starts from their join time (not class start time); teacher override available

---

## 31. Assignment Creation — Builder Interface

Teacher creates assignment in-app:
1. **Title** — assignment name
2. **Subject** — linked from enrolled subjects
3. **Target** — class/section, batch, individual students, or groups
4. **Assignment type** — practice, formative, holiday, timed, etc.
5. **Available from** — date and time students can first access
6. **Due date and time** — submission deadline
7. **Grace period** — additional time after deadline (configurable)
8. **Total marks** — auto-calculated from question marks
9. **Instructions** — rich text field; can include regional language text
10. **Questions** — added one by one using question type selector

Questions can be:
- Created fresh in the builder
- Pulled from Question Bank (Module 17)
- Copied from a saved template

---

## 32. Question Bank Integration (Module 17)

- Teacher opens Question Bank within assignment builder
- Searches by: subject, chapter/topic, class level, question type, difficulty, Bloom's level
- Selected questions auto-populate in assignment with correct answers and marks
- Teacher modifies as needed before saving
- Newly created questions optionally saved back to Question Bank (teacher checks "Save to Question Bank")
- NCERT standard exercise questions importable directly as templates (tagged by chapter and exercise number)

---

## 33. Syllabus Topic Linking (Module 15)

- Each assignment linked to one or more syllabus topics from Module 15 Syllabus Builder
- Linking purpose:
  - Tracks which topics have been assessed
  - Feeds syllabus coverage dashboard (are untested topics being skipped?)
  - Allows student to see which chapter this assignment is from
  - HOD can see topic-wise assessment coverage across the term
- Multiple topic links per assignment allowed (for integrated/cross-chapter assignments)

---

## 34. Question Randomisation

- Teacher enables per assignment: question order shuffled per student
- MCQ option order also shuffled per student independently
- Match-the-following: Column B shuffled per student
- Randomisation seed stored (teacher can see each student's question order in grading view)
- Prevents desk-neighbour copying; effective for in-class timed assignments
- System-level randomisation; no student action or awareness needed

---

## 35. Bulk Assign to Multiple Sections

- Teacher creates one assignment and publishes to multiple sections simultaneously (e.g., Class 10 A, B, C, D)
- Each section gets an independent assignment instance:
  - Independent submission tracking
  - Independent grading list
  - Independent analytics
- Useful when the same subject teacher handles multiple parallel sections
- Grade distribution visible across sections for comparison

---

## 36. Assignment for Individual Student

- Teacher creates a personalised assignment visible only to one specific student
- Use cases:
  - Extra practice for weak student (specific topic)
  - Advanced problem set for high-performer
  - Make-up assignment for student who was absent
  - Special assignment for CWSN student (Point 70)
- Other students in the class do not see this assignment
- Marks from individual assignments: counted toward internal assessment if teacher configures

---

## 37. Assignment Prerequisite Sequence

- For coaching batches and structured learning paths:
  - Assignment B visible to student only after Assignment A is submitted
  - Student cannot skip ahead to more advanced assignment
- Teacher configures prerequisite chain at assignment creation
- Used for: JEE preparation ladder (Basic → Intermediate → Advanced), language skill building, coding curriculum
- Chain displayed to student as a learning path map: completed (unlocked) vs locked assignments

---

## 38. Scheduled Auto-Publish

- Teacher creates and saves assignment with a future publish date/time
- System auto-publishes at configured time (e.g., 9:00 PM Sunday for Monday morning class)
- Teacher does not need to be online at publish time
- Student notification triggered automatically at publish time
- Useful for: weekend preparation, batch-start assignments, holiday homework published on last working day

---

## 39. Assignment Versioning After Publish

- If teacher edits a published assignment (corrects typo, adjusts marks, adds a question):
  - System creates Version 2; original (v1) archived
  - Students who already submitted under v1: graded as per v1; not affected by v2
  - Students who have not yet submitted: see v2 with "Updated" tag showing what changed
  - Version history: teacher can view all versions, what changed, when, by whom
- Prevents confusion; maintains submission integrity

---

## 40. Student Submission Flow

```
Student receives in-app notification: "New assignment: [Title] — Due: [Date/Time]"
  → Opens assignment; reads instructions
  → Answers questions one by one (text / sketch / MCQ / equation / code)
  → Auto-save every 60 seconds
  → Reviews all answers before submitting
  → Taps Submit
  → Submission receipt: assignment name, timestamp, submission ID
  → Status updates to "Submitted" on student's dashboard
```

Student can pause and resume from any device (mobile, tablet, desktop) before submission.

---

## 41. Auto-Save Draft

- Student's answers auto-saved every 60 seconds to server
- Student can close app midway and resume from any device
- Resume prompt: "You have a saved draft for [Assignment]. Continue from where you left off?"
- Draft clearly marked (not submitted); student must tap Submit to finalise
- Draft auto-deletes 24 hours after assignment deadline (configurable)

---

## 42. Submission Receipt

- On submission: in-app confirmation card displayed:
  - Assignment title
  - Subject
  - Submission timestamp
  - Unique submission ID (alphanumeric)
  - "Successfully Submitted" status
- Submission receipt stored in student's assignment history permanently
- Prevents disputes: "I submitted but it didn't register"
- Student can show submission receipt to teacher as proof

---

## 43. Late Submission Policy (Per Assignment)

Configurable options:

| Policy | Description |
|---|---|
| Hard Close | Submission blocked at deadline; no exceptions |
| Grace Period | Extra N hours after deadline; no marks penalty |
| Late with Penalty | Accepted; Y% deduction per day late |
| Open | Always accepted; teacher decides penalty manually |

- Default: Hard Close for timed/in-class; Grace Period (24 hours) for regular homework
- Late submission tagged in submission record
- Late penalty auto-applied to final score if percentage deduction policy selected

---

## 44. Re-Submission

- Teacher enables re-submission per assignment (configurable: unlimited attempts or up to N attempts)
- Student resubmits; latest submission is the graded version
- All previous submissions archived; teacher can view history of attempts (tracks effort improvement)
- Re-submission window: open until assignment deadline (or extended deadline if teacher allows)
- Useful for: formative practice, assignments where feedback loop is part of learning

---

## 45. Assignment Exemption

- Student with medical certificate or documented special circumstances exempted from a specific assignment
- Exemption granted by: class teacher (practice), HOD (formative), Principal (high-stakes)
- Exemption logged: student, assignment, reason, approved by, date
- Marks calculation: exempt assignments excluded from student's internal average
- Parent notified of exemption (school level)
- CWSN students (Point 70): broader exemption and alternative assessment framework

---

## 46. Auto-Grading (Objective Types)

Immediately on submission, system auto-grades:
- MCQ (single/multiple correct)
- True/False
- Fill in the blank (exact/keyword match)
- Match the following
- Numerical (within tolerance + unit check)
- Integer type
- Assertion-Reason
- Statement-based
- Matrix match
- Code (output match)

Auto-graded score held internally; **not shown to student until teacher publishes results** (prevents cheating if some students submit before others).

---

## 47. Tolerance Range for Numerical Answers

- Teacher sets:
  - Expected value: e.g., 9.81
  - Tolerance: ± 0.05 (absolute) or ± 0.5% (relative — teacher selects)
  - Required units: m/s² (mandatory correct unit for full marks)
  - Significant figures: optional — answer must have exactly 3 significant figures
- Within tolerance + correct unit = full marks
- Within tolerance + wrong unit = configurable partial marks
- Outside tolerance = zero
- Calculation shown to teacher in grading view: student's value, expected range, pass/fail

---

## 48. Manual Grading for Subjective Questions

- Teacher opens grading interface for one assignment
- Two grading modes:
  1. **Student-by-student**: see all questions for Student A, then Student B
  2. **Question-by-question**: see all students' answers to Q1, then Q2 (recommended for consistency)
- For each answer: teacher reads, types marks (0 to max), types feedback
- Teacher can also use annotation (Point 88) for inline comments
- Partial marks awarded by typing exact number (not forced to round)
- Save and continue: teacher's progress auto-saved; can resume grading later

---

## 49. Rubric-Based Grading

- Teacher creates scoring rubric at assignment creation:
  - Criterion 1: Content accuracy (0–4 marks)
  - Criterion 2: Explanation clarity (0–3 marks)
  - Criterion 3: Examples given (0–2 marks)
  - Criterion 4: Language and grammar (0–1 mark)
  - Total: 10 marks
- During grading: teacher rates each criterion; total auto-calculated
- Rubric shown to students after results published (transparency; teaches students what is valued)
- Pre-built rubric templates: Essay, Project, Lab Report, Creative Writing, Code Review

---

## 50. Partial Marks

- Question-level partial marking: teacher awards any value from 0 to question's max marks
- For fill-in-blank: partial marks per blank (auto-calculated: 1 mark per correct blank)
- For code: partial marks based on how many test cases pass vs total test cases
- For peer review: weighted average may result in fractional marks (rounded per institution config)
- Marks rounding rule (institution config): round half up, round to nearest, truncate

---

## 51. Class-Level Side-by-Side Grading View

- Teacher selects Question 3 → sees all students' answers to Q3 in a scrollable list
- Each entry shows: student name, their answer, marks field, feedback field
- Benefits:
  - Faster than switching between students
  - Consistency: grades all responses to same question with same standard
  - Identifies common misconceptions visually (many students with same wrong answer)
- Teacher can switch to student-by-student view anytime

---

## 52. HOD Moderation

- HOD can review and adjust any teacher's grading for high-stakes assignments
- Moderation workflow:
  - HOD opens assignment → selects specific students or all
  - Reviews original marks + teacher feedback
  - Adjusts marks with mandatory reason
  - Moderated score replaces original in results
- Both original and moderated marks stored with timestamps
- Moderation audit report: list of all moderated assignments, who moderated, original vs final marks, reason
- Available to Principal for academic integrity oversight

---

## 53. Teacher Inline Annotation

- For manually graded text answers: teacher highlights a specific sentence or phrase
- Attaches inline comment to highlighted text (e.g., "This formula is incorrect", "Strong argument here")
- Multiple annotations per answer allowed
- Student sees annotated version when results published: highlighted text + bubbled comments
- Not just overall feedback at the bottom — specific, precise, point-of-error feedback
- Improves learning: student understands exactly where they went right/wrong

---

## 54. Student Self-Assessment

- Before teacher grades: student rates their own answer using the same rubric
- Student inputs self-score + one-line justification per question or rubric criterion
- Teacher sees side-by-side: student self-score vs teacher's actual score
- Gap analysis:
  - Overconfident students (self-score >> teacher score): counsellor alert
  - Underconfident students (self-score << teacher score): encouragement note
- Used in NEP 2020-aligned formative assessment; develops metacognitive skills
- Self-assessment data shared with counsellor (Module 32) for academic support planning

---

## 55. CBSE Homework Load Guidelines Compliance

Per CBSE/NCF 2005/Ministry of Education guidelines on homework:

| Class | Maximum Daily Written Homework |
|---|---|
| Classes 1–2 | No written homework |
| Classes 3–5 | Up to 2 hours combined per day |
| Classes 6–8 | Up to 2.5 hours combined per day |
| Classes 9–10 | Up to 3 hours combined per day |
| Classes 11–12 | Teacher-judged (no strict limit, but manageable) |

- Teacher inputs estimated completion time when creating assignment
- System calculates combined daily load across all subjects for that class
- If load exceeds guideline: warning to the teacher publishing the last assignment that day (advisory, not hard block)
- Historical load calendar: teacher sees previous week's daily load for their class

---

## 56. No Homework Hard Block — Classes 1–2

- Assignment creation blocked for Classes 1–2 by default
- Teacher who attempts to create a submitted-work assignment for Class 1 or 2 sees:
  - "CBSE/NCF guidelines prohibit written homework for Classes 1–2. Use Activity Cards (Point 84) for home engagement."
- Override possible with Principal approval + reason (e.g., special holiday reading activity)
- Configurable per institution: some schools may apply this restriction to Classes 1–3 (stricter state policies)

---

## 57. State Board Homework Policies

State-specific homework restrictions loaded at institution onboarding:

| State / Board | Policy |
|---|---|
| Delhi (DoE) | No homework Classes 1–2; reduced load Classes 3–5 |
| Maharashtra (SSC) | State circular on homework limits per class |
| Tamil Nadu | State Board circular on homework load |
| Rajasthan | Education department guidelines |
| Kerala | State-specific norms (generally strict on overloading) |

- System applies applicable state policy on top of CBSE defaults
- Custom override by Principal for institution-specific decisions (logged)

---

## 58. CCE / Continuous Assessment Marks Integration

- CBSE internal assessment (20 marks per subject):
  - Graded assignments automatically contribute marks
  - Contribution configurable per subject by class teacher/HOD:
    - Periodic Test 1: 5 marks
    - Periodic Test 2: 5 marks
    - Assignment/Portfolio: 5 marks
    - Subject Enrichment: 5 marks
- Running internal score per student per subject visible to teacher in real-time
- Auto-fed to Module 21 Results at term end
- State board internal assessment: configurable with state-specific marks distribution

---

## 59. NCERT Exercise Templates

- Standard NCERT exercise questions imported into Module 17 Question Bank (tagged by Class, Subject, Chapter, Exercise number)
- Teacher assigns NCERT back exercises directly without retyping
- Question bank tagged with NCERT chapter reference: e.g., "NCERT Class 10 Science – Chapter 4 – Q3"
- Teacher customises NCERT questions before assigning (modify numbers, change context)
- Covers: all CBSE subjects Classes 1–12
- State board textbook exercises: importable similarly (state-specific tagging)

---

## 60. Bloom's Taxonomy Level Tagging

- Teacher tags each question with Bloom's cognitive level:
  1. **Remember** — recall facts, definitions
  2. **Understand** — explain, summarise, classify
  3. **Apply** — use knowledge in new situation
  4. **Analyse** — break down, compare, differentiate
  5. **Evaluate** — judge, critique, justify
  6. **Create** — design, construct, produce

- NEP 2020 and NCERT guidelines emphasise Higher Order Thinking Skills (HOTS — levels 4–6)
- Assignment analytics show distribution across Bloom's levels
- Principal / HOD dashboard: school-wide HOTS vs lower-order question ratio per subject
- Identifies if teaching is over-focused on rote recall vs critical thinking

---

## 61. Assignment Difficulty Tagging

- Teacher marks each assignment (and each question) as: Easy / Medium / Hard
- Assignment-level difficulty shown in HOD view
- Analytics breakdown:
  - Class average score on Easy vs Medium vs Hard assignments
  - Student-level performance by difficulty
- Ensures balanced assessment (not all easy, not all hard)
- Coaching batches: JEE/NEET assignments tagged as Easy / JEE Mains Level / JEE Advanced Level

---

## 62. NIPUN Bharat / FLN Activity Tracking

- Foundational Literacy & Numeracy Mission (Ministry of Education):
  - Classes 1–3 competency-based activities
  - Oral reading fluency check, number recognition, basic arithmetic
  - Activities done at home with parent participation
- In EduForge: parent marks activity completed in-app
- No student written submission; no formal grading
- Teacher sees class-level completion rate
- Student competency flags: Achieved Basic Literacy / In Progress / Not Yet (per NIPUN Bharat learning outcomes framework)
- State FLN dashboard export: system generates state-prescribed format for NIPUN Bharat data submission

---

## 63. Parent Engagement Activity Cards (Classes 1–2)

- Instead of written homework: teacher creates structured activity suggestions
- Examples:
  - "Count 10 objects at home and draw them"
  - "Read a story together for 10 minutes"
  - "Name 5 vegetables you see in the kitchen"
- Parent reads activity card in-app → does activity with child → taps "We did this today"
- Teacher sees class-level engagement (% of parents who acknowledged)
- No student submission; no grading; supports holistic development without pressure
- Aligned with RTE Act Section 29(2)(g): curriculum shall not cause fear, trauma, or anxiety

---

## 64. Word Count Guidance

- Teacher sets recommended word count range per long-answer question (e.g., 150–200 words)
- Student sees live word counter below text editor
- Colour indicator:
  - Green: within recommended range
  - Yellow: ±25% of range
  - Red: significantly over or under
- Student not blocked from submitting outside range; it is guidance, not a limit
- Builds answer-length discipline for board exams (CBSE board exam answer expectations are well-known: 1-mark = 1 line, 2-mark = 2–3 lines, 5-mark = 8–10 lines)

---

## 65. Assignment Conflict Detection

- When teacher publishes an assignment with a specific due date:
  - System checks: do other subjects already have assignments due the same day for this class?
  - If yes: warning shown: "[Subject 1] and [Subject 2] homework is also due on this day. Consider adjusting the due date to avoid overloading students."
- Advisory warning; teacher can proceed or change date
- Class teacher (who has overview of all subjects) sees weekly load calendar to co-ordinate
- HOD receives weekly load summary: days with high concentration of assignments

---

## 66. Daily Homework Load Calculator

- For each day, system calculates:
  - Total estimated completion time = sum of all subjects' assignment times due that day
  - Compared against CBSE class-level guideline (Point 55)
- Visual calendar: colour-coded days (green = within limit, yellow = approaching limit, red = exceeding limit)
- Last teacher publishing on a high-load day receives a specific warning with the total
- HOD sees monthly load distribution across all classes

---

## 67. Plagiarism Detection

- Submitted text answers (short and long answer) compared with all classmates' submissions for the same question using text similarity algorithm
- Similarity score calculated per student pair
- Threshold: flagged if > 80% similar (configurable)
- Teacher notified with: Student A vs Student B — [X]% similarity
- Teacher decides action (not auto-penalised by system)
- Actions available: teacher notes, reduce marks, escalate to HOD
- Cross-section detection: if same assignment published to multiple sections, cross-section comparison also runs

---

## 68. In-App Copy Block

- Text selection on question display is disabled (prevents copy-paste of question text)
- Text selection on other students' submissions is disabled
- Screenshot detection: if student attempts screenshot during timed assignment, in-app warning displayed: "Screenshots are not allowed during this assignment"
- Cannot prevent OS-level screenshots but logs attempt timestamps
- Logging used as evidence in integrity investigations

---

## 69. Submission Lock

- Once student submits: answers are locked; no modification permitted
- Re-submission only if teacher explicitly enables (Point 44)
- If student accidentally submits: within 5 minutes of submission, student can request "Undo Submit" (teacher approval required)
- Post-deadline: no undo option regardless of circumstances

---

## 70. Assignment for CWSN Students

- Differently-abled students receive modified assignment:
  - **Extra time**: configurable additional time (e.g., 25 minutes extra for 60-minute assignment; as per NCF Special Education norms)
  - **Simplified language**: teacher toggles "Plain Language Mode"; complex sentences simplified; technical jargon explained inline
  - **Alternative format**: instead of written long answer, student records voice response (captured via device microphone within app — not an uploaded file); teacher listens and grades
  - **Reduced question count**: teacher may assign a subset of questions for CWSN students
- CWSN modifications linked to student's IEP (Individualised Education Plan, Module 32)
- RTE Act 2009 and Rights of Persons with Disabilities Act 2016 compliance

---

## 71. Cross-Subject Integrated Assignment

- Teacher creates assignment tagged to multiple subjects (e.g., Environment Studies + Language; History + Social Science + Geography)
- Each subject teacher grades from their perspective:
  - History teacher: historical accuracy (5 marks)
  - Language teacher: expression and grammar (5 marks)
- Composite score auto-calculated from both evaluations
- Promotes NEP 2020's integrated / holistic learning approach
- Student sees individual subject scores + total composite score

---

## 72. Regional Language Input Support

- Student types answers in any Indian language using device's installed language keyboard
- Supported (Unicode-based): Hindi, Tamil, Telugu, Kannada, Bengali, Marathi, Gujarati, Malayalam, Odia, Punjabi, Assamese, Urdu (RTL supported)
- Assignment questions authored in regional language by teacher using the same method
- Teacher feedback also writable in regional language
- Critical for state board schools with regional medium of instruction
- Bilingual assignments: question in English + regional language; student answers in preferred language

---

## 73. Assignment Print-Friendly View (Low-Connectivity Students)

- For students without reliable internet access:
  - Teacher generates print-friendly HTML view of the assignment (rendered in browser)
  - Printed and physically distributed
- Student submits on paper; teacher evaluates paper
- Teacher manually enters marks per question on behalf of the student in the platform
- Record tagged as "Offline Submission — Paper" with teacher's entry timestamp
- Student's offline submissions count toward internal assessment same as online submissions
- Common in rural schools, border areas, areas with frequent power outages

---

## 74. Negative Marking Student Warning System

- Before student finalises submission of a negatively marked assignment:
  - System displays: "You have [N] unattempted questions. Attempting may risk negative marks. Do you want to review before submitting?"
  - Student sees: Questions Attempted: [X] / Total: [Y] / Estimated Score: [Z] (with current negatives factored)
- When changing an already-answered MCQ:
  - Warning: "You are changing your answer. This may result in negative marks if your new answer is wrong. Confirm change?"
- Teaches students to apply exam strategy (leave vs attempt) — mirrors actual JEE/NEET exam experience

---

## 75. Student Effort Time Tracking

- System records: time from first open to submission for each assignment
- Analytics available to teacher (not shown to students):
  - Very short time + high score: possible integrity concern; teacher investigates
  - Very long time + low score: student struggling with topic; counsellor alert
  - Average effort time per student per subject over term: engagement indicator
- Effort time report per class: average time spent on assignments by subject; subject with very low average time may need attention

---

## 76. Assignment Streak — Motivation

- Student submits all assignments on time for X consecutive weeks (configurable: default 4 weeks):
  - In-app achievement badge displayed: "4-Week Perfect Submission Streak!"
  - Parent notified (school level): "Congratulations! [Student] has submitted all assignments on time for 4 weeks."
- Streak counter resets on first missed/late submission
- Personal best streak tracked and visible on student's profile
- Particularly effective for primary and middle school students; gamifies responsibility

---

## 77. Subject-Wise Pending Assignments Counter

- On student home screen (dashboard):
  - Each subject shown with a pending assignment badge count
  - Colour urgency coding:
    - Green badge: due 3+ days away
    - Yellow badge: due in 1–2 days
    - Red badge: due today or overdue
- Immediate visual priority guide; student knows which subject needs attention first
- Separate view: full pending list sorted by due date/time (earliest first)

---

## 78. Parent Homework Visibility (School Level)

- Parent sees (school-level students only; per Module 09 access rules):
  - Child's all pending assignments with subject and due date
  - Submitted assignments with status
  - Graded assignments with score and teacher feedback (after published)
- Cannot see other students' assignments (privacy — DPDPA 2023)
- Separate parent view from student view; both show same data but with different interaction options

---

## 79. Parent Acknowledgement

- Parent in-app button: "I have seen this homework" per assignment
- Digital equivalent of parent signature in physical homework diary
- Teacher dashboard shows acknowledgement status per student: Acknowledged / Not Acknowledged
- Unacknowledged by parent after 24 hours: optional reminder to parent (configurable)
- Used in parent-teacher discussions: "You acknowledged seeing this assignment on [date]"
- Builds parent-school communication loop without requiring meetings

---

## 80. Homework Diary Digital View

- Student's daily view on app:
  - Today's assignments by subject (colour-coded by subject)
  - Status per assignment: Pending / Submitted / Graded
  - Due time shown
  - Tomorrow's assignments preview
- Parent sees same view for their child
- Replaces physical homework diary entirely
- Weekly view also available: all subjects' assignments in a 7-day grid

---

## 81. Missed Assignment Alert

- Student who has not submitted:
  - 24 hours before deadline: in-app reminder to student
  - At deadline (if not submitted): "You have missed [Assignment]. Contact your teacher."
  - Parent notified (school) 48 hours after deadline if still not submitted
- Consecutive missed assignments in same subject (3+ in a term): counsellor (Module 32) flagged
- Teacher's non-submission list: updated in real-time; visible in teacher's assignment dashboard

---

## 82. Overdue Grading Alert

- Teacher not graded within:
  - 5 days after deadline: in-app reminder to teacher
  - 10 days: HOD alert
  - 15 days: Principal alert; listed in academic quality report
- Ungraded assignments affect student's internal marks calculation (system shows "Pending Teacher Grading" in student's marks view)
- Principal's overdue grading report: per teacher per subject; monthly academic quality metric

---

## 83. Plagiarism Report to HOD

- End of each month: HOD receives summary of plagiarism flags across department:
  - Assignment name, subject, class, number of flagged student pairs
  - Highest similarity cases listed (teacher action taken or pending)
- Used for: academic integrity monitoring, identifying classes with copying culture
- Serious cases (same assignment, 95%+ similarity, multiple students): referred to Principal for inquiry

---

## 84. Assignment Completion Rate — HOD / Principal View

- Per subject per class per week: % of students who submitted on time
- Visualised as heat map: subject × class × week
- Low completion rate (< 60%) flagged in red: possible issues (difficult assignment, topic confusion, teacher communication gap, student disengagement)
- Principal sees school-wide completion rate trends over the term

---

## 85. Student Assignment Performance Trend

- Per student per subject: assignment scores over the term plotted as trend line
- Improving / Stable / Declining trend identified automatically
- Visible to: subject teacher, class teacher, counsellor (Module 32), parent (school level)
- Declining trend over 3 consecutive assignments: counsellor flag; parent notification

---

## 86. Question-Level Difficulty Analysis

- Per question across all submissions:
  - Percentage of students who answered correctly
  - Too-easy questions (> 90% correct): flag for teacher (consider using harder questions next time)
  - Too-hard questions (< 20% correct): flag (topic needs re-teaching or question was ambiguous)
- Teacher sees per-question performance summary in grading view
- Feeds Module 17 Question Bank: question difficulty auto-tagged based on historical performance data
- HOD uses this data for curriculum and question quality review

---

## 87. Low-Performing Student Flag

- Student with average assignment score < 40% in any subject over 4 consecutive assignments:
  - Flagged to class teacher and counsellor (Module 32) in-app
  - Alert includes: subject, last 4 scores, specific questions consistently wrong
- Counsellor creates intervention plan (Module 32 remedial support)
- Also triggers: remedial class scheduling (Module 10 Point 32)
- Parent notified (school level) after counsellor has been assigned (not immediately — avoids panic)

---

## 88. Assignment vs Attendance Correlation

- Per student per subject: cross-reference assignment completion rate with attendance %
- Patterns flagged to counsellor:
  - Low attendance + high missed assignments = highest dropout/disengagement risk
  - High attendance + high missed assignments = engagement issue (in class but not completing work)
  - Low attendance + high assignment completion = student self-studying well despite absences
- Correlation report generated weekly for counsellor dashboard

---

## 89. Assignment Template / Bank

- Teacher saves any assignment as a reusable template
- Template library per subject and class level
- Searchable by: subject, class, topic, assignment type, difficulty
- Sharable with colleagues in same institution (teacher grants sharing permission)
- Assignment rollover: at new academic year start, teacher copies previous year's assignment templates; updates dates, topic links, and minor modifications; reuses question sets without re-entry

---

## 90. Multiple Evaluators

- For large classes or fairness concerns: same assignment graded by two teachers independently
- Each teacher grades without seeing the other's scores
- Discrepancy check: if scores differ by > configured threshold (e.g., > 20% of total marks): flagged
- HOD receives discrepancy notification; adjudicates and sets final score
- Final score = average (if no discrepancy) or HOD-adjudicated (if discrepancy)
- Particularly useful for: Language subject long answers, project work, essay assignments

---

## 91. Assignment Analytics Export

- Teacher / HOD exports for parent-teacher meetings, report card preparation, academic reviews:
  - **PDF**: class-wise average scores, individual student score list, question-wise performance
  - **CSV**: full raw data (student, question, score, timestamp) for external analysis
- NAAC documentation: assignment completion rates and average scores exported in NAAC format
- State board internal assessment report: marks compiled and exported per board-prescribed format
- Accessible to: subject teacher, HOD, Principal

---

## 92. Scheduled Assignment Announcement Link (Period Diary)

- When teacher marks a period diary entry (Module 10/11 linkage): "Assigned homework — [Assignment Name]"
- Assignment pushed to students simultaneously from period diary entry
- Ensures academic record (period diary) and student notification are in sync
- Teacher does not need to manually notify separately; diary entry triggers notification

---

## 93. Student Assignment History

- Per student: all assignments across all subjects
- Searchable/filterable by: subject, date range, status (submitted/missed/graded), score range
- Long-term history: accessible for previous terms and years (read-only after term close)
- Used by counsellor for academic trend analysis over student's entire school/college career
- TC record: assignment history archived with student's academic record (Module 07)

---

## 94. Assignment for Coaching — UPSC / CA Pattern

- Long-form essay assignments (1,000+ words) for UPSC Mains, Law entrance, CA Final:
  - Rich text editor with word count (Point 64)
  - Rubric: Introduction, Arguments, Examples, Counter-arguments, Conclusion, Language
  - Teacher evaluates holistically using rubric
- Précis writing: student reads a passage (displayed in app); writes a précis within a word limit
- Comprehension passage with analytical questions: Paragraph-based (Point 16)
- Current affairs based: teacher types current affairs scenario; student answers application-based questions

---

## 95. Viva-Voce Linked to Lab Record

- After student submits digital lab record (Point 20):
  - Teacher generates viva questions specifically about that student's submitted lab record
  - Viva preparation assignment (Point 22) pre-populated with questions based on student's observations
  - Teacher marks discrepancies: "Your observations show X but your conclusion says Y — explain"
- Builds higher-order understanding of practical work
- Contributes to CBSE internal practical assessment alongside lab record marks

---

## 96. Principal Academic Quality Dashboard

- School-wide assignment analytics:
  - Subject-wise average assignment score (all classes combined)
  - Classes with consistently low scores (< 50% average)
  - Teachers with consistently overdue grading (> 10 days ungraded)
  - Holiday homework submission rates
  - Assignment completion rates by class and subject
  - HOTS vs lower-order question ratio (Bloom's tagging data)
- Monthly academic quality report auto-generated for Principal
- Used for: faculty meetings, academic calendar adjustments, teacher support decisions

---

## 97. Assignment-Level DPDPA 2023 Compliance

- Student's assignment responses are personal data under DPDPA 2023
- Data retention: 3 years after student leaves institution (configurable per institution policy)
- Access controls: subject teacher, class teacher, HOD (for moderation), Principal (for oversight), student (own data), parent (school level — child's data only)
- No third-party sharing without consent
- Data portability: student can request export of their assignment history in structured format
- Purge: after retention period, data auto-purged; purge log maintained

---

## 98. Assignment Notification Do-Not-Disturb

- Student/parent can set quiet hours for notifications (e.g., 10 PM – 7 AM)
- Assignment notifications (new assignment, reminder, results published) queued and delivered at quiet hours end
- Assignment still visible in app at any time; only notification delivery is deferred
- Exam night DND: student can set DND for a specific night; all notifications held until morning
- DPDPA 2023 aligned: user controls over their own communication preferences

---

## 99. Homework Completion % in Report Card

- CBSE internal assessment and state board assessments require portfolio/homework completion as part of internal marks
- System calculates per student per subject per term:
  - Total assignments assigned: [N]
  - Assignments submitted: [M]
  - Completion percentage: M/N × 100
  - Average score across submitted assignments
- Both data points (completion % and average score) fed to Module 21 Results for report card
- Report card shows: "Assignment Completion: [%] | Average Score: [X/Y]"

---

## 100. Lab Record Contribution to CBSE Practical Assessment

- CBSE Classes 11–12 Science practical assessment (30 marks per subject):
  - Lab Record (digital lab record book — Point 20): typically 5–8 marks
  - Viva-voce: typically 5 marks
  - Actual practical examination: remaining marks
- System tracks: number of experiments completed, lab record marks per experiment
- Cumulative lab record marks calculated at term end
- Auto-fed to Module 21 Results for practical marks compilation
- CBSE school-conducted practical examination marks submitted to CBSE via system export (school's own practical marks, not board-conducted)

---

## DB Schema (Core Tables)

```
institution.assignments
  id, tenant_id, branch_id, subject_id, class_id, section_ids (array),
  batch_id, created_by_teacher_id, title, description, instructions,
  assignment_type (practice/formative/holiday/project/group/differential/
  peer_review/timed/in_class/lab_record/viva_prep/activity_card/fln),
  available_from, due_at, grace_period_minutes,
  late_policy (hard_close/grace/penalty/open), penalty_pct_per_day,
  total_marks, estimated_minutes, difficulty (easy/medium/hard),
  allow_resubmission (bool), max_attempts, is_randomised (bool),
  is_timed (bool), time_limit_minutes, negative_marking_config (JSON),
  scheduled_publish_at, status (draft/scheduled/published/closed/archived),
  version_number, syllabus_topic_ids (array), bloom_level (array),
  language (en/hi/ta/te/ka/...), is_individual (bool),
  prerequisite_assignment_id, created_at

institution.assignment_questions
  id, assignment_id, question_number, question_type
  (mcq_single/mcq_multiple/fill_blank/true_false/match/short_answer/
  long_answer/numerical/equation/chemical/sketch/code/integer/
  assertion_reason/paragraph/matrix_match/statement),
  question_body (JSON — supports text + math + image ref),
  options (JSON array), correct_answer (JSON),
  tolerance_value, tolerance_type (absolute/relative), required_unit,
  sig_figs_required, marks, negative_marks, partial_marks_config (JSON),
  difficulty (easy/medium/hard), bloom_level,
  rubric (JSON — criteria + marks), recommended_minutes,
  word_count_min, word_count_max, camera_capture_allowed (bool),
  code_language, expected_output, created_at

institution.assignment_submissions
  id, assignment_id, student_id, group_id,
  started_at, submitted_at, submission_method (online/offline_paper),
  attempt_number, is_late (bool), late_by_minutes,
  auto_score (decimal), manual_score (decimal), final_score (decimal),
  graded_by_teacher_id, graded_at, moderated_by_hod_id,
  moderated_score, moderation_reason, results_published_at,
  self_assessment_score (decimal), self_assessment_note,
  time_spent_seconds, plagiarism_flag (bool), plagiarism_score (decimal),
  submission_receipt_id, status
  (draft/submitted/graded/results_published/exempted)

institution.submission_answers
  id, submission_id, question_id, response_data (JSON — type-specific),
  auto_score (decimal), manual_score (decimal), partial_score (decimal),
  teacher_feedback (text), teacher_annotations (JSON — highlight + comment),
  is_correct (bool), attempt_number, time_spent_seconds

institution.assignment_groups
  id, assignment_id, group_name, member_student_ids (array),
  formed_by (teacher/self_select), leader_student_id,
  contribution_log (JSON — student_id: sections_contributed)

institution.peer_review_allocations
  id, assignment_id, reviewer_student_id, reviewee_student_id,
  reviewer_score, reviewer_feedback, reviewed_at

institution.assignment_templates
  id, tenant_id, created_by_teacher_id, template_name, subject_id,
  class_level, assignment_type, question_count, total_marks,
  is_shared (bool), academic_year_ref, created_at

institution.parent_acknowledgements
  id, assignment_id, student_id, parent_id, acknowledged_at

institution.plagiarism_flags
  id, assignment_id, question_id, student_a_id, student_b_id,
  similarity_score (decimal), flagged_at, teacher_action_taken,
  hod_notified (bool), status (pending/reviewed/escalated/dismissed)

institution.lab_records
  id, assignment_id, student_id, experiment_name, subject_id,
  section_scores (JSON — section: marks), total_marks,
  viva_marks, practical_exam_marks, final_practical_marks,
  teacher_id, graded_at

institution.fln_activity_completions
  id, tenant_id, student_id, activity_card_id, completed_by_parent_id,
  completion_date, competency_tag, status (achieved/in_progress/not_yet)
```

---

## Integration Map

| Module | How |
|---|---|
| 05 — Academic Year & Calendar | Holiday homework tied to vacation dates; assignment due dates within working days |
| 07 — Student Enrolment | Student roster; CWSN flag for modified assignments; class/section assignment |
| 08 — Staff Management | Teacher assignment (who created, who grades); HOD moderation |
| 10 — Timetable & Scheduling | Period diary links to assignment announcement; in-class timed assignments during specific periods |
| 11 — Attendance School/College | Attendance cross-reference for missed assignments correlation |
| 12 — Attendance Coaching | Batch assignment linkage; coaching-specific question types |
| 15 — Syllabus & Curriculum Builder | Assignment linked to syllabus topic; coverage tracking |
| 17 — Question Bank & MCQ | Questions pulled from and saved to question bank |
| 21 — Results & Report Cards | Assignment marks auto-fed to internal assessment; homework completion % on report card |
| 22 — Test Series & Mock Tests | Coaching pattern assignments (JEE/NEET types) share question type engine |
| 25 — Fee Collection | Assignment fine for persistent non-submission (optional institutional config) |
| 32 — Counselling | Low-performing student flag; CWSN IEP; effort analytics; attendance correlation |
| 35 — Notifications | New assignment, reminders, results published — all in-app only |
| 45 — Live Classes | Follow-up assignments linked to live class recordings |
| 47 — AI Performance Analytics | Assignment performance trends feed AI analytics engine |
