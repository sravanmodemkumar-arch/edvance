# EduForge — Group 5: Coaching Centre Roles

> Covers all coaching institutes registered on EduForge.
> Scale: 100 coaching centres · 5,000 to 15,000 members each.
> Types: JEE · NEET · SSC · RRB · Banking · UPSC · Foundation (Class 6–10) · CA.

---

## Coaching Is Fundamentally Different From School/College

| Aspect | School / College | Coaching Centre |
|---|---|---|
| Affiliation | CBSE / BIEAP / UGC | None — purely commercial |
| Compliance | NAAC, UGC, POCSO mandatory | POCSO (minors only), DPDP |
| Model | Academic year (June–March) | Batch-based — multiple batches simultaneously |
| Revenue | Fee per year | Fee per course/batch + renewals + upsell |
| Students | Fixed class, fixed age | Any age — Class 6 to working professionals |
| Dropout | Low (compulsory attendance) | High — retention is critical KPI |
| Results | Board exam pass % | JEE rank, NEET rank, SSC selection — brand driver |
| Admissions | Annual once | Rolling admissions — new batches every month |
| Parent role | High (minor students) | Low (most students are adults) |
| Toppers | Celebrated internally | Toppers are public brand ambassadors |
| B2B | Not common | School/college tie-ups — a major revenue channel |
| Franchise | Rare | Common — coaching chains have franchises |

---

## Types of Coaching Centres — Platform Must Support All

### Large Institute (10,000–15,000 members)
> Multi-branch · JEE + NEET + Foundation + Online · Residential option
- 50–100 faculty across all subjects
- 200+ batches running simultaneously
- Boys + Girls hostel for dropper/residential batches
- Full online delivery arm (live + recorded)
- B2B school tie-ups for foundation students
- YouTube channel + social media as marketing engine
- Franchise network management
- Dedicated topper relations team

### Medium Institute (5,000–10,000 members)
> Single city · 2–3 exam categories · Mix of classroom + online
- 20–50 faculty
- 50–100 batches
- Limited hostel (dropper batch only)
- Some online delivery

### Small Coaching (Local — not in this spec but platform supports)
> Single branch · 500–2,000 members · One exam focus

---

## Student Type Matrix — Coaching

| Student Type | Description | Age | Hostel | Parent Portal |
|---|---|---|---|---|
| Regular Batch — Classroom | Daily classroom attendance | 13–25 | ❌ | If minor |
| Weekend Batch | Sat–Sun only — working students | 18–30 | ❌ | ❌ |
| Online Live Batch | Live Zoom/platform classes | Any | ❌ | If minor |
| Recorded Course Only | Self-paced video access | Any | ❌ | ❌ |
| Crash Course | 1–3 months intensive | 16–25 | ❌ | If minor |
| Dropper — JEE | Full-year after 12th, JEE retry | 18–20 | ✅ Often | ❌ (adult) |
| Dropper — NEET | Full-year after 12th, NEET retry | 18–20 | ✅ Often | ❌ (adult) |
| Repeater — SSC/Banking | Re-attempting govt exam | 20–30 | ❌ | ❌ |
| Foundation — Class 6–8 | Early competitive prep | 11–13 | ❌ | ✅ Always |
| Foundation — Class 9–10 | Pre-JEE/NEET base building | 14–15 | ❌ | ✅ Always |
| B2B — School Tie-up | Attends coaching via school contract | 13–16 | ❌ | ✅ |
| Scholarship Student | Fee waiver based on rank/need | Any | ❌/✅ | If minor |
| Distance/Correspondence | Study material + tests only | Any | ❌ | ❌ |
| Part-time — Working Prof. | Banking/SSC while employed | 22–30 | ❌ | ❌ |
| International Student | NRI/foreign prep for Indian exams | Any | ✅ Often | ❌ |

---

## System Access Levels — Coaching

| Level | Label | Who Uses It |
|---|---|---|
| K0 | No Platform Access | Security, cook, maintenance, driver |
| K1 | Read Only | Owner reports, franchise partner view, B2B partner |
| K2 | Teaching | Faculty — attendance, notes, test creation, marks |
| K3 | Batch Level | Batch coordinator, counsellor — one batch's full data |
| K4 | Course Level | Course head, test series coordinator — cross-batch |
| K5 | Operations | Admissions, fee, hostel warden, analytics |
| K6 | Admin | Branch Manager, Academic Director |
| K7 | Super Admin | Director/Owner, MD — full institute access |

---

## Division A — Governance (8 roles)

| # | Role | Level | Large | Medium | Key Platform Actions |
|---|---|---|---|---|---|
| 1 | Director / Owner | K7 | ✅ Dedicated | ✅ Same | Full access — all branches, all batches, all revenue |
| 2 | Managing Director | K7 | ✅ Dedicated | ❌ | Operations across all branches |
| 3 | CEO | K6 | ✅ Dedicated | ❌ | Day-to-day management, SLA with EduForge |
| 4 | Branch Manager | K6 | ✅ Per branch | ✅ 1 person | One branch full access — staff, students, fee |
| 5 | Academic Director | K6 | ✅ Dedicated | ✅ Shared | Faculty management, batch scheduling, quality |
| 6 | Operations Director | K6 | ✅ Dedicated | ❌ | Cross-branch coordination, infra, support |
| 7 | Board of Advisors Member | K1 | ✅ Optional | ❌ | Read-only analytics dashboard |
| 8 | Franchise Network Head | K5 | ✅ Dedicated | ❌ | Manage all franchise branches under the brand |

---

## Division B — Academic Leadership (10 roles)

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 9 | Chief Academic Officer | K6 | ✅ Dedicated | ❌ (Acad. Dir.) | Academic standards, faculty quality, exam results |
| 10 | Course Head — JEE | K5 | ✅ Dedicated | ✅ Shared | All JEE batches — schedule, faculty, content, mock tests |
| 11 | Course Head — NEET | K5 | ✅ Dedicated | ✅ Shared | All NEET batches |
| 12 | Course Head — SSC / RRB | K5 | ✅ Dedicated | ✅ Shared | All SSC/RRB batches |
| 13 | Course Head — Banking | K5 | ✅ Dedicated | ❌ | All Banking/IBPS/SBI batches |
| 14 | Course Head — UPSC | K5 | ✅ Dedicated | ❌ | All UPSC/State PSC batches |
| 15 | Course Head — Foundation (6–10) | K5 | ✅ Dedicated | ❌ | All foundation batches for school students |
| 16 | Course Head — CA / Commerce | K5 | ✅ Dedicated | ❌ | CA Foundation, Inter, Final batches |
| 17 | Academic Coordinator | K5 | ✅ Dedicated | ✅ 1 person | Timetable, faculty roster, batch calendar |
| 18 | Curriculum Designer | K4 | ✅ Dedicated | ❌ | Design course material, topic sequence, MCQ mapping |

---

## Division C — Faculty (20 role types)

> Each role type = multiple faculty members per exam category.
> Faculty own their batch's attendance, notes, and test creation.

### JEE Faculty (3 roles)
| # | Role Type | Level | Teaches | Batch |
|---|---|---|---|---|
| 19 | Faculty — JEE Mathematics | K2 | Calculus, Algebra, Coordinate, Vectors, Probability | JEE Main + Advanced |
| 20 | Faculty — JEE Physics | K2 | Mechanics, Optics, Electricity, Modern Physics | JEE Main + Advanced |
| 21 | Faculty — JEE Chemistry | K2 | Organic, Inorganic, Physical Chemistry | JEE Main + Advanced |

### NEET Faculty (3 roles)
| # | Role Type | Level | Teaches | Batch |
|---|---|---|---|---|
| 22 | Faculty — NEET Physics | K2 | NCERT Physics, previous papers | NEET UG |
| 23 | Faculty — NEET Chemistry | K2 | NCERT Chemistry | NEET UG |
| 24 | Faculty — NEET Biology | K2 | Botany + Zoology, NCERT | NEET UG |

### SSC / RRB Faculty (5 roles)
| # | Role Type | Level | Teaches | Batch |
|---|---|---|---|---|
| 25 | Faculty — Quantitative Aptitude | K2 | Arithmetic, DI, Algebra, Geometry | SSC/RRB/Banking |
| 26 | Faculty — Reasoning | K2 | Verbal, Non-verbal, Logical, Analytical | SSC/RRB/Banking |
| 27 | Faculty — English | K2 | Grammar, RC, Vocabulary, Error Spotting | SSC/RRB/Banking |
| 28 | Faculty — General Knowledge / GS | K2 | Current Affairs, Static GK, Polity, History | SSC/RRB/Banking |
| 29 | Faculty — Computer Awareness | K2 | MS Office, Networking, Database Basics | Banking/SSC |

### Banking / UPSC Faculty (3 roles)
| # | Role Type | Level | Teaches | Batch |
|---|---|---|---|---|
| 30 | Faculty — Banking Awareness | K2 | RBI, SEBI, Monetary Policy, Financial Markets | Banking |
| 31 | Faculty — UPSC General Studies | K2 | History, Polity, Economy, Geography, Science | UPSC CSE |
| 32 | Faculty — UPSC Optional Subject | K2 | Per student choice — Geography, Public Admin, etc. | UPSC CSE |

### Foundation Faculty (3 roles)
| # | Role Type | Level | Teaches | Batch |
|---|---|---|---|---|
| 33 | Faculty — Foundation Maths | K2 | Class 6–10 Maths aligned to school + competitive | Foundation |
| 34 | Faculty — Foundation Science | K2 | Physics, Chemistry, Biology for Class 6–10 | Foundation |
| 35 | Faculty — Foundation Mental Ability | K2 | Reasoning, IQ, Olympiad prep | Foundation |

### General Faculty Roles (3 roles)
| # | Role Type | Level | Notes |
|---|---|---|---|
| 36 | Senior Faculty / Star Faculty | K2 | 5+ years experience, high conversion in admissions |
| 37 | Demo Faculty | K2 | Conducts demo/trial classes for admission conversion |
| 38 | Guest / Visiting Faculty | K2 | Part-time, specific topics, external experts |

---

## Division D — Batch Management (7 roles)

> Coaching runs 200+ simultaneous batches in a large institute.
> Each batch needs dedicated management — not just faculty.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 39 | Batch Coordinator | K3 | ✅ Per batch | ✅ Shared | One batch — schedule, attendance, parent comm, performance |
| 40 | Batch Counsellor | K3 | ✅ Per batch | ✅ Shared | Student motivation, dropout prevention, performance tracking |
| 41 | Doubt Clearing Session Coordinator | K3 | ✅ Dedicated | ✅ Shared | Extra doubt sessions — schedule, faculty allocation |
| 42 | Revision Class Coordinator | K3 | ✅ Dedicated | ❌ | Revision before major tests — schedule, material |
| 43 | Crash Course Coordinator | K4 | ✅ Dedicated | ✅ Shared | Short-term intensive batch management |
| 44 | Online Batch Coordinator | K3 | ✅ Dedicated | ✅ Shared | Zoom/live class coordination, attendance, recording links |
| 45 | Foundation Batch Coordinator | K3 | ✅ Dedicated | ❌ | Class 6–10 batch — parent communication heavy |

---

## Division E — Test Series & Exam Management (9 roles)

> Test series is the CORE product of coaching — what differentiates them.
> EduForge TSP (Test Series Platform) is the backbone.
> 74,000 concurrent submissions on major test days.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 46 | Test Series Director | K5 | ✅ Dedicated | ✅ Course Head | Overall test calendar, question bank strategy |
| 47 | Test Series Coordinator | K4 | ✅ Dedicated | ✅ 1 person | Schedule tests, publish via EduForge, results |
| 48 | Question Paper Setter | K4 | ✅ Multiple | ✅ Faculty | Create MCQs, upload to EduForge bank |
| 49 | Question Reviewer | K4 | ✅ Dedicated | ❌ | Quality review before paper goes live |
| 50 | Answer Key Coordinator | K4 | ✅ Dedicated | ✅ Shared | Publish answer keys, handle objections |
| 51 | Results & Rank Coordinator | K4 | ✅ Dedicated | ✅ Shared | Trigger rank computation, publish results, rank cards |
| 52 | Performance Analytics Officer | K4 | ✅ Dedicated | ❌ | Topic-wise analysis, weak area identification per student |
| 53 | All India Rank (AIR) Coordinator | K4 | ✅ Large only | ❌ | Manage AIR across all students in national test series |
| 54 | Mock Test Invigilator | K3 | ✅ Multiple | ✅ Faculty | Online proctoring, malpractice monitoring |

---

## Division F — Admissions & Sales (10 roles)

> Admissions = revenue. Coaching is a sales-heavy business.
> Demo class → Counselling → Fee payment → Enrolment → Batch allocation.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 55 | Admissions Director | K5 | ✅ Dedicated | ❌ (Branch Mgr) | Admission pipeline, targets, conversion rate |
| 56 | Admission Counsellor | K4 | ✅ Multiple | ✅ 2–3 | Student/parent counselling, course recommendation |
| 57 | Demo Class Coordinator | K4 | ✅ Dedicated | ✅ Shared | Schedule demo, assign demo faculty, track conversion |
| 58 | Lead Management Executive | K4 | ✅ Dedicated | ❌ | CRM leads — calls, follow-up, conversion funnel |
| 59 | Field Sales Executive | K4 | ✅ Multiple | ✅ 1–2 | Visit schools, colleges, area campaigns |
| 60 | B2B / School Tie-up Manager | K5 | ✅ Dedicated | ✅ Shared | Contract with schools for foundation batch delivery |
| 61 | Scholarship Exam Coordinator | K4 | ✅ Dedicated | ✅ Shared | Coaching's own scholarship entrance test |
| 62 | Franchise Coordinator | K5 | ✅ Dedicated | ❌ | Onboard, train, support franchise branches |
| 63 | Referral Program Manager | K4 | ✅ Dedicated | ❌ | Student/alumni referral scheme — incentive tracking |
| 64 | Walk-in Reception / Enquiry Handler | K4 | ✅ Multiple | ✅ 1–2 | First point of contact for new enquiries |

---

## Division G — Finance & Fee Management (8 roles)

> Coaching fee has complex structure — installments, EMI, scholarships, refunds.
> Large institutes collect 50–100 crores/year.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 65 | Finance Manager | K5 | ✅ Dedicated | ✅ 1 person | Full P&L, revenue per batch/course, Razorpay |
| 66 | Fee Collection Executive | K5 | ✅ Multiple | ✅ 1–2 | Collect fees, issue receipts, update EduForge |
| 67 | EMI / Installment Tracker | K4 | ✅ Dedicated | ❌ | Track installment due dates, remind, restrict access |
| 68 | Scholarship Manager | K4 | ✅ Dedicated | ✅ Shared | Merit scholarships, fee waivers, govt schemes |
| 69 | Refund Processing Executive | K4 | ✅ Dedicated | ✅ Shared | Refund policy, Razorpay reversal, approval workflow |
| 70 | Fee Defaulter Coordinator | K4 | ✅ Dedicated | ❌ | Restrict portal access for defaulters, recovery |
| 71 | GST / Accounts Officer | K4 | ✅ Dedicated | ❌ | SAC code billing, CGST/SGST, TDS |
| 72 | Cashier | K4 | ✅ Dedicated | ❌ | Cash handling, daily closing, bank deposit |

---

## Division H — Online Delivery Team (8 roles)

> Large coaching institutes run parallel online arm — equal size to classroom.
> Live classes + recorded videos + online tests = full digital product.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 73 | Online Program Director | K6 | ✅ Dedicated | ❌ | Full online delivery strategy, tech platform config |
| 74 | Live Class Coordinator | K4 | ✅ Dedicated | ✅ Shared | Schedule Zoom/live, faculty links, attendance |
| 75 | Video Production Executive | K4 | ✅ Dedicated | ❌ | Record, edit, upload faculty lectures to EduForge |
| 76 | LMS / EduForge Administrator | K5 | ✅ Dedicated | ✅ 1 person | Configure EduForge portal, batches, content |
| 77 | Technical Support — Live Classes | K4 | ✅ Dedicated | ❌ | Fix audio/video issues during live sessions |
| 78 | YouTube / Content Manager | K4 | ✅ Dedicated | ❌ | YouTube channel, free content, playlist curation |
| 79 | Online Doubt Resolution Coordinator | K3 | ✅ Dedicated | ❌ | Manage online doubt forum, assign faculty responses |
| 80 | Online Exam Proctor | K3 | ✅ Multiple | ✅ Shared | Monitor online test sessions for malpractice |

---

## Division I — Hostel Management (10 roles)

> Only for institutes with residential facility — dropper batches primarily.
> Dropper students (JEE/NEET retry year) live on campus full time.

| # | Role | Level | Large | Medium (if hostel) | Owns |
|---|---|---|---|---|---|
| 81 | Hostel Warden — Boys | K5 | ✅ Dedicated | ✅ 1 person | Boys hostelers — discipline, welfare, roll call |
| 82 | Hostel Warden — Girls | K5 | ✅ Dedicated | ✅ 1 person | Girls hostelers — safety, welfare |
| 83 | Hostel Matron | K5 | ✅ Dedicated | ❌ | Daily welfare checks, hygiene, room inspection |
| 84 | Night Duty Supervisor | K5 | ✅ Dedicated | ❌ | Night roll call, emergency |
| 85 | Mess Manager | K5 | ✅ Dedicated | ❌ | Menu, food quality, hygiene, mess fee |
| 86 | Hostel Admission Coordinator | K5 | ✅ Dedicated | ✅ Shared | Room allocation — dropper, JEE, NEET batches |
| 87 | Parent Visit Coordinator | K5 | ✅ Dedicated | ✅ Shared | Scheduled visits, visitor log, biometric |
| 88 | Hostel Medical Attendant | K5 | ✅ Dedicated | ✅ Shared | First aid, medical room, doctor visits |
| 89 | Hostel Discipline Committee | K5 | ✅ Dedicated | ❌ | Misconduct, eviction process |
| 90 | Hostel Store Keeper | K0 | ✅ Dedicated | ❌ | Inventory — food, stationery — no login |

---

## Division J — Student Affairs & Welfare (8 roles)

> High-pressure exam prep = high mental health risk.
> Dropper year is highest risk period — JEE/NEET failure + family pressure.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 91 | Student Welfare Officer | K4 | ✅ Dedicated | ✅ Shared | Log welfare events, follow-up, parent alerts |
| 92 | Counsellor — Academic | K4 | ✅ Dedicated | ✅ Shared | Study plan, weak subject guidance, goal setting |
| 93 | Counsellor — Mental Health | K4 | ✅ Dedicated | ❌ | Exam anxiety, depression, dropper stress |
| 94 | Topper Relations Manager | K4 | ✅ Dedicated | ❌ | JEE/NEET rank holders as brand ambassadors |
| 95 | Alumni Coordinator | K4 | ✅ Dedicated | ❌ | Alumni database, IIT/MBBS alumni mentorship |
| 96 | Grievance Redressal Officer | K4 | ✅ Dedicated | ✅ Shared | Student/parent complaints, resolution |
| 97 | Child Protection Officer | K4 | ✅ Dedicated | ✅ Shared | POCSO — mandatory for minor students |
| 98 | Anti-Ragging In-charge | K4 | ✅ Dedicated | ✅ Shared | Ragging among hostel students — policy + action |

---

## Division K — Analytics & MIS (6 roles)

> Analytics is the competitive differentiator for coaching.
> "Which student needs help before they drop out?" is the key question.

| # | Role | Level | Large | Medium | Key Reports |
|---|---|---|---|---|---|
| 99 | Analytics Manager | K5 | ✅ Dedicated | ❌ | Institute-wide MIS — batch performance, revenue, churn |
| 100 | Batch Performance Analyst | K4 | ✅ Dedicated | ❌ | Cross-batch rank comparison, subject-wise weakness |
| 101 | Student Retention Analyst | K4 | ✅ Dedicated | ❌ | Dropout prediction — attendance + test score signals |
| 102 | Rank Improvement Tracker | K4 | ✅ Dedicated | ❌ | Month-on-month rank improvement per student |
| 103 | Test Analytics Officer | K4 | ✅ Dedicated | ❌ | Topic-wise heatmaps, difficulty calibration |
| 104 | Revenue Analytics Officer | K4 | ✅ Dedicated | ❌ | Batch-wise revenue, CAC, LTV per student type |

---

## Division L — Marketing & Growth (7 roles)

> Coaching marketing = results marketing. Toppers drive 80% of admissions.
> Social media + YouTube + field campaigns = primary acquisition channels.

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 105 | Marketing Manager | K0 | ✅ Dedicated | ❌ (Dir. covers) | Brand, campaigns, admission season planning |
| 106 | Digital Marketing Executive | K0 | ✅ Dedicated | ✅ Shared | Google Ads, Meta Ads, YouTube pre-rolls |
| 107 | Content Creator — YouTube | K0 | ✅ Dedicated | ❌ | Free lecture videos, shorts, topper interviews |
| 108 | Social Media Manager | K0 | ✅ Dedicated | ✅ Shared | Instagram, WhatsApp, Telegram for student community |
| 109 | Event Coordinator | K0 | ✅ Dedicated | ❌ | Free seminars, open tests, campus events for leads |
| 110 | WhatsApp Broadcast Manager | K4 | ✅ Dedicated | ✅ Shared | Result announcements, batch schedules, OTP routing |
| 111 | Topper Campaign Manager | K4 | ✅ Dedicated | ❌ | Topper events, press coverage, AIR announcement |

---

## Division M — Operations & Infrastructure (6 roles)

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 112 | Operations Manager | K6 | ✅ Dedicated | ❌ (Branch Mgr) | Daily ops, vendor management, SLA |
| 113 | Branch Coordinator | K5 | ✅ Per branch | ✅ 1 person | Liaison between HQ and branch |
| 114 | Infrastructure Manager | K0 | ✅ Dedicated | ❌ | Classrooms, ACs, projectors, seating — no login |
| 115 | IT Admin — Internal | K5 | ✅ Dedicated | ✅ Shared | EduForge config, smart boards, network |
| 116 | Library / Study Room Manager | K3 | ✅ Dedicated | ❌ | Study material library, book issue, e-resources |
| 117 | Canteen / Cafeteria Manager | K0 | ✅ Dedicated | ❌ | Food quality, timings — no platform access |

---

## Division N — Compliance & Safety (5 roles)

| # | Role | Level | Large | Medium | Owns |
|---|---|---|---|---|---|
| 118 | BGV Manager | K4 | ✅ Dedicated | ✅ 1 person | Background verification for all faculty/staff |
| 119 | POCSO Compliance Officer | K4 | ✅ Dedicated | ✅ Shared | POCSO for minor students — training, reporting |
| 120 | Data Privacy Officer | K1 | ✅ Dedicated | ✅ Shared | DPDP Act 2023 — student data, consent |
| 121 | POSH Committee Head | K4 | ✅ Dedicated | ✅ Shared | Women's safety — female staff + female students |
| 122 | Franchise Compliance Officer | K4 | ✅ Large only | ❌ | Ensure franchise branches follow brand + compliance |

---

## Division O — Parent & Guardian Access (4 roles)

> Only for minor students (Foundation Class 6–10 + dropper batch under 18).
> Adult coaching students (18+) get their own self-access — no parent portal.

| # | Role | Level | Applies To | Can Do in EduForge |
|---|---|---|---|---|
| 123 | Parent — Father | K1 | Minor students only | Attendance, test scores, fee, batch schedule |
| 124 | Parent — Mother | K1 | Minor students only | Same |
| 125 | Parent / Legal Guardian | K1 | Minor students | Full parent view for ward |
| 126 | Student — Self Access (18+) | K2 | All adult students | Own marks, notes, tests, fee, schedule |

---

## Division P — External Partners (5 roles)

| # | Role | Level | Who | Access |
|---|---|---|---|---|
| 127 | School Partner Admin | K1 | B2B school admin | View foundation batch students from their school |
| 128 | Franchise Partner Owner | K1 | Franchise branch owner | Their branch data — read only |
| 129 | Franchise Branch Manager | K5 | Franchise branch manager | Their branch full ops |
| 130 | Corporate Client HR (if CSR batch) | K1 | Company HR for employee upskilling | Their employees' batch data |
| 131 | Government Scheme Coordinator | K1 | Govt. skill development partner | Track govt-funded batch progress |

---

## Division Q — Support Staff — No Platform Access (5 roles)

| # | Role |
|---|---|
| 132 | Security Guard |
| 133 | Housekeeping / Sweeper |
| 134 | Electrician / Maintenance |
| 135 | Driver (if transport) |
| 136 | Office Boy / Peon |

---

## Full Role Count

| Division | Total | Large Uses | Medium Uses |
|---|---|---|---|
| A — Governance | 8 | 8 | 4–5 |
| B — Academic Leadership | 10 | 10 | 4–5 |
| C — Faculty Role Types | 20 | 20 | 8–12 |
| D — Batch Management | 7 | 7 | 3–4 |
| E — Test Series & Exam | 9 | 9 | 4–5 |
| F — Admissions & Sales | 10 | 10 | 4–6 |
| G — Finance & Fee | 8 | 8 | 3–4 |
| H — Online Delivery | 8 | 8 | 2–3 |
| I — Hostel Management | 10 | 10 | 2–3 (if hostel) |
| J — Student Affairs | 8 | 8 | 4–5 |
| K — Analytics & MIS | 6 | 6 | 1–2 |
| L — Marketing & Growth | 7 | 7 | 2–3 |
| M — Operations | 6 | 6 | 2–3 |
| N — Compliance & Safety | 5 | 5 | 3–4 |
| O — Parent & Student Access | 4 | 4 | 4 |
| P — External Partners | 5 | 5 | 2–3 |
| Q — Support Staff (K0) | 5 | 5 | 3–4 |
| **Total** | **136** | **136** | **~55** |

---

## Coaching vs School vs College — Key Differences

| Aspect | School | College | Coaching |
|---|---|---|---|
| Revenue model | Annual fee | Annual fee | Batch fee + renewals |
| Dropout risk | Low | Low | **High — KPI tracked daily** |
| Sales team | Not needed | Not needed | **Core function** |
| Demo classes | Not applicable | Not applicable | **Conversion driver** |
| Toppers | Internal recognition | Board toppers | **Public brand asset** |
| Online arm | Supplementary | Limited | **Equal to classroom** |
| Batch concurrency | 1 class/section | 1 section/stream | **200+ batches simultaneously** |
| Analytics depth | Marks + attendance | Marks + attendance | **Rank improvement + dropout prediction** |
| Parent role | High (minors) | Moderate | **Low — most students are adults** |
| Franchise model | ❌ | ❌ | **Common — major channel** |
| B2B | Rare | Rare | **School tie-ups — major revenue** |
| Hostel | Common | Common | **Only for dropper batches** |
