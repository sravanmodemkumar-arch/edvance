# EduForge — Module 05: Academic Year & Calendar

> Every institution on EduForge has its own independent academic year.
> Schools, colleges, and coaching institutes all operate on different calendars —
> the platform supports all structures without forcing a common pattern.

---

## Academic Year Definition

| Item | Decision |
|---|---|
| Scope | Per institution — fully independent |
| Active year | Only one active academic year per institution at a time |
| Label | Auto-generated — "2024–25" from start + end year |
| Data tagging | Every record (attendance, fee, exam, result) tagged to academic year |
| Year boundary | All modules operate strictly within active year boundary |
| Coaching | Batch-based — no academic year concept |

### Year Start Month — By Institution Type

| Institution Type | Suggested Start Month |
|---|---|
| CBSE School | April |
| ICSE School | April |
| State Board School | June / July (varies by state) |
| Intermediate College | June |
| Degree / Engineering College | July / August |
| Medical College | August |
| ITI / Polytechnic | August |
| Coaching (batch) | Any month — batch decides |

- Admin sets start month at institution setup
- Suggestion shown — admin can override to any month
- Start month locked after Principal + Management approval
- Change after lock: Principal + Management approval only

---

## Academic Structure Types

Admin selects structure type at institution setup. Platform adapts exam scheduling, attendance reports, and results based on selected structure.

| # | Structure | Who Uses | Divisions |
|---|---|---|---|
| 1 | Terms | Schools (CBSE, ICSE, State Board) | 2 or 3 terms per year |
| 2 | Semesters | Modern degree / engineering / medical colleges | 2 semesters per year |
| 3 | Annual | Old / traditional colleges — no mid-point | 1 — year-end exam only |
| 4 | Continuous | Autonomous colleges — no fixed division | Rolling assessment |
| 5 | Batch-based | Coaching institutes | Batch start to batch end |

### Combined Structure

- Some institutions have multiple structures — e.g. B.Com Annual + B.Tech Semester in same college
- Admin selects multiple structures per course / department
- Change requires Principal + Management approval only — EduForge not required

### How Structure Affects Platform

| Structure | Attendance Report | Exams | Results |
|---|---|---|---|
| Terms | Per term | Per term | Per term |
| Semesters | Per semester | Per semester | Per semester |
| Annual | Full year | Year-end only | Once per year |
| Continuous | Rolling | As scheduled | As scheduled |
| Batch-based | Per batch | As scheduled | Per batch |

### Number of Terms / Semesters

| Structure | Count | Notes |
|---|---|---|
| Terms | 2 or 3 | Admin sets at setup |
| Semesters | 2 per year | Standard |
| Annual | 1 | No division |
| Polytechnic | 6 total — 2 per year | 3-year diploma |
| Continuous / Batch | Not applicable | — |

- Each term / semester has: name, start date, end date, break dates
- Auto-named: Term 1 / Term 2 / Semester 1 / Semester 2
- Admin can rename: "First Term", "Monsoon Semester", etc.

---

## Coaching Batch Calendar

Coaching institutes are batch-based — completely different from school / college calendar.

| Item | Details |
|---|---|
| No academic year | Coaching runs on batch calendar — not year calendar |
| Batch definition | Batch name + target exam + start date + end date |
| Multiple batches | Multiple active batches simultaneously — each independent |
| Example | JEE 2025 Batch — July 2023 → March 2025 |
| Schedule | Each batch has own timetable, test series, holidays |
| Batch holidays | Set per batch — not institution-wide |
| Batch closure | Batch ends after target exam — archived |
| New batch | Can start any month — no fixed cycle |
| Sunday classes | Regular — batch admin marks Sunday as working day |

---

## Working Days Configuration

| Pattern | Who Uses |
|---|---|
| Monday – Friday | Some CBSE schools, colleges |
| Monday – Saturday | Most state board schools, coaching |
| Alternate Saturdays | Many urban schools — 2nd and 4th Saturday off |
| Monday – Friday + selected Saturdays | Some colleges |

- Admin configures at setup
- Working day count: auto-calculated — drives attendance % denominator
- Change: Principal + Management approval

### Saturday Rule

| Item | Decision |
|---|---|
| Who decides | Principal |
| Options | All Saturdays working / All off / 2nd & 4th off / 1st & 3rd off / Selected |
| Configuration | Principal sets at academic year start |
| Auto-calculation | Platform auto-marks selected Saturdays for full year |
| Change mid-year | Principal + Management approval |

### Two-Shift Institutions

| Item | Details |
|---|---|
| Shift A | Morning — e.g. 7 AM → 12 PM |
| Shift B | Afternoon — e.g. 12 PM → 5 PM |
| Separate calendars | Each shift has own timetable + attendance |
| Common holidays | Both shifts share same holiday calendar |
| Working day count | Same for both shifts |

---

## Holiday Management

### Holiday Entry Rule

| Holiday Type | Who Enters | Who Approves |
|---|---|---|
| National holidays | Institution admin | Principal |
| State holidays | Institution admin | Principal |
| GO-mandated dates | Institution admin | Principal |
| Board / university dates | Institution admin | Principal |
| Institution-specific holidays | Institution admin | Principal |
| Summer / winter / festival breaks | Institution admin | Principal |
| Emergency closures | Institution admin | Principal |
| Study holidays | Institution admin | Principal |

> All holidays entered by institution admin — approved by Principal.
> Platform does not auto pre-load any holidays.

### National Holidays

| Category | Holidays |
|---|---|
| National | Republic Day (26 Jan), Independence Day (15 Aug), Gandhi Jayanti (2 Oct) |
| Hindu | Holi, Ram Navami, Janmashtami, Dussehra, Diwali, Mahavir Jayanti, Buddha Purnima |
| Muslim | Eid-ul-Fitr, Eid-ul-Adha, Muharram, Milad-un-Nabi |
| Sikh | Guru Nanak Jayanti, Baisakhi |
| Christian | Good Friday, Christmas (25 Dec) |
| National Leaders | Ambedkar Jayanti (14 Apr) |
| New Year | 1 January |

- Floating holidays (Eid, Holi, Diwali) — admin enters correct date each year
- Admin can remove any holiday — Principal approval
- Working day counter auto-adjusts

### State Holidays

- Admin enters state-specific holidays manually
- Applicable to schools + colleges only
- Examples by state:

| State | State-Specific Holidays |
|---|---|
| Telangana / AP | Ugadi, Bathukamma, Bonalu, Formation Day |
| Tamil Nadu | Pongal, Tamil New Year, Puthandu |
| Maharashtra | Gudi Padwa, Chhatrapati Shivaji Jayanti |
| Kerala | Onam, Vishu |
| Punjab | Baisakhi, Lohri |
| West Bengal | Durga Puja, Rabindra Jayanti |
| Karnataka | Rajyotsava Day, Ugadi |
| Gujarat | Uttarayan, Gujarat Formation Day |
| Assam | Bihu |

### Government Order (GO) Based Calendar

| Item | Details |
|---|---|
| GO issued by | State education department |
| Content | Academic year start, mandatory holidays, exam schedule, vacation dates |
| Who enters | Institution admin |
| Approval | Principal |
| Applicable to | State board schools + government colleges only |
| CBSE / ICSE | Follow board circulars — not state GO |
| Private unaided | Can follow own calendar |

### Board / University Calendar

| Board / University | What They Publish |
|---|---|
| CBSE | Board exam dates, practical dates, result dates |
| ICSE | Board exam dates, practical dates |
| State Board | Class 10 & 12 exam dates, holidays |
| University (affiliated) | Semester start/end, exam dates, result dates |

- Admin enters board / university published dates
- Principal approves
- These dates locked after approval
- Internal exam dates: institution schedules around board dates
- Conflict check: internal exam on board exam date → system warns

### Institution-Specific Holidays

| Type | Examples |
|---|---|
| Founder's Day | Institution anniversary |
| Local festival | Village fair, temple festival |
| Sports Day | Full day event — no classes |
| Annual Day | School function |
| Staff Training Day | Teachers in training — students holiday |
| Inspection Day | NAAC, NABET, board inspection |
| Local elections | District / municipal election |
| Bandh / Strike | Admin declares closure |

### Vacation Breaks

| Break | Typical Duration | Applicable To |
|---|---|---|
| Summer vacation | 30–60 days | Schools — May/June |
| Winter break | 7–15 days | Schools — December |
| Diwali break | 3–7 days | All institutions |
| Pongal / Sankranti break | 3–5 days | South Indian institutions |
| Eid break | 2–3 days | All institutions |
| Mid-term break | 3–5 days | Between terms / semesters |
| Study holidays | 7–15 days | Colleges — before exams |

### Special Day Types

| Special Day | Effect |
|---|---|
| Sports Day | No regular classes — full day event |
| Annual Day | No regular classes — full day event |
| PTM Day | Half day or full day — no regular classes |
| Teachers Day | Modified schedule |
| Children's Day | Modified schedule |
| Inspection Day | Normal classes — staff prepared |
| Inter-school event | Selected students on-duty |
| Cultural Program | Half day — modified schedule |
| Revision Period | Modified timetable — subject-wise revision |

### Half Days

| Item | Details |
|---|---|
| Types | Morning half day / Afternoon half day |
| Working day count | Counted as 0.5 working day |
| Attendance | Marked for active session only |
| Timetable | Affected periods auto-cancelled |

### Compensatory Working Days

| Item | Details |
|---|---|
| Purpose | Compensate for lost working day due to holiday |
| Example | Diwali holiday on Wednesday → Saturday becomes working day |
| Working day count | Compensatory day added to counter |
| Attendance | Marked normally |

### Public Holiday Falling on Sunday

| Item | Details |
|---|---|
| Rule | If public holiday falls on Sunday → next Monday declared holiday |
| Control | Admin enables/disables rule — Principal approves |
| State-specific | Not forced — institution decides |
| Auto-flag | If rule enabled — platform flags when holiday falls on Sunday |

### Emergency Closures

| Type | Who Declares | Approval | Online Classes |
|---|---|---|---|
| Weather-based (heat, cyclone, rain) | Institution admin | Principal | Principal decides |
| State-wide emergency (COVID, flood) | Institution admin | Principal | Principal decides |
| Bandh / strike | Institution admin | Principal | Principal decides |
| Same-day closure | Institution admin | Principal within 2 hours | Principal decides |

### Staff Training / CPD Days

| Item | Details |
|---|---|
| Effect on students | Holiday — no classes |
| Effect on staff | Working day — training / meeting |
| Attendance | Staff marked — student not marked |
| Working day count | Not counted for students — counted for staff |

### Year-Round Institution

| Item | Details |
|---|---|
| Configuration | Admin marks at setup |
| Summer vacation | Not applicable |
| Working days | Higher count |
| Holidays | National, state, institution-specific only |
| Attendance % | Calculated on higher working day count |

---

## Calendar Approval Workflow

| Step | Who | Action |
|---|---|---|
| 1 | Institution admin | Prepares full year calendar |
| 2 | Principal | Reviews + approves |
| 3 | System | Calendar published — visible to staff, students, parents |

### Calendar Freeze

| Item | Details |
|---|---|
| Freeze trigger | Principal approval |
| Changes after freeze | Admin submits → Principal → Management approves |
| Past dates | Cannot be changed — ever |
| Future dates | Can be changed — Principal + Management approval |
| Emergency same-day | Principal approves — Management informed |
| Audit | Every change logged |

### Retroactive Changes

| Item | Decision |
|---|---|
| Past holidays | Cannot be added or removed — ever |
| Past working days | Cannot be changed |
| Past attendance | Not affected by any change |
| Reason | Prevents manipulation of attendance % |
| Exception | None — no retroactive changes allowed |

---

## Calendar Sync

### Sync with Attendance Module

| Calendar Event | Attendance Effect |
|---|---|
| Holiday declared | Attendance blocked — cannot mark |
| Holiday removed | Attendance re-enabled |
| Working day added | Attendance opens |
| Half day | Active session only |
| Emergency closure | Blocked same day — retroactive |
| Working day counter | Updates instantly |

### Sync with Exam Module

| Calendar Event | Exam Effect |
|---|---|
| Holiday | Cannot schedule exam |
| Break period | Cannot schedule exam |
| Board exam dates | Internal exams blocked on those dates |
| Exam conflict | System warns if two exams clash |
| Emergency closure | Exam auto-postponed — admin reschedules |

### Sync with Fee Module

| Calendar Event | Fee Effect |
|---|---|
| Fee due date on holiday | System warns — suggests next working day |
| Fee due date on exam day | System warns |
| Late fee trigger | Starts from next working day after due date |
| Academic year end | All pending fees flagged |

### Sync with Timetable Module

| Calendar Event | Timetable Effect |
|---|---|
| Holiday | All periods auto-cancelled |
| Half day | Morning or afternoon periods cancelled |
| Special day | Affected periods suspended |
| Exam day | Regular timetable replaced by exam schedule |
| Emergency closure | All periods cancelled |
| Compensatory day | Regular timetable applies |

---

## Working Day Counter

| Item | Details |
|---|---|
| Auto-calculated | Counts working days from year start to current date |
| Excludes | Holidays, breaks, half days (0.5), emergency closures |
| Includes | Compensatory working days |
| Per institution | Each institution has own count |
| Per shift | Two-shift institutions track separately |
| Per class | Class 10, 12 may differ due to board exams |
| Attendance % | Days present ÷ Working days × 100 |
| Real-time | Updates automatically on any calendar change |

---

## Exam-Specific Calendar Rules

### Exam Blackout Period

| Item | Details |
|---|---|
| Trigger | Admin marks exam dates |
| Effect | No sports day, PTM, events during exam period |
| System check | Blocks + warns if event scheduled during blackout |
| Exception | Emergency closure only — Principal + Management |

### Section-Specific Exam Dates

| Item | Details |
|---|---|
| Example | Class 10 Section A — Maths Monday, Section B — Tuesday |
| Reason | Hall capacity, invigilator availability |
| Calendar | Each section sees own exam dates |
| Conflict check | System ensures no student in two exams same time |

### Pre-Board Exam Dates

| Item | Details |
|---|---|
| Applicable | Class 10 + Class 12 only |
| Timing | 1–2 months before actual board exam |
| Calendar entry | Marked separately from main exams |
| Blackout | Pre-board period blocked for other events |
| Results | Published before board exam |

### Re-exam / Supplementary Exam

| Item | Details |
|---|---|
| Timing | After main results published |
| Eligible | Failed students only — system auto-identifies |
| Blackout | Re-exam period blocked for other events |
| Hall ticket | New hall ticket generated |

### Online Exam Time Slots

| Item | Details |
|---|---|
| Time slot | Admin sets start time + end time |
| Window | Student must start within entry window |
| Late entry | Cannot join after window closes |
| Multiple slots | Different slots for different sections |
| Reminder | In-app 1 hour before exam |
| Conflict check | No student in two online exams simultaneously |

### Study Holidays

| Item | Details |
|---|---|
| Purpose | Students study at home — no classes |
| Duration | 7–15 days before exams |
| Attendance | Not marked |
| Working day count | Not counted |
| Applicable | Colleges + Intermediate — not primary/secondary schools |

---

## Multi-Branch Calendar

| Item | Details |
|---|---|
| Base calendar | Group admin sets common holidays for all branches |
| Branch override | Each branch admin adds local holidays |
| Group holidays | Mandatory — all branches follow |
| Branch-specific | Optional — local festivals, events |
| Group view | Group admin sees consolidated calendar |
| Conflict check | Group admin notified of branch conflicts |

---

## Special Calendar Features

### Hostel Calendar

| Item | Details |
|---|---|
| Common holidays | Applies to both hostelers and day scholars |
| Hostel-specific | Mess timings, warden rounds, hostel events |
| Night attendance | Warden marks separately |
| Applicable | Only if hostel module enabled |

### Online vs Offline Class Calendar

| Item | Details |
|---|---|
| Online class days | Admin marks — Principal approves |
| Emergency | Offline closed — online may continue if Principal decides |
| Applicable | Institutions with video learning module enabled |

### Multiple Boards Under Same Institution

| Item | Details |
|---|---|
| Separate calendars | Each board has own exam dates + schedule |
| Common holidays | Both boards share institution holidays |
| Working day count | Calculated per board separately |

### Inter-School / Inter-College Events

| Item | Details |
|---|---|
| Participating students | Marked on-duty — not absent |
| Non-participating | Regular attendance marked |
| Calendar entry | Shows as special event — not holiday |

### Recurring Events

| Item | Details |
|---|---|
| Examples | Assembly every Monday, library period every Friday |
| Recurrence | Daily / Weekly / Monthly |
| Cancel single | Admin cancels one occurrence |
| Cancel all | Admin cancels series — Principal approves |

### Makeup / Extra Classes

| Item | Details |
|---|---|
| Trigger | Emergency closure, lost periods |
| Timing | Before / after school hours / Saturday |
| Attendance | Counted as working day |
| Mandatory | Principal marks mandatory or optional |

### Academic Planner

| Item | Details |
|---|---|
| Who creates | Subject teacher |
| Content | Topic, date planned, chapter, periods needed |
| Linked to | Syllabus module |
| Auto-adjust | If holiday declared — topics shift forward automatically |
| Completion | Teacher marks done — syllabus tracker updates |
| Delay alert | Teacher falls behind — HOD + Principal notified |

### Revision Class Schedule

| Item | Details |
|---|---|
| Timing | After syllabus completion — before exam |
| Calendar entry | Marked as revision period |
| Timetable | Modified — subject-wise revision sessions |
| Syllabus link | Triggers syllabus 100% complete status |

---

## Calendar Visibility

| Audience | What They See | When |
|---|---|---|
| Staff | Full calendar | After Principal approval |
| Students | Holidays, breaks, exam dates, special days | After Principal approval |
| Parents | Holidays, breaks, exam dates, PTM dates, fee due dates | After Principal approval |
| Public | Nothing — login required | — |
| Group admin | All branch calendars | Real-time |
| EduForge super-admin | All institution calendars | Real-time |

---

## Calendar Notifications

| Event | Who Notified | Channel |
|---|---|---|
| Calendar published | All staff, students, parents | In-app only |
| Holiday added | All staff, students, parents | In-app only |
| Holiday removed | All staff, students, parents | In-app only |
| Emergency closure | All staff, students, parents | In-app only |
| Exam date changed | All staff, students, parents | In-app only |
| Special day added | All staff, students, parents | In-app only |
| New academic year | All staff | In-app only |
| PTM date added | Parents + teachers | In-app only |

---

## PTM Dates on Calendar

| Item | Details |
|---|---|
| Who adds | Institution admin — Principal approves |
| Visible to | Parents — after calendar published |
| Shows | PTM date, time, venue |
| Reminder | In-app 3 days before + on PTM day |
| Link | Links to PTM booking (Module 33) |

---

## Fee Payment Deadlines on Calendar

| Item | Details |
|---|---|
| Visible to | Parents + students |
| Conflict check | System warns if due date on holiday |
| Reminder | In-app 7 days before + on due date |
| Late fee start | Next working day after due date |
| Installments | All shown for full year |

---

## Admission Process Dates on Calendar

| Item | Details |
|---|---|
| Dates shown | Open date, form deadline, test date, result date, close date |
| Visible to | Public — on institution homepage |
| In-app | Existing users also see |
| Conflict check | Warns if clashes with exam blackout |

---

## Calendar Dashboard Widgets

### Today's Calendar Widget

| Item | Details |
|---|---|
| Shows | Today's date, events, period schedule |
| Holiday | Holiday name + reason |
| Exam | Subject, time, venue |
| Normal day | Today's timetable |
| Design | Follows institution theme + layout |
| Source | CDN |

### Upcoming Events Widget — Next 7 Days

| Role | What They See |
|---|---|
| Student | Exams, holidays, special days, fee due dates |
| Parent | Child's exams, holidays, PTM dates, fee due dates |
| Teacher | Classes, exams, PTM slots, holidays |
| Principal | All upcoming events + pending approvals |
| Admin | All events + pending tasks |

---

## Calendar Health Indicator

| Item | Details |
|---|---|
| Shows on | Principal + Admin dashboard |
| Calculation | Total working days vs elapsed vs remaining |
| Syllabus link | Remaining working days vs syllabus completion % |
| Warning | Insufficient days to complete syllabus |
| Per class | Shown per class |
| Generated by | Python analytics |
| Updates | Recalculates on every calendar change |

---

## Calendar Conflict Report

| Item | Details |
|---|---|
| Who sees | Admin + Principal |
| Shows | Exam on holiday, two events same day, fee due on holiday |
| Generated by | Python — auto-detects conflicts |
| Updates | Real-time |
| Unresolved | Highlighted in red on calendar |
| Dashboard | Conflict count on admin dashboard |

---

## Academic Year Lifecycle

### New Academic Year Creation

| Step | Action |
|---|---|
| 1 | Admin initiates — 30 days before year end |
| 2 | Previous year structure copied as template |
| 3 | Admin reviews + updates dates |
| 4 | Principal + Management approve |
| 5 | New year activated after old year closes |

- Cannot create new year while current year active
- Label auto-generated: "2025–26"
- Coaching: new batch created — not linked to academic year

### Year End Admin Reminders

| Trigger | Channel |
|---|---|
| 30 days before year end | In-app — Admin + Principal |
| 15 days before year end | In-app — Admin + Principal |
| 7 days before year end | In-app — Admin + Principal |

### Old Year Data Archival

| Item | Details |
|---|---|
| Status | Read only after year closes |
| Access | Staff + Principal — view only |
| Student | Can view own records |
| Retention | 5 years accessible → then cold storage |
| Attendance % | Locked — cannot change |
| Reports | Can still generate from archived year |

### Calendar Template — Copy Previous Year

| What is copied | What is NOT copied |
|---|---|
| Working day pattern | Specific dates |
| Saturday rule | Floating holiday dates |
| Term structure | Board exam dates (change each year) |
| Recurring events | Emergency closures |

---

## Calendar Audit Log

| Item | Details |
|---|---|
| What is logged | Every add, edit, delete of any calendar entry |
| Logged fields | Who, what, old value, new value, date/time, reason |
| Visible to | Principal + EduForge super-admin only |
| Immutable | Cannot be edited or deleted |
| Retention | 1 year |
| Change reason | Mandatory — admin must enter reason for every change |

---

## Calendar Display

| Item | Details |
|---|---|
| View | Full year — month-by-month in app |
| Color coding | Holidays red, exams blue, special days green, breaks yellow |
| Access | Staff, students, parents — after login |
| No download | View in app only |
| Not shareable | Outside app |
