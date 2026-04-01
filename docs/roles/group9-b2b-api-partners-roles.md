# EduForge — Group 12: B2B Technology & API Partners

> Companies, developers, and government bodies that integrate with EduForge
> or consume EduForge data/services via API or data partnership.

---

## Types of B2B / API Partners

| Partner Type | What They Do | Example |
|---|---|---|
| EdTech App Partner | Embed EduForge test engine in their app | School ERP companies |
| Content Publisher | Feed MCQ content into EduForge bank via API | Textbook publishers |
| HR / Assessment Company | Use EduForge MCQ engine for hiring | Job portals, staffing firms |
| State Govt. Integration | State education portal pulls student data | AP SCERT, TS SCERT |
| LMS Integration | Their LMS uses EduForge for assessments | Corporate L&D platforms |
| Analytics Aggregator | Consume anonymised data for research | EdTech research firms |
| Payment Gateway Partner | Razorpay, payment aggregators | Razorpay (existing) |
| SMS / WhatsApp Partner | MSG91, Meta — notification delivery | MSG91 (existing) |
| Cloud / Infra Partner | AWS, Cloudflare — infrastructure | AWS (existing) |

---

## System Access Levels — B2B Partners

| Level | Label | Access |
|---|---|---|
| B0 | No Platform Access | Contractual only — no system access |
| B1 | API Read Only | Read-only data via API — their students' data only |
| B2 | API Read + Write | Can push content/data into EduForge via API |
| B3 | Dashboard Access | View partner dashboard — analytics, billing, usage |
| B4 | Partner Admin | Manage their integration config, API keys, webhooks |
| B5 | EduForge Partner Manager | EduForge employee managing all partners |

---

## Division A — EdTech App & LMS Partners (8 roles)

| # | Role | Level | Who | Access |
|---|---|---|---|---|
| 1 | Partner CTO / Tech Lead | B4 | Partner company tech head | API config, webhook setup, sandbox access |
| 2 | Integration Developer | B4 | Partner's developer | API calls, test embedding, data sync |
| 3 | Partner Product Manager | B3 | Partner PM | Dashboard — usage metrics, student counts |
| 4 | Partner QA Engineer | B3 | Partner's QA | Test integration in sandbox environment |
| 5 | Partner Support Engineer | B3 | Partner's support | Resolve integration issues, API error logs |
| 6 | Partner Account Owner | B3 | Partner company director | Contract, billing, SLA |
| 7 | Data Sync Manager | B2 | Partner data team | Push student enrolment, pull results via API |
| 8 | Webhook Config Admin | B4 | Partner's DevOps | Configure webhooks for real-time events |

---

## Division B — Content Publisher Partners (6 roles)

| # | Role | Level | Who | Access |
|---|---|---|---|---|
| 9 | Publisher Content Head | B2 | Textbook company editorial head | Upload MCQ batches via API |
| 10 | Content Upload Engineer | B2 | Publisher's tech team | Bulk MCQ upload — subject, topic, difficulty tags |
| 11 | Content Quality Officer | B3 | Publisher's QA | View review queue status for submitted content |
| 12 | Publisher Account Manager | B3 | Publisher's commercial team | Contract, revenue share, billing dashboard |
| 13 | Royalty Tracker | B3 | Publisher finance | Track per-MCQ usage, royalty computation |
| 14 | Content IP Manager | B3 | Publisher legal | Ensure content attribution, IP rights tracking |

---

## Division C — Government Integration Partners (7 roles)

| # | Role | Level | Body | Access |
|---|---|---|---|---|
| 15 | State Education Dept. Admin | B3 | AP / TS Education Dept | Aggregated school/college data dashboard |
| 16 | SCERT Integration Officer | B2 | State SCERT | Pull curriculum-aligned MCQ data, push syllabus |
| 17 | Scholarship Portal Integrator | B2 | State scholarship portal | Student eligibility data for govt. scholarships |
| 18 | Skill India / PMKVY Partner | B2 | NSDC / Skill India | Govt-funded batch management, attendance, results |
| 19 | NIC Integration Officer | B2 | National Informatics Centre | DigiLocker integration for certificates |
| 20 | RTE Monitoring Officer | B1 | Govt RTE cell | Read-only RTE quota student compliance data |
| 21 | UDISE Integration Officer | B2 | UDISE+ portal (NCERT/Govt) | Push enrolment, attendance data to UDISE+ |

---

## Division D — HR & Assessment Partners (5 roles)

| # | Role | Level | Who | Access |
|---|---|---|---|---|
| 22 | HR Partner Tech Lead | B4 | Hiring company's tech | Integrate EduForge MCQ engine for screening tests |
| 23 | Assessment Designer | B2 | HR company's content team | Create custom question sets for hiring |
| 24 | Candidate Results Consumer | B1 | HR recruiter | View candidate test scores via API/dashboard |
| 25 | HR Partner Billing Admin | B3 | HR company finance | Per-candidate billing, usage-based invoices |
| 26 | Assessment Compliance Officer | B3 | HR company legal | Candidate data privacy, consent management |

---

## Division E — EduForge Partner Management Team (7 roles)

> EduForge's own team managing all B2B partners.

| # | Role | Level | Owns |
|---|---|---|---|
| 27 | Partner Ecosystem Director | B5 | Overall B2B strategy — which partners, what terms |
| 28 | Partner Onboarding Manager | B5 | New partner setup — API keys, sandbox, docs, training |
| 29 | Partner Account Manager | B5 | Ongoing relationship — renewals, upsell, issues |
| 30 | API Developer Relations (DevRel) | B5 | Developer documentation, SDKs, sample code |
| 31 | Partner Billing Admin | B5 | Invoice all partners, track API usage fees |
| 32 | Partner Compliance Officer | B5 | Ensure partners follow EduForge data policies |
| 33 | Partner Technical Support | B5 | API issues, webhook failures, integration bugs |

---

## Full Role Count — Group 12

| Division | Total |
|---|---|
| A — EdTech App & LMS Partners | 8 |
| B — Content Publisher Partners | 6 |
| C — Government Integration Partners | 7 |
| D — HR & Assessment Partners | 5 |
| E — EduForge Partner Management | 7 |
| **Total** | **33** |
