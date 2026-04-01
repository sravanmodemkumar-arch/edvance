# Module 15 — Syllabus & Curriculum Builder

## Purpose
Provide a unified, multi-board, multi-institution-type syllabus management system for EduForge.
Teachers, HODs, and Principals plan, track, and report curriculum coverage in real time.
The syllabus hierarchy drives question-paper weightage, assignment tagging, lesson planning,
annual teaching plans, board compliance reporting, and NAAC/NBA/AICTE accreditation exports.
No file uploads required for core syllabus operations — all content is platform-native.

---

## 1. Scope — Institution Types Supported

| Institution Type | Syllabus Model |
|---|---|
| School (K-12) | Board + Grade + Subject + Term |
| Degree College | University-affiliated / Autonomous — Semester / Annual / Trimester |
| Engineering / Polytechnic | AICTE model curriculum, University + autonomous |
| Medical / Pharmacy | NMC / PCI prescribed curriculum |
| ITI / Vocational | NCVT MIS unit-wise, SCVT, NSQF Level 1–8 |
| Coaching Centre | Competitive exam topic list (JEE / NEET / UPSC / SSC / Banking / Law) |
| Open / Distance | NIOS, CBSE Open School, IGNOU-pattern |

---

## 2. Board & Curriculum Type Registry

### 2.1 School Boards
- CBSE (Central Board of Secondary Education)
- ICSE / ISC (Council for the Indian School Certificate Examinations)
- IB (International Baccalaureate — PYP / MYP / DP)
- IGCSE / Cambridge (O Level / A Level)
- NIOS (National Institute of Open Schooling)
- CBSE Open School
- All 28 State Boards:
  - RBSE (Rajasthan Board of Secondary Education)
  - UP Board (UPMSP)
  - MP Board (MPBSE)
  - Maharashtra Board (MSBSHSE)
  - Karnataka (KSEEB / PUC Board)
  - Tamil Nadu (TNBSE — SSLC / HSC)
  - AP Board (BSEAP)
  - Telangana Board (BSETS)
  - Bihar Board (BSEB)
  - West Bengal Board (WBBSE / WBCHSE)
  - Gujarat Board (GSEB)
  - Haryana Board (HBSE)
  - Punjab Board (PSEB)
  - Himachal Pradesh Board (HPBOSE)
  - Uttarakhand Board (UBSE)
  - Chhattisgarh Board (CGBSE)
  - Jharkhand Board (JAC)
  - Odisha Board (BSE Odisha / CHSE)
  - Assam Board (SEBA / AHSEC)
  - Kerala Board (SCERT Kerala / DHSE)
  - Goa Board (GBSHSE)
  - J&K Board (JKBOSE)
  - HP Board, Manipur Board, Meghalaya Board, Mizoram Board, Nagaland Board,
    Tripura Board, Sikkim Board, Arunachal Pradesh Board

### 2.2 Higher Education Frameworks
- University-affiliated college (semester / annual / trimester system)
- Autonomous college (own curriculum, university-approved)
- Deemed / private university
- UGC CBCS (Choice Based Credit System)
- NEP 2020 OBE (Outcome Based Education) — 4-year UG, multi-entry/exit
- AICTE model curriculum (B.Tech / M.Tech / MBA / MCA / Diploma)
- UGC LOCF (Learning Outcomes-based Curriculum Framework) for degree programs
- NMC (National Medical Commission) curriculum for MBBS
- PCI (Pharmacy Council of India) for B.Pharm / M.Pharm
- BCI (Bar Council of India) for LLB / LLM
- NCTE for B.Ed / M.Ed / D.El.Ed

### 2.3 Competitive Exam Curriculum
- JEE Main (NTA syllabus — Physics / Chemistry / Maths)
- JEE Advanced (IIT syllabus — extended topics)
- NEET UG (NTA — Physics / Chemistry / Biology)
- NEET PG (NBE — 19 clinical subjects)
- CA Foundation / Intermediate / Final (ICAI)
- CS Foundation / Executive / Professional (ICSI)
- CMA Foundation / Intermediate / Final (ICMAI)
- UPSC CSE Prelims / Mains (GS 1–4, Optional papers — 26 optionals supported)
- SSC CGL / CHSL / MTS / GD / CPO
- IBPS PO / Clerk / SO / RRB PO / Clerk
- SBI PO / Clerk
- RRB NTPC / ALP / Group D
- State PSC (all 28 states — Prelims + Mains syllabus)
- CLAT / AILET / LSAT India
- CUET UG / PG (NTA)
- NDA / CDS / AFCAT / MNS
- CTET / TET (state-wise) / STET
- NTA NET / SET (state-wise)
- GATE (29 papers)
- CAT / XAT / MAT / CMAT
- AIIMS / JIPMER (historical pattern)

### 2.4 Vocational / Skill Curriculum
- NCVT MIS unit-wise trade syllabus (all 150+ ITI trades)
- SCVT (State Council for Vocational Training)
- PMKVY sector skill council competency maps (38 SSCs)
- NSQF Level 1–8 competency units
- DDU-GKY skill modules

---

## 3. Syllabus Hierarchy

Six-level deep hierarchy — each level is independently configurable:

```
Board / Framework
  └── Subject
        └── Grade / Semester / Year
              └── Unit
                    └── Chapter
                          └── Topic
                                └── Sub-topic (optional 6th level)
```

### 3.1 Hierarchy Rules
- Board and Subject are institution-wide master records (admin-managed)
- Grade / Semester assignment is branch-level
- Units and below are created by subject HOD or teacher
- Sub-topic level is optional; activated per subject when needed
- Each node carries: name (English + regional language), code, estimated hours,
  marks weightage, Bloom's level, difficulty tag, NSQF code (vocational),
  prerequisite pointers, and learning outcomes

---

## 4. Learning Outcomes (LOs)

### 4.1 SMART Format per Topic
Each topic must have at minimum one learning outcome written in SMART format:
- **S** — Specific: clearly names the concept/skill
- **M** — Measurable: defines how it will be assessed
- **A** — Actionable: verb from Bloom's taxonomy action list
- **R** — Relevant: aligned to board/university mandate
- **T** — Time-bound: expected within the lesson / unit / term

### 4.2 Bloom's Taxonomy Tagging
Each topic tagged at one primary Bloom's level:

| Level | Description | Example Verb |
|---|---|---|
| L1 — Remember | Recall facts | Define, List, State |
| L2 — Understand | Explain concepts | Explain, Describe, Summarise |
| L3 — Apply | Use in new situation | Solve, Calculate, Demonstrate |
| L4 — Analyse | Break down, examine | Differentiate, Compare, Examine |
| L5 — Evaluate | Judge, critique | Justify, Assess, Critique |
| L6 — Create | Produce new work | Design, Construct, Formulate |

HOT (Higher Order Thinking) tag auto-applied for L4–L6 topics.

### 4.3 NEP 2020 Competency Tags
Each topic optionally tagged with one or more 21st-century competencies:
- Critical Thinking
- Creativity & Innovation
- Communication
- Collaboration
- Digital Literacy
- Emotional Intelligence
- Civic / Constitutional Citizenship
- Financial Literacy (NEP 2020 Appendix)
- Environmental & Sustainability Awareness

### 4.4 NIPUN Bharat / FLN Milestone Mapping (Classes 1–3)
- Topics in Hindi, English, and Maths for Classes 1–3 linked to NIPUN Bharat
  FLN competency codes (NCERT FLN framework, 2022)
- FLN competency: code, description, expected grade-end mastery level
- Teacher marks FLN milestone achieved per student cluster
- Feeds NIPUN Bharat progress reporting to district/state DEO portal

---

## 5. Marks & Weightage Distribution

### 5.1 Unit-wise Marks Weightage
- Teacher assigns marks weightage to each unit
- System auto-sums and validates against board-mandated total
- Guard rail: cannot publish syllabus if sum ≠ board total (±0 tolerance)
- Weightage drives Module 18 Exam Paper Builder's auto-distribution engine

### 5.2 Difficulty Tagging per Topic
Each topic tagged:

| Tag | Meaning |
|---|---|
| Foundation | Basic recall; all students expected to answer |
| Standard | Core concept; majority of students |
| Higher | Application level; above-average students |
| HOT | Higher Order Thinking; top-tier / competitive |

Feeds question bank difficulty filter (Module 17) and paper builder (Module 18).

### 5.3 CBSE CCE / Internal Assessment Allocation
- Unit-wise marks allocated to internal assessment components:
  - Periodic Test 1 / 2 / 3
  - Notebook Submission
  - Subject Enrichment Activity
  - Term 1 / Term 2 split
- Subject HOD defines allocation; auto-feeds CCE report card module (Module 21)

### 5.4 Practical / Lab Syllabus
- Lab experiments listed under corresponding theory chapters
- Each experiment: name, NCERT reference, apparatus list, observation table template,
  viva topics, marks (CBSE practical 30-mark split)
- Linked to Module 14 digital lab record book
- Lab syllabus tracked separately from theory coverage

### 5.5 CBSE Activity / Project Calendar
- Subject-wise projects and activities scheduled per CBSE circular
- Distributed across Term 1 and Term 2
- Teacher assigns project topics per student/group; linked to Module 14 assignments

---

## 6. Teaching Hours Management

### 6.1 Estimated Teaching Hours
- Teacher assigns estimated hours per topic at syllabus creation
- Hours auto-summed per unit, subject, and full-year plan
- Compared against available periods from Module 10 timetable
- Alert if total estimated hours > available periods for that subject

### 6.2 Annual Teaching Plan (ATP) — Auto-generation
- System fetches working days from Module 05 (academic calendar) filtering:
  - Public holidays
  - Exam-blackout days
  - PTM days (Module 33)
  - Annual day / sports day / other events
- Distributes all chapters/topics across available working days proportionally
  by estimated hours and unit weightage
- Teacher reviews and manually adjusts topic-to-date mapping
- ATP locked once HOD approves; changes tracked with reason log
- Python generation engine — same pattern as Module 10 timetable generator

### 6.3 Weekly Teaching Plan (WTP) — Auto-generation
- Derived from ATP for the current week
- Shows: Day → Period → Topic to be taught
- Teacher can drag-and-drop to reorder within week
- Adjusts ATP forward when a topic is moved

### 6.4 Holiday-Adjusted Auto-Reschedule
- When unplanned holiday added to calendar (Module 05), ATP auto-shifts
  all pending topics forward to next available working day
- Teacher receives in-app notification of revised pacing
- If rescheduling causes gap before board exam, alert sent to HOD with
  suggested mitigation (reduction in revision days / increase periods/week)

---

## 7. Syllabus Progress Tracking

### 7.1 Daily Diary / Lesson Tracker
- Teacher logs after each period: topics taught, topics skipped (with reason),
  additional topics covered beyond plan
- Feeds planned vs actual coverage delta
- Aggregated per subject, per teacher, per grade, per branch

### 7.2 Planned vs Actual Coverage Dashboard
- Real-time % coverage by: subject / grade / section / teacher / unit / chapter
- Traffic light: Green ≥ 90% | Yellow 70–89% | Red < 70%
- HOD/Principal view: all subjects in one dashboard
- Timeline chart: expected completion line vs actual completion line

### 7.3 Monthly Pacing Gap Alert
- At end of each month, system calculates % of planned topics actually taught
- If < 80% of monthly plan: automatic in-app alert to HOD
- Alert contains: subject, teacher name, number of topics pending, suggested
  additional periods needed to catch up before term-end

### 7.4 Batch / Section Syllabus Divergence Report
- For same subject taught by different teachers across sections:
  - Which section is ahead / behind
  - Number of topics diverged
  - Last common topic across all sections
- HOD can use this to schedule catch-up or instruct pacing correction

### 7.5 Topic Coverage Heatmap
- Calendar view per subject
- Each day coloured by number of topics taught (0 = white, 1 = light, 2+ = dark)
- HOD/Principal spots idle days and rapid-coverage days at a glance
- Click on any day to see exact topics logged

### 7.6 Attendance-Syllabus Correlation
- For each topic, shows average attendance of students on the days it was taught
- Topics taught on < 60% attendance days flagged for re-coverage
- Teacher prompted: "This topic was taught when only 42% students were present.
  Consider re-teaching or assigning a practice assignment."

### 7.7 Topic Re-teach Flag
- Teacher or system (via test result threshold from Module 20/21) can mark
  a topic for re-teaching
- Re-teach slot auto-inserted into next WTP
- Re-teach count tracked per topic; if same topic re-taught 3+ times,
  HOD alerted to investigate conceptual difficulty

### 7.8 Syllabus Completion Certificate
- Auto-generated PDF when teacher logs 100% theory + practical coverage
- Contents: institution name, board, grade, subject, academic year,
  teacher name, completion date, digital signature slot
- Used for submission to board/university at year-end
- Stored in institution's document vault (Module 40)

---

## 8. Revision Planning

### 8.1 Revision Plan Builder
- Activated 4–6 weeks before board exam (configurable per board)
- Auto-distributes all chapters across revision days weighted by:
  - Unit marks weightage
  - Average student performance on that unit's tests (Module 20/21)
  - Number of HOT topics in unit
- Teacher can drag-and-drop to adjust chapter order

### 8.2 Pre-Board Syllabus Audit
- 4 weeks before board exam, system auto-generates report:
  - All uncovered theory topics (by subject)
  - All uncovered practical experiments
  - Teacher-wise accountability table
  - Suggested emergency catch-up schedule
- Report sent to Principal as in-app notification + PDF export

### 8.3 Exam-Blackout Enforcement
- Topics not yet marked as taught in daily diary cannot be selected in
  Module 18 Exam Paper Builder question filters
- API check: paper builder calls syllabus coverage API before allowing
  topic selection for internal exams
- For board exams (external): all board-prescribed topics included regardless
  of institution coverage (board controls external paper)

---

## 9. Syllabus Versioning & Governance

### 9.1 Syllabus Revision Workflow
- States: Draft → HOD Review → Principal / Academic Director Approval → Published
- Once Published, syllabus is version-locked for that academic year
- Amendments require re-entry into draft; new minor version created
- Full audit trail: who changed what, when, reason for change

### 9.2 Academic Year Snapshot
- Each academic year generates an independent syllabus snapshot
- Historical comparison: view syllabus of AY 2023-24 vs AY 2024-25 side-by-side
- Diff view highlights: added topics (green), removed topics (red),
  reordered topics (yellow)

### 9.3 Clone from Previous Year
- Clone entire syllabus structure from previous academic year with one click
- Selective override: teacher can modify specific chapters/topics after cloning
- All changes from previous year tracked in diff view for record

### 9.4 Syllabus Lock After Board Exam Registration
- When institution registers students for board exams (Module 19 / external),
  theory syllabus is frozen
- No topic deletion allowed after lock
- Additions allowed with audit trail (new circular / board addendum)
- Lock can only be lifted by Super Admin with documented reason

### 9.5 Deleted-Topic Recovery
- All topic deletions are soft-delete (hidden, not permanently removed)
- Institution Admin can restore any deleted topic with reason log
- Recovery log visible to HOD and Principal
- Hard-delete only after academic year archive (automated)

---

## 10. Multi-Branch Syllabus Management

### 10.1 Master Syllabus and Branch Inheritance
- Institution sets one master syllabus per board/grade/subject/academic year
- All branches inherit master syllabus by default
- Branch-level override allowed per chapter/unit (e.g., branch B uses
  different chapter order for local language)
- Override tracked; institution-level report shows branch divergences

### 10.2 Subject Mapping Across Sections
- Single subject can be taught by multiple teachers across sections
- Syllabus progress aggregated at subject level across all sections
- Per-section progress also viewable
- Cross-section assignment creation from single subject view (Module 14)

### 10.3 Co-Teaching Support
- Two teachers can co-own a single subject:
  - Teacher A owns Units 1–4
  - Teacher B owns Units 5–8
- Each teacher's coverage tracked separately
- Combined subject coverage view for HOD
- Lesson plans mergeable into single subject plan

### 10.4 Guest / Visiting Faculty Assignment
- Chapters/units can be assigned to guest faculty
- Guest faculty access scoped to assigned chapters only
- Their progress tracked distinctly from regular staff
- Audit log retained when guest faculty access ends

---

## 11. Lesson Plan System

### 11.1 Lesson Plan Structure
Each lesson plan linked to a specific topic:
- Topic reference (board / subject / chapter / topic)
- Lesson objectives (from topic LOs + teacher additions)
- Prior knowledge required (prerequisite topics)
- Teaching strategy (select from template)
- Introduction / Hook (5 minutes)
- Main content delivery (breakdown by time)
- Activities / Practicals / Demonstrations
- Assessment / Check for understanding (exit ticket)
- Homework / Assignment (link to Module 14)
- Resources required (reference books, Module 16 notes, Module 44 videos)
- Expected duration (minutes)

### 11.2 Lesson Plan Templates

| Template | Use Case |
|---|---|
| Direct Instruction | Lecture-based theory delivery |
| Demonstration | Science experiments, Math proofs |
| Activity-Based Learning | Group work, hands-on tasks |
| Flipped Classroom | Students study material before class (Module 44) |
| Project-Based Learning | Extended inquiry across multiple lessons |
| Socratic Method | Discussion-led, question-driven |
| Inquiry-Based | Student-driven investigation |
| Differentiated Instruction | Mixed ability — Foundation + Standard + HOT variations |

### 11.3 Lesson Plan Approval Workflow
- Teacher creates lesson plan → HOD reviews → Approved / Returned with comments
- Approved plans archived under topic permanently
- HOD can view all pending approvals in queue

### 11.4 Digital Lesson Plan Repository
- Institution-wide searchable repository
- Search by: subject / grade / chapter / topic / Bloom's level / teaching strategy
- Teacher can clone any approved plan and customise for own section
- Cloning tracked — original author credited

### 11.5 Lesson Plan Compliance
- CBSE mandates lesson plans for all teachers (CBSE Circular No. Acad-45/2022)
- System enforces: teacher cannot mark topic as taught in daily diary if
  no approved lesson plan exists for that topic (configurable enforcement level:
  Hard Block / Warning / Advisory)

---

## 12. NCERT & Reference Material Alignment

### 12.1 NCERT Chapter Alignment
- When board is CBSE or any NCERT-following state board, system suggests
  NCERT chapter mapping for each topic
- NCERT textbook name, edition, chapter number, page range stored per topic
- Teachers confirm or override suggested mapping

### 12.2 Reference Book Mapping per Chapter
- Each chapter supports multiple reference book entries:
  - Book name, author, publisher, edition, chapter number, page range
  - Category: Primary Textbook / Reference / Supplementary
- Visible to students as recommended reading list
- Linked to Module 30 Library Management (book availability check)

### 12.3 Library Reading List per Grade
- Consolidated reading list per grade/subject exported from reference mappings
- Visible to students and parents in their app views
- Linked to Module 30 Library catalogue for availability and reservation

---

## 13. Differentiated Curriculum Support

### 13.1 Remedial Syllabus
- Separate lightweight syllabus for remedial student groups
- Identified automatically: students below threshold in attendance (Module 11)
  and test performance (Module 20)
- Reduced depth: Foundation-level topics only; HOT topics deferred
- Separate tracking — does not affect mainstream syllabus coverage stats
- CWSN students (RTE Section 2(d) / RPWD Act 2016) auto-enrolled in adapted stream

### 13.2 Advanced / Enrichment Syllabus
- Optional extended content for high-performing students
- Unlocked per student by teacher or automatically when test score > threshold
- Topics marked as Enrichment do not count in board syllabus coverage
- Tracks separately for gifted programme reporting (NEP 2020)

### 13.3 CWSN Adapted Syllabus
- Modified learning outcomes: simplified language, reduced scope
- Extended time provisions noted against each topic
- Modified assessment criteria (oral response allowed, practical alternatives)
- Aligned to RTE Act, RPWD Act 2016, and NCERT Inclusive Education guidelines
- Reported separately in U-DISE+ CWSN category

### 13.4 Supplementary Syllabus for Detained Students
- Students detained in Class 9/10/11 (repeaters) may have partial syllabus
  credit from previous year
- System marks carried-forward topics as pre-covered; teacher can override

---

## 14. Multilingual & Script Support

### 14.1 Bilingual Topic Names
Each topic stores names in:
- English (mandatory)
- Hindi (mandatory for CBSE/RBSE/UP/MP/CG/Jharkhand boards)
- Regional language (optional — Tamil, Telugu, Kannada, Malayalam, Marathi,
  Gujarati, Bengali, Odia, Punjabi, Assamese — configurable per branch)

### 14.2 Regional Language Input
- All topic name fields support Unicode input for all 22 scheduled languages
- Devanagari, Tamil, Telugu, Kannada, Malayalam, Gujarati, Bengali, Odia,
  Gurmukhi, Assamese scripts fully supported
- Right-to-left support for Urdu (Nastaliq) in J&K Board context

### 14.3 Multilingual Syllabus Export
- PDF export with regional language topic names for distribution to
  students/parents in regional medium institutions
- Supports mixed-script PDF rendering (English headers, regional body text)

---

## 15. Special Subject Syllabi

### 15.1 Physical Education
- Theory component: CBSE PE Theory syllabus (Classes 11–12)
- Practical component: fitness tests (600m run, Standing Broad Jump,
  Partial Curl-Up, Push-Ups, BMI), sports skills, health education
- Rajasthan specific: RBSE PE practical schedule
- Term-wise performance record linked to PE practical marks

### 15.2 Art / Music / Dance / Theatre (Co-Curricular)
- Subject syllabus builder for performing arts
- Performance rubrics attached to topics
- Term-wise recital / portfolio schedule
- Assessment criteria: Skill Demonstration / Composition / Appreciation / Theory
- Linked to Module 21 results for co-curricular grade entry

### 15.3 Foreign Languages
- French, German, Spanish, Japanese: CBSE foreign language syllabi
- Sanskrit: CBSE + state board Sanskrit curricula
- Arabic, Persian: CBSE / Madrasa board syllabi
- Script-aware topic names in respective Unicode blocks

### 15.4 Digital Literacy & Computational Thinking
- CBSE / NEP 2020 coding curriculum for Classes 6–8:
  - Classes 6–8: Block coding (Scratch-equivalent) → text coding (Python)
- Classes 9–10: Computer Science / Information Technology syllabus
- AI for Classes 8–12: CBSE AI curriculum framework
- Progress feeds digital literacy competency tag per student

### 15.5 Environmental Education (EVS)
- EVS Classes 3–5: spiral curriculum mapped against NCERT EVS framework
- Themes: Family / Food / Travel / Things / Animals / Water / Shelter /
  Our Country / Natural Phenomena
- Each theme cross-linked to Science and Social Studies topics in Classes 6+
  to show conceptual progression

### 15.6 Vocational / Skill Education (CBSE)
- CBSE Skill Education syllabus (Classes 9–12) for all 40+ vocational subjects
- Vocational subject marks: Theory + Practical + On-the-Job Training (OJT)
- OJT units mapped to industry partner sessions
- PSSCIVE / CBSE alignment verified per trade

---

## 16. Higher Education — NEP 2020 OBE Framework

### 16.1 Credit-Based Curriculum (CBCS / NEP OBE)
- Credit hours defined per course (theory credits + practical credits + tutorial credits)
- Credit distribution: 1 credit = 15 lecture hours / 30 lab hours / 30 tutorial hours
- Total program credits validated against UGC/AICTE minimum requirements

### 16.2 Programme Outcomes (PO) and Course Outcomes (CO)
- Programme Outcomes defined at department level (12 POs for engineering per NBA)
- Course Outcomes defined per course (minimum 5 COs per course per NBA norms)
- CO-PO mapping matrix (1–3 scale: 1=Low, 2=Medium, 3=High correlation)
- CO-PSO (Programme Specific Outcomes) mapping
- Attainment calculation (direct + indirect — exams + surveys)
- NBA OBE documentation auto-generated from mapping data

### 16.3 NEP 2020 Multi-Entry / Multi-Exit
- Certificate after Year 1, Diploma after Year 2, Degree after Year 3, Honours after Year 4
- Exit milestone tracking per student
- Credit bank integration concept (ABC — Academic Bank of Credits)
- Transfer credit recognition workflow

### 16.4 Elective Course Management
- Open electives, discipline-specific electives, interdisciplinary electives
- Student elective selection workflow (linked to Module 50 subscription/access)
- Elective seat capacity management
- NEP 2020 multidisciplinary stream validation (invalid combinations blocked)

### 16.5 AICTE Model Curriculum Alignment
- B.Tech / M.Tech: compare institution curriculum against AICTE model curriculum
- Gap analysis report: missing courses, insufficient credits per category
- Categories: Humanities & Social Sciences, Basic Science, Engineering Science,
  Professional Core, Professional Elective, Open Elective, Project/Seminar/Internship
- AICTE accreditation gap report exported as structured table

### 16.6 UGC LOCF Alignment
- For non-technical degree programs (BA / B.Sc / B.Com / MA / M.Sc)
- Compare syllabi against UGC LOCF subject templates
- Gap report flagging missing COs, inadequate credit allocation
- AQAR (Annual Quality Assurance Report) data export for NAAC criterion 1

---

## 17. Vocational & Skill Curriculum (ITI / PMKVY)

### 17.1 NCVT MIS Trade Syllabus Import
- Structured import of NCVT MIS trade syllabus (all 150+ trades)
- Import format: DGT (Directorate General of Training) prescribed XML/JSON
- Unit-wise competency blocks with NSQF level codes
- Hours per unit auto-imported and validated

### 17.2 NSQF Level Mapping
- Each unit tagged with NSQF Level (1–8):
  - Level 1–2: Basic / Semi-skilled
  - Level 3–4: Skilled
  - Level 5–6: Supervisory / Technician
  - Level 7–8: Professional / Expert
- NSQF level drives assessment criteria and certification eligibility
- Export to NSDC MIS portal in prescribed format

### 17.3 PMKVY Competency Map
- Sector Skill Council (SSC) job role mapped to syllabus
- 38 SSCs supported (ASDC, BFSI, Construction, Logistics, Retail, etc.)
- Competency units from SSC QP (Qualification Pack) loaded per job role
- NOS (National Occupational Standards) codes stored per unit
- PMKVY batch reporting: unit-wise completion exported to SMART portal

### 17.4 DDU-GKY Skill Modules
- Module-wise curriculum with placement-linked competencies
- 80% attendance linkage to NSDC reporting (Module 12 feeds this)
- Employer feedback integration: industry partner rates competency delivery quality

### 17.5 OJT / Internship Module Mapping
- On-the-Job Training units mapped to theory chapters
- Employer OJT feedback form (digital, in-platform) linked to topic completion
- OJT hours tracked against NCVT requirement
- Transport integration for plant visits (Module 29)

---

## 18. Cross-Module Linkages

### 18.1 Study Material Linkage (Module 16)
- Each topic shows count of notes/slides available
- One-click navigate to all material for that topic — view-only in-app; no download option
- "Add material" shortcut from syllabus topic row

### 18.2 Video Lecture Linkage (Module 44)
- Each topic linked to video lectures (platform-hosted or YouTube link)
- YouTube links open inside the app (in-app browser / WebView) — YouTube app is never launched; user stays within EduForge
- A "Watch Video" button is displayed per video; tapping it opens the YouTube URL in-app
- No download option for any video — streaming / in-app view only
- Video count and total watch duration visible per topic
- Teacher can assign a specific video as the primary lecture for a topic

### 18.3 Question Bank Linkage (Module 17)
- Each topic shows count of questions in bank: MCQ / short / long / numerical
- Difficulty distribution (Foundation / Standard / Higher / HOT) visible
- "Add question" shortcut from syllabus topic row

### 18.4 Assignment Linkage (Module 14)
- Each topic shows: assignments created, average score, submission rate
- "Create assignment" shortcut pre-fills chapter/topic tag
- Overdue assignment alert visible at topic level

### 18.5 Exam Paper Builder (Module 18)
- Unit weightage from syllabus auto-populates marks distribution in paper builder
- Coverage check API: paper builder cannot include questions on uncovered topics
  (configurable — internal exams enforce; board-pattern papers exempt)

### 18.6 Attendance Linkage (Module 11)
- Attendance-syllabus correlation (see Section 7.6) pulls from Module 11 data
- Topics taught on low-attendance days flagged

### 18.7 Result / Report Card (Module 21)
- Syllabus completion % feeds into teacher performance section of report card
- CBSE CCE unit-wise marks allocation (Section 5.3) feeds report card directly

### 18.8 Timetable (Module 10)
- Available periods fetched from Module 10 for ATP calculation
- Period diary in Module 10 cross-references daily diary here for consistency

---

## 19. Parent & Student Views

### 19.1 Parent Syllabus View
- Read-only access to monthly pacing plan per subject for their ward
- Current chapter being taught visible
- % coverage progress bar per subject
- No editing access
- School-type: all parents
- College-type: parents of students below 18 only (DPDPA 2023 — Section 9)
- Coaching-type: parents of students below 18 only

### 19.2 Student Syllabus View
- Chapter list with status: Done / In Progress / Upcoming
- Prerequisite lock: upcoming chapters locked until prerequisites marked done
- Study material and video links per topic (if released by teacher)
- Self-paced unlock for coaching: chapter unlocks after completing minimum
  practice questions on previous chapter

### 19.3 Self-Paced Coaching Unlock Logic
```
unlock_chapter(student_id, chapter_id):
  prerequisites = get_prerequisites(chapter_id)
  for each prerequisite topic:
    if practice_questions_completed(student_id, topic_id) < MIN_QUESTIONS:
      return LOCKED
    if avg_score(student_id, topic_id) < MIN_SCORE_PERCENT:
      return LOCKED
  return UNLOCKED
```
- MIN_QUESTIONS and MIN_SCORE_PERCENT configurable per institution

---

## 20. Accreditation & Compliance Exports

### 20.1 NAAC SSR Criterion 1 — Curriculum Design & Development
- Export: curriculum matrix (Programme → Course → CO → Unit → Topic)
- CO-PO mapping table
- Percentage of syllabus aligned to NEP 2020 / industry need
- Number of syllabus revisions per academic year
- Format: NAAC SSR prescribed table structure (Word / PDF)

### 20.2 NBA OBE Documentation
- CO-PO and CO-PSO mapping matrices
- Attainment report (direct + indirect methods)
- Rubric definitions per CO
- PO attainment level computation
- NBA criterion 3 auto-populated tables

### 20.3 AICTE Accreditation Report
- Model curriculum gap analysis table
- Credit distribution compliance table
- Programme category credit totals vs AICTE minimum
- Export as AICTE prescribed format

### 20.4 UGC AQAR Export
- Criterion 1: Curriculum and Learning Processes
- Number of new/revised courses
- Certificate / Diploma / Degree programs with NEP exit points
- Percentage of courses with LOs defined
- CBCS / OBE implementation status
- Export as NAAC IQAC prescribed Excel format

### 20.5 U-DISE+ Syllabus Data
- Board-wise subject list per grade per school
- Number of periods/week per subject (from Module 10 timetable)
- Medium of instruction per section
- Export in U-DISE+ school profile XML/Excel format

### 20.6 State DEO / Education Department Submissions
- Rajasthan: Shala Darpan syllabus completion report format
- UP: UDISE / PRERNA portal format
- MP: RSK (Rajya Shiksha Kendra) format
- Maharashtra: Saral format
- Tamil Nadu: EMIS format
- Other states: generic CSV with configurable column mapping
- All formats maintained in state compliance template library

### 20.7 NCVT MIS Reporting
- Unit-wise syllabus completion report for ITI trades
- Trade, unit code, hours planned vs delivered, instructor name
- Export to DGT portal CSV format

---

## 21. Syllabus Analytics Dashboard

### 21.1 Institution-Level Overview
- Total topics across all subjects and grades
- % covered overall, by grade, by subject, by teacher
- Teacher-wise coverage rank (highest to lowest)
- Grade-wise completion trend (line chart over months)
- Subjects at risk (< 70% coverage with < 60 days to exam)

### 21.2 Benchmark Comparison
- Anonymised peer cohort comparison:
  - Same board + grade + city tier (Metro / Tier-1 / Tier-2 / Tier-3)
  - Shows if institution pacing is Ahead / On Track / Behind vs cohort median
- Data aggregated anonymously across EduForge tenants
- Opt-in per institution (DPDPA 2023 compliant — institution data, not student data)

### 21.3 Topic Difficulty Heatmap
- Per subject: which topics generate most re-teach flags and low scores
- Identifies perennial weak spots in curriculum delivery
- HOD uses this to plan targeted teacher training

### 21.4 Syllabus vs Assessment Alignment Report
- For each unit: marks weightage in syllabus vs marks asked in last 3 internal exams
- Flags misalignment: over-testing low-weightage units, under-testing high-weightage units
- Actionable: helps teacher balance internal exam paper design

### 21.5 Assignment Export for Analytics
- Subject-wise: total assignments created, submitted, graded, pending
- Average score per topic, average submission time, average effort time
- Exportable as Excel for institution's academic committee review

---

## 22. Data Architecture

### 22.1 Tenancy
- All syllabus data tagged with `tenant_id` (PostgreSQL RLS)
- Master board/subject registry is platform-wide (shared, read-only per tenant)
- Institution syllabus records are tenant-isolated

### 22.2 Database Schema

```sql
-- Board/Curriculum Registry (platform-wide, read-only per tenant)
boards (
  board_id UUID PK,
  board_code VARCHAR(20),        -- CBSE, RBSE, UP_BOARD, etc.
  board_name VARCHAR(200),
  board_type VARCHAR(30),        -- SCHOOL | COLLEGE | COACHING | VOCATIONAL
  country VARCHAR(50) DEFAULT 'India',
  state VARCHAR(50),
  is_active BOOLEAN,
  created_at TIMESTAMPTZ
)

subjects_master (
  subject_id UUID PK,
  board_id UUID FK boards,
  subject_code VARCHAR(30),
  subject_name_en VARCHAR(200),
  subject_name_regional VARCHAR(200),
  medium VARCHAR(30),            -- ENGLISH | HINDI | REGIONAL
  category VARCHAR(30),          -- THEORY | PRACTICAL | COMPOSITE | VOCATIONAL | CO_CURRICULAR
  is_active BOOLEAN
)

-- Syllabus Hierarchy (tenant-scoped)
syllabi (
  syllabus_id UUID PK,
  tenant_id UUID FK tenants,
  branch_id UUID FK branches,
  board_id UUID FK boards,
  subject_id UUID FK subjects_master,
  grade_or_semester VARCHAR(20),
  academic_year_id UUID FK academic_years,
  medium VARCHAR(30),
  status VARCHAR(20),            -- DRAFT | REVIEW | APPROVED | PUBLISHED | LOCKED
  parent_syllabus_id UUID,       -- for branch-override child
  version INTEGER DEFAULT 1,
  cloned_from_syllabus_id UUID,
  locked_at TIMESTAMPTZ,
  locked_by UUID FK users,
  created_by UUID FK users,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)

syllabus_units (
  unit_id UUID PK,
  syllabus_id UUID FK syllabi,
  unit_code VARCHAR(20),
  unit_name_en VARCHAR(300),
  unit_name_regional VARCHAR(300),
  sequence_no INTEGER,
  marks_weightage NUMERIC(5,2),
  estimated_hours NUMERIC(5,1),
  nsqf_level INTEGER,            -- 1–8 for vocational
  created_at TIMESTAMPTZ
)

syllabus_chapters (
  chapter_id UUID PK,
  unit_id UUID FK syllabus_units,
  chapter_code VARCHAR(20),
  chapter_name_en VARCHAR(300),
  chapter_name_regional VARCHAR(300),
  sequence_no INTEGER,
  estimated_hours NUMERIC(5,1),
  ncert_chapter_ref VARCHAR(100),
  is_practical BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ
)

syllabus_topics (
  topic_id UUID PK,
  chapter_id UUID FK syllabus_chapters,
  topic_name_en VARCHAR(500),
  topic_name_regional VARCHAR(500),
  sequence_no INTEGER,
  bloom_level VARCHAR(20),       -- REMEMBER | UNDERSTAND | APPLY | ANALYSE | EVALUATE | CREATE
  difficulty_tag VARCHAR(20),    -- FOUNDATION | STANDARD | HIGHER | HOT
  estimated_minutes INTEGER,
  marks_weightage NUMERIC(4,2),
  is_nipun_fln BOOLEAN DEFAULT FALSE,
  nipun_competency_code VARCHAR(50),
  nsqf_nos_code VARCHAR(50),
  prerequisite_topic_ids UUID[],
  learning_outcomes TEXT[],
  nep_competency_tags TEXT[],
  is_enrichment BOOLEAN DEFAULT FALSE,
  is_remedial_only BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMPTZ
)

-- Coverage Tracking
topic_coverage_log (
  log_id UUID PK,
  tenant_id UUID FK tenants,
  topic_id UUID FK syllabus_topics,
  teacher_id UUID FK users,
  section_id UUID FK sections,
  date DATE,
  period_id UUID FK timetable_periods,
  status VARCHAR(20),            -- TAUGHT | SKIPPED | PARTIAL | RETEACH
  skip_reason TEXT,
  actual_minutes INTEGER,
  student_count INTEGER,
  attendance_percent NUMERIC(5,2),
  notes TEXT,
  created_at TIMESTAMPTZ
)

-- Annual Teaching Plan
annual_teaching_plan (
  atp_id UUID PK,
  tenant_id UUID FK tenants,
  syllabus_id UUID FK syllabi,
  section_id UUID FK sections,
  teacher_id UUID FK users,
  academic_year_id UUID FK academic_years,
  status VARCHAR(20),            -- DRAFT | HOD_APPROVED | ACTIVE
  generated_at TIMESTAMPTZ,
  approved_by UUID FK users,
  approved_at TIMESTAMPTZ
)

atp_entries (
  entry_id UUID PK,
  atp_id UUID FK annual_teaching_plan,
  topic_id UUID FK syllabus_topics,
  planned_date DATE,
  planned_period_id UUID FK timetable_periods,
  sequence_no INTEGER,
  is_revision BOOLEAN DEFAULT FALSE,
  rescheduled_from DATE,
  reschedule_reason TEXT
)

-- Lesson Plans
lesson_plans (
  plan_id UUID PK,
  tenant_id UUID FK tenants,
  topic_id UUID FK syllabus_topics,
  teacher_id UUID FK users,
  section_id UUID FK sections,
  academic_year_id UUID FK academic_years,
  template_type VARCHAR(30),
  objectives TEXT[],
  prior_knowledge TEXT,
  introduction_text TEXT,
  main_content_text TEXT,
  activities TEXT,
  assessment_method TEXT,
  resources TEXT,
  expected_duration_minutes INTEGER,
  status VARCHAR(20),            -- DRAFT | SUBMITTED | HOD_APPROVED | RETURNED
  reviewed_by UUID FK users,
  review_comments TEXT,
  reviewed_at TIMESTAMPTZ,
  cloned_from_plan_id UUID,
  created_at TIMESTAMPTZ,
  updated_at TIMESTAMPTZ
)

-- Accreditation Exports
syllabus_export_log (
  export_id UUID PK,
  tenant_id UUID FK tenants,
  export_type VARCHAR(50),       -- NAAC_SSR | NBA_OBE | AICTE | UGC_AQAR | UDISE | STATE_DEO | NCVT_MIS
  academic_year_id UUID FK academic_years,
  generated_by UUID FK users,
  generated_at TIMESTAMPTZ,
  file_path TEXT,
  status VARCHAR(20)             -- PENDING | READY | FAILED
)
```

### 22.3 Indexes
```sql
CREATE INDEX idx_topic_coverage_tenant_date ON topic_coverage_log(tenant_id, date);
CREATE INDEX idx_topic_coverage_teacher ON topic_coverage_log(teacher_id, topic_id);
CREATE INDEX idx_atp_entries_date ON atp_entries(atp_id, planned_date);
CREATE INDEX idx_lesson_plans_topic ON lesson_plans(topic_id, teacher_id);
CREATE INDEX idx_syllabus_topics_chapter ON syllabus_topics(chapter_id, sequence_no);
```

---

## 23. Roles & Permissions

| Action | Teacher | HOD | Principal | Academic Director | Admin |
|---|---|---|---|---|---|
| Create / Edit topics | Own subject | Department | All | All | All |
| Approve syllabus | — | ✅ | ✅ | ✅ | — |
| Lock syllabus | — | — | ✅ | ✅ | ✅ |
| Log topic coverage | ✅ | — | — | — | — |
| View coverage dashboard | Own | Department | All | All | All |
| Approve lesson plans | — | ✅ | View | View | — |
| Generate ATP | ✅ | ✅ | View | View | — |
| Export accreditation reports | — | — | ✅ | ✅ | ✅ |
| View parent/student syllabus | Read | Read | Read | Read | Read |

---

## 24. Notifications (In-App Only)

| Trigger | Recipient |
|---|---|
| Monthly pacing < 80% | HOD, Teacher |
| Topic flagged for re-teach | Teacher |
| Holiday rescheduled ATP | Teacher |
| Lesson plan returned by HOD | Teacher |
| Syllabus approved / published | Teacher, HOD |
| Uncovered topic 4 weeks before board exam | Principal, HOD, Teacher |
| Enrichment chapter unlocked for student | Student |
| New chapter available (prerequisite cleared) | Student |
| Syllabus completion certificate generated | Teacher, Principal |
| Accreditation export ready | Admin, Principal |

---

## 25. Compliance Summary

| Standard | Coverage in This Module |
|---|---|
| CBSE Curriculum Framework 2023 | Board-wise syllabus hierarchy, CCE marks, activity calendar, lesson plan mandate |
| NEP 2020 | OBE credit framework, multi-entry/exit, 21st-century competency tagging, spiral curriculum, digital literacy |
| UGC CBCS / LOCF | Credit-based syllabus, CO-PO mapping, AQAR export |
| AICTE Model Curriculum | Engineering curriculum gap analysis, credit category compliance |
| NBA OBE | CO-PO-PSO mapping matrix, attainment computation, criterion 3 tables |
| NAAC SSR Criterion 1 | Curriculum matrix export, % syllabus aligned to NEP, revision frequency |
| NCVT / DGT | NCVT MIS trade syllabus import, unit-wise hours, NOS codes, DGT export |
| NSQF (Level 1–8) | Level tagging per unit, PMKVY QP competency mapping, NSDC MIS export |
| NIPUN Bharat / FLN | Classes 1–3 competency code mapping, milestone tracking, DEO reporting |
| U-DISE+ | Subject list, medium of instruction, periods/week — annual data feed |
| Shala Darpan / PRERNA / EMIS | State-level syllabus completion report formats |
| RTE Act 2009 | No-detention Classes 1–8 note; CWSN adapted syllabus per Section 3 |
| RPWD Act 2016 | CWSN simplified LOs, modified assessment, separate tracking |
| DPDPA 2023 | Benchmark data anonymisation; parent access scoped to minors |
