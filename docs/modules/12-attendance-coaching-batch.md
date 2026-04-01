# Module 12 — Attendance (Coaching & Batch)

## Purpose
Define how EduForge captures, validates, manages, and reports student attendance specifically for coaching centres and batch-based institutions — covering small local tutors to large national chains (ALLEN, Aakash, Resonance, FIITJEE scale), government skill development batches (PMKVY/DDU-GKY), residential coaching (Kota model), competitive exam coaching (JEE/NEET/UPSC/CA/Banking), and state coaching regulation compliance (Rajasthan Coaching Regulation Act 2023 and emerging state laws).

All advanced features in this module are **optional per institution config** — small coaching centres can operate with basic teacher-marks-attendance only.

---

## 1. Batch-Session as the Attendance Unit

- Coaching attendance is per **batch session**, not period-wise like school (Module 11)
- Each scheduled batch session = one independent attendance entry
- All calculation — percentage, total hours, eligibility check — is session-based
- A student in multiple batches (JEE Maths + JEE Physics + Test Series) has completely independent attendance records per batch; no cross-contamination between batches
- Session-level data is the authoritative record; batch-level summaries are computed aggregates

---

## 2. Multi-Batch Student Tracking

- Student enrolled in N batches: N separate attendance records, one per batch
- Each batch attendance calculated independently:
  - Batch A: 80% attendance
  - Batch B: 65% attendance → Batch B eligibility blocked; Batch A unaffected
- Student's combined schedule (all enrolled batches) shown in their personal timetable view (Module 10 Point 26 — cross-batch conflict detection)
- Admin sees student's enrollment across all batches in a single profile view

---

## 3. Session Hours Tracking

- Each session has a defined duration (configured in batch schedule, Module 10 Point 24)
- System tracks: sessions attended AND total hours attended
- Total hours = Σ (attended sessions × session duration)
- Partial sessions (late entry, early exit, partial cancellation) contribute fractional hours based on actual time present
- Hours accumulated across all sessions of a batch; displayed on student dashboard

---

## 4. Minimum Hours Completion Requirement

- Batch-level config: minimum X hours required for eligibility (certificate, internal test, batch completion)
- Example: JEE Advanced batch — 240 planned hours; minimum 180 hours required for completion certificate
- Configurable per batch:
  - Minimum percentage only (e.g., 75%)
  - Minimum hours only (e.g., 180 hours)
  - Both (e.g., 75% AND 180 hours — whichever is stricter)
- PMKVY government batches: NSDC mandates minimum 80% of total session hours for assessment eligibility
- Real-time counter shown to student: "You have completed [X] of [Y] required hours"

---

## 5. Percentage vs Hours — Dual Tracking

- Both metrics tracked simultaneously regardless of which is the eligibility criterion
- Dashboard shows: attendance %, total hours attended, sessions attended, sessions missed
- Center director can switch eligibility criterion without losing historical data
- Reports can be filtered by: percentage view, hours view, or combined view
- For PMKVY/NSDC: hours-based tracking is mandatory; percentage is supplementary

---

## 6. Teacher / Faculty Attendance at Batch

- Teacher checks in to their batch session via app or biometric before starting attendance marking
- Teacher attendance is the upstream trigger for session status:
  - Teacher checked in = Session "Conducted"
  - Teacher absent, no substitute = Session "Cancelled"
  - Substitute present = Session "Conducted — Substituted"
- Teacher late check-in logged with timestamp; if > 15 minutes late, session tagged "Teacher Late"
- Teacher attendance data feeds management reports and teacher appraisal (Module 08)

---

## 7. Teacher Attendance vs Student Attendance Correlation

- Monthly analytics: compare student attendance % across batches taught by the same teacher vs same subject taught by other teachers
- If Teacher A's JEE Chemistry batch has 60% average student attendance vs Teacher B's JEE Chemistry batch at 85%: management flagged
- Possible interpretations: teaching quality concern, scheduling inconvenience, or student dissatisfaction
- Flagged to center director; used in appraisal discussion (Module 08)
- Not used as sole evidence of poor performance — context investigated before action

---

## 8. Teacher Marks Batch Session Attendance

- Teacher opens active batch session in their app → marks each enrolled student
- Default: all absent; teacher marks exceptions as Present (faster for large batches where most are present: bulk-mark-present option → mark exceptions as absent)
- Or default: all present; teacher marks absences (configurable per center preference)
- Student list shows: name, photo, roll number, last session status (quick context)
- Voice-assisted roll call option: teacher calls name, app confirms tap

---

## 9. Biometric Entry at Coaching Centre

- Fingerprint / RFID reader at coaching centre entry (main gate or classroom door)
- Entry timestamp stored; cross-referenced with session attendance
- Gate biometric ≠ session attendance — both maintained independently
- Anomaly: student has gate biometric entry but teacher marked absent = flagged for investigation
- Reverse anomaly: student marked present by teacher but no biometric entry that day = also flagged
- Common in large coaching chains: ALLEN, Aakash, Resonance, Vedantu offline centers

---

## 10. Student Self-Check-In Kiosk

- Large coaching centers (500+ students): student taps ID card or scans face at entry kiosk
- Auto-marks Present for the active batch session at that time (batch identified from student's enrollment + current time)
- If student is enrolled in two batches at overlapping times: system prompts student to select batch
- Kiosk check-in confirmed by teacher's roll call (kiosk = initial mark; teacher can override within session)
- Reduces teacher roll call time for large batches (200+ students)

---

## 11. Physical ID Card Scan at Entry

- Simpler alternative to biometric — no finger condition issues (dusty/dry hands in students)
- ID card has barcode / QR code printed on it (generated at enrolment, Module 07)
- Student scans card at entry point scanner; auto-marks present for active batch
- Lost card: admin deactivates old card, issues new card with same student ID
- Common in medium-sized coaching centers (100–500 students); low hardware cost vs biometric

---

## 12. QR Code Session Attendance

- Teacher generates time-limited QR code for the current session via app
- Displayed on classroom projector / screen or shared as in-app prompt to students
- Students scan within window (configurable: 5–15 minutes from session start)
- QR code is session-specific: encrypted with batch ID + session ID + date + timestamp
- Cannot be reused across sessions or forwarded — device fingerprint check prevents proxy scanning
- Students who miss QR window: manually corrected by teacher within 24 hours

---

## 13. Offline Marking with Sync

- Teacher marks attendance offline (no internet connectivity)
- Data stored locally on device with precise timestamp
- Auto-syncs when connection restored
- Conflict resolution: if same session has both offline marks and online marks (e.g., QR scan also processed), system shows conflict screen to teacher; teacher resolves
- Sync delay logged: "Marked offline at [time]; synced at [time]"
- Critical for: small coaching centers in semi-urban/rural areas, basement classrooms, power-cut scenarios

---

## 14. Bulk Import from Biometric Device

- Large centers using standalone biometric devices (ZKTeco, BioMax, Matrix, Realtime):
  - Device exports daily attendance log as CSV
  - Admin uploads CSV to EduForge or API integration pulls automatically
  - System maps device employee/student IDs to EduForge student IDs
  - Device-imported marks overridable by teacher within 24 hours (device read errors, biometric failures)
- API integration optional; CSV upload always available as fallback

---

## 15. Regular Batch Session Attendance

- Standard lecture/tutorial session; forms the base of attendance percentage and hours calculation
- Status options: Present / Absent / Late / Authorized Absent / Medical Absent / Exam Day / On Duty
- Marked per student per session
- Session record contains: batch ID, session date, session start time, session end time, conducted by (teacher ID), session type

---

## 16. Doubt Clearing Session Attendance

- Separate session type: "Doubt Session"
- Tracked independently from regular lectures
- Institution config:
  - Option A: Doubt sessions count toward total session attendance (encourages participation)
  - Option B: Doubt sessions tracked separately only (does not affect lecture % — default)
- Student can see doubt session attendance history separate from lecture history
- Teacher marks which specific doubts were addressed (optional diary entry)

---

## 17. Extra / Make-Up Batch Session

- Additional sessions beyond regular schedule (teacher compensating for missed class, pre-exam extras)
- Tagged: "Extra Session" or "Make-Up Session (for [Original Date])"
- Counts toward total hours attended
- Institution config: whether extra sessions count toward percentage denominator (total planned sessions) or not
- Students notified in-app when extra session is scheduled; advance notice configurable (default: 24 hours)

---

## 18. Revision / Crash Course Session

- Intensive short-duration batches (30-day JEE crash course, NEET 45-day intensive, Board revision batch)
- Own independent attendance cycle; own completion threshold
- Separate batch record; does not affect main long-term batch attendance
- Completion threshold often higher (e.g., 85% required for crash course certificate)
- Duration clearly shown: batch start date, batch end date, total planned sessions

---

## 19. Test Series Session Attendance

- Student attends scheduled mock test / test series sessions (Module 22)
- Test attendance tracked completely separately from lecture attendance
- Does not mix with lecture attendance in any report or eligibility calculation
- Test session status: Appeared / Absent / Medical Absent / Exam Day
- Absent from test series session = no penalty to lecture attendance %; but test series certificate may require minimum test appearances
- Test performance data linked to Module 22 Test Series & Mock Tests

---

## 20. Special Workshop / Seminar Attendance

- One-time sessions: exam strategy workshop, time management seminar, motivational session, career counselling talk
- Tracked as "Special Session" type
- Optional — non-attendance does not affect regular batch attendance %
- Certificate of participation generated if student attended (Module 39)
- Used for: student engagement tracking, parent communication ("your child attended X enrichment sessions")

---

## 21. Group Study Supervised Session

- Supervised self-study period at coaching centre (library / study hall)
- Optional participation; separate tracking
- Attendance tracked but does not count in regular lecture attendance
- Useful for: tracking study hall utilisation, identifying serious vs casual students
- Residential coaching: may be mandatory (see Point 82)

---

## 22. Trial / Demo Class Attendance

- Inquiry student (Module 31 Admission CRM) attending trial session
- Attendance recorded in separate "Trial" record — does not affect enrolled students' attendance
- Trial status: Attended / Did Not Attend
- On admission confirmation: student transitions to enrolled; trial record archived
- Trial records used for: conversion rate analytics (how many trial attendees converted to enrolled students)

---

## 23. Online Session Attendance — Hybrid Coaching

- Student joins live online class (Module 45 Live Classes)
- System captures: join time, leave time, total duration present, number of rejoins
- Attendance credit rule (institution config):
  - Must attend ≥ 70% of session duration to count as Present
  - 50–69% = Late / Partial Present (institution decides credit)
  - < 50% = Absent
- Manual override: teacher can mark Present for student with documented connectivity issue within 24 hours
- HOD/center director approves connectivity-related overrides beyond 24 hours

---

## 24. Recorded Lecture Attendance

- Student watches a recorded session (uploaded to platform after live class)
- System tracks watch duration via video player events (play, pause, seek, complete)
- Credit rule (institution config):
  - Watch ≥ 75% of video duration = Attendance credit
  - Prevents gaming: fast-forward through >40% of video = not credited; seek-and-skip detection
- Enabled/disabled per batch — some batches allow recorded makeup; others require live attendance only
- Recorded lecture attendance tagged separately: "Recorded Watch" vs "Live Present"
- Recorded credit cannot exceed 20% of total sessions in a batch (configurable cap — prevents full course via recordings)

---

## 25. Partial Online Attendance

- Student joins for first 30 minutes then disconnects
- Partial credit calculation: time present / session duration × 1 session credit
- Institution config: minimum threshold for any credit (e.g., must attend ≥ 30 minutes to get 0.5 credit)
- Below minimum threshold = Absent
- Partial present shown in attendance history with exact duration

---

## 26. Late Entry to Session

| Arrival Timing | Status |
|---|---|
| Within grace period (configurable: 5–15 min) | Present |
| After grace, within first third of session | Late |
| After first half of session | Partial Present (0.5 credit) |
| After 75% of session elapsed | Absent |

- Grace period configured per batch or per centre
- Late entry logged with timestamp
- Teacher confirms late student was genuinely late (not proxy)
- Multiple late entries: 3 lates in a month = 1 absent equivalent (institution config)

---

## 27. Early Exit from Session

- Student leaves before session ends
- Teacher records: student name, exit time
- Hours present = exit time − session start time
- If hours present < minimum threshold (e.g., 50% of session): marked Absent
- If hours present ≥ threshold: marked Present with "Early Exit" flag
- Parent notification (for < 18 students) if early exit is unplanned

---

## 28. Student Falls Ill During Session

- Teacher marks "Medical Exit" with time student left for medical room / home
- Hours before exit credited; hours after = absent
- If in residential coaching: warden and medical room notified automatically
- Parent notified in-app (for < 18 students): "Your child felt unwell and left the session at [time]. Please contact the centre."
- Follow-up wellness check next session: teacher confirms student is well

---

## 29. Authorized Absent

- Parent / student submits advance leave request (Point 63)
- Class teacher / batch admin approves
- Still counts as absent in percentage calculation
- Does NOT trigger parent surprise notification (parent already aware)
- Visible in attendance history with "Authorized" tag and reason

---

## 30. Medical Absent

- Absent due to illness with medical certificate
- Certificate uploaded within 3 days of return
- Teacher / center admin verifies; marks "Medical Absent"
- Eligible for medical condonation (Point 46)
- Certificate stored in student health record (Module 07)

---

## 31. Exam Day Absent

- Student misses coaching session because they are appearing in:
  - School unit test / mid-term / terminal exam
  - Board examination (CBSE, state board)
  - Competitive exam: JEE Main, JEE Advanced, NEET, CUET, CAT, UPSC, SSC, Banking, CA, CS exams
- Status: "Exam Day" — authorized, does not count against attendance
- Automatic if exam registration date linked in student profile (Module 07 exam registrations field)
- Manual entry if not linked: teacher / admin marks "Exam Day" with exam name
- No condonation needed — exam day is automatically treated as authorized OD

---

## 32. Batch Holiday

- Center admin declares holiday for a specific batch (not institution-wide)
- That session removed from total session count — students not penalized
- Other batches run as normal
- Affected students notified in-app: "Your [Batch Name] session on [Date] has been declared a holiday"
- Batch holiday does not affect other batches' attendance calculation
- Reason logged: festival, teacher unavailability, local event

---

## 33. Cancelled Session

- Teacher absent with no substitute found: session cancelled
- Marked as "Cancelled Session" in batch record
- NOT counted in total sessions denominator — students not penalized
- Students notified in-app immediately with reason and reschedule note (if available)
- Cancelled session can be rescheduled (Point 79)
- Cancelled session report: center director sees monthly count of cancelled sessions per batch and per teacher

---

## 34. Cross-Batch Makeup Class

- Student misses a regular session; can attend the same topic in another batch's session
- Makeup attendance process:
  1. Student attends the other batch's session
  2. That batch's teacher marks the visiting student as "Makeup Present"
  3. System records makeup in original batch's attendance with "Makeup" tag
- Cross-batch makeup requires: same subject, same centre (or same chain branch), within makeup validity window (configurable: default 7 days from missed session)
- Makeup counted in original batch's attended sessions

---

## 35. Makeup Policy Configuration

Institution admin configures per batch:
- Allowed or not allowed
- Maximum makeups per student per month (default: 2)
- Scope: same-subject-only, or any teacher, or any batch
- Makeup validity window: days after missed session within which makeup must happen (default: 7 days)
- Double-count prevention: system checks student is not already marked present in their own batch on the same day (cannot attend both original and makeup on same day)

---

## 36. Makeup Attendance Calculation

- Makeup sessions counted in total attended sessions for the original batch
- Clearly tagged "Makeup" in history (student knows which sessions were makeup)
- Double-count protection: if student attended makeup AND their original batch ran the same day: only one attendance credited per day per subject (teacher confirms which to count)
- Makeup hours credited at original session duration, not makeup session duration (if different)

---

## 37. Batch Transfer — Attendance Migration

- Student moves from Batch A (e.g., Morning JEE Maths 7–9 AM) to Batch B (Evening JEE Maths 6–8 PM)
- Migration process:
  - Admin initiates transfer with effective date
  - Historical attendance from Batch A preserved and migrated to Batch B record
  - Sessions attended in Batch A + sessions attended in Batch B = cumulative total
  - Effective from transfer date: new sessions in Batch B; old sessions from Batch A archived
- No attendance loss; student does not restart from zero
- Transfer logged in audit trail

---

## 38. Batch Merge — Attendance Consolidation

- Two low-strength batches merged into one combined batch
- Per-student attendance history from both source batches preserved under merged batch
- Total sessions recalculated: combined unique sessions (deduplication if batches had same sessions on same dates)
- Historical batch identifiers preserved in audit log
- Students of both merged batches notified in-app of new combined schedule

---

## 39. Batch Split — Attendance Preservation

- One large batch split into two smaller batches
- Each student's historical attendance migrated to their assigned new batch
- New batch start date = split date; pre-split attendance carried forward
- Post-split: each new batch has independent attendance tracking
- Students assigned to new batches notified in-app; new schedule communicated

---

## 40. Batch Pause / Suspension

- Batch suspended for a defined period (teacher on extended leave, exam season where school-going students unavailable, centre renovation)
- Suspended period: sessions not scheduled; not counted in total session denominator
- Students not penalized for suspension period
- Suspension declared by center admin with reason and duration
- Students notified in-app; resume date communicated when known

---

## 41. Batch Close / Completion

- At end of batch duration (all planned sessions conducted):
  - Students who met minimum attendance/hours threshold: eligible for completion certificate (Module 39)
  - Students who did not: ineligible — shown in report with shortfall
- Batch closed in system; status changes to "Completed"
- Records archived but accessible (read-only) for 3 years (coaching centre retention policy)
- Center director receives batch completion summary: enrolled count, completed count, dropout count, average attendance %

---

## 42. Retake Batch — New Attendance Cycle

- Student who failed attendance threshold or did not qualify the course:
  - Re-enrolled in next batch cycle (new batch of same course)
  - New attendance cycle starts fresh from zero
  - Previous batch record archived with status "Incomplete / Retake"
  - Previous record accessible for reference; not added to new batch calculations
- Retake enrollment fee policy per centre (full fee / discounted retake fee)

---

## 43. Re-enrollment Offer After Low Attendance

- Center admin generates re-enrollment offer for students below attendance threshold
- Offer sent in-app: "You have not met the minimum attendance for [Batch Name]. Would you like to re-enroll in the next batch?"
- Student / parent accepts or declines
- Accepted: new enrollment created; fee invoice raised (Module 25)
- Declined: marked as Formal Dropout (Point 98)
- Offer tracked; accepted/declined rate reported to center director

---

## 44. Attendance-Based Batch Level Promotion

- Multi-level programs: Foundation → Advanced → Expert; UPSC Prelims → Mains → Interview
- Promotion eligibility check runs at end of each batch cycle:
  - Criterion 1: Attendance ≥ minimum threshold (configurable per level)
  - Criterion 2: Test score ≥ promotion score (from Module 22)
  - Both criteria must be met; system checks both automatically
- Students meeting both: promotion offer generated
- Students failing either: re-enroll at current level or conditional promotion (center director override with reason)

---

## 45. Post-Exam Batch Continuation Tracking

- After JEE/NEET/UPSC/CA result declaration:
  - Students who qualified: marked "Qualified Dropout" — positive dropout reason; batch attendance record closed with "Course Objective Achieved" status
  - Students who want to retake: continue in batch; attendance tracking resumes normally
  - Students who give up (no result, no retake): Formal Dropout (Point 98)
- Qualified dropout does NOT count as absence; does not affect batch average attendance statistics
- Qualification record linked to student profile (Module 07 achievements)

---

## 46. Waiting List Promotion from Chronic Absentee

- Student with [configurable threshold, default: 7+] consecutive sessions absent, no response to 3 contact attempts:
  - Center admin initiates seat release workflow
  - Seat release requires center director approval
  - Waitlisted student (from Module 31 Admission CRM) notified of seat availability
  - Absent student formally notified: "Your seat has been released due to non-attendance. Please contact centre to re-enroll."
- Seat transfer logged; original enrollment record closed with reason "Seat Released — Non-Attendance"

---

## 47. Parent Notification Rules

- **Students below 18:** in-app absent notification same timing as Module 11 (within 30 minutes of session start)
  - Notification: "Your child [Name] did not attend [Batch Name] session today"
  - No notification if leave is pre-approved (authorized absent)
- **Students 18 and above:** no parent notification; direct in-app notification to student only
  - Unless student has explicitly opted in for parent sharing in their privacy settings (Module 09 P-level rules)
- Coaching centres cannot force parent notification for adult students (DPDPA 2023 compliance)

---

## 48. Consecutive Absence Alert

| Consecutive Sessions Absent | Action |
|---|---|
| 3 sessions | Alert to center admin; in-app to student (18+) or parent (<18) |
| 5 sessions, no response | Dropout risk flag; counsellor assigned (Module 32) |
| 7 sessions, no response | Management review; seat release workflow option (Point 46) |
| 10+ sessions | Formal dropout process initiated |

- Consecutive count resets on any attendance (Present / Late / Authorized / Medical)
- Alerts logged in student record with follow-up action required field

---

## 49. Low Attendance In-App Alert

| Attendance % | Alert |
|---|---|
| 80–89% | Advisory: "Your attendance is at [%]. Please attend regularly." |
| 75–79% | Warning to student + parent (<18): "Attendance below 80%. Eligibility at risk." |
| 70–74% | Shortage alert: "You may not qualify for certificate/test. Contact centre admin." |
| < threshold | Eligibility blocked in-app: "Attendance insufficient for certificate. Apply for condonation." |

---

## 50. Center Director Daily Summary

Auto-generated at end of each day:
- Total sessions conducted today (per batch)
- Per-batch: enrolled count, present count, absent count, average % today
- Batches with < 60% average today: highlighted in red
- New consecutive absence flags: students hitting 3/5/7 session absence thresholds
- Cancelled sessions today with teacher name and reason
- Sent as in-app notification to center director and branch manager

---

## 51. Certificate Eligibility Check

- Before batch completion certificate issued (Module 39):
  - System checks: attendance % ≥ minimum AND total hours ≥ minimum (if hours-based)
  - Eligible: certificate generation unlocked
  - Ineligible: certificate blocked with message: "Attendance: [%] / Required: [%]. Shortfall: [N] sessions / [H] hours."
- Condonation (Points 53–55) can lift the block
- Certificate generated only after eligibility confirmed; logged with approval timestamp

---

## 52. Attendance Shortage Warning — Remaining Sessions Counter

Real-time counter shown on student dashboard:
- "You have attended [X] sessions / [Y] hours"
- "Minimum required: [Z] sessions / [W] hours"
- "You need [N] more sessions to qualify" (if still achievable)
- "Not achievable — remaining sessions are [R]; maximum reachable: [%]" (if impossible without condonation)
- Updated after every session; motivates student attendance in final weeks

---

## 53. Medical Condonation

```
Student / Parent submits condonation application (in-app)
  → Uploads medical certificate (doctor name, reg. no., dates)
  → Center admin reviews certificate authenticity
  → HOD / Center Director approves
  → Condonation recorded; effective attendance recalculated
  → Student notified: "Condonation approved. Updated attendance: [%]"
```

- Condonable percentage: configurable per batch (default: up to 10% of total sessions)
- PMKVY/NSDC batches: NSDC allows up to 10% medical condonation
- Coaching regulation states: condonation limit per state law applied

---

## 54. Exam Day Condonation

- Automatic: if student's exam date (JEE/NEET/Board/CA/UPSC) is registered in their profile (Module 07) and matches a coaching session date: session auto-condoned
- No application needed; no approval needed
- Manual: teacher / admin marks "Exam Day" with exam name for unlisted exams
- Exam day condonation does not count against medical condonation limit

---

## 55. Calamity / Force Majeure Condonation

- Center closed due to flood, cyclone, epidemic, riot, or government order:
  - Admin marks period as "Calamity Closure" with reference
  - All students: sessions on those days not counted in denominator
  - No application needed; automatic
- Individual student affected by local calamity (road block, area flooding): admin marks specific student with calamity exemption for those days with Principal approval

---

## 56. Refund Eligibility Based on Attendance

- When student discontinues mid-course:
  - Refund calculation = total fee − (sessions attended × per-session cost)
  - Attendance record is the legal basis for refund amount
  - Per-session cost = total batch fee / total planned sessions
  - Disputes: attendance audit log with timestamps is evidence
- Refund policy configured per institution (may include non-refundable registration portion)
- Linked to Module 25 Fee Collection; refund transaction initiated from attendance-based calculation

---

## 57. Fee Discount / Cashback for High Attendance

- Optional incentive: students with ≥ 90% (or configurable threshold) attendance in a batch receive fee discount or cashback at batch end
- System auto-identifies eligible students at batch completion
- Discount / cashback triggered in Module 25 Fee Collection
- Notification to student: "Congratulations! Your [%] attendance has earned you a [₹amount] fee discount."
- Purpose: motivate regularity; reduce absenteeism; reward high-performing students

---

## 58. Fee Defaulter Attendance Access Lock

- Student with overdue coaching fee: their attendance access restricted:
  - App: locked from joining online sessions, viewing timetable
  - Physical: entry kiosk/biometric may trigger admin alert on centre entry attempt
- Per Module 04 fee-due app lock rules
- Lock lifted immediately on fee payment (Module 25 payment confirmation)
- Teacher still marks attendance even for locked students (if they physically attend); lock is a soft access control, not a physical ban

---

## 59. Pay-Per-Class Billing Model

- Small coaching centres charging per class attended (not fixed monthly fee)
- Attendance record = billing input
- Month-end process: system counts attended sessions per student → generates invoice at (sessions × per-class rate)
- Invoice sent to student/parent via in-app; payment collected via Module 25
- Disputed attendance: student can raise query within 7 days; resolved via attendance log audit trail
- Absence = no charge for that session (student knows they lose the session but save the fee)

---

## 60. PMKVY / DDU-GKY Government Skill Batch Attendance

- Pradhan Mantri Kaushal Vikas Yojana (PMKVY) and Deen Dayal Upadhyaya Grameen Kaushalya Yojana (DDU-GKY):
  - Minimum 80% of total session hours required for assessment eligibility (NSDC mandate)
  - Attendance marked daily; biometric mandatory for NSDC-registered centres
  - NSDC requires Aadhaar-linked student IDs for attendance records
  - Batch strength, session hours, and individual attendance fed into NSDC portal report
- Assessment eligibility check: system blocks assessment registration if hours < NSDC minimum
- Government funding tranche release linked to attendance compliance reports

---

## 61. NSDC Portal Attendance Export

- PMKVY/DDU-GKY centres submit attendance data to NSDC Skills portal periodically
- System generates NSDC-compatible export:
  - Batch ID, TP (Training Partner) code, TC (Training Centre) code
  - Student Aadhaar number (or enrollment ID), name, course ID
  - Session-wise attendance (date, hours attended, biometric confirmation)
- Export format: NSDC-prescribed CSV / Excel
- Submitted by centre admin via NSDC portal upload or API push (future)
- Submission logged with date, submitted by, portal acknowledgement reference

---

## 62. Rajasthan Coaching Regulation Act 2023 Compliance

- Registered coaching institutes in Rajasthan must:
  - Maintain detailed daily attendance records per batch
  - Submit monthly attendance reports to state authority
  - Maintain student-wise cumulative attendance for the course duration
  - Allow state inspectors to access attendance records on demand
- System generates Rajasthan-prescribed compliance reports:
  - Batch-wise daily attendance register (session-by-session)
  - Student-wise monthly attendance summary
  - Cumulative course attendance report
- Exported as PDF; submitted physically or via state portal (as mandated)
- Inspection readiness: instant printable reports via one-click export (Point 85)

---

## 63. Other State Coaching Regulations

- States progressively enacting coaching regulation laws (Chhattisgarh, MP, UP, Uttarakhand, Maharashtra under consideration):
  - Institution admin selects applicable state regulation at onboarding
  - System loads state-specific compliance report format
  - Alert when regulation requirements change (EduForge platform update)
- Common requirements across states: attendance records, grievance register, fee transparency, batch strength limits

---

## 64. Batch Strength Monitoring — Fire Safety Capacity

- Coaching regulation and fire safety norms (NBC 2016: National Building Code) limit maximum occupancy per room
- Room capacity configured in Module 06 Branch & Campus Management
- Actual session attendance vs room capacity tracked:
  - If actual attendees > room capacity: fire safety violation alert to center admin and branch manager
- Batch enrollment cap set equal to room capacity; admin warned if enrollment approaches cap
- Compliance report: maximum single-session occupancy per batch per month for fire safety audit

---

## 65. Student Leave Application

- Student / parent submits leave request via app before absence:
  - Date(s), reason, type (medical / personal / exam / other)
  - Batch teacher / center admin approves or rejects
  - Approved: marked Authorized Absent in advance
  - Rejected: if student absent = Unauthorized Absent
- Retroactive leave: student was absent; parent applies within 2 working days of return; teacher approves; converts to Authorized Absent
- Beyond 2 working days: retroactive leave not accepted except with medical certificate (teacher + admin jointly approve)

---

## 66. Attendance Percentage Calculation

```
Attendance % = (Sessions Attended / Total Sessions Conducted) × 100
```

- Denominator = sessions actually conducted (excludes cancelled sessions, batch holidays, calamity days)
- Numerator = sessions marked Present + Late (if late counts as present) + Makeup Present + Medical condoned + Exam Day condoned
- Makeup sessions included in numerator only; not added to denominator
- Partial sessions (late/early exit): contribute partial credit to numerator based on hours fraction
- Recalculated in real-time after every session marking or condonation update

---

## 67. Scholarship Batch Attendance Compliance

- Students on merit / need-based scholarship from coaching centre required to maintain minimum attendance (e.g., 85% for scholarship batch)
- 30 days before scholarship renewal date: system alerts admin of students below threshold
- Scholarship batch attendance certificate generated for eligible students
- Non-eligible: scholarship review triggered; center director + scholarship committee notified
- Scholarship continuation or discontinuation logged in student financial record (Module 24)

---

## 68. Government Free Coaching Scheme Attendance

- State government free coaching programs:

| Scheme | State | Eligibility | Attendance Requirement |
|---|---|---|---|
| Free UPSC Coaching | Rajasthan | SC/ST/OBC students | 75% minimum |
| Rajiv Gandhi Free Coaching | Karnataka | SC/ST students | 75% minimum |
| Dr. Ambedkar Free Coaching | Delhi | SC/ST/OBC/Minority | 80% minimum |
| Free Coaching Scheme | Chandigarh | SC/ST/OBC/Minority/EWS | 80% minimum |
| Maulana Azad Scheme | Centre/States | Minority students | 75% minimum |

- System tracks these students separately (scholarship category flag)
- Monthly attendance compliance report generated for scheme authority
- Students below threshold: scheme coordinator alerted; student given improvement window
- Non-compliant students: scheme enrollment discontinued after due notice

---

## 69. Mental Health / Counselling Session Tracking

- Rajasthan Coaching Regulation Act 2023 and NHRC guidelines (post-Kota suicide prevention measures) mandate:
  - Weekly mental health check-in sessions for residential coaching students
  - Access to counsellor for all enrolled students
- Counselling session attendance tracked in aggregate for compliance reporting:
  - Total sessions conducted per month
  - Total unique students who attended (count only — not student names in public reports)
- Detailed counsellor records maintained with student names under restricted access (Module 32 confidentiality)
- Compliance report: monthly aggregate submitted to state authority showing mental health support sessions conducted

---

## 70. Mandatory Recreation / Sports Time Attendance

- Rajasthan Coaching Regulation Act 2023 mandates minimum 1-hour recreation/sports time per day for students in residential coaching centres
- Recreation session attendance tracked separately:
  - Session type: "Recreation / Sports"
  - Attendance marked by PE teacher or hostel supervisor
  - Minimum 6 hours/week required for compliance (1 hr/day × 6 working days)
- Monthly compliance report: total recreation hours per student
- Non-compliance flagged to center director; state authority compliance report includes recreation hours data

---

## 71. Hostel Mess Biometric Cross-Reference

- Large residential coaching centers (Kota model): biometric / ID scan at mess (breakfast, lunch, dinner)
- Cross-reference logic:
  - Student present at lunch mess but marked absent from morning session → "Bunking Class" anomaly
  - Student absent from morning + afternoon sessions + dinner mess → welfare concern flag (possible unwell, left campus without notice)
- Hostel warden + center admin alerted on both anomaly types
- Wellness check triggered for welfare concern flags
- Mess attendance also used for: meal count reporting, kitchen planning, POSHAN-linked scheme compliance (if applicable)

---

## 72. Night Study Hall Attendance

- Mandatory supervised self-study period (typical: 8:00–11:00 PM) in residential coaching
- Separate attendance tracking: "Study Hall" session type
- Marked by duty teacher / hostel supervisor
- Non-attendance triggers warden alert: student not in study hall + not in room = location unknown flag
- Study hall attendance used in: student discipline report, parent communication (monthly study hall attendance for parents of < 18 students)
- Linked to Module 28 Hostel Management

---

## 73. Attendance Freeze at Batch Completion

- When batch end date approaches and final sessions complete:
  - Attendance for the batch is soft-locked automatically
  - Teacher and admin cannot modify records after lock
  - Corrections require center director approval with reason
- Locked records used for: certificate issuance, refund calculation, scholarship compliance, court/legal reference
- Soft lock applied 7 days after batch end date (gives time for any final corrections)

---

## 74. Attendance Correction — Levels

| Timing | Authority |
|---|---|
| Within 24 hours | Teacher self-correction (no approval needed) |
| 24–48 hours | Center admin approval required |
| 48 hours – 5 days | Center director approval with reason |
| Beyond 5 days | Not allowed unless batch is still open AND management approves |
| After batch lock | Center director only; reason mandatory; audit flagged |

- All corrections logged: original value, corrected value, corrected by, approved by, reason, timestamp
- Correction audit report available for inspection

---

## 75. DPDPA 2023 Consent for Attendance Data

- Student / parent consented to attendance data use (Module 09 DPDPA framework) for:
  - Parent notifications
  - Performance analytics
  - Scholarship compliance reporting
  - Government scheme reporting (NSDC, state free coaching)
- Consent flag checked before any external data sharing or analytics processing
- Students who withdraw consent: analytics processing stops; external reports anonymize their data; parent notifications stop (for 18+ students who withdraw consent)
- Consent records stored with timestamp and version of consent text

---

## 76. Attendance Notification for 18+ Students

- Students 18 and above: direct in-app notification for:
  - Attendance shortage warnings (Point 49)
  - Certificate eligibility alerts
  - Consecutive absence alerts (personal, not to parent)
- No parent notification unless student explicitly opted in (Module 09 rules)
- Student controls their own notification preferences for 18+ scenarios
- Platform never sends parent notification for adult students without their consent (DPDPA 2023)

---

## 77. Student Attendance Self-View

- Student sees their own attendance per batch in their app:
  - Session-by-session history: date, status, hours
  - Monthly summary: sessions attended / total sessions conducted, %
  - Hours tracker: completed / required
  - Certificate eligibility status: Eligible / [N sessions / H hours short]
  - Remaining sessions counter (Point 52)
- Cannot view other students' attendance (privacy — DPDPA 2023)
- Parent sees same view for < 18 students in parent app (school-age students attending coaching)

---

## 78. Teacher Substitution Effect on Attendance

- When substitute takes a batch session (Module 10 Point 44):
  - Substitute teacher logs in, opens the batch session, marks attendance
  - Session tagged: "Substituted Session — Original Teacher: [Name]; Substitute: [Name]"
  - Substitute's marking is authoritative for that session
  - If neither original nor substitute marks: session flagged "Unattended — Attendance Missing" → center admin must resolve
- Substitute session counted normally in attendance % and hours
- High frequency of substituted sessions in a batch: management alert (teacher reliability concern)

---

## 79. Rescheduled Session Tracking

- Cancelled session often rescheduled to a new date/time
- Rescheduled session record tagged: "Rescheduled — Original: [Date]; Rescheduled to: [New Date]"
- Original cancelled session marked: "Cancelled — Rescheduled to [New Date]"
- Students notified in-app of new date/time immediately on reschedule confirmation
- Rescheduled session attendance taken normally on new date
- Original cancelled session NOT counted in denominator; rescheduled session counts when conducted

---

## 80. Session Partial Cancellation

- Session starts but must end early (power failure, fire alarm, venue issue, teacher health emergency):
  - Admin / teacher marks: session start time, actual end time, reason
  - Hours conducted = actual end time − session start time
  - Students who were present before cancellation: credited for actual hours present
  - Partial session flagged in records with reason
  - If conducted duration < 50% of planned: institution config — count as cancelled (no penalty) or count as partial session (partial credit)
- Reschedule of remaining session content: linked to make-up session scheduling

---

## 81. Attendance for UPSC / CA / Banking Mock Interview Sessions

- UPSC Mains, Banking PO, MBA admissions, CA Final coaching include mock interview/group discussion sessions
- Mock interview attendance tracked as separate session type: "Mock Interview / GD Session"
- Performance feedback from interview panel linked to student profile (Module 47 AI Performance Analytics)
- Separate attendance history for interview sessions vs lecture sessions
- Mock interview attendance certificate: "Participated in [N] mock interview sessions" — useful for student portfolio

---

## 82. Attendance for Form-Filling Assistance Sessions

- Coaching centres help students fill JEE/NEET/CUET/CA Foundation/CS registration forms
- Form-filling sessions tracked as special session type
- Attendance confirms: student was guided by centre expert; centre can claim value-add service
- Students who attended form-filling sessions: early form submission support flag in profile
- Useful for: centre's service quality reporting, parental reassurance communication

---

## 83. Coaching Attendance Certificate Generation

- Student requests official coaching attendance certificate for:
  - CA Foundation / CS Foundation exam form (requires coaching attendance proof)
  - Bank educational loan application
  - Government scholarship application
  - UPSC / PSC exam documentation
  - Legal / court requirement
- Certificate includes:
  - Student name, enrollment number, course/batch name
  - Batch duration (start date to date of certificate)
  - Sessions attended / total sessions conducted, attendance %
  - Total hours attended
  - Centre name, registration number, director name, stamp, signature
- Generated by Python; downloadable PDF; logged in student documents

---

## 84. NRI / International Student Timezone-Aware Attendance

- Coaching for GMAT, GRE, SAT, IELTS, TOEFL: international / NRI students in different timezones join online
- Session scheduled and displayed in IST (master timezone) + student's local timezone
- Attendance timestamp stored in both IST and student's declared local timezone
- Join time / exit time verified against session schedule in student's local timezone
- Late entry grace period applied in local timezone (prevents penalizing for timezone confusion)
- Report: attendance history shown in IST with local timezone noted

---

## 85. Coaching Centre Inspection Readiness

- When state authority inspector, NSDC assessor, or fire safety officer visits:
  - Instant printable reports generated: batch-wise attendance register, student-wise monthly summary, cumulative course attendance
  - Rajasthan format, NSDC format, or custom state format as applicable
  - No manual compilation; export ready within 60 seconds
- Inspection log: date, inspecting authority, inspector name, documents provided, observations noted
- Any compliance gaps found during inspection: action items logged with resolution deadline

---

## 86. Attendance Discrepancy Report

- Before inspection, audit, or batch closure:
  - Digital records vs physical register (if both maintained) comparison
  - Discrepancies listed: date, batch, student, digital status, physical register status
  - Admin reconciles discrepancies with center director approval; reason documented
- Periodic self-audit: center admin runs discrepancy report monthly
- Large unexplained discrepancies flagged for investigation

---

## 87. Attendance Audit Log

- Every attendance action logged:
  - Initial marking: who marked, method (app/biometric/QR/kiosk), timestamp
  - Corrections: original, corrected, who corrected, who approved, reason
  - Condonations: type, days condoned, approved by, timestamp
  - Cancellations: session cancelled by, reason, timestamp
  - Makeups: original session, makeup session, confirming teacher
- Audit log is immutable (append-only); cannot be deleted
- Center director and management can search/filter audit log by date range, student, batch, teacher

---

## 88. Dropout Formal Marking

- When student officially stops attending (written withdrawal, family contact, no-response to extended outreach):
  - Admin marks as "Formal Dropout" with date and reason:
    - Qualified for exam (positive dropout)
    - Financial difficulty
    - Health reasons
    - Relocation
    - Joined another coaching centre
    - Family reasons
    - No reason given
  - Attendance record frozen with last active date; reason logged
  - Excluded from ongoing batch statistics (not counted as absent in remaining sessions)
  - Refund calculation triggered if eligible (Point 56)
  - Module 25 fee outstanding settled or waived per centre policy

---

## 89. Batch Fill Rate Tracking

- Per batch: enrolled students vs students actually attending regularly (≥ 3 sessions/week pattern)
- Fill rate = regularly attending / enrolled × 100
- Fill rate < 60% for 2+ consecutive weeks: management alert (batch viability concern)
- Fill rate drop detection: sudden drop of > 20% in a week → management alert (possible teacher issue, schedule conflict, external exam season)
- Used for: batch viability review, teacher assignment decisions, batch merger consideration (Point 38)

---

## 90. Dropout Predictor — AI-Assisted Flag

Three-week declining trend in a student:
- Attendance dropping week-on-week (> 2 consecutive weeks declining)
- Test score declining (from Module 22)
- Doubt session participation = zero

Trigger: high-risk dropout flag in-app to:
- Center admin
- Counsellor (Module 32) — assigned for follow-up

Follow-up workflow:
- Counsellor contacts student/parent
- Outcome logged: student retained / enrolled in different batch / dropout confirmed
- Intervention history stored; used to improve centre's retention strategies

---

## 91. Attendance vs Test Performance Correlation

- Per student per batch: attendance % vs average mock test score trend plotted
- Patterns identified:
  - High attendance + high scores: healthy student
  - High attendance + low scores: teaching quality / student comprehension issue → counsellor + teacher flag
  - Low attendance + high scores: student self-studying; attendance intervention needed
  - Low attendance + low scores: highest dropout risk; immediate intervention
- Correlation analysis feeds Module 47 AI Performance Analytics
- Batch-level correlation: if 40%+ of batch shows low attendance + low scores → batch-level pedagogical review triggered

---

## 92. Seasonal Dip Mapping

- Coaching centres see predictable seasonal attendance dips:
  - Post-Diwali / Holi (2–3 days)
  - Pre-board exam period for school-going students (Oct–Nov, Feb–Mar)
  - Post-JEE/NEET result anxiety period
  - Summer (April–May) in non-residential centres
  - Navratri in Gujarat/Rajasthan; Durga Puja in Bengal/Odisha; Onam in Kerala
- System maps seasonal dips per batch per year
- Historical 2-year comparison: is this year's dip worse or better than last year?
- Center uses data: avoid scheduling important topics on historically high-absence dates, plan extra sessions to compensate

---

## 93. Session Feedback Cross-Confirmation

- After each session, students optionally rate the session (1–5 stars + comment)
- Feedback submission cross-references with attendance:
  - Student who submits feedback = additional confirmation they were present
  - Student marked present but submits feedback saying "I wasn't there" = anomaly flag
- Teacher receives session feedback summary after 24 hours
- Poor rating (< 3 stars) from > 30% of students: center director alerted (teaching quality flag)
- Feedback data feeds teacher appraisal (Module 08 Point 95)

---

## 94. Batch Health Score

Composite score per batch shown on center director dashboard:

| Metric | Weight |
|---|---|
| Average student attendance % | 40% |
| Average test score (from Module 22) | 30% |
| Dropout rate (month) | 20% |
| Teacher session cancellation rate | 10% |

- Score 80–100: Healthy (green)
- Score 60–79: Watch (yellow)
- Score < 60: Critical (red — immediate management review)
- Trend: week-on-week health score movement shown

---

## 95. Multi-Branch Centralized Attendance — Large Coaching Chains

- Large chains (ALLEN, Aakash, Resonance: multi-city, 50+ branches):
  - Student's attendance visible at central admin/national level
  - Branch transfer: attendance history migrated to new branch (Point 37 extended to cross-branch)
  - National performance model (for rank prediction) uses attendance data across all branches
  - Central compliance report: all branches' attendance aggregated for NSDC, state authority, or franchisor review
- Branch-level admin sees only their branch; national admin sees all branches
- DPDPA consent covers multi-branch data processing within the same tenant group

---

## 96. Attendance Before / After Batch Dates — Guard

- System prevents marking attendance for dates before batch official start date
- System prevents marking for dates after batch official end date
- If batch end date is extended (batch running longer than planned): admin updates end date with center director approval
- Guards prevent data entry errors; particularly important during batch transfers and merges

---

## 97. Attendance Data Export for Centre Records

- Center admin can export at any time:
  - Batch-wise attendance CSV: all students, all sessions, all statuses
  - Student-wise PDF attendance report for any date range: single student, all batches
  - Monthly attendance summary: all batches in one PDF
- Exports used for: centre's own records, parent formal requests, court/legal requirements, bank loan documentation
- Export logged: who exported, what, when (audit trail for data governance)

---

## 98. Parent Orientation Session Attendance

- Coaching centre conducts parent orientation for school-age students (beginning of batch):
  - Session covers: course plan, attendance expectations, test schedule, fee payment schedule, how to track child's progress
  - Parent attendance tracked (confirms parental engagement and awareness)
  - Parent present: reduces future disputes about fees, attendance rules, exam schedules
- Parent attendance linked to student record
- Centres with low parent orientation attendance: admin follows up with parents who missed; reschedule offered
- Parent orientation attendance used in: dropout risk profiling (parents who never attended orientation show higher child dropout correlation)

---

## DB Schema (Core Tables)

```
coaching.batch_sessions
  id, tenant_id, batch_id, session_date, session_start, session_end,
  session_type (regular/doubt/extra/revision/test_series/workshop/
  group_study/trial/mock_interview/form_filling/recreation/study_hall/
  parent_orientation/orientation),
  status (scheduled/conducted/cancelled/cancelled_rescheduled/partial),
  conducted_by_teacher_id, substitute_teacher_id,
  actual_end_time (for partial cancellation), cancelled_reason,
  rescheduled_to_session_id, created_at

coaching.batch_attendance
  id, batch_session_id, student_id,
  status (present/absent/late/authorized_absent/medical_absent/
  exam_day/makeup_present/recorded_watch/partial_present/
  formal_dropout/qualified_dropout/cancelled_session/batch_holiday),
  marked_by (teacher_id), marked_at, marking_method
  (app/biometric/rfid/kiosk/qr_code/bulk_import/offline_sync/manual),
  hours_present (decimal, for partial), is_makeup (bool),
  makeup_from_batch_id, makeup_from_session_id,
  correction_count, last_corrected_by, last_corrected_at

coaching.batch_attendance_corrections
  id, batch_attendance_id, original_status, corrected_status,
  corrected_by, correction_reason, approved_by, approved_at,
  correction_level (self/admin/director/management), created_at

coaching.batch_condonations
  id, tenant_id, student_id, batch_id,
  condonation_type (medical/exam_day/calamity/scholarship),
  sessions_condoned, hours_condoned, evidence_document_id,
  applied_by, approved_by, status (pending/approved/rejected),
  created_at

coaching.recorded_watch_log
  id, tenant_id, student_id, batch_id, recording_id,
  watch_start, watch_end, total_watch_duration_minutes,
  video_total_duration_minutes, watch_percentage,
  credit_awarded (bool), created_at

coaching.makeup_sessions
  id, tenant_id, original_batch_id, original_session_id,
  makeup_batch_id, makeup_session_id, student_id,
  confirmed_by_makeup_teacher_id, created_at

coaching.dropout_log
  id, tenant_id, student_id, batch_id, dropout_type
  (formal/qualified/seat_released/non_response),
  dropout_date, reason, last_attended_session_id,
  logged_by, logged_at, re_enrollment_offer_sent (bool),
  re_enrollment_status (none/offered/accepted/declined)

coaching.batch_health_scores
  id, tenant_id, batch_id, score_date, avg_attendance_pct,
  avg_test_score, dropout_rate_pct, cancellation_rate_pct,
  composite_health_score, trend (improving/stable/declining)

coaching.govt_compliance_log
  id, tenant_id, branch_id, scheme_type
  (pmkvy/ddu_gky/nsdc/rajasthan_reg/state_free_coaching/other),
  period_month, period_year, submitted_by, submitted_at,
  portal_reference, file_path

coaching.biometric_entry_log
  id, tenant_id, branch_id, student_id, entry_type (gate/mess/study_hall),
  log_timestamp, device_id, method (fingerprint/rfid/face/qr_id_card)
```

---

## Integration Map

| Module | How |
|---|---|
| 07 — Student Enrolment | Student roster, batch enrollment, exam registrations (exam day auto-condonation), biometric enrollment |
| 08 — Staff Management | Teacher batch attendance, substitution, teacher appraisal input |
| 09 — Parent & Guardian | Parent notification rules (18+ no parent notification), DPDPA consent, parent access levels |
| 10 — Timetable & Scheduling | Batch session schedule; demo class slots; batch timetable |
| 22 — Test Series & Mock Tests | Test session attendance; attendance vs performance correlation |
| 24 — Fee Structure | Scholarship attendance compliance; fee concession trigger |
| 25 — Fee Collection | Pay-per-class billing; refund calculation; fee defaulter lock |
| 28 — Hostel Management | Residential coaching: mess biometric cross-reference, study hall, recreation |
| 29 — Transport | Students commuting to coaching; field trip attendance |
| 31 — Admission CRM | Trial/demo class conversion tracking; waitlist promotion |
| 32 — Counselling | Dropout risk referral; mental health session tracking; re-integration |
| 35 — Notifications | Absent alerts, shortage warnings, session cancellation notices |
| 39 — Certificates | Batch completion certificate eligibility; coaching attendance certificate |
| 40 — Document Management | Attendance certificates, condonation records, govt compliance reports |
| 45 — Live Classes | Online session join/duration data for attendance credit |
| 47 — AI Performance Analytics | Attendance vs test score correlation; dropout predictor |
