# EduForge — Roles & Permissions

Total: **87 distinct roles** across 6 groups.

---

## Group 1 — Platform Level (76 roles)

> EduForge company employees only — not institution staff.
> Mapped to 14 functional divisions covering every platform module.
> System access levels: 0=none · 1=read-only · 2=content · 3=tenant mgmt · 4=infra · 5=full

---

### Platform Modules Covered
Tenant Mgmt · User Mgmt · MCQ Bank · Notes · Videos · Exam Engine ·
Exam Day Operations · Results & Ranks · BGV · AI Generation ·
Notifications · Billing · Analytics · Support · Sales · Marketing ·
Compliance · Infrastructure · Incident Response

---

### Division A — Executive Leadership (4 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 1 | Platform Owner / CEO | Level 5 | Full access — all modules, all tenants, all data |
| 2 | Platform CTO | Level 5 | Technical config, architecture, infra, security keys |
| 3 | Platform COO | Level 3 | Operations, SLAs, support escalations, onboarding |
| 4 | Platform CFO | Level 1 | Revenue dashboards, GST reports, Razorpay settlements |

---

### Division B — Product & Design (5 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 5 | Product Manager — Platform | Level 3 | Feature flags, plan config, release management |
| 6 | Product Manager — Exam Domains | Level 3 | SSC/RRB/Board domain config, test series setup |
| 7 | Product Manager — Institution Portal | Level 3 | School/college/coaching portal features |
| 8 | UI/UX Designer | Level 1 | Read-only access for design review, no data edit |
| 9 | QA Engineer | Level 3 | Test all modules, create test users, validate flows |

---

### Division C — Engineering (8 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 10 | Platform Admin | Level 5 | All tenant mgmt, user provisioning, system config |
| 11 | Backend Engineer | Level 4 | API config, DB migrations, service deployments |
| 12 | Frontend Engineer | Level 4 | HTMX/Django templates, CDN cache invalidation |
| 13 | Mobile Engineer — Flutter | Level 4 | App builds, Hive encryption, FCM push config |
| 14 | DevOps / SRE Engineer | Level 4 | AWS Lambda, ECS, RDS, CI/CD pipelines, rollbacks |
| 15 | Database Administrator | Level 4 | PostgreSQL schemas, backups, migrations, query tuning |
| 16 | Security Engineer | Level 4 | JWT keys, AWS KMS, WAF rules, CERT-In reporting |
| 17 | AI / ML Engineer | Level 4 | MCQ generation pipeline, model tuning, prompt management |

---

### Division D — Content & Academics (13 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 18 | Content Director | Level 2 | All MCQ bank, notes, video strategy — all exam types |
| 19 | SME — Mathematics | Level 2 | Create/edit Maths MCQs (SSC, RRB, Board, Coaching) |
| 20 | SME — Physics | Level 2 | Create/edit Physics MCQs |
| 21 | SME — Chemistry | Level 2 | Create/edit Chemistry MCQs |
| 22 | SME — Biology | Level 2 | Create/edit Biology MCQs |
| 23 | SME — English | Level 2 | Grammar, comprehension, vocabulary questions |
| 24 | SME — General Knowledge | Level 2 | Current affairs, static GK, polity, history |
| 25 | SME — Reasoning | Level 2 | Verbal + non-verbal reasoning questions |
| 26 | SME — Computer Science | Level 2 | IT, programming, digital literacy questions |
| 27 | SME — Regional Language | Level 2 | Telugu, Hindi, regional board questions |
| 28 | Question Reviewer | Level 2 | Review MCQs for quality, flag errors, send back to SME |
| 29 | Question Approver | Level 2 | Final publish authority — no question live without this |
| 30 | Notes Editor | Level 2 | Format, structure, publish faculty notes |

---

### Division E — Video & Learning (3 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 31 | Video Curator | Level 2 | Map YouTube videos to subject → topic → exam |
| 32 | Playlist Manager | Level 2 | Create learning paths, order videos per syllabus |
| 33 | YouTube Channel Manager | Level 2 | Manage EduForge YouTube channel, upload, playlists |

---

### Division F — Exam Day Operations (5 roles)

> Critical division — 74,000 concurrent submissions need a dedicated ops team.

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 34 | Exam Operations Manager | Level 3 | Monitor all live exams, pause/extend on issues |
| 35 | Exam Support Executive | Level 3 | Handle student issues during live exam window |
| 36 | Results Coordinator | Level 3 | Trigger rank computation, review results before publish |
| 37 | Notification Manager | Level 3 | WhatsApp/SMS templates, broadcast results, alerts |
| 38 | Incident Manager — Exam Day | Level 4 | Escalate infra issues during exam, coordinate DevOps |

---

### Division G — Background Verification & Safety (3 roles)

> Required by POCSO Act 2012 — all staff working with minors must be BGV verified.

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 39 | BGV Manager | Level 3 | Manage BGV status of all staff across institutions |
| 40 | BGV Executive | Level 3 | Process verification requests, update BGV records |
| 41 | POCSO Compliance Officer | Level 1 | Audit BGV coverage, mandatory reporting dashboard |

---

### Division H — Data & Analytics (5 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 42 | Analytics Manager | Level 1 | Platform-wide MIS — usage, revenue, exam trends |
| 43 | Data Engineer | Level 4 | Build data pipelines, EventBridge jobs, aggregations |
| 44 | Data Analyst | Level 1 | Institution reports, rank trends, dropout signals |
| 45 | AI Generation Manager | Level 3 | Manage MCQ AI pipeline, approve AI batch outputs |
| 46 | Report Designer | Level 1 | Design MIS report templates for institutions |

---

### Division I — Customer Support (6 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 47 | Support Manager | Level 3 | Manage support team, SLA tracking, escalation rules |
| 48 | L1 Support Executive | Level 3 | Login issues, OTP problems, basic tenant queries |
| 49 | L2 Support Engineer | Level 3 | Bug investigation, DB read queries, log analysis |
| 50 | L3 Support Engineer | Level 4 | Code-level fix, hotfixes, DB writes, rollbacks |
| 51 | Onboarding Specialist | Level 3 | Train new institution admins, configure first setup |
| 52 | Training Coordinator | Level 2 | Create training material, conduct staff training sessions |

---

### Division J — Customer Success (4 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 53 | Customer Success Manager | Level 3 | Monitor institution health, retention, renewal pipeline |
| 54 | Account Manager | Level 3 | Existing institution relationships, upsell, expansion |
| 55 | Escalation Manager | Level 3 | Handle critical institution complaints, SLA breaches |
| 56 | Renewal Executive | Level 1 | Track subscription renewals, send reminders |

---

### Division K — Sales & Business Development (7 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 57 | B2B Sales Manager | Level 3 | Full institution onboarding pipeline, pricing approvals |
| 58 | Sales Executive — Schools | Level 3 | School acquisition, demo setup, trial activation |
| 59 | Sales Executive — Colleges | Level 3 | College/intermediate institution acquisition |
| 60 | Sales Executive — Coaching | Level 3 | Coaching centre acquisition |
| 61 | Partnership Manager | Level 3 | State board tie-ups, coaching chain deals, govt contracts |
| 62 | Demo Manager | Level 3 | Manage free trial tenants, demo data, sandbox reset |
| 63 | Channel Partner Manager | Level 1 | Manage reseller/partner network, commission tracking |

---

### Division L — Marketing & Growth (5 roles)

| # | Role | System Access | Level | Key Focus |
|---|---|---|---|---|
| 64 | Marketing Manager | Level 0 | Strategy, brand, campaigns across all domains |
| 65 | SEO / Content Executive | Level 0 | Blog, landing pages, exam prep content for organic traffic |
| 66 | Social Media Manager | Level 0 | YouTube, Instagram, Twitter — student community |
| 67 | Performance Marketing Exec | Level 0 | Google Ads, Meta Ads — school/coaching acquisition |
| 68 | Brand Manager | Level 0 | Visual identity per domain (SSC, RRB, Board brands) |

---

### Division M — Finance & Billing (6 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 69 | Finance Manager | Level 1 | Revenue reports, P&L, Razorpay reconciliation |
| 70 | Billing Admin | Level 3 | Subscription plans, invoice generation, refund processing |
| 71 | Accounts Receivable Exec | Level 1 | Outstanding fee tracking, payment follow-up |
| 72 | GST / Tax Consultant | Level 1 | SAC 9993 compliance, CGST/SGST/IGST filing |
| 73 | Refund Processing Exec | Level 3 | Validate and process student/institution refunds |
| 74 | Pricing Admin | Level 3 | Configure subscription tiers, discounts, promo codes |

---

### Division N — Legal, Compliance & HR (7 roles)

| # | Role | System Access | Key Permissions |
|---|---|---|---|
| 75 | Legal Officer | Level 1 | Contracts, ToS, privacy policy, regulatory filings |
| 76 | Data Privacy Officer (DPO) | Level 1 | DPDP Act 2023, data residency audit, breach 72hr notify |
| 77 | Regulatory Affairs Exec | Level 1 | TRAI (SMS), CERT-In, MeitY reporting |
| 78 | HR Manager | Level 0 | Internal staff — no platform access |
| 79 | Recruiter | Level 0 | Hiring only — no platform access |
| 80 | IT Admin (Internal) | Level 4 | Employee laptops, internal tools, VPN, GitHub access |
| 81 | Office Administrator | Level 0 | Facilities — no platform access |

---

### System Access Level Summary

| Level | Label | Who Has It | What They Can Do |
|---|---|---|---|
| 0 | No Access | HR, Marketing, Office Admin | Internal tools only, not the platform |
| 1 | Read Only | CFO, Legal, Analytics, Compliance | View dashboards and reports, no edits |
| 2 | Content | SMEs, Editors, Video Curator | Create, edit, publish content (MCQs, notes, videos) |
| 3 | Tenant Manager | Support, Sales, Account Mgr, Exam Ops | Manage institutions, users, subscriptions, exams |
| 4 | Infrastructure | Engineers, DevOps, DB Admin, Security | System config, deployments, DB access, keys |
| 5 | Super Admin | CEO, CTO, Platform Admin | Unrestricted access to everything |

---

## Group 2 — Institution Group Level (7 roles)

| Role | Scope |
|---|---|
| Group Chairman | All colleges/schools in group |
| Group CEO / Director | Operations across all branches |
| Group Academic Director | Curriculum, exams, results |
| Group Finance Director | Fees, billing, audits |
| Group IT Admin | All portals in group |
| Group HR Manager | Staff across branches |
| Group Audit Officer | Reports, MIS, compliance |

---

## Group 3 — School Roles (31 roles)

### Admin Staff (8 roles)

| Role | Key Permissions |
|---|---|
| School Owner / Chairman | Full school access |
| Principal | Academic + admin |
| Vice Principal | Academic oversight |
| Academic Director | Syllabus, exams |
| Exam Controller | Exams, results, ranks |
| Admission Coordinator | Enrolment, TC |
| Accountant / Finance | Fee collection, reports |
| Administrative Officer | General management |

### Teaching Staff (8 roles)

| Role | Key Permissions |
|---|---|
| HOD | Dept. teachers, syllabus |
| Senior Teacher | Classes, marks, attendance |
| Class Teacher | Attendance, behaviour, welfare |
| Subject Teacher | Lesson plans, marks |
| Lab Instructor | Practical schedules |
| Sports Coach | Physical, sports records |
| Librarian | Books, library records |
| Counsellor | Student welfare events |

### Support Staff (4 roles)

| Role | Key Permissions |
|---|---|
| Hostel Warden | Hosteler management |
| Hostel Matron | Daily welfare check |
| Transport Coordinator | Routes, vehicles |
| Security Staff | Gate entry logs |

### Student Types — School (9 roles)

| Type | Description |
|---|---|
| Day Scholar — Regular | Standard day student |
| Day Scholar — Scholarship | Fee concession tracking |
| Day Scholar — RTE | Right to Education quota |
| Hosteler — AC | Premium hostel |
| Hosteler — Non-AC | Standard hostel |
| Hosteler — Scholarship | Subsidised hostel |
| Special Needs | IEP tracking, welfare |
| NRI / Foreign National | Separate fee structure |
| TC Received | Transfer certificate in |

### Parent / Guardian Types — School (5 roles)

| Type | Access Level |
|---|---|
| Father | Full parent portal |
| Mother | Full parent portal |
| Guardian | Full parent portal |
| Emergency Contact | View only, notifications |
| Court-appointed Guardian | Restricted, POCSO-aware |

---

## Group 4 — College Roles (20 roles)

### Admin Staff (8 roles)

| Role |
|---|
| College Principal |
| Vice Principal |
| Dean of Academics |
| Examination Branch Head |
| Admission Officer |
| Student Affairs Officer |
| Placement Officer |
| Finance Officer |

### Faculty (6 roles)

| Role |
|---|
| Head of Department |
| Senior Lecturer |
| Lecturer |
| Guest Lecturer |
| Lab Instructor |
| NSS / NCC / Sports Coordinator |

### Student Types — College (6 roles)

| Type |
|---|
| Regular Student |
| Lateral Entry |
| Scholarship — Merit |
| Scholarship — Government |
| Hosteler |
| Fee Defaulter (restricted access) |

---

## Group 5 — Coaching Centre Roles (16 roles)

### Management (6 roles)

| Role |
|---|
| Institute Owner / Director |
| Branch Manager |
| Academic Coordinator |
| Sales / Admission Counsellor |
| Fee Collection Staff |
| Back Office / Data Entry |

### Faculty (4 roles)

| Role |
|---|
| Senior Faculty |
| Faculty |
| Demo / Guest Faculty |
| Online Faculty (recorded content) |

### Student Types — Coaching (6 roles)

| Type | Description |
|---|---|
| Regular Batch | Full-time classroom |
| Weekend Batch | Saturday/Sunday only |
| Online Batch | Live classes only |
| Correspondence | Material + tests only |
| Crash Course | Short duration |
| B2B (via institution tie-up) | Billed to institution |

---

## Group 6 — Online Mock Test Domain Roles (8 roles)

| Role | Description |
|---|---|
| Domain Admin | Manages one exam domain (SSC, RRB, etc.) |
| Content Creator | Writes and uploads MCQs |
| Question Reviewer | Reviews quality before publish |
| Question Approver | Final approval + publish |
| Student — Free | Limited tests/month |
| Student — Premium | Unlimited tests |
| Student — B2B | Via coaching institution subscription |
| Topper / Ranker | Special badge, leaderboard visibility |

---

## Permission Matrix

| Permission | Platform Admin | Group Director | Principal | HOD | Teacher | Student | Parent |
|---|---|---|---|---|---|---|---|
| View all tenants | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Manage institution | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Manage staff | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Manage students | ✅ | ✅ | ✅ | ❌ | partial | ❌ | ❌ |
| Take exam | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| View own child | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| Upload notes | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Create MCQs | ✅ | ❌ | ❌ | ✅ | ✅ | ❌ | ❌ |
| Approve MCQs | ✅ | ❌ | ❌ | ✅ | ❌ | ❌ | ❌ |
| View analytics | ✅ | ✅ | ✅ | ✅ | partial | own only | own child |
| Manage billing | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ | ❌ |
| Manage hostel | ✅ | ✅ | ✅ | ❌ | warden only | ❌ | ❌ |
| View results | ✅ | ✅ | ✅ | ✅ | own class | own only | own child |
