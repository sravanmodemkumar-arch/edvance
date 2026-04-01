# EduForge — Group 7: TSP (Test Series Platform) Roles

> TSP is a white-label product — any coaching, publisher, or individual
> can run their OWN branded test series powered by EduForge engine.
> Explicitly listed as a separate portal in EduForge architecture.

---

## TSP vs Exam Domains — Critical Difference

| Aspect | Group 6 — Exam Domains | Group 7 — TSP |
|---|---|---|
| Brand | EduForge's own brand | Operator's own brand |
| URL | ssc.eduforge.in | narayana.testpro.in |
| Content | EduForge SMEs create | Operator creates their own |
| Students | Public self-signup | Operator's enrolled students |
| Revenue | EduForge collects | Operator collects — pays EduForge SaaS fee |
| Control | EduForge controls all | Operator controls everything in their portal |
| Use case | National mock test for all | Coaching's own internal test series |

---

## Who Uses TSP

| TSP Operator Type | Example | Students |
|---|---|---|
| Large coaching chain | Narayana's own test series | Their own 15,000 students |
| Regional coaching | City-level institute's mock tests | 500–2,000 students |
| Individual educator / YouTuber | A YouTube teacher's paid test series | 100–50,000 subscribers |
| Publisher | Textbook company's practice tests | Book buyers |
| School chain | Group's internal exam platform | Their own school students |
| State govt. | Govt. scholarship entrance test | Lakh+ applicants |
| Corporate HR | Pre-employment assessment platform | Job applicants |

---

## System Access Levels — TSP

| Level | Label | Who |
|---|---|---|
| T0 | No Access | Support staff, marketing (internal tools) |
| T1 | Read Only | Investor, silent partner — analytics only |
| T2 | Content Creator | Create MCQs, notes — no publish |
| T3 | Content Reviewer | Review and approve content |
| T4 | Test Operations | Schedule tests, publish results, manage students |
| T5 | TSP Admin | Full portal config — branding, pricing, roles |
| T6 | TSP Super Admin | All TSP operators — EduForge platform team |

---

## Division A — TSP Operator Governance (6 roles)

| # | Role | Level | Who Holds It | Key Platform Actions |
|---|---|---|---|---|
| 1 | TSP Owner / Operator | T5 | Coaching director, YouTuber, publisher | Full TSP portal — branding, content, students, billing |
| 2 | TSP Co-Owner / Partner | T5 | Business partner of operator | Same scope as owner |
| 3 | TSP Admin | T5 | Designated tech admin | Portal config, user management, feature toggles |
| 4 | TSP Branch Manager | T5 | Per-branch manager (multi-branch operators) | One branch's TSP — staff, students, tests |
| 5 | TSP Franchise Operator | T5 | Franchise branch running TSP under parent brand | Their own students within franchise |
| 6 | TSP Reseller | T1 | Third party reselling TSP access | View their clients' aggregate data only |

---

## Division B — Content Management (8 roles)

| # | Role | Level | Large TSP | Small TSP | Owns |
|---|---|---|---|---|---|
| 7 | Content Head | T4 | ✅ Dedicated | ❌ (Owner covers) | All MCQ bank, notes, video for this TSP portal |
| 8 | Subject Expert — Quant / Maths | T2 | ✅ Dedicated | ✅ 1 person | Create Maths/Quant MCQs for their exam focus |
| 9 | Subject Expert — Reasoning | T2 | ✅ Dedicated | ✅ Shared | Verbal + non-verbal reasoning MCQs |
| 10 | Subject Expert — English | T2 | ✅ Dedicated | ✅ Shared | English grammar, comprehension MCQs |
| 11 | Subject Expert — GK / Subject | T2 | ✅ Dedicated | ✅ Shared | GK, current affairs, domain-specific subjects |
| 12 | Content Reviewer | T3 | ✅ Dedicated | ✅ 1 person | Review all MCQs — accuracy, language, difficulty |
| 13 | Content Approver | T3 | ✅ Dedicated | ✅ 1 person | Final publish gate — no question live without approval |
| 14 | Notes & Video Manager | T4 | ✅ Dedicated | ✅ Shared | Manage study notes, map YouTube videos to topics |

---

## Division C — Test Series Operations (8 roles)

| # | Role | Level | Large TSP | Small TSP | Owns |
|---|---|---|---|---|---|
| 15 | Test Series Manager | T4 | ✅ Dedicated | ✅ Owner covers | Full test calendar — schedule, types, sections |
| 16 | Test Scheduler | T4 | ✅ Dedicated | ❌ | Schedule each test, set duration, question count |
| 17 | Live Test Monitor | T4 | ✅ On exam day | ✅ Shared | Monitor active tests, handle student session issues |
| 18 | Answer Key Manager | T4 | ✅ Dedicated | ✅ Shared | Publish answer keys, manage student objections |
| 19 | Objection Handler | T3 | ✅ Dedicated | ❌ | Review + resolve student MCQ objections |
| 20 | Results Coordinator | T4 | ✅ Dedicated | ✅ Shared | Trigger rank computation, publish results |
| 21 | Rank & Analytics Officer | T4 | ✅ Dedicated | ❌ | Post-test analysis — topic-wise, difficulty, rank distribution |
| 22 | Certificate Generator | T4 | ✅ Dedicated | ✅ Shared | Generate rank certificates, email/download via EduForge |

---

## Division D — Student Management (7 roles)

| # | Role | Level | Owns |
|---|---|---|---|
| 23 | Student Enrollment Officer | T4 | Enrol students into TSP — batch assignment, access grant |
| 24 | Batch Coordinator | T4 | One batch — attendance, schedule, parent comm |
| 25 | Student Support Executive | T4 | Login issues, test access, result queries |
| 26 | Student Performance Counsellor | T4 | Track weak students — dropout risk, improvement plan |
| 27 | Parent Communication Officer | T4 | WhatsApp/SMS to parents of minor students |
| 28 | Scholarship / Access Officer | T4 | Free/subsidised access for scholarship students |
| 29 | Topper Recognition Manager | T4 | Rank holders — certificates, social media, brand value |

---

## Division E — Finance & Subscriptions (6 roles)

| # | Role | Level | Large TSP | Small TSP | Owns |
|---|---|---|---|---|---|
| 30 | Finance Manager | T1 | ✅ Dedicated | ❌ (Owner) | Revenue from subscriptions, Razorpay, EduForge fee |
| 31 | Fee Collection Executive | T4 | ✅ Dedicated | ✅ Owner | Collect student subscription fees, receipts |
| 32 | Subscription Plan Manager | T4 | ✅ Dedicated | ✅ Owner | Set subscription tiers — per test / monthly / annual |
| 33 | Refund Processing Executive | T4 | ✅ Dedicated | ✅ Shared | Validate and process refunds |
| 34 | B2B Billing Manager | T4 | ✅ Dedicated | ❌ | Bulk billing for coaching/school clients |
| 35 | EduForge Platform Fee Tracker | T1 | ✅ Dedicated | ✅ Owner | Track EduForge SaaS fee owed — per student/per test |

---

## Division F — Marketing & Growth (5 roles)

| # | Role | Level | Large TSP | Small TSP | Owns |
|---|---|---|---|---|---|
| 36 | Marketing Manager | T0 | ✅ Dedicated | ❌ (Owner) | TSP brand, acquisition campaigns |
| 37 | Social Media Manager | T0 | ✅ Dedicated | ✅ Owner | Telegram, Instagram, YouTube for test series |
| 38 | Affiliate / Referral Manager | T0 | ✅ Dedicated | ❌ | Student referral program, influencer tie-ups |
| 39 | Free Test Campaign Manager | T4 | ✅ Dedicated | ✅ Owner | Free tests as lead magnets — schedule, promote |
| 40 | Topper Campaign Manager | T0 | ✅ Dedicated | ❌ | AIR topper press, social media, lead conversion |

---

## Division G — Analytics & MIS (4 roles)

| # | Role | Level | Owns |
|---|---|---|---|
| 41 | Analytics Manager | T1 | Test performance MIS — batch, subject, rank distribution |
| 42 | Student Retention Analyst | T4 | Login gap + score drop = dropout risk signal |
| 43 | Revenue Analyst | T1 | Subscription revenue, churn rate, LTV |
| 44 | Competitive Benchmarking Analyst | T1 | How students rank vs EduForge national average |

---

## Division H — Compliance & Safety (4 roles)

| # | Role | Level | Owns |
|---|---|---|---|
| 45 | BGV Officer | T4 | BGV for all staff with student access |
| 46 | POCSO Officer | T4 | POCSO compliance for minor students in TSP |
| 47 | Data Privacy Officer | T1 | DPDP Act — student data, consent, breach |
| 48 | Anti-Cheating Officer | T4 | Online proctoring, malpractice investigation |

---

## Division I — EduForge → TSP Operator Interface (5 roles)

> These roles are on EduForge's side managing all TSP operators.

| # | Role | Level | Owns |
|---|---|---|---|
| 49 | TSP Onboarding Manager | T6 | Onboard new TSP operators — portal setup, training |
| 50 | TSP Account Manager | T6 | Ongoing relationship with each TSP operator |
| 51 | TSP Technical Support | T6 | API integration help, custom domain, branding config |
| 52 | TSP Billing Admin | T6 | Collect EduForge SaaS fees from all operators |
| 53 | TSP Compliance Auditor | T6 | Ensure all TSP operators follow EduForge policies |

---

## Full Role Count — Group 7

| Division | Total |
|---|---|
| A — Operator Governance | 6 |
| B — Content Management | 8 |
| C — Test Series Operations | 8 |
| D — Student Management | 7 |
| E — Finance & Subscriptions | 6 |
| F — Marketing & Growth | 5 |
| G — Analytics & MIS | 4 |
| H — Compliance & Safety | 4 |
| I — EduForge → TSP Interface | 5 |
| **Total** | **53** |
