# Module 23 — Leaderboard & Rankings

## 1. Purpose
Provide a multi-scope, multi-period, privacy-first leaderboard and ranking engine for all
institution types on EduForge — schools, coaching institutes, colleges, and skill centres.
Rank students across academic performance, attendance, assignments, test series, and engagement;
support house competitions, inter-class and inter-institution challenges; enforce DPDPA 2023
consent and RPWD Act ethical guardrails; surface actionable analytics for teachers, HODs,
principals, and academic directors; and motivate through gamification without causing rank
anxiety or unfair socioeconomic comparisons.

---

## 2. Leaderboard Types

| Leaderboard | Data Source | Audience |
|---|---|---|
| Academic Performance | Module 21 result ledger | Student, Parent, Teacher, Admin |
| Test Series Rank | Module 22 test attempts | Student, Teacher, Coaching Director |
| Subject-wise | Module 21 per-subject marks | Student, Subject Teacher |
| Attendance | Module 11/12/13 attendance | Student, Class Teacher |
| Assignment / Homework | Module 14 submission rate + marks | Student, Class Teacher |
| Overall Merit (Composite) | Weighted: Exam + Attendance + Assignment + Co-curricular | Principal, Academic Director |
| Improvement | Gain over previous period (not absolute marks) | All — primary default for <Class 9 |
| Streak / Engagement | Module 22 DPT streak + XP | Student |
| XP Points | Module 22 XP log | Student, Batch |
| House Competition | House points from all modules | Institution, Parents (kiosk) |
| Library Reading | Module 30 books issued/returned | School (Classes 1–8) |
| Hostel Conduct | Module 28 warden ratings | Hostel Warden, Principal |
| Group / Study Team | Study group average score | Student (group members) |
| Parent Engagement | PTM attendance + app activity | Institution Admin (private) |
| Fee Punctuality | Module 24/25 on-time payments | Institution Admin (private) |

---

## 3. Scope Levels

### 3.1 Student-Facing Scopes
| Scope | Description |
|---|---|
| Section | Within one class section (10-A only) |
| Class / Grade | All sections of a grade (10-A + 10-B + 10-C) |
| Stream | Science / Commerce / Arts (Class 11–12) |
| Programme | B.Tech CSE / B.Com / MBA — within one programme (college) |
| Department | All programmes under a department (college) |
| Batch | Within a coaching batch |
| Branch / Campus | All classes in one branch |
| Institution | All branches of the institution |
| State | All EduForge institutions in a state — institution opt-in |
| National (All-India) | Platform-wide — institution + student consent (DPDPA 2023) |

### 3.2 Scope Visibility Cap
- Institution configures maximum scope visible to students (e.g., class-only for primary school;
  institution-wide for coaching).
- State/National scope: requires explicit opt-in from both institution admin and each student
  (or parent for under-18).
- Teacher/Admin always see full scope regardless of student-facing cap.

---

## 4. Time Periods

| Period | Reset / Refresh |
|---|---|
| Daily | Every 24 hours; for DPT streak + engagement boards |
| Weekly | Resets Monday 00:00 |
| Monthly | Resets 1st of each month |
| Term | Term 1 / Term 2 (school); configurable term dates |
| Semester | Per UGC/university semester (college) |
| Phase | Coaching phase: Phase 1 (Jul–Sep) / Phase 2 (Oct–Dec) / Phase 3 (Jan–Mar); configurable |
| Annual | Full academic year; final rank locked after Module 21 result verification |
| Test-Specific | Live during test window; archived after window closes |
| Rolling 30-day | Smooth rolling window; no hard reset; always shows last 30 days |
| All-Time | Since student joined institution; for alumni honour board |
| Season | Academic year divided into 3 seasons; each has fresh start (prevents uncatchable leaders) |

---

## 5. Rank Computation Engine

### 5.1 Composite Score Formula
```
composite_score =
  (exam_component    × w_exam)    +
  (attendance_%      × w_att)     +
  (assignment_score  × w_assign)  +
  (cocurricular_pts  × w_cocurr)

Default weights (institution-configurable):
  w_exam    = 60%
  w_att     = 20%
  w_assign  = 15%
  w_cocurr  = 5%
  Total     = 100%
```

### 5.2 Normalization
- Raw marks normalized to 100 per subject before aggregation; prevents subjects with higher
  max marks dominating the composite.
- Formula: `normalized = (marks_obtained / marks_max) × 100`
- Applied per exam component; then averaged across subjects for the exam component score.

### 5.3 Weighted Recency
- Recent exams weighted higher than older ones using exponential decay factor (configurable).
- Prevents stale good performance from masking current decline.
- Default: last exam weight = 1.0; previous = 0.85; two before = 0.72; and so on.
- Institution can disable recency weighting (flat average) in Academic Settings.

### 5.4 Tie-Breaking
1. Highest marks in English / first language.
2. Highest marks in Mathematics / core subject.
3. Highest marks in remaining subjects (sequential).
4. If still tied: joint rank assigned (e.g., two students at Rank 3; next is Rank 5).
- Tie-break subject priority configurable per institution.

### 5.5 Exclusion Rules
- CWSN exempted subjects excluded from academic component (same exclusion as Module 21).
- Medical leave days excluded from attendance component denominator.
- Pre-board exam marks excluded (pre-board is analytics-only per Module 21 rule).
- Detained/Fail students excluded from public leaderboard automatically.

### 5.6 Rank Refresh Cycle
- Provisional rank: recomputed within 1 minute of any new score entering system; labelled
  "PROVISIONAL" until result verification completes (Module 21).
- Final rank: locked after Module 21 verification workflow completion; immutable thereafter;
  "FINAL" badge on leaderboard.

### 5.7 Rank Audit Log
- Every rank computation stored: component_inputs (JSONB), formula_string, output_rank,
  computed_at, snapshot_id — immutable; RTI-defensible.
- Anomaly flag: if any component score jumps >30 points in one cycle → flag to HOD for review
  before rank update published.

---

## 6. Privacy & Consent (DPDPA 2023)

### 6.1 Default — Opt-In
- Student's rank not shown to peers without explicit consent (DPDPA 2023 §7).
- Default state: anonymous mode (name replaced with "Student #[rank]").
- Opt-in: student (if 18+) or parent (if under 18) explicitly enables full-name visibility.

### 6.2 Parent Consent for Under-18
- Parental consent for leaderboard visibility collected during admission (Module 09 consent flow).
- Includes: leaderboard name visibility, photo on leaderboard, kiosk display consent, WhatsApp
  digest consent — each as separate consent checkbox.
- Parent can revoke any consent at any time from parent dashboard; takes effect within 1 hour.

### 6.3 Visibility Modes
| Mode | Peer Sees | Teacher/Admin Sees |
|---|---|---|
| Anonymous (default) | "Student #[rank]" + avatar | Full name + rank |
| Full Visible | Name + photo (if consented) + rank | Full name + rank |
| Hidden | Not shown on leaderboard at all | Internal rank computed; visible to staff |

### 6.4 Data Minimisation
- Leaderboard API response to peers: rank, score band (Top 10% / Top 25% etc.), delta,
  badge — never full marks breakdown.
- Full marks accessible only to self, class teacher, HOD, Principal, Academic Director.

### 6.5 Opt-Out
- Single tap from student dashboard → "Remove me from public leaderboard."
- No explanation required; no admin approval needed.
- Rank continues computed internally for teacher/admin; excluded from peer-visible display.

### 6.6 Photo on Leaderboard
- Student/parent photo consent: separate from leaderboard visibility consent.
- If photo not consented: avatar (auto-generated initials, no face) shown instead.
- Kiosk/smart TV display: photo shown only if both leaderboard + photo consent active.

### 6.7 Minimum Age Rules
- Default: no public rank display for students below Class 3 (approximately age 8–9).
- Configurable: institution can raise threshold; cannot lower below Class 1.
- Academic Director override: with documented justification — enables for younger grades.

---

## 7. Display & UI

### 7.1 Podium View
- Ranks 1–3: gold / silver / bronze podium card with profile photo (or avatar) and name.
- Animated entrance on first load (subtle — not distracting).
- Score shown as percentage band: "Top 2%" rather than raw score (peer view).
- Full score shown to self + staff.

### 7.2 My Rank Card (Always Pinned)
- Pinned at bottom of screen regardless of position.
- Shows: rank, score, rank delta (↑ / ↓ / — unchanged), period label.
- Tapping opens full personal analytics (Module 22/21 integration).

### 7.3 Nearest Neighbours
- 3 ranks above + 3 ranks below student shown; creates motivational "chase" and "defend" context.
- Names shown per privacy mode (full / anonymous / avatar).

### 7.4 Rank Movement Indicators
- ↑12: green up-arrow; rose 12 positions.
- ↓5: red down-arrow; fell 5 positions.
- NEW: first appearance on leaderboard.
- —: no change.

### 7.5 Badge Icons on Leaderboard
| Badge | Source |
|---|---|
| XP Level (Bronze/Silver/Gold/Platinum/Diamond) | Module 22 XP engine |
| Subject Topper Crown | Highest marks in a subject this period |
| Attendance Star | 100% attendance this month |
| Streak Flame | Consecutive weeks in top 10 (with count) |
| Most Improved | Highest rank gain this period |
| Teacher's Pick | Awarded by class teacher |
| Subject Expert | >90% accuracy in same subject, 3 consecutive tests |
| Century Club | 100 DPTs completed |
| Comeback | Jumped from bottom 50% to top 20% |

### 7.6 Filters
- Student filters: time period, subject (for subject leaderboard), scope level.
- Teacher/Admin filters: time period, subject, class, section, category (SC/ST/OBC/General),
  gender, CWSN status, student name search.

### 7.7 Pagination & Search
- 20 students per page; student's own card always pinned.
- Teacher/Admin: search any student by name → jumps to their rank card.

### 7.8 Leaderboard Freeze
- After final rank locked: "FINAL — Academic Year 2025–26" badge; no movement.
- Historical leaderboards accessible under "Past Leaderboards" tab.

---

## 8. School-Specific Leaderboards

### 8.1 House Competition Board
- Houses: typically 4 (Red/Blue/Green/Yellow or named after national figures).
- Points earned from: academics (exam rank), sports (entered by sports teacher), cultural events
  (entered by event coordinator), NCC/NSS/Scout, attendance.
- House points table: displayed on school kiosk (smart TV mode) — auto-rotates.
- House champion: trophy awarded at annual day; shown on institution dashboard.

### 8.2 Inter-Class Competition
- Class 10-A vs 10-B vs 10-C: average composite score per section ranked.
- Class teacher sees own class standing vs peer sections.
- "Top Section" badge awarded to winning section monthly — displayed on section's virtual notice
  board.

### 8.3 Subject Olympiad Rank
- NTSE / SOF / Silverzone / Unified Council rank entered by institution admin after external
  results.
- Displayed on school leaderboard with external badge icon (distinct from internal ranks).

### 8.4 Special School Boards
- Attendance Champion: 100% attendance students highlighted monthly; "Gold Attendance" badge;
  resets each month.
- Assignment Star: highest assignment submission rate per class; weekly; "Homework Hero" badge.
- Most Improved (Term): student with highest % gain — displayed on school notice board with name
  (with consent); reduces pressure on absolute rank.
- Reading Milestone (Classes 1–5): number of chapters/notes read from Module 16; "Bookworm of
  the Month" badge; engagement-first, score-free.

### 8.5 NIPUN Bharat FLN (Classes 1–3)
- Literacy + numeracy milestone completion rate per section — for teacher/HOD monitoring only.
- Not shown to students (developmental appropriateness); helps teacher identify students needing
  FLN intervention before Class 4.

---

## 9. Coaching-Specific Leaderboards

### 9.1 NTA Percentile Board
- Students ranked by NTA percentile (not raw marks) — realistic competitive picture for
  JEE/NEET coaching.
- Shown alongside raw score; percentile = primary rank metric for coaching context.

### 9.2 Category-Adjusted Rank
- Student sees: Overall Rank + Category Rank (OBC/SC/ST/EWS).
- Category rank: "Among OBC candidates in this batch — your rank is 3."
- Helps students assess realistic college probability with reservation benefit.

### 9.3 Target College Board
- Students who set same target college + branch (e.g., IIT Bombay CSE) grouped.
- Board shows: "Among 18 students targeting IIT Bombay CSE in this batch — your rank."
- Updates after each test; drives specific competitive motivation.

### 9.4 Phase-wise Champion
- At end of each coaching phase: phase champion identified; digital badge + FCM.
- Phase leaderboard archived; cumulative leaderboard continues across phases.
- Mock Series Champion: highest average percentile across complete test series — awarded at
  series completion; rank certificate generated (Module 21 engine).

### 9.5 Subject Mastery Trio (JEE/NEET)
- Three separate rank badges per student: Physics Rank + Chemistry Rank + Maths (or Biology)
  Rank.
- Shown on student profile and leaderboard entry.
- Helps students identify which subject is their weakest link for targeted improvement.

### 9.6 Score Projection Board
- Students ranked by projected JEE/NEET score at exam date (Module 22 trajectory model).
- Labelled "PROJECTED AIR — ESTIMATED" prominently; not treated as actual rank.
- Refreshed after each test; trend shows if student is improving toward target.

### 9.7 Batch vs National
- Coaching director dashboard: batch's average percentile vs national EduForge average for
  same test series.
- Used for batch quality assessment and admission pitch to prospective students.

---

## 10. College-Specific Leaderboards

### 10.1 CGPA Board
- Semester-wise SGPA rank + cumulative CGPA rank within programme/batch.
- Backlog flag: students with active backlogs shown with a star (*) on staff view only;
  not shown on peer view (privacy).

### 10.2 Honour Roll
- Backlog-free honour roll: "Clean Slate" — zero backlogs across all completed semesters;
  highlighted on department board.
- Dean's List: top 10% CGPA per programme per semester; auto-generated after result lock.

### 10.3 Placement Readiness Board
- Composite: CGPA (50%) + internship completion (20%) + certified skill count (20%) +
  project marks (10%).
- Used by placement cell to shortlist students for company visits; not shown to students by
  default (placement cell view only).

### 10.4 Research & Project Board
- Highest project/dissertation marks per department — for research-oriented programmes.
- UG Research Honours: 4-year UG research programme (NEP 2020) — research rank displayed.

### 10.5 CO Attainment Board
- Highest Course Outcome attainment score per subject (Module 20/21 link).
- NBA/NAAC relevance: identifies top CO achievers for accreditation evidence portfolio.

### 10.6 Alumni Honour Board
- Top 10 historical rank holders per programme (all-time).
- Displayed on college app home screen: first name + graduation year + city (with consent).
- Updates when new students break into all-time top 10.

---

## 11. Inter-Institution & Platform Competitions

### 11.1 EduForge City Challenge
- Monthly: all institutions in same city appear in a common platform test series.
- Top 3 institutions ranked by average student score; city champion badge awarded to institution.
- Student scores contribute to institution average; individual ranks also computed.

### 11.2 State Champion Board
- Quarterly: state-level ranking of institutions by pass %, average CGPA, attendance rate.
- Institutions opt-in; institution name shown (not individual student names) on public state board.
- State board trophy: displayed on institution's EduForge profile page.

### 11.3 National Topper Wall
- Top 50 students by All-India Rank on platform mock series — displayed on EduForge app home
  (public section).
- Displayed: student first name + city + institution name (no surname; no photo unless opted in).
- Requires individual student consent + institution opt-in.

### 11.4 Inter-Institution Challenge
- Two institutions agree to use same Module 22 test series; combined leaderboard generated.
- Batch-level average comparison shown to institution directors.
- Individual ranks: shown to own institution's students only (cross-institution individual data
  not shared per DPDPA 2023).

### 11.5 Government School Board
- Separate leaderboard for government schools — prevents discouragement from private school
  dominance.
- Institution type tag (GOVT / AIDED / PRIVATE UNAIDED) from institution profile used.
- Government school state/national board displayed as separate tab on state/national leaderboard.

---

## 12. Special Recognition Boards

### 12.1 First-Generation Learner Board
- Students flagged as first-generation college-goers (from student profile) — separate
  recognition board.
- Removes socioeconomic comparison disadvantage; celebrates achievement in context.
- Eligible for targeted scholarship recommendation (Module 21 integration).

### 12.2 Rural Achiever Board
- Students from rural/semi-urban pin codes (from student profile address) — highlighted
  separately.
- Relevant for government rural scholarship targeting and Aspirational Districts programme
  (NITI Aayog).

### 12.3 Girl Achiever Board
- Top-performing girl students per class/batch — separate recognition.
- Aligns with BETI BACHAO BETI PADHAO, NEP 2020 gender equity mandate, Mahila Shakti Kendra.
- Notified to institution for state government girl scholarship schemes.

### 12.4 Divyang Achiever Board
- CWSN students' achievement board — completely separate from general leaderboard.
- Celebrates within-category performance; aligned with RPWD Act 2016 spirit.
- Shown to CWSN student + parents + special educator; not on general leaderboard.

### 12.5 Language Medium Achiever Board
- Hindi/regional medium students ranked separately from English medium.
- Fair comparison within medium; removes language-of-instruction bias.
- State board relevance: most state board students appear in regional medium.

### 12.6 Late Enrolment Achiever Board
- Students who joined mid-year or transferred from weaker boards — "Most Improved Since Joining"
  board.
- Rank computed from date of joining; prevents comparison disadvantage in first few months.

---

## 13. Gamification & Rewards

### 13.1 Seasons (3 per Year)
- Academic year divided into 3 seasons (Term 1 / Term 2 / Annual Final).
- Each season: fresh leaderboard start; Season Champion badge awarded.
- Prevents early leaders becoming uncatchable; everyone has a fresh chance each season.

### 13.2 Wildcard Week
- One week per month declared "Wildcard" by institution admin.
- Only improvement points count during Wildcard week (not absolute marks).
- Any student can top the leaderboard that week — drives disengaged students back.

### 13.3 Double XP Events
- Institution declares "Double XP Day" (exam day, Teacher's Day, Founder's Day, Republic Day).
- All activities earn 2× XP; drives engagement on special occasions.

### 13.4 Group / Study Team Leaderboard
- Students form study groups (3–5 members); group's average score ranked against other groups.
- Collaborative competition; all members benefit from each other's improvement.
- Group formation: invite via student ID; group leader approves/rejects join requests.

### 13.5 Teacher's Pick
- Teacher awards "Star of the Week" to any student — for effort, attitude, improvement, not
  necessarily score.
- Shown on leaderboard with special star icon; not score-based; purely discretionary.
- Maximum 1 per class per week; teacher enters reason (shown to student only).

### 13.6 Subject Expert Badge
- Student scores >90% in same subject in 3 consecutive tests → "Subject Expert: Physics"
  permanent badge on profile.
- Shown on leaderboard alongside name.

### 13.7 Century Club
- Student completes 100 DPTs → "Century Club" membership badge; shown on leaderboard.
- 200 DPTs → "Double Century" badge; 365 DPTs → "Year-Long Warrior" badge.

### 13.8 Achievement Badges Summary
| Badge | Trigger | Permanence |
|---|---|---|
| Hat-trick | 3 consecutive tests >90% | Season |
| Comeback | Bottom 50% → Top 20% in one period | Season |
| Most Improved | Highest rank gain in a period | Season |
| Streak Master | 30-day daily engagement streak | Permanent |
| Series Champion | Highest avg percentile in complete series | Permanent |
| Subject Expert | >90% same subject, 3 consecutive tests | Permanent |
| Century Club | 100 DPTs | Permanent |
| Backlog-Free | Zero backlogs all semesters (college) | Semester |
| Gold Attendance | 100% attendance in a month | Monthly |
| Teacher's Pick | Awarded by class teacher | Weekly |

---

## 14. Display Channels

### 14.1 In-App (Primary)
- Student app: Leaderboard tab on home screen; default view = weekly composite.
- Teacher app: Class leaderboard with full names + metrics.
- Parent app: "Where My Child Stands" widget — rank + delta + score band; no peer data.
- Admin/Principal app: institution-wide leaderboard with drill-down.

### 14.2 Smart TV / Kiosk Mode
- School installs EduForge kiosk app on hallway TV / reception screen.
- Content rotates every 5 minutes: Class Toppers → House Points → Attendance Champions →
  Subject Toppers → Most Improved.
- Photos displayed only with leaderboard + photo consent (per student).
- Content controlled by institution admin; teacher can add custom message overlay.

### 14.3 WhatsApp Digest (Module 36)
- Weekly top-5 of class sent to class WhatsApp group (teacher-controlled broadcast).
- Text-only format; no photos; opt-in by parents for each student.
- Template: "Class 10-A Week of [date]: 1. [Name] — 96%, 2. [Name] — 94%..."
- Requires parent consent for each student's name to appear in group message.

### 14.4 Notice Board PDF
- Principal/teacher generates one-click printable A3 notice board:
  - Class toppers (top 10 per class).
  - House standings.
  - Subject toppers.
  - Attendance champions.
- Institution logo + watermark + date; printer-optimised PDF from CDN.

### 14.5 Parent App Widget
- Home screen widget: "Rahul — Rank 7 this week ↑2 | Physics Topper" — glanceable.
- Tapping opens full leaderboard + analytics.

### 14.6 Email Weekly Digest (Module 37)
- Opt-in weekly email to parent: child's rank, score trend, attendance %, top badge earned.
- Clean single-email format; responsive HTML; sent Monday morning.
- Unsubscribe link mandatory (CAN-SPAM / DPDPA compliance).

---

## 15. Analytics on Leaderboard Data

### 15.1 Rank Volatility Index
- Standard deviation of a student's rank across all periods in a season.
- High volatility = inconsistent performer; counsellor flag sent (Module 32).
- Low volatility = consistent; shown as "Consistent Performer" badge.

### 15.2 Class Consistency Index
- Standard deviation of all student ranks within a class.
- Low SD = competitive, close class; High SD = wide ability spread.
- Displayed to Academic Director; helps identify classes needing differentiated instruction.

### 15.3 Leaderboard Engagement Rate
- % of students who viewed leaderboard in a given week.
- Low rate → leaderboard not motivating; institution admin alerted with suggestion to run a
  Wildcard Week or Double XP event.

### 15.4 Correlation Reports
- Rank vs attendance % per class: Principal sees if attendance drives performance.
- Rank vs assignment submission rate: quantifies homework's impact on academic rank.
- Exportable for management meetings.

### 15.5 Gender Rank Gap Trend
- Average rank of boys vs girls per subject across terms.
- NEP 2020 gender equity monitoring; exported for AISHE annual return.
- Triggers intervention recommendation if gap widens for 2+ consecutive terms.

### 15.6 Prediction Accuracy
- Student's Module 22 projected rank vs actual term/annual rank.
- Validates and calibrates the rank predictor model; fed back to Module 22 analytics engine.

### 15.7 Teacher Effectiveness Insight
- Which teacher's class consistently ranks highest in the institution — internal, Academic
  Director view only; not published; used for HR and professional development, not punitive.

---

## 16. Mental Health & Ethical Design

### 16.1 No Rank Shaming
- Peer view never shows absolute rank number in anonymous mode — only "above/below" context.
- Bottom ranks not highlighted; no "worst student" display ever.

### 16.2 Improvement-First Default (Under Class 9)
- Students below Class 9: default leaderboard shows improvement rank (gains vs previous period),
  not absolute marks rank.
- Absolute rank available only in teacher/admin view for this age group.

### 16.3 Counsellor Auto-Flag
- Student drops >20 rank positions in a single week → silent flag sent to Module 32
  (Counselling) for teacher check-in.
- Student not notified of the flag; counsellor decides whether to initiate conversation.

### 16.4 Positive Framing
- Rank shown as "Top 12%" not "Rank 150 of 1200."
- "You've improved by 8 positions" not "You fell from Rank 5 to Rank 13."
- All notification copy reviewed for neutral/positive language — no shame language.

### 16.5 Opt-Out Zero Friction
- Single tap; confirmed immediately; no explanation required.
- No peer notification that student opted out (privacy of the opt-out itself).

### 16.6 Detained / Failed Students
- Excluded from public academic leaderboard automatically on Module 21 status update.
- Internal rank computed for teacher view; never shown in peer-facing display.

### 16.7 CWSN Exclusion Option
- Institution can disable public leaderboard display for CWSN students entirely.
- Rank computed internally for IEP (Individualised Education Plan) tracking.
- Divyang Achiever Board (Section 12.4) is the alternative recognition channel.

### 16.8 No Comparison by Caste / Religion
- System never segments public leaderboard by religion or caste.
- Category (SC/ST/OBC) used only for private scholarship/reservation purposes in staff view.
- Category-adjusted rank in coaching leaderboard: visible to student for self-awareness only;
  never shown to peers.

### 16.9 No Leaderboard for Detained / Expelled
- Expelled or withdrawn student: removed from leaderboard immediately.
- Historical snapshot retained internally for audit; not accessible to anyone except Platform
  Admin with documented justification.

---

## 17. Parent & Teacher Views

### 17.1 Parent Dashboard
- "Where My Child Stands" frame: rank (as percentile band) + score trend + badges earned.
- Not competitive: framed as personal progress; no peer data shown to parent.
- Historical rank chart: term-by-term rank trend for child.
- Alert: if child drops >20 ranks → parent notified with gentle, positive message (teacher
  already flagged to counsellor per Section 16.3).

### 17.2 Class Teacher View
- Full class leaderboard: real names + all component scores + rank + delta.
- Export PDF: leaderboard for PTM (Module 33); printable for parent meetings.
- Filter: by subject, by component (see attendance rank separately from exam rank).
- Weak student highlight: bottom 20% of class highlighted in red — for early intervention.

### 17.3 HOD View
- Department-level leaderboard: all classes under HOD; class average rank comparison.
- Identifies weak classes for targeted support.
- Subject performance comparison: which section scores highest in Physics — identifies teaching
  effectiveness variation across sections.

### 17.4 Principal / Academic Director View
- Institution-wide leaderboard with drill-down to class/section.
- Teacher effectiveness: which class consistently tops across subjects.
- Export: institution leaderboard PDF for management board / trust meetings.
- Inter-branch comparison: if multi-campus, branch-wise average rank comparison.

---

## 18. Notifications & Communication

### 18.1 Rank-Up (Student)
- FCM: "You moved from Rank 15 to Rank 8 this week in Class 10 Science — great progress!"
- Triggered when rank improves by ≥3 positions.

### 18.2 Topper Notification
- FCM + SMS: "Congratulations! You are Rank 1 in Class 12 Science this term."
- Also sent to parent (with consent).

### 18.3 Subject Topper
- FCM: "You are the Physics topper in your batch this month — Subject Expert badge earned!"

### 18.4 Rank Drop (Teacher Only)
- Internal alert: "5 students dropped >10 ranks this week" — class teacher dashboard.
- Not sent to students; for teacher intervention only.

### 18.5 Dethrone Alert (Opt-In Student)
- Student opts in: notified when displaced from top 3.
- Template: "You've been overtaken — someone is catching up! Step up!"
- Shown only if student explicitly enabled this notification type.

### 18.6 Weekly Digest (Student Opt-In)
- Monday FCM summary: "Your week — Rank 12 (↑3), Attendance 95%, 4 tests done, XP: 240."

### 18.7 House Champion Alert
- FCM to all students of winning house: "Red House is leading this week! Keep it up!"
- Sent weekly if house standings change.

### 18.8 Badge Earned
- FCM on any badge earned: "You've earned the Subject Expert badge for Physics! It's on your
  profile now."

---

## 19. Leaderboard APIs & Integrations

### 19.1 Leaderboard Widget API (Module 51)
- Institution embeds live leaderboard snippet on their own website via B2B API.
- Shows only opted-in students; authenticated per institution API key.
- Returns: rank, name (or "Student #N"), badge, score band — no full marks.

### 19.2 Export API
- Institution's ERP/MIS pulls rank data via authenticated API for their own reporting.
- Per DPDPA 2023: bulk rank export requires institution admin + Platform Admin authorization.
- Each export logged with timestamp, requested_by, purpose.

### 19.3 Scholarship Integration (Module 21)
- Top 10% identification from leaderboard → auto-feeds Module 21 scholarship eligibility engine.
- Girl Achiever Board feeds girl-specific scholarship schemes.
- Rural Achiever Board feeds Aspirational Districts / rural scholarship targeting.

### 19.4 Placement Cell API (Module 51)
- College placement cell pulls CGPA rank + placement readiness rank for shortlisting.
- Requires student consent token (DPDPA 2023 §7).

### 19.5 NAAC/NBA Export
- Institution-level rank distribution exported in NAAC SSR Criterion II format.
- Student progression data: % in top quartile, % improved year-on-year.

### 19.6 Internal Module Integrations
| Module | Integration |
|---|---|
| Module 11/12/13 (Attendance) | Attendance component of composite rank |
| Module 14 (Assignments) | Assignment component of composite rank |
| Module 21 (Results) | Exam component; rank certificate; scholarship list |
| Module 22 (Test Series) | Test series rank; XP; DPT streak; badges |
| Module 28 (Hostel) | Hostel conduct board |
| Module 30 (Library) | Reading leaderboard |
| Module 32 (Counselling) | Auto-flag on rank drop |
| Module 33 (PTM) | Leaderboard PDF for parent meetings |
| Module 34 (Announcements) | House champion broadcast |
| Module 35/36/37/38 (Notifications) | FCM / WhatsApp / Email / SMS hooks |

---

## 20. Edge Cases & Integrity

### 20.1 Transferred Student
- Prior institution's rank history not imported; rank computed fresh from date of joining.
- "New Joinee" tag shown on leaderboard for first 4 weeks.

### 20.2 Rank Manipulation Detection
- If component score jumps anomalously (e.g., assignment marks suddenly 100% after weeks of
  0%) → flag to HOD before rank update published.
- HOD can approve (genuine) or reject (suspicious); if rejected, previous score used pending
  investigation.

### 20.3 Duplicate Student
- If same student created twice (name + DOB + class match) → ranks merged after admin
  verification; no double-counting.
- Merged student's best composite score per period retained.

### 20.4 Rank During Re-evaluation
- Marked "PROVISIONAL" if any component score is under Module 21 re-evaluation.
- Frozen until re-evaluation resolved; then rank updated with corrected score.

### 20.5 Expelled / Withdrawn
- Removed from leaderboard immediately on status change.
- Historical snapshots retained internally; accessible only to Platform Admin with documented
  justification.

### 20.6 System Downtime Compensation
- If scheduled test could not run due to platform downtime → test excluded from rank
  computation for that period; all students treated as if test not held.
- Platform Admin can flag a test as "EXCLUDED_FROM_RANK" with reason.

---

## 21. Compliance Checklist

| Regulation / Standard | Compliance Point |
|---|---|
| DPDPA 2023 §7 | Opt-in consent for leaderboard visibility; parent consent for under-18; data minimisation |
| RPWD Act 2016 | Divyang Achiever Board; CWSN exclusion from general leaderboard; no discriminatory display |
| RTE Act | RTE-seat students compete equally; no economic marker shown to peers |
| NEP 2020 | Gender gap monitoring; improvement-first philosophy; multidisciplinary credit integration |
| POCSO Act | No student photo on kiosk/public without explicit parent photo consent |
| RTI Act 2005 | Rank audit log immutable and RTI-defensible; computation trail stored |
| BETI BACHAO BETI PADHAO | Girl Achiever Board; gender rank gap reporting |
| Aspirational Districts (NITI Aayog) | Rural Achiever Board; rural student recognition |
| NIPUN Bharat | FLN leaderboard for Classes 1–3 (teacher-only monitoring) |
| NAAC/NBA | CO attainment rank; institution rank distribution export in SSR format |
| AISHE | Gender rank gap data export for annual return |

---

## 22. DB Schema

### Table: `leaderboard_config`
```
config_id              UUID PRIMARY KEY
name                   VARCHAR(100)
scope                  VARCHAR(30)   -- SECTION | CLASS | STREAM | BATCH | BRANCH | INSTITUTION | STATE | NATIONAL
time_period            VARCHAR(20)   -- DAILY | WEEKLY | MONTHLY | TERM | SEMESTER | PHASE | ANNUAL | ROLLING_30 | TEST
component_weights      JSONB         -- {exam: 60, attendance: 20, assignment: 15, cocurr: 5}
max_student_scope      VARCHAR(30)   -- cap for student-visible scope
privacy_default        VARCHAR(20)   -- ANONYMOUS | FULL_VISIBLE | HIDDEN
min_age_display        INT DEFAULT 8
improvement_first_below_class INT DEFAULT 9
active                 BOOLEAN DEFAULT TRUE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `leaderboard_snapshots`
```
snapshot_id            UUID PRIMARY KEY
config_id              UUID REFERENCES leaderboard_config(config_id)
snapshot_date          DATE
period_label           VARCHAR(50)   -- "Week 12 — Mar 2026" / "Term 1 2025-26"
student_id             UUID
rank                   INT
composite_score        NUMERIC(6,2)
rank_delta             INT           -- positive = improved; negative = fell
component_scores       JSONB         -- {exam: 78.5, attendance: 92, assignment: 88, cocurr: 75}
is_provisional         BOOLEAN DEFAULT TRUE
is_final               BOOLEAN DEFAULT FALSE
anomaly_flagged        BOOLEAN DEFAULT FALSE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `leaderboard_privacy`
```
privacy_id             UUID PRIMARY KEY
student_id             UUID
config_id              UUID REFERENCES leaderboard_config(config_id)
is_visible             BOOLEAN DEFAULT FALSE
use_anonymous          BOOLEAN DEFAULT TRUE
photo_consent          BOOLEAN DEFAULT FALSE
kiosk_consent          BOOLEAN DEFAULT FALSE
whatsapp_consent       BOOLEAN DEFAULT FALSE
consent_by             UUID          -- student_id (18+) or parent_id (under 18)
consent_date           TIMESTAMPTZ
tenant_id              UUID NOT NULL
updated_at             TIMESTAMPTZ
```

### Table: `house_points`
```
point_id               UUID PRIMARY KEY
house_id               UUID
student_id             UUID
points                 INT
source                 VARCHAR(30)   -- EXAM | SPORTS | CULTURAL | ATTENDANCE | NCC_NSS | SCOUT
source_ref_id          UUID NULL     -- exam_id / event_id etc.
awarded_by             UUID          -- staff_id
awarded_at             TIMESTAMPTZ DEFAULT NOW()
tenant_id              UUID NOT NULL
```

### Table: `rank_certificates`
```
cert_id                UUID PRIMARY KEY
student_id             UUID
period_label           VARCHAR(50)
rank                   INT
scope                  VARCHAR(30)
cdn_path               VARCHAR(500)
document_hash          CHAR(64)
issued_at              TIMESTAMPTZ
issued_by              UUID
digilocker_uri         VARCHAR(500) NULL
tenant_id              UUID NOT NULL
```

### Table: `study_groups`
```
group_id               UUID PRIMARY KEY
group_name             VARCHAR(100)
created_by             UUID          -- student_id
members                JSONB         -- [{student_id, joined_at, role: LEADER | MEMBER}]
max_members            INT DEFAULT 5
active                 BOOLEAN DEFAULT TRUE
tenant_id              UUID NOT NULL
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `group_leaderboard`
```
entry_id               UUID PRIMARY KEY
group_id               UUID REFERENCES study_groups(group_id)
period_label           VARCHAR(50)
avg_score              NUMERIC(6,2)
rank                   INT
rank_delta             INT
tenant_id              UUID NOT NULL
snapshot_date          DATE
```

### Table: `special_awards`
```
award_id               UUID PRIMARY KEY
student_id             UUID
award_type             VARCHAR(30)   -- TEACHERS_PICK | SUBJECT_EXPERT | CENTURY_CLUB | COMEBACK |
                                     -- MOST_IMPROVED | STREAK_MASTER | SERIES_CHAMPION |
                                     -- BACKLOG_FREE | GOLD_ATTENDANCE | DETHRONE_ALERT
awarded_by             UUID NULL     -- staff_id (for TEACHERS_PICK)
period_label           VARCHAR(50)
subject                VARCHAR(100) NULL
reason                 TEXT NULL     -- for TEACHERS_PICK
tenant_id              UUID NOT NULL
awarded_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `kiosk_config`
```
kiosk_id               UUID PRIMARY KEY
device_name            VARCHAR(100)
location               VARCHAR(200)  -- "Main Corridor / Reception / Hostel"
display_scope          VARCHAR(30)
rotation_interval_sec  INT DEFAULT 300
content_types          TEXT[]        -- ['CLASS_TOPPER','HOUSE_BOARD','ATTENDANCE_STAR','SUBJECT_TOPPER']
consent_verified       BOOLEAN DEFAULT FALSE
active                 BOOLEAN DEFAULT TRUE
tenant_id              UUID NOT NULL
configured_by          UUID
created_at             TIMESTAMPTZ DEFAULT NOW()
```

### Table: `leaderboard_audit_log`
```
log_id                 UUID PRIMARY KEY
snapshot_id            UUID REFERENCES leaderboard_snapshots(snapshot_id)
student_id             UUID
computed_at            TIMESTAMPTZ
component_inputs       JSONB         -- raw scores fed in
formula_string         TEXT          -- formula used
output_rank            INT
anomaly_flagged        BOOLEAN DEFAULT FALSE
anomaly_reason         TEXT NULL
reviewed_by            UUID NULL
review_decision        VARCHAR(20) NULL  -- APPROVED | REJECTED
tenant_id              UUID NOT NULL
```
