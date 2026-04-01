# Module 13 — Attendance (Hostel)

## Purpose
Define how EduForge tracks, manages, and reports student presence within hostel premises — covering night roll call, gate pass system, leave management, meal attendance, warden hierarchy, POCSO compliance, anti-ragging measures, government hostel compliance (NVS, KGBV, EMRS, SC/ST hostels), and all Indian regulatory requirements (UGC, Supreme Court, NHRC, Rajasthan Coaching Regulation Act). Hostel attendance is completely separate from academic attendance (Module 11/12) but the two systems are coordinated.

---

## 1. Hostel Attendance Model

- Hostel attendance tracks **physical presence within hostel premises** at defined checkpoints — it is not the same as academic attendance
- Key checkpoints:
  - Night roll call (primary — mandatory every night)
  - Morning roll call (optional per institution config)
  - Meal attendance (breakfast, lunch, evening snack, dinner)
  - Gate entry / exit (biometric / QR against gate pass)
- Academic attendance (Module 11/12) and hostel attendance are independent systems coordinated through leave synchronisation (Point 58)
- Hostel attendance record is the authoritative basis for: leave calculation, mess fee adjustment, scholarship compliance, government grant disbursement, welfare escalations

---

## 2. Hostel Types Covered

| Hostel Type | Governing Body | Special Compliance |
|---|---|---|
| School boarding hostel | CBSE / State Board | POCSO, UGC guidelines |
| College / university hostel | UGC / AICTE | UGC Hostel Dev. Guidelines 2018, anti-ragging |
| Coaching residential hostel (Kota model) | State Coaching Regulation | Rajasthan Act 2023, NHRC mental health |
| ITI / polytechnic hostel | NCVT / State DTE | AICTE norms |
| Govt SC/ST hostel | Social Welfare Dept | DSWO reporting, Aadhaar-linked |
| Navodaya Vidyalaya (NVS) | NVS/MHRD | NVS portal submission |
| Kasturba Gandhi Balika Vidyalaya (KGBV) | State Govt / MWCD | Female-only staff at night |
| Eklavya Model Residential School (EMRS) | Ministry of Tribal Affairs | Tribal welfare dept reporting |
| Sports Authority of India (SAI) hostel | SAI / Ministry of Sports | Training attendance linked |
| Model Residential Schools (state) | State Education Dept | State-specific reporting |

Each hostel type activates relevant compliance features in institution config.

---

## 3. Night Roll Call

- Most critical hostel attendance event — mandatory every night
- Configured time per institution (typically: boys 9–10 PM; girls 7–9 PM)
- Warden / floor in-charge marks each student:
  - **Present** — in their room / hostel premises
  - **Absent** — not found, no approved leave
  - **On Leave** — approved home / outstation / medical leave
  - **Sick Bay** — confined to hostel medical room
  - **Medical Emergency** — hospitalised
  - **OD (On Duty)** — official institutional duty (NCC, sports, field trip)
- Roll call taken floor by floor; floor warden submits to block warden; block warden compiles for Chief Warden
- Night roll call result visible to Chief Warden and Principal within 30 minutes of roll call time

---

## 4. Morning Roll Call

- Optional per institution config; enabled typically in residential schools
- Marks student present before leaving for classes
- Time: configured (typically 6:00–7:00 AM)
- Taken by class teacher at assembly or floor warden at hostel gate exit
- Used for: early absentee detection before academic day begins, confirming student returned from night without incident
- Results shared with academic attendance module for that day's first-period context

---

## 5. Meal Attendance

- Tracked per meal: Breakfast / Lunch / Evening Snack / Dinner
- Marking method: biometric finger scan or RFID card tap at dining hall entry; or manual count by mess supervisor
- Three primary purposes:
  1. **Kitchen planning** — advance headcount for food preparation quantity
  2. **Government scheme compliance** — POSHAN 2.0 / MDM / state hostel schemes (meal count = beneficiary count for funding)
  3. **Wellness monitoring** — student consistently skipping meals triggers welfare alert (Point 54)
- Meal attendance stored per student per meal per day
- Weekly meal attendance summary visible to warden; parent monthly summary includes meal % (Point 85)

---

## 6. Gate Pass — Mandatory Requirement

- Student must have an approved gate pass to exit hostel premises at any time
- Without gate pass: exit is unauthorized; security does not permit exit; alert raised
- Gate pass is the central safety and accountability tool for hostel management
- Gate pass types: Local (Point 7), Outstation (Point 8), Medical (Point 9), Official (Point 10), Emergency (Point 11)
- Gate pass system applies to all hostel types; strictness level configurable per institution

---

## 7. Local Gate Pass

- Purpose: within-city outing (shopping, bank, local doctor visit)
- Valid: same day; must return before curfew time
- Approval: floor warden or block warden
- Parent confirmation: required for students below 18 (in-app)
- Destination logged: area/locality (not exact address required)
- Quota: institution can limit local gate passes per week (e.g., max 2 per week during term)

---

## 8. Outstation Gate Pass

- Purpose: travel to home city / another city for personal reasons
- Duration: multi-day; return date specified
- Approval chain:
  1. Student submits in-app: destination, travel dates, mode of travel, expected return
  2. Parent confirms in-app (mandatory for all students regardless of age — hostel safety rule)
  3. Block warden approves
  4. Principal approves for extended leave (> 3 days)
- QR gate pass generated on final approval
- Security scans QR on exit; logs departure time
- Parent/guardian must confirm student's safe arrival at destination within 6 hours (in-app confirmation)

---

## 9. Medical Gate Pass

- Purpose: hospital visit, specialist consultation, dental appointment
- Approval: medical officer (hostel) + block warden
- Hospital / clinic name and appointment details required
- If planned: normal gate pass flow (Point 12)
- If emergency: fast-track (warden + medical officer jointly approve within 15 minutes)
- Parent notified regardless of student age
- Return: student checks in at hostel medical room on return; medical officer notes condition

---

## 10. Official Gate Pass

- Purpose: institutional duty — NCC camp, NSS event, sports tournament, industrial visit, college cultural event, inter-institutional competition
- Approval: HOD / department head + block warden (no separate Principal approval needed if event is in academic calendar)
- Status in hostel roll call: "OD" for duration
- Coordinated with Module 11/12 OD status so academic attendance also updated
- Return date specified; warden confirms check-in on return (Point 68)

---

## 11. Emergency Gate Pass

- Purpose: sudden family emergency (death, critical illness of close family member)
- Fast-track workflow: warden directly approves; Principal notified immediately after
- Parent / emergency contact acknowledgement logged
- Issued within 30 minutes of request
- Return date left open (estimated); student/parent updates return date in-app
- Student in transit: warden calls to confirm safe travel at configured intervals (every 6 hours for long distance)

---

## 12. Gate Pass Application Workflow

```
Student submits application in-app
  → Reason, destination, departure date/time, return date/time
  → Parent confirms in-app (mandatory for minors; recommended for all)
  → Floor / Block Warden reviews and approves / rejects with reason
  → [For outstation > 3 days: Principal approval added]
  → On approval: QR code gate pass generated in student app
  → Student shows QR to security guard on exit
  → Security scans QR: logs departure timestamp, gate pass number
  → On return: student scans QR again at gate
  → Return timestamp logged; warden notified of return
  → Academic attendance module notified (leave period = Authorized Absent)
```

- Rejected gate pass: student notified with reason; can reapply with modification
- Gate pass record retained permanently in student's hostel record

---

## 13. Gate Pass Expiry and Late Return

- System monitors gate pass return time in real-time
- **T + 15 minutes past expiry:** in-app alert to warden; warden calls student
- **T + 30 minutes:** parent notified in-app and phone
- **T + 45 minutes:** Principal notified; welfare check initiated
- **T + 2 hours:** missing person protocol if no contact (Point 52)
- Late return logged: student name, gate pass expiry time, actual return time, delay duration, reason given, action taken
- 3 late returns in a term = written warning; 5 = disciplinary committee referral

---

## 14. Unauthorized Exit

- Student leaves hostel without gate pass
- Security records: student name, time, description; immediate alert to warden
- Warden calls student immediately; Principal notified within 15 minutes
- Parent notified in-app: "Your ward [Name] has left the hostel without authorisation at [time]"
- Disciplinary case opened (Point 77)
- If student is minor and unreachable within 30 minutes: police informed

---

## 15. Night Curfew Time Configuration

| Hostel Type | Default Curfew | Configurable |
|---|---|---|
| Boys hostel (school) | 9:00 PM | Yes |
| Girls hostel (school) | 7:00 PM | Yes |
| Boys hostel (college) | 10:00 PM | Yes |
| Girls hostel (college) | 8:00 PM | Yes (UGC guideline) |
| Coaching hostel (boys) | 9:30 PM | Yes |
| Coaching hostel (girls) | 7:30 PM | Yes |
| PG / senior students | 11:00 PM | Yes |

- Weekend curfew extension: configurable (+30 to +60 minutes)
- Festival eve curfew: configurable per festival
- Night curfew enforced via gate biometric; entry after curfew without gate pass = violation

---

## 16. Absent from Night Roll Call Without Gate Pass

Most serious hostel violation — immediate action protocol:

```
T+0: Warden marks student Absent in roll call
T+5 min: Warden checks common areas (TV room, study room, bathroom)
T+10 min: Room-mates and floor neighbours asked
T+15 min: Block Warden + Chief Warden notified
T+20 min: Parent called and in-app notification
T+30 min: Principal notified; security full search of campus
T+45 min: If minor — police informed; welfare officer activated
T+60 min: Missing student protocol (Point 52) formally initiated
```

All timestamps recorded in incident log; welfare check created in Module 32.

---

## 17. Night Curfew Violation Log

Each violation logged:
- Student name, date, gate pass reference (if any)
- Scheduled return time vs actual return time
- Delay in minutes
- Reason given by student
- Action taken: Verbal Warning (1st) → Written Warning (2nd) → Parent Meeting (3rd) → Disciplinary Committee (4th+)
- Cumulative violation count shown on warden dashboard
- Violation history included in student's hostel record

---

## 18. Night Duty Warden Log

- Duty warden logs rounds every night:
  - Time of each round, floor covered, observations
  - Any student not in room during round (name, room, floor)
  - Any maintenance issue observed (lock broken, light out, suspicious activity)
  - Any incident (altercation, medical, suspicious visitor)
- Round log linked to night roll call: students absent from rounds cross-referenced with roll call
- Morning summary: duty warden submits log to Chief Warden; any incidents highlighted

---

## 19. Home Leave

- Student applies for leave to visit home for holidays, weekends, or personal reasons
- Application in-app: from date, to date, reason, mode of travel
- Warden approves; parent confirms
- Hostel roll call shows "Home Leave" for approved dates
- Academic attendance for those dates: auto-set to "Authorized Absent" (Point 58)
- Parent confirmation of student's safe arrival at home: requested within 6 hours of departure (in-app)
- Return confirmed at hostel gate (Point 68)

---

## 20. Medical Leave

- Student hospitalised or bedridden at home:
  - Medical officer certifies nature of illness; hospitalization details logged
  - Hostel status: "Medical Leave"
  - Academic attendance: auto-set to "Medical Absent" (Module 11 coordination)
  - Warden + counsellor notified; welfare officer checks in every 2 days
  - Hospital name, admission date, discharge date logged
  - Medical certificate required on return (same as Module 11 Point 65)
- Re-admission to hostel after medical leave: medical officer clearance required; fitness certificate uploaded

---

## 21. Sick Bay / In-House Medical Room

- Student unwell but not severe enough for hospitalization:
  - Hostel medical room admission; medical officer or nurse assessment
  - Roll call status: "Sick Bay" — present on hostel premises but confined
  - Academic attendance: teacher informed; OD or Medical Absent applied for those periods
  - Meals delivered to sick bay (Point 45)
  - Parent notified in-app: "Your ward is unwell and resting in the hostel medical room. They are being attended by the medical officer."
  - Medical officer reviews daily; escalates to hospital if condition worsens
  - Sick bay stay > 3 days: compulsory parent visit or hospital transfer

---

## 22. Emergency Leave

- Sudden family bereavement or critical family medical emergency:
  - Fast-track workflow: warden directly approves; Principal notified
  - Emergency gate pass issued within 30 minutes
  - Parent acknowledgement mandatory
  - Return date left open; student/parent updates in-app when situation is clear
  - Student in transit: warden calls at configured intervals to confirm safe travel
  - Academic attendance: Emergency Leave status; counsellor follows up on return for emotional support

---

## 23. Festival Leave Calendar

Major Indian festivals: hostel declares leave for most/all students:

| Festival | Region | Typical Hostel Leave Duration |
|---|---|---|
| Diwali | Pan-India | 3–7 days |
| Holi | North/Central India | 2–3 days |
| Eid ul-Fitr / Eid ul-Adha | Pan-India | 1–3 days |
| Durga Puja / Navratri | East/West India | 3–5 days |
| Onam | Kerala | 2–3 days |
| Pongal / Makar Sankranti | South India | 2–3 days |
| Christmas | Pan-India | 2–5 days |
| Guru Nanak Jayanti | Punjab / North India | 1–2 days |

- Festival leave declared by Principal; hostel auto-marks "Festival Leave" for those nights
- Students who stay back during festival leave: separately tracked; warden reduces to skeleton strength
- Hostel closes or operates at minimum capacity; mess may offer reduced menu

---

## 24. Weekly / Monthly Leave Quota

- Institution can configure leave quota per student per month:
  - Example: maximum 2 home leaves/month (each up to 2 days) during term
  - Example: maximum 4 weekend leaves per semester
- System tracks: leaves taken vs quota remaining
- Warden sees quota before approving new leave; application blocked if quota exhausted (except emergency/medical)
- Unused quota does not automatically carry forward (institution config); leave bank option (Point 27)
- Quota resets at start of each term

---

## 25. Mandatory Stay-In Period (Exam Lock)

- During internal exams, semester exams, board exams:
  - Hostel enforces stay-in rule for exam-appearing students
  - System auto-blocks all non-emergency gate pass requests for exam-period dates
  - Exceptions allowed only: medical emergency, death in family, institutional duty
  - Stay-in period dates configurable; synced from academic calendar (Module 05)
  - Students notified in-app 7 days before stay-in period begins
- Purpose: ensure students get adequate rest and study time; prevent last-minute travel risk

---

## 26. Leave Extension Request

- Student on approved leave needs to extend return date (illness, family emergency):
  - Parent submits extension request via app with reason
  - Block warden reviews; approves or rejects
  - Extended return date updated in hostel record
  - Academic attendance module notified of extended absence dates
  - Approvals beyond 7 days require Principal approval
  - Extensions not approved retroactively (must be requested before original return date lapses)

---

## 27. Leave Bank

- Unused leave days (up to configured monthly cap) carry forward to next month
- Example: student entitled to 4 leave days/month; used 2; remaining 2 carry forward (maximum bank size: 6 days)
- System tracks cumulative leave bank balance per student
- Displayed on student's hostel dashboard: "Remaining this month: [X] days + [Y] days banked"
- Warden sees bank balance before approving extended leaves
- Leave bank resets to zero at term end (unused carried days lapse)

---

## 28. Warden Hierarchy

```
Chief Warden (faculty member — UGC mandatory)
  ↓
Block Warden (one per hostel block)
  ↓
Floor Warden / Assistant Warden (one per floor or per 50 students)
  ↓
Night Duty Warden (rotational duty; covers after curfew)
```

- Chief Warden must be a faculty member per UGC Hostel Development Guidelines 2018
- Each level has defined responsibilities:
  - Floor Warden: daily roll call, room inspection, student welfare
  - Block Warden: consolidates floor roll calls, gate pass approvals, minor disciplinary actions
  - Chief Warden: overall hostel management, major disciplinary cases, compliance reporting
  - Night Duty Warden: after-curfew rounds, emergency response, night roll call supervision

---

## 29. Lady Warden — UGC Mandatory

- UGC Hostel Development Guidelines 2018: every girls' hostel must have a designated lady warden
- Lady warden has primary authority over girls' hostel roll call, gate pass approvals, and disciplinary matters
- System flags lady warden position vacancy as UGC compliance gap: alert to Principal and management
- Lady warden must reside on campus or within 500 metres (UGC guideline); residence address stored
- Lady warden contact details displayed prominently in girls' hostel app view for emergency access

---

## 30. Warden Roll Call Substitution

- If floor warden absent: another warden takes the absent warden's floor roll call
- Substitution logged: original warden name, substitute warden name, date, reason
- Chief Warden receives notification of substitution
- Substitute's roll call is fully authoritative for that night
- Persistent substitutions for the same warden (> 3 times/month): Chief Warden reviews warden attendance compliance

---

## 31. Warden Performance Report

Monthly report per warden:
- Roll call conducted on time vs delayed vs missed (%)
- Gate passes processed (count, approval rate, rejection rate)
- Incidents logged (welfare checks, disciplinary cases, missing reports)
- Disciplinary actions taken
- Anti-ragging rounds conducted (college hostels)
- Night duty logs submitted

Report available to: Chief Warden, Principal, Management
Input to staff appraisal (Module 08)

---

## 32. Hostel Staff Attendance

- All hostel staff tracked separately from students:
  - Warden (Chief, Block, Floor, Night Duty)
  - Security guard (day shift, night shift)
  - Mess staff (cook, assistant)
  - Housekeeping staff
  - Medical officer / nurse
- Staffing gap alerts:
  - Night security absent = immediate Principal alert (safety risk)
  - Lady warden absent in girls' hostel = UGC compliance alert
  - Medical officer absent = Principal alert (welfare risk)
- Staff attendance feeds Module 08 Staff Management

---

## 33. POCSO Physical Separation — Girls' Hostel

- Male staff (wardens, security, maintenance) **prohibited from entering girls' hostel residential floors**
- System logs all hostel entry/exit via biometric gate:
  - Male ID attempting girls' hostel residential floor entry = immediate alert to Chief Warden + POCSO committee (Module 41)
- Male maintenance staff: allowed only in common areas and during daytime, escorted by lady warden
- Male visitors: strictly to visitor room / lobby only (Point 49)
- Any POCSO incident from girls' hostel: escalates directly to POCSO committee (not through male warden chain)

---

## 34. Female-Only Night Security — Girls' Hostel

- Girls' hostel: female security guards mandated for night shift (POCSO Act + state norms + UGC guidelines)
- System tracks security guard gender against shift assignment
- Male guard assigned to girls' hostel night shift = compliance violation alert to Principal
- Female guard availability gap: immediate escalation; alternative arrangement before night begins
- Security guard shift log maintained: guard name, gender, shift start/end, hostel assigned

---

## 35. Girls' Hostel Visitor Restriction

Approved male visitors to girls' hostel (common visiting area only):
- Father, grandfather, brother, husband (for married students)
- Official institutional guests (with prior written request to Principal)

- Identity verified against approved visitor list (submitted by parents at admission)
- Unrecognized male visitor: not admitted; incident logged; Principal notified
- Female visitors: less restricted but still require student to receive and sign out
- Visitor not allowed on residential floors under any circumstances
- POCSO committee receives monthly visitor log summary for girls' hostels

---

## 36. POCSO Direct Complaint from Hostel

- Any hostel resident can file a POCSO complaint via in-app anonymous button
- Complaint route: directly to Principal + POCSO committee (Module 41)
- **Not routed through warden** — prevents conflict of interest if complaint involves hostel staff
- System records: submission timestamp, anonymous flag, hostel / block / floor (approximate location)
- POCSO committee receives alert immediately; 24-hour response protocol activated
- UGC helpline number 1800-180-5522 displayed in hostel section of student app at all times

---

## 37. Biometric at Hostel Gate

- Fingerprint / RFID reader at hostel entry/exit gate
- Student scans on exit: system checks for valid active gate pass; no gate pass = exit blocked + alert
- Student scans on return: return timestamp logged; gate pass marked "Returned"; warden notified
- Cross-reference with roll call: student showed gate biometric exit but still marked present in roll call = anomaly (incorrect roll call marking)
- Reverse: student marked absent in roll call but biometric shows they are in hostel = warden missed them during round
- Anomaly reports generated nightly for Chief Warden

---

## 38. QR Code Room Check-In for Roll Call

- Each room has a QR code affixed to door (generated from room record)
- Warden scans room QR during roll call rounds using their app
- After scanning room QR: marks each listed occupant as Present / Absent / Sick Bay
- Faster than verbal roll call for large hostels (100+ rooms per block)
- Warden cannot mark a room without physically scanning its QR (prevents remote marking)
- Digital round log auto-created: rooms visited, time, any observations

---

## 39. Self-Check-In for Morning Roll Call

- Student marks self-present via app within a defined time window (e.g., 6:00–7:00 AM)
- Prevents warden needing to physically visit every room at dawn
- Warden verifies by random spot check: visits 15–20% of rooms each morning (random selection by system)
- Spot check results logged: confirmed present / not found
- Students who do not self-check-in by window close: marked absent; warden physically checks

---

## 40. CCTV Coverage Map

- Common area CCTV camera locations registered in system:
  - Entry gates, corridors, dining hall, common room, stairwells, parking
  - NOT in rooms or bathrooms (privacy — DPDPA 2023)
- Camera coverage map available to: Chief Warden, Principal, Security Supervisor
- Used as reference during incident investigations (not live tracking)
- CCTV footage retention policy: minimum 30 days (standard); 90 days for sensitive incidents (logged as evidence)
- New camera installation: logged in coverage map; location described; ensures no blind spots in common areas

---

## 41. Room Assignment and Occupancy Tracking

- Each student assigned to: Block → Floor → Room → Bed Number
- Room types: Single, Double, Triple, Dormitory (4–8 beds)
- Room occupancy tracked: beds occupied vs total beds; vacancy visible to admin for new allotments
- Room assignment record: effective date, assigned by, room key issued (key serial number)
- Occupancy report per block/floor: used for new admission planning and hostel capacity management

---

## 42. Room Change Request

- Student requests room change: reason (compatibility issue, medical need, floor preference, study environment)
- Block warden reviews and approves / rejects
- Chief Warden approval for cross-block transfers
- System updates room assignment with effective date
- Old room: bed marked vacant; new room: bed marked occupied
- Attendance records continue uninterrupted under new room assignment
- Key handover: old key returned, new key issued; both logged

---

## 43. Room Inspection Record

- Periodic inspection by warden (weekly or monthly per institution config):
  - Cleanliness, furniture condition, prohibited items, electrical safety, no food stored in room
  - Inspection findings logged per room: pass / requires action / serious violation
  - Requires-action items: follow-up date set; warden verifies resolution
  - Serious violations (prohibited items, damage): disciplinary action (Point 77)
- Pre-vacation inspection: before students leave for vacation, room inspection mandatory
- End-of-year inspection: before permanent checkout (Point 71)

---

## 44. Room Inventory / Amenity Assignment

Items issued to student at room allotment (per bed):
- Furniture: bed, mattress, study table, chair, wardrobe shelf allocation, locker
- Linen: pillow, pillow cover, bedsheet, blanket (government hostels: issued by department)
- Key: room key serial number; duplicate key charge logged
- Any additional items: fan, lamp, power extension (as per hostel rules)

- Issue logged with condition (Good / Fair / Damaged at issue)
- On checkout: condition re-assessed; damage / missing items logged; cost deducted from security deposit
- Security deposit clearance linked to inventory clearance (Point 110)

---

## 45. Sick Student Meal Delivery

- When student is in sick bay or quarantined in room:
  - Warden submits meal delivery request to mess supervisor
  - Delivery log per meal: mess staff name, delivery time, food items
  - Student acknowledgement: student or warden confirms receipt via app
  - Ensures no student misses nutrition during illness
  - Dietary instructions from medical officer followed (light food, no spicy, specific diet)
- Daily delivery log reviewed by warden; any missed deliveries escalated to mess supervisor

---

## 46. Room-mate Emergency Contact

- Room allocation data stored with all occupants listed
- If student is absent without explanation: room-mates are the first informal contact point
- Warden calls / visits room-mates before escalating to parent or Principal
- Room-mate information also used: if student falls unconscious in room, room-mate identifies them for medical officer
- Room-mate details visible to warden for the rooms they manage; not visible to other students (privacy)

---

## 47. Visitor Log

- Parent and family member visits on designated visiting days/hours:
  - Visitor name, relationship to student, government ID type and number
  - Cross-check against approved visitor list (Point 48)
  - Student name, arrival time, exit time
  - Items brought in: checked by security (prohibited items list configured by institution)
  - Items brought out: student cannot remove hostel property (furniture, linen); checked on exit
- Visitor log maintained digitally; accessible to Chief Warden and Principal
- Retained for 2 years for reference in case of any incident

---

## 48. Approved Visitor List

- Parent submits list of authorized visitors at hostel admission:
  - Name, relationship to student, government ID proof (Aadhaar / PAN / Passport), contact number
  - Photo upload optional but recommended
- Security verifies every visitor against the list before entry
- Unrecognized visitor: not admitted; student called to the gate to verify; if student confirms → visitor allowed with manual log entry; warden notified
- Students below 18: approved visitor list is **mandatory** before any visitor is admitted
- Visitor list updatable by parent via app; new additions take 24 hours to activate (prevents gaming)

---

## 49. Visitor Room / Lobby Restriction

- All visitors (including parents) confined to designated visitor room or lobby area
- Visitors not permitted on residential floors under any circumstances
- Girls' hostel: male visitors further restricted to ground-floor visitor room only
- Security enforces floor restriction; any visitor seen on residential floor = incident report
- Meeting duration: configurable (typically max 2 hours during visiting hours)
- After visiting hours: visitor must leave; security confirms exit; any visitor remaining after hours = security alert

---

## 50. Parent Visit Register

- Formal register of all parent visits (separate from general visitor log):
  - Date, parent name, student name, relationship, entry time, exit time, purpose of visit
  - Parent acknowledges hostel rules and student's condition during visit
- Used in case of dispute: "parent was informed of situation on [date]"
- Parent visit frequency tracked; unusually frequent visits (e.g., every week) noted for counsellor awareness (possible student distress signal)

---

## 51. Medical Emergency Protocol

Immediately triggered when student faces a medical emergency in hostel:

```
1. Night warden / warden calls ambulance (108 / private)
2. Medical officer / nurse provides first aid
3. Parent called immediately (phone) + in-app notification
4. Student status in roll call: "Medical Emergency"
5. Hospital name, ambulance call time, departure time logged
6. Chief Warden + Principal notified within 5 minutes
7. Welfare officer assigned; follows up with hospital
8. Student insurance information retrieved (Point 107) for hospital admission
9. Counsellor (Module 32) assigned for post-recovery support
```

Incident report auto-created; all timestamps logged; immutable record.

---

## 52. Missing Student Protocol

When student not found during night roll call, not on any leave, not in sick bay, not found in common areas:

```
T+0: Warden marks Absent; begins physical search
T+5 min: Room-mates, floor neighbours, study room checked
T+15 min: Block Warden + Chief Warden notified; all block wardens alerted
T+20 min: Parent called + in-app notification; campus security activated
T+30 min: Principal notified; CCTV last sighting checked (Point 40)
T+45 min: [For minors] Police informed per law; [For adults] Campus security full search + police advisory
T+60 min: Missing person incident report formally created; welfare officer activated
```

Every step timestamped; welfare check created in Module 32; incident record immutable.

---

## 53. Consecutive Absence from Night Roll Call

| Consecutive Nights | Action |
|---|---|
| 2 nights absent, no leave | Warden calls student and parent; counsellor informed |
| 3 nights absent | Principal notified; welfare check (Module 32) created |
| 5 nights absent, no contact | Management + legal guardian involved; welfare officer home visit |
| 7+ nights absent | Police advisory (for minors); missing person protocol re-initiated |

Consecutive count resets on any confirmed present / approved leave.

---

## 54. Mental Health Check-In at Hostel

- Mandated by Rajasthan Coaching Regulation Act 2023, NHRC guidelines, and UGC Student Welfare guidelines:
  - Weekly mental health check-in with hostel counsellor
  - Check-in can be: group session, individual drop-in, or brief warden-level conversation
- Aggregate attendance tracked for compliance reporting: total check-in sessions held, total unique student interactions (count only — not student names in public reports)
- Detailed records per student maintained in Module 32 Counselling with restricted access
- Students expressing distress: immediate referral to counsellor + warden welfare round increased for that student
- Residential coaching hostels (Kota model): additional daily check-in by warden during room rounds; any concerning observation → immediate counsellor referral

---

## 55. Student Buddy System

- Each student assigned a buddy (preferably room-mate or adjacent room student)
- Buddy's responsibility: alert warden if their buddy is not seen at mealtimes or has not returned by curfew
- Proactive welfare measure; especially critical for first-year students and students from distant regions
- Buddy pairs stored in system; updated if room changes
- Buddy system does not replace warden's roll call — it supplements it for informal early detection
- End-of-term buddy feedback: optional; students rate their buddy relationship (comfort level); used to improve future pairing

---

## 56. Fire Drill Attendance

- Mandatory fire drill per NBC 2016 (National Building Code of India) and state fire safety regulations
- Frequency: minimum once per semester
- All hostel students must participate; attendance marked per drill by floor warden
- Absent students flagged: not excused unless medical/leave
- Drill metrics logged:
  - Evacuation start time → all-clear time
  - Response time per floor
  - Any students who did not evacuate promptly (requires re-training)
- Fire drill compliance report for: fire department inspection, NAAC, NHRC, insurance renewal
- Next drill date set immediately after each drill; auto-reminder to Chief Warden 7 days before

---

## 57. Cross-Module Double-Absence Welfare Flag

**Highest priority welfare alert:**
- Student marked absent in academic attendance (Module 11) AND absent from night roll call on the same day
- Without any approved leave in either system
- Trigger: immediate in-app alert to counsellor (Module 32), class teacher, warden, and Principal simultaneously
- This combination suggests student may have left campus without informing anyone — welfare emergency
- Missing student protocol (Point 52) initiated in parallel with welfare check

---

## 58. Academic Attendance Coordination

- When student is on approved hostel leave: academic attendance (Module 11/12) automatically updated:

| Hostel Leave Type | Academic Attendance Status Set |
|---|---|
| Home Leave | Authorized Absent |
| Medical Leave | Medical Absent |
| Official Duty (OD) | OD / On Duty |
| Emergency Leave | Authorized Absent (Emergency) |
| Sick Bay (on premises) | Medical Absent (for missed periods) |

- Synchronisation is one-way: hostel leave → academic leave (teacher still takes attendance; system pre-fills)
- Academic teacher can override if student came to class despite being on hostel leave (day return)
- No double-entry required; both systems stay in sync automatically

---

## 59. Board Exam / Semester Exam Hostel Coordination

- During board / semester exam period:
  - Students marked present in exam hall (Module 19) cross-referenced with previous night's hostel roll call
  - Student appearing in exam but absent from previous night's hostel roll call (without gate pass): anomaly flagged for investigation
  - Ensures students did not leave campus the night before exam without approval
  - Result: either gate pass was issued and not recorded (admin error) or unauthorized absence (disciplinary)

---

## 60. Government SC/ST Hostel Compliance

- Social Welfare Department-operated hostels:
  - Attendance records mandatory for state government grant disbursement
  - Monthly attendance report submitted to District Social Welfare Officer (DSWO) in state-prescribed format
  - Student must maintain minimum 75% hostel nights attended to continue receiving: free accommodation, food allowance, monthly stipend
  - Aadhaar-linked student IDs mandatory; attendance records cross-referenced with Aadhaar for government audit
- System generates DSWO format monthly report (state-specific format: varies across Maharashtra, Karnataka, Tamil Nadu, Rajasthan, UP)
- Students falling below threshold: DSWO notified; student given improvement window before benefit suspension

---

## 61. Navodaya Vidyalaya Samiti (NVS) Hostel

- All NVS students are residential (no day scholars)
- Strict attendance norms per NVS operational guidelines
- NVS HQ requires attendance data submitted via NVS portal periodically
- System generates NVS-compatible export: student NVSHQ ID, class, hostel block, attendance days, leave days
- CBSE academic attendance and hostel attendance linked in NVS reports (single combined report)
- NVS inspection checklist: hostel safety, warden staffing, anti-ragging measures — all reportable from system

---

## 62. Kasturba Gandhi Balika Vidyalaya (KGBV) Hostel

- State government residential schools for girls from SC/ST/OBC/minority/BPL families (Classes 6–12)
- Additional safeguards:
  - Female staff only allowed in residential areas at all times
  - Night security: female guards mandatory (no exceptions)
  - POCSO protocol stricter than standard: any male staff access logged and reported monthly to state authority
- Monthly attendance submitted to State KGBV Coordinator / State Project Director (SSA/SAMSA/SMSA)
- Attendance linked to state funding for KGBV scheme (attendance < threshold = funding review)
- Warden herself must be female (state mandate)

---

## 63. Eklavya Model Residential Schools (EMRS) Hostel

- Ministry of Tribal Affairs; exclusively for tribal (ST category) students
- Attendance records maintained for EMRS Society reporting and State Tribal Welfare Department
- Monthly report to District Tribal Welfare Officer (DTWO)
- Additional welfare monitoring: tribal students often from remote areas; first-time hostel experience for many
- Homesickness protocol: counsellor assigned to new admissions for first 2 months; check-in frequency higher
- Cultural sensitivity in hostel management: local tribal language support in app (where feasible)

---

## 64. Sports Authority of India (SAI) Hostel

- Student-athletes in SAI / institutional sports hostels:
  - Mandatory morning training (typically 5:00–6:30 AM): attendance taken by coach
  - Mandatory evening training (typically 4:00–6:00 PM): attendance taken by coach
  - Training attendance cross-referenced with hostel night roll call (athlete present in hostel but absent from training = performance concern)
- Training attendance data feeds: SAI performance reports, national sports federation reporting, scholarship review
- Missing training session + missing from hostel = immediate coach + warden combined alert
- Selection trial periods: attendance must be 100% during trial camps; any absence = trial disqualification

---

## 65. Government Scholarship Hostel Compliance

Students on state / central government hostel stipend schemes:

| Scheme | Ministry | Min Attendance |
|---|---|---|
| Post-Matric Scholarship (Hostel allowance) | Ministry of Social Justice | 75% |
| Tribal Welfare Hostel Stipend | Ministry of Tribal Affairs | 75% |
| Minority Welfare Hostel Scheme | Ministry of Minority Affairs | 75% |
| Central Sector Scholarship | Ministry of Education | 75% |
| State-specific SC/ST/OBC hostel schemes | State Social Welfare | 75–80% (state-specific) |

- System tracks scholarship holder students separately (scholarship category flag from Module 07)
- 30 days before renewal deadline: alert to admin of students below threshold
- Hostel attendance certificate auto-generated for eligible students (Point 104)
- Non-compliant students: scheme coordinator alerted; student given improvement window with deadline

---

## 66. NAAC Hostel Documentation

- NAAC Criterion 4.1 (Physical Facilities) and 5.1 (Student Support) require:
  - Hostel occupancy data (beds available vs occupied)
  - Safety compliance documentation (fire, POCSO, anti-ragging)
  - Warden staffing and qualifications
  - Welfare services (counselling, medical, recreation)
  - Grievance mechanism for hostel students
- System generates NAAC format report with all required data points
- NAAC peer team can verify during on-site visit via real-time dashboard access (read-only view for inspector)

---

## 67. New Student Hostel Check-In

First arrival at hostel — complete onboarding process:
1. Room key handover: key serial number logged; student signs receipt
2. Room condition report: student and warden jointly assess room condition; signed by both
3. Inventory issued: all items listed (Point 44); signed acknowledgement
4. Hostel rules briefing: student reads and digitally acknowledges hostel rules document
5. Anti-ragging undertaking: student AND parent sign digitally (Point 93 — hostel admission blocked until signed)
6. Approved visitor list submission: parent submits authorized visitor names and IDs
7. Emergency contact verification: parent/guardian contacts confirmed current
8. Hostel fee receipt confirmation: payment confirmation from Module 25
9. Orientation attendance: hostel orientation session attendance marked (Point 92 — see DB schema)

---

## 68. Return from Leave Check-In

- Student returns from any approved leave (home, outstation, medical, official):
  - Student scans biometric at hostel gate on return; return timestamp auto-logged
  - Gate pass record updated: "Returned at [time]"
  - Warden receives in-app notification of student's return
  - Night roll call updated: student moves from "On Leave" to "Present" status from that night
  - Academic attendance module notified: authorized absence period ends
- If student returns after curfew: late return logged (Point 17); reason noted

---

## 69. Vacation Hostel Closure

- At academic year end or term break:
  - Checkout deadline set by Principal
  - Students check out by deadline: room key returned, room inspection done, inventory cleared, dues settled
  - Last checkout logged per student
  - Security deposit status updated (Point 110)
  - Hostel status switches to "Closed" or "Vacation Mode"
  - Remaining inventory stored; any damage documented
- Hostel closed status prevents new gate pass applications and roll call requirements

---

## 70. Vacation Skeleton Operation

- Students who remain during vacation (international students, students from distant regions, sports students, students preparing for competitive exams):
  - "Vacation Resident" status marked
  - Attendance tracking continues normally
  - Enhanced welfare monitoring: warden checks more frequently; emergency contact on standby
  - Reduced mess operation: simplified menu; headcount for kitchen
  - Reduced warden staffing: skeleton strength; night security maintained
  - Principal and management informed of vacation-staying student list

---

## 71. Permanent Check-Out (TC / Graduation / Transfer)

- Student leaving hostel permanently:
  1. Room inspection: warden + student; condition documented
  2. Inventory reconciliation: all issued items returned; damage/missing items noted
  3. Key return: room key returned; logged
  4. Dues clearance: hostel fee, mess fee, damage charges, all settled (Module 25)
  5. Security deposit: refund or forfeiture calculated; linked to Module 25
  6. Hostel clearance certificate issued (Point 110)
  7. Check-out timestamp logged; hostel record closed
- Checkout cannot happen without clearance certificate (linked to TC / migration certificate issuance in Module 07)

---

## 72. Inter-Hostel / Inter-Campus Transfer

- Student transfers from Hostel A (Branch 1) to Hostel B (Branch 2):
  - Chief Warden of both hostels approve
  - Room assignment at new hostel confirmed before transfer
  - Key handover at old hostel; key issue at new hostel
  - Attendance records migrated to new hostel (historical preserved)
  - Parent notified in-app of new hostel details
  - Emergency contact and approved visitor list transferred
  - Academic module notified of new branch (Module 07 transfer coordination)

---

## 73. Mess Opt-Out for Leave

- Student going home or on leave: opts out of meals for those days via app
- Opt-out must be submitted before 8 PM previous evening (for breakfast opt-out) or configurable window
- Mess headcount reduced accordingly; mess contractor informed
- Mess fee credit: for opted-out days beyond minimum threshold (configurable: e.g., > 3 consecutive days):
  - Credit calculated: days × daily mess rate
  - Credit applied to next month's mess bill
- Last-minute opt-out (day-of): no fee credit; headcount already placed with contractor

---

## 74. Special Diet Tracking

- Student with documented dietary requirement:
  - **Medical:** diabetes, hypertension, food allergy (nut allergy, lactose intolerance, gluten intolerance)
  - **Religious:** vegetarian, Jain (no root vegetables), halal, kosher, no beef/pork
  - **Cultural:** specific regional food preferences (accommodation where feasible)
- Special diet flag set in student hostel profile with medical officer / warden confirmation
- Mess management receives daily special diet list automatically
- Meals prepared separately; labelled; delivered or set aside for special diet students
- Non-compliance (wrong food served) logged and reported to mess supervisor

---

## 75. Mess Fee Adjustment / Refund

- For approved leave > minimum threshold (configurable: default 3+ consecutive days):
  - Mess fee prorated: (leave days × daily mess rate) = credit amount
  - Credit applied to next month's mess bill or refunded (institution config)
  - Calculation based on hostel leave record (authoritative)
- Monthly mess bill: fee − credits = net payable; linked to Module 25 Fee Collection
- Disputed adjustments: student raises query; attendance / leave record is evidence; Chief Warden arbitrates

---

## 76. POSHAN 2.0 / MDM Compliance — Government Hostels

- Government residential schools (Navodaya, KGBV, SC/ST hostels):
  - Daily meal beneficiary count = students present on that day (per POSHAN 2.0 / NP-NSPE scheme)
  - Count per meal: breakfast, lunch, dinner
  - Report generated daily by hostel admin; submitted to block/district office
  - Monthly POSHAN report: cumulative beneficiary-days per student
- Discrepancy: if meal attendance count > roll call present count = anomaly (extra food claimed); flagged for review
- State-specific POSHAN portal export formats supported

---

## 77. Disciplinary Action Log

Each hostel violation logged with full detail:

| Severity | Examples | Action |
|---|---|---|
| Minor | Noise after curfew, untidy room | Verbal warning |
| Moderate | 3rd late return, minor mess rule violation | Written warning + parent intimation |
| Serious | Unauthorized exit, bringing alcohol/tobacco | Parent meeting + disciplinary committee |
| Severe | Ragging, drug use, unauthorized visitor in room, violence | Hostel suspension or expulsion |

- All actions recorded: violation, evidence, witness, action taken, date, follow-up
- Parent notified in-app for all serious and severe cases
- Disciplinary record linked to student profile (Module 07); considered in scholarship and certificate decisions

---

## 78. Hostel Discipline Committee

- Formal committee: Chief Warden, Principal, one senior faculty member, one non-teaching staff representative
- Serious cases referred by block warden; committee convened within 72 hours
- Hearing process: student presents explanation; warden presents evidence; committee deliberates
- Outcomes:
  - Hostel suspension (temporary removal from hostel; student continues studies as day scholar)
  - Hostel expulsion (permanent removal)
  - Probation (remain in hostel under intensified monitoring — Point 106)
  - No action (case dismissed)
- Outcome recorded in student's hostel disciplinary record; Principal countersigns
- Expelled student: TC process (Module 07) initiated if student cannot continue as day scholar

---

## 79. Prohibited Items Confiscation Log

- Prohibited items found during room inspection:
  - Alcohol, tobacco, drugs, weapons, excessive cash
  - Opposite-gender clothing (co-ed hostels with strict norms)
  - Unapproved electrical appliances (immersion rods, kettles — fire hazard)
  - Pets
- Confiscation logged: item description, quantity, date, room, student name
- Item retained by warden; parent notified
- Disciplinary action linked (Point 77)
- Repeated offence: escalated to discipline committee (Point 78)

---

## 80. Hostel Safety Compliance Checklist

Monthly checklist completed by warden (digitally in app):

| Item | Frequency |
|---|---|
| Fire extinguisher inspection date and pressure check | Monthly |
| Emergency exit signage visibility | Monthly |
| First aid kit: items present and in-date | Monthly |
| Electrical safety: no exposed wiring | Monthly |
| Water quality: tanker/supply cleanliness | Monthly |
| Pest control: last treatment date | Monthly |
| CCTV cameras: all functional | Monthly |
| Emergency lighting: functional | Monthly |

- Overdue items flagged to Principal at 7-day overdue
- Safety inspection records required for: fire department NOC renewal, NAAC inspection, insurance, NHRC inspection

---

## 81. Fire Extinguisher Maintenance Log

- Each fire extinguisher tagged with a unique ID (block + floor + location)
- Record per extinguisher: installation date, last service date, next service due, pressure rating
- Auto-alert to Chief Warden 30 days before service due date
- Post-drill check: any extinguisher used in drill is serviced and recharged before next drill
- Annual hydrostatic test record maintained per NBC 2016 requirements

---

## 82. Emergency Evacuation Map — Digital Record

- Evacuation plan per building floor registered in system (floor plan with exit routes marked)
- Updated annually or when building layout changes
- Accessible to: all wardens (in-app), security staff
- Displayed on hostel notice board (physical); digital copy in warden app
- Fire drill after evacuation map update: ensures new layout is practiced
- NAAC / fire department inspection: evacuation map submitted as compliance document

---

## 83. Hostel Occupancy Heatmap

Visual analytics showing:
- Occupancy by: day of week, week of month, month of year
- Patterns visible:
  - Festival season: very low (80–90% on leave)
  - Exam season: very high / mandatory stay
  - Weekend: moderate dip (local leave / home leave)
  - Summer / winter vacation: zero or skeleton occupancy
- Used for: staff rostering, mess planning, infrastructure maintenance scheduling (low occupancy = maintenance window)
- Branch/block-level drill-down available

---

## 84. Night Roll Call Compliance Rate

Monthly report per warden:
- Roll calls conducted on time (%) vs delayed (%) vs missed (%)
- Average roll call completion time (from start to submission of full block result)
- Rooms not visited during rounds (% of total)
- Anomalies flagged vs anomalies investigated

Available to: Chief Warden, Principal
Input to warden performance report (Point 31)
Persistent low compliance = warden performance issue; Principal review initiated

---

## 85. Monthly Attendance Summary for Parent

Sent to parent of residential students (all ages — residential school, college hostel, coaching hostel):
- Nights present in hostel
- Nights on approved leave (home/medical/official)
- Unexpected absences (if any)
- Meal attendance % (breakfast, lunch, dinner separately)
- Any disciplinary incidents (summary only — details available on request from Principal)
- Gate passes used: count and types

Sent as in-app report on the 1st of each month for the previous month.
Builds parent trust; reduces parental anxiety about residential students; reduces surprise phone calls to warden.

---

## 86. Long-Term Absence Pattern Detection

- Student taking frequent short leaves (e.g., every other weekend, every Friday):
  - System identifies pattern: X leaves in last Y weeks
  - Warden + counsellor alerted: possible homesickness, hostel discomfort, academic difficulty, personal issue
- Student accumulating leave quota rapidly: flag to warden before quota exhausted
- Pattern report available to counsellor (Module 32) for targeted wellness intervention
- Leave pattern included in student's mid-term welfare review

---

## 87. Hostel Annual Inspection Report

Inspection by: State Government, UGC, AICTE, NHRC, NCPCR (National Commission for Protection of Child Rights):
- Instant comprehensive report generated:
  - Current occupancy and bed utilisation
  - Warden staffing (ratio compliance)
  - Safety compliance (fire, CCTV, first aid)
  - POCSO measures implemented
  - Anti-ragging measures (for college hostels)
  - Grievance register (Point 103 — count and resolution rate)
  - Night roll call compliance rate
  - Visitor log summary
  - Disciplinary incidents (count and outcomes)
- Report available for: immediate printout during inspection; email to inspector; portal upload
- Inspection log: date, authority, inspector name, documents provided, observations, action items with deadlines

---

## 88. Coaching Hostel Linked to Batch Attendance (Module 12)

- Coaching session attendance (Module 12) and hostel night roll call cross-referenced:
  - Student present in coaching session but absent from previous night's hostel roll call (no gate pass) = anomaly
  - Student marked in night roll call but absent from all coaching sessions that day = wellness concern
- Anomaly report generated daily; center admin + warden jointly review
- Prevents scenarios where student is counted present in academic records but has actually left campus

---

## 89. Mess Biometric Cross-Reference

- Student present at mess (lunch biometric) but absent from morning coaching/academic session (no gate pass) = "bunking class" anomaly
- Student absent from mess (dinner) but present in night roll call = wellness concern (not eating)
- Both anomaly types alerted to warden:
  - Class bunking: center admin + warden
  - Not eating: warden + medical officer
- Anomaly log maintained; patterns (consistent meal skipping = potential eating disorder or financial difficulty) flagged to counsellor

---

## 90. Mandatory Recreation Time Compliance

- Rajasthan Coaching Regulation Act 2023 mandate: minimum 1-hour recreation/sports time per day
- Recreation sessions tracked by hostel PE teacher / warden:
  - Activities: outdoor sports, indoor games, walking, yoga
  - Attendance marked per session
- Monthly compliance report: total recreation hours per student; minimum 22 hours/month (1 hr × 22 working days)
- Submitted to state authority as part of coaching regulation compliance
- Students below minimum: counsellor follow-up (possible physical health concern or disengagement)

---

## 91. Mental Health Welfare Round

- Mandatory warden welfare round (beyond standard night roll call):
  - Warden visits each room for a brief check-in conversation
  - Frequency: weekly minimum (coaching hostels: daily recommended)
  - Observations logged: student demeanour, any concerning statements, signs of stress/depression
- Student expressing distress: immediate referral to counsellor (Module 32)
- Welfare round log maintained separately from roll call log; restricted access (counsellor + Principal + Chief Warden)
- Required for NHRC / Rajasthan Coaching Regulation compliance reporting

---

## 92. Anti-Ragging Digital Undertaking

- Mandatory per **Supreme Court of India order (SLP 24295/2006)** and **UGC Anti-Ragging Regulations 2009**:
  - Every hostel student AND parent must sign anti-ragging undertaking before hostel allotment
  - Digital signature via EduForge app; timestamp recorded
  - Undertaking text: UGC-prescribed standard text (not customizable)
  - **Hostel admission hard-blocked until both student and parent sign**
- Signed undertakings stored digitally with timestamps; produced during UGC/NHRC inspection
- Annual renewal: at start of each academic year, fresh undertaking required
- UGC portal submission: undertaking count submitted to UGC Anti-Ragging Cell

---

## 93. Senior-Fresher Floor Separation

- First-year / fresher students allotted to designated floors or blocks
- Senior students **cannot enter fresher floors** without written warden permission (entry logged)
- Biometric gate at floor access restricted to room occupants and wardens only
- Any senior student found on fresher floor without permission: incident report; anti-ragging committee notified
- Fresher floor warden designated specifically to monitor first-year student welfare
- Senior mentors (if institution allows): approved in advance; visits supervised and logged

---

## 94. Anti-Ragging Night Round

- Warden conducts dedicated anti-ragging check during night rounds:
  - Separate from general welfare round
  - Specifically checks: no seniors in fresher rooms, no group intimidation in common areas, no physical or verbal harassment
  - Any observation: immediately reported to anti-ragging committee (not handled by warden alone)
- Logged as "Anti-Ragging Round" in warden's nightly log
- Frequency: daily for first 2 months of academic year; weekly thereafter (peak ragging risk is early in year)
- Anti-ragging round completion rate included in warden performance report (Point 31)

---

## 95. Anonymous Ragging Report

- In-app anonymous button: "Report Ragging"
- Report goes directly to: Principal + anti-ragging committee + institution's UGC Anti-Ragging Cell coordinator
- **Not routed through any warden** (prevents suppression if warden is complicit or ineffective)
- Report contains: location (floor/block, approximate), description, date/time; no reporter identity stored
- Response protocol: anti-ragging committee responds within 24 hours; inquiry initiated
- UGC helpline number **1800-180-5522** displayed prominently in hostel section of student app
- Report to UGC National Anti-Ragging Helpline if institution fails to act within 7 days: student guided to escalate

---

## 96. Warden-to-Student Ratio Compliance

- **UGC Hostel Development Guidelines 2018**: minimum 1 warden per 50 students
- System calculates current ratio per hostel:
  - Active wardens (excluding on-leave) / current occupancy
- Ratio displayed on hostel dashboard
- Non-compliance alert:
  - 1:60 — advisory warning
  - 1:70 — compliance alert to Principal
  - 1:80+ — management escalation; UGC compliance risk
- Lady warden-specific ratio for girls' hostel tracked separately
- Warden vacancy (resignation, transfer) immediately recalculates ratio; alert if ratio breaches on vacancy

---

## 97. Local Guardian Designation

- For students whose parents are abroad (NRI), deceased, or physically incapacitated:
  - A local guardian designated at hostel admission
  - Guardian details: name, relationship, address, phone, government ID proof (Aadhaar / PAN)
  - Guardian has same approval authority as parent for: gate pass confirmation, outstation leave, emergency contact
- System distinguishes: parent (primary) vs local guardian (secondary / proxy)
- Guardian contact verified at admission; must be updated when guardian changes (Point 105)
- For NRI parents: Indian mobile number for emergency contact mandatory (in addition to overseas number)

---

## 98. International Student Hostel FRRO Compliance

- Foreign students (students on Student Visa) must reside at their registered address (hostel):
  - Hostel check-in recorded as residence registration for FRRO purposes
  - FRRO registration must be done within 14 days of arrival (if from FRRO-mandated countries); hostel admin tracks compliance
  - Passport number, visa number, visa expiry date stored in student hostel profile
- Prolonged unauthorized absence (student not in hostel, no gate pass) = potential visa condition violation:
  - Alert to International Students Office
  - FRRO reporting obligation triggered if absence > 7 days
- Check-out on graduation / course completion: FRRO intimation required; system generates departure letter for FRRO

---

## 99. Night Study Room

- Designated room for students who need to study after lights-out time:
  - Capacity limited (e.g., 10–20 students per block)
  - Sign-in required via app: student books a slot (start time, expected end time)
  - Sign-out required when leaving study room
- Study room log maintained: student name, entry, exit, warden on duty
- Night warden monitors study room during rounds
- Study room access automatically revoked during exam mandatory stay-in period (no need — regular room study during exams)
- Usage pattern: high frequency = serious student; reported positively in student profile

---

## 100. Hostel Allotment Waiting List

- When hostel is full: waiting list maintained with priority criteria:

| Priority | Criterion |
|---|---|
| P1 | Distance from institution > 100 km |
| P2 | Girl student (institutional priority for safety) |
| P3 | SC / ST category (government mandate) |
| P4 | OBC / EWS category |
| P5 | Differently-abled (CWSN) |
| P6 | Sports quota |
| P7 | Merit-based (top academic performers) |
| P8 | First-come-first-served (remaining seats) |

- Vacancy notification: when a bed becomes available, highest-priority waitlisted student notified in-app; 48-hour window to confirm; if no response, next candidate offered

---

## 101. Temporary Exam-Period Hostel Admission

- Day scholars can apply for short-term hostel stay during board/semester exam periods:
  - Purpose: avoid long commute risk; ensure rest before exam
  - Duration: exam period start to exam period end
  - Hostel fee: prorated for days stayed (linked to Module 25)
  - Standard hostel rules apply; temporary residents follow same gate pass, curfew, roll call rules
  - Temporary resident status: "Temp Resident" flag in room assignment; separate from permanent residents

---

## 102. Hostel Grievance System

- Student can raise a grievance about hostel via in-app:
  - Category: food quality, room maintenance, warden behaviour, peer conflict, safety concern, facilities, discrimination
  - Anonymous option available for sensitive complaints
- Grievance workflow:
  1. Submitted → Chief Warden receives
  2. Chief Warden assigns to relevant staff
  3. Resolution within 7 days (configurable)
  4. Student notified of resolution
  5. Student can escalate if unsatisfied → Principal
- Overdue grievances (> 7 days unresolved): auto-escalation to Principal
- Monthly grievance report: total raised, categories, resolution rate, pending items; required for NAAC and UGC inspection

---

## 103. Hostel Attendance Certificate

- Students on government hostel stipend schemes need hostel attendance certificate for scholarship renewal
- Certificate includes:
  - Student name, class/course, hostel name, room number
  - Academic year and term
  - Total nights present / total working nights
  - Attendance %
  - Chief Warden's digital signature + institution stamp
- Python generates PDF; accessible in student's document store (Module 40)
- Government scheme format variants supported (different states have different prescribed formats)

---

## 104. Emergency Contact Staleness Alert

- If parent/guardian emergency contact details not updated for > 6 months: alert to warden and admin
- Outstation and home gate passes blocked until contact details verified
- Contact verification: admin calls the listed number; confirmed = record updated with verification date
- If contact is unreachable (disconnected, wrong number): admin contacts student for updated number; updated before any leave approval
- Prevents hostel from attempting to contact a disconnected number during a real emergency

---

## 105. Hostel Suspension and Readmission

- Student suspended from hostel for serious disciplinary violation:
  - Suspension period: typically 1 month to 1 semester
  - Student continues academics as day scholar during suspension
  - Hostel room allocated to waitlisted student during suspension
- Readmission after suspension:
  - Disciplinary committee clearance required
  - Parent meeting mandatory (both parents or guardian present)
  - Written undertaking: student commits to rules compliance; counter-signed by parent
  - Probationary period: typically 1 term; intensified monitoring
  - Probationary status flagged on warden dashboard: extra attention during rounds
- Repeat serious violation during probation: permanent hostel expulsion

---

## 106. Student Group Insurance

- Group accident and health insurance policy for all hostel students (mandated by several states and UGC guidelines):
  - Coverage: accident, hospitalisation, emergency medical treatment
  - Policy details stored per student: policy number, insurer name, coverage period, coverage amount
  - Nominee / beneficiary: parent/guardian
- Medical emergency (Point 51): insurance information retrieved instantly for hospital admission procedures
- Claim initiation: incident report from hostel + student identity + medical records → insurance claim process
- Claim status tracked in student hostel record; outcome logged
- Annual policy renewal: admin notified 60 days before expiry

---

## 107. Gender-Neutral / Transgender Student Accommodation

- Per **NEP 2020** and **UGC Guidelines on Transgender Persons in Higher Education (2022)**:
  - Institution must provide appropriate, comfortable accommodation for transgender students
  - Accommodation options:
    - Designated gender-neutral room/block
    - Placement based on student's self-identified gender (with consent)
    - Single occupancy room option (where available)
  - No forced placement without student's consent
- Accommodation preference captured at admission: classified as DPDPA sensitive personal data; restricted access
- Warden trained in transgender-inclusive behaviour (training record linked to Module 08)
- Any discrimination complaint: POCSO equivalent path + UGC Grievance Portal

---

## 108. SAI / Sports Hostel Training Attendance Linkage

- Student-athlete: mandatory training sessions twice daily (morning + evening)
- Training attendance taken by coach in sports module
- Cross-reference with hostel roll call:
  - Present in hostel night roll call = must attend morning training (unless medical excuse)
  - Absent from training without medical excuse = sports scholarship review trigger
- Persistent training absence: national sports federation notified (for SAI students)
- Match/competition travel: official gate pass issued; hostel attendance = OD during travel dates
- Training attendance feeds performance tracking in Module 47 AI Performance Analytics

---

## 109. Hostel Attendance Impact on TC / Certificates

- Student cannot receive TC, migration certificate, or degree certificate until:
  - All hostel nights accounted for (no unexplained extended absences)
  - All dues cleared (Point 110)
  - Room inspection completed and signed off
  - Anti-ragging undertaking for departing year on record
- Hostel clearance certificate generated by Chief Warden after all conditions met
- Clearance certificate is a prerequisite for: TC issuance (Module 07), migration certificate, degree certificate (Module 39)
- Without clearance: certificate issuance blocked in system

---

## 110. Hostel Dues Clearance Certificate

- Student leaving hostel (permanently or on TC) must clear all hostel dues:

| Due Type | Source |
|---|---|
| Hostel room fee outstanding | Module 25 Fee Collection |
| Mess fee outstanding | Mess attendance record |
| Damage charges | Room inspection report + inventory |
| Unreturned library books | Module 30 Library |
| Unreturned sports equipment | Sports inventory |
| Security deposit forfeiture (if any) | Calculated vs damage |
| Security deposit refund (if clean) | Net of deductions |

- Clearance certificate generated when all dues = ₹0 or disputed dues resolved
- Linked to Module 07 TC issuance (hard block without clearance)
- Dispute resolution: Chief Warden arbitrates; Management as final authority

---

## DB Schema (Core Tables)

```
hostel.hostel_blocks
  id, tenant_id, branch_id, block_name, block_type (boys/girls/mixed/
  gender_neutral), floors, total_rooms, total_beds, warden_id,
  lady_warden_id, status (active/closed/renovation)

hostel.hostel_rooms
  id, hostel_block_id, floor_number, room_number, room_type
  (single/double/triple/dormitory), bed_count, room_condition,
  qr_code_ref, created_at

hostel.hostel_assignments
  id, tenant_id, student_id, hostel_block_id, room_id, bed_number,
  effective_from, effective_to, key_serial_number, key_issued_at,
  key_returned_at, assigned_by, status (active/vacated/suspended)

hostel.roll_calls
  id, hostel_block_id, roll_call_date, roll_call_type
  (night/morning/spot_check/fire_drill/anti_ragging),
  roll_call_time, conducted_by_warden_id, submitted_at,
  completion_status (complete/incomplete/substituted)

hostel.roll_call_entries
  id, roll_call_id, student_id, status (present/absent/on_leave/
  sick_bay/medical_emergency/od/temp_absent/vacation_resident),
  notes, marked_at

hostel.gate_passes
  id, tenant_id, student_id, gate_pass_type
  (local/outstation/medical/official/emergency),
  destination, travel_mode, applied_at, departure_date,
  departure_time, return_date, return_time_expected,
  parent_confirmed_at, approved_by_warden_id, approved_at,
  qr_code, exit_scanned_at, return_scanned_at,
  actual_return_time, late_return_minutes,
  status (pending/approved/rejected/active/returned/overdue)

hostel.leave_applications
  id, tenant_id, student_id, leave_type (home/medical/official/
  emergency/festival/vacation), from_date, to_date, reason,
  applied_by (student/parent/admin), parent_confirmed_at,
  warden_approved_by, principal_approved_by (if > 3 days),
  status (pending/approved/rejected/extended), extension_to_date,
  created_at

hostel.meal_attendance
  id, tenant_id, student_id, meal_date, meal_type
  (breakfast/lunch/evening_snack/dinner),
  status (present/opted_out/sick_bay_delivery/not_marked),
  marked_by, marked_at

hostel.visitor_log
  id, tenant_id, student_id, visitor_name, relationship,
  id_type, id_number, entry_time, exit_time, purpose,
  is_on_approved_list (bool), approved_by_security,
  items_brought (JSON), warden_notified (bool)

hostel.disciplinary_cases
  id, tenant_id, student_id, violation_type, violation_date,
  reported_by, evidence_notes, action_taken, parent_notified_at,
  committee_referral (bool), committee_decision,
  suspension_from, suspension_to, expulsion (bool),
  probation (bool), probation_end_date, created_at

hostel.welfare_checks
  id, tenant_id, student_id, trigger_type
  (absent_roll_call/consecutive_absent/cross_module_flag/
  meal_skip_pattern/leave_pattern/mental_health/sos),
  trigger_date, assigned_to (counsellor_id + warden_id),
  action_log (JSON), outcome, resolved_at

hostel.safety_compliance
  id, hostel_block_id, check_date, checked_by_warden_id,
  fire_extinguisher_ok (bool), emergency_exit_ok (bool),
  first_aid_ok (bool), electrical_ok (bool), water_quality_ok (bool),
  pest_control_ok (bool), cctv_ok (bool), emergency_lighting_ok (bool),
  issues_found (text), next_due_date

hostel.clearance_records
  id, tenant_id, student_id, hostel_block_id, room_id,
  checkout_date, room_inspection_ok (bool), inventory_cleared (bool),
  key_returned (bool), dues_amount, dues_cleared (bool),
  security_deposit_refund, clearance_certificate_issued_at,
  issued_by

hostel.anti_ragging_undertakings
  id, tenant_id, student_id, academic_year_id,
  student_signed_at, parent_signed_at,
  undertaking_version, ugc_submission_ref
```

---

## Integration Map

| Module | How |
|---|---|
| 05 — Academic Year & Calendar | Festival leave calendar sync; exam period stay-in lock |
| 07 — Student Enrolment | Student profile, room assignment, TC clearance |
| 08 — Staff Management | Warden assignment, lady warden compliance, staff attendance |
| 09 — Parent & Guardian | Parent notifications, gate pass confirmation, approved visitor list |
| 11 — Attendance School/College | Academic attendance coordination; leave sync; double-absence flag |
| 12 — Attendance Coaching | Batch attendance cross-reference; mess anomaly detection |
| 24 — Fee Structure | Hostel fee, mess fee, security deposit structure |
| 25 — Fee Collection | Dues clearance; mess fee adjustment; refunds; security deposit |
| 28 — Hostel Management | Room inventory, maintenance requests, hostel facilities |
| 29 — Transport | Gate pass exit transport booking; field trip coordination |
| 30 — Library | Library book dues for clearance certificate |
| 32 — Counselling | Welfare checks, mental health referrals, re-integration plans |
| 35 — Notifications | Gate pass alerts, late return alerts, absence notifications to parents |
| 39 — Certificates | Hostel clearance certificate; NCC/sports certificates |
| 40 — Document Management | Anti-ragging undertakings, clearance certificates, inspection reports |
| 41 — POCSO Compliance | POCSO complaints from hostel, girls' hostel safety, CCTV records |
| 45 — Live Classes | Online class attendance coordination for hostel students |
| 47 — AI Performance Analytics | Attendance + training attendance for sports students |
