# Module 18 — Exam Paper Builder

## Purpose
Provide a fully automated and manual exam paper construction system for EduForge.
Teachers can generate board-compliant, syllabus-weighted, Bloom's-balanced question
papers in minutes using Auto mode, or hand-pick every question in Manual mode, or
combine both in Hybrid mode. Papers are stored as structured JSON on CDN, delivered
securely to Module 19 (Exam Session & Proctoring), and analysed post-exam for quality
improvement. Every Indian board pattern, competitive exam pattern, and college assessment
format is pre-loaded as a template.

---

## 1. Paper Builder Modes

### 1.1 Three Modes

| Mode | Description | Best For |
|---|---|---|
| **Auto** | System generates complete paper from rules | Routine unit tests, periodic tests, quick mock tests |
| **Manual** | Teacher hand-picks every question | Board-pattern pre-boards, carefully curated papers |
| **Hybrid** | Teacher locks certain questions; auto fills remaining slots | Mid-terms, semester papers with specific required questions |

### 1.2 Auto Mode Engine
- Reads syllabus unit-wise marks weightage from Module 15
- Queries Module 17 CDN manifest for available questions per topic/type
- Applies configured rules: Bloom's targets, difficulty targets, type distribution, PYQ ratio, repeat prevention
- Generates complete paper in one click
- Shows predicted difficulty score and expected average before publishing
- "Regenerate" button: discards current selection, generates new one meeting same rules
- "Lock & Regenerate": teacher locks questions to keep → auto fills only unlocked slots

### 1.3 Manual Mode
- Teacher browses question bank: Board → Subject → Grade → Unit → Chapter → Topic → Sub-topic
- Filter by: type / difficulty / Bloom's / exam tag / PYQ year / marks / never-used
- Selects question → added to paper in real time
- Running totals shown: marks added / marks remaining / Bloom's distribution / difficulty balance
- Drag-and-drop to reorder questions within sections

### 1.4 Hybrid Mode
- Teacher starts with Auto generation
- Replaces specific questions manually (right-click → "Replace this question")
- Locks replacements; regenerate fills only unfilled slots
- Full audit: which questions were auto-selected vs teacher-selected

### 1.5 CDN-Driven Topic Availability
- Paper builder reads CDN manifest per subject / grade / topic / question type
- Topic selector shows only topics with available questions of the selected type
- Greyed-out topics = no questions available for that type → links to Module 17 gap report
- Availability count shown per topic: "Electric Field — MCQ: 24 questions available"
- Real-time update: as new questions are added to Module 17, CDN manifest refreshes; paper builder reflects immediately

---

## 2. Exam Types Supported

### 2.1 School Exam Types

| Exam Type | Scope | Marks | Duration |
|---|---|---|---|
| Surprise / Class Test | 1–2 topics | 10–20 | 15–30 min |
| Unit Test | 1–2 chapters | 25–30 | 45 min |
| Periodic Test (CBSE CCE) | 1 chapter | 25 | 45 min |
| Mid-Term / Half-Yearly | 5–8 chapters (Term 1) | 80 | 3 hrs |
| Annual / Final Exam | Full syllabus | 80/100 | 3 hrs |
| Pre-Board 1 | Full syllabus, board pattern | 80 | 3 hrs |
| Pre-Board 2 | Full syllabus, board pattern (no repeat from Pre-Board 1) | 80 | 3 hrs |
| Practical Exam | Lab experiments + viva | 30 | 2–3 hrs |
| Remedial Test | Foundation level only | 25–50 | 1–2 hrs |
| Supplementary / Compartment | Only failed topics | 80 | 3 hrs |
| Scholarship / Entrance | Custom scope | Custom | Custom |
| Olympiad Practice | NSO/IMO/NTSE/KVPY pattern | Custom | Custom |
| CWSN Adapted Test | Modified from standard | Same | Extended |

### 2.2 College / Higher Education Exam Types

| Exam Type | Scope | Marks | Pattern |
|---|---|---|---|
| Sessional / Internal Assessment | 2–4 units | 20–30 | University-prescribed |
| Mid-Semester Exam | Half syllabus | 30–50 | University-prescribed |
| Semester End Exam (SEE) | Full course syllabus | 60–80 | University-prescribed |
| Practical / Lab Exam | Lab work + viva | 25–50 | Department-specific |
| Project Viva | Project defence | 25–100 | Rubric-based |
| Open Book Exam | Full syllabus, HOTS only | 50–100 | L3–L6 Bloom's enforced |
| Take-Home Assessment | Extended deadline | 25–50 | Application/analysis |

### 2.3 Coaching / Competitive Exam Types

| Exam Type | Pattern | Duration |
|---|---|---|
| JEE Main Mock | 3 sections × 25 Qs | 3 hrs |
| JEE Advanced Mock | Paper 1 + Paper 2 | 3+3 hrs |
| NEET UG Mock | 4 sections × 45 Qs | 3 hrs 20 min |
| UPSC Prelims Mock | GS1 + CSAT | 2+2 hrs |
| SSC CGL / CHSL Mock | Tier 1 + Tier 2 | Custom |
| Banking Mock (IBPS/SBI) | Prelims / Mains | Custom |
| State PSC Mock | State-specific pattern | Custom |
| Weekly / Biweekly Test | Custom chapter scope | 1–2 hrs |
| Crash Course Test | Rapid revision scope | 30–60 min |
| Chapter-wise Mini Test | Single chapter | 20–30 min |
| Grand Test / Full Syllabus Test | Complete course | 3 hrs |

---

## 3. Paper Structure & Sections

### 3.1 Multi-Section Configuration

Each section independently configured:

```
Section A — Objective Questions
  Type:            MCQ_SINGLE
  Questions:       20
  Marks each:      1
  Negative marks:  0
  Attempt rule:    ALL_COMPULSORY

Section B — Very Short Answer
  Type:            SHORT_ANSWER
  Questions:       6
  Marks each:      2
  Attempt rule:    ALL_COMPULSORY

Section C — Short Answer
  Type:            SHORT_ANSWER / CASE_STUDY
  Questions:       7
  Marks each:      3
  Attempt rule:    ALL_COMPULSORY

Section D — Long Answer (Internal Choice)
  Type:            LONG_ANSWER
  Questions:       3 (each with internal choice: OR)
  Marks each:      5
  Attempt rule:    ALL_COMPULSORY (one of two choices)

Section E — Case Study / Source Based
  Type:            CASE_STUDY
  Questions:       3 sets (4 marks each)
  Attempt rule:    ALL_COMPULSORY
```

### 3.2 Attempt Rules Per Section

| Rule | Description | Used In |
|---|---|---|
| ALL_COMPULSORY | All questions must be attempted | Most sections |
| ATTEMPT_ANY_N_OF_M | Choose N from M available | CBSE long-answer choice, NEET Section B |
| INTERNAL_CHOICE | Q5a OR Q5b (not both) | CBSE 3/5-mark questions |
| OPTIONAL_SECTION | Entire section optional | College elective papers |

### 3.3 Internal Choice Builder
- Teacher creates both versions of a question (Q5a and Q5b)
- System labels as "OR" between them in paper
- Both share the same marks; answer key has separate entries for each
- Both are from the same topic at the same difficulty level (enforced by builder)

### 3.4 Sub-Part Questions
- Q5(a), Q5(b), Q5(c) under one question number
- Each sub-part: independently marked, can be different types
- Example: Q5(a) = 1 mark definition; Q5(b) = 2 marks explanation; Q5(c) = 2 marks numerical
- Carry-forward dependency: teacher flags if part (c) depends on answer from part (b); shown in examiner copy

### 3.5 Total Marks Guard
- Running total always shown in builder UI
- Cannot publish if total marks ≠ configured target
- Section-wise and overall validation before each save

---

## 4. Board Pattern Templates

### 4.1 CBSE School Templates (Pre-loaded)

**Class 10 (2024–25 pattern):**

| Section | Type | Count | Marks Each | Total |
|---|---|---|---|---|
| A | MCQ + Assertion-Reason | 20 | 1 | 20 |
| B | Very Short Answer | 6 | 2 | 12 |
| C | Short Answer | 7 | 3 | 21 |
| D | Long Answer (internal choice) | 3 | 5 | 15 |
| E | Case Study (4 sub-Qs each) | 3 | 4 | 12 |
| **Total** | | | | **80** |

Subject-specific patterns stored for: Maths, Science, Social Science, English,
Hindi, Sanskrit, Computer Science, IT, all CBSE vocational subjects.

**Class 12 per-subject templates:**
- Physics, Chemistry, Biology, Maths, Computer Science
- Accountancy, Business Studies, Economics
- History, Political Science, Geography, Sociology, Psychology
- English (Core + Elective), Hindi (Core + Elective)
- Physical Education, Fine Arts, Music

All patterns updated annually per CBSE SQP (Sample Question Paper) released each October.
Platform loads CBSE SQP within 48 hours of official release.

### 4.2 State Board Templates (All 28 States)

Each state board's pattern stored per subject per class:
- RBSE (Rajasthan): Classes 10 + 12 per subject
- UP Board (UPMSP): High School + Intermediate per subject
- MP Board (MPBSE): Classes 10 + 12 per subject
- Maharashtra Board (MSBSHSE): SSC + HSC per subject
- Karnataka (KSEEB / PUC): SSLC + PUC per subject
- Tamil Nadu (TNBSE): SSLC + HSC per subject
- AP Board / Telangana Board: SSC + Inter per subject
- Bihar Board (BSEB): Matric + Inter per subject
- West Bengal Board (WBBSE/WBCHSE): MP + HS per subject
- Gujarat Board (GSEB): SSC + HSC per subject
- All remaining 18 state boards: respective class/subject patterns

Update policy: state board pattern changes loaded within 7 working days of official notification.

### 4.3 ICSE / ISC Templates
- ICSE Class 10: all subjects per CISCE pattern
- ISC Class 12: all subjects including Literature papers

### 4.4 IB / IGCSE Templates
- IB DP SL/HL papers per subject
- IGCSE per subject (Paper 1 / Paper 2 / Paper 3 / Paper 4 as applicable)

### 4.5 Competitive Exam Pattern Templates

**JEE Main (NTA pattern 2024):**
```
Section A: 20 MCQ Single Correct  (+4 / −1)
Section B: 10 Numerical (attempt any 5, no negative)
Per subject: Physics / Chemistry / Mathematics
Total: 300 marks, 180 minutes
```

**JEE Advanced (IIT pattern):**
- Paper 1 + Paper 2; all question types per latest IIT pattern
- Complex partial marking per question type stored in template
- Updated per IIT announcement each year

**NEET UG (NTA pattern):**
```
Section A: Q1–35 compulsory (+4 / −1)
Section B: Q36–45, attempt any 10 (+4 / −1)
Subjects: Physics / Chemistry / Botany / Zoology
Total: 720 marks, 200 minutes
```

**UPSC CSE Prelims:**
```
GS Paper 1: 100 MCQ, +2 / −0.66, 120 min
CSAT Paper 2: 80 MCQ, qualifying 33%, +2.5 / −0.83, 120 min
```

**Banking (IBPS PO Prelims):**
```
English Language:      30 questions, 30 marks, 20 min
Quantitative Aptitude: 35 questions, 35 marks, 20 min
Reasoning Ability:     35 questions, 35 marks, 20 min
Total: 100 marks, 60 min (sectional time limits enforced)
```

**SSC CGL Tier 1:**
```
General Intelligence & Reasoning: 25 Qs, 50 marks
General Awareness:                 25 Qs, 50 marks
Quantitative Aptitude:             25 Qs, 50 marks
English Comprehension:             25 Qs, 50 marks
Total: 100 Qs, 200 marks, 60 min (+2 / −0.5)
```

**All 28 State PSC patterns:** stored individually per state.

### 4.6 College / University Templates
- University-affiliated: configurable per university + department
- Sessional: 2-hour, 30-mark template (common for most universities)
- Semester End: 3-hour, 80-mark template with question type mix
- Autonomous college: fully custom pattern saved as institution template
- CBCS pattern: internal (30 marks) + external (70 marks) split enforced

### 4.7 Custom Pattern Creation
- Institution creates own pattern → saved as reusable template
- Template library: browsable by exam type / board / subject
- Clone and modify existing template
- Share template across branches in same institution

---

## 5. Auto Paper Generation Rules

### 5.1 Syllabus Weightage Distribution
- Auto mode reads unit-wise marks weightage from Module 15 for the exam scope
- Distributes questions proportionally: Unit with 20% weightage → 20% of paper marks
- Fractional marks handled: rounds to nearest question boundary
- Teacher can override per-unit allocation after auto-generation

### 5.2 Coverage Check (Module 15 Integration)
- Auto mode queries Module 15 topic coverage log for the section
- Hard block mode: questions from uncovered topics completely excluded
- Advisory mode: uncovered topics flagged but teacher can include with override + reason
- Configurable per institution (Hard Block recommended for internal exams; Advisory for pre-boards)

### 5.3 Bloom's Taxonomy Distribution Targets

Teacher configures target % per paper type:

| Exam Type | L1–L2 (Recall) | L3 (Apply) | L4–L6 (HOTS) |
|---|---|---|---|
| Unit Test | 40% | 40% | 20% |
| Annual Exam | 30% | 40% | 30% |
| JEE/NEET Mock | 10% | 40% | 50% |
| Open Book | 0% | 20% | 80% |

Auto mode selects questions to match targets (±5% tolerance).
Visual pie chart shows Bloom's distribution of current paper in real time.

### 5.4 Difficulty Distribution Targets

Teacher sets target per paper:
- Easy % / Medium % / Hard % / Very Hard %
- Example Annual Exam: Easy 20% / Medium 50% / Hard 25% / Very Hard 5%
- Auto mode uses Module 17 item-analysis difficulty index (not just teacher-tagged difficulty)
- System uses system-calibrated p-value if available (30+ attempts); else uses teacher tag

### 5.5 Question Type Distribution
Teacher specifies per section: count of each question type.
Auto mode fills from question bank per type availability per topic.

### 5.6 PYQ Control
- Teacher sets: max PYQ % in paper (e.g., max 30%)
- Auto mode respects ceiling; fills rest with non-PYQ questions
- "PYQ Only" mode: for PYQ practice papers — 100% PYQ from specified year range

### 5.7 Repeat Prevention
- Auto mode checks paper bank (all institution's past papers for this subject/grade)
- Excludes questions used in last N papers (N configurable: 1–5; default: 3)
- Pre-Board 2: system ensures zero overlap with Pre-Board 1 automatically

### 5.8 Predicted Difficulty Score (Pre-Exam)
Before publishing, auto mode calculates:
- Expected average score %: weighted average of all questions' difficulty indices
- Grade distribution prediction: estimated % of students in each grade band
- Shown as: "Expected class average: 62% | Predicted distribution: A(15%) B(30%) C(35%) D(15%) E(5%)"
- If predicted average < 35% or > 80% → auto warning: "Paper may be too hard/easy"

### 5.9 Paper Quality Score
Composite score (0–100) calculated before publish:
- Syllabus weightage alignment (25%)
- Bloom's distribution vs target (20%)
- Difficulty balance vs target (20%)
- Repeat question % (< 5% is ideal) (15%)
- PYQ ratio within configured limit (10%)
- Questions with complete solutions/marking scheme (10%)

Green ≥ 80 | Yellow 60–79 | Red < 60 — cannot publish Red without HOD override.

---

## 6. Multi-Set Generation (Anti-Copying)

### 6.1 Question Order Shuffle (Sets A/B/C/D)
- Same questions, different order per set
- Section structure maintained (Section A questions stay in Section A)
- Within-section order randomised per set

### 6.2 Option Shuffle (MCQ)
- Options (A/B/C/D) reshuffled per set
- Correct answer tracked internally by option content, not label
- Answer key reflects reshuffled option labels per set

### 6.3 Parallel Question Sets (Different Questions Per Set)
- Questions drawn from Module 17 pools
- Set A gets pool_option_1, Set B gets pool_option_2, etc.
- All options from same pool: same topic, same type, same difficulty
- Truly different questions — not just reordered

### 6.4 Shift-Wise Papers (Coaching / Competitive)
- Multi-shift exams (morning/afternoon/evening): separate paper per shift
- All shifts drawn from same pool; zero question overlap between shifts
- Marks distribution identical across shifts
- Answer key separate per shift

### 6.5 Per-Student Unique Paper (High-Stakes)
- For high-stakes internal exams: each student gets unique question combination
- Questions drawn from large pool per marks slot
- System generates and stores answer key per roll number
- Module 20 auto-grading uses roll-number-specific answer key

### 6.6 Roll-Number-Based Set Assignment
- Linked to Module 19 seating plan
- Adjacent students (same row/column in hall) always assigned different sets
- Set assignment: alternating pattern per seating matrix

### 6.7 Watermarking
- **Set code watermark**: every page of printed/digital paper carries set code
- **Roll number watermark** (digital delivery): invisible metadata watermark in Module 19 student view carries roll number — identifies source if paper is photographed/leaked
- **QR code per copy**: unique QR linking to roll-number-specific answer key; examiner scans during evaluation to verify correct set

---

## 7. Paper JSON Architecture & CDN Storage

### 7.1 Unified Paper JSON Structure
```json
{
  "paper_id":       "uuid",
  "version":        1,
  "tenant_id":      "uuid",
  "branch_id":      "uuid",
  "exam_id":        "uuid",
  "set_code":       "A",
  "metadata": {
    "exam_type":        "ANNUAL_EXAM",
    "board_code":       "CBSE",
    "subject_code":     "PHYSICS",
    "grade":            "12",
    "academic_year_id": "uuid",
    "total_marks":      80,
    "duration_minutes": 180,
    "negative_marking": true,
    "language":         "en",
    "secondary_language": "hi",
    "is_bilingual":     true,
    "pattern_template": "CBSE_12_PHYSICS_2024",
    "quality_score":    87,
    "predicted_avg_pct": 62.4,
    "bloom_distribution": {"L1":10,"L2":20,"L3":30,"L4":25,"L5":10,"L6":5},
    "difficulty_distribution": {"EASY":20,"MEDIUM":50,"HARD":25,"VERY_HARD":5},
    "coverage_check_passed": true,
    "repeat_check_passed": true,
    "created_by":       "uuid",
    "approved_by":      "uuid",
    "locked_at":        "2025-03-01T08:00:00Z",
    "status":           "LOCKED"
  },
  "general_instructions": [
    {"lang": "en", "text": "All questions are compulsory."},
    {"lang": "hi", "text": "सभी प्रश्न अनिवार्य हैं।"}
  ],
  "sections": [
    {
      "section_id":     "sec-A",
      "label":          "Section A",
      "title":          {"en": "Multiple Choice Questions", "hi": "बहुविकल्पीय प्रश्न"},
      "type":           "MCQ_SINGLE",
      "marks_each":     1,
      "negative_marks": 0,
      "attempt_rule":   "ALL_COMPULSORY",
      "total_marks":    20,
      "questions": [
        {
          "sl_no":       1,
          "question_id": "uuid",
          "version":     2,
          "marks":       1,
          "is_internal_choice": false,
          "choice_pair_id": null
        }
      ]
    }
  ]
}
```

### 7.2 CDN Storage Structure
Paper JSON and supporting files stored on CDN — not in database:
```
CDN Path:
/papers/
  /{tenant_id}/
    /{academic_year}/
      /{exam_type}/
        /{subject_code}/
          /{grade}/
            /paper_{set}.json          ← time-locked (active at exam start)
            /answer_key_{set}.json     ← access: teacher/admin signed URL only
            /marking_scheme_{set}.json ← access: teacher/admin signed URL only
            /paper_{set}_print.pdf     ← cached PDF for print
            /paper_{set}_cwsn.pdf      ← large-print CWSN version
            /paper_{set}_bilingual.pdf ← bilingual print version
```

### 7.3 Time-Lock Mechanism
- Paper JSON CDN URL: restricted until exam start time
- At T=0 (exam start): CDN signed URL becomes active automatically
- Module 19 fetches paper JSON from CDN at T=0 and renders to students
- If paper leak detected: Admin invalidates CDN URL → emergency replacement generated

### 7.4 Answer Key & Marking Scheme CDN
- Answer key JSON: separate CDN file; only accessible via teacher/admin signed URL (never student)
- Marking scheme JSON: per-question rubric for descriptive questions; teacher/evaluator access only
- Both files cryptographically hashed at creation; hash stored in DB for tamper detection

---

## 8. Bilingual & Multilingual Papers

### 8.1 Bilingual Paper (English + Hindi / Regional)
- Question renders in: English + Hindi side by side (two-column layout) OR sequentially
- General instructions: English on top + Hindi below (or regional language)
- Options: bilingual per option
- Both languages sourced from question JSON `translations` field (Module 17)

### 8.2 Regional Language Medium Paper
- Full paper in regional language: Tamil / Telugu / Marathi / Gujarati / Bengali /
  Kannada / Odia / Punjabi / Malayalam / Assamese / Urdu
- Used for: state board vernacular medium schools, coaching in regional language
- RTL rendering for Urdu (Nastaliq script)

### 8.3 Mixed Language Paper
- Some questions in English, some in regional language (per-question language tag)
- Used for: language subject papers (Hindi literature, Tamil literature, etc.)

### 8.4 Language Availability Check
- Before publishing bilingual paper: system checks all selected questions have translations
  in the required language
- Missing translations flagged: "3 questions missing Hindi translation — please add in
  Module 17 or switch to English-only paper"

---

## 9. Answer Key & Marking Scheme

### 9.1 Auto-Generated Answer Key
For objective question types:
- MCQ Single/Multiple: correct option(s) per set (option labels differ by set due to shuffling)
- Numerical/Integer/Decimal: correct value + tolerance range
- Match the Following: correct pairs per set
- Assertion-Reason: correct option per set
- Sequence/Arrangement: correct order

Answer key PDF: clean table format — Question No. | Correct Answer | Marks
Separate answer key per set (A/B/C/D).

### 9.2 Marking Scheme for Descriptive Questions
Teacher-authored step-by-step marks breakdown:
```
Q7 — Derive the expression for electric potential energy (5 marks)
  Step 1: State definition of electric potential energy          — 1 mark
  Step 2: Draw diagram with two charges                          — 0.5 mark
  Step 3: Write work done expression for bringing charge q2      — 1 mark
  Step 4: Integrate to get potential energy formula              — 1.5 marks
  Step 5: Write final expression with correct symbols and units  — 1 mark

Accept alternate correct method: full marks if answer is correct
Common mistake: missing negative sign in derivation — deduct 0.5 mark
Expected answer range: [model answer content blocks here]
```

### 9.3 Marking Scheme Templates
Platform provides templates for standard question types:
- Derivation template: Definition + Diagram + Steps + Result
- Numerical template: Given + Find + Formula + Substitution + Answer + Unit
- Short Answer template: Point 1 + Point 2 + Example
- Diagram question: Diagram (marks) + Labels (marks each) + Description

### 9.4 Grace Marks Workflow (Post-Exam)
- HOD marks a question as erroneous/ambiguous post-exam
- Grace type: Full marks to all / Full marks to students who attempted / Award correct answer only
- Module 20/21 auto-updates scores for all affected students
- Audit log: who granted grace, reason, affected student count

### 9.5 Expected Answer Range for Numerical
- Answer key shows: "Accept answers between X and Y" (tolerance range from Module 17)
- Ensures consistent evaluation across multiple evaluators
- Module 20 auto-grading uses same tolerance

---

## 10. Paper Security

### 10.1 Paper Lock
- Once HOD approves: paper locked — no content edits
- Admin unlock: requires reason entry; creates audit log entry; HOD re-approval needed
- Locked papers: timestamp + approver name stamped permanently in metadata

### 10.2 Access Control
- Before exam: paper visible only to creator + co-examiner + HOD + Principal + Admin
- Students: zero access until Module 19 exam goes live at T=0
- Every view of locked paper: logged — who, when, device, IP

### 10.3 Confidentiality Watermark
- Print version: "CONFIDENTIAL — FOR EXAMINER USE ONLY" on every page
- Digital preview: watermark overlay with teacher name + timestamp
- Removed from student-facing copy after paper is distributed

### 10.4 Digital Seal (Tamper Detection)
- Approved paper JSON: cryptographic hash (SHA-256) stored in DB
- On any exam delivery: Module 19 verifies hash before displaying to students
- If hash mismatch: paper delivery blocked; security alert to Admin

### 10.5 Emergency Paper Replacement
- Trigger: Admin activates emergency replacement if leak confirmed
- System auto-generates new paper from same pools (parallel set not yet used)
- Old paper CDN URL invalidated (returns 403 immediately)
- New paper CDN URL activated; all students get new paper at next page load
- Emergency replacement log: reason, who triggered, time, old vs new paper IDs

---

## 11. Supporting Documents — Auto-Generation

### 11.1 Cover Page
Auto-populated from exam metadata:
- Institution logo and name
- Exam name, subject, class/grade, date, time, duration
- Maximum marks, passing marks (if applicable)
- General instructions (board-specific template pre-loaded; teacher customises)
- "CONFIDENTIAL" stamp (removed after exam distribution)
- Bilingual cover (English + Hindi / regional language)

### 11.2 Invigilator Instructions Sheet
Generated per exam hall / per exam:
- Exam name, subject, date, time, duration
- Total students in hall, set code assignments
- CWSN students list: name, roll number, accommodation (extra time / scribe / large print)
- Step-by-step distribution instructions
- Emergency contact: HOD mobile number
- Instructions for handling absentees, unfair means, early submission

### 11.3 OMR Answer Sheet
- Auto-generated matching paper's MCQ count and set code
- Student entry fields: Roll Number + Set Code (bubbles)
- Question bubbles: 4 options (A/B/C/D) per question
- Compatible with Module 20 OMR scanning engine
- Institution logo and exam name printed on OMR

### 11.4 Answer Booklet
- Ruled pages PDF
- Question number pre-printed at each section start
- Page count calculated from total marks and average answer length per question type
- Student name + roll number + date fields on cover

### 11.5 Examiner Copy
- Same paper PDF with answer key and marks printed alongside each question
- Marking scheme notes printed under each descriptive question
- "FOR TEACHER USE ONLY" header on every page

### 11.6 Attendance Sheet (Exam Hall)
- Pre-printed: student name, roll number, set code, seat number, signature column
- Links to Module 19 seating plan
- Invigilator fills: Present / Absent per student
- Feeds Module 19 exam attendance and absentee report

### 11.7 Absentee Report
Auto-generated post-exam:
- List of absent students per subject per exam date
- Feeds re-examination scheduling workflow
- Notifies parents (Module 09) via in-app notification

### 11.8 Admit Card Data Feed
Paper details (name, date, time, subject, marks, duration) auto-fed to Module 19
admit card generation — no manual re-entry.

### 11.9 Roll Number Slip
- Per student: name, roll number, exam schedule, set code, venue, seat number
- Auto-generated from Module 19 seating data + this module's paper data
- Printed in bulk or distributed digitally via student app

---

## 12. CWSN & Adapted Papers

### 12.1 CWSN Paper Auto-Adaptation
From any standard paper, one-click CWSN variant:
- HOT questions (Bloom's L5–L6) replaced with Foundation-level equivalents from same topic
- Font size: 16pt minimum
- Line spacing: 1.5× standard
- One question per page (no cramped layout)
- MCQ: 4 options reduced to 3 (remove most similar distractor)
- Total marks same; extra time notation added (25% additional — RTE/RPWD standard)

### 12.2 Scribe Instructions Sheet
Auto-generated per CWSN student requiring scribe:
- Student name, roll number, exam, extra time (minutes)
- Scribe name (if pre-assigned)
- Instructions for scribe: read each question, do not interpret, write exactly as student says
- Language of communication preference noted

### 12.3 Visual Impairment Variant
- All diagrams replaced with text descriptions
- All charts replaced with data tables
- LaTeX equations have verbal descriptions appended
- Braille-ready plain text export for conversion by school support staff

### 12.4 Hearing Impairment Variant
- Audio questions replaced with visual equivalents
- All listening comprehension converted to reading comprehension

### 12.5 Remedial Test Paper
- Only Foundation and Easy questions
- No HOTS, no negative marking
- Shorter duration
- Larger font, more whitespace
- Used for: Class 9/10 detained students, re-test after remedial teaching

---

## 13. Paper Review & Approval Workflow

### 13.1 Review States

```
DRAFT → SUBMITTED_FOR_REVIEW → CO_EXAMINER_REVIEW → HOD_APPROVAL
      → ACADEMIC_DIRECTOR_APPROVAL (for board/semester papers)
      → LOCKED (published; no further edits)
```

### 13.2 Co-Examiner Review
- Paper shared with second teacher (co-examiner)
- Co-examiner can: flag questions (with reason), suggest replacement questions,
  add inline comments per question, approve or reject section
- Teacher (creator) sees flags; accepts/rejects suggestions; revises paper

### 13.3 HOD Approval
- HOD reviews final paper: quality score, Bloom's distribution, coverage check, repeat check
- HOD can: approve → lock / return with comments
- HOD cannot edit paper directly (separation of duties)

### 13.4 Academic Director Approval (Board / Semester Papers)
- For Pre-Board, Annual, and Semester End exams: Academic Director final sign-off
- Academic Director sees: paper content + quality report + co-examiner notes + HOD comments
- Approve → paper locked permanently

### 13.5 Paper Version History
- Every save creates new version
- Diff view: question additions/removals/swaps between versions
- Final approved version timestamped and attributed to approver
- Versions retained for 3 academic years

---

## 14. Paper Quality & Analytics

### 14.1 Pre-Exam Quality Report
- Quality score (0–100) with breakdown by component
- Bloom's distribution chart vs target
- Difficulty distribution chart vs target
- Topic coverage map: marks per chapter vs syllabus weightage (Module 15)
- Repeat question list (if any)
- Missing answer key / marking scheme: flagged per question

### 14.2 Comparison with Previous Year Paper
- Topic-wise marks: this year vs last year same exam
- Highlights over/under-tested topics vs syllabus weightage
- Bloom's level shift: is this year's paper cognitively harder/easier than last year?
- Used by HOD in academic planning

### 14.3 Post-Exam Difficulty Validation
After Module 20/21 results:
- Compare predicted average (from pre-exam calculation) vs actual class average
- Question-by-question: predicted difficulty (p-value) vs actual % correct in this exam
- Calibration feedback: auto-adjusts difficulty index weights for future auto-generation
- Paper quality retrospective: HOD reviews what worked and what didn't

### 14.4 Per-Question Post-Exam Analytics
For each question in paper (online exams — Module 19):
- % correct, % chose each option (MCQ)
- Average time spent per question
- Correlation with total score (discrimination validation)
- Feeds Module 17 item analysis update

### 14.5 Student Paper Feedback (Post-Exam)
- Students rate paper difficulty: 1–5 scale; visible to HOD as aggregate
- Flag ambiguous questions: student identifies specific question → reviewed by HOD
- Anonymous feedback option (DPDPA 2023 compliant)
- Grace marks trigger: if > 40% students flag same question → HOD auto-prompted to review

### 14.6 Subject-Level Paper Statistics (Multi-Year)
Per subject per exam type:
- Average paper quality score trend (3 years)
- Average class performance trend
- Most frequently tested chapters vs syllabus weightage alignment trend
- Used in NAAC/NBA annual quality review

---

## 15. Print & Export Options

### 15.1 Standard Print PDF
- Clean A4 layout: institution letterhead, cover page, questions, answer boxes
- Section-wise formatting per template
- Question numbering: auto-formatted per section pattern
- Equations: LaTeX → rendered PNG embedded in PDF
- Diagrams: canvas JSON → rendered PNG embedded
- Charts: chart JSON → rendered PNG embedded

### 15.2 Compact Print
- 2 questions per row for MCQ sections
- Reduces paper usage for large objective sections
- Full-width for descriptive sections

### 15.3 Bilingual Print
- Two columns: English (left) + Hindi/Regional (right) for each question
- Or: full question in English → full question in Hindi below (sequential bilingual)
- Cover page: bilingual general instructions

### 15.4 Large Print (CWSN)
- 16pt minimum font, double spacing, one question per page
- Auto-generated from CWSN variant paper

### 15.5 Braille-Ready Text Export
- Plain text structured export: no diagrams, no charts
- LaTeX converted to verbal descriptions
- Used by school support staff to convert to Braille using standard software

### 15.6 OMR Sheet PDF
- Bubble sheet matching MCQ count + set code
- Roll number + set code entry bubbles
- Institution logo, exam name, date
- Compatible with Module 20 OMR scanner

### 15.7 Answer Key PDF
- Clean table: Q.No. | Section | Marks | Correct Answer
- Numerical: value + accepted range
- Descriptive: reference to marking scheme
- Per-set separate PDFs

### 15.8 Examiner Copy PDF
- Paper + answer key side by side
- Marking scheme notes under descriptive questions
- "FOR TEACHER USE ONLY" watermark
- Per-set PDFs

### 15.9 Marking Scheme PDF
- Detailed step-by-step marks breakdown per question
- Used for evaluation training and uniform grading across evaluators
- CBSE format: aligns with CBSE official marking scheme structure

---

## 16. Platform Paper Bank (Pre-Built Papers)

### 16.1 Platform Sample Paper Library
EduForge content team provides ready-made papers:
- CBSE Classes 10 + 12: all subjects, 5 sample papers per subject per year
- State boards: 3 sample papers per subject per class for major state boards
- JEE Main: 10 mock tests (full pattern)
- JEE Advanced: 5 mock test sets (Paper 1 + Paper 2)
- NEET UG: 10 mock tests
- UPSC Prelims: 5 mock test sets (GS1 + CSAT)
- Banking: IBPS PO/Clerk, SBI PO — 5 mock tests each
- SSC CGL/CHSL: 5 mock tests each

### 16.2 CBSE Official Sample Paper Integration
- CBSE official SQP (Sample Question Paper) loaded within 48 hours of release
- Available as-is for institution to assign to students
- Institution can clone and modify SQP for internal use

### 16.3 Platform Paper Update Cycle
- Annual: new academic year papers by April 1
- Board pattern change → template updated within 7 working days
- CBSE SQP → loaded within 48 hours of October release

---

## 17. Paper Archive & Compliance

### 17.1 Paper Bank (Institution Archive)
- All published papers stored permanently in institution's paper bank
- Browsable by: subject / grade / exam type / academic year / set
- Used for: repeat prevention check / clone for next year / NAAC evidence

### 17.2 Paper Cloning (Year-to-Year)
- Clone last year's paper → replace 30–40% of questions (configurable) → new paper
- Change log shows: which questions are new, which carried forward
- Useful for: question paper sets where partial continuity is desired

### 17.3 NAAC / NBA Paper Audit Export
- NAAC SSR Criterion 2.4: examination reforms, question paper quality evidence
- NBA Criterion 5: CO assessment evidence — CO-wise marks distribution per paper
- Export: per subject per semester — paper inventory, Bloom's distribution, CO mapping, quality scores
- Format: NAAC/NBA prescribed table structure (Excel/PDF)

### 17.4 Board Submission Package
- For CBSE/state board affiliated schools: some boards require internal exam papers for record
- Auto-package: paper PDF + answer key PDF + marks distribution table
- Institution seal / principal signature field included in PDF
- Exported per CBSE/board prescribed format

### 17.5 3-Year Paper Retention
- All locked papers retained for minimum 3 academic years
- Soft-archival after 3 years (accessible to Admin, not default visible)
- DPDPA 2023: paper content does not contain personal student data; retention is institutional record

---

## 18. Spell Check, Readability & Language Quality

### 18.1 Spell Check & Grammar Check
- Runs on all text content before publishing
- English: standard spell check + grammar (subject-specific vocabulary exempted)
- Hindi: Devanagari spell check (common errors flagged)
- Errors highlighted inline; teacher clicks to fix
- Cannot publish with unresolved critical errors

### 18.2 Readability Score
- Flesch-Kincaid grade level calculated for paper overall and per section
- Advisory if readability > 2 grades above target class level
- Used to ensure language complexity is appropriate

### 18.3 Standard Instructions Templates
Board-specific general instruction templates pre-loaded:
- CBSE standard general instructions (updated per CBSE circular annually)
- State board instructions per state
- Competitive exam instructions per exam
- Teacher edits as needed; original template preserved

---

## 19. Open Book & Take-Home Assessment

### 19.1 Open Book Exam
- Tagged as `is_open_book: true`
- Auto mode enforces: minimum 80% HOTS (Bloom's L3–L6); no L1–L2 recall questions
- System warns if teacher tries to include recall questions
- Instructions: "This is an open-book examination. Candidates may refer to textbooks
  and notes but may not communicate with other candidates."

### 19.2 Take-Home Assessment
- Tagged as `is_take_home: true`
- No time lock (extended deadline — hours to days)
- Submission via Module 14 (assignment submission)
- Questions tagged as take-home type in Module 17
- Anti-plagiarism check on submissions (Module 14 handles)

---

## 20. Data Architecture

### 20.1 Tenancy
- All paper data tagged with `tenant_id` (PostgreSQL RLS)
- Platform sample papers: `tenant_id = NULL` (read-only to all)
- Paper JSON and PDFs on CDN (not in DB)
- DB stores paper metadata, section structure (question IDs + versions), and CDN paths

### 20.2 Database Schema

```sql
-- Exam papers master
exam_papers (
  paper_id            UUID PK,
  tenant_id           UUID FK tenants NULL,        -- NULL = platform sample
  branch_id           UUID FK branches NULL,
  exam_id             UUID FK exams NULL,           -- links to Module 19
  set_code            VARCHAR(5),                   -- A | B | C | D | SHIFT_1 etc.
  board_id            UUID FK boards NULL,
  subject_id          UUID FK subjects_master,
  grade               VARCHAR(20),
  academic_year_id    UUID FK academic_years,
  exam_type           VARCHAR(30),
  pattern_template_id UUID FK paper_templates NULL,
  total_marks         NUMERIC(6,1),
  duration_minutes    INTEGER,
  primary_language    VARCHAR(10) DEFAULT 'en',
  secondary_language  VARCHAR(10) NULL,
  is_bilingual        BOOLEAN DEFAULT FALSE,
  is_cwsn_variant     BOOLEAN DEFAULT FALSE,
  is_open_book        BOOLEAN DEFAULT FALSE,
  is_take_home        BOOLEAN DEFAULT FALSE,
  is_platform_sample  BOOLEAN DEFAULT FALSE,
  quality_score       NUMERIC(5,1) NULL,
  predicted_avg_pct   NUMERIC(5,2) NULL,
  bloom_distribution  JSONB,
  diff_distribution   JSONB,
  coverage_check_ok   BOOLEAN DEFAULT FALSE,
  repeat_check_ok     BOOLEAN DEFAULT FALSE,
  status              VARCHAR(20) DEFAULT 'DRAFT',
  -- DRAFT | SUBMITTED | CO_REVIEW | HOD_APPROVED | DIRECTOR_APPROVED | LOCKED | ARCHIVED
  co_examiner_id      UUID FK users NULL,
  approved_by_hod     UUID FK users NULL,
  approved_by_hod_at  TIMESTAMPTZ NULL,
  approved_by_dir     UUID FK users NULL,
  approved_by_dir_at  TIMESTAMPTZ NULL,
  locked_at           TIMESTAMPTZ NULL,
  paper_hash          VARCHAR(64) NULL,             -- SHA-256 of paper JSON
  cdn_paper_path      TEXT NULL,
  cdn_answer_key_path TEXT NULL,
  cdn_marking_scheme_path TEXT NULL,
  cdn_print_pdf_path  TEXT NULL,
  cdn_cwsn_pdf_path   TEXT NULL,
  cdn_bilingual_pdf_path TEXT NULL,
  cdn_omr_pdf_path    TEXT NULL,
  created_by          UUID FK users,
  cloned_from_id      UUID NULL,
  version             INTEGER DEFAULT 1,
  created_at          TIMESTAMPTZ,
  updated_at          TIMESTAMPTZ
)

-- Paper sections
paper_sections (
  section_id          UUID PK,
  paper_id            UUID FK exam_papers,
  label               VARCHAR(10),                  -- A, B, C, D, E
  title_json          JSONB,                        -- {en: "...", hi: "..."}
  question_type       VARCHAR(30),
  marks_each          NUMERIC(4,1),
  negative_marks      NUMERIC(4,2) DEFAULT 0,
  partial_marks       BOOLEAN DEFAULT FALSE,
  attempt_rule        VARCHAR(30),
  attempt_n           INTEGER NULL,                 -- for ATTEMPT_ANY_N_OF_M
  attempt_m           INTEGER NULL,
  sequence_no         INTEGER,
  total_marks         NUMERIC(6,1),
  time_limit_minutes  INTEGER NULL                  -- for sectional time-limit exams
)

-- Paper questions
paper_questions (
  pq_id               UUID PK,
  section_id          UUID FK paper_sections,
  paper_id            UUID FK exam_papers,
  question_id         UUID FK questions,
  question_version    INTEGER,
  sl_no               INTEGER,
  marks               NUMERIC(4,1),
  is_internal_choice  BOOLEAN DEFAULT FALSE,
  choice_group_id     UUID NULL,                   -- groups Q5a and Q5b
  choice_label        VARCHAR(5) NULL,             -- "a" or "b"
  sub_part_parent_id  UUID NULL,                   -- for Q5(a), Q5(b)
  sub_part_label      VARCHAR(5) NULL,             -- "a", "b", "c"
  carry_forward_flag  BOOLEAN DEFAULT FALSE,
  bloom_level         VARCHAR(20),
  difficulty_tag      VARCHAR(15),
  is_auto_selected    BOOLEAN DEFAULT FALSE,
  selection_reason    TEXT NULL
)

-- Paper templates
paper_templates (
  template_id         UUID PK,
  tenant_id           UUID FK tenants NULL,         -- NULL = platform template
  board_id            UUID FK boards NULL,
  subject_id          UUID FK subjects_master NULL,
  grade               VARCHAR(20) NULL,
  exam_type           VARCHAR(30),
  template_name       VARCHAR(200),
  template_json       JSONB,                        -- full section structure config
  total_marks         NUMERIC(6,1),
  duration_minutes    INTEGER,
  is_platform_template BOOLEAN DEFAULT FALSE,
  platform_version    VARCHAR(20) NULL,
  created_by          UUID FK users NULL,
  created_at          TIMESTAMPTZ
)

-- Paper review log
paper_review_log (
  review_id           UUID PK,
  paper_id            UUID FK exam_papers,
  reviewer_id         UUID FK users,
  review_stage        VARCHAR(30),                  -- CO_EXAMINER | HOD | DIRECTOR
  action              VARCHAR(20),                  -- APPROVED | RETURNED | FLAGGED
  comments            TEXT NULL,
  flagged_question_ids UUID[],
  created_at          TIMESTAMPTZ
)

-- Paper access log (security audit)
paper_access_log (
  log_id              UUID PK,
  paper_id            UUID FK exam_papers,
  accessed_by         UUID FK users,
  access_type         VARCHAR(20),                  -- VIEW | PRINT | EXPORT | CDN_FETCH
  ip_address          INET,
  device_info         TEXT,
  created_at          TIMESTAMPTZ
)

-- Grace marks log
grace_marks_log (
  grace_id            UUID PK,
  paper_id            UUID FK exam_papers,
  question_id         UUID FK questions,
  granted_by          UUID FK users,
  grace_type          VARCHAR(30),                  -- FULL_ALL | FULL_ATTEMPTED | CORRECT_ONLY
  reason              TEXT,
  affected_students   INTEGER,
  created_at          TIMESTAMPTZ
)

-- Post-exam paper analytics
paper_post_analytics (
  analytics_id        UUID PK,
  paper_id            UUID FK exam_papers,
  exam_id             UUID FK exams NULL,
  actual_avg_pct      NUMERIC(5,2) NULL,
  actual_dist_json    JSONB NULL,                   -- actual grade distribution
  predicted_vs_actual JSONB NULL,                   -- question-level comparison
  calculated_at       TIMESTAMPTZ
)
```

### 20.3 Indexes
```sql
CREATE INDEX idx_papers_tenant_subject  ON exam_papers(tenant_id, subject_id, grade, academic_year_id);
CREATE INDEX idx_papers_exam_type       ON exam_papers(tenant_id, exam_type, status);
CREATE INDEX idx_paper_questions_paper  ON paper_questions(paper_id, section_id, sl_no);
CREATE INDEX idx_paper_questions_qid    ON paper_questions(question_id, paper_id);
CREATE INDEX idx_access_log_paper       ON paper_access_log(paper_id, created_at DESC);
CREATE INDEX idx_templates_board        ON paper_templates(board_id, subject_id, grade, exam_type);
```

---

## 21. Roles & Permissions

| Action | Teacher | Co-Examiner | HOD | Academic Director | Principal | Admin |
|---|---|---|---|---|---|---|
| Create / edit paper (own subject) | ✅ | Read + Flag | ✅ | View | View | ✅ |
| Auto-generate paper | ✅ | — | ✅ | — | — | ✅ |
| Submit for review | ✅ | — | ✅ | — | — | ✅ |
| Co-examiner review | — | ✅ | — | — | — | — |
| HOD approve / lock | — | — | ✅ | — | ✅ | ✅ |
| Academic Director approve | — | — | — | ✅ | ✅ | — |
| View locked paper | ✅ (own) | — | ✅ | ✅ | ✅ | ✅ |
| Print / export paper | ✅ (own) | — | ✅ | ✅ | ✅ | ✅ |
| Grant grace marks | — | — | ✅ | ✅ | ✅ | ✅ |
| Emergency replacement | — | — | — | — | ✅ | ✅ |
| View paper access log | — | — | — | — | ✅ | ✅ |
| Export NAAC/NBA evidence | — | — | ✅ | ✅ | ✅ | ✅ |

---

## 22. Notifications (In-App Only)

| Trigger | Recipient |
|---|---|
| Paper submitted for co-examiner review | Co-examiner |
| Co-examiner review complete (approved/returned) | Paper creator |
| Paper submitted for HOD approval | HOD |
| Paper approved and locked | Paper creator, Academic Director |
| Paper returned by HOD with comments | Paper creator |
| Emergency paper replacement triggered | All exam invigilators, Admin |
| Paper CDN time-lock activated (exam going live) | Paper creator (confirmation) |
| Grace marks granted on a question | Paper creator, HOD |
| Post-exam quality report ready | Paper creator, HOD |
| Student paper feedback exceeds flag threshold | HOD |
| Platform sample paper updated (new CBSE SQP loaded) | All subject HODs |

---

## 23. Compliance Summary

| Standard | Coverage |
|---|---|
| CBSE Question Paper Design (QPD) | Pre-loaded QPD templates per subject/class; deviation flagged; Section E Case Study enforced |
| CBSE SQP Integration | Official Sample Question Paper loaded within 48 hrs of October release |
| NEP 2020 Competency-Based Assessment | Minimum HOTS % enforced; open-book exam HOTS-only; L3–L6 distribution targets |
| UGC / AICTE CO Coverage | CO coverage heatmap; every CO assessed at least once per semester enforced |
| RTE Act 2009 / RPWD Act 2016 | CWSN adapted papers, extra time, scribe instructions, Braille-ready export |
| DPDPA 2023 | Paper access log; student feedback anonymous option; 3-year retention policy |
| Copyright Act 1957 § 52(1)(i) | PYQ-based questions used under educational fair use; platform papers EduForge IP |
| IT Act 2000 | Cryptographic hash tamper detection; access control logs; watermarking |
| NAAC SSR Criterion 2.4 | Paper quality scores, Bloom's distribution, CO mapping archived for accreditation |
| NBA Criterion 5 | CO-wise marks distribution per paper; attainment evidence export |
| State Board Compliance | All 28 state board patterns pre-loaded; updated within 7 days of board notification |
