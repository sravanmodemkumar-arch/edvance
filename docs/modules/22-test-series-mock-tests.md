# Module 22 — Test Series & Mock Tests

## 1. Purpose
Provide a full-featured, exam-day–accurate mock testing platform covering every major Indian
competitive exam (JEE, NEET, UPSC, State PSC, Banking, SSC, Railways, CUET, GATE, CA/CS/CMA,
Olympiads, NTSE, ITI/NCVT), school board revision series, and coaching custom series. All test
interfaces simulate the real exam environment exactly — NTA colour palette, section timers,
partial marking, negative marking, bilingual toggle, NAT input — with instant analytics, All-India
ranking, adaptive mock generation, PYP library, answer key dispute workflow, and deep integration
with Modules 14–21.

---

## 2. Test Series Management

### 2.1 Test Series Entity
- Name, target exam, total test count, schedule type (weekly / bi-weekly / monthly / custom),
  validity start date, validity end date, tenant_id.
- Series status: DRAFT → PUBLISHED → ACTIVE → COMPLETED → ARCHIVED.
- Series cloning: duplicate an existing series; modify for new batch or new academic year.
- Multi-batch assignment: one series assigned to multiple batches simultaneously with independent
  schedule windows per batch.

### 2.2 Test Types
| Type | Description |
|---|---|
| Full-Length Mock Test (FLT) | Complete exam simulation — all sections, full duration, all question types |
| Part Test (PT) | Subset of syllabus — 2–3 chapters; shorter duration |
| Chapter Test (CT) | Single chapter; 20–40 questions |
| Subject Test (ST) | One subject; all chapters covered so far in batch |
| Previous Year Paper (PYP) | Actual past exam paper; exam mode or practice mode |
| Sectional Test | One section of the target exam only |
| Daily Practice Test (DPT) | 20 questions; auto-generated daily from current syllabus position |
| Adaptive Booster Test | Auto-generated from student's weakest chapters |
| Pre-Exam Revision Test | High-weightage topics + weak areas; generated 7 days before target exam |
| Interview / GD Mock | Subjective; evaluator-marked (UPSC/Bank PO/Campus) |

### 2.3 Target Exam Library (Pre-loaded by EduForge Content Team)
**Engineering & Medical**
- JEE Main (NTA pattern, all shifts Jan/Apr, bilingual)
- JEE Advanced (Paper 1 + Paper 2, IIT pattern, English only)
- NEET UG (NTA pattern, 4 sections, bilingual)
- NEET PG / MDS (NBE pattern)
- BITSAT, VITEEE, SRMJEEE, MH-CET Engineering, KCET, KEAM, WBJEE, AP/TS EAMCET

**Civil Services & Administrative**
- UPSC CSE Pre (GS + CSAT), Mains (GS I–IV + Essay + Optional), Interview
- State PSC: RPSC RAS, UPPSC PCS, MPSC, KPSC, TNPSC Group I/II/IV, APPSC, TSPSC,
  BPSC, JPSC, GPSC, OPSC, HPSC, PPSC, MPPSC, CGPSC, JKPSC, UKPSC, Goa PSC, Manipur PSC
- Revenue & Patwari: Rajasthan Patwari, UP Lekhpal, MP Patwari, Gram Sevak
- State SI / Constable written exam patterns (all states)
- Panchayati Raj exams (state-specific)

**Banking & Finance**
- IBPS PO, Clerk, SO, RRB Officer Scale I/II/III, RRB Office Assistant
- SBI PO, Clerk, Junior Associate
- RBI Grade B (Phase I + II), RBI Assistant
- NABARD Grade A/B, SEBI Grade A
- LIC AAO, ADO, HFL, GIC AO
- NIACL AO/Assistant, UIIC AO

**SSC & Railways**
- SSC CGL Tier I/II/III/IV, CHSL, MTS, CPO, GD Constable
- RRB NTPC (CBT 1 + CBT 2), Group D, ALP + Technician, JE
- RPF SI / Constable

**Defence & Paramilitary**
- NDA (Maths + GAT), CDS (English + GK + Maths), AFCAT
- CAPF (AC), BSF, CRPF, CISF written patterns

**Entrance Exams**
- CUET UG (Domain + Language + General Test) and CUET PG
- CLAT, AILET, LSAT India, MH-CET Law
- MAT, CAT, XAT, SNAP, NMAT, CMAT, IIFT
- GATE (all 30 papers: CS, EC, ME, CE, EE, CH, IN, PI, BT, AE, AG, etc.)
- NTA UGC NET/JRF (all 83 subjects), CSIR NET (5 subjects), SET/SLET (state-wise)

**Professional Courses**
- CA Foundation, Inter (Group I/II), Final (Group I/II) — ICAI pattern
- CS Foundation, Executive (Module I/II), Professional — ICSI pattern
- CMA Foundation, Inter, Final — ICMAI pattern
- B.Ed / D.El.Ed entrance (state-wise — DUET, MP B.Ed CET, etc.)
- NEET MDS, AIAPGET (Ayurveda PG)

**Teaching**
- CTET Paper I (Classes 1–5) and Paper II (Classes 6–8)
- All state TETs (UPTET, REET, HTET, MPTET, MAHA-TET, APTET, TSTET, Karnataka TET, etc.)
- KVS PGT/TGT/PRT, NVS, DSSSB

**School & Olympiad**
- CBSE Class 6–12 board revision series (all subjects)
- All 28 state board SSC / HSC / SSLC revision series
- NTSE Stage I (state) + Stage II (national) — MAT + SAT
- SOF Olympiads: NSO, IMO, IEO, ICO, ISSO, IGKO (Class 1–12)
- Silverzone, Unified Council, Humming Bird olympiads
- NMMS (Class 8)
- Sainik School AISSEE (Class 6 + Class 9)
- Pre-RMO / RMO (Regional Mathematical Olympiad — subjective)
- KVPY / INSPIRE-SHE aptitude test

**Vocational & Skill**
- NCVT ITI trade tests (150+ trades: Electrician, Fitter, Welder, COPA, Machinist, Plumber,
  Mechanic Motor Vehicle, Electronic Mechanic, Draughtsman, etc.)
- NSQF Level 1–8 competency assessments
- PMKVY sector-wise assessments (BFSI, Healthcare, Construction, Beauty & Wellness, Retail,
  Logistics, Tourism, Media, Agriculture, Apparel, etc.)
- DDU-GKY trade assessment mocks
- RPL (Recognition of Prior Learning) competency checks

---

## 3. Exam Pattern Configuration

### 3.1 Pre-loaded Patterns (Key Exams)

**JEE Main (NTA)**
- 3 sections: Physics / Chemistry / Mathematics
- 30 questions each: Section A (20 MCQ, +4/−1) + Section B (10 Integer, +4/0, attempt any 5)
- Total: 90 questions, 300 marks, 180 minutes
- Free movement between sections; question palette per section
- Bilingual: English + Hindi toggle

**JEE Advanced (IIT)**
- Paper 1 + Paper 2 (3 hours each); separate attempt sessions
- Question types per paper: Single Correct MCQ (+3/−1), Multiple Correct MCQ (+4 all correct /
  partial: +3 for 3 correct / +2 for 2 correct / +1 for 1 correct / −2 for incorrect),
  Integer (0–9, +3/0), Matching (+3/0 per row), Paragraph-based (MCQ on given passage)
- No section-level time limit within each paper

**NEET UG (NTA)**
- 4 sections: Physics / Chemistry / Botany / Zoology
- 50 questions each: Section A (35 MCQ mandatory) + Section B (15 MCQ, attempt any 10)
- +4 correct / −1 wrong / 0 unattempted; 200 minutes; bilingual

**UPSC Pre**
- GS Paper I: 100 MCQ, 200 marks, 120 min, −0.667 per wrong (2/3 deduction)
- CSAT Paper II: 80 MCQ, 200 marks, 120 min, −0.833 per wrong (qualifying 33%)
- No sectional division; free movement within paper

**IBPS PO (Prelims)**
- English Language: 30Q / 20 min sectional timer
- Quantitative Aptitude: 35Q / 20 min sectional timer
- Reasoning Ability: 35Q / 20 min sectional timer
- Sectional cutoff enforced; cannot proceed to next section before current timer expires

**SSC CGL Tier I**
- 4 sections (GI & Reasoning / General Awareness / Quantitative Aptitude / English): 25Q each
- 60 min composite (no sectional timers); +2 correct / −0.5 wrong; 200 marks

**GATE**
- General Aptitude: 10Q (5 MCQ + 5 NAT), 15 marks — mandatory across all 30 papers
- Technical Subject: 55Q (25 MCQ + 30 NAT/MSQ mix), 85 marks
- 3 hours; on-screen virtual calculator mandatory; no physical calculator
- NAT input: text field; evaluated against tolerance range (e.g., 2.45 ± 0.01)
- MSQ: no negative marking; MCQ: −1/3 for 1-mark, −2/3 for 2-mark

### 3.2 Custom Pattern Builder
- Institution defines: section count, Q count per section, time per section (independent or
  composite), marks per question, negative marking per section, partial marking rules.
- Optional section choice: student selects N sections from M at test start (CUET-style);
  system locks unchosen sections and excludes them from scoring.
- Section-wise independent timer: each section has own countdown; moving to next section
  pauses current timer (JEE Advanced behaviour) — configurable per pattern.
- Partial marking engine: configurable per question type per section; handles all combinations
  without code change.

---

## 4. Test Scheduling

### 4.1 Scheduling Modes
| Mode | Behaviour |
|---|---|
| Scheduled Window | Fixed start + end datetime; student attempts only within window |
| Live Test | All students appear simultaneously; real-time leaderboard after window closes |
| Anytime | Student attempts any time within series validity period |
| Sequential Unlock | Test N+1 unlocks only after Test N submitted (or Test N window closes) |
| All-Unlock | All tests available from day one (self-paced) |

### 4.2 Re-attempt Policy
- 0 re-attempts: exam mode — one shot only; simulates real exam.
- Unlimited re-attempts: practice mode; student can redo to improve.
- Configurable per test within a series (FLT = 0, CT = unlimited typical setup).

### 4.3 Batch-Specific Schedules
- Different batches assigned same paper with different windows (morning / evening batch).
- Paper is the same; question shuffle unique per student (Section 14).
- Results merged for All-India Rank after all batch windows close.

### 4.4 Makeup Window
- Institution opens a makeup slot for students who missed a live test (medical / emergency).
- Makeup attempt result: included in analytics; excluded from All-India Rank (to prevent
  advantage from seeing peer discussions).

### 4.5 Test Series Calendar
- Student dashboard: full calendar view — upcoming (orange), ongoing (green), completed (grey),
  missed (red).
- Calendar syncs with device calendar on opt-in (ICS file link).

---

## 5. Test Interface

### 5.1 Exam-Day Simulation
- Full-screen enforcement: browser enters full screen at test start; first exit → warning toast;
  second exit → auto-submit (configurable threshold 1–3 exits per institution).
- Exam instructions page: rules shown for 2 minutes before timer starts (NTA behaviour);
  student confirms "I have read all instructions."

### 5.2 Question Palette (NTA 5-Colour)
| State | Colour |
|---|---|
| Not Visited | White / grey border |
| Not Answered (visited, no answer) | Red |
| Answered | Green |
| Marked for Review (no answer) | Purple |
| Answered + Marked for Review | Purple with green tick |

- Palette shows all questions across all sections; section tabs above palette.
- Status updates in real time as student interacts.

### 5.3 Question Display
- Content rendered from Unified Question JSON (Module 17): TEXT, LATEX, TABLE, CHART, DIAGRAM,
  IMAGE, CODE, CHEM_EQUATION, AUDIO blocks — same dynamic renderer.
- MCQ: radio buttons (single correct); MSQ: checkboxes (multiple correct).
- Integer / NAT: numeric input field; virtual numpad on mobile.
- Match the columns: drag-and-drop on desktop; dropdown on mobile.
- Comprehension / Paragraph: passage shown in left panel; questions on right panel.
- Fill-in-the-blank: text input field; keyboard input.
- Diagram-based: image rendered from CDN; question below.

### 5.4 Navigation & Tools
- Section navigation: free movement (JEE Main) or section-locked after timer (IBPS); per pattern.
- Mark for Review + Answer: student can answer AND mark simultaneously; NTA behaviour.
- On-screen scientific calculator: available for GATE/JEE/Maths exams; configurable ON/OFF.
- Digital rough work pad: per-question scratch pad (text + basic stylus); not submitted;
  cleared on section change (configurable retain/clear).
- Question flag (personal): student marks "Tricky / Revisit" — personal note; no effect on
  scoring.
- Font size: Normal / Large / Extra Large — accessibility; LaTeX and diagrams scale.
- Bilingual toggle: English ↔ Hindi; mid-test switch; available wherever bilingual JSON exists.
- Virtual keyboard (Devanagari/regional): for UPSC Mains Hindi medium descriptive answers;
  regional script for state PSC.
- Language selection at test start: student chooses language once; cannot change mid-test
  (per UPSC/NTA rule); configurable per exam pattern.

### 5.5 Auto-save & Network Resilience
- Auto-save every 30 seconds to server; local IndexedDB draft on device simultaneously.
- If network drops: local draft continues; sync on reconnect; no answer loss.
- Sync conflict: server timestamp vs local timestamp — later timestamp wins; student notified
  "Answers auto-recovered."
- Timer continues running offline (device clock); server validates on sync.

### 5.6 Submit Flow
- Submit confirmation: "X questions unattempted, Y Marked for Review — Confirm Submit?"
- Force-submit at timer = 0: auto-submit with current saved state; toast notification.
- Post-submit: locked screen "Submitted successfully at HH:MM:SS" — no further edits.

---

## 6. Proctoring

### 6.1 Proctoring Levels (Module 19 Engine Reused)
| Level | Description |
|---|---|
| None | No monitoring; fully open practice |
| Basic | Tab-switch + full-screen exit detection only |
| Standard | Basic + camera snapshot every 2 min |
| Strict | Standard + AI face detection + IP lock |

### 6.2 Proctoring Events
- Camera snapshot → CDN `/proctoring/{tenant_id}/{test_id}/{student_id}/` — 90-day DPDPA
  auto-delete; not shown on student report card.
- Tab-switch: browser Visibility API; alert on switch + event logged with timestamp.
- Full-screen exit: warning on first exit; configurable auto-submit on Nth exit.
- Multiple face detection (AI): suspicion score incremented; advisory in mock mode; not
  auto-disqualify; coaching centre can review events in staff dashboard.
- One active session: second login to same test invalidates first session; first session shows
  "Your session was taken over from another device."

---

## 7. Auto-Grading & Score Card

### 7.1 Instant Result (Objective)
- Raw score computed within 3 seconds of submit for all objective question types.
- Score card auto-generated; student sees result immediately (practice mode) or after test
  window closes (exam mode — all students see results together).

### 7.2 NTA Score Simulation
- Percentile = (students below this score / total students) × 100; displayed as NTA-style
  percentile score (e.g., 98.73).
- Normalised score (multi-shift/multi-batch): NTA equi-percentile normalisation method applied
  if same paper run across multiple sessions.

### 7.3 Exam-Specific Score Computations
| Exam | Score Card Shows |
|---|---|
| JEE Main | Raw score, Percentile, Estimated Rank, JEE Advanced eligibility flag |
| JEE Advanced | Paper 1 + Paper 2 + Combined; subject-wise marks; IIT branch predictor |
| NEET UG | Raw score, Percentile, Category-wise cutoff comparison (UR/OBC/SC/ST/PWD/EWS), Medical college predictor |
| UPSC Pre | GS score, CSAT score (pass/fail at 33%), Historical cutoff comparison (5 years) |
| IBPS PO | Section-wise score + sectional cutoff PASS/FAIL per section; composite score |
| SSC CGL | Tier I score + normalised score; Tier II eligibility flag |
| GATE | Raw score, GATE Score (out of 1000), Estimated Rank, M.Tech cutoff comparison, PSU eligibility |
| CA Foundation | Group aggregate check (40% per paper + 50% aggregate); PASS/FAIL per group |

### 7.4 Scoring Detail Breakdown
- Negative marking breakdown: per question — marks awarded / deducted; total loss from wrong
  answers shown separately.
- Attempt accuracy: (correct / attempted) × 100%; shown alongside raw accuracy.
- Time efficiency: score per minute of exam duration.
- Partial marking detail (JEE Advanced MSQ): per-question breakdown of partial credit awarded.

---

## 8. Solutions & Explanations

### 8.1 Solution Release Policy
- Practice mode: solution visible immediately after submit.
- Exam mode (live test): solution visible after test window closes for all batches/shifts.
- PYP practice mode: solution after each question.

### 8.2 Per-Question Solution
- Step-by-step explanation using Unified Question JSON content blocks: TEXT + LATEX + DIAGRAM
  + TABLE + CHART + CHEM_EQUATION — same dynamic renderer as question display.
- Difficulty label: Easy / Medium / Hard shown in solution view.
- Topic tag: Chapter + Topic tag; clickable → Module 16 notes for that topic (in-app).
- Multiple approaches: algebraic, graphical, shortcut trick — tabbed display per approach.
- Expert tip: "Common trap / Time-saving trick / Conceptual note" — short callout per question.

### 8.3 Video Solution
- "Watch Solution Video" button → in-app WebView (YouTube link); no download option.
- Shown only if video solution available for that question (from question JSON `video_links`
  array — Module 17).
- Teacher debrief video: teacher records post-test debrief (YouTube link); "Watch Debrief"
  button appears on test result page; in-app WebView.

### 8.4 Practice Recommendations
- After each wrong answer: 3 similar questions from Module 17 question bank — same chapter,
  adjacent difficulty — shown as "Practice More."
- Weak topic notes link: "Read Notes" button per wrong question → Module 16 notes in-app.
- Revision priority list: top 10 topics to revise before next test; auto-generated from wrong
  answers + weightage in target exam.

---

## 9. Performance Analytics

### 9.1 Score Summary Card
- Total marks obtained, max marks, percentage, raw rank (batch), All-India Rank, percentile.
- Compared to: batch average, top 10% of batch, topper.

### 9.2 Section-wise Breakdown
- Per section: marks obtained, max marks, accuracy %, time spent, avg time per question.
- Section-wise efficiency: marks per minute per section.

### 9.3 Chapter-wise Accuracy Report
| Column | Content |
|---|---|
| Chapter | Chapter name |
| Attempted | Questions attempted |
| Correct | Correct answers |
| Wrong | Wrong answers |
| Skipped | Unattempted |
| Accuracy % | Correct / Attempted × 100 |
| Avg Time | Average seconds per question in this chapter |

### 9.4 Speed vs Accuracy Quadrant
- 4-quadrant matrix per section/subject:
  - **Fast-Accurate** (optimal): high speed + high accuracy
  - **Fast-Inaccurate** (reckless): high speed + low accuracy → possible guessing
  - **Slow-Accurate** (careful but slow): low speed + high accuracy → needs speed drills
  - **Slow-Inaccurate** (struggling): low speed + low accuracy → needs concept reinforcement
- Student plotted per section; quadrant shown as text label + interpretation.

### 9.5 Attempt Pattern Analysis
- Guessing detection: high attempt rate (>90%) + low accuracy (<40%) → "Possible guessing —
  review negative marking strategy."
- Skipping pattern: student skips >50% of Hard questions → "Working on Hard question strategy
  may improve score."
- Time sink: questions where student spent >3× average time — listed as "Time Drain Questions."

### 9.6 Trend Analytics (Across Test Series)
- Percentile trend: Test 1 → Test N percentile progression; "Trending Up / Stable / Declining."
- Rank trend: rank movement across tests; top-3 improvement milestones flagged.
- Score velocity: average score gain per test; predicts target achievement date.

### 9.7 Comparative Analytics
- My score vs batch average vs top 10% vs topper — bar comparison per section.
- Subject gap: "Physics: You vs Batch Average — −18 marks; priority focus area."

### 9.8 Coaching-Specific Analytics
- All-India percentile trajectory across series (for JEE/NEET coaching centres).
- Target vs actual chart: student's JEE/NEET target score set at enrolment; each test result
  plotted against target trajectory; "On Track / Behind / Ahead."
- JEE/NEET score projection: predicted score range at exam date based on current trajectory +
  historical batch conversion data.
- Improvement suggestion: "Focus on Organic Chemistry — 30% accuracy vs 70% Physical Chemistry;
  15 marks expected in JEE Main from this chapter."

### 9.9 Platform-Level Analytics (Institution Admin)
- Test series dashboard: avg score, avg percentile, completion rate, dropout count per test.
- Question performance: p-value (difficulty index) + D-value (discrimination index) + distractor
  analysis per question — feeds back to Module 17 item bank.
- Batch comparison: same test, multiple batches — score distribution overlay.
- Dropout tracking: students who started but did not submit — names + follow-up flag.
- Coaching effectiveness: mock test percentile vs actual exam result correlation (student enters
  real exam score post-result; system computes r² correlation).

---

## 10. All-India Ranking

### 10.1 Rank Types
| Rank | Scope |
|---|---|
| All-India Rank (AIR) | All EduForge students on same test series (platform-wide) |
| State Rank | Students from same home state (from student profile) |
| Category Rank | SC / ST / OBC / EWS / General category-wise |
| Batch Rank | Within own coaching batch (primary rank shown to student) |
| Gender Rank | Male / Female / Transgender — for scholarship-aware tracking |
| Subject Rank | Top scorer per subject within batch |

### 10.2 Rank Certificate
- Auto-generated PDF for top 100 AIR per test; accessible in-app only.
- Content: student name, test name, date, AIR, percentile, institution name, EduForge seal.
- "Save to DigiLocker" option triggers DigiLocker push (Module 21 mechanism).
- Verifier portal: employer/university enters certificate_id → confirms rank, test, date.

### 10.3 Leaderboard
- Real-time leaderboard during live test window: visible AFTER student submits only (not during
  attempt); prevents peer pressure affecting test.
- Refreshes every 5 minutes post-test-window as remaining students submit.
- Top 50 shown on public leaderboard; full rank visible only to self.

### 10.4 Rank Notifications
- FCM push: "You are AIR 342 in JEE Main Mock Test 5 — Top 2% nationwide."
- Rank improvement: "You moved from AIR 450 to AIR 312 — 138 positions up!"

---

## 11. Previous Year Papers (PYP)

### 11.1 PYP Library (Pre-loaded)
| Exam | Coverage |
|---|---|
| CBSE Class 10/12 | Last 10 years, all sets (A/B/C/D), all subjects |
| JEE Main | All shifts (Jan + Apr, Morning + Evening), last 5 years |
| JEE Advanced | Last 10 years (Paper 1 + Paper 2) |
| NEET UG | Last 10 years, all sets |
| UPSC Pre GS + CSAT | Last 15 years |
| All 28 State Board SSC/HSC | Last 5 years per board |
| IBPS PO/Clerk, SBI PO/Clerk | Last 5 years |
| SSC CGL/CHSL | Last 5 years |
| RRB NTPC | Last 3 years |
| CUET UG/PG | All years since 2022 |
| GATE (all papers) | Last 5 years |
| UGC NET | Last 5 years |

### 11.2 PYP Modes
- **Exam mode**: full timer + exam pattern enforced; no solutions during attempt; result + solution
  after submit.
- **Practice mode**: no timer; question-by-question; solution shown immediately after each answer.

### 11.3 Shift-wise Papers
- JEE Main: each shift (Jan Morning / Jan Evening / Apr Morning / Apr Evening) available as
  separate paper; student can attempt all shifts to cover maximum question variety.
- NEET: multiple sets (AA/BB/CC/etc.) each available separately.

### 11.4 PYP Intelligence
- Topic frequency heatmap per PYP: each question tagged to chapter/topic; heatmap shows
  "Thermodynamics: appeared in 8 of last 10 JEE Main papers."
- PYP gap analysis: after completing a PYP, system highlights high-frequency topics where
  student scored poorly — "You scored 40% in topics that appear every year."

---

## 12. Adaptive & AI-Suggested Tests

### 12.1 Adaptive Difficulty
- Score >80% in Test N → Test N+1 generated with 60% Hard + 30% Medium + 10% Easy mix.
- Score <50% → Test N+1 generated with 20% Hard + 40% Medium + 40% Easy mix.
- Difficulty levels from Module 17 item tags (Bloom's taxonomy + p-value).

### 12.2 Weak Area Booster Test
- Auto-generated from student's weakest 5 chapters (accuracy <50%).
- Appears as "Booster Test: [chapter names]" in student dashboard.
- Student can trigger on demand or system schedules automatically (weekly).

### 12.3 Pre-Exam Revision Test
- Triggered automatically 7 days before student's target exam date (set in profile).
- Content: 60% high-weightage topics (from PYP frequency map) + 40% student's weak areas.
- Full-length; simulates final exam conditions.

### 12.4 Daily Practice Test (DPT)
- 20 questions; timed (configurable 20–40 min per batch).
- Topics auto-selected from: (a) current batch timetable position (Module 15 link), (b) spaced
  repetition queue (Ebbinghaus model — Module 17 link).
- Generated fresh each day; no two consecutive DPTs repeat same questions.

### 12.5 Study Plan Integration
- Wrong answers from every test → weak topics auto-added to student's personal study plan
  (Module 15 Curriculum Builder link).
- Study plan pending topics → selected for next DPT automatically.
- Syllabus completion % (Module 15) shown alongside test performance: "68% syllabus covered;
  tested on 45%."

---

## 13. Descriptive / Subjective Mock (UPSC Mains & Others)

### 13.1 UPSC Mains Interface
- Rich text editor with live word count; word limit enforced (cannot exceed; warning at 90%).
- Word limits: 150-word (Part a), 250-word (Part b), 500-word (longer answer) — per question.
- Essay Paper: two essays; 1000–1200 words each; 3-hour timer.
- GS Paper I–IV answer writing: typed answers; word limit enforced.
- Hindi medium: virtual Devanagari keyboard + basic Hindi spell check.

### 13.2 Evaluation Workflow (Descriptive)
- Blind evaluation: evaluator sees student code only (no name) — same Module 20 blind eval engine.
- Marking scheme: uploaded by teacher/institution as PDF (CDN); evaluator refers alongside
  student answer.
- AI-assisted feedback (advisory): keyword match + argument structure check; shown as
  "Auto-Feedback" to evaluator as hint; evaluator makes final decision.
- Model answer comparison: after evaluation, model answer shown to student; student can also
  self-evaluate (1–10 scale); both stored separately.
- Second evaluator: HOD assigns; same blind process; reconciliation if marks differ >20%.

### 13.3 Answer Script (Descriptive)
- Student's typed answer compiled to PDF; stored on CDN; accessible to student + evaluator
  in-app; no download option.
- Previous year UPSC Mains questions: topic-wise sorted; used for DPT (Mains variant — 1
  descriptive question per day).

### 13.4 Interview / GD Mock
- UPSC Interview mock: panel-style scenario questions; student types response; evaluator
  scores on 5 parameters (personality, current affairs awareness, communication, leadership,
  ethical grounding) — rubric configurable.
- Bank PO Group Discussion: topic assigned; student types point-form arguments; evaluator
  scores on logical consistency + communication.
- Campus placement mock interview: HR + Technical + Managerial rounds; each round as separate
  session; evaluator marks per round.

---

## 14. GATE Test Series

### 14.1 GATE Interface Specifics
- Virtual calculator: GATE-approved on-screen scientific calculator (same UI as actual exam);
  no physical calculator allowed.
- NAT (Numerical Answer Type): text input field; no options; evaluated against tolerance range
  configured per question (e.g., 2.45 ± 0.01 acceptable).
- MSQ (Multiple Select): checkboxes; no negative marking; partial credit not given — all correct
  or 0.
- 30-paper patterns: each loaded with correct GA (10Q) + subject (55Q) split.

### 14.2 GATE Score Card
- Raw marks → GATE Score (normalised out of 1000 using GATE normalisation formula).
- Estimated rank based on score distribution.
- M.Tech admissions cutoff comparison: IIT/NIT/IIIT branch-wise GATE cutoff (last 3 years)
  vs student score.
- PSU cutoff comparison: ONGC/BHEL/IOCL/NTPC/GAIL/PGCIL/AAI GATE cutoff vs score.

---

## 15. CA / CS / CMA Test Series

### 15.1 CA (ICAI)
- Foundation: 4 papers (Principles of Accounting, Business Laws, Maths/Stats, Business
  Economics); 3-hour each; OMR-style MCQ (some descriptive in few papers).
- Inter Group I & II: 6 papers total; group-wise test series; pass requires 40% per paper +
  50% group aggregate; system checks both.
- Final Group I & II: 8 papers total; same pass criteria.
- Eligibility check: CA Final series accessible only if student has Inter pass flag in profile.

### 15.2 CS (ICSI)
- Foundation: 4 papers; MCQ + descriptive mix.
- Executive Module I/II: 7 papers; same group pass logic.
- Professional: 9 papers across 3 modules + practical training completion flag.

### 15.3 CMA (ICMAI)
- Foundation / Inter / Final: same group aggregate logic.
- Cost accounting practicals: numerical problems with step-by-step marking scheme.
- 4-hour exam simulation for Final papers.

---

## 16. School & Olympiad Test Series

### 16.1 NTSE
- Stage I (State-level): MAT (90Q, 90 min) + SAT (100Q, 90 min); state-specific cutoff
  comparison; SCERT question style per state.
- Stage II (National): same structure; national cutoff comparison.

### 16.2 SOF Olympiads
- NSO, IMO, IEO, ICO, ISSO, IGKO — Level 1 (School) + Level 2 (Zonal/National).
- Class 1–12; subject-specific syllabus; silver/gold zone cutoff comparison.
- Section-wise: Achievers Section (higher difficulty, more marks) simulated.

### 16.3 Sainik School (AISSEE)
- Class 6: Maths + Language (Hindi or English); 300 marks.
- Class 9: Maths + Intelligence + English + GK + Social Studies; 400 marks.
- State-wise merit list comparison (seats allocated state-wise).

### 16.4 Pre-RMO / RMO
- Subjective Maths: student types solution in rich text + LaTeX editor.
- Evaluator marks manually (institute faculty).
- Topics: Number Theory, Combinatorics, Geometry, Algebra — aligned to IMO syllabus.

### 16.5 NMMS
- Class 8; MAT (90Q) + SAT (90Q); state-wise pass cutoff (55% general, 50% SC/ST).
- Family income eligibility display (reference only; income from student profile).

---

## 17. Banking & Insurance Patterns

### 17.1 IBPS RRB
- Officer Scale I/II/III: Regional Language paper mandatory (Hindi / Marathi / Tamil / Telugu /
  Kannada / Bengali / Punjabi / etc. based on state preference).
- Office Assistant: same language requirement; simpler Quant/Reasoning level.

### 17.2 RBI Grade B
- Phase I: objective (GA / English / Reasoning / Quant) — 200Q, 120 min.
- Phase II: Paper I (Economic & Social Issues — descriptive), Paper II (English Writing —
  descriptive), Paper III (Finance & Management — descriptive + objective mix).
- Descriptive interface from Section 13 used for Phase II.

### 17.3 Sectional Time-Lock
- IBPS PO Mains: section-wise time enforced; student cannot return to previous section.
- System disables answered questions from previous sections after section timer expires.

---

## 18. State PSC Deep Coverage

### 18.1 State-Specific Language Papers
- RPSC RAS Mains: Hindi + General Hindi paper (compulsory); Devanagari interface.
- UPPSC Mains: Hindi paper (compulsory); 300 marks; typed in Devanagari virtual keyboard.
- MPSC: Marathi language paper; Marathi font rendering support.
- TNPSC: Tamil language + General Tamil paper; Tamil font rendering.
- KPSC: Kannada compulsory; Kannada virtual keyboard.
- APPSC/TSPSC: Telugu medium option; Telugu font support.

### 18.2 Revenue / Village-Level Exam Series
- Rajasthan Patwari, UP Lekhpal, MP Patwari, Gram Sevak: district-specific syllabus variations;
  local revenue laws + land records Q bank tagged by state.
- Panchayat Secretary / Gram Rozgar Sevak (MGNREGS): scheme-specific awareness Q bank.

### 18.3 State SI / Constable
- Written exam pattern loaded per state; bilingual (English + state language).
- Physical test standards shown as reference (height / weight / vision) — advisory display only;
  no biometric data stored.

---

## 19. Vocational & Skill Test Series

### 19.1 NCVT ITI (150+ Trades)
- Theory: trade-specific MCQ aligned to NCVT question bank pattern.
- Practical knowledge MCQ: tool identification, safety, process steps — image-based questions
  (from Platform Image Library — Module 17).
- Trade certificate grade: A/B/C/D; NSQF level noted.

### 19.2 PMKVY Assessment Mocks
- Sector-wise: BFSI, Healthcare, Construction, Beauty & Wellness, Retail, Logistics, Tourism,
  Agriculture, Apparel, IT/ITeS, Automotive, Gems & Jewellery.
- QP-NOS (Qualification Pack – National Occupational Standards) aligned questions.
- Pass mark: 70% per QP (PMKVY 4.0 guideline).

### 19.3 RPL Assessment
- Competency-check test for workers seeking NSQF certification without formal training.
- Portfolio-based questions: scenario-based; evaluator-marked descriptive component.
- RPL Level: system auto-suggests NSQF level based on score.

---

## 20. Test Paper Security

### 20.1 Time-Locked CDN Paper
- Paper JSON encrypted on CDN; decryption key released only at scheduled start time (Module 18
  time-lock mechanism reused).
- Signed CDN URL expires 10 minutes after test window closes — no late access.

### 20.2 Per-Student Unique Paper
- Question order + option order shuffled uniquely per student (Module 18 multi-set engine).
- Same question pool; different sequence per student; eliminates direct copying.

### 20.3 Anti-Leak Measures
- Watermark: student's name + roll number watermarked on every question screen.
- Screenshot block: Android FLAG_SECURE; iOS WKWebView screenshot restriction; browser
  print/Ctrl+P/Cmd+P disabled.
- Copy-paste block: right-click disabled; Ctrl+C/Cmd+C disabled in test interface.
- Paper validity: CDN signed URL invalidated 10 min after test end.

### 20.4 Response Integrity
- Student's final submitted responses hashed (SHA-256) at submit time; stored in DB.
- Dispute resolution: disputed response compared against stored hash; tampered submissions
  detected.
- Time-gap anomaly: full 90Q paper submitted in <20 min → flag for institutional review
  (configurable threshold).

---

## 21. Answer Key Dispute

### 21.1 Dispute Workflow
```
Student flags question → select question → enter reason → submit flag
        ↓
Routed to Content Team (EduForge) for PYP / Platform series
OR to Institution Subject HOD for institution series
        ↓
Review: ACCEPTED (key updated) or REJECTED (explanation sent)
        ↓
If ACCEPTED: all students' scores for that test recalculated
Result cards updated; students notified via FCM
        ↓
Dispute closed; resolution note visible to student
```

### 21.2 SLA & Log
- Resolution SLA: 5 working days; student notified of decision in-app.
- Dispute log: question_id, raised_by, reason, status, resolved_by, resolution_note,
  score_delta (how many students affected, average score change).

---

## 22. Offline & Low-Connectivity Mode

### 22.1 Offline Test
- Paper pre-downloaded to device 30 min before window opens (encrypted, time-locked).
- Download window closes at test start; no late download.
- Student appears offline; all interactions stored locally.
- Responses synced to server on reconnect; conflict resolution: later timestamp wins.
- "Auto-recovered" notice shown to student after sync.

### 22.2 Low-Bandwidth Optimisation
- Question images: served in compressed WebP from CDN; text-only fallback if image fails.
- LaTeX: rendered server-side to SVG; SVG cached on device.
- Audio questions: pre-loaded on test start; not streamed mid-test.

---

## 23. Gamification

### 23.1 XP & Levels
- XP (experience points): correct answer +10, full test completion +50, daily streak +20/day,
  >90% accuracy in any test +30 bonus.
- Levels: Bronze (0–500 XP) → Silver (501–2000) → Gold (2001–5000) → Platinum (5001–10000) →
  Diamond (10001+).
- Level badge shown on student profile and leaderboard.

### 23.2 Achievement Badges
| Badge | Trigger |
|---|---|
| Hat-trick | 3 consecutive tests with >90% accuracy |
| Comeback | Rank improved by 200+ positions in one test |
| Perfectionist | 100% accuracy in any subject test |
| Speed Demon | Top 10% in time efficiency |
| Streak Master | 30-day daily practice test streak |
| Series Champion | Highest rank in a completed test series |
| PYP Veteran | Completed 10 PYPs |

### 23.3 Peer Challenge
- Student challenges a batchmate to same chapter test; both attempt within 24 hrs.
- Result comparison shown to both: score, accuracy, time — winner declared.
- Challenge acceptance / rejection; declined challenge shows "Batchmate declined."

### 23.4 Weekly Platform Challenge
- Platform-wide 10-question challenge every Sunday; same for all EduForge students.
- Top 3 win in-app badge + rank certificate (in-app only).

---

## 24. Teacher & Evaluator Tools

### 24.1 Live Test Monitoring
- Real-time dashboard: how many students started / submitted / still attempting.
- Per-student status: question number reached, time remaining, flagged proctoring events.
- Evaluator does not see student's answers during the test — only status.

### 24.2 Post-Test Teacher Dashboard
- Per-student drill-down: question-wise response + time spent; wrong answers highlighted.
- Class weakness heatmap: chapter × student matrix; red = wrong; used to plan re-teaching.
- Per-question class performance: % students correct; teacher marks "Discuss in class" flag.
- Dropout list: students who started but did not submit — names + time spent before drop.

### 24.3 Model Answer
- Teacher uploads model answer PDF (CDN); visible to students after solution release.
- For subjective tests: evaluator refers to model answer PDF alongside student script.

---

## 25. Notifications & Reminders

### 25.1 Pre-Test Reminders
- FCM + SMS: 24 hours before scheduled test; 1 hour before live test start.
- Calendar reminder: ICS file link in notification for device calendar sync.

### 25.2 Post-Test Notifications
- Result ready: instant FCM on submit (practice mode); batch FCM after window closes (exam mode).
- Rank update: FCM when AIR computed post-window.
- Rank improvement: "You improved 138 positions — keep going!"

### 25.3 Engagement Nudges
- Missed test alert: student missed scheduled test → follow-up FCM + makeup window link.
- Weak area reminder: "You haven't practiced Organic Chemistry in 7 days — try a Booster Test."
- Streak reminder: "You are on a 6-day streak — don't break it today!"
- Series completion: "You've completed all 10 tests in JEE Main Series 1 — Series 2 is now
  unlocked."

---

## 26. Multi-Language Support

### 26.1 Question Display Languages
- All 22 scheduled Indian languages supported for question display (where translation available
  in question JSON — Module 17 `stem_translations` field).
- State exam series fully rendered in regional language (Marathi for MPSC, Tamil for TNPSC,
  Telugu for APPSC/TSPSC, Kannada for KPSC, Bengali for WBPSC, Punjabi for PPSC).
- Bilingual toggle (English ↔ Hindi): available for all NTA exams; mid-test language switch.
- Hindi medium UPSC: entire interface in Hindi; Devanagari virtual keyboard + basic spell check.

### 26.2 Interface Language
- Student can set app interface language independently of question language.
- Instructions, button labels, alert messages rendered in selected interface language.
- Supported interface languages: English, Hindi, Tamil, Telugu, Kannada, Marathi, Bengali,
  Gujarati, Punjabi, Malayalam, Odia, Assamese, Urdu.

---

## 27. CWSN / Special Needs Accommodations

### 27.1 Compensatory Time
- Extra 20 min (visual / locomotor / hearing impairment) or 40 min (intellectual / autism /
  multiple disabilities) — per NTA/CBSE CWSN circular.
- CWSN flag required on student profile (disability type + certificate reference).
- Timer extension applied automatically on test assignment if CWSN flag active.

### 27.2 Accessible Interface
- Large text mode: all content scales; LaTeX/diagram images scale proportionally.
- High contrast mode: black background + white/yellow text; configurable for low-vision students.
- Screen reader: all content blocks accessible via ARIA labels; LaTeX rendered with MathML
  for screen reader compatibility.
- Dyslexia-friendly font: OpenDyslexic font toggle available in test settings.
- Audio question playback: text-to-speech per question (for reading difficulty / dyslexia).

### 27.3 Scribe-Assisted Mode
- Authorised staff logs in as scribe; enters answers on behalf of student under supervision.
- Every scribe entry logged: question_id, answer_entered, time, scribe_staff_id.
- Student profile must have CWSN flag + scribe approval from institution before this mode
  activates.

### 27.4 Voice Input
- Speech-to-text for descriptive answers; student reviews transcribed text before submit.
- Available in supported languages: Hindi, English, Tamil, Telugu, Kannada, Marathi.
- Works in low-noise environment; disclaimer shown to student.

---

## 28. Competitive Exam Cutoff Intelligence

### 28.1 Cutoff Database
- Maintained by EduForge content team; updated after each real exam result declaration.
- Last-updated timestamp visible to student; "ESTIMATED" label on projections.

### 28.2 Cutoff Comparisons Available
| Exam | Cutoff Type |
|---|---|
| JEE Advanced | IIT-wise, branch-wise, category-wise (JoSAA historical) |
| NEET UG | Medical college-wise, course-wise (MBBS/BDS/AYUSH), state-wise (MCC + state counselling) |
| GATE | M.Tech cutoff: IIT/NIT/IIIT branch-wise; PSU: ONGC/BHEL/IOCL/NTPC/GAIL |
| IBPS/SBI | State-wise, category-wise, section-wise cutoffs |
| SSC CGL | Post-wise, category-wise |
| UPSC Pre | General/OBC/SC/ST/PwD — last 5 years |
| State PSC | State-specific; category-wise |

### 28.3 College Predictor
- JEE Main score → likely colleges + branches (JoSAA/CSAB historical data); shown as range.
- NEET score → likely state + private medical colleges (last 3 years counselling data).
- Results labelled "PREDICTED — based on historical data; subject to change."

### 28.4 Cutoff Alert
- Student sets target college/institute + programme in profile.
- System sends FCM alert when cutoff data for that college is updated.

---

## 29. Access Control & Packages

### 29.1 Test Series as Subscription Product
- Bundled into Module 50 subscription packages; access auto-revoked on package expiry.
- Institution-gated: test series visible only to enrolled batch students; RLS enforces
  tenant-level isolation.

### 29.2 Free Access
- Free trial test: first test in any paid series always accessible free.
- Platform-level guest DPT: 10 questions per day without login (for student acquisition).
- Institution can mark any test as free for all enrolled students regardless of subscription.

### 29.3 Expiry Handling
- Test attempt blocked after package expiry; student shown "Subscription expired — renew to
  continue."
- Results of attempted tests remain accessible permanently even after expiry.

---

## 30. DB Schema

### Table: `test_series`
```
test_series_id       UUID PRIMARY KEY
name                 VARCHAR(200)
target_exam          VARCHAR(100)
series_type          VARCHAR(30)  -- FULL | PART | CHAPTER | SUBJECT | PYP | DAILY | ADAPTIVE
total_tests          INT
schedule_type        VARCHAR(20)  -- WEEKLY | BIWEEKLY | MONTHLY | CUSTOM | ANYTIME
validity_start       DATE
validity_end         DATE
access_mode          VARCHAR(20)  -- FREE | SUBSCRIPTION | INSTITUTIONAL
created_by           ENUM         -- PLATFORM | INSTITUTION
status               VARCHAR(20)  -- DRAFT | PUBLISHED | ACTIVE | COMPLETED | ARCHIVED
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `mock_tests`
```
test_id              UUID PRIMARY KEY
series_id            UUID REFERENCES test_series(test_series_id)
test_type            VARCHAR(30)  -- FLT | PT | CT | ST | PYP | DPT | BOOSTER | REVISION | INTERVIEW
pattern_id           UUID         -- references exam_patterns table
scheduled_start      TIMESTAMPTZ NULL
scheduled_end        TIMESTAMPTZ NULL
mode                 VARCHAR(20)  -- EXAM | PRACTICE | LIVE
re_attempt_allowed   BOOLEAN DEFAULT FALSE
max_attempts         INT DEFAULT 1
proctoring_level     VARCHAR(20)  -- NONE | BASIC | STANDARD | STRICT
solution_release     VARCHAR(20)  -- IMMEDIATE | AFTER_WINDOW | MANUAL
language_options     TEXT[]       -- ['en','hi','ta','te']
is_bilingual         BOOLEAN DEFAULT FALSE
offline_allowed      BOOLEAN DEFAULT FALSE
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `test_attempts`
```
attempt_id           UUID PRIMARY KEY
test_id              UUID REFERENCES mock_tests(test_id)
student_id           UUID REFERENCES students(student_id)
attempt_number       INT DEFAULT 1
started_at           TIMESTAMPTZ
submitted_at         TIMESTAMPTZ NULL
raw_score            NUMERIC(7,2)
normalised_score     NUMERIC(7,2) NULL
percentile           NUMERIC(6,3) NULL
air_rank             INT NULL
state_rank           INT NULL
batch_rank           INT NULL
category_rank        INT NULL
status               VARCHAR(20)  -- IN_PROGRESS | SUBMITTED | FORCE_SUBMITTED | ABANDONED
proctoring_events    INT DEFAULT 0  -- count of flagged events
device_fingerprint   VARCHAR(200)
ip_address           INET
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `test_responses`
```
response_id          UUID PRIMARY KEY
attempt_id           UUID REFERENCES test_attempts(attempt_id)
question_id          UUID
section_id           VARCHAR(50)
selected_option      TEXT NULL     -- option_id(s) for MCQ/MSQ; numeric string for NAT/Integer
response_text        TEXT NULL     -- for descriptive answers
is_correct           BOOLEAN NULL
marks_awarded        NUMERIC(5,2)
time_spent_sec       INT
visit_count          INT DEFAULT 1
flagged_for_review   BOOLEAN DEFAULT FALSE
personal_flag        VARCHAR(20) NULL  -- TRICKY | REVISIT
last_modified        TIMESTAMPTZ
tenant_id            UUID NOT NULL
```

### Table: `test_analytics`
```
analytics_id         UUID PRIMARY KEY
attempt_id           UUID REFERENCES test_attempts(attempt_id)
student_id           UUID
test_id              UUID
section_wise         JSONB  -- {section_id: {marks, accuracy, time_spent, avg_time_per_q}}
chapter_wise         JSONB  -- {chapter_id: {attempted, correct, wrong, skipped, accuracy, avg_time}}
speed_accuracy       JSONB  -- {section_id: quadrant_label}
weak_chapters        JSONB  -- [{chapter_id, accuracy}] sorted asc
strong_chapters      JSONB  -- [{chapter_id, accuracy}] sorted desc
attempt_pattern      VARCHAR(30)  -- NORMAL | GUESSING | SKIPPING | TIME_SINK
difficulty_hit_rate  JSONB  -- {easy: %, medium: %, hard: %}
target_gap           NUMERIC(6,2) NULL
improvement_tips     JSONB  -- [{topic, suggestion}]
tenant_id            UUID NOT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `pyp_library`
```
pyp_id               UUID PRIMARY KEY
exam_name            VARCHAR(100)
year                 INT
month                VARCHAR(20) NULL   -- JAN | APR (JEE shifts)
shift                VARCHAR(20) NULL   -- MORNING | EVENING
paper_set            VARCHAR(10) NULL   -- A | B | C | D | SET1
question_count       INT
pattern_id           UUID
cdn_path             VARCHAR(500)
topic_frequency_map  JSONB   -- {topic_id: count}
created_by           ENUM    -- PLATFORM | INSTITUTION
tenant_id            UUID NULL  -- NULL = platform-level
created_at           TIMESTAMPTZ DEFAULT NOW()
```

### Table: `answer_key_disputes`
```
dispute_id           UUID PRIMARY KEY
test_id              UUID
question_id          UUID
raised_by            UUID   -- student_id
reason               TEXT
status               VARCHAR(20)  -- OPEN | UNDER_REVIEW | ACCEPTED | REJECTED
resolved_by          UUID NULL
resolution_note      TEXT NULL
score_delta_per_student NUMERIC(5,2) NULL
students_affected    INT NULL
created_at           TIMESTAMPTZ DEFAULT NOW()
resolved_at          TIMESTAMPTZ NULL
tenant_id            UUID NOT NULL
```

### Table: `student_xp_log`
```
xp_id                UUID PRIMARY KEY
student_id           UUID
test_id              UUID NULL
xp_earned            INT
reason               VARCHAR(100)  -- CORRECT_ANS | TEST_COMPLETE | STREAK | ACCURACY_BONUS
earned_at            TIMESTAMPTZ DEFAULT NOW()
cumulative_xp        INT
level_after          VARCHAR(20)  -- BRONZE | SILVER | GOLD | PLATINUM | DIAMOND
tenant_id            UUID NOT NULL
```

### Table: `peer_challenges`
```
challenge_id         UUID PRIMARY KEY
challenger_id        UUID   -- student_id
challenged_id        UUID   -- student_id
test_id              UUID   -- chapter test used for challenge
status               VARCHAR(20)  -- PENDING | ACCEPTED | DECLINED | COMPLETED | EXPIRED
challenger_score     NUMERIC(6,2) NULL
challenged_score     NUMERIC(6,2) NULL
winner_id            UUID NULL
expires_at           TIMESTAMPTZ  -- 24 hrs from creation
created_at           TIMESTAMPTZ DEFAULT NOW()
tenant_id            UUID NOT NULL
```

### Table: `offline_sync_log`
```
sync_id              UUID PRIMARY KEY
attempt_id           UUID
student_id           UUID
device_id            VARCHAR(200)
offline_start        TIMESTAMPTZ
sync_timestamp       TIMESTAMPTZ
conflict_resolved    BOOLEAN DEFAULT FALSE
resolution_method    VARCHAR(30)  -- LATER_TIMESTAMP | SERVER | LOCAL
responses_synced     INT
tenant_id            UUID NOT NULL
```

### Table: `test_cutoffs`
```
cutoff_id            UUID PRIMARY KEY
exam_name            VARCHAR(100)
year                 INT
category             VARCHAR(20)  -- GENERAL | OBC | SC | ST | EWS | PWD
state                VARCHAR(100) NULL
college_name         VARCHAR(200) NULL
branch               VARCHAR(200) NULL
cutoff_score         NUMERIC(7,2) NULL
cutoff_rank          INT NULL
cutoff_percentile    NUMERIC(6,3) NULL
source               VARCHAR(100)  -- JOSAA | MCC | IBPS_OFFICIAL | NTA | GATE_IIT
updated_at           TIMESTAMPTZ DEFAULT NOW()
updated_by           UUID   -- content team staff_id
```

---

## 31. Integration Map

```
Module 15 (Curriculum) ──→ DPT topic selection, study plan sync
Module 16 (Notes) ──────→ "Read Notes" link from wrong answers
Module 17 (Question Bank)→ Question JSON, item analysis feedback, PYP tagging
Module 18 (Paper Builder)→ Paper generation (auto/manual), CDN time-lock
Module 19 (Proctoring) ──→ Camera snapshot, tab-switch, session management
Module 20 (Auto-Grading)→ Objective grading engine, descriptive evaluation
Module 21 (Results) ────→ DigiLocker rank certificate push
Module 24/25 (Fee) ──────→ Test series subscription fee
Module 35/38 (FCM/SMS) ──→ Test reminders, result notifications, rank updates
Module 50 (Subscriptions)→ Test series access control
Module 51 (B2B API) ────→ Rank certificate verification
```

---

## 32. Compliance Checklist

| Regulation / Standard | Compliance Point |
|---|---|
| NTA Exam Conduct Rules | JEE/NEET/CUET pattern exact simulation; NTA 5-colour palette; section timers |
| UPSC Exam Notice | UPSC Pre pattern, CSAT qualifying mark, Mains word limits, Hindi medium |
| IBPS/SBI/RBI Notification | Sectional time-lock; sectional cutoff enforcement; regional language paper |
| GATE IIT Regulations | Virtual calculator; NAT tolerance; 30-paper patterns; GATE score normalisation |
| ICAI/ICSI/ICMAI Rules | Group pass criteria; eligibility check before series access |
| NCVT ITI Regulations | 150+ trade patterns; theory + practical knowledge mix |
| PMKVY 4.0 Guidelines | QP-NOS alignment; 70% pass mark; sector-wise patterns |
| NSQF Framework | Level 1–8 competency descriptors mapped to test difficulty |
| RPWD Act 2016 | Compensatory time; accessible formats; scribe mode; CWSN flag required |
| DPDPA 2023 | Proctoring snapshot 90-day delete; no biometric storage; consent for data use |
| RTI Act 2005 | Answer key dispute resolution within statutory SLA |
| RTE Act | No fee barrier for RTE-seat students accessing institution test series |
| Copyright Act 1957 §52(1)(i) | PYP questions used for educational purpose — fair use; EduForge not reproducing for commercial resale |
| NEP 2020 | Multidisciplinary test support; credit-linked assessment integration |
| NTA Anti-Malpractice | Screenshot block; per-student unique paper; response hash; session lock |
