# Module 19 — Exam Session & Proctoring

## Purpose
Provide a full-featured internal exam delivery and management platform for EduForge.
This is an internal / mock exam system — not a replacement for official board exams
(CBSE, JEE, NEET are external). However the platform delivers near-real-exam quality
for internal tests, pre-boards, sessionals, coaching mock tests, and test series.
Supports both online (device-based) and offline (physical paper + OMR) exams, with
professional-grade proctoring, seating management, invigilator tools, answer booklet
management, centralised evaluation assignment, and full compliance archival.

---

## 1. Exam Scheduling & Configuration

### 1.1 Exam Creation
Fields:
- Exam name, type (from Module 18 exam type list)
- Subject, board, grade / batch / section
- Academic year, term
- Date, start time, duration (minutes)
- Total marks, passing marks (optional)
- Negative marking: Yes / No (inherited from Module 18 paper; overridable)
- Exam mode: Online / Offline / Hybrid
- Paper source: link to Module 18 paper (one or more sets A/B/C/D)
- Proctoring level: None / Basic / Standard / Strict
- Late-joining window: 0–30 minutes (configurable)
- Grace time after expiry: 0–5 minutes
- Answer key release: Immediate / After all submit / Scheduled date-time / Manual
- Score release: With answer key / After evaluation / On report date / Manual

### 1.2 Exam Modes

| Mode | Description |
|---|---|
| Online | Students take exam on device (app/web); paper from Module 18 CDN |
| Offline | Physical paper; system used for attendance, OMR, result entry |
| Hybrid | Some students online (standard), some offline (CWSN/no device) |

### 1.3 Multi-Date Exam
- Same exam conducted across multiple dates for different batches/sections
- Each date-batch combination is a separate "session" under one exam record
- Separate papers (parallel sets) used per session to prevent leakage between dates

### 1.4 Multi-Subject Exam Schedule (Semester Timetable)
- Link multiple subject exams into a named schedule (e.g., "Mid-Term Nov 2025")
- Exam conflict check: auto-validates no student has two exams at same time
- Teacher/invigilator conflict check: no teacher assigned to two halls simultaneously
- Published as exam timetable visible to all students and staff

### 1.5 Exam Series
- Group multiple exams into a named series:
  - "Mock Test Series 1 — JEE 2025 (10 tests)"
  - "Periodic Test Series — Class 12 Science 2025–26"
- Series-level analytics: student performance trend across all tests in series
- Auto-scheduling: define series frequency (weekly/biweekly); system creates all exam slots

### 1.6 Student Visibility
- Exam hidden from students until teacher publishes
- On publish: exam appears in student's exam calendar with: name, subject, date, time, duration, marks
- Unpublish allowed before exam starts (reverts to hidden)

### 1.7 Demo / Practice Test
- Auto-created for every online exam: 5-question demo using same question types as main exam
- Student takes demo test 24 hours before main exam (available window configurable)
- Demo: identical UI, timer, tools, keyboard shortcuts — pure familiarisation
- No marks recorded; student can retake demo unlimited times before main exam
- System check runs automatically at start of demo

---

## 2. Admit Card / Hall Ticket

### 2.1 Auto-Generation
Admit card populated from:
- Student: name, roll number, photo (from Module 07 profile), class/grade, section
- Exam: name, subject, date, start time, duration, venue/hall, seat number, set code
- Instructions: general exam instructions
- QR code: unique per student per exam — encodes student_id + exam_id + set_code

### 2.2 Photo Source
- Photo fetched directly from Module 07 student profile
- No re-upload required
- If profile photo absent: placeholder shown; Admin notified to update profile

### 2.3 Digital Delivery
- Available in student app 48 hours before exam start
- Student can save admit card PDF to device (exception to no-download rule — admit card is a personal identity document)
- Admit card also visible in parent app (Module 09) for school students (Classes 1–12) and college students under 18

### 2.4 Bulk Print
- Teacher/Admin prints all admit cards for a section/exam in one PDF (one per page)
- Used for: physical distribution, notice board display

### 2.5 QR Verification by Invigilator
- Invigilator opens invigilator app → scans QR on student's admit card
- App shows: student photo, name, roll number, set code, seat number, CWSN flag
- Identity mismatch: invigilator flags for impersonation investigation

### 2.6 Admit Card Gates
- Fee clearance gate: configurable — students with overdue fees (Module 25) blocked from admit card
- Document pending gate: configurable — students with pending mandatory documents blocked
- Disciplinary hold: Admin can hold individual student's admit card with reason
- HOD override: HOD can release any held admit card with documented reason

---

## 3. Seating Plan

### 3.1 Hall Configuration
- Define exam halls: name, building, floor, rows × columns capacity
- Multiple halls per exam (auto-distributed by student count)
- Hall features: CWSN accessible (ground floor, ramp, wide aisle) — flagged per hall

### 3.2 Auto Seating Plan Generation
- Students distributed across halls: sections mixed (students from different sections share hall — reduces same-section copying)
- Roll number range assigned per hall
- Adjacent students (same row, adjacent columns) assigned different sets (A/B/C/D) automatically — feeds from Module 18 set assignment
- CWSN students: auto-assigned front row, aisle seat, near exit; scribe seat adjacent

### 3.3 Seating Chart Outputs
- Hall-wise seating chart: seat number → roll number + student name + set code
- Printable per hall for invigilators
- Digital view in invigilator app: tap seat → see student details

### 3.4 Manual Override
- Admin can reassign any student to a different seat/hall before exam
- Reassignment: set code updated automatically for new seating position
- Change log: who changed, when, reason

### 3.5 Virtual Seating (Online Exam)
- No physical hall assignment needed
- Set-code assignment still generated (for multi-set online exams)
- "Virtual hall": each section is a virtual hall for monitoring dashboard purposes

---

## 4. Roll Number & Set Assignment

### 4.1 Roll Number Format
Configurable format per institution:
- Sequential: 001, 002, 003…
- Year-prefixed: 2025-001
- Section-coded: 12-A-001, 12-B-001
- Institution code: EF-2025-SCI-001

### 4.2 Roll Number Scope
- Per exam: same student may have different roll numbers in different exams (exam-specific roll) — OR — institution assigns permanent annual roll number (used across all exams in the year)
- Institution configures preference at setup

### 4.3 Set Code Binding
- Roll number → set code binding locked 24 hours before exam
- Printed on admit card, OMR sheet, attendance sheet
- Cannot be changed after admit cards are distributed (Admin override with reason only)

---

## 5. Student Authentication for Online Exam

### 5.1 Exam Login
- Student logs in with existing EduForge app credentials
- No separate exam login required
- Exam appears in "My Exams" dashboard when published

### 5.2 Email OTP Re-Verification (Configurable)
- For high-stakes internal exams: student re-verifies with email OTP before entering
- OTP valid for 10 minutes
- Configurable per exam (off by default for routine tests; recommended for pre-boards)

### 5.3 Face Match Check (Configurable)
- Student takes real-time selfie at exam start
- System compares with Module 07 profile photo (face similarity score)
- Similarity < 70%: flagged to invigilator dashboard (not hard block — invigilator reviews)
- Similarity ≥ 70%: auto-cleared; student proceeds
- Configurable: off / advisory / hard block per exam

### 5.4 Device Binding (Configurable)
- Strict mode: exam accessible only on student's registered primary device (Module 01 device registry)
- Standard mode: any logged-in device allowed (default for routine tests)
- Device binding configured per exam

### 5.5 Single Device Enforcement
- If same student opens exam on second device:
  - First session: auto-paused with message "Session opened on another device"
  - Second device: "This exam is already active on another device"
  - Invigilator dashboard: alert shown — "Student X: multiple device attempt"
  - Student must contact invigilator to resolve

---

## 6. Pre-Exam System Check

### 6.1 System Check Wizard
Auto-runs before demo test and before main exam:

| Check | Pass Condition | Fail Action |
|---|---|---|
| Internet speed | ≥ 1 Mbps download | Warning (Yellow); < 256 Kbps = Red |
| Browser compatibility | Chrome 90+ / Firefox 88+ / Safari 14+ / Edge 90+ | Red block |
| Camera access | Permission granted (if proctoring enabled) | Red block if Strict proctoring |
| Full-screen mode | Browser supports full-screen API | Warning |
| Device time sync | ≤ 30 seconds drift from server time | Red if > 5 min drift |
| Storage available | ≥ 50 MB free for local cache | Warning |

### 6.2 Result States
- Green: all checks passed → proceed
- Yellow: warnings present → student informed; proceeds with risk acknowledged
- Red: critical failure → cannot proceed; troubleshooting guidance shown

### 6.3 Check Log
- System check results logged per student per exam
- Used in dispute resolution: "Student claims they were disconnected — check log shows internet was 200 Kbps at exam start"

---

## 7. Instructions & Acknowledgement

### 7.1 Instructions Page
- General instructions (from Module 18 cover page template)
- Subject-specific instructions
- Proctoring rules (if enabled): camera, full-screen, tab-switch warnings
- Tool availability: calculator (Yes/No), formula sheet (Yes/No), rough work (Yes/No)
- Marking scheme summary: marks per section, negative marking details
- Student must scroll to bottom before "Start Exam" button activates

### 7.2 Unfair Means Declaration
- Checkbox: "I declare that I will not use any unfair means during this examination and that all work submitted is my own."
- Must be ticked to proceed
- Declaration recorded with: student_id, exam_id, device_id, IP address, timestamp
- DPDPA 2023 compliant: stored as exam integrity record; retained 5 years

### 7.3 Exam Token / PIN Entry (Configurable)
- Institution generates one-time 6-digit PIN per exam session
- Invigilator announces PIN verbally in hall at exam start time
- Online students enter PIN to start exam (confirms physical presence — anti-proxy measure)
- PIN valid for 5-minute window from announced time

---

## 8. Online Exam Interface — Student

### 8.1 Paper Loading
- At T=0: Module 18 CDN time-locked URL activates
- Paper JSON fetched; all questions loaded and cached locally
- If network drops after loading: student can continue from local cache
- Loading confirmation: "Paper loaded successfully — X questions across Y sections"

### 8.2 Full-Screen Enforcement
- Exam auto-enters full screen on start
- Exit 1: warning popup — "You are about to leave full screen. This will be recorded."
- Exit 2: logged; invigilator alert sent — "Student X exited full screen"
- Exit 3+: auto-flag for review; invigilator can terminate session

### 8.3 Question Palette
Sidebar / bottom panel showing all question numbers colour-coded:

| Colour | Status |
|---|---|
| Grey | Not Visited |
| Red | Visited but Not Answered |
| Green | Answered |
| Purple | Marked for Review |
| Purple + Green | Answered AND Marked for Review |

- Click any number → jump to that question
- Section tabs at top: one per section; section-wise summary (answered/unanswered/flagged)

### 8.4 Section Navigation Rules
- Free navigation (default): student can move between sections freely
- Section lock (configurable): once student submits a section and moves on, cannot return — JEE Advanced pattern; configurable per exam
- Section timer: for exams with sectional time limits (banking pattern), timer per section shown; section auto-locks when section time expires; student moves to next section automatically

### 8.5 Answer Input by Type

| Question Type | Input Method |
|---|---|
| MCQ Single / Multiple | Radio / Checkbox buttons |
| True / False | Toggle buttons |
| Fill in Blank | Text input field |
| Numerical | On-screen number pad + decimal point + backspace |
| Integer (0–9) | Single digit pad (0–9 only) |
| Decimal | Number pad + decimal point |
| Match the Following | Dropdown per row OR drag-and-drop |
| Sequence / Arrangement | Drag-and-drop items into order OR number inputs |
| Short Answer | Text box with live word counter |
| Long Answer | Rich text box (bold/italic/bullet lists only; no images) |
| Diagram Label | Dropdown selector per blank label |
| Assertion-Reason | Radio buttons (A/B/C/D/E) |
| Matrix Match | Checkbox grid (row × column) |

### 8.6 Mark for Review
- "Mark for Review" button per question
- Flagged = Purple in palette
- Can be answered + flagged (Purple-Green)
- All flagged questions listed in submission confirmation screen
- Auto-submit includes all answered questions (flagged or not)
- Flagged but unanswered = not submitted (no marks, no negative)

### 8.7 Answer Change
- Student can change answer any number of times within time limit
- Each change logged: previous answer, new answer, timestamp
- Full answer history stored; accessible to HOD for dispute resolution
- Final submitted state = last answer before submission/auto-submit

### 8.8 Auto-Save
- Every 30 seconds: all current answers synced to server
- Confirmation tick shown per save ("Saved at 10:32:45")
- Network failure: answers saved to device local storage (IndexedDB)
- On reconnect: local storage synced to server; merge conflict → server state wins for objective; local state wins for text answers (to preserve longer typed answers)

### 8.9 Connection Loss Handling
- Banner shown immediately on disconnect: "You are offline. Your answers are being saved locally."
- Countdown: 5-minute auto-reconnect attempt; if not reconnected in 5 min → invigilator alerted
- Timer continues running during disconnect (no pause for connectivity issues)
- On reconnect: sync completes; banner removed; confirmation shown

---

## 9. Exam Tools for Students

### 9.1 Countdown Timer
- Always visible in fixed header
- Colour changes: White → Orange (30 min) → Red (10 min) → Flashing Red (5 min)
- Popup alert at 30 min, 10 min, 5 min: "X minutes remaining"
- At T=0: auto-submit fires

### 9.2 Rough Work Scratchpad
- Floating in-app scratchpad: text input + basic freehand drawing
- Not submitted, not visible to evaluator
- Cleared automatically after exam submission
- Available throughout exam; minimise/maximise toggle

### 9.3 Scientific Calculator
- Built in-app floating overlay
- Functions: basic arithmetic, trigonometry (sin/cos/tan and inverses), logarithm (log/ln), square root, powers, π, e
- History: last 10 calculations shown
- Availability: configurable per exam — enabled for Physics/Chemistry/Maths/JEE/NEET; disabled for English/History/Reasoning
- Cannot be used to copy-paste values into answer fields (input fields and calculator are separate)

### 9.4 Formula Sheet (Open Book Exams)
- For exams tagged `is_open_book: true`: formula sheet note (Module 16) available in side panel during exam
- Side panel: read-only view of published formula sheets for that subject/chapter
- Does not pause timer
- Normal (closed book) exams: formula sheet panel absent

### 9.5 Watch Video Button
- Questions with video links (Module 17) show "Watch Video" button in exam review mode (post-submission)
- During live exam: video button hidden by default (configurable — can be shown for open-book / take-home exams)
- Opens in in-app WebView; YouTube app never launched

### 9.6 Zoom / Font Size
- Pinch-to-zoom for questions with diagrams/charts
- Font size toggle: 3 levels — does not affect answer submission
- Persisted for duration of exam session

### 9.7 Language Toggle (Bilingual Paper)
- For bilingual papers: "English / हिंदी" toggle in header
- Student switches language at any time; does not affect answers
- Selected language preference logged

---

## 10. Proctoring Features

### 10.1 Proctoring Levels

| Level | Features Active |
|---|---|
| None | No restrictions (open practice) |
| Basic | Tab switch detection + copy-paste disable + right-click disable |
| Standard | Basic + full-screen enforcement + screenshot detection + single device |
| Strict | Standard + camera monitoring + audio monitoring + face match |

Configured per exam by HOD/Admin.

### 10.2 Tab Switch & Focus Loss Detection
- Browser focus lost (tab switch / window minimise / alt+tab):
  - Warning 1: popup — "You have switched away from the exam. This is being recorded." (student returns)
  - Warning 2: logged + invigilator dashboard alert with timestamp
  - Warning 3+: cumulative flag count shown on invigilator dashboard; HOD review required post-exam
- Focus loss events logged: timestamp, duration of absence, question being answered at that time

### 10.3 Copy-Paste & Right-Click Disable
- Ctrl+C, Ctrl+V, Ctrl+X, Ctrl+A (select all) disabled in exam window
- Right-click context menu disabled (no "inspect", "save", "copy")
- Browser developer tools: F12 / Ctrl+Shift+I trigger warning + log entry

### 10.4 Screenshot Detection
- PrintScreen / Ctrl+PrtScn / Fn+PrtScn key events detected and logged
- Warning popup shown to student: "Screenshot attempt detected and recorded."
- Event logged: timestamp, question on screen at time of attempt

### 10.5 Camera Monitoring (Strict Proctoring)
- Webcam access requested at exam start; permission denial blocks exam entry (Strict mode)
- Periodic snapshots: every 2 minutes (configurable: 1–5 min)
- Stored per student per exam on CDN: `/proctoring/{tenant_id}/{exam_id}/{student_id}/snap_{timestamp}.jpg`
- CDN access: teacher/admin signed URL only; never student-accessible
- Retention: 90 days post-exam; then auto-deleted (DPDPA 2023)
- Flags auto-raised for:
  - Multiple faces detected in frame
  - No face detected for > 30 seconds
  - Significant change in background (student moved location)
  - Bright light source covering camera

### 10.6 Multiple Face Detection
- AI-based face count in each snapshot
- > 1 face: alert to invigilator dashboard — "Multiple faces detected — Student X — [snapshot thumbnail]"
- Invigilator reviews snapshot; marks: "False positive / Confirmed violation"

### 10.7 No-Face Detection
- 0 faces detected for > 30 seconds: warning popup to student — "Please ensure your face is visible to the camera"
- Persistent no-face (> 2 consecutive snapshots): invigilator alerted

### 10.8 Audio Monitoring (Strict Proctoring)
- Microphone access requested at exam start
- Continuous ambient sound analysis — does NOT record audio; only analyses volume/voice patterns
- Triggers: elevated voice level, multiple voice patterns detected
- Flag raised: "Unusual audio detected — Student X — 10:47:32"
- No audio recording stored (privacy compliance — DPDPA 2023)

### 10.9 VPN Detection
- Student exam session checked for VPN/proxy indicators
- VPN detected: logged as advisory flag (not hard block — institutional VPNs may be legitimate)
- Flagged students reviewed post-exam by invigilator

### 10.10 Multiple Monitor Detection
- If student connects second monitor during exam: warning shown — "Multiple display detected. Please disconnect additional monitors."
- Event logged; invigilator alerted

### 10.11 Virtual Machine Detection
- Exam running inside VM: flagged (advisory)
- Combined with other flags: escalates suspicion score

### 10.12 IP Address Monitoring
- Multiple students submitting from same IP: flagged — "3 students sharing same IP — possible proxy"
- Geolocation check (configurable): if institution requires campus-only exam, student IP geolocated; off-campus flagged

### 10.13 Suspicion Score
- Each flag type has a weight:
  - Tab switch (×1 per occurrence), full-screen exit (×2), screenshot (×3), multiple face (×5), no-face extended (×3), VPN (×2), multiple device (×5), IP sharing (×4)
- Suspicion score calculated per student
- Dashboard shows score with flag breakdown
- HOD sets threshold: score > X → "Review Required" tag on student's exam record

---

## 11. Invigilator App & Physical Exam Management

### 11.1 Invigilator Role & Assignment
- Invigilators assigned to exam halls by Admin before exam
- Chief Invigilator: one per exam; oversees all halls; can view all halls' data
- Hall Invigilator: assigned to specific hall(s); sees only their hall's students
- Flying Squad (configurable): roving invigilators not assigned to a hall; can view any hall

### 11.2 Invigilator App Features
- Hall student list with: name, roll number, seat, set code, photo (for identity check)
- QR scanner: scan student admit card QR → identity verified
- Live status: each student's exam status (Not Started / In Exam / Submitted / Flagged / Absent)
- Questions attempted count per student (online exams)
- Flag alerts: real-time — tab switch, face detection, multiple device, etc.
- Remote session terminate: end a specific student's exam session (unfair means action)

### 11.3 Physical Attendance Marking
- Invigilator opens hall attendance list in app
- Marks each student: Present / Absent at exam start
- Late arrivals: marked Present with late-entry time stamp
- Attendance auto-synced to exam record
- Discrepancy alert: if total Present + Absent ≠ total enrolled for hall

### 11.4 Late Entry Management
- Configurable late window: 0–30 minutes from exam start
- After late window: hall sealed; no new entries
- Late entrant: marked Present + Late; late entry time logged; no extra time compensated
- Post-late-window: hall door sealed; invigilator reports any attempt to enter

### 11.5 OMR / Answer Booklet Distribution Tracking
- Invigilator scans each OMR sheet barcode / answer booklet barcode at distribution
- Linked to student roll number
- At collection: scan again; reconciliation — issued vs collected
- Missing booklet: immediate alert; invigilator reports
- Supplementary booklet: scanned and linked to primary booklet barcode

### 11.6 Unfair Means Incident Report
Form fields:
- Student name, roll number, section, seat number
- Incident type: Copying from adjacent student / Cheat sheet found / Mobile phone found / Impersonation / Talking / Carrying prohibited material / Other
- Description (free text)
- Witness (co-invigilator name)
- Evidence: note text in app (no file upload)
- Action taken: Warning given / Paper seized / Student expelled from hall / Paper cancelled
Auto-notifies: Principal, HOD, Admin immediately on submission.

### 11.7 Paper Shortage Alert
- Invigilator reports: "Question paper copies insufficient for hall"
- Admin notified; emergency printing initiated
- Affected students: given extra time equivalent to delay

### 11.8 Exam Halt & Resume
- Chief Invigilator or Admin triggers emergency halt
- All online student sessions: exam state frozen; timer paused
- Physical exams: invigilator instructs students to stop writing
- Resume: Chief Invigilator triggers resume; timer restarts from paused point; all students notified in-app
- Halt reason logged (fire alarm / power cut / administrative instruction / security threat)

---

## 12. Exam Submission

### 12.1 Manual Submission
- "Submit Paper" button prominent in header
- Double-confirmation popup:
  - Shows: sections completed, questions answered, questions unanswered, questions marked for review
  - Option to go back and review
  - "Submit Now" confirmation button

### 12.2 Auto-Submit at T=0
- Timer reaches zero: auto-submit fires for all active sessions
- All answers in last auto-save included
- Student sees: "Time expired. Your paper has been auto-submitted."

### 12.3 Grace Time
- Configurable 0–5 minutes post time-expiry
- During grace: submission still accepted; marked as "submitted within grace period" — valid submission
- After grace: session locked; no new submissions

### 12.4 Submission Receipt
- Immediate on-screen receipt:
  - Submission timestamp
  - Questions attempted / total
  - Sections completed
  - Reference number (submission_id)
- "Your answers have been securely recorded." confirmation

### 12.5 Submission Locked
- Once submitted: student cannot re-enter exam
- App shows: "Exam submitted. Results will be available on [configured release date/time]."

### 12.6 Partial Submission (Disconnected Students)
- Student disconnects and never reconnects before deadline:
  - At deadline + grace time: auto-submit fires using last auto-saved state from server
  - If only local save available: server retrieves local save sync on next login
  - Partial submission flag: "Submitted via auto-save — possible connection issue" in invigilator record

### 12.7 Submission Audit Trail
- Per question: all answer changes with timestamps
- Final submitted answer per question
- Submission method: Manual / Auto-time-expiry / Grace period / Partial-auto-save
- Device info: device_id, OS, browser/app version
- Connection log: connected/disconnected events with timestamps
- Full audit accessible to HOD for dispute resolution

---

## 13. Post-Exam Review & Answer Key

### 13.1 Answer Key Release Timing
Configurable per exam:

| Option | Behaviour |
|---|---|
| Immediate | Answer key visible to student as soon as they submit |
| After All Submit | Released when last student submits (or deadline passes) |
| Scheduled | Released at specific admin-set date-time |
| Manual | HOD/Admin manually triggers release |
| Never | For exams where answer key is not shared with students |

### 13.2 Student Review Mode (Post-Release)
Student sees their submitted paper with:
- Own answer highlighted: Correct (green) / Incorrect (red) / Not Attempted (grey)
- Correct answer shown per question
- Marks earned per question
- Full solution (all content blocks from Module 17): text, LaTeX, diagrams, charts
- Watch Video button: "Watch Solution: [topic concept]" — opens in-app WebView
- Hints (revealed): if student used hints, shown in review
- Time spent per question vs class average

### 13.3 Score & Grade Display
- Total marks earned, total marks, percentage
- Grade (A+ / A / B+ / B / C / D / Fail) per institution's grading scale
- Rank: position in class/batch/section
- Percentile: within class / within institution / within EduForge cohort (anonymised)
- Passing status: Pass / Fail / Detained (configurable threshold)

### 13.4 Section-Wise Analysis
- Marks earned per section
- Accuracy % per section
- Questions attempted vs total per section

### 13.5 Bloom's Level Performance
- Score breakdown: L1–L2 (Recall) / L3 (Apply) / L4–L6 (HOTS)
- Shows if student's weakness is recall, application, or higher-order thinking

### 13.6 Difficulty-Wise Performance
- Accuracy on: Easy / Medium / Hard / Very Hard
- "You scored X% on Hard questions — above class average of Y%"

### 13.7 Weak Topic Identification
- Topics where student scored < 40%: listed as "Focus Areas"
- Direct links: "Read Notes" (Module 16) + "Practice Questions" (Module 17)
- Auto-added to student's spaced repetition queue (Module 17)

### 13.8 Time Analysis
- Average time per question vs class average
- Questions where student spent too long (> 2× class average): flagged as "Time traps"
- Questions answered fastest: correlated with correctness (quick-correct vs quick-wrong analysis)

---

## 14. Evaluation Workflow

### 14.1 Auto-Grading (Objective)
- MCQ Single / Multiple, True/False, Numerical, Integer, Decimal, Match, Assertion-Reason, Sequence:
  auto-graded immediately on submission using Module 18 answer key JSON
- Tolerance range applied for numerical (from Module 18 marking scheme)
- Per-set answer key used (Set A student graded with Set A key)
- Score available immediately after submission for objective-only exams

### 14.2 Manual Evaluation Queue (Descriptive)
- Short Answer and Long Answer questions → queued for teacher evaluation (Module 20)
- Queue appears in teacher's evaluation dashboard in Module 20
- HOD sets evaluation deadline; alert sent if teacher hasn't started by 50% of deadline

### 14.3 Multi-Evaluator Assignment
- Long papers split across evaluators:
  - "Teacher A evaluates Q1–Q15 for all students"
  - "Teacher B evaluates Q16–Q30 for all students"
- Or by student batch: "Teacher A evaluates Section A students; Teacher B evaluates Section B"
- Configured per exam before evaluation starts

### 14.4 Blind Evaluation (Centralised)
- Pre-board and annual exams: student identity masked from evaluator
- Evaluator sees: barcode ID + question answers; not student name/roll number
- Identity revealed only after all marks entered (un-masking triggered by HOD)

### 14.5 Double Evaluation
- Configurable for high-stakes exams
- Second evaluator independently grades same answers
- System compares: if difference > configurable threshold (e.g., > 5 marks) → sent to third evaluator (Head of Department)
- Final marks: average of two evaluations OR higher of two (per institution policy)

---

## 15. Re-Examination & Supplementary Exam

### 15.1 Absentee Re-Exam
- Students absent with valid reason (medical certificate / emergency) eligible for re-exam
- Re-exam scheduled on different date
- Different paper auto-generated from Module 18 (parallel set, zero overlap with original)
- Absence reason documented; medical certificate noted in record (certificate brought physically; Admin notes receipt — no upload)

### 15.2 Medical Exemption
- Student with medical condition: HOD approves exemption
- Exempted exam: marked "EX" in result (not counted in average)
- Re-exam scheduled after recovery; alternative assessment per institution policy
- Aligned with CBSE Circular on CWSN and medical cases

### 15.3 Improvement Exam
- Students below passing marks can appear in improvement exam (institution policy on/off)
- Improvement exam: same scope, different paper
- Both original and improvement scores recorded; higher considered (configurable)

### 15.4 Supplementary / Compartment Exam
- Scope restricted to topics/chapters where student failed
- Paper auto-configured from Module 18 supplementary exam type
- Module 15 scope: only failed units included in paper generation

### 15.5 Re-Totalling Request
- Student submits re-totalling request within configurable window (e.g., 7 days from result)
- System re-tally: sum all marks from Module 20 evaluation records
- Discrepancy found: corrected with audit log; result updated; notification to student and parent
- No answer re-evaluation in re-totalling (only marks addition re-checked)

---

## 16. Exam Postponement & Cancellation

### 16.1 Postponement
- HOD/Admin reschedules: new date + time entered
- All enrolled students: in-app notification immediately — "Exam [name] has been rescheduled to [new date/time]"
- Parent notification (school students + minors): parent app updated
- Admit card: auto-updated with new date/time (student refreshes app to see)
- Module 18 paper: unchanged; same paper used on new date

### 16.2 Cancellation
- Exam cancelled with documented reason
- Students notified in-app
- Exam record: archived with cancellation reason and date
- Module 18 paper: preserved in paper bank
- If partially conducted: partial attendance and answers preserved in archive

### 16.3 Emergency Halt & Resume
(See Section 11.8)

---

## 17. NTA Score Simulation (JEE/NEET Coaching Mock)

### 17.1 JEE Main NTA Score Simulation
For JEE Main mock tests:
- Raw score calculated from attempted questions
- NTA normalised score: percentile-based across all students who took same mock
- Formula: NTA Score = (100 × students with raw score ≤ candidate) / total students
- Displayed: Raw Score / Total Marks / NTA Score (out of 100 per subject + overall)
- Predicted rank band: based on NTA score → mapped to JEE Main counselling rank ranges
- Comparison: "Your NTA score: 85.4 | Top 10% of students in this mock test"

### 17.2 NEET Score vs Cutoff
For NEET UG mock tests:
- Score calculated per subject (Physics / Chemistry / Biology)
- Score vs last 5 years' category-wise NEET cutoffs displayed:

| Category | Your Score | 2023 Cutoff | 2022 Cutoff | Status |
|---|---|---|---|---|
| General | 520 | 715 | 720 | Below |
| OBC | 520 | 650 | 660 | Below |
| SC | 520 | 590 | 600 | Below |
| ST | 520 | 540 | 545 | ✅ Would qualify (2023) |

### 17.3 All-India Rank Estimation
- For coaching institutions: mock tests taken by students across multiple batches/institutions
- Rank estimated based on: own score vs distribution of all EduForge students who took the same mock pattern
- Shown as: "Estimated All-India Rank (from EduForge mock cohort): ~45,000–55,000"
- Disclaimer: "This is an estimate based on internal mock data. Official ranks depend on actual exam performance."

---

## 18. Exam Analytics & Reports

### 18.1 Live Exam Dashboard (During Exam)
Real-time view for HOD/Admin:

| Metric | Display |
|---|---|
| Total enrolled | Count |
| Students online | Count + % |
| Not yet started | Count |
| Submitted | Count |
| Disconnected | Count + list |
| Flagged | Count + list (with flag type) |
| Average questions attempted | Number |
| Questions answered per section | Bar chart (live) |

### 18.2 Post-Exam Instant Report
Generated immediately after all submissions (or deadline):
- Total enrolled / appeared / absent / submitted / auto-submitted
- Average score, highest score, lowest score, median score
- Standard deviation
- Grade distribution: count and % per grade band
- Section-wise class average
- Pass % and fail %

### 18.3 Rank List
- Class/batch/section-wise rank list
- Ties: same rank if same score; secondary sort by submission time (earlier = higher for same score)
- Rank list published to students: configurable (show rank or hide rank)
- Rank list export: Excel per exam

### 18.4 Percentile Calculation
- Within class: student's percentile among classmates
- Within institution: all students of same grade/subject
- EduForge cohort (anonymised): institution's class average vs anonymised cohort of same board/grade

### 18.5 Subject-Level Multi-Exam Trend
- Per student: score trend across all exams in same subject this academic year (line chart)
- Per class: class average trend across exam series
- Used in PTM (Module 33) and report card (Module 21)

### 18.6 Exam Series Analytics
- Series-level performance: each test in series shown as time series
- Topic-wise accuracy across all tests in series: identifies persistent weak areas
- Improvement rate: % improvement from Test 1 to latest test

### 18.7 Cohort Benchmark
- Institution's average % score in this exam vs anonymised EduForge platform cohort (same board/grade/subject)
- "Your Class 12 Physics Mid-Term average: 61% | Platform cohort average: 64%"
- Opt-in per institution (DPDPA 2023 — institutional data only, no student data shared)

---

## 19. Compliance & Archival

### 19.1 Exam Integrity Certificate
Auto-generated per exam after completion:
- Exam name, date, subject, total students
- Paper lock timestamp + hash (from Module 18)
- Set generation details
- Proctoring level applied
- Flag count (by type)
- Submission count / auto-submit count
- Evaluation completion date
- Principal digital signature field
- Stored in Module 40 institution document vault

### 19.2 CBSE / Board Submission Readiness
For pre-board and internal exams where board submission is required:
- Package generated: attendance sheet + question paper PDF + answer key PDF + marks tabulation
- Format aligned to CBSE / state board prescribed format
- Principal/HOD signs marks tabulation (digital signature field + physical print option)

### 19.3 AISHE Exam Data Export (College)
- Total students appeared per subject per semester
- Pass / fail counts
- Marks distribution
- Exported to AISHE (All India Survey on Higher Education) annual data format
- Used for NAAC Criterion 2 evidence

### 19.4 NAAC Evidence
- Criterion 2.5 (Evaluation Process and Reforms): exam records, question paper quality scores (Module 18), evaluation completion rates, re-checking requests, grievance resolutions
- Criterion 2.6 (Student Performance): pass %, grade distribution, improvement over years
- Export: NAAC SSR prescribed table format (Excel/PDF)

### 19.5 5-Year Exam Record Retention
- All exam records retained for 5 academic years:
  - Attendance, submitted answers, scores, flags, evaluation records, integrity certificates
- Auto-archived (not deleted) after 5 years; accessible to Admin only
- DPDPA 2023: student answer data is personal data; retained under legitimate exam administration purpose; deletable on request after 5-year statutory period

### 19.6 Anti-Ragging Compliance During Exam
- Male and female students in same hall: invigilator assignment must include at least one male + one female invigilator (CBSE/UGC mandate)
- POCSO compliance: female students below 18 must have female invigilators present in hall at all times
- Violations of gender-invigilator rule flagged before exam start (system checks invigilator assignments)

---

## 20. Exam Calendar Integration

### 20.1 Institution Exam Calendar
- All scheduled exams appear in institution calendar (Module 05 academic calendar)
- Colour-coded by exam type (Unit Test / Periodic / Mid-Term / Pre-Board / Mock / Sessional)
- Exam conflict auto-detected on calendar: same student two exams same time → red flag

### 20.2 Student Personal Exam Calendar
- Student sees only their own exams: subject, date, time, hall, seat, admit card link
- iCal / reminder integration: student can add exam to device calendar (read-only export)
- Day-before reminder: in-app notification at 8 PM the night before each exam

### 20.3 Teacher Exam Duty Calendar
- Teacher sees: subjects they set papers for, exams they are assigned to invigilate, evaluation deadlines
- Duty conflicts: auto-flagged to Admin

---

## 21. Student Grievance During Exam

### 21.1 "Raise Hand" Feature (Online Exam)
- Student taps "Help" button during exam
- Invigilator dashboard: notification shows — "Student X [name] needs help — currently on Q14"
- Invigilator responds via in-app private chat (one-to-one)
- Chat is text-only; no file transfer
- All chats logged in exam record

### 21.2 Question Objection During Exam
- Student taps "Flag Question" → selects reason: Ambiguous / Printing error / Wrong question / Factual error / Translation error
- Flag sent to HOD dashboard in real time
- HOD reviews; can issue a broadcast clarification to ALL students in exam simultaneously
- Broadcast message appears as banner in all students' exam interface
- Broadcast logged with: HOD name, message text, timestamp, questions acknowledged by students

### 21.3 Post-Exam Grievance
- Student submits written objection within configurable window (e.g., 3 days)
- Objection types: Wrong answer key / Marking error / Technical issue during exam / Unfair means allegation against student (counter-complaint)
- HOD reviews and responds; resolution documented
- Grace marks workflow triggered if objection is upheld (Module 18)

---

## 22. Data Architecture

### 22.1 Tenancy
- All exam session data tagged with `tenant_id` (PostgreSQL RLS)
- Proctoring snapshots on CDN: `/proctoring/{tenant_id}/{exam_id}/{student_id}/` — signed URL access only
- Exam papers on CDN: served from Module 18 CDN paths (time-locked)
- Answer data: stored in DB per student per question (not on CDN — exam integrity requires DB)

### 22.2 Database Schema

```sql
-- Exam master
exams (
  exam_id             UUID PK,
  tenant_id           UUID FK tenants,
  branch_id           UUID FK branches,
  exam_name           VARCHAR(300),
  exam_type           VARCHAR(30),
  subject_id          UUID FK subjects_master,
  board_id            UUID FK boards NULL,
  grade               VARCHAR(20),
  academic_year_id    UUID FK academic_years,
  series_id           UUID NULL,
  scheduled_date      DATE,
  start_time          TIME,
  duration_minutes    INTEGER,
  total_marks         NUMERIC(6,1),
  passing_marks       NUMERIC(6,1) NULL,
  exam_mode           VARCHAR(10),               -- ONLINE | OFFLINE | HYBRID
  proctoring_level    VARCHAR(10),               -- NONE | BASIC | STANDARD | STRICT
  late_window_minutes INTEGER DEFAULT 0,
  grace_minutes       INTEGER DEFAULT 0,
  answer_key_release  VARCHAR(20),               -- IMMEDIATE | AFTER_ALL | SCHEDULED | MANUAL | NEVER
  answer_key_at       TIMESTAMPTZ NULL,
  score_release       VARCHAR(20),
  score_release_at    TIMESTAMPTZ NULL,
  exam_token          VARCHAR(10) NULL,
  status              VARCHAR(20) DEFAULT 'DRAFT',
  -- DRAFT | PUBLISHED | ONGOING | COMPLETED | CANCELLED | POSTPONED
  created_by          UUID FK users,
  created_at          TIMESTAMPTZ,
  updated_at          TIMESTAMPTZ
)

-- Exam-paper linkage (which set goes to which exam)
exam_papers_map (
  map_id              UUID PK,
  exam_id             UUID FK exams,
  paper_id            UUID FK exam_papers,
  set_code            VARCHAR(5)
)

-- Exam halls
exam_halls (
  hall_id             UUID PK,
  tenant_id           UUID FK tenants,
  exam_id             UUID FK exams,
  hall_name           VARCHAR(100),
  building            VARCHAR(100) NULL,
  floor               VARCHAR(20) NULL,
  rows                INTEGER,
  columns             INTEGER,
  capacity            INTEGER,
  is_cwsn_accessible  BOOLEAN DEFAULT FALSE,
  chief_invigilator_id UUID FK users NULL,
  created_at          TIMESTAMPTZ
)

-- Seating plan
exam_seating (
  seating_id          UUID PK,
  exam_id             UUID FK exams,
  hall_id             UUID FK exam_halls,
  student_id          UUID FK users,
  roll_number         VARCHAR(30),
  set_code            VARCHAR(5),
  row_no              INTEGER,
  col_no              INTEGER,
  seat_label          VARCHAR(20),
  is_cwsn             BOOLEAN DEFAULT FALSE,
  is_scribe_seat      BOOLEAN DEFAULT FALSE,
  created_at          TIMESTAMPTZ
)

-- Invigilator assignment
exam_invigilators (
  assignment_id       UUID PK,
  exam_id             UUID FK exams,
  hall_id             UUID FK exam_halls NULL,   -- NULL = flying squad
  invigilator_id      UUID FK users,
  role                VARCHAR(20),               -- CHIEF | HALL | FLYING_SQUAD
  assigned_by         UUID FK users,
  created_at          TIMESTAMPTZ
)

-- Student exam sessions (online)
exam_sessions (
  session_id          UUID PK,
  exam_id             UUID FK exams,
  student_id          UUID FK users,
  tenant_id           UUID FK tenants,
  roll_number         VARCHAR(30),
  set_code            VARCHAR(5),
  device_id           VARCHAR(100) NULL,
  ip_address          INET NULL,
  system_check_result JSONB NULL,
  face_match_score    NUMERIC(4,3) NULL,
  declaration_signed  BOOLEAN DEFAULT FALSE,
  declaration_at      TIMESTAMPTZ NULL,
  exam_token_entered  BOOLEAN DEFAULT FALSE,
  started_at          TIMESTAMPTZ NULL,
  submitted_at        TIMESTAMPTZ NULL,
  submit_method       VARCHAR(20) NULL,          -- MANUAL | AUTO_TIME | GRACE | PARTIAL_AUTO
  total_marks_earned  NUMERIC(6,1) NULL,
  objective_marks     NUMERIC(6,1) NULL,
  descriptive_marks   NUMERIC(6,1) NULL,
  grade               VARCHAR(5) NULL,
  rank                INTEGER NULL,
  percentile          NUMERIC(5,2) NULL,
  suspicion_score     INTEGER DEFAULT 0,
  is_flagged          BOOLEAN DEFAULT FALSE,
  flag_reviewed       BOOLEAN DEFAULT FALSE,
  status              VARCHAR(20) DEFAULT 'NOT_STARTED',
  -- NOT_STARTED | DEMO | IN_EXAM | SUBMITTED | ABSENT | EXPELLED
  created_at          TIMESTAMPTZ
)

-- Per-question answers
exam_answers (
  answer_id           UUID PK,
  session_id          UUID FK exam_sessions,
  question_id         UUID FK questions,
  question_version    INTEGER,
  tenant_id           UUID FK tenants,
  section_id          UUID FK paper_sections,
  response_json       JSONB,                     -- student's answer
  is_marked_review    BOOLEAN DEFAULT FALSE,
  is_correct          BOOLEAN NULL,              -- NULL until evaluated
  marks_earned        NUMERIC(4,1) NULL,
  hints_used          INTEGER DEFAULT 0,
  time_spent_seconds  INTEGER DEFAULT 0,
  language_used       VARCHAR(10),
  last_changed_at     TIMESTAMPTZ,
  change_count        INTEGER DEFAULT 0,
  answer_history      JSONB NULL                 -- [{answer, timestamp}, ...]
)

-- Proctoring flags
proctoring_flags (
  flag_id             UUID PK,
  session_id          UUID FK exam_sessions,
  flag_type           VARCHAR(30),
  -- TAB_SWITCH | FULLSCREEN_EXIT | COPY_PASTE | SCREENSHOT | MULTIPLE_FACE
  -- NO_FACE | AUDIO_ANOMALY | VPN | MULTIPLE_DEVICE | MULTI_MONITOR | IP_SHARING
  severity            INTEGER,                   -- weight (1–5)
  snapshot_cdn_path   TEXT NULL,
  details             JSONB NULL,
  reviewed_by         UUID FK users NULL,
  review_action       VARCHAR(20) NULL,          -- FALSE_POSITIVE | CONFIRMED | DISMISSED
  created_at          TIMESTAMPTZ
)

-- Physical attendance
exam_attendance (
  attendance_id       UUID PK,
  exam_id             UUID FK exams,
  hall_id             UUID FK exam_halls,
  student_id          UUID FK users,
  roll_number         VARCHAR(30),
  status              VARCHAR(15),               -- PRESENT | ABSENT | LATE | EXPELLED
  late_minutes        INTEGER NULL,
  marked_by           UUID FK invigilators NULL,
  marked_at           TIMESTAMPTZ,
  notes               TEXT NULL
)

-- Unfair means incidents
unfair_means_incidents (
  incident_id         UUID PK,
  exam_id             UUID FK exams,
  hall_id             UUID FK exam_halls NULL,
  student_id          UUID FK users,
  reported_by         UUID FK users,
  incident_type       VARCHAR(50),
  description         TEXT,
  action_taken        VARCHAR(50),
  witness_id          UUID FK users NULL,
  notified_principal  BOOLEAN DEFAULT FALSE,
  created_at          TIMESTAMPTZ
)

-- Re-exam / supplementary
reexam_schedule (
  reexam_id           UUID PK,
  original_exam_id    UUID FK exams,
  student_id          UUID FK users,
  reexam_type         VARCHAR(20),               -- ABSENTEE | IMPROVEMENT | SUPPLEMENTARY
  reason              TEXT,
  new_exam_id         UUID FK exams NULL,
  approved_by         UUID FK users,
  created_at          TIMESTAMPTZ
)
```

### 22.3 Indexes
```sql
CREATE INDEX idx_sessions_exam        ON exam_sessions(exam_id, status);
CREATE INDEX idx_sessions_student     ON exam_sessions(student_id, exam_id);
CREATE INDEX idx_answers_session      ON exam_answers(session_id, question_id);
CREATE INDEX idx_answers_question     ON exam_answers(question_id, is_correct);
CREATE INDEX idx_flags_session        ON proctoring_flags(session_id, flag_type);
CREATE INDEX idx_attendance_exam_hall ON exam_attendance(exam_id, hall_id, status);
CREATE INDEX idx_seating_exam         ON exam_seating(exam_id, student_id);
```

---

## 23. Roles & Permissions

| Action | Student | Invigilator | Teacher | HOD | Principal | Admin |
|---|---|---|---|---|---|---|
| View own exam schedule | ✅ | — | ✅ | ✅ | ✅ | ✅ |
| View / download admit card | ✅ own | — | — | ✅ | ✅ | ✅ |
| Take online exam | ✅ own | — | — | — | — | — |
| Mark physical attendance | — | ✅ own hall | — | — | — | ✅ |
| View live dashboard | — | ✅ own hall | — | ✅ | ✅ | ✅ |
| File unfair means report | — | ✅ | — | ✅ | ✅ | ✅ |
| Terminate student session | — | ✅ | — | ✅ | ✅ | ✅ |
| Halt / resume exam | — | Chief only | — | ✅ | ✅ | ✅ |
| View proctoring flags | — | ✅ own hall | — | ✅ | ✅ | ✅ |
| Review proctoring snapshots | — | — | — | ✅ | ✅ | ✅ |
| Issue broadcast clarification | — | — | — | ✅ | ✅ | — |
| Grant re-exam | — | — | — | ✅ | ✅ | ✅ |
| View post-exam analytics | Own results | — | Own subject | Dept | All | All |
| Export NAAC/AISHE data | — | — | — | ✅ | ✅ | ✅ |

---

## 24. Notifications (In-App Only)

| Trigger | Recipient |
|---|---|
| Exam published / scheduled | Student, Parent (school/minor) |
| 7-day reminder | Student |
| 24-hour reminder | Student, Invigilator |
| 2-hour reminder | Student |
| 30-minute reminder | Student |
| Admit card available | Student |
| Exam postponed / cancelled | Student, Invigilator, Parent |
| Demo test available | Student |
| Exam started (live) | Invigilator confirmation |
| Student raised hand during exam | Invigilator |
| Question flagged during exam | HOD |
| HOD broadcast clarification | All students in exam |
| Proctoring flag raised (multiple face / no face / multiple device) | Invigilator |
| Student disconnected > 5 min | Invigilator |
| Unfair means report filed | Principal, HOD, Admin |
| Exam emergency halt / resume | All active students, all invigilators |
| Auto-submit fired (time expired) | Student (confirmation) |
| Answer key released | Student |
| Score / rank published | Student, Parent (school/minor) |
| Re-exam scheduled | Student, Parent |
| Evaluation deadline approaching | Teacher (Module 20) |
| Grace marks granted | Student |
| Re-totalling result | Student |

---

## 25. Compliance Summary

| Standard | Coverage |
|---|---|
| CBSE Exam Conduct Guidelines | Pre-board pattern fidelity, invigilator gender mandate, CWSN extra time, unfair means procedure |
| NEP 2020 | Competency-based assessment exam types, open-book exam support, online mode |
| UGC Examination Reforms | Online exam delivery, centralised evaluation, blind evaluation, re-totalling |
| RTE Act 2009 / RPWD Act 2016 | CWSN adapted paper, exam exemption, scribe support, extended time (25%), accessible seating |
| POCSO Act 2012 | Female invigilator mandatory for halls with female students below 18; flagged if not assigned |
| Anti-Ragging (Supreme Court / UGC 2009) | Mixed seating (different sections); incident reporting; Principal notification |
| DPDPA 2023 | Proctoring snapshots: 90-day retention + auto-delete; audio not recorded; student data 5-year retention; deletion on request after statutory period; anonymised cohort benchmarking |
| IT Act 2000 | Exam integrity certificate with digital hash; access logs; tamper detection |
| AISHE | College exam data export (appeared / passed / marks distribution) |
| NAAC SSR Criterion 2 | Exam records, evaluation reforms, student performance data for accreditation |
| State Board Compliance | State-specific exam conduct rules configurable; board submission package generation |
| NTA Pattern (JEE/NEET Mock) | Pattern fidelity validated per exam type; NTA score simulation for JEE Main; NEET cutoff comparison |
