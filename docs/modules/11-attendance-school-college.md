# Module 11 — Attendance (School & College)

## Purpose
Define how EduForge captures, validates, manages, and reports student attendance for schools (CBSE and all state boards) and colleges (UGC/AICTE regulated), covering period-wise, subject-wise, and day-wise attendance — including Indian regulatory compliance, government portal submissions, special student categories, welfare triggers, and all edge-case scenarios specific to Indian educational institutions.

---

## 1. Attendance Model — School (Period-Wise)

- Every timetable period (from Module 10) generates an independent attendance slot
- Teacher assigned to that period marks each student: Present / Absent / Late / OD / Authorized / Medical
- Each period's attendance is stored as a separate record
- Day-level attendance is derived by aggregating period-level records:
  - Present all periods = Full Day Present
  - Present ≥ 50% of periods = Half Day Present
  - Present < 50% of periods = Half Day Absent
  - Absent all periods = Full Day Absent
- Period-wise data is the authoritative record; day-level is a computed summary

---

## 2. Attendance Model — College (Lecture / Tutorial / Lab Wise)

- Each lecture slot, tutorial session, and lab practical batch generates a separate attendance entry
- Subject-wise cumulative attendance calculated independently for each course
- A student may be above 75% overall but below 75% in one subject — subject-wise tracking is authoritative for exam eligibility
- Tutorial sessions counted toward the subject's total; lab hours counted separately (as per UGC credit-hour norms)
- Department-wise rollup available for HOD review

---

## 3. Morning Assembly / Prayer Roll Call

- First attendance of the day taken during morning assembly / prayer period
- Marked by class teacher as: Present / Absent / Late
- Separate from subject-period attendance; does not count toward subject-wise percentage
- Used for: early absentee detection, day-level flag, parent notification trigger
- Schools without assembly can disable this in institution config; system defaults to first period class teacher roll call

---

## 4. First Period Class Teacher Roll Call

- Class teacher takes overall day-level roll call at start of first period
- Early identification of absentees before subject teacher marking begins
- Flagged absentees trigger: parent in-app notification (within 30 min of period start) for school-level students
- Roll call logged separately; used for daily absentee list generation

---

## 5. Half-Day Attendance Model

- Some state board schools track morning session (Periods 1–4) and afternoon session (Periods 5–8) as separate half-day units
- Each half = 0.5 attendance unit
- Student present for full morning but absent for afternoon = 0.5 present, 0.5 absent
- Half-day model enabled/disabled per institution config
- Useful for institutions where students are formally released at noon on specific days

---

## 6. In-App Marking by Teacher

- Teacher opens their personal timetable view → selects active period → marks each student
- Default mark: Present (teacher changes to Absent / Late / OD / etc. for exceptions)
- Bulk-mark all present, then mark exceptions (faster for large classes)
- Voice-assisted marking option: teacher calls roll; app confirms taps
- Marking interface shows: student name, photo, roll number, previous day's attendance status (quick context)

---

## 7. Biometric Attendance — Gate Entry

- Fingerprint reader at school gate captures entry and exit timestamps
- Gate entry ≠ period attendance — both systems maintained independently
- Gate biometric used as: anomaly cross-reference (student marked present in period but no gate entry that day is flagged)
- Exit timestamp used for early dismissal tracking
- Biometric device linked to branch; data stored under `institution.biometric_logs`
- Biometric enrollment done at student onboarding (Module 07)

---

## 8. RFID Card Tap Attendance

- Student taps RFID card on reader at classroom door or entry point
- Attendance auto-marked as Present for that period
- RFID card issued at enrolment; lost card reported to admin; new card issued with same student ID
- RFID reader installed at classroom level (period-wise) or at entry gate (day-wise)
- If RFID reader unavailable (power/technical issue), teacher falls back to in-app marking

---

## 9. Face Recognition at Classroom

- Camera at classroom door automatically recognises enrolled students as they enter the room
- Attendance auto-marked as Present for the period on recognition
- Unrecognised face logged as anomaly alert
- Optional — institution-level config; disabled by default (DPDPA 2023 biometric data consent required before activation)
- Face recognition data processed on-device or on-premise; not sent to cloud without consent

---

## 10. QR Code Session Attendance

- Teacher generates a time-limited QR code for the current period via their app
- QR code displayed on classroom projector/screen or shared as in-app prompt to students
- Students scan QR code on their device within the window → marked Present
- QR code expires after configurable window (default: 10 minutes from period start)
- QR is unique per period per section per day — cannot be reused across periods or by students not enrolled in that section
- Prevents proxy attendance from outside classroom
- Students who did not scan within window can be manually corrected by teacher within 24 hours

---

## 11. Manual Fallback Register

- If digital system unavailable (power outage, network failure, device damage):
  - Teacher marks paper register (provided as printable template per class)
  - Admin or teacher enters data into system within 24 hours with "Offline Entry" flag
  - Correction audit trail notes: date of offline entry, reason, entered by
- Paper registers retained physically for CBSE inspection (minimum 1 academic year)
- Common in rural/government schools with unreliable connectivity

---

## 12. Attendance Marking Window

- Teacher must mark attendance within the period duration
- 15-minute grace window after period ends for late marking
- Beyond grace: system locks the period for teacher self-entry
- Locked period requires HOD approval to mark (HOD approval unlocks for that teacher + period only)
- Persistent missed marking (> 3 periods/week) triggers HOD alert
- End-of-day: all unmarked periods visible on admin dashboard as red flags

---

## 13. Late Arrival Handling

| Arrival Time | Status |
|---|---|
| Within grace period (configurable: 5–10 min after bell) | Present |
| After grace period but within first half of period | Late |
| After half the period has elapsed | Half-period absent (0.5) |
| After 75% of period elapsed | Absent for that period |

- Grace period configured per institution (some strict schools: 0 minutes; some lenient: 15 minutes)
- Late marks accumulate: 3 late marks in a month = 1 absent equivalent (institution config)
- Late arrival logged with timestamp; visible in student attendance history

---

## 14. Early Dismissal

- Student leaves before end of school day (medical emergency, family emergency, scheduled appointment)
- Admin or class teacher records: student name, departure time, reason, authorised by (parent / admin)
- Periods attended before departure = Present; periods after departure = Authorised Early Dismissal (not counted as absent)
- Parent confirmation required for early dismissal (parent must call or appear in person; recorded in log)
- Exit via biometric gate logged; cross-referenced with dismissal record

---

## 15. Medical Leave During School Hours

- Student falls ill during school hours (nurse assessment or teacher observation)
- Nurse / admin marks student as "Medically Excused" from specific periods
- Periods before medical dismissal = Present; periods after = Medical Absent (excluded from absence count)
- Parent notified in-app immediately with student's condition and dismissal time
- Medical visit record created in student health log; feeds into Module 32 Counselling if chronic pattern detected

---

## 16. Proxy Attendance Prevention — Biometric Cross-Reference

- System runs daily reconciliation: students marked present by teacher but with no biometric gate entry that day
- Flagged as anomaly; HOD receives list of anomalies next morning
- Teacher must confirm or correct each anomaly within 24 hours (genuine late entry, biometric failure, etc.)
- Unresolved anomalies escalate to Principal after 48 hours
- Anomaly count per teacher tracked; persistent high anomaly rate = investigation trigger

---

## 17. QR Code Proxy Prevention

- QR code is time-bound (expires after marking window)
- QR code is session-specific: contains encrypted period ID + section ID + timestamp
- A student cannot scan QR code from outside the classroom after the window closes
- System detects duplicate scans from same device (student ID)
- QR code cannot be forwarded — scanning from a screenshot of another student's screen is detected by device fingerprint check

---

## 18. Random Student Spot Verification

- After QR / RFID marking, app randomly selects 2–3 students per period
- Teacher prompted: "Verbally confirm student [Name] is present"
- Teacher confirms (Yes) or corrects (No → marks absent)
- Spot verification log maintained; used as audit evidence during CBSE inspection or internal audit
- Frequency configurable: every period, alternate periods, or random (default: 1 in 3 periods)

---

## 19. CBSE 75% Attendance Rule

- CBSE Circular (Exam Unit): student must have minimum 75% attendance in the academic year to be eligible for CBSE board examination (Classes 10 and 12)
- For Class 11 / 12 Sr. Secondary: subject-wise 75% in each subject individually
- System enforces as hard block at exam registration (Module 19): student below 75% cannot register
- Condonation process available (Points 33–36) to lift the block
- CBSE allows medical condonation up to 25% of working days (i.e., student can have up to 25% medical absence and still be eligible with condonation)

---

## 20. State Board Attendance Thresholds

| State Board | Minimum Attendance |
|---|---|
| Kerala HSE / SSLC | 85% |
| Tamil Nadu State Board | 80% |
| Karnataka SSLC / PU | 75% |
| Maharashtra SSC / HSC | 75% |
| UP Board (Madhyamik / Inter) | 75% |
| Rajasthan Board | 75% |
| West Bengal Board | 80% |
| Gujarat Board (GSEB) | 75% |
| Andhra / Telangana (BSEAP / BSETS) | 75% |
| Bihar Board (BSEB) | 75% |

- Threshold stored per affiliated board (set at institution onboarding, Module 04)
- Custom threshold configurable for institutions with board dispensation (Principal confirms, logged)
- Threshold applies for both exam eligibility and scholarship compliance

---

## 21. UGC 75% Mandatory — College

- UGC Regulations 2018: minimum 75% attendance per subject per semester mandatory for all UG / PG students
- Subject-wise tracking is authoritative — student below 75% in any one subject is blocked from that subject's semester exam
- HOD can recommend condonation for medical / OD reasons; Dean / Principal approves
- Medical condonation: up to 10% (effective minimum 65% with medical)
- Overall attendance also calculated but subject-wise is the enforcement criterion

---

## 22. AICTE Engineering College Attendance

- AICTE Approval Process Handbook: minimum 75% attendance per subject per semester for all technical programmes (B.Tech, B.E., Diploma, Pharmacy, MBA, MCA)
- Lab attendance and theory attendance tracked separately per AICTE norms
- Below 75% in theory OR lab = blocked from semester exam for that course
- AICTE also mandates attendance display on notice board at end of each month; system generates printable class-wise subject attendance sheet for notice board

---

## 23. No Detention Policy — RTE Act (Classes 1–8)

- Right to Education Act 2009, Section 16: no student shall be held back in any class or expelled from school till completion of elementary education (Class 8)
- Attendance tracked and reported for all classes including 1–8
- Attendance data used for: parent communication, government reporting, scholarship compliance
- System never uses attendance as a detention criterion for Classes 1–8; hard-coded rule
- Attendance shortage in Classes 1–8 triggers parent counselling (Module 32) but not retention action
- Detention eligibility (Classes 9+) described in Point 59

---

## 24. Authorized Absent

- Parent submits advance leave application (Point 66) and class teacher approves
- Status = "Authorized Absent" (AA)
- Counts as absent in percentage calculation (AA is still an absence)
- Does NOT trigger parent surprise notification (parent already aware)
- Visible in attendance history with "Authorized" tag and reason
- Appears in reports as a separate column (Authorized vs Unauthorized absence count)

---

## 25. Unauthorized Absent

- Student absent without prior leave application or parent communication
- In-app notification sent to parent within 30 minutes of first absent period (morning period or assembly roll call)
- Notification content: "Your child [Name] has not attended school today. Please contact the class teacher if there is an issue."
- Consecutive unauthorized absence triggers escalating alerts (Point 44)
- Used in chronic absenteeism tracking and counsellor referral (Point 89)

---

## 26. On Duty (OD) — College

- College-specific status for student on authorized institutional duty:
  - Industrial visit / field trip
  - NCC camp / NSS special camp
  - Sports tournament (representing institution)
  - Paper presentation at conference
  - Government-assigned duty (election, census)
  - Inter-college cultural / technical competition
- OD status: counted as Present in subject attendance per UGC convention
- OD must be pre-approved by HOD; evidence (selection letter, participation certificate) uploaded
- OD periods are not condonation — they count as present without deduction

---

## 27. Medical Absent

- Student absent due to illness with medical certificate
- Parent uploads medical certificate via app within 3 days of return
- Class teacher / HOD verifies certificate (authenticity check: doctor name, registration number, date)
- Marked "Medical Absent" — eligible for condonation process
- Medical certificate stored in student health record (Module 07)
- Fake certificate flag: if pattern of monthly 1–2 day medical absences without valid certificates detected, flagged to Principal

---

## 28. NCC / NSS Duty Absence

- Student attending NCC Annual Training Camp, NCC Republic Day Camp, NSS Special Camp, or national-level NCC/NSS event
- Absence pre-approved by Principal (Module 08 duty log)
- Attendance status: "NCC/NSS Duty" — counted as present per Ministry of Defence / Ministry of Youth Affairs guidelines
- Camp attendance certificate submitted on return; stored in student record
- Achievement records linked to Module 39 Certificates (NCC B/C Certificate, NSS certificate)

---

## 29. Sports / Cultural Representation Absence

- Student representing institution/district/state/nation in sports, cultural, or academic competition
- Status: "Sports/Cultural Duty" — counted as OD/Present in school attendance
- Selection letter and participation/achievement certificate uploaded on return
- CBSE allows condonation for such absences (up to 5% additional on top of medical condonation)
- State board rules vary; system applies state-specific condonation rule based on affiliated board

---

## 30. Calamity / Force Majeure Absence

- School closed or inaccessible due to floods, cyclone, earthquake, epidemic, riot, or national emergency
- Admin marks period/day as "Calamity Holiday" with reference to government order / news source
- All students for that day = Calamity Holiday — not counted as absent
- If school was open but certain students could not reach (localized flooding, road blockage):
  - Admin can apply calamity exemption to specific students (by area/address) for those days
  - EduForge super-admin can issue platform-level condonation during national emergencies (e.g., COVID-19 type scenarios)

---

## 31. Attendance Shortage Warning Levels

| Attendance % | Action |
|---|---|
| 90–100% | No action; shown in green |
| 80–89% | Advisory in-app notification to student: "Your attendance is at [%]. Please maintain regularity." |
| 75–79% | Formal in-app warning to student + parent: "Attendance below 80%. Risk of shortage." |
| 70–74% | Shortage warning letter (PDF) generated; parent called in for meeting |
| < 75% | Exam eligibility blocked; condonation application window opens |
| < 65% | Condonation unlikely; management review; may be detained (Class 9+) |

- Warning notifications sent to student + parent (school level)
- For colleges: same levels applied subject-wise + overall
- All warnings logged with timestamp; used in shortage notice PDF

---

## 32. Subject-Wise Shortage List — College

- Before each internal exam and end-semester exam registration:
  - System generates: list of all students below threshold (75%) in each subject
  - Report shared with HOD; HOD shares with subject faculty
  - Students on list notified individually in-app
- Shortage list includes: student name, roll number, total classes held, classes attended, attendance %, shortage in number of classes to reach 75%
- HOD submits shortage list to Dean/Principal for condonation review

---

## 33. Medical Condonation Process

```
Student / Parent submits condonation application (in-app)
  → Uploads medical certificate (doctor name, reg. no., hospital, dates)
  → Class Teacher / Subject Faculty verifies certificate authenticity
  → HOD recommends (approve / reject with reason)
  → Principal approves (for up to 15% of working days)
  → Management approves (beyond 15%)
  → Condonation recorded; effective attendance recalculated
  → Student notified in-app with updated eligibility status
```

- CBSE: up to 25% of working days can be condoned with medical grounds (10% routine medical + 15% for hospitalisation + surgery)
- State boards: thresholds vary — system applies board-specific rules
- Medical condonation cannot be applied for the same period twice

---

## 34. Sports / Cultural Condonation

- Additional condonation on top of medical: up to 5% of working days for inter-institution/state/national representation
- Evidence mandatory: selection letter (from school/sports authority) + participation certificate
- HOD verifies event is on approved list (CBSE/state board recognized competitions)
- Approved automatically if student represented institution at state or national level
- Logged separately from medical condonation; cumulative totals tracked

---

## 35. Calamity Condonation

- For government-declared calamity days: automatic condonation — no application needed
- For partial calamity (localized impact): admin marks affected students; Principal approves
- Platform-level condonation (e.g., COVID-19 extended school closure): EduForge super-admin issues blanket condonation across all tenants for specified date range; individual institution Principals confirm application
- All calamity condonations logged with government order reference

---

## 36. Condonation Authority Levels

| Condonation Up To | Authority |
|---|---|
| Advisory only | Class Teacher |
| Up to 5% of working days | HOD |
| Up to 15% of working days | Principal |
| Beyond 15% | Management (Group/Trust level) |
| Platform-wide calamity | EduForge Super-Admin + Principal confirmation |

- All condonations logged: who approved, date, reason, percentage condoned
- Condonation cannot exceed board-prescribed maximum (CBSE: medical up to 25%; beyond is ineligible regardless)
- Condonation history visible to Principal and auditors; not visible to students/parents (only final effective % shown)

---

## 37. Post-Condonation Recalculation

- After condonation approved:
  - System removes condoned absences from denominator (for medical) or converts to present (for OD/NCC/sports)
  - Effective attendance % recalculated for each subject (college) or overall (school)
  - Exam eligibility status updated: blocked → eligible (if above threshold after recalculation)
  - Student and parent notified in-app: "Condonation approved. Your updated attendance is [%]. Exam eligibility: [Eligible / Still Ineligible]"
- If after condonation student is still below threshold: additional condonation application can be submitted (subject to board maximum)

---

## 38. Attendance Shortage Notice — PDF Letter

System generates formal shortage notice letter:
- Student name, class/section, roll number, admission number
- Subject-wise attendance table (for college) or overall (for school): total working days, days present, days absent, % attendance
- Subjects/overall below threshold highlighted in red
- Condonation eligibility (eligible / not eligible) with application deadline
- Principal signature (digital/e-sign via Module 39)
- Institution letterhead, logo, date
- Sent to parent in-app as downloadable PDF; physical copy dispatch option

---

## 39. Attendance Correction — Self (Within 24 Hours)

- Teacher can correct an error within 24 hours of marking
- Correction logged: original value, corrected value, corrected by, timestamp, reason (free text)
- No approval needed for within-24-hour self-correction
- If correcting from absent → present (upgrade): biometric entry cross-check runs; if no gate entry, anomaly flag raised alongside correction

---

## 40. HOD-Approved Correction (24–48 Hours)

- Corrections between 24 and 48 hours after marking require HOD approval
- Teacher submits correction request: student name, period, date, original status, requested status, reason
- HOD approves or rejects in-app
- Approved corrections logged with HOD's name + timestamp

---

## 41. Principal-Approved Backdated Correction (Beyond 48 Hours)

- Beyond 48 hours: requires Principal approval
- Principal reviews: reason for late correction, original teacher's justification, supporting evidence
- Maximum backdating window: configurable (default: 5 working days from event date)
- Beyond 5 working days: Management approval required (anti-manipulation safeguard)
- All backdated corrections visible in audit report for CBSE inspection

---

## 42. Soft Lock After Term End

- Once academic term ends:
  - Attendance for that term is soft-locked automatically
  - No teacher or HOD can modify locked records
  - Corrections require: Principal + Management joint approval with documented reason
- Prevents retrospective manipulation of attendance before board exam eligibility submission
- Locked records remain readable; only write access is restricted

---

## 43. Absent Notification to Parent

- School-level only (college students and coaching students: no parent notification as per platform rules)
- Trigger: student absent in Period 1 (or assembly roll call)
- Notification sent within 30 minutes of period start
- Content: "Dear [Parent], [Student Name] has not attended school today ([Date]). Please contact the class teacher [Teacher Name] if you need to inform about the absence."
- No notification if leave is pre-approved (authorized absent)
- Daily notification cap: 1 per day per student (not repeated for every absent period)

---

## 44. Consecutive Absence Alert

| Duration | Action |
|---|---|
| 3 consecutive days absent | Alert to class teacher + counsellor (Module 32); counsellor to contact parent |
| 5 consecutive days absent, no parent response | Welfare check trigger (Point 89); POCSO committee notified |
| 7 consecutive days absent | Management notified; welfare officer visits student's home; emergency contact called |
| 15+ days absent (no medical leave) | Academic re-integration plan created; possible TC / dropout prevention process |

---

## 45. Mass Absence Anomaly Alert

- If > 50% of a section absent on a day without a declared holiday:
  - Immediate alert to admin and Principal
  - Possible causes: unreported holiday, teacher absent and students sent home, local event, transport failure
  - Admin must acknowledge and provide reason within 2 hours
  - If no acknowledgement: auto-escalation to Management
- Threshold configurable (default: 50% of section)

---

## 46. Teacher Marking Compliance Alert

- 30 minutes after period end: if teacher has not marked attendance, in-app alert to HOD
- End of school day: list of all unmarked periods sent to Principal
- Monthly report: per teacher — periods marked on time vs late vs missed
- Consistent missed marking (> 5 periods/month): note added to teacher's service record (Module 08)
- Input to teacher appraisal cycle (Module 08 Point 95)

---

## 47. Exam Eligibility Warning — Advance Notice

- 4 weeks before exam registration opens (Module 19):
  - System scans all students' subject-wise attendance
  - Students at 76–84% (near the threshold): advance in-app warning to student + parent
  - Message: "Your attendance in [Subject] is currently [%]. You need [N more classes] to be safe above 75% before exams."
- Students at 75–76% flagged as borderline — counsellor assigned for monitoring
- Students already below 75%: condonation application window pre-opened with instructions

---

## 48. Daily Attendance Summary — End of Day

- Auto-generated at end of each school day:
  - Class-wise: total students, present, absent, late, authorized absent
  - School-wide totals
  - Visible to: admin, Principal, Vice-Principal on dashboard
- Highlights: classes with unusually high absence, teachers with unmarked periods, new consecutive absence flags
- No manual trigger needed — runs automatically at configured end-of-day time

---

## 49. Monthly Attendance Report

- Generated on last working day of each month
- Per student: total working days in month, days present, days absent, late count, authorized absences, current attendance %
- College: subject-wise breakdown per student per month
- Class-wise summary: average attendance %, top 5 absentees list
- Reports visible to: class teacher, HOD (department), Principal, management
- Downloadable PDF + exportable CSV

---

## 50. Term Attendance Register — PDF

- Cumulative attendance for the term per student
- CBSE-prescribed format: columns for each working day, present/absent marks, monthly totals, term total, percentage
- Signed (digitally) by class teacher and Principal
- Stored in student records (Module 40 Document Management)
- Physical printout generated for CBSE inspection compliance
- State board format variants supported (Maharashtra, TN, Karnataka formats configurable)

---

## 51. Annual Attendance Summary

- Full academic year: per student, per subject (college) — total working days, present, absent, attendance %
- School: single overall percentage per student
- Required for: mark sheet compilation (Module 21), TC attendance entry (Module 07), CBSE board submission
- Generated at academic year close; immutable after lock
- Archived for 5 years per CBSE retention requirement (Point 52)

---

## 52. CBSE 5-Year Attendance Record Retention

- CBSE affiliation norms: attendance records retained for minimum 5 years
- Records stored in DB with read-only flag after each academic year closes
- Deletion or modification of records beyond 5-year mark requires EduForge super-admin action
- Records queryable by: student name, admission number, academic year, class
- Physical register PDF archives stored in Module 40 Document Management with the same 5-year policy

---

## 53. Attendance Percentage on Report Card

- CBSE/State board report cards mandate attendance percentage display
- Auto-filled from attendance module into Module 21 Results & Report Cards
- College: subject-wise attendance % included in internal marks sheet
- Attendance column: "Total Working Days: [X] | Days Present: [Y] | Attendance: [Z%]"
- If below minimum: report card shows attendance in red with note "Below Required Attendance"

---

## 54. Exam Registration Hard Block

- At exam registration (Module 19):
  - System checks each registering student against applicable attendance threshold (CBSE 75%, state board threshold, UGC 75%)
  - For college: checked subject-by-subject
  - Students below threshold: registration blocked for specific subject / overall
  - Block message: "Registration blocked for [Subject]. Current attendance: [%]. Required: 75%. Apply for condonation to proceed."
  - Condonation-approved students: block lifted automatically on approval

---

## 55. Subject-Wise Shortage List — Pre-Exam

- 2 weeks before exam registration:
  - System auto-generates subject-wise shortage list
  - College: per department, per subject — list of students below 75%
  - School: overall list of students below board threshold
  - Shared with: subject faculty, HOD, Principal, Dean (college)
  - Students on list receive in-app notification with their shortage details and condonation instructions
- AICTE requirement: displayed on department notice board; system generates printable PDF version

---

## 56. Physical Attendance Register PDF Export

- Generates attendance register in physical register format (landscape, day-wise columns)
- CBSE-prescribed layout: student serial number, name, admission number, month-wise daily attendance, monthly total
- State board variants: Maharashtra, TN, UP format registers supported
- Signed PDF export with class teacher and Principal e-signatures
- For CBSE inspection: exported and printed, maintained alongside digital records

---

## 57. Attendance Freeze Before Board Submission

- 4 weeks before CBSE board exam date:
  - Class 10 and Class 12 attendance automatically frozen
  - No corrections allowed except by Principal with documented reason
  - Freeze notification sent to all class teachers and HODs
- Data prepared for CBSE online submission: student roll number, total working days, days attended, subject-wise (Sr. Secondary)
- Submitted via CBSE portal (manual upload); EduForge generates submission-ready format

---

## 58. CBSE Attendance Submission Format

- CBSE-prescribed columns: student roll number, exam roll number (if assigned), total working days, days attended, % attendance
- Sr. Secondary: subject-wise total and attendance per subject
- Exported as: PDF (for physical records) + CSV/Excel (for CBSE online portal upload)
- Batch export: all classes in one file
- Submission logged with date and uploaded-by name; stored in compliance records

---

## 59. Detention Eligibility Flag (Class 9+)

- At end of academic year, system flags students who:
  - Are in Class 9 or above (RTE no-detention does not apply)
  - Have attendance below institution-configured threshold (e.g., below 75%)
  - AND / OR have academic performance below passing threshold (from Module 21)
- Flagged students listed for Principal's review
- Principal confirms detention or grant of grace based on individual circumstances
- Confirmed detentions feed into Module 07 Promotion & Detention workflow
- Parents notified formally via attendance shortage notice + academic performance letter

---

## 60. Lab Batch Attendance (A / B Split)

- Lab sessions have Batch A and Batch B (as per Module 10 batch splitting)
- Separate attendance taken for Batch A session and Batch B session
- Both lab attendance entries counted toward subject-wise attendance:
  - Theory periods + lab periods = total subject hours
  - Subject attendance % = (theory present + lab present) / (total theory + total lab hours)
- AICTE engineering: lab attendance tracked separately; below threshold in lab = blocked from practical exam
- Lab batch assignment stored in student profile; can be changed by admin with HOD approval

---

## 61. Remedial Class Attendance

- Attendance tracked for all remedial / extra classes (scheduled via Module 10 Point 32)
- Institution config: whether remedial periods count toward subject attendance total
  - Option A: Yes, count toward subject % (encourages attendance in remedials)
  - Option B: No, tracked separately for teacher load only (default for most schools)
- Remedial attendance visible to: teacher, HOD, counsellor
- Student with persistent remedial absences flagged to counsellor (dropout risk)

---

## 62. Online / Hybrid Period Attendance

- For hybrid institutions (some periods online, some in-person):
  - Online period: attendance auto-captured from Module 45 Live Classes join confirmation
  - Student joins live class = Present for that period
  - Student absent from live class = Absent; subject to same rules as in-person absence
- Manual fallback: teacher can override if student had documented connectivity issue (within 24 hours)
- HOD approves connectivity-related corrections beyond 24 hours
- Online attendance and in-person attendance treated identically for percentage calculation

---

## 63. Advance Leave Application

- Parent submits leave application via app before the absence:
  - Date(s) of absence, reason, type (medical / personal / family / emergency)
  - Class teacher receives in-app notification; approves or rejects
  - Approved: dates marked as "Authorized Absent" in advance
  - Rejected: parent notified; if student still absent = unauthorized absent
- Admin can submit on parent's behalf (for parents with low digital access)
- Leave application archived in student record

---

## 64. Retroactive Leave Application

- Student was absent; parent applies for leave within 2 working days of return
- Application submitted with reason; class teacher reviews
- If approved: absence converted from "Unauthorized" to "Authorized Absent"
- Window strictly enforced: beyond 2 working days, leave cannot be applied retroactively (prevents backdated excuse fabrication)
- Exception: medical certificate submitted late (doctor note backdated); class teacher + HOD jointly approve
- All retroactive conversions logged in audit trail

---

## 65. Medical Certificate Upload

- For medical absence of 3 or more consecutive days: medical certificate mandatory
- Parent uploads certificate via app (photo/scan): doctor name, registration number, hospital/clinic, diagnosis (optional), period of rest recommended
- Class teacher verifies certificate within 2 working days of receipt
- Verified certificate stored in student health record (Module 07)
- System checks: doctor registration number format (MCI/State Medical Council number pattern); flags clearly invalid entries
- Certificates used in condonation application (Points 33–36)

---

## 66. Student Leave Balance

- Institution can allocate a fixed number of casual leaves per term per student (e.g., 5 CL/term)
- Leave balance tracked: applied leaves, approved leaves, remaining balance
- Student / parent sees remaining balance in app
- Excess casual leaves: treated as unauthorized absent even if parent applies
- Leave balance resets at start of each term
- Some institutions (particularly residential schools) use this to manage planned absences for family events

---

## 67. Rain Holiday / District Collector Order Holiday

- District Collector (DC) or state government declares school holiday:
  - Heavy rain, cyclone, flood, heatwave, epidemic control
  - Admin manually enters: DC order number or government notification reference, date(s), reason
  - System bulk-converts all student records for those days to "Government Holiday" — not absent
- If declaration arrives after some students already came to school:
  - Students already marked present = remain present
  - Students not yet marked = holiday
- Government holiday never reduces a student's attendance percentage

---

## 68. Bandh / Hartaal Partial Day

- School forced to close mid-day due to local bandh, protest, or emergency:
  - Admin marks: closure time, reason
  - Periods before closure: attendance as marked by teachers (present/absent)
  - Periods after closure: system marks all students as "Holiday" for those periods
- Students present for morning session but school closes at noon: morning periods = as marked; afternoon = holiday
- Admin records government/police advisory reference if available

---

## 69. Election Day Polling Booth Holiday

- School building designated as polling booth by Election Commission:
  - School declares holiday; admin marks as "Election Holiday"
  - All students = holiday for that day
  - Staff may be required for election duty (tracked in Module 08 leave)
- If school building not used but school declares precautionary holiday: marked as "Institution Holiday"
- Polling booth holidays coordinated with Election Commission notice; reference number stored

---

## 70. Republic Day / Independence Day Attendance

- School opens for flag hoisting ceremony (typically 1–2 hours; 8–9 AM):
  - Attendance taken during flag hoisting assembly: Present / Absent
  - Stored as "National Event Attendance" (separate category)
  - Regular period attendance not taken — no academic periods on these days
  - Students who attended flag hoisting = Present for national event; does not affect regular period attendance %
- Cultural programme rehearsals before these dates handled via Module 10 (Point 34)

---

## 71. Internal Exam Day Attendance Model

- On internal exam day (unit test, mid-term, terminal):
  - Students appearing in exam = Present for that exam period (subject-wise, per exam they are writing)
  - Regular period-wise attendance not taken for appearing students during exam hours
  - Students of other classes not writing exam: follow normal timetable and regular attendance
- Exam presence recorded in Module 19 Exam Session; feeds into subject-wise attendance total
- Absent from exam = Absent for that subject's period; medical certificate required for make-up eligibility

---

## 72. Study Tour / Educational Trip Attendance

- Multi-day trips away from school (science tour, heritage trip, industrial visit):
  - Accompanying teacher marks daily attendance for all trip participants each day
  - Trip day attendance = Present in school records (as OD / Trip category)
  - Non-participating students at school follow regular attendance
- Trip attendance logged under trip record with trip details (destination, date, teacher-in-charge)
- Linked to Module 29 Transport for bus booking
- Trip attendance counts toward subject percentage (institution config)

---

## 73. Attendance Certificate Generation

Student requests an official attendance certificate for:
- NSP scholarship renewal
- Bank educational loan application
- Bonafide certificate for passport / visa
- College leaving / TC requirement
- Court / legal requirement

Certificate includes:
- Student name, roll number, admission number, class, academic year
- Attendance % (overall + subject-wise for college)
- Period (from date to date)
- Institution name, UDISE code / affiliation number
- Principal's digital signature and institution seal
- Generated by Python; downloadable PDF; logged in student document records

---

## 74. National Scholarship Portal (NSP) Compliance

- Students receiving NSP scholarships (Pre-Matric, Post-Matric, Merit-cum-Means) must maintain minimum 75% attendance for scholarship renewal
- System tracks NSP scholarship holders (flagged at fee management / scholarship module)
- 30 days before NSP renewal deadline: system alerts admin of students with attendance < 75%
- NSP-format attendance certificate auto-generated for each eligible student
- Rejected cases (below 75%) flagged; HOD/Principal contacted for condonation or explanation
- NSP data cross-references DPDPA consent (student/parent consented to scholarship data sharing)

---

## 75. AISHE Annual Data Feed — College

- AISHE (All India Survey on Higher Education): Ministry of Education mandatory annual survey
- Data required: enrolled students by gender/category, attendance data, pass percentage
- System generates AISHE-compatible export at academic year end:
  - Institution code, course-wise enrollment, average attendance %, subject-wise data
- Export format: AISHE portal-compatible CSV / Excel
- Generated by Principal or IQAC coordinator; logged in compliance records

---

## 76. NAAC Attendance Documentation

- NAAC Criterion 2.6 (Student Performance and Learning Outcomes) and Criterion 2.4 (Teacher Quality) include attendance monitoring as an assessed metric
- System generates NAAC-format reports:
  - Student attendance % distribution (>90%, 75–90%, <75% — year-wise)
  - Attendance monitoring mechanism description
  - Action taken on shortage cases (counselling, shortage notices, condonation)
- Reports exported as PDF for NAAC Self Study Report (SSR) documentation
- NAAC peer team can verify by reviewing attendance records during on-site visit

---

## 77. U-DISE+ Data Export

- U-DISE+ (Unified District Information System for Education Plus): Ministry of Education portal for government and aided schools
- Schools must update attendance and enrolment data on U-DISE+ portal periodically
- EduForge generates U-DISE+ compatible export:
  - Class-wise enrolment by gender, caste category
  - Monthly/annual attendance data
  - Dropout data
- Export as U-DISE-prescribed format (CSV/Excel); admin uploads manually to portal
- Data reconciles with U-DISE enrolment numbers entered at student onboarding (UDISE Student ID, Module 07)

---

## 78. Shala Darpan / State Portal Integration

- State-specific school management portals used by government and government-aided schools:

| State | Portal |
|---|---|
| Rajasthan | Shala Darpan |
| Madhya Pradesh | Shiksha Portal |
| Maharashtra | Saral / MahaShala |
| Uttar Pradesh | UP PRERNA / Manav Sampada |
| Delhi | Delhi DoE Portal |
| Andhra Pradesh | School Education AP Portal |

- EduForge generates state-prescribed format export for each portal
- Admin downloads export and uploads to respective portal (manual process initially; API integration future)
- Export frequency: daily / weekly / monthly as required by state

---

## 79. DEO / BEO Monthly Submission

- Some states require monthly attendance reports submitted to District Education Officer (DEO) or Block Education Officer (BEO)
- Report format: class-wise enrollment, working days, average attendance %, absentee list
- Python generates state-prescribed format (varies by state)
- Admin downloads PDF + CSV; physically submits or emails to DEO/BEO office
- Submission log maintained (date submitted, submitted by, reference number)
- States with online DEO portals: export formatted for portal upload

---

## 80. RTE EWS / DG Student Attendance Monitoring

- Students admitted under RTE 25% quota (EWS and Disabled/DG categories) require special monitoring:
  - If attendance drops below 60% for 2 consecutive months: alert to admin and RTE nodal officer
  - Social worker / counsellor (Module 32) assigned to follow up
  - Parents contacted; home visit arranged if no response
- RTE-specific attendance report generated quarterly for state education department
- Low-attendance EWS students: school cannot withhold seat without formal notice and hearing (RTE Act protections)

---

## 81. Scholarship Attendance Monitoring

- State and central government scholarships requiring attendance compliance:
  - Pre-Matric Scholarship (SC/ST/OBC/Minority)
  - Post-Matric Scholarship
  - National Merit Scholarship
  - State merit scholarships (varies by state)
- System flags scholarship holders with attendance < 75% four weeks before renewal deadline
- Auto-generates scholarship-specific attendance certificate for each eligible student
- Non-eligible (below 75%) students receive alert with condonation instructions

---

## 82. Offline Attendance Marking with Sync

- Teacher can mark attendance in offline mode (no internet connectivity):
  - Device stores attendance data locally with timestamp
  - Auto-syncs when connection restored (next time teacher opens app with connectivity)
  - Sync identifies and de-duplicates: if same period has both offline and online marks, conflict resolution screen shown to teacher
- Sync delay logged: "Marked offline at [time]; synced at [time]"
- Useful for: rural schools, basement classrooms, network outage scenarios
- Offline window: attendance can be marked offline for up to 72 hours before forced sync reminder

---

## 83. Bulk Retroactive Holiday Update

- Admin declares a past date as holiday after it has already been marked by teachers:
  - System bulk-converts all student "Absent" marks for that day to "Holiday"
  - Teacher-marked period attendance records for that day are soft-deleted (kept in audit trail)
  - All affected students and parents notified in-app: "Attendance for [Date] has been updated to Holiday"
- Requires Principal approval for retroactive holiday declaration
- Reason and authority reference (government order / management decision) mandatory
- Audit trail preserved: original marks + bulk override logged

---

## 84. Government School Daily Muster Roll

- Government and government-aided schools must maintain a daily muster roll (register of attendance)
- System generates muster roll in state education department's prescribed format:
  - Student serial number, name, roll number, daily attendance (P/A) for each period or half-day
  - Teacher signature column
- Generated as PDF; downloadable per class per day
- End-of-month muster roll consolidation for official records
- Some states (Maharashtra, Karnataka, Tamil Nadu) require muster roll submission to Block Resource Centre (BRC)

---

## 85. Mid-Day Meal (MDM) Attendance Link

- Government primary schools (Classes 1–8): MDM (Mid-Day Meal) scheme beneficiary count = students present on that day
- POSHAN 2.0 / NP-NSPE (National Programme for Nutritional Support to Primary Education) compliance:
  - System generates daily MDM beneficiary count: class-wise number of students present
  - Report submitted to MDM scheme nodal teacher / head teacher
  - Monthly MDM report for block/district office submission
- MDM attendance count auto-generated from morning roll call / first-period attendance
- Discrepancy between MDM count and actual present count flagged to head teacher

---

## 86. Transfer Certificate Attendance Entry

- When student applies for TC (Module 07):
  - System calculates attendance from enrolment date to TC effective date
  - Overall attendance % and subject-wise (college) included
  - TC form (CBSE prescribed format) auto-filled with attendance data
- TC attendance field: "Total Working Days: [X] | Days Attended: [Y] | Attendance %: [Z]"
- State board TC formats vary: system supports state-specific TC templates
- Attendance calculation excludes periods after TC issue date

---

## 87. Chronic Illness Modified Attendance Threshold

- Student with documented chronic illness (cancer treatment, organ transplant, dialysis, cardiac condition):
  - Parents and treating doctor submit formal request to Principal with medical documentation
  - Principal + Management approve modified minimum attendance threshold (e.g., 50% instead of 75%)
  - Approved modification stored in student profile with effective date and review date
  - All attendance reports and exam eligibility checks apply the modified threshold for this student
  - Counsellor (Module 32) assigned for academic support plan
  - Review annually or at each term; modification can be extended or restored to standard

---

## 88. Long-Term Medical Leave Re-Integration

- Student absent 30+ consecutive days (hospitalization, surgery, serious illness):
  - Status: "Long-Term Medical Leave"
  - Attendance module shows two trajectories: pre-leave attendance % and post-return attendance %
  - Cumulative annual attendance calculation handles the gap period (gap days excluded from total working days with Principal approval)
  - On return: counsellor (Module 32) creates academic re-integration plan
  - HOD reviews pending syllabus coverage; Module 15 shows topics missed during leave
  - Parent notified of make-up plan and updated attendance standing

---

## 89. POCSO / Child Welfare Absence Trigger

- Unexplained absence > 5 consecutive days:
  - No leave application submitted
  - No parent response to in-app notifications or phone contact
  - Condition: student had no prior history of extended absence
- System auto-triggers:
  - Alert to class teacher, counsellor (Module 32), and POCSO committee (Module 41)
  - Welfare check record created: date, student details, action taken log
  - Principal notified
  - If student resides in school-provided transport area: transport staff queried (Module 29)
- Welfare check outcome logged: student safe (return explanation), welfare concern identified, or referred to child welfare authority
- Entire welfare trigger process logged as restricted-access record (POCSO confidentiality — Point 90)

---

## 90. POCSO Restricted Attendance Record

- Students under POCSO protection orders or active child welfare proceedings:
  - Attendance records flagged as restricted-access in DB
  - Only Principal, school counsellor, POCSO committee members, and the student's class teacher can view
  - Standard bulk reports (monthly, CBSE format, DEO) anonymize or exclude restricted students
  - Export reports show row as "Restricted" — not blank (blank could reveal count of restricted students)
- Access log maintained: who viewed restricted student's attendance record, timestamp
- Aligns with POCSO Act, DPDPA 2023 sensitive personal data protections

---

## 91. Attendance Anomaly Investigation Report

Weekly generated report for admin / Principal:

**Type 1 — Cross-Period Anomaly:**
Student marked absent by Period 1 teacher but present by Period 3 teacher without any late-entry record in between.

**Type 2 — Biometric vs Period Mismatch:**
Student has no biometric gate entry but is marked present in multiple periods.

**Type 3 — Bulk Pattern Anomaly:**
One teacher marking entire class as present every single day without variation (statistical impossibility).

**Type 4 — Retroactive Pattern:**
High volume of same-day corrections by same teacher (possible systematic error or manipulation).

- Report generated weekly; admin reviews and investigates each anomaly
- Anomalies acknowledged as: resolved (explanation noted), under investigation, false alarm
- Persistent Type 3/4 anomalies escalated to Principal for staff inquiry

---

## 92. Induction Program Attendance — NEP 2020

- NEP 2020 mandates a 4-week induction program for first-year students in higher education institutions
- Induction program topics: familiarization with institution, values, sports, arts, crafts, language, traditions
- Separate attendance tracking for induction program (not part of regular semester attendance)
- Minimum 75% induction attendance recommended; some universities link it to first-semester exam eligibility
- Faculty assigned to induction sessions marked in induction timetable (separate from regular timetable)
- Induction attendance certificate generated for each student at programme end

---

## 93. Convocation / Graduation Day Attendance

- Final-year college students attending annual convocation ceremony:
  - Attendance for that day = "Convocation Present" (special category)
  - Counts as present in records for that date
  - Students not attending convocation (remote students, NRI): marked accordingly
- Convocation event recorded in academic calendar (Module 05); attendance auto-linked

---

## 94. Substitute Teacher Attendance Authority

- When a substitute teacher takes a period (Module 10 Point 44):
  - Substitute teacher marks attendance for that period via their own app
  - Attendance is attributed to: the period slot (timetable entry) with a "Substitute" flag
  - Original teacher's name retained in timetable entry for record
  - Substitute's marking is authoritative for that period
  - If neither original nor substitute marks attendance: period flagged as "Unattended — Attendance Missing"

---

## 95. Attendance Discrepancy Report

- Before CBSE inspection, NAAC visit, government audit, or annual verification:
  - Admin generates discrepancy report: compares digital attendance records vs physical register entries (if both maintained)
  - Discrepancies listed: date, class, student, digital status, physical register status
  - Reconciliation: admin corrects discrepancy with Principal approval; reason documented
- Discrepancy report helps identify data entry errors in either system
- Schools maintaining only digital records: discrepancy report compares period-wise records vs teacher confirmation logs

---

## 96. Section-Wise Attendance Comparison

- Principal / admin compares daily and monthly attendance rates across sections of the same class:
  - Example: Class 10-A: 91%, Class 10-B: 83%, Class 10-C: 76%
  - Abnormally low section: Principal investigates (class teacher relationship, classroom environment, subject issues)
- Comparison chart shows section-wise trends over the term
- Consistently low-attendance sections flagged for: counsellor intervention, parent meeting, teaching method review

---

## 97. Attendance Trend Analysis

- Week-on-week and month-on-month attendance trend per class, per subject (college):
  - Seasonal dips visible: monsoon months (July–August), pre-exam anxiety (October, February), post-holiday slump (after Diwali, summer)
  - Unusual dip on specific days of week (e.g., Mondays consistently low = possible recurring unofficial holiday pattern)
- Trend data exported to Principal dashboard as visual chart
- Used for: academic calendar planning, parent communication campaigns, timetable adjustment (avoid major topics on high-absence days)

---

## 98. Peer Group Attendance Rank — Counsellor View

- Counsellor-only view (not visible to students or parents):
  - Student's attendance rank within their section / batch (1st to last)
  - Rank change month-on-month (improving / declining trend)
- Used for: targeted intervention for bottom 10% attendees
- Combined with academic performance rank to identify at-risk students (low attendance + low scores = high dropout risk)
- Alerts counsellor when a student drops significantly in attendance rank within a month

---

## DB Schema (Core Tables)

```
institution.attendance_slots
  id, tenant_id, branch_id, timetable_entry_id (FK → timetable_entries),
  slot_date, slot_type (period/lab_batch_a/lab_batch_b/assembly/prayer/
  remedial/online/study_tour/exam/induction), status (open/marked/locked/holiday),
  marking_deadline, created_at

institution.attendance_records
  id, attendance_slot_id, student_id, status
  (present/absent/late/authorized_absent/medical_absent/od/ncc_duty/
  sports_duty/calamity_holiday/govt_holiday/election_holiday/
  national_event/early_dismissal/half_present/restricted),
  marked_by (teacher_id), marked_at, marking_method
  (app/biometric/rfid/face_recognition/qr_code/manual/offline_sync),
  correction_count, last_corrected_by, last_corrected_at

institution.attendance_corrections
  id, attendance_record_id, original_status, corrected_status,
  corrected_by (teacher_id), correction_reason, approved_by, approved_at,
  correction_level (self/hod/principal/management), created_at

institution.attendance_condonations
  id, tenant_id, student_id, academic_year_id, term_id, subject_id (null for school),
  condonation_type (medical/sports/ncc/calamity/chronic_illness),
  days_condoned, % condoned, evidence_document_id, applied_by,
  recommended_by_hod, approved_by_principal, approved_by_management,
  status (pending/approved/rejected), created_at

institution.leave_applications
  id, tenant_id, student_id, applied_by (parent_id or admin_id),
  from_date, to_date, reason, leave_type (medical/personal/family/emergency),
  supporting_document_id, status (pending/approved/rejected),
  reviewed_by, reviewed_at, is_retroactive, created_at

institution.biometric_logs
  id, tenant_id, branch_id, student_id, log_type (entry/exit),
  log_timestamp, device_id, verified (bool)

institution.attendance_anomalies
  id, tenant_id, student_id, slot_date, anomaly_type
  (cross_period/biometric_mismatch/bulk_pattern/retroactive_pattern/
  pocso_welfare), detected_at, acknowledged_by, acknowledgement_note,
  status (open/resolved/escalated)

institution.welfare_checks
  id, tenant_id, student_id, trigger_type (consecutive_absent/pocso_trigger),
  trigger_date, consecutive_days, assigned_to (counsellor_id),
  action_log (JSON), outcome
  (student_safe/welfare_concern/referred_to_authority/student_withdrawn),
  resolved_at

institution.attendance_certificates
  id, tenant_id, student_id, requested_by, purpose
  (nsp/bonafide/bank_loan/court/tc/aishe),
  from_date, to_date, attendance_pct, subject_wise_data (JSON),
  generated_by, generated_at, document_id

institution.govt_submission_log
  id, tenant_id, branch_id, submission_type
  (udise/shala_darpan/deo_monthly/cbse_board/nsp/aishe/naac/mdm),
  period_month, period_year, submitted_by, submitted_at,
  portal_reference_number, file_path
```

---

## Integration Map

| Module | How |
|---|---|
| 05 — Academic Year & Calendar | Holidays auto-block attendance; working days calendar drives slots |
| 07 — Student Enrolment | Student roster, section assignment, biometric enrollment, RTE/scholarship flags |
| 08 — Staff Management | Teacher assigned to period; substitute teacher marking authority |
| 10 — Timetable & Scheduling | Each timetable period generates attendance slot; substitute periods flagged |
| 15 — Syllabus & Curriculum Builder | Period-wise "conducted" status feeds syllabus completion |
| 18 — Exam Paper Builder | Internal exam days; exam present = subject attendance |
| 19 — Exam Session & Proctoring | Exam registration block based on attendance |
| 21 — Results & Report Cards | Attendance % printed on report card; detention eligibility flag |
| 24 — Fee Structure | Attendance-based fee concession trigger |
| 29 — Transport | Field trip / study tour attendance linkage |
| 31 — Admission CRM | New student induction attendance |
| 32 — Counselling | Welfare checks, chronic absentee referrals, re-integration plans |
| 35 — Notifications | Parent absent alerts, shortage warnings, welfare triggers |
| 39 — Certificates | NCC/NSS certificates; attendance certificates |
| 40 — Document Management | Physical register PDFs, attendance certificates, medical certificates |
| 41 — POCSO Compliance | Welfare absence trigger, restricted record handling |
| 45 — Live Classes | Online period attendance capture |
