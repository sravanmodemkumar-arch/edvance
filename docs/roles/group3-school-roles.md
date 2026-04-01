# EduForge — Group 3: School Level Roles

> Covers all schools under EduForge — standalone and group-owned.
> Scale: 1,000 schools · 200 to 5,000 students per school · day scholars + hostelers.

---

## Two Types of Schools — Platform Must Support Both

### Large School (Residential)
> 1,000–5,000 students · Boys + Girls hostels · 20–50 buses
- Dedicated HOD per subject department
- Multiple class teachers per class
- Separate boys hostel + girls hostel campuses
- AC and Non-AC hostel blocks
- Full labs: Physics, Chemistry, Biology, Computer, Language
- Dedicated medical room with nurse on campus
- Full-time counsellor, librarian, sports coaches
- Separate accounts department
- 50–200 non-teaching staff
- CBSE / State Board / ICSE / International streams

### Small School (Day Scholar)
> 200–500 students · Day scholars only or tiny hostel (30–50)
- Principal handles most admin functions
- One teacher covers HOD + teaching
- No hostel or 1 warden for small hostel
- 2–5 buses or no buses
- First aid only — no nurse on campus
- Combined science lab
- Part-time librarian
- No dedicated counsellor

---

## School Student Type Matrix

| Student Type | Large School | Small School | Hostel | Special Care |
|---|---|---|---|---|
| Day Scholar — Regular | ✅ | ✅ | ❌ | — |
| Day Scholar — Scholarship (Merit) | ✅ | ✅ | ❌ | — |
| Day Scholar — RTE Quota | ✅ | ✅ | ❌ | Gov. compliance |
| Day Scholar — Management Quota | ✅ | ✅ | ❌ | — |
| Day Scholar — NRI | ✅ | ❌ | ❌ | Separate fee |
| Hosteler — Boys AC | ✅ | ❌ | ✅ | — |
| Hosteler — Boys Non-AC | ✅ | ✅ (if hostel) | ✅ | — |
| Hosteler — Girls AC | ✅ | ❌ | ✅ | — |
| Hosteler — Girls Non-AC | ✅ | ✅ (if hostel) | ✅ | — |
| Hosteler — Scholarship | ✅ | ✅ (if hostel) | ✅ | Subsidised |
| Special Needs — Day | ✅ | ✅ | ❌ | IEP tracking |
| Special Needs — Hosteler | ✅ | ❌ | ✅ | Enhanced care |
| TC Received (Transfer In) | ✅ | ✅ | ❌/✅ | Mid-year join |
| Government School Migrant | ✅ | ✅ | ❌ | RTE compliance |

---

## System Access Levels — School

| Level | Label | Who Uses It |
|---|---|---|
| S0 | No Platform Access | Cook, driver, gardener, sweeper, security guard |
| S1 | Read Only | PTA members, SMC members, DEO/BEO (govt inspection) |
| S2 | Content & Teaching | Subject teachers — attendance, marks, notes, tests |
| S3 | Class Management | Class teachers — full class data, welfare, parent comm |
| S4 | Department Management | HODs — dept staff, syllabus, dept exams |
| S5 | Operations | Exam coord, fee staff, hostel warden, admission coord |
| S6 | School Admin | Vice Principal, Admin Officer — school-wide config |
| S7 | School Super Admin | Principal, Correspondent — full school access |

---

## Division A — School Governance (8 roles)

| # | Role | Level | Large | Small | Key Platform Actions |
|---|---|---|---|---|---|
| 1 | School Correspondent / Owner | S7 | ✅ Dedicated | ✅ Same as Principal | Full school access, activate/deactivate portal |
| 2 | Principal | S7 | ✅ Dedicated | ✅ Covers everything | Manage all staff, all students, all reports |
| 3 | Vice Principal | S6 | ✅ Dedicated | ❌ (Principal covers) | Academic + admin oversight, exam approval |
| 4 | Academic Director / Headmaster | S6 | ✅ Dedicated | ❌ | Curriculum, timetable, teacher performance |
| 5 | Administrative Officer | S6 | ✅ Dedicated | ✅ Shared (clerk) | Records, admissions, compliance documents |
| 6 | School Secretary / Office Manager | S5 | ✅ Dedicated | ❌ | Calendar, correspondence, notices, meetings |
| 7 | Dean of Students | S5 | ✅ Large only | ❌ | Student welfare, discipline, parent relations |
| 8 | School Management Committee Chair | S1 | ✅ Govt req. | ✅ Govt req. | Read-only governance — government mandate |

---

## Division B — Academic Leadership (10 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 9 | HOD — Mathematics | S4 | ✅ Dedicated | ❌ (Sr. Teacher covers) | Maths dept staff, syllabus, unit test papers |
| 10 | HOD — Science (Physics/Chem/Bio) | S4 | ✅ Dedicated | ❌ | Science dept, lab scheduling, practicals |
| 11 | HOD — Languages (English/Telugu/Hindi) | S4 | ✅ Dedicated | ❌ | Language dept, grammar tests, reading programs |
| 12 | HOD — Social Studies | S4 | ✅ Dedicated | ❌ | History, Civics, Geography, Economics dept |
| 13 | HOD — Computer Science | S4 | ✅ Dedicated | ❌ | Computer lab, coding, digital literacy |
| 14 | HOD — Physical Education | S4 | ✅ Dedicated | ✅ Shared | Sports, PT periods, sports day, fitness records |
| 15 | Academic Coordinator | S5 | ✅ Dedicated | ✅ 1 person | Timetable, lesson plans, academic calendar |
| 16 | Timetable Coordinator | S5 | ✅ Dedicated | ❌ | Weekly timetable, substitution management |
| 17 | Curriculum Coordinator | S4 | ✅ Dedicated | ❌ | Syllabus pacing, lesson plan review, NCERT mapping |
| 18 | Research & Innovation Coordinator | S4 | ✅ Large only | ❌ | Science fairs, Olympiads, project-based learning |

---

## Division C — Teaching Staff (18 role types)

> Each role type can have multiple staff members.
> Example: 8 Maths teachers across classes 6–12 all share "Subject Teacher — Mathematics" role.

| # | Role Type | Level | Subjects Covered | Large | Small |
|---|---|---|---|---|---|
| 19 | Primary Teacher (Class 1–5) | S2 | All subjects (class teacher model) | ✅ Multiple | ✅ Multiple |
| 20 | Subject Teacher — Mathematics | S2 | Maths (Class 6–12) | ✅ 5–10 staff | ✅ 1–2 staff |
| 21 | Subject Teacher — Physics | S2 | Physics (Class 9–12) | ✅ 2–4 staff | ✅ 1 staff |
| 22 | Subject Teacher — Chemistry | S2 | Chemistry (Class 9–12) | ✅ 2–4 staff | ✅ 1 staff |
| 23 | Subject Teacher — Biology | S2 | Biology (Class 9–12) | ✅ 2–4 staff | ✅ 1 staff |
| 24 | Subject Teacher — English | S2 | English (Class 1–12) | ✅ 5–8 staff | ✅ 2–3 staff |
| 25 | Subject Teacher — Telugu | S2 | Telugu / Regional Lang | ✅ 3–5 staff | ✅ 1–2 staff |
| 26 | Subject Teacher — Hindi | S2 | Hindi (second language) | ✅ 2–3 staff | ✅ 1 staff |
| 27 | Subject Teacher — Social Studies | S2 | History, Civics, Geo, Eco | ✅ 3–5 staff | ✅ 1–2 staff |
| 28 | Subject Teacher — Computer Science | S2 | CS, Coding, Digital Literacy | ✅ 2–4 staff | ✅ 1 staff |
| 29 | Subject Teacher — Environmental Science | S2 | EVS (Class 1–5) | ✅ 2–3 staff | ✅ 1 staff |
| 30 | Special Education Teacher | S3 | IEP, remedial, inclusion | ✅ 2–3 staff | ✅ 1 shared |
| 31 | Art & Drawing Teacher | S2 | Fine arts, craft | ✅ 1–2 staff | ✅ 1 shared |
| 32 | Music Teacher | S2 | Vocal, instruments | ✅ 1–2 staff | ✅ 1 shared |
| 33 | Dance Teacher | S2 | Classical, folk, cultural | ✅ 1–2 staff | ❌ (optional) |
| 34 | Moral Science / Value Ed Teacher | S2 | Ethics, life skills | ✅ 1–2 staff | ✅ 1 shared |
| 35 | Physical Education Teacher | S2 | PT, sports theory | ✅ 2–4 staff | ✅ 1 staff |
| 36 | Guest / Visiting Faculty | S2 | Any subject (part-time) | ✅ Multiple | ✅ 1–2 |

---

## Division D — Class Teachers (special role layer)

> Class teacher has EXTRA permissions beyond subject teacher.
> They own the full class: attendance, welfare, parent contact, marks collection.

| # | Role | Level | Owns |
|---|---|---|---|
| 37 | Class Teacher — Primary (Class 1–5) | S3 | Attendance, marks, welfare, parent comm for one class |
| 38 | Class Teacher — Upper Primary (Class 6–8) | S3 | Same + subject coordination across dept teachers |
| 39 | Class Teacher — High School (Class 9–10) | S3 | Same + board exam preparation tracking |
| 40 | Class Teacher — Senior Secondary (Class 11–12) | S3 | Same + career counselling, college application |

---

## Division E — Lab & Technical Staff (7 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 41 | Lab Assistant — Physics | S2 | ✅ Dedicated | ❌ (teacher manages) | Physics lab equipment, practical setup, safety |
| 42 | Lab Assistant — Chemistry | S2 | ✅ Dedicated | ❌ | Chemical inventory, safety, practical records |
| 43 | Lab Assistant — Biology | S2 | ✅ Dedicated | ❌ | Bio specimens, microscopes, lab records |
| 44 | Lab Assistant — Computer | S2 | ✅ Dedicated | ✅ 1 person | Computer lab maintenance, software, student login |
| 45 | Lab Assistant — Language | S2 | ✅ Dedicated | ❌ | Language lab headsets, software, audio records |
| 46 | IT Technician | S5 | ✅ Dedicated | ❌ | School network, EduForge devices, projectors |
| 47 | Audio Visual Technician | S2 | ✅ Large only | ❌ | Smart board, projector, recording equipment |

---

## Division F — Exam & Assessment (7 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 48 | Exam Controller | S5 | ✅ Dedicated | ✅ (VP covers) | All internal exams — unit test, half-yearly, annual |
| 49 | Exam Coordinator | S5 | ✅ Dedicated | ❌ | Question paper collection, seating plan, invigilation |
| 50 | Exam Superintendent | S5 | ✅ Multiple | ❌ | Invigilate exam hall, manage malpractice |
| 51 | Answer Sheet Custodian | S5 | ✅ Dedicated | ❌ | Secure custody of answer sheets, distribution/collection |
| 52 | Results Processing Staff | S5 | ✅ Dedicated | ❌ | Enter marks, compute results, generate rank cards |
| 53 | Board Exam Coordinator | S5 | ✅ Dedicated | ✅ Shared | CBSE/State board registration, hall tickets, results |
| 54 | Scholarship Exam Coordinator | S5 | ✅ Dedicated | ✅ Shared | NTSE, NMMS, school-level Olympiad registration |

---

## Division G — Admissions & Student Records (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 55 | Admission Coordinator | S5 | ✅ Dedicated | ✅ (Admin Officer) | New student enrolment, admission form, seat allocation |
| 56 | Records Clerk | S5 | ✅ Dedicated | ❌ | Student files, TC issuance, migration certificates |
| 57 | Data Entry Operator | S5 | ✅ Multiple | ❌ | Enter marks, attendance, fee data into EduForge |
| 58 | Reception / Front Desk | S1 | ✅ Dedicated | ❌ | Visitor management, parent query, appointments |
| 59 | Student Welfare Data Entry | S5 | ✅ Dedicated | ❌ | Enter welfare events, medical records, incident logs |
| 60 | Alumni Coordinator | S5 | ✅ Large only | ❌ | Maintain alumni database, school reunion, referrals |

---

## Division H — Finance & Fee Collection (7 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 61 | School Accountant | S5 | ✅ Dedicated | ✅ 1 person | Full accounts — fee, salary, vendor payments |
| 62 | Fee Collection Staff | S5 | ✅ Multiple | ❌ (Accountant does) | Collect fees, issue receipts, update EduForge |
| 63 | Cashier | S5 | ✅ Dedicated | ❌ | Cash handling, daily closing, bank deposit |
| 64 | Hostel Fee Manager | S5 | ✅ (if hostel) | ✅ (if hostel) | Hostel + mess fee, AC/Non-AC rates, extras |
| 65 | Transport Fee Manager | S5 | ✅ (if transport) | ✅ (if transport) | Route-wise fee, monthly collection |
| 66 | Fee Defaulter Coordinator | S5 | ✅ Dedicated | ❌ | Follow up on pending fees, generate demand letters |
| 67 | Scholarship Disbursement Officer | S5 | ✅ Dedicated | ✅ Shared | Track, disburse, report government + institution scholarships |

---

## Division I — Hostel Management (13 roles)

> Only for schools with residential facility.
> Boys and Girls always managed separately — never shared warden.

| # | Role | Level | Large | Small (if hostel) | Owns |
|---|---|---|---|---|---|
| 68 | Hostel Warden — Boys | S5 | ✅ Dedicated | ✅ 1 person | All boys hostelers — discipline, welfare, roll call |
| 69 | Hostel Warden — Girls | S5 | ✅ Dedicated | ✅ 1 person | All girls hostelers — safety, welfare, visiting hours |
| 70 | Hostel Matron — Boys | S5 | ✅ Dedicated | ❌ | Daily welfare checks, hygiene, room inspections |
| 71 | Hostel Matron — Girls | S5 | ✅ Dedicated | ❌ | Daily welfare, hygiene, parent communication |
| 72 | Night Duty Supervisor — Boys | S5 | ✅ Dedicated | ❌ | Night roll call, emergency response |
| 73 | Night Duty Supervisor — Girls | S5 | ✅ Dedicated | ❌ | Night roll call, emergency response |
| 74 | Mess Manager | S5 | ✅ Dedicated | ❌ | Menu planning, food quality, hygiene, mess fee |
| 75 | Hostel Admission Coordinator | S5 | ✅ Dedicated | ✅ Shared | Hostel seat allotment, room assignment, AC/Non-AC |
| 76 | Hostel Discipline In-charge | S5 | ✅ Dedicated | ❌ | Student misconduct in hostel, suspension process |
| 77 | Parent Visit Coordinator | S5 | ✅ Dedicated | ✅ Shared | Schedule parent visits, biometric entry, visitor log |
| 78 | Hostel Medical Attendant | S5 | ✅ Dedicated | ✅ Shared | First aid in hostel, medical room, doctor coordination |
| 79 | Laundry / Housekeeping In-charge | S0 | ✅ Large only | ❌ | Laundry, room cleanliness — no platform access |
| 80 | Hostel Store Keeper | S0 | ✅ Dedicated | ❌ | Hostel inventory — food, toiletries, stationery |

---

## Division J — Transport Management (5 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 81 | Transport Coordinator | S5 | ✅ Dedicated | ✅ 1 person | All routes, buses, driver roster, GPS monitoring |
| 82 | Bus Route In-charge | S5 | ✅ Multiple | ❌ | One route — pickup/drop points, student list |
| 83 | Transport Fee Collector | S5 | ✅ Dedicated | ❌ | Route-wise fee, monthly tracking in EduForge |
| 84 | Vehicle Maintenance Supervisor | S0 | ✅ Dedicated | ❌ | Bus fitness — no platform access |
| 85 | Driver / Conductor | S0 | ✅ Multiple | ✅ If buses | No platform access — GPS app only |

---

## Division K — Health & Medical (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 86 | School Nurse / Medical Officer | S5 | ✅ Dedicated | ❌ (first aid only) | Medical room, health records, medication log |
| 87 | First Aid Coordinator | S5 | ✅ Dedicated | ✅ Any teacher | Emergency first aid, incident log in EduForge |
| 88 | School Counsellor | S5 | ✅ Dedicated | ✅ Shared (group) | Mental health, exam stress, peer issues, career |
| 89 | Special Needs Support Aide | S3 | ✅ Dedicated | ✅ 1 shared | IEP implementation, classroom support for SEN students |
| 90 | Health & Hygiene Educator | S2 | ✅ Dedicated | ❌ | Health programs, hygiene campaigns, WASH |
| 91 | Emergency Response Coordinator | S5 | ✅ Dedicated | ✅ Principal | Fire drill, medical emergency, evacuation plan |

---

## Division L — Library & Learning Resources (4 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 92 | Librarian | S3 | ✅ Dedicated | ✅ Part-time | Book catalog, issue/return, library records in EduForge |
| 93 | Library Assistant | S2 | ✅ Dedicated | ❌ | Shelving, book repair, member records |
| 94 | Digital Resource Coordinator | S2 | ✅ Dedicated | ❌ | E-books, digital library, YouTube playlist mapping |
| 95 | Reading Program Coordinator | S2 | ✅ Dedicated | ❌ | Reading challenges, book clubs, literacy programs |

---

## Division M — Sports & Extra-Curricular (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 96 | Sports Director / Coach | S4 | ✅ Dedicated | ✅ PT Teacher | Sports calendar, inter-school tournaments, training |
| 97 | Cricket Coach | S2 | ✅ Dedicated | ❌ | Cricket training, school team, district competitions |
| 98 | Athletics Coach | S2 | ✅ Dedicated | ❌ | Track & field, running events, state meets |
| 99 | Cultural Activities Coordinator | S4 | ✅ Dedicated | ✅ Shared | Annual day, cultural fest, debate, quiz, drawing |
| 100 | NSS / NCC Coordinator | S4 | ✅ Dedicated | ✅ Shared | NSS camps, community service, NCC drills |
| 101 | Eco Club / Science Club Coordinator | S2 | ✅ Dedicated | ❌ | Environment programs, science exhibitions |

---

## Division N — Welfare & Safety (7 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 102 | Child Protection Officer | S5 | ✅ Dedicated | ✅ Principal | POCSO policy, complaint handling, NCPCR reporting |
| 103 | Anti-Ragging Committee In-charge | S5 | ✅ Dedicated | ✅ Shared | Anti-ragging policy, complaint investigation |
| 104 | Grievance Redressal Officer | S5 | ✅ Dedicated | ✅ VP covers | Student/parent complaints, resolution tracking |
| 105 | CCTV & Security In-charge | S5 | ✅ Dedicated | ❌ | CCTV monitoring, gate log, visitor register |
| 106 | Welfare Events Monitor | S5 | ✅ Class Teachers | ✅ Class Teachers | Log welfare events Severity 1–4 in EduForge |
| 107 | Discipline Committee Head | S5 | ✅ Dedicated | ✅ VP covers | Student misconduct, suspension, parent hearing |
| 108 | Women's Safety Committee (POSH) | S5 | ✅ Dedicated | ✅ Shared | POSH Act compliance for female staff + students |

---

## Division O — Parent & Community Relations (6 roles)

| # | Role | Level | Access | Can Do in EduForge |
|---|---|---|---|---|
| 109 | Parent — Father | Parent Portal | S1 | View child attendance, results, fee, timetable |
| 110 | Parent — Mother | Parent Portal | S1 | View child attendance, results, fee, timetable |
| 111 | Parent / Legal Guardian | Parent Portal | S1 | Full parent access for child |
| 112 | Emergency Contact Only | Notification | S1 | Receive alerts only — no login |
| 113 | PTA President | S1 | Limited | View school analytics shared by Principal |
| 114 | PTA Member | S1 | Limited | Attend PTM, view own child data only |

---

## Division P — External Stakeholders with Limited Access (5 roles)

| # | Role | Level | When They Access | What They See |
|---|---|---|---|---|
| 115 | Block Education Officer (BEO) | S1 | Annual inspection | Attendance %, enrolment numbers, results summary |
| 116 | District Education Officer (DEO) | S1 | Annual inspection | Same as BEO + fee structure |
| 117 | CBSE / Board Inspector | S1 | Affiliation inspection | Infrastructure data, teacher qualifications |
| 118 | School Accreditation Auditor | S1 | NAAC / ISO visit | Quality metrics, student outcomes |
| 119 | Right to Education (RTE) Monitor | S1 | Government audit | RTE quota students, fee waiver records |

---

## Division Q — Support Staff (S0 — No Platform Access) (6 roles)

> These staff are on the payroll but do not use EduForge directly.

| # | Role | Who They Are |
|---|---|---|
| 120 | Security Guard | Gate entry, campus security |
| 121 | Gardener / Groundskeeper | Campus maintenance |
| 122 | Electrician / Plumber | Maintenance staff |
| 123 | Cook / Mess Staff | Hostel kitchen |
| 124 | Peon / Office Boy | Office errands |
| 125 | Sweeper / Sanitation Staff | Cleanliness |

---

## Full Role Count

| Division | Total | Large Uses | Small Uses |
|---|---|---|---|
| A — School Governance | 8 | 8 | 3–4 |
| B — Academic Leadership | 10 | 10 | 2–3 |
| C — Teaching Staff (role types) | 18 | 18 | 8–10 |
| D — Class Teachers | 4 | 4 | 4 |
| E — Lab & Technical | 7 | 7 | 1–2 |
| F — Exam & Assessment | 7 | 7 | 2–3 |
| G — Admissions & Records | 6 | 6 | 2–3 |
| H — Finance & Fee | 7 | 7 | 2–3 |
| I — Hostel Management | 13 | 13 | 2–3 (if hostel) |
| J — Transport | 5 | 5 | 1–2 |
| K — Health & Medical | 6 | 6 | 1–2 |
| L — Library | 4 | 4 | 1 |
| M — Sports & Extra-Curricular | 6 | 6 | 2–3 |
| N — Welfare & Safety | 7 | 7 | 3–4 |
| O — Parent & Community | 6 | 6 | 6 |
| P — External Stakeholders | 5 | 5 | 5 |
| Q — Support Staff (S0) | 6 | 6 | 3–4 |
| **Total** | **125** | **125** | **~45** |

---

## School vs Group — Who Controls What

| Action | Group Level | School Level |
|---|---|---|
| Create school portal | Group IT Admin ✅ | Principal ❌ |
| Hire a teacher | Group HR ✅ | Principal ✅ (within quota) |
| Transfer teacher to another school | Group HR ✅ | Principal ❌ |
| Set fee structure | Group Finance ✅ | Accountant ❌ |
| Publish cross-school results | Group Results Coord ✅ | Principal ❌ |
| Create unit test (internal) | Exam Controller ✅ | School only |
| Mark daily attendance | Class Teacher ✅ | School only |
| Log welfare event | Class Teacher ✅ | School only |
| Allocate hostel room | Hostel Warden ✅ | School only |
| Issue TC (Transfer Certificate) | Records Clerk ✅ | School only |
| POCSO complaint | Child Protection Officer ✅ | School — triggers Group |

---

## Day Scholar vs Hosteler — School Level Differences

| Function | Day Scholar | Hosteler |
|---|---|---|
| Attendance | Morning session only | Morning + afternoon + night roll call |
| Parent contact | Daily SMS / weekly PTM | Weekly welfare update + restricted call hours |
| Medical | First aid + emergency | Medical room + nurse + daily health check |
| Safety | Gate in/out with ID card | Biometric + visitor register + warden approval |
| Fee | Tuition + transport | Tuition + hostel (AC/Non-AC) + mess + extras |
| Welfare monitoring | Welfare events if flagged | Daily Severity 1–4 welfare check |
| Night supervision | Not applicable | Night duty supervisor + roll call |
| Food | Tiffin box / canteen | Mess — breakfast, lunch, snack, dinner |
| Laundry | Self-managed | Hostel laundry service |
| Visiting hours | Parents visit anytime | Scheduled visiting hours only |
