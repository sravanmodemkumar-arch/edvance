# Page 27 — Question Bank Manager

**URL:** `/portal/product/question-bank/`
**Permission:** `product.manage_question_bank`
**Priority:** P1
**Roles:** PM Exam Domains, Content Manager, QA Engineer, UI/UX Designer (for question layout review)

---

## Purpose

Central management and governance interface for the SRAV platform's entire question bank — 2,000,000+ questions across 8 exam domains, 42 categories, and thousands of topics. While the Domain Analytics page (page 13) tracks how domains perform and the Exam Pattern Builder (page 10) defines exam structure, this page is where the PM Exam Domains team manages the content itself: reviewing questions for quality, approving new additions, managing the question review workflow, assigning content tasks to the content team, detecting duplicates, managing question difficulty calibration, and ensuring the question bank remains the platform's strongest competitive differentiator.

Core responsibilities:
- Browse, search, and filter 2M+ questions across all domains and categories
- Manage question quality review and approval workflow (Draft → Under Review → Approved → Published)
- Detect and resolve duplicate questions
- Score question difficulty and quality using multiple signals
- Assign content creation and review tasks to the content team
- Track question bank coverage gaps (topics with insufficient questions)
- Import questions from external sources (NCERT PDFs, previous year papers, partner question banks)
- Manage question versioning (corrections, option reorders, updated answer keys)
- Support multilingual questions (English, Hindi, and regional languages)
- Ensure DPDPA and copyright compliance for all question content

**Scale:**
- 2,000,000+ questions in the bank
- 8 exam domains: SSC / RRB / NEET / JEE / AP Board / TS Board / IBPS / SBI
- 42 categories with 200+ subjects and 2,000+ topics
- 800K+ monthly attempts providing quality signals
- Content team: 20–50 content writers and reviewers
- 1,950+ institutions rely on this question bank for their exam content

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Question Bank Manager"     [New Question]  [Import]  [Export] │
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards (auto-refresh every 300s)                  │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Browse · Review Queue · Coverage Gaps · Duplicates             │
│  Quality Analytics · Content Tasks · Import / Bulk · Audit Log  │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 6 Cards (auto-refresh every 300s)

| # | Label | Value | Colour | Delta | Click Action |
|---|---|---|---|---|---|
| 1 | Total Questions | All published + approved questions | — | vs last month | Opens Browse tab |
| 2 | Pending Review | Questions awaiting review in workflow | Amber if > 500 | — | Opens Review Queue |
| 3 | Coverage Gaps | Topics with < 50 questions (insufficient for quality exam) | Red if > 50 | — | Opens Coverage Gaps tab |
| 4 | Detected Duplicates | Pairs flagged as potential duplicates | Amber if > 100 | — | Opens Duplicates tab |
| 5 | Avg Quality Score | Average quality score across all published questions (0–100) | Green ≥80 · Amber 60–79 · Red <60 | vs last month | Opens Quality Analytics |
| 6 | Content Tasks Open | Open content creation/review tasks assigned to content team | — | — | Opens Content Tasks |

---

## Tab 1 — Browse

The primary interface for navigating and searching the question bank.

### Browse Layout: Left Sidebar + Main Panel

**Left Sidebar — Domain/Category/Topic Tree (280px)**

Collapsible hierarchical tree:
```
▶ SSC (CGL / CHSL / MTS)
   ▶ General Intelligence & Reasoning  [2,400 questions]
      ▶ Analogy  [320 q]
      ▶ Blood Relations  [180 q]
      ▶ Coding-Decoding  [240 q]
      ▶ Series  [290 q]
      ▶ Syllogism  [210 q]
      ▶ Direction Sense  [160 q]
      ▶ [30+ more sub-topics]
   ▶ General Awareness  [3,200 questions]
   ▶ Quantitative Aptitude  [4,100 questions]
   ▶ English Comprehension  [2,800 questions]
▶ RRB (NTPC / Group D / JE)
▶ NEET
   ▶ Physics  [8,200 questions]
   ▶ Chemistry  [7,400 questions]
   ▶ Biology  [10,800 questions]
▶ JEE (Main + Advanced)
   ▶ Mathematics  [9,400 questions]
   ▶ Physics  [8,800 questions]
   ▶ Chemistry  [7,200 questions]
▶ AP Board (Class 10–12)
▶ TS Board (Class 10–12)
▶ IBPS (PO / Clerk / SO)
▶ SBI (PO / Clerk)
```

Node label colour:
- Green: > 200 questions, avg quality ≥ 75
- Amber: 50–200 questions, or avg quality 60–74
- Red: < 50 questions (gap), or avg quality < 60

**Right Main Panel — Question List**

### Toolbar

| Control | Options |
|---|---|
| Search | Full-text search across question stem, options, and explanation (debounced 400ms) |
| Domain | Multi-select dropdown |
| Question Type | MCQ / MSQ / Integer / Fill-in-the-blank / Passage-based / Match-the-following |
| Difficulty | All / Very Easy / Easy / Medium / Hard / Very Hard |
| Language | All / English / Hindi / Telugu / Tamil / Malayalam / Kannada / Bengali / Marathi |
| Status | All / Draft / Under Review / Approved / Published / Deprecated |
| Source | All / SRAV Content Team / NCERT / Previous Year Paper / Partner Import / Institution Contributed |
| Quality Score | All / ≥80 / 60–79 / < 60 / Unscored |
| Used in Exams | Filter by usage count: Never used / Used ≥ 1 / Used ≥ 10 |
| Attempt Count | Low (<50) / Medium (50–500) / High (>500) |

### Question List Table — 12 columns

| Column | Detail |
|---|---|
| QID | Q-NNNNNN (click to open detail) |
| Question Stem | First 80 chars of question text |
| Domain | Domain badge |
| Subject / Topic | Breadcrumb |
| Type | MCQ / MSQ / Integer / etc. badge |
| Difficulty | Colour-coded badge: Very Easy (blue) / Easy (green) / Medium (amber) / Hard (orange) / Very Hard (red) |
| Language | Flag icon |
| Quality Score | 0–100 with colour bar |
| Status | Draft / Under Review / Approved / Published badge |
| Used In | Count of exams this question appears in |
| Attempt Count | Total student attempts |
| Actions | View · Edit · Clone · Flag as Duplicate · Archive |

**Row expand:** Shows full question text, all options with correct answer marked, explanation preview.

**Pagination:** Showing X–Y of Z questions · page pills · per-page selector (25 / 50 / 100 / 250)

### Question Detail Drawer (720px)

Opened by clicking any question or "View".

#### Drawer Tab 1 — Question Content

- **Domain / Subject / Topic:** Breadcrumb with edit button
- **Question Type:** MCQ / MSQ / Integer badge
- **Language:** English / Hindi / Regional
- **Difficulty tag:** Programmatic (calculated) + Manual override
- **Cognitive level (Bloom's taxonomy):** Recall / Understanding / Application / Analysis / Synthesis
- **Question stem:** Full text rendered with MathJax (for equations), image thumbnails
- **Options (for MCQ/MSQ):** A / B / C / D with correct answer(s) marked
- **Correct answer:** Green tick marks
- **Explanation:** Full explanation text with step-by-step working
- **Hint** (optional): One-line hint for practice mode
- **Reference:** NCERT Chapter / Previous Year (exam + year) / Textbook chapter reference

#### Drawer Tab 2 — Quality Signals

How the quality score is calculated for this question:

| Signal | Weight | Current Value | Score Contribution |
|---|---|---|---|
| Discrimination Index | 25% | 0.42 | 10.5/25 |
| Avg Correct Rate (target 40–70%) | 20% | 58% | 16/20 |
| Distractor Performance (all options selected) | 15% | 3/4 distractors active | 12/15 |
| Explanation Quality (length + clarity rating) | 15% | Good | 12/15 |
| Reviewer Rating | 20% | 4.2/5 | 16.8/20 |
| Language & Grammar check | 5% | No issues | 5/5 |
| **Total Quality Score** | 100% | — | **72.3 / 100** |

**Discrimination Index:** measures how well the question distinguishes strong from weak students (0 = no discrimination; 1 = perfect discrimination). Calculated from attempt data. Target: > 0.3.

**Distractor Performance:** For MCQ, ideally all 3 wrong options are each selected by at least 5% of students. "Dead distractors" (selected by < 2%) reduce quality score.

**Manual reviewer rating:** Content reviewers can rate questions 1–5 stars. Average of all ratings shown.

#### Drawer Tab 3 — Usage Analytics

- **Total attempt count:** across all time
- **Correct rate:** % of attempts where student got the correct answer
- **Avg time to answer:** seconds (vs topic average)
- **Usage in exams:** table of all exam series/exams that use this question (exam name · institution type · date range)
- **Trend chart:** monthly attempt count over last 12 months. Detects if question is overexposed (same students seeing it repeatedly).
- **Overexposure warning:** if question has been seen by > 60% of students in its primary domain, amber warning shown.

#### Drawer Tab 4 — Versions

All versions of this question (edits, corrections):

| Version | Date | Changed By | Change Summary | Status |
|---|---|---|---|---|
| v1.0 | 12 Jan 2025 | Ramesh Kumar | Initial creation | Archived |
| v1.1 | 3 Mar 2025 | Priya Sharma | Corrected option C (typo fix) | Archived |
| v2.0 | 15 Jan 2026 | Kavya Nair | Updated explanation with new NCERT reference | Published |

"Restore version" button: creates a new Draft from an older version.

#### Drawer Tab 5 — Review Activity

Full history of all review actions:
- Created by (content writer, date)
- Submitted for review
- Reviewer A: Approved (with notes)
- Reviewer B: Requested changes (reason: "Option D is ambiguous")
- Updated by content writer (v1.1 created)
- Published by PM Exam Domains (date)
- Later: flagged for difficulty recalibration (date)

---

## Tab 2 — Review Queue

Questions that have been submitted and are awaiting quality review before being approved and published.

### Queue Summary Cards (4 cards)

| Card | Value |
|---|---|
| Awaiting First Review | Questions not yet assigned to a reviewer |
| Assigned to Me | Questions where logged-in user is the assigned reviewer |
| In Review | Questions actively being reviewed |
| Avg Time in Queue | Average days questions wait before review (target: < 3 days) |

### Review Queue Table

| Column | Detail |
|---|---|
| QID | Q-NNNNNN |
| Question Stem | First 80 chars |
| Domain / Subject | Breadcrumb |
| Type | Badge |
| Language | Flag |
| Submitted By | Content writer name |
| Submitted On | Date (amber if > 3 days waiting) |
| Assigned Reviewer | Name or "Unassigned" |
| Days in Queue | Count |
| Actions | Review · Assign · Skip (to back of queue) |

### Review Workflow

When a reviewer clicks "Review":
- Full question shown (same as drawer Tab 1)
- **Review panel on right:** checklist + rating + actions

**Review Checklist:**
- [ ] Question stem is grammatically correct
- [ ] Question is unambiguous (only one valid interpretation)
- [ ] Correct answer is accurate (reviewer has verified)
- [ ] All incorrect options are clearly incorrect
- [ ] Explanation is accurate and sufficient
- [ ] Difficulty tag is appropriate (easy/medium/hard)
- [ ] No copyright issues (not a verbatim copy of copyrighted material)
- [ ] Language is appropriate for target exam level
- [ ] Image quality (if question contains image) is adequate

**Rating:** 1–5 stars (mandatory)
**Notes:** Free text (optional for Approve; required for Request Changes)

**Actions:**
- **Approve** → question moves to "Approved" (published after PM Exam Domains confirms)
- **Request Changes** → returns to content writer with specific change requests
- **Reject** → question rejected (reason required); cannot be resubmitted without creating a new question
- **Escalate to PM** → flags for PM Exam Domains to review (for difficult/borderline cases)

### Reviewer Assignment Rules

- Questions are auto-assigned to reviewers based on domain expertise tags on reviewer profiles
- Max 50 questions in review per reviewer at one time (backlog protection)
- If unassigned for > 48 hours: PM Exam Domains receives in-app alert
- Self-review not allowed: content writer cannot review their own questions

---

## Tab 3 — Coverage Gaps

Identifies areas of the question bank that need more questions to adequately cover the exam domain.

### Coverage Gap Definition

A topic is "under-covered" if it has fewer than the required minimum question count:

| Exam Type | Minimum Questions per Topic | Reason |
|---|---|---|
| Competitive (SSC/RRB/IBPS/SBI) | 100 questions | Topic may be tested across 10 exam sets needing 10 distinct questions each |
| Medical (NEET) | 150 questions | NEET is highly standardised; broad coverage required |
| Engineering (JEE) | 150 questions | JEE Advanced requires high variety |
| Board Exams (AP/TS Board) | 80 questions | Syllabus is fixed; lower variety needed |

### Coverage Gaps Table

| Domain | Subject | Topic | Questions Available | Required | Gap | Priority | Actions |
|---|---|---|---|---|---|---|---|
| SSC | Quantitative Aptitude | Data Interpretation — Table | 42 | 100 | 58 | High | Create Task |
| NEET | Biology | Human Endocrine System | 65 | 150 | 85 | Critical | Create Task |
| JEE | Mathematics | Differential Equations | 88 | 150 | 62 | High | Create Task |
| IBPS | Reasoning | Puzzles — Floor Arrangement | 35 | 100 | 65 | Critical | Create Task |

Sorted by gap size descending by default.

**Priority Calculation:**
- Critical: gap > 50% of required (< 50 when need 100, or < 75 when need 150)
- High: gap 25–50% of required
- Medium: gap < 25% of required

**"Create Task" button:** opens Content Task creation form (pre-filled with domain, subject, topic, count needed).

### Coverage Heatmap

Grid: Subject (rows) × Difficulty Level (columns). Cell = question count. Green = adequate · Amber = borderline · Red = gap.

Shows distribution gaps: e.g. SSC Quant has 4,100 questions but 90% are Easy/Medium with almost no Hard questions — students preparing for SSC CGL Tier 2 are under-served.

---

## Tab 4 — Duplicates

Duplicate detection to maintain question bank quality and prevent students from seeing the same question repeatedly.

### Duplicate Detection Method

Questions are flagged as potential duplicates if:
- **Exact match:** Question stem is identical (after normalising whitespace and punctuation)
- **Near-duplicate:** Question stem is > 85% similar (using fuzzy string matching + NLP similarity)
- **Same question, different format:** e.g. same calculation question in different units or framing

Duplicate detection runs nightly as a Celery scheduled task. New pairs added to Duplicates tab for human review.

### Duplicate Pairs Table

| Pair | Question 1 | Question 2 | Similarity | Status | Actions |
|---|---|---|---|---|---|
| DP-1042 | "A train travels 240km in 4 hours..." [SSC] | "A train covers 240km in 4 hours..." [SSC] | 96% | Pending | Review · Mark as Duplicate · Mark as Different |
| DP-1041 | "If A:B = 2:3 and B:C = 4:5..." [IBPS] | "If A:B = 2:3 and B:C = 4:5..." [SSC] | 100% | Pending | Review · Mark as Duplicate · Mark as Different |

**"Review" button:** Opens comparison view (side-by-side both questions with all options and explanations).

**"Mark as Duplicate" button:** Selects which version to keep (the higher quality score version is suggested). The lower-quality version is deprecated.

**"Mark as Different" button:** Confirms both questions are intentionally different (different options, different correct answers, or different context). Removes from duplicates list.

---

## Tab 5 — Quality Analytics

Analytics to understand and improve question bank quality over time.

### Quality Score Distribution

Histogram: distribution of all published questions by quality score. X-axis: score buckets (0–10 / 10–20 / ... / 90–100). Shows what proportion of the question bank is high-quality vs needs improvement.

### Quality by Domain

Bar chart: average quality score per domain. Identifies which domains need most quality improvement attention.

| Domain | Avg Quality Score | Total Questions | High Quality (≥80) | Need Improvement (<60) |
|---|---|---|---|---|
| SSC | 72.4 | 380,000 | 45% | 12% |
| NEET | 81.2 | 280,000 | 68% | 4% |
| JEE | 78.9 | 250,000 | 60% | 7% |
| RRB | 68.1 | 190,000 | 38% | 18% |
| IBPS | 70.5 | 160,000 | 41% | 15% |
| AP Board | 65.2 | 140,000 | 32% | 22% |

### Difficulty Distribution

Stacked bar chart: question count by difficulty level per domain. Should follow a bell curve (fewer Very Easy and Very Hard; most in Medium).

### Content Team Performance

| Content Writer | Questions Submitted (30d) | Approval Rate | Avg Quality Score | Avg Review Cycles |
|---|---|---|---|---|
| Ramesh Kumar | 142 | 94% | 76.2 | 1.2 |
| Priya Sharma | 98 | 88% | 79.8 | 1.6 |
| Kavya Nair | 201 | 96% | 82.1 | 1.1 |

### Discrimination Index Analysis

Distribution chart: histogram of discrimination index values across all questions. Questions with discrimination index < 0.2 flagged for review (poor at differentiating strong vs weak students).

---

## Tab 6 — Content Tasks

Task management for the content team. PM Exam Domains assigns tasks to content writers and tracks completion.

### Task Table

| Column | Detail |
|---|---|
| Task ID | CT-NNNN |
| Title | Descriptive task name (e.g. "Create 50 Hard questions: NEET Biology — Genetics") |
| Domain / Subject / Topic | Target area |
| Type | Create / Review / Update / Translate / Recalibrate Difficulty |
| Assigned To | Content writer name |
| Target Count | Number of questions to create or review |
| Completed Count | Questions completed so far (progress bar) |
| Due Date | Target completion date |
| Priority | High / Medium / Low badge |
| Status | Not Started / In Progress / Completed / Overdue |
| Actions | View · Edit · Reassign · Close |

**Pagination:** 25 / 50 / 100 per page.

### Create Content Task Modal

Fields:
- Task title (required)
- Task type: Create / Review / Update / Translate / Recalibrate
- Domain (required)
- Subject (required)
- Topic (optional — for focused tasks)
- Difficulty target (for Create tasks): Easy / Medium / Hard / Any
- Language (for Translate tasks): target language
- Target count (required, numeric)
- Assigned to (dropdown of content team members)
- Due date (date picker)
- Priority: High / Medium / Low
- Notes: additional instructions for the writer
- Link to Coverage Gap (optional — auto-populates from Coverage Gaps tab)

### Content Task Detail Drawer (640px)

**Tab 1 — Task Details:** All fields as created, with edit capability.

**Tab 2 — Submitted Questions:** List of questions submitted against this task. Shows QID · status · quality score. Progress: "32 of 50 submitted, 28 approved."

**Tab 3 — Notes:** Thread of notes between PM and content writer.

---

## Tab 7 — Import / Bulk

Bulk operations for large-scale question bank management.

### Import Sources

| Source Type | Format | Description |
|---|---|---|
| CSV Upload | SRAV Question CSV format | Bulk import from spreadsheets. Download CSV template with all required columns. |
| PDF Scan (OCR) | PDF / scanned image | Upload previous year question paper PDF → OCR extracts questions and options → PM reviews and approves extracted questions |
| Partner Question Bank API | JSON (partner format) | Authorised partners can push questions via API with domain/subject/topic metadata |
| NCERT Textbook Questions | PDF → structured extract | NCERT chapter-end questions and exercises imported after copyright clearance |
| Institution Contributed | Moderated submission | Institutions that generate their own questions can contribute to the shared bank (moderated before publishing) |

### CSV Import Template Columns

QID (leave blank for new) · Domain · Subject · Topic · QuestionType · Difficulty · Language · QuestionStem · OptionA · OptionB · OptionC · OptionD · CorrectAnswer · Explanation · Source · CopyrightClearance (Yes/No) · CognitiveLevel

### Import Process

1. Upload file (drag-and-drop or file picker)
2. Column mapping dialog (auto-mapped; manual adjustment available)
3. Validation: errors shown per row (missing required fields, invalid difficulty value, unknown topic, etc.)
4. Preview first 10 rows (full question rendering)
5. Choose import mode: Add to Review Queue / Add as Draft (for internal review before queue)
6. Confirm import → questions created (async Celery job for large files)
7. Import summary notification: X created · Y skipped (duplicates) · Z errors

### Bulk Operations

With questions selected in Browse tab:

| Bulk Action | Detail |
|---|---|
| Change Difficulty | Update difficulty tag for all selected |
| Archive | Archive all selected (with confirmation; must not be in active exams) |
| Assign to Content Task | Link selected to a content task for review or update |
| Export | Download as CSV / JSON / PDF |
| Submit for Review | Move all selected Drafts to Review Queue |
| Add to Exam | Add selected questions to an exam (links to Exam Creator) |
| Flag as Duplicate Set | Manually flag a group as duplicates for human review |

---

## Tab 8 — Audit Log

### Filters

- Date range (default: last 30 days)
- Actor: admin / content writer name
- Action type: Question Created / Question Approved / Question Rejected / Question Deprecated / Question Edited / Question Imported / Task Created / Task Completed / Duplicate Resolved / Coverage Gap Created
- Domain

### Audit Table

| Timestamp | Actor | Action | QID / Task | Detail |
|---|---|---|---|---|
| 20 Mar 2026, 10:34 | Kavya Nair | Question Approved | Q-482901 | "Approved NEET Biology question after 2 review cycles" |
| 20 Mar 2026, 09:12 | Ramesh Kumar | Question Submitted | Q-483100 | "New SSC Quant question submitted for review" |
| 19 Mar 2026, 16:40 | PM Exam Domains | Task Created | CT-1042 | "50 Hard IBPS Puzzles assigned to Priya Sharma, due Apr 1" |

CSV export. Pagination: 25 / 50 / 100.

---

## Question Types Supported

| Type | Description | Question Display | Answer Capture |
|---|---|---|---|
| MCQ (Single Correct) | One correct answer among 4 options | Radio buttons | 1 selection |
| MSQ (Multiple Correct) | One or more correct answers | Checkboxes | Multiple selections |
| Integer Type | Exact numeric answer | Numeric input (no options shown) | Number entry |
| Fill in the Blank | Complete the sentence | Text input or word bank | Text entry |
| Passage-Based | Multiple questions share a single passage | Passage shown above; questions below | Per-question MCQ |
| Match the Following | Match Column I to Column II | Two columns with 4–6 items each | Dropdown mapping |
| True/False | Binary choice | Two radio options | 1 selection |
| Assertion-Reason | Statement + reasoning format | Two statements shown | MCQ (5 options) |

---

## Difficulty Calibration

Question difficulty is both manually tagged and algorithmically calculated:

### Manual Difficulty Tag

Set by content writer at creation time. Based on curriculum level and expected student performance.

### Algorithmic Difficulty Calculation

After 50+ attempts on a question, the system calculates:
- **Correct rate:** % of students who got it right
- **Calibrated difficulty:**
  - > 80% correct rate → Recalibrate to Easy (regardless of manual tag)
  - 60–80% → Easy
  - 40–60% → Medium
  - 20–40% → Hard
  - < 20% → Very Hard

**Conflict alert:** When algorithmic difficulty disagrees with manual tag by more than 1 level, a yellow "Recalibrate" badge appears on the question and it's added to a recalibration task queue.

PM Exam Domains reviews recalibration suggestions weekly and bulk-approves or overrides.

---

## Copyright and Source Management

Every question has a mandatory source field:

| Source Type | Copyright Clearance Required | Behaviour |
|---|---|---|
| SRAV Original | No (SRAV owns) | Standard publish |
| NCERT (textbook) | No (NCERT is open) | Tag with NCERT chapter reference |
| Previous Year Paper (government exams) | No (government papers are public domain in India) | Tag with exam, year, question number |
| Competitive content partner | Yes (partner agreement required) | Import only after PM approves partnership agreement |
| Institution contributed | Institutional agreement | Institution must grant SRAV right to use; signed during onboarding |
| Unknown source | Not allowed | Questions without clear source cannot be published |

**Copyright flag:** If a content writer flags a question as "source unclear," it is placed in a "Copyright Review" sub-queue and cannot be published until source is confirmed.

---

## Integration Points

| Page | Integration |
|---|---|
| Page 13 — Domain Analytics | Domain analytics shows question bank health metrics per domain. Coverage gaps flagged here appear in domain analytics. Question quality scores roll up to domain health score. |
| Page 10 — Exam Pattern Builder | Exam patterns specify how many questions per subject/topic/difficulty. Question bank must have sufficient approved questions in each bucket to fulfil the pattern. Unfulfillable patterns are flagged with "insufficient questions in Q bank" warning. |
| Page 11 — Test Series Manager | Test series pull questions from this bank. Series with questions from deprecated questions are flagged for review. |
| Page 14 — Portal Feature Config | Institution Question Contribution feature flag controls whether institutions can submit questions to the shared bank. |
| Page 26 — Automation Monitor | Question import pipelines and nightly duplicate detection jobs are visible in Automation Monitor. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Two-panel tree + list | Domain tree + filtered list | 2M+ questions require hierarchical navigation; flat search alone is insufficient for domain experts |
| Algorithmic difficulty calibration | Real attempt data overrides manual tagging | Content writers systematically underestimate difficulty; attempt data provides objective calibration |
| Quality score multi-signal | 6 factors weighted | Single correct-rate metric misses explanation quality, distractor health; multi-signal is more robust |
| Discrimination index tracking | Key quality signal | Questions that don't differentiate strong/weak students are low-value for competitive exam prep |
| Nightly duplicate detection | Automated, human-confirmed | Manual duplicate detection of 2M+ questions is impossible; automation surfaces; human confirms |
| Overexposure warning | > 60% of students seen question | Students retaking practice see same questions; overexposed questions give inflated scores |
| Copyright field mandatory | Cannot publish without source | IP protection and compliance risk — unknowing copyright infringement is a serious business risk |
| Difficulty recalibration alert | Conflict between manual and algorithmic | Keeps difficulty tags accurate without requiring PM to manually audit all 2M+ questions |
| Review queue max 50 per reviewer | Reviewer backlog protection | More than 50 unreviewed questions per reviewer leads to reviewer burnout and quality degradation |
| Bloom's taxonomy cognitive level | Additional classification | Competitive exam prep needs all levels; tracking ensures balance between recall and application questions |
| Content team performance metrics | Visible to PM, not used punitively | Identifies training needs, not for HR evaluation; team lead insight only |
| Institution-contributed questions | Moderated before publishing | Institutions may contribute low-quality or copyrighted content; moderation gate is essential |

---

## Amendment G9 — Content Flags Tab

**Gap:** No workflow for user-reported question errors. Students and teachers flag questions with typos, incorrect answers, misleading distractors, or broken images — but there is no PM-facing interface to review, act on, or close these flags. Flagged questions accumulate without resolution.

### New Tab: "Content Flags"

Added to the Tab Bar after `Review Queue`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ CONTENT FLAGS                       Filter: [All ▼] [Unresolved ▼] [Domain ▼] │
│ User-reported question errors requiring PM review                               │
│                                                                     [Export CSV]│
├─────────────────────────────────────────────────────────────────────────────────┤
│ Summary: 47 Open · 12 In Review · 284 Resolved (last 30 days)                  │
├───────────────────────────────────────────────────────────────────────────────────┤
│ FLAG LIST                                                                        │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ #FL-2892  OPEN   ⚠️ Wrong Answer Key                         3 reports      │ │
│ │ Question: "In SSC CGL 2023 Tier 1, Q47 — The correct answer..."             │ │
│ │ Domain: SSC > CGL > Quantitative Aptitude > Time & Work                     │ │
│ │ Reported by: 2 students, 1 teacher  |  First flagged: 2026-03-18            │ │
│ │ Flag reason: "Answer key shows B but correct answer is C — verified in..."  │ │
│ │ [View Question] [Assign to Reviewer] [Mark: Duplicate] [Dismiss]           │ │
│ ├─────────────────────────────────────────────────────────────────────────────┤ │
│ │ #FL-2891  IN REVIEW   🖼️ Broken Image                       1 report       │ │
│ │ Question: "Identify the geometric figure shown in..."                        │ │
│ │ Domain: NEET > Biology > Cell Biology                                        │ │
│ │ Assigned to: Ravi (Content Team) since 2026-03-19                           │ │
│ │ [View Question] [View Review Notes] [Escalate] [Close — Fixed]             │ │
│ ├─────────────────────────────────────────────────────────────────────────────┤ │
│ │ #FL-2889  OPEN   📝 Typo / Grammar                          1 report       │ │
│ │ Question: "The treaty of Versalles was signed in..."                         │ │
│ │ Domain: SSC > CGL > General Awareness > History                             │ │
│ │ Reported by: 1 student  |  First flagged: 2026-03-20                        │ │
│ │ [View Question] [Assign to Reviewer] [Dismiss]                             │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Flag Detail Drawer (560px right)

Clicking `[View Question]` or any flag opens a detail drawer:

```
┌──────────────────────────────────────────────────────────┐
│ Flag #FL-2892 — Wrong Answer Key           [×]            │
├──────────────────────────────────────────────────────────┤
│ QUESTION PREVIEW                                          │
│ [Full question text with options A/B/C/D rendered]       │
│ Answer key: B (stored) | Most-reported correct: C        │
│                                                          │
│ REPORTS (3)                                              │
│  Student #1 (2026-03-18 14:22): "Answer is C, not B.    │
│    Refer RRB RRB-NTPC 2022 official answer key."        │
│  Student #2 (2026-03-19 09:10): "Confirmed wrong."      │
│  Teacher (IIT Delhi Coaching) (2026-03-19 16:40):       │
│    "This is a known error. Answer C is correct."        │
│                                                          │
│ REVIEW NOTES                                             │
│  [Textarea — PM / Content team notes on this flag]      │
│                                                          │
│ ACTIONS                                                  │
│  Assign to: [Content Team Member ▼]                     │
│  Resolution:                                             │
│  ○ Fix Answer Key → new correct option: [C ▼]          │
│  ○ Edit Question Text → opens question editor           │
│  ○ Replace Image → upload new image                     │
│  ○ Retire Question → move to archive, replace in exams  │
│  ○ Dismiss (Not a bug) → reason required                │
│                                                          │
│ [Save Review Notes] [Apply Resolution & Close Flag]      │
└──────────────────────────────────────────────────────────┘
```

### Flag Workflow States

```
Reported → Open → [Assign] → In Review → [Apply Fix] → Resolved
                           ↘ [Duplicate] → Closed (linked to original)
                           ↘ [Dismiss] → Closed (reason logged)
```

### Auto-escalation Rules

- Flag with ≥ 5 reports and status still `Open` after 48h → auto-escalates to `High Priority` (amber badge)
- Flag with ≥ 10 reports → auto-escalates to `Critical` (red badge), email sent to PM Platform lead
- `Wrong Answer Key` flags with ≥ 3 reports → question auto-tagged `answer_disputed`; exam results using this question flagged for re-evaluation

### Models Added

```python
class QuestionFlag(models.Model):
    FLAG_TYPE = [
        ('wrong_answer', 'Wrong Answer Key'),
        ('broken_image', 'Broken Image'),
        ('typo', 'Typo / Grammar'),
        ('misleading_distractor', 'Misleading Distractor'),
        ('outdated_content', 'Outdated Content'),
        ('other', 'Other'),
    ]
    STATUS = [
        ('open', 'Open'),
        ('in_review', 'In Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
        ('duplicate', 'Duplicate'),
    ]
    PRIORITY = [
        ('normal', 'Normal'),
        ('high', 'High Priority'),
        ('critical', 'Critical'),
    ]

    question = models.ForeignKey(
        'questions.Question', on_delete=models.CASCADE, related_name='flags'
    )
    flag_type = models.CharField(max_length=30, choices=FLAG_TYPE)
    status = models.CharField(max_length=15, choices=STATUS, default='open')
    priority = models.CharField(max_length=10, choices=PRIORITY, default='normal')
    report_count = models.PositiveIntegerField(default=1)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='assigned_flags'
    )
    review_notes = models.TextField(blank=True)
    resolution_type = models.CharField(max_length=30, blank=True)
    dismiss_reason = models.TextField(blank=True)
    duplicate_of = models.ForeignKey(
        'self', on_delete=models.SET_NULL, null=True, blank=True
    )
    resolved_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='resolved_flags'
    )
    first_reported_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-report_count', '-first_reported_at']
        indexes = [
            models.Index(fields=['status', 'priority', '-report_count']),
            models.Index(fields=['question', 'status']),
        ]


class QuestionFlagReport(models.Model):
    """Individual user report linked to a flag."""
    REPORTER_TYPE = [('student', 'Student'), ('teacher', 'Teacher'), ('institution_admin', 'Institution Admin')]

    flag = models.ForeignKey(QuestionFlag, on_delete=models.CASCADE, related_name='reports')
    reporter_type = models.CharField(max_length=20, choices=REPORTER_TYPE)
    reporter_id = models.IntegerField()  # ID in respective model
    institution = models.ForeignKey(
        'institutions.Institution', on_delete=models.SET_NULL, null=True
    )
    report_text = models.TextField()
    reported_at = models.DateTimeField(auto_now_add=True)
```

### Celery Task for Auto-escalation

```python
@shared_task(queue='content')
def auto_escalate_content_flags():
    """Runs every hour via Celery beat."""
    now = timezone.now()

    # Escalate to high priority
    QuestionFlag.objects.filter(
        status='open',
        priority='normal',
        report_count__gte=5,
        first_reported_at__lte=now - timedelta(hours=48),
    ).update(priority='high')

    # Escalate to critical + notify
    critical_flags = QuestionFlag.objects.filter(
        status__in=['open', 'in_review'],
        priority__in=['normal', 'high'],
        report_count__gte=10,
    )
    for flag in critical_flags:
        flag.priority = 'critical'
        flag.save(update_fields=['priority'])
        notify_critical_flag.delay(flag.id)

    # Mark answer_disputed on wrong-answer flags with 3+ reports
    QuestionFlag.objects.filter(
        flag_type='wrong_answer',
        report_count__gte=3,
        status__in=['open', 'in_review'],
    ).select_related('question').update(
        # tag applied to question model via signal
    )
```
