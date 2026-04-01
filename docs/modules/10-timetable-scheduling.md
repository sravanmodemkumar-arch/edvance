# Module 10 — Timetable & Scheduling

## Purpose
Define how EduForge generates, manages, publishes, and tracks timetables for all institution types — school, college, coaching centre, ITI, and exam centre — across all Indian academic structures (terms, semesters, annual, continuous, batch-based), ensuring compliance with CBSE, UGC, state board, and NEP 2020 norms.

---

## 1. Institution-Type-Specific Timetable Models

Each institution type has a distinct timetable model:

| Institution Type | Timetable Model |
|---|---|
| School (CBSE / State Board) | Class → Section → Period per day |
| College (UG / PG / Degree) | Department → Course → Lecture / Lab / Tutorial per slot |
| Coaching Centre | Batch → Weekly time pattern (e.g., Mon/Wed/Fri 6–8 PM) |
| ITI | Trade → Theory half-day + Practical half-day alternating |
| Exam Centre | Hall schedule only — no regular class timetable |

Institution type is set during onboarding (Module 04) and drives which timetable model is activated.

---

## 2. Academic Structure Linkage

- Every timetable belongs to: Academic Year → Term / Semester / Batch (as per Module 05 structure type)
- Timetable cannot span across term or semester boundaries
- When a new term/semester starts, a new timetable version is created
- Annual-structure schools have one timetable per academic year with mid-year revision capability
- Batch-based coaching timetables are tied to batch start/end dates

---

## 3. Bell Schedule Definition

- Institution admin defines the bell schedule per branch per shift
- Each bell entry has: slot name, start time, end time, type (Lecture / Lab / Recess / Lunch / PT / Assembly / Free / Prayer / Yoga / Zero Period)
- Different wings of the same campus (primary, secondary, senior secondary) can have different bell schedules
- Bell schedule is approved by Principal before activation
- Changes to bell schedule mid-year require Principal approval and trigger in-app notification to all staff and students

---

## 4. Period Slot Matrix

| Institution Type | Max Slots/Day | Typical Duration |
|---|---|---|
| School (primary) | 6–7 | 35–40 min |
| School (secondary/sr. sec.) | 8–10 | 40–45 min |
| College | 6–8 | 50–55 min (lecture), 2–3 hrs (lab) |
| Coaching | 2–4 | 1.5–2 hrs per slot |
| ITI | 4–6 | 1 hr (theory), 3 hrs (practical block) |

Period count and duration are configurable per institution. System does not enforce a fixed national default — institution sets its own, within CBSE/UGC/State Board compliance bounds.

---

## 5. Double Period / Continuous Slot

- Consecutive period pair explicitly marked as a double period for: lab practicals, drawing, art, workshop
- Double period cannot be split for substitution — if teacher absent, entire double period is treated as one unit
- System prevents scheduler from inserting a single-period subject into a double-period slot

---

## 6. Zero Period & Extra Period

- Zero period: before regular bell (e.g., 6:30–7:15 AM) for early batches or coaching add-ons
- Extra period: after regular bell for remedial, coaching, or enrichment classes
- Both are optional and configured per institution
- Attendance and period diary entries are tracked for zero/extra periods separately
- Students/parents can see zero/extra period entries in their timetable view

---

## 7. Morning Prayer / National Anthem Slot

- Dedicated first slot for morning prayer and national anthem — mandatory in government-aided and many private schools per state government and NCERT norms
- Duration: typically 10–15 minutes before Period 1
- Attendance captured during assembly/prayer separately from class attendance
- Slot type = "Prayer" in bell schedule; cannot be assigned a subject or teacher
- Schools that do not have this requirement can disable the slot in institution config

---

## 8. Morning Assembly Slot

- Separate from prayer — assembly includes announcements, thought of the day, student presentations
- Duration configurable (typically 15–20 min)
- Can be combined with prayer slot or kept separate
- Class teacher or duty teacher manages assembly; logged in duty roster

---

## 9. Subject–Teacher Mapping

- Admin assigns: Subject → Teacher → Class/Section (for schools) or Course → Faculty → Batch/Section (for colleges)
- One subject can have multiple teachers (parallel sections, split teaching between two staff)
- For a subject taught by two teachers in the same section (co-teaching), both are listed; period diary entries required from both
- Mapping stored per academic year → term/semester; can be revised for next term
- HOD reviews and approves department-level subject–teacher mappings before timetable generation

---

## 10. Visiting / Guest Faculty Availability Windows

- Part-time, visiting, or contract faculty declare available days and time windows
- System stores availability as a recurring weekly pattern (e.g., Tuesday and Thursday, 10 AM–2 PM)
- Auto-generation engine respects these windows — visiting faculty never assigned outside declared availability
- Admin can override with faculty consent (logged)
- If visiting faculty availability changes mid-term, affected timetable periods are flagged for reassignment

---

## 11. Room / Hall Assignment per Subject

| Subject Type | Required Room Type |
|---|---|
| Theory / Lecture | Classroom (capacity matched to section strength) |
| Science Lab | Designated lab (Physics / Chemistry / Biology) |
| Computer Science | Computer lab (with system count ≥ section strength) |
| Physical Education | Ground / court / gymnasium |
| Drawing / Art | Drawing hall |
| Music | Music room |
| Library period | Library |
| Workshop / Practical (ITI) | Trade-specific workshop |

Room assignment is constraint-enforced — if no suitable room is available in a slot, generator flags it and does not auto-assign.

---

## 12. Lab Practical Batch Splitting

- For a class of N students, lab capacity is typically N/2
- System splits the class into Batch A and Batch B for lab periods
- Batch A attends lab in first half; Batch B attends theory; swapped next period or next week
- Both batches covered within the same week using the same lab room
- Attendance and period diary maintained separately for each batch
- Splitting configuration stored: batch size, split method (alphabetical / roll number range / manual)

---

## 13. Cross-Section / Combined Class Periods

- Two or more sections merged for a subject period (e.g., one EVS teacher for Sections A + B simultaneously)
- Combined class requires a room with sufficient capacity (sum of both sections)
- System checks room capacity before allowing combined period
- Attendance taken section-wise even when combined
- Period diary entry logged once but mapped to both sections

---

## 14. Elective Subject Parallel Grouping

- Students who chose different electives (e.g., Computer Science vs Physical Education vs Fine Arts) go to different rooms in the same period
- Student-wise elective choice (recorded at enrolment / subject selection) drives individual timetable generation
- Parallel groups auto-created: Group 1 (CS elective), Group 2 (PE elective), Group 3 (Fine Arts) — each with own teacher and room
- Student's personal timetable shows their specific elective group schedule
- Conflict check: a student cannot be in two elective groups simultaneously

---

## 15. Python Auto-Generation Engine

Python script generates a conflict-free timetable given:
- Input: subjects list, teacher–subject mapping, room constraints, period quotas per subject per week, unavailability windows, double period requirements, elective groups, lab batch splits
- Algorithm: constraint-satisfaction with backtracking; attempts to distribute subjects evenly across the week (no subject twice in a day unless quota demands)
- Output: populated `timetable_entries` table; draft status for HOD/Principal review
- Generation time target: < 30 seconds for a 40-section school
- If constraints cannot be fully satisfied, generator produces a partial timetable with a gap report listing unresolved conflicts for manual resolution

---

## 16. CBSE Subject Period Quota Compliance

CBSE prescribes minimum periods per week per subject for affiliated schools:

| Level | Subject | Min Periods/Week |
|---|---|---|
| Secondary (9–10) | Mathematics | 6 |
| Secondary (9–10) | Science | 6 |
| Secondary (9–10) | Social Science | 5 |
| Secondary (9–10) | Languages (each) | 5 |
| Sr. Secondary (11–12) | Core subject | 5–6 |
| Sr. Secondary (11–12) | Elective | 4–5 |

System stores CBSE quota table per class group. Timetable cannot be published if any subject falls below CBSE minimum. Warning displayed with specific subject and shortfall count.

---

## 17. UGC Credit-Hour Compliance

- Each college course carries credit units (e.g., 3-credit course = 45 contact hours per semester = ~3 lectures/week for 15-week semester)
- System calculates required lectures per week from credit units and semester duration
- Timetable auto-fills required lecture count per course; warns if allocated periods fall short of UGC minimum
- Lab courses: 1 credit = 2 lab hours/week (UGC norm)
- Tutorial sessions: counted separately, minimum 1 tutorial/week for Mathematics and Science courses
- Compliance dashboard shows credit-hour status per course per department

---

## 18. State Board Period Compliance

Different state boards have their own period-per-subject norms:

| State Board | Period Norm |
|---|---|
| Maharashtra SSC | 35–36 periods/week total; subject-wise distribution per state circular |
| Tamil Nadu State Board | 40 periods/week; Tamil mandatory 6 periods/week |
| UP Board (Madhyamik) | 6 working hours/day; subject periods per prescribed syllabus |
| Karnataka SSLC | 240 working days/year; subject hours per DSERT circular |
| Rajasthan Board | 210 working days; state-prescribed subject distribution |

Institution admin selects affiliated board during onboarding. System loads the corresponding compliance quota table. Timetable validation checks against the selected board's norms. Custom quota override available for institutions with special dispensation (requires Principal to confirm and reason is logged).

---

## 19. NEP 2020 Mandated Periods

NEP 2020 introduces mandatory non-academic periods:

| Period Type | Minimum Allocation |
|---|---|
| Yoga & Health Education | 1 period/week (all classes) |
| Value Education / Ethics | 1 period/week (Classes 1–12) |
| Art / Craft / Cultural | 2 periods/week (Classes 1–8) |
| Life Skills | 1 period/week (Classes 9–12) |
| Physical Education | 2 periods/week (all classes) |
| Work Experience | 1 period/week (Classes 6–10 per CBSE) |

System tracks these as mandatory slots. Timetable compliance check includes NEP slot verification. Institutions can mark themselves as "NEP-transitioning" to get a soft warning instead of a hard block.

---

## 20. Teaching Load per Staff Category

| Staff Category | Min Periods/Week | Max Periods/Week |
|---|---|---|
| PGT (Post-Graduate Teacher) | 18 | 24 |
| TGT (Trained Graduate Teacher) | 24 | 30 |
| PRT (Primary Teacher) | 30 | 36 |
| College Lecturer / Assistant Professor | 14 | 16 (UGC norm) |
| College Associate Professor | 12 | 14 |
| Coach / Trainer | 20 | 28 |
| ITI Trade Instructor | 22 | 28 |
| Visiting Faculty | Per declared availability | No fixed max |

UGC Regulation 2018: Assistant Professor maximum direct teaching = 16 hours/week; Associate Professor = 14 hours/week; Professor = 14 hours/week. System enforces these limits. Auto-generation respects min/max; manual override triggers overload alert to HOD.

---

## 21. Conflict Detection

System prevents saving a timetable that contains:
- Teacher assigned to two different sections in the same period
- Same room booked for two different sections/subjects in the same period
- A section assigned two subjects in the same period
- A subject allocated more periods than its weekly quota in a single day (subject appearing 3 times on the same day)
- A teacher assigned a period during a declared unavailability window
- A combined class where total student count exceeds room capacity

All conflicts are listed with specific details (teacher name, period, section, date) before the save is blocked.

---

## 22. Multi-Building Travel Buffer

- Campus buildings/blocks tagged with travel time between them (configured by admin — e.g., Block A to Lab Building: 5 minutes)
- If a teacher has consecutive periods (back-to-back) in rooms requiring > 0 minutes travel, system warns: "Teacher X has no travel time between Block A Room 204 and Lab Block Room L3"
- Warning is non-blocking (advisory) — Principal can override
- Large campuses with separate hostel buildings, medical blocks, and main buildings benefit from this constraint

---

## 23. Teacher Unavailability Blocking

- Staff can mark specific dates and periods as unavailable (medical, election duty, exam invigilation duty, training, family emergency)
- Unavailability request approved by HOD (for planned) or auto-approved for emergencies with admin notification
- System flags all timetable periods assigned to that teacher during unavailability window for substitution
- Approved unavailability windows are excluded from auto-generation constraints

---

## 24. Coaching Batch Time Pattern

- Each coaching batch has a fixed weekly recurring pattern: days of week + start time + end time
- Examples: JEE Maths Batch A → Mon, Wed, Fri 6:00–8:00 PM; NEET Bio Batch B → Tue, Thu, Sat 7:00–9:00 PM
- Multiple batches of the same subject can run at different time slots (morning batch, evening batch, weekend batch)
- Student is enrolled in a specific batch; their timetable shows only their batch schedule
- Batch pattern can include Sunday (coaching centres commonly run Sunday sessions)

---

## 25. Demo / Trial Class Slot

- Inquiry students (from Module 31 Admission CRM) can be assigned a one-time trial/demo class slot
- Trial slot pulled from existing batch timetable (student sits in a live batch)
- Trial attendance recorded separately; does not affect enrolled students' attendance percentage
- On admission confirmation, student transitions from trial to enrolled status in that batch automatically

---

## 26. Batch Overlap Conflict

- A student may be enrolled in multiple coaching batches (e.g., JEE Maths + JEE Physics)
- System detects if any two of the student's batch schedules overlap (same day + overlapping time window)
- Conflict flagged at enrolment time with specific batch names, days, and conflicting time range
- Admin must resolve before confirming enrolment
- Student-level timetable view shows combined schedule across all enrolled batches

---

## 27. Coaching Holiday Override

- Coaching centre admin can declare a holiday for a specific batch without affecting other batches or other institution types
- Batch-level holiday: "JEE Maths Batch A — no class on 14 March"
- Other batches run as normal
- Affected students notified in-app
- Batch holiday does not count as a working day for that batch's attendance percentage calculation

---

## 28. Exam Timetable Generator

- Separate exam schedule distinct from regular class timetable (generated from Module 18 Exam Paper Builder)
- Exam timetable defines: date, subject, start time, duration, exam hall(s), seating count
- Regular class timetable is auto-suspended for all classes on exam days
- For large institutions, multiple sessions (morning/afternoon) per day supported
- Exam timetable published via Principal approval; in-app notification to all students and parents
- Seating arrangement (hall ticket + seat number) generated from exam timetable + enrolled students list (Python)

---

## 29. Exam Duty Roster

- Invigilator, relief invigilator, and flying squad assigned per exam hall per session
- Duty roster generated by Python: distributes duty across teaching staff (excluding teachers of the subject being examined in that hall where possible)
- Chief Superintendent and Additional Superintendent assigned per exam day
- Duty roster approved by Principal and published; staff notified in-app
- Exchange of duty requires HOD approval and is logged

---

## 30. Pre-Exam Study Leave Schedule

- Configurable study leave days before exam start date (e.g., 3 days for unit test, 5 days for term exam, 10 days for board prep)
- During study leave, timetable shows "Study Leave" for all periods; regular attendance not taken
- Self-study / library access during study leave tracked separately (optional log)
- Study leave dates set by Principal; cannot overlap with exam days

---

## 31. PTM Slot Scheduling

- Parent-Teacher Meeting (PTM) days scheduled in advance on the academic calendar
- On PTM day, regular timetable is shortened (e.g., 4 periods instead of 8); remaining time used for PTM slots
- Each teacher assigned a PTM slot window; parents book specific slot within window (linked to Module 33)
- PTM timetable generated and published separately; in-app reminder sent to parents 48 hours before

---

## 32. Remedial / Extra Class Scheduling

- Remedial classes scheduled outside regular periods for students identified as weak (based on assessment scores from Module 21)
- Separate timetable view for remedial schedule; does not appear in main class timetable
- Attendance tracked separately; counts toward teacher's additional teaching hours
- Remedial session linked to specific subject; teacher's remedial period count shown in monthly report
- Student/parent notified in-app when remedial class is scheduled

---

## 33. Board Exam Special Revision Timetable

- For Class 10 / Class 12: 4–6 weeks before board exam, a special revision timetable activates
- Revision timetable: more periods for core exam subjects, reduced or suspended non-exam activities (cultural, PT, etc.)
- Generated separately; co-exists with regular timetable but overrides it for specified date range
- Aligned with CBSE / state board exam schedule
- Principal approves and publishes; staff and students notified in-app

---

## 34. Annual Function / Cultural Event Rehearsal Scheduling

- Admin allocates rehearsal periods weeks in advance for annual function, sports day, cultural fest, Republic Day / Independence Day programmes
- Rehearsal periods placed in timetable as special slots (type = "Rehearsal"); regular periods for that slot are suspended or shortened
- System generates a modified timetable for rehearsal days showing shortened academic periods + rehearsal blocks
- Staff assigned to supervise rehearsal groups listed in duty roster
- In-app notification to participating students and staff on rehearsal schedule

---

## 35. Sports Day / Inter-House Competition Schedule

- Full-day or half-day special event timetable for sports day, inter-house competitions, annual sports meet
- Regular class periods suspended for participating classes; non-participating classes (if any) follow regular timetable
- Ground / court / gymnasium allocated as event venues; no other booking allowed on that day
- Staff duty assignments (start, finish, event management, first-aid duty) generated and published
- Results from inter-house competitions optionally linked to Module 23 Leaderboard

---

## 36. Saturday Catch-Up Class Schedule

- If school/college working days are lost due to floods, bandh, unexpected closure, or examination duty:
  - Principal can schedule Saturday catch-up classes for affected classes
  - System generates one-time Saturday timetable with periods for missed subjects
  - Attendance and period diary tracked as normal
  - Students and parents notified in-app with specific Saturday schedule
- Saturday catch-up does not automatically recur — each Saturday session requires explicit Principal scheduling

---

## 37. Internal Practical Exam Slot

- Internal lab / practical exams scheduled as special timetable entries (separate from regular lab sessions)
- Lab room locked for that slot — no other booking allowed
- External examiner (for college practicals per UGC norms) assigned and logged
- Practical exam date communicated to students via in-app notification
- Results from internal practical exams fed into Module 20 / Module 21

---

## 38. Guest Lecture / Expert Session

- One-time external expert lecture allocated to a specific period, replacing regular subject for that day
- Recorded in timetable as special slot type "Guest Lecture"
- Guest speaker details (name, designation, organisation) captured
- Attendance taken for that period; period diary notes: topic, speaker
- Students notified in-app; regular subject teacher's period diary shows "Replaced by Guest Lecture" for that period

---

## 39. Industrial Visit / Field Trip Timetable Override

- On field trip or industrial visit day: participating sections have all periods suspended; system marks them "Field Trip"
- Non-participating sections follow regular timetable
- Attendance for participating students captured under category "Field Trip" (counted as present per CBSE norms)
- School bus / transport booking linked to Module 29 Transport
- Return time logged; if return is after school hours, partial day attendance applied

---

## 40. Staff Meeting / Department Meeting Scheduling

- HOD schedules department meetings during staff free periods (cross-checked against timetable)
- Principal schedules all-staff meeting; system finds a common free window across all staff
- Meeting event appears in staff timetable view for that period
- Meeting agenda and attendance recorded in staff meeting log
- Conflicts between a scheduled meeting and a period assignment trigger a warning to HOD / admin

---

## 41. Split-Shift School Operation

- One building operates two shifts: morning shift (e.g., 6:30 AM–12:30 PM) and afternoon shift (12:30–6:30 PM)
- Each shift has its own set of sections, bell schedule, and timetable
- Staff may be assigned to morning shift only, afternoon shift only, or both (load calculated across both shifts)
- Room allocation is shift-aware: same room can be used by different sections in different shifts without conflict
- Common to government schools in urban areas and double-shift coaching centres

---

## 42. Shared Building — Two Institutions

- Two separate tenant institutions share the same physical building (e.g., government school in morning + private coaching in evening)
- Each institution is a separate tenant in EduForge
- Room booking system checks across both tenants' timetables to prevent physical room overlap
- Cross-tenant room conflict detection managed at the branch level by branch admin with dual-institution access
- Handled via platform-level room booking, not tenant-level timetable (tenants cannot see each other's timetable)

---

## 43. Substitution Trigger

- When a teacher is marked absent in Module 11 Attendance (or marks self-absent via leave application):
  - All that teacher's timetable periods for that day are flagged as "Substitution Required"
  - Admin / HOD receives in-app alert: teacher X absent, N periods need substitution
  - Substitution must be assigned before that period begins; overdue substitution alerts escalate to Principal

---

## 44. Substitute Suggestion Engine

Python suggests substitute teachers for each period requiring substitution:
- Criteria: teacher is free in that period (no assigned class), same subject qualification preferred (but not mandatory), not exceeding daily period cap, not on leave
- Ranked list: first preference = same subject; second = related subject; third = any available teacher
- HOD selects from suggested list or manually assigns
- Substitution confirmed in-app notification sent to substitute teacher and affected students

---

## 45. Substitution Log

- Every substitution records: date, period, original teacher, substitute teacher, subject, class/section, reason (original teacher absent / on leave / official duty)
- Digitises the physical substitution register maintained in schools
- Substitution log searchable by date range, teacher, class
- End-of-month substitution summary: per teacher — periods substituted (given to others + taken from others), net balance
- Generated as PDF for physical records if required

---

## 46. Monthly Substitution Report

- Per teacher: total periods scheduled, total periods conducted, total periods substituted (by others), total substitutions done (for others)
- Comparison against scheduled timetable: effective teaching percentage
- Report generated for Principal at end of each month
- Integrated into teacher's service record (Module 08 period diary)
- Chronic absence requiring substitution flagged to management

---

## 47. Self-Substitution / Period Exchange

- A teacher can request to swap a period with another teacher on a future date (e.g., I'll take your Monday 3rd period if you take my Wednesday 5th)
- Both teachers must confirm the exchange in-app
- HOD approves the exchange
- Swap recorded in timetable; both teachers' period diary entries adjusted
- Prevents unofficial informal swaps that go unrecorded

---

## 48. Timetable Draft → HOD → Principal → Publish Workflow

```
Auto-generated / manually created (Admin)
        ↓
HOD Review (per department / per class level)
  — HOD can edit teacher assignments, request period changes
        ↓
Principal Final Review & Approval
  — Principal can send back to HOD for revision
        ↓
Published
  — In-app notification: all affected students, parents (school), staff
  — Timetable locked for editing
```

For coaching centres without HOD structure: Admin → Principal/Owner approval → Publish.

---

## 49. Timetable Versioning

- Every published timetable gets a version number (e.g., v1, v2, v3) with timestamp and approver name
- Previous versions archived and viewable (read-only) — useful for dispute resolution, inspection
- Audit log records every change: field changed, old value, new value, changed by, timestamp
- Version comparison: admin can diff two versions to see exactly what changed

---

## 50. Mid-Term Timetable Revision

- Post-publication changes require Principal to unlock the timetable with reason
- Changes logged in audit trail (who, what, when, reason)
- After revision, HOD re-reviews changed sections; Principal re-approves
- Affected staff and students receive in-app notification: "Timetable updated — [specific change details]"
- Students/parents see revision history with timestamps in their timetable view

---

## 51. Timetable Lock After Publish

- Published timetable is locked against accidental edits
- Any edit requires: Principal unlocks → admin edits → HOD reviews → Principal re-approves → re-publish
- Unlock with reason is mandatory; reason appears in audit log
- Time-limited unlock: system re-locks after 24 hours if re-publish not completed, discarding unapproved changes

---

## 52. Subject Mid-Term Addition

- A new subject added during the term (e.g., new vocational elective, bridge course):
  - System scans all sections' timetables for free slots matching required period count
  - Suggests least-disruptive insertion points (free periods or lower-priority optional periods)
  - Teacher assigned; room allocated; conflict check run
  - Minimal disruption: existing periods not moved unless unavoidable
  - Published after standard HOD → Principal approval

---

## 53. Timetable Template Library

- Admin can save current timetable as a named template (e.g., "Class 10 — 2024–25 Term 1 Timetable")
- Templates stored per institution, per branch, per class level
- Next year / next term: admin loads template, updates teacher assignments for any staff changes, runs conflict check, publishes
- Reduces setup time for new terms by 60–70%
- Templates can be shared across branches of the same institution (branch admin can adopt with local modifications)

---

## 54. Class/Section Timetable View (Student & Parent)

- Students and parents (school-level) see the complete class timetable:
  - Today's schedule highlighted at top with current period and next period countdown
  - Weekly view: Mon–Sat (or Mon–Fri per institution config)
  - Period details: subject, teacher name, room number
  - Colour-coded by subject type (theory, lab, PE, activity)
- Timetable shown in parent app only for school students (no parent timetable view for college / coaching as per Module 09 rules)

---

## 55. Teacher Personal Timetable View

- Teacher sees their personal timetable: which class, which subject, which room, each period
- Free periods clearly marked
- Substitution periods shown in a different colour with original teacher noted
- Today's schedule at top; weekly view navigable
- Period diary entry button on each period in teacher view (direct link to syllabus/diary module)

---

## 56. Room Utilization View

- Admin sees room-wise timetable: every room × every period × every day
- Free slots visible for ad-hoc meeting / guest lecture bookings
- Room utilization percentage: how much of available time each room is booked
- Filter by room type (classroom, lab, ground, hall)
- Export as PDF for facilities management

---

## 57. Live Concurrent School View

- Admin / Principal sees a real-time grid: every section × every period right now
- Current period highlighted; shows: subject being taught, teacher name, room
- Substitution flags in red for periods where substitution is pending
- Absent teacher periods shown in orange
- Refreshes automatically; can be displayed on admin dashboard monitor

---

## 58. Weekly and Monthly Calendar View

- Timetable overlaid on academic calendar (from Module 05)
- Holidays shown as blocked days; exam weeks shown as exam timetable
- Events (PTM, sports day, annual function) shown inline with timetable
- Month view shows cumulative period count per subject for the month
- Teacher can see their own monthly calendar with periods, meetings, and events

---

## 59. Timetable PDF Export

- Class-wise timetable PDF: formatted for display on classroom notice board (A4 / A3)
- Teacher-wise PDF: personal timetable for each staff member
- Generated by Python using institution branding (logo, institution name, academic year, term)
- Batch export: all class timetables in one ZIP for principal's records
- CBSE-format export for affiliation submission (structured layout per CBSE prescribed format)

---

## 60. CBSE Affiliation Timetable Export

- CBSE requires schools to submit timetable details during affiliation / renewal
- System exports timetable in CBSE-prescribed format:
  - School hours (start time, end time, number of working days)
  - Periods per subject per week for each class
  - Teacher names against subjects
- Export as PDF + structured data (CSV format for CBSE portal upload)
- Generated by Principal or admin; logged in compliance records

---

## 61. Period Diary Entry per Timetable Slot

- Every published timetable period generates a diary stub for the assigned teacher
- After the period, teacher marks the diary entry: topic taught, textbook pages covered, homework assigned, next topic planned
- If period was not conducted (teacher absent, holiday, event), teacher marks reason
- Period diary feeds into:
  - Syllabus completion tracker (Module 15)
  - Attendance module (Module 11) — period-wise attendance
  - Monthly teaching report for management
- Diary entry must be completed within 24 hours of the period; overdue entries flagged to HOD

---

## 62. Effective Teaching Day Tracker

- System tracks: periods scheduled vs periods actually conducted per subject per class per term
- Deficit = scheduled periods − conducted periods; shown per subject
- Surplus: extra periods (catch-up, guest lecture same subject) add to conducted count
- Displayed on: teacher dashboard, HOD dashboard, Principal dashboard
- Alerts when any subject falls below 75% of scheduled periods (CBSE: minimum 75% lecture attendance for students; mirrored requirement for teachers)
- Data feeds Module 15 (Syllabus Builder) to show how much of planned syllabus was covered

---

## 63. Subject-Wise Period Utilization Report

- At end of term: total periods scheduled vs conducted per subject across all classes
- Exported as report: subject, teacher, class, scheduled periods, conducted periods, utilisation %
- Low-utilisation subjects (< 80%) flagged in red for Principal attention
- High-utilisation (catch-up done) shown in green
- Report available to HOD (department subjects), Principal (all subjects)

---

## 64. Teacher-Wise Utilisation Report

- Per teacher per month: total periods scheduled, conducted, substituted-out (given), substituted-in (taken), free periods
- Effective teaching percentage = conducted / (conducted + absent) × 100
- Report available to: teacher (self), HOD, Principal, Management
- Used in teacher appraisal (Module 08)
- Comparison across teachers in same subject / department for performance benchmarking

---

## 65. Room Utilization Heatmap

- Visual heatmap: rooms on Y-axis, time slots on X-axis, colour intensity = booking density
- Identifies heavily over-used rooms (candidates for new infrastructure investment)
- Identifies under-used rooms (can be repurposed or used for extra batches)
- Weekly and monthly views
- Data exported to Branch Management module (Module 06) for infrastructure planning

---

## 66. Timetable Compliance Dashboard

- Single view showing compliance status for:
  - CBSE period quotas per subject per class (green = compliant, red = below minimum)
  - UGC credit-hour allocation per course per department
  - NEP 2020 mandatory periods (yoga, value ed, life skills, PE, art)
  - State board norms (if state board institution)
  - Teacher load limits (within UGC/institution norms)
- Drill-down: click any red item to see which class / subject / teacher is non-compliant
- Must be all-green before timetable is approved for publication

---

## 67. Missing Timetable Alert

- 7 days before academic term start, system checks: every active class/section/batch has a published timetable
- If any section is missing a timetable: in-app alert to admin and Principal
- Alert escalates daily (7 days → 3 days → 1 day before term start) if not resolved
- Prevents students from arriving on day 1 with no class schedule

---

## 68. Teacher Overload Alert

- Before timetable is published: system checks all teacher period counts against max load for their staff category
- Overloaded teachers flagged with: teacher name, assigned periods, category maximum
- Timetable cannot be published with overloaded teachers without Principal explicit override + reason
- Underloaded teachers also flagged (below minimum) to ensure equitable work distribution

---

## 69. Timetable Change In-App Notification

- Any post-publication timetable change (period swap, teacher change, room change, cancellation) triggers:
  - In-app notification to affected students: "Your [subject] period on [day] has changed to [new details]"
  - In-app notification to affected teachers: "Your timetable has been updated"
- Notifications sent immediately on publish of revised timetable
- Students can view change history in their timetable screen (what changed and when)

---

## 70. Section Transfer Timetable Sync

- When a student transfers from Section A to Section B mid-term (Module 07):
  - Student's timetable automatically updates to Section B's timetable
  - Previous Section A timetable removed from student's view
  - Effective date of timetable change matches transfer effective date
  - In-app notification to student and parent (school level) confirming new timetable

---

## 71. NCC / NSS Slot Allocation

- NCC (National Cadet Corps) and NSS (National Service Scheme) are semi-mandatory in many Indian schools and colleges (under Ministry of Defence / Ministry of Youth Affairs directives)
- Dedicated period(s) per week allocated in timetable for NCC drill, NSS activities
- NCC / NSS periods marked as type "Co-Curricular Activity"; attendance tracked separately
- NCC / NSS officer (from staff) assigned to these periods; period diary maintained
- Certificates and participation records linked to Module 39 Certificates

---

## 72. Cultural / Co-Curricular Period

- Designated periods for music, fine arts, drama, dance, debate, quiz
- Treated as regular periods with attendance
- Subject teacher (music teacher, art teacher) assigned
- Graded in internal assessment if part of CBSE continuous assessment scheme
- Co-curricular achievements from these periods optionally linked to student profile (Module 07)

---

## 73. Physical Education & Yoga Period

- PT / PE periods assigned to ground / gymnasium with PE teacher
- Yoga period: minimum 1 per week (NEP 2020); yoga instructor or trained PE teacher assigned
- Adverse weather protocol: if ground unavailable (rain), system suggests indoor alternative room; PE teacher notified
- PT / yoga attendance tracked; students below 75% PT attendance flagged for health concern review

---

## 74. Work Experience / Vocational Period

- CBSE Secondary curriculum mandates work experience (Classes 6–10) and vocational subjects (Classes 11–12)
- Vocational subjects (CBSE Skill Education): each skill subject has theory + practical components
- Practical component requires workshop / lab room; scheduling handled same as lab practical with batch splitting if needed
- CBSE skill subject partners (industry partners) may conduct sessions; tracked as guest lectures under vocational subject

---

## 75. Life Skills / Career Counselling Period

- Scheduled slot for life skills, career awareness, personality development — especially Classes 9–12
- Linked to Module 32 Counselling & Student Welfare — counsellor uses this period for group sessions
- Topics logged in period diary; students cannot opt out of this period
- External career counsellor sessions treated as guest lectures under Life Skills subject

---

## 76. Library Period

- Dedicated library period allocated in timetable (1–2 per week for primary/middle school per CBSE activity guidelines)
- Room assignment = library; class teacher or librarian supervises
- Book issues, returns, and reading activity during library period logged in Module 30 Library Management
- Attendance tracked; students not attending library period without reason are flagged

---

## 77. ITI Trade-Specific Scheduling

- ITI timetable alternates theory and practical on a half-day basis:
  - Batch A: theory morning (8 AM–12 PM) + practical afternoon (12–4 PM)
  - Batch B: practical morning + theory afternoon
  - Alternation may be daily or weekly depending on trade
- Trade-specific workshop rooms: fitting shop, welding shop, COPA lab, electronics lab, plumbing workshop
- Trade instructor assigned both theory and practical sessions
- Practical sessions have a demonstrator / lab assistant in addition to trade instructor
- NCVT (National Council for Vocational Training) period norms apply: minimum workshop hours per trade per semester tracked

---

## 78. Teaching Assistant / Lab Demonstrator

- Junior staff (demonstrator, lab assistant, teaching assistant) assigned to assist in lab sessions alongside the primary subject teacher
- Teaching assistant's period count tracked separately; does not count toward their main teaching load
- Lab demonstrator responsible for equipment setup, safety compliance, student supervision
- Teaching assistant can be assigned to multiple lab sessions in a day (unlike primary teacher subject-assignment rules)

---

## 79. Special Educator Slot (CWSN)

- Resource teacher or special educator periods allocated for CWSN (Children with Special Needs) students
- Schedule may be individual (one-on-one pull-out sessions) or small-group (3–5 students)
- Special educator's timetable shows student names, not class/section (unlike regular teacher view)
- Sessions linked to each student's IEP (Individualised Education Plan) in Module 32 Counselling
- RTE Act 2009 compliance: free and appropriate education for CWSN students; session records support compliance audit

---

## 80. Bridge Course Scheduling

- Pre-academic-year bridge classes for newly admitted students (orientation, catch-up, foundational skills)
- Scheduled before regular timetable start date (during onboarding window)
- Bridge course has its own timetable (condensed, fewer subjects, orientation focus)
- Attendance tracked; does not count toward annual attendance percentage
- Transitions to regular timetable on the official academic year start date

---

## 81. Staggered Lunch / Break for Large Institutions

- Large schools (1,000+ students) stagger lunch breaks across sections to avoid overcrowding
- System assigns lunch slot times per class group (e.g., Classes 1–4: 11:00–11:30 AM; Classes 5–8: 11:30 AM–12:00 PM; Classes 9–12: 12:00–12:30 PM)
- Bell schedule reflects staggered breaks per class group
- Canteen / dining hall capacity constraint optionally configured; system warns if too many sections have overlapping lunch slots

---

## 82. Coaching Centre Sunday / Holiday Batch

- Coaching centres commonly run Sunday as a regular class day
- System supports any day of the week (Mon–Sun) as a batch day
- Holiday calendar for coaching batches is managed separately from school/college calendar
- A batch-level holiday (specific batch, specific date) does not affect other batches
- Students enrolled in Sunday batches see Sunday timetable entries in their schedule

---

## 83. Online / Hybrid Period Slot

- Post-NEP and post-COVID, some institutions run hybrid mode (some periods online, some in-person)
- Each timetable period can be marked: In-Person / Online / Hybrid
- Online periods: video link (from Module 45 Live Classes) embedded in timetable slot
- Attendance for online periods captured via live class join confirmation (Module 11)
- Institutions can configure default mode per subject or per class group

---

## 84. Timetable for Exam Centre (No Regular Timetable)

- Institutions registered as pure exam centres (no regular classes, only conduct board / competitive exams):
  - No regular class timetable module active
  - Only exam hall scheduling active (hall → date → session → exam → invigilator)
  - Hall availability calendar managed per exam season
  - Duty roster for exam staff generated per session
  - Linked to Module 19 Exam Session & Proctoring

---

## DB Schema (Core Tables)

```
institution.bell_schedules
  id, tenant_id, branch_id, academic_year_id, shift (morning/afternoon),
  wing (primary/secondary/sr_sec/all), created_by, approved_by, status

institution.bell_periods
  id, bell_schedule_id, slot_number, slot_name, start_time, end_time,
  type (lecture/lab/recess/lunch/pt/assembly/prayer/yoga/free/zero/extra)

institution.timetable_versions
  id, tenant_id, branch_id, academic_year_id, term_id, class_id, section_id,
  version_number, status (draft/hod_review/principal_review/published/archived),
  published_at, published_by, locked, created_at

institution.timetable_entries
  id, timetable_version_id, day_of_week (1–7), bell_period_id, subject_id,
  primary_teacher_id, secondary_teacher_id, room_id, entry_type
  (regular/lab/combined/elective/remedial/event/exam/substitution/free),
  is_double_period, double_with_entry_id, lab_batch (A/B/both), created_at

institution.timetable_subject_quotas
  id, tenant_id, board_type (cbse/ugc/state_mah/state_tn/state_up/custom),
  class_group, subject_id, min_periods_per_week, max_periods_per_week

institution.teacher_load_config
  id, tenant_id, staff_category, min_periods_per_week, max_periods_per_week,
  max_periods_per_day, source (ugc/cbse/institution)

institution.substitution_log
  id, tenant_id, branch_id, date, bell_period_id, original_teacher_id,
  substitute_teacher_id, subject_id, class_id, section_id,
  reason, assigned_by, assigned_at, status (pending/confirmed/completed)

institution.duty_roster
  id, tenant_id, branch_id, duty_type (gate/library/lab/ground/exam_invigilation/
  flying_squad/chief_superintendent/additional_superintendent/ncc/cultural),
  date, bell_period_id, staff_id, assigned_by, status

institution.period_diary
  id, timetable_entry_id, teacher_id, diary_date, status (conducted/absent/holiday/
  event/exam/substitution), topic_covered, textbook_pages, homework_given,
  next_topic, logged_at, overdue_flag

institution.timetable_templates
  id, tenant_id, branch_id, class_id, template_name, academic_year_ref,
  term_ref, created_by, created_at

institution.teacher_unavailability
  id, tenant_id, teacher_id, start_date, end_date, specific_periods (JSON array),
  reason, approved_by, status (pending/approved/rejected)

institution.timetable_audit_log
  id, timetable_version_id, changed_by, change_type, old_value (JSON),
  new_value (JSON), change_reason, changed_at

coaching.batch_schedules
  id, tenant_id, batch_id, day_of_week (1–7), start_time, end_time,
  room_id, teacher_id, is_online, video_link, effective_from, effective_to

coaching.batch_holidays
  id, tenant_id, batch_id, holiday_date, reason, declared_by, declared_at
```

---

## Integration Map

| Integrated Module | How |
|---|---|
| 05 — Academic Year & Calendar | Timetable tied to academic year, term; holidays block timetable |
| 06 — Branch & Campus Management | Rooms, labs, grounds allocated from branch room registry |
| 07 — Student Enrolment | Section assignment drives timetable view; elective choice drives parallel groups |
| 08 — Staff Management | Teacher assignments, load limits, unavailability, BGV-cleared staff only |
| 11 — Attendance (School & College) | Each timetable period generates an attendance slot |
| 15 — Syllabus & Curriculum Builder | Period diary feeds syllabus completion tracker |
| 18 — Exam Paper Builder | Exam timetable generated from exam paper schedule |
| 19 — Exam Session & Proctoring | Hall allocation, invigilator duty from exam duty roster |
| 21 — Results & Report Cards | Effective teaching days data used in term report |
| 29 — Transport | Field trip days trigger transport booking request |
| 30 — Library Management | Library periods generate library session records |
| 31 — Admission CRM | Demo/trial class slots for inquiry students |
| 32 — Counselling | Life skills periods, CWSN special educator slots |
| 33 — PTM | PTM day timetable modification |
| 35 — Notifications | All timetable publish / change notifications via in-app |
| 39 — Certificates | NCC/NSS participation periods linked to certificate records |
| 45 — Live Classes | Online/hybrid period slots linked to live class sessions |
