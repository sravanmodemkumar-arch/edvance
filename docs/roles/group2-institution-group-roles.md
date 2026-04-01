# EduForge — Group 2: Institution Group Level Roles

> Institution Groups are chains/trusts/societies owning multiple schools/colleges.
> Scale: 150 groups · 5 to 50 branches per group · ~1,900 total institutions.

---

## Two Types of Groups — Platform Must Support Both

### Large Group (Enterprise)
> Example: Narayana, Sri Chaitanya, Tirumala Educational Society
- 20–50 branches across multiple districts or states
- 20,000–1,00,000 students
- Hostelers (Boys + Girls, AC + Non-AC) + Day Scholars
- 500+ buses across all branches
- Dedicated hostel campuses separate from day school
- Multiple streams: MPC, BiPC, MEC, CEC, HEC
- Integrated JEE/NEET coaching with college
- IIT Foundation from Class 6
- Separate boys campus + girls campus in some branches
- Zone-level management layer between Group and Branch
- Full dedicated team for every function

### Small Group (SME Trust)
> Example: District education society, family-run 5-school chain
- 5–10 branches in one district
- 2,000–8,000 students
- Day scholars only OR small hostel (50–100 hostelers)
- 10–20 buses
- Single stream (MPC or BiPC)
- No zone layer — Group HQ directly manages branches
- One person wears multiple hats (Principal = Academic Director)

---

## Student Type Matrix — Group Must Track Both

| Student Type | Large Group | Small Group | Hostel? | Special Needs? |
|---|---|---|---|---|
| Day Scholar — Regular | ✅ | ✅ | ❌ | — |
| Day Scholar — Scholarship | ✅ | ✅ | ❌ | — |
| Day Scholar — RTE Quota | ✅ | ✅ | ❌ | — |
| Hosteler — Boys AC | ✅ | ❌ | ✅ | — |
| Hosteler — Boys Non-AC | ✅ | ✅ (if hostel) | ✅ | — |
| Hosteler — Girls AC | ✅ | ❌ | ✅ | — |
| Hosteler — Girls Non-AC | ✅ | ✅ (if hostel) | ✅ | — |
| Hosteler — Scholarship | ✅ | ✅ (if hostel) | ✅ | — |
| Special Needs — Day | ✅ | ✅ | ❌ | ✅ |
| Special Needs — Hosteler | ✅ | ❌ | ✅ | ✅ |
| NRI / Foreign National | ✅ | ❌ | ✅/❌ | — |
| Integrated Coaching Student | ✅ | ❌ | ✅ | — |

---

## System Access Levels

| Level | Label | Can Do |
|---|---|---|
| G0 | No Platform Access | External tools only — no EduForge login |
| G1 | Group Read Only | View all branches' dashboards, reports, MIS — no edits |
| G2 | Group Content | Upload/manage shared content library for all branches |
| G3 | Group Operations | Manage staff, students, fees, exams across all branches |
| G4 | Group Admin | Configure branch portals, roles, feature toggles |
| G5 | Group Super Admin | Full unrestricted access to every branch in the group |

---

## Division A — Group Governance (8 roles)

| # | Role | Level | Large Group | Small Group | Key Platform Actions |
|---|---|---|---|---|---|
| 1 | Group Chairman / Founder | G5 | ✅ Dedicated | ✅ Owner | All data, approve annual plan |
| 2 | Group Managing Director | G5 | ✅ Dedicated | ❌ (CEO covers) | User provisioning for principals |
| 3 | Group CEO | G4 | ✅ Dedicated | ✅ Same as Chairman | Activate/deactivate branches |
| 4 | Group President | G4 | ✅ Dedicated | ❌ | Approve exam schedules |
| 5 | Group Vice President | G4 | ✅ Dedicated | ❌ | Operational oversight |
| 6 | Group Board Member / Trustee | G1 | ✅ Multiple | ✅ 1–2 | Read-only governance dashboards |
| 7 | Group Executive Secretary | G3 | ✅ Dedicated | ❌ | Communication to all principals |
| 8 | Group Strategic Advisor | G1 | ✅ Dedicated | ❌ | View analytics, no edits |

---

## Division B — Group Academic Leadership (14 roles)

> Core of the platform — academic standardization across branches.
> A student in Branch A must compete fairly with Branch B.
> Both large and small groups need this — small groups share roles.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 9 | Chief Academic Officer (CAO) | G4 | ✅ Dedicated | ✅ (Principal covers) | Curriculum, exam calendar, result policy group-wide |
| 10 | Group Academic Director | G3 | ✅ Dedicated | ❌ | Syllabus design, teacher performance, academic MIS |
| 11 | Group Curriculum Coordinator | G2 | ✅ Dedicated | ✅ (shared) | Standardize lesson plans, upload shared study material |
| 12 | Group Exam Controller | G3 | ✅ Dedicated | ✅ (shared) | Central question papers, result moderation all branches |
| 13 | Group Results Coordinator | G3 | ✅ Dedicated | ❌ | Cross-branch rank computation, topper lists |
| 14 | Group Stream Coordinator — MPC | G3 | ✅ Dedicated | ❌ | Maths-Physics-Chemistry stream standardization |
| 15 | Group Stream Coordinator — BiPC | G3 | ✅ Dedicated | ❌ | Biology-Physics-Chemistry stream |
| 16 | Group Stream Coordinator — MEC/CEC | G3 | ✅ Dedicated | ❌ | Commerce streams |
| 17 | Group JEE/NEET Integration Head | G3 | ✅ Dedicated | ❌ | Integrated coaching schedule, test series for JEE/NEET |
| 18 | Group IIT Foundation Director | G3 | ✅ Dedicated | ❌ | Class 6–10 IIT foundation program management |
| 19 | Group Olympiad & Scholarship Coordinator | G3 | ✅ Dedicated | ✅ (shared) | NTSE, NMMS, NSO, IMO, KVPY exam coordination |
| 20 | Group Special Education Coordinator | G3 | ✅ Dedicated | ✅ (shared) | IEP for special needs students across all branches |
| 21 | Group Academic MIS Officer | G1 | ✅ Dedicated | ✅ (shared) | Subject-wise, branch-wise, teacher-wise performance |
| 22 | Group Academic Calendar Manager | G3 | ✅ Dedicated | ✅ (shared) | Working days, PTM, holidays, sports day across all branches |

---

## Division C — Group Admissions (7 roles)

> Admissions are the lifeblood — both large and small groups run campaigns.
> Large groups have centralized admission + branch allocation.
> Small groups let each branch handle their own but report to group.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 23 | Group Admissions Director | G3 | ✅ Dedicated | ✅ (CEO covers) | Seat allocation, admission criteria, cut-offs per branch |
| 24 | Group Admission Coordinator | G3 | ✅ Dedicated | ✅ Shared | Centralized application pipeline, branch-wise allocation |
| 25 | Group Admission Counsellor | G3 | ✅ Multiple | ✅ 1 | Student counselling, scholarship recommendation |
| 26 | Group Scholarship Exam Manager | G3 | ✅ Dedicated | ✅ Shared | Entrance tests, scholarship exams, results |
| 27 | Group Scholarship Manager | G3 | ✅ Dedicated | ✅ Shared | Merit + need scholarships, waiver approvals |
| 28 | Group Alumni Relations Manager | G3 | ✅ Dedicated | ❌ | Alumni network, topper database, referral admissions |
| 29 | Group Demo Class Coordinator | G3 | ✅ Dedicated | ❌ | Coordinate demo/trial classes for prospective students |

---

## Division D — Group Finance & Billing (11 roles)

> Large groups collect crores in fees across 50 branches.
> Day scholar fee ≠ Hosteler fee ≠ Integrated coaching fee.
> Small groups have simpler structure but still need financial oversight.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 30 | Group CFO / Finance Director | G1 | ✅ Dedicated | ✅ (Chairman covers) | Group P&L, revenue per branch, EduForge billing |
| 31 | Group Finance Manager | G1 | ✅ Dedicated | ❌ | Monthly branch reconciliation, audit reports |
| 32 | Group Accounts Manager | G1 | ✅ Dedicated | ❌ | Ledger, payable/receivable cross-branch |
| 33 | Group Fee Structure Manager | G3 | ✅ Dedicated | ✅ Shared | Day scholar fee, hosteler fee, coaching fee per branch |
| 34 | Group Fee Collection Head | G3 | ✅ Dedicated | ❌ | Defaulter tracking, waiver approvals cross-branch |
| 35 | Group Scholarship Finance Officer | G3 | ✅ Dedicated | ✅ Shared | Scholarship disbursement, government grant tracking |
| 36 | Group Internal Auditor | G1 | ✅ Dedicated | ✅ 1 person | Quarterly branch audits, irregularity detection |
| 37 | Group GST / Tax Officer | G1 | ✅ Dedicated | ✅ Shared | SAC 9993, CGST/SGST/IGST, TDS compliance |
| 38 | Group EduForge Billing Coordinator | G3 | ✅ Dedicated | ✅ 1 person | Renew/upgrade EduForge plans, raise support tickets |
| 39 | Group Procurement Finance | G1 | ✅ Dedicated | ❌ | Vendor payments for books, uniforms, lab equipment |
| 40 | Group Payroll Coordinator | G0 | ✅ Dedicated | ❌ | Salary across all branches — payroll software only |

---

## Division E — Group HR & Staff Management (12 roles)

> Large groups have 3,000+ staff across branches.
> BGV is mandatory for all staff with access to minors (POCSO).
> Small groups hire locally but BGV is still mandatory.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 41 | Group HR Director | G3 | ✅ Dedicated | ✅ (CEO covers) | Hiring policy, grade bands, compensation |
| 42 | Group HR Manager | G3 | ✅ Dedicated | ❌ | Recruitment, onboarding, exit across all branches |
| 43 | Group Recruiter — Teaching | G0 | ✅ Multiple | ❌ | Teacher campus hiring, ATS tool only |
| 44 | Group Recruiter — Non-Teaching | G0 | ✅ Dedicated | ❌ | Admin, hostel, transport staff hiring |
| 45 | Group Training & Development Manager | G2 | ✅ Dedicated | ✅ Shared | CPD programs, induction training for new staff |
| 46 | Group Performance Review Officer | G1 | ✅ Dedicated | ✅ Shared | Annual teacher appraisal, promotion recommendations |
| 47 | Group Staff Transfer Coordinator | G3 | ✅ Dedicated | ❌ | Inter-branch transfers — Branch cannot self-transfer |
| 48 | Group BGV Manager | G3 | ✅ Dedicated | ✅ 1 person | BGV status for all staff across all branches |
| 49 | Group BGV Executive | G3 | ✅ Multiple | ❌ | Process BGV, update verification status |
| 50 | Group POCSO Coordinator | G3 | ✅ Dedicated | ✅ Shared | POCSO training, incident reporting, child safety audits |
| 51 | Group Disciplinary Committee Head | G3 | ✅ Dedicated | ✅ Shared | Staff misconduct cases, show-cause, dismissal |
| 52 | Group Employee Welfare Officer | G3 | ✅ Dedicated | ❌ | Staff welfare, medical insurance, grievances |

---

## Division F — Group IT & Technology (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 53 | Group IT Director | G4 | ✅ Dedicated | ❌ (CEO covers) | Technology strategy, EduForge integration |
| 54 | Group IT Admin | G4 | ✅ Dedicated | ✅ 1 person | All branch portal config, user roles, feature toggles |
| 55 | Group Data Privacy Officer | G1 | ✅ Dedicated | ✅ Shared | DPDP Act 2023 — consent, data residency, breach |
| 56 | Group Cybersecurity Officer | G1 | ✅ Dedicated | ❌ | Device policy, phishing, data handling across branches |
| 57 | Group IT Support Executive | G3 | ✅ Multiple | ✅ 1 person | Tech support for all branch staff on EduForge |
| 58 | Group EduForge Integration Manager | G4 | ✅ Dedicated | ❌ | API integrations, SSO, custom domain setup per branch |

---

## Division G — Group Operations (8 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 59 | Group COO | G4 | ✅ Dedicated | ❌ (CEO covers) | Day-to-day ops across all branches |
| 60 | Group Operations Manager | G3 | ✅ Dedicated | ❌ | Branch SLAs, grievance resolution, escalations |
| 61 | Group Branch Coordinator | G3 | ✅ Multiple | ✅ 1 | Liaison between HQ and each branch principal |
| 62 | Group Zone Director | G4 | ✅ Large only | ❌ | Zone of 10–15 branches between Group and Branch |
| 63 | Group Zone Academic Coordinator | G3 | ✅ Large only | ❌ | Academic oversight for one zone |
| 64 | Group Zone Operations Manager | G3 | ✅ Large only | ❌ | Operations for one zone |
| 65 | Group Procurement Manager | G0 | ✅ Dedicated | ❌ | Bulk purchase of books, uniforms, lab equipment |
| 66 | Group Facilities Manager | G0 | ✅ Dedicated | ❌ | Buildings, maintenance across campuses |

---

## Division H — Hostel Management (12 roles)

> Critical for groups with hostelers.
> Boys and Girls hostels are ALWAYS separate — never shared management.
> AC and Non-AC hostels have different fee structures and amenities.
> Small groups with 50–100 hostelers: 2–3 hostel roles only.

| # | Role | Level | Large | Small (if hostel) | Owns |
|---|---|---|---|---|---|
| 67 | Group Hostel Director | G3 | ✅ Dedicated | ✅ 1 person | Hostel policy, welfare standards across all branches |
| 68 | Group Boys Hostel Coordinator | G3 | ✅ Dedicated | ❌ | All boys hostels — warden supervision, discipline |
| 69 | Group Girls Hostel Coordinator | G3 | ✅ Dedicated | ❌ | All girls hostels — warden supervision, safety |
| 70 | Group Hostel Welfare Officer | G3 | ✅ Dedicated | ✅ Shared | Daily welfare monitoring, incident escalation |
| 71 | Group Mess / Cafeteria Manager | G3 | ✅ Dedicated | ❌ | Food quality, menu standards, hygiene across hostels |
| 72 | Group Hostel Admission Coordinator | G3 | ✅ Dedicated | ✅ Shared | Hosteler seat allocation across branches |
| 73 | Group Hostel Fee Manager | G3 | ✅ Dedicated | ✅ Shared | AC/Non-AC fee, mess charges, extra charges |
| 74 | Group Hostel Security Coordinator | G3 | ✅ Dedicated | ❌ | Night security, CCTV policy, visitor management |
| 75 | Group Parent Visit Coordinator | G3 | ✅ Dedicated | ✅ Shared | Schedule parent visits, biometric entry for hostelers |
| 76 | Group Hostel Medical Coordinator | G3 | ✅ Dedicated | ✅ Shared | Medical rooms, first aid, doctor visits schedule |
| 77 | Group Laundry / Housekeeping Coord | G0 | ✅ Large only | ❌ | Housekeeping standards, laundry services |
| 78 | Group Hostel Discipline Committee | G3 | ✅ Dedicated | ✅ Shared | Hosteler misconduct, suspension from hostel |

---

## Division I — Transport Management (6 roles)

> Large groups run 200–500 buses across all branches.
> Day scholars need transport — hostelers do not (they live on campus).
> Small groups: 10–20 buses, 1–2 transport roles only.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 79 | Group Transport Director | G3 | ✅ Dedicated | ✅ 1 person | Fleet policy, route approval, GPS monitoring |
| 80 | Group Fleet Manager | G3 | ✅ Dedicated | ❌ | Vehicle maintenance, fitness certificates, permits |
| 81 | Group Route Planning Manager | G3 | ✅ Dedicated | ❌ | Route optimization, pickup/drop points across branches |
| 82 | Group Transport Fee Manager | G3 | ✅ Dedicated | ✅ Shared | Transport fee per route, per branch |
| 83 | Group Driver/Conductor HR | G0 | ✅ Dedicated | ❌ | Driver hiring, training, license verification |
| 84 | Group Transport Safety Officer | G3 | ✅ Dedicated | ✅ Shared | GPS tracking, accident reporting, student safety |

---

## Division J — Health & Medical (5 roles)

> Large campuses with hostelers need dedicated medical infrastructure.
> Day scholar schools need first aid + emergency response.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 85 | Group Medical Coordinator | G3 | ✅ Dedicated | ✅ Shared | Medical rooms, doctor visit schedule across branches |
| 86 | Group School Medical Officer | G3 | ✅ Dedicated | ❌ | On-campus doctor coordination, prescription records |
| 87 | Group Mental Health Coordinator | G3 | ✅ Dedicated | ✅ Shared | Counselling services, exam stress, student wellbeing |
| 88 | Group Medical Insurance Coordinator | G0 | ✅ Dedicated | ✅ Shared | Student accident insurance, claim processing |
| 89 | Group Emergency Response Officer | G3 | ✅ Dedicated | ✅ Shared | Fire, medical emergency protocols across all branches |

---

## Division K — Welfare & Safety (7 roles)

> POCSO mandates child safety infrastructure.
> Both large and small groups are equally liable.

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 90 | Group Child Protection Officer | G3 | ✅ Dedicated | ✅ 1 person | Child safety policy, complaint handling, NCPCR reporting |
| 91 | Group Anti-Ragging Committee Head | G3 | ✅ Dedicated | ✅ Shared | Anti-ragging policy, UGC compliance, investigation |
| 92 | Group Grievance Redressal Officer | G3 | ✅ Dedicated | ✅ Shared | Student/parent complaints escalated from branches |
| 93 | Group CCTV & Security Head | G3 | ✅ Dedicated | ❌ | CCTV coverage policy, security guard management |
| 94 | Group Counselling Head | G3 | ✅ Dedicated | ✅ Shared | Career counselling, peer counselling, college guidance |
| 95 | Group Welfare Events Coordinator | G3 | ✅ Dedicated | ✅ Shared | Track welfare events (Severity 1–4) across all branches |
| 96 | Group Safety Audit Officer | G1 | ✅ Dedicated | ❌ | Annual safety inspections, compliance reports |

---

## Division L — Sports & Extra-Curricular (5 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 97 | Group Sports Director | G3 | ✅ Dedicated | ✅ Shared | Sports policy, inter-branch tournaments, state team |
| 98 | Group Sports Coordinator | G3 | ✅ Dedicated | ❌ | Coach management, equipment, sports calendar |
| 99 | Group Cultural Activities Head | G3 | ✅ Dedicated | ✅ Shared | Annual day, competitions, debate, quiz across branches |
| 100 | Group NSS / NCC Coordinator | G3 | ✅ Dedicated | ✅ Shared | National Service Scheme, NCC camps, civic programs |
| 101 | Group Library & Learning Resources Head | G2 | ✅ Dedicated | ✅ Shared | Central e-library, shared digital resources across branches |

---

## Division M — Analytics & MIS (6 roles)

| # | Role | Level | Large | Small | Key Reports |
|---|---|---|---|---|---|
| 102 | Group Analytics Director | G1 | ✅ Dedicated | ❌ | Cross-branch performance intelligence |
| 103 | Group MIS Officer | G1 | ✅ Dedicated | ✅ 1 person | Monthly MIS for Chairman/Board — attendance, fee, results |
| 104 | Group Academic Data Analyst | G1 | ✅ Dedicated | ❌ | Dropout signals, rank trends, teacher performance |
| 105 | Group Exam Analytics Officer | G1 | ✅ Dedicated | ❌ | Test performance heatmaps per branch, topic-wise gaps |
| 106 | Group Hostel Analytics Officer | G1 | ✅ Dedicated | ❌ | Hosteler welfare trends, occupancy, fee collection |
| 107 | Group Strategic Planning Officer | G1 | ✅ Dedicated | ❌ | New branch feasibility, 3-year expansion plan |

---

## Division N — Legal & Compliance (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 108 | Group Legal Officer | G0 | ✅ Dedicated | ❌ (owner handles) | Trust deed, land, staff contracts, regulatory filings |
| 109 | Group Compliance Manager | G1 | ✅ Dedicated | ✅ Shared | CBSE/State Board affiliation compliance all branches |
| 110 | Group RTI Officer | G1 | ✅ Dedicated | ✅ Shared | Right to Information responses |
| 111 | Group Regulatory Affairs Officer | G0 | ✅ Dedicated | ❌ | State education dept filings, AISHE, NITI Aayog |
| 112 | Group POCSO Reporting Officer | G1 | ✅ Dedicated | ✅ Shared | Mandatory NCPCR reporting, child welfare coordination |
| 113 | Group Data Privacy Officer | G1 | ✅ Dedicated | ✅ Shared | DPDP Act 2023 — consent, 72hr breach notification |

---

## Division O — Marketing & Admissions Campaigns (7 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 114 | Group Marketing Director | G0 | ✅ Dedicated | ❌ | Brand strategy, campaigns across all branches |
| 115 | Group Brand Manager | G0 | ✅ Dedicated | ❌ | Visual identity, branch signage, brand standards |
| 116 | Group Digital Marketing Executive | G0 | ✅ Dedicated | ✅ Shared | Google Ads, Meta Ads, YouTube for group + branches |
| 117 | Group PR & Communications Manager | G0 | ✅ Dedicated | ❌ | Topper press releases, media relations |
| 118 | Group Social Media Manager | G0 | ✅ Dedicated | ✅ Shared | WhatsApp broadcasts, Instagram, YouTube community |
| 119 | Group Admissions Campaign Manager | G3 | ✅ Dedicated | ✅ Shared | Cross-branch enrollment drive, leads, conversion |
| 120 | Group Topper Relations Manager | G3 | ✅ Dedicated | ❌ | Toppers as brand ambassadors — scholarships, events |

---

## Division P — Audit & Quality (6 roles)

| # | Role | Level | Large | Small | Owns |
|---|---|---|---|---|---|
| 121 | Group Internal Audit Head | G1 | ✅ Dedicated | ✅ 1 person | Annual financial + academic audit every branch |
| 122 | Group Academic Quality Officer | G1 | ✅ Dedicated | ✅ Shared | Lesson plan compliance, teaching quality inspections |
| 123 | Group Inspection Officer | G3 | ✅ Multiple | ✅ Shared | Physical branch visits, on-site data verification |
| 124 | Group ISO / NAAC Coordinator | G1 | ✅ Dedicated | ❌ | Quality certification compliance |
| 125 | Group Affiliation Compliance Officer | G1 | ✅ Dedicated | ✅ Shared | CBSE/BSEAP/BSETS affiliation renewal, inspections |
| 126 | Group Grievance Audit Officer | G1 | ✅ Dedicated | ❌ | Audit complaint resolution across branches |

---

## Full Role Count

| Division | Total | Large Uses | Small Uses |
|---|---|---|---|
| A — Governance | 8 | 8 | 3–4 |
| B — Academic Leadership | 14 | 14 | 4–5 |
| C — Admissions | 7 | 7 | 3–4 |
| D — Finance & Billing | 11 | 11 | 4–5 |
| E — HR & Staff | 12 | 12 | 3–4 |
| F — IT & Technology | 6 | 6 | 2–3 |
| G — Operations | 8 | 8 | 2–3 |
| H — Hostel Management | 12 | 12 | 2–3 (if hostel) |
| I — Transport Management | 6 | 6 | 1–2 |
| J — Health & Medical | 5 | 5 | 2–3 |
| K — Welfare & Safety | 7 | 7 | 3–4 |
| L — Sports & Extra-Curricular | 5 | 5 | 2–3 |
| M — Analytics & MIS | 6 | 6 | 1–2 |
| N — Legal & Compliance | 6 | 6 | 3–4 |
| O — Marketing & Admissions | 7 | 7 | 2–3 |
| P — Audit & Quality | 6 | 6 | 2–3 |
| **Total** | **126** | **126** | **~40** |

---

## Group vs Branch — Who Controls What

| Action | Group Level | Branch Level |
|---|---|---|
| Create/delete a branch portal | Group IT Admin ✅ | Branch Principal ❌ |
| Hire a teacher | Group HR ✅ | Principal ✅ (within quota) |
| Transfer a teacher between branches | Group Staff Transfer ✅ | Branch ❌ |
| Set fee structure (day scholar / hosteler) | Group Finance ✅ | Branch Accountant ❌ |
| Approve scholarship | Group Scholarship Mgr ✅ | Branch recommends only |
| Set exam calendar | Group Exam Controller ✅ | Branch (local tests only) |
| View all branches results | Group Academic MIS ✅ | Branch (own only) ❌ |
| BGV a new staff member | Group BGV Manager ✅ | Branch cannot do alone |
| Allocate hostel room | Group Hostel Coord ✅ | Branch Hostel Warden ✅ |
| Approve transport route | Group Transport Dir ✅ | Branch cannot add route |
| Raise EduForge support ticket | Group EduForge Billing ✅ | Branch IT Admin (limited) |
| POCSO incident reporting | Group POCSO Coord ✅ | Branch Principal (trigger only) |
| Publish exam results cross-branch | Group Results Coord ✅ | Branch ❌ |
| Configure WhatsApp notifications | Group IT Admin ✅ | Branch cannot configure |

---

## Day Scholar vs Hosteler — Functional Differences

| Function | Day Scholar Only Branch | Hosteler Branch |
|---|---|---|
| Fee structure | Tuition + transport | Tuition + hostel (AC/Non-AC) + mess + extras |
| Attendance | Daily morning session | Daily + night roll call |
| Parent communication | Daily SMS/WhatsApp | Weekly welfare update + restricted calling hours |
| Medical | First aid + emergency | On-campus doctor + medical room + night duty |
| Safety | Gate in/out with ID | Biometric entry + visitor register + CCTV |
| Welfare monitoring | Basic welfare events | Severity 1–4 welfare tracking (daily) |
| Transport | Required (buses) | Not required (on campus) |
| Mess | Not applicable | Menu planning + hygiene audits + mess fee |
| Night security | Not applicable | 24/7 security guards + CCTV + warden on duty |
| Student type roles | 3 types | 9 types (AC/Non-AC × Boys/Girls × Scholarship) |
