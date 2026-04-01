# EduForge — Group 1: Platform Level Roles

> EduForge company employees only. Not institution staff.
> Total: **108 roles** across **15 divisions**.

---

## Scale Context

| Segment | Institutions | Students |
|---|---|---|
| Schools | 1,000 | ~10,00,000 |
| Colleges (Intermediate) | 800 | ~4,80,000 |
| Coaching Centres | 100 | ~10,00,000 |
| Institution Groups | 150 | (child institutions counted above) |
| **Total** | **2,050** | **~24L – 76L (2.4M – 7.6M)** |

| Platform Metric | Value |
|---|---|
| Peak concurrent exam load | **74,000 simultaneous submissions** |
| Questions in bank | **2M+** |
| Active test series | **800+** |
| Mobile app installs | **~3M+** (Flutter — iOS + Android) |
| Platform ARR | **₹18Cr – ₹90Cr** |
| Institution staff with minor access (BGV required) | **~28,000 across 1,900+ institutions** |
| Total institutional staff | **~1,00,000+** |

---

## Platform Modules → Role Ownership

| Module | Owned By |
|---|---|
| Tenant onboarding / offboarding | Sales + Support + Engineering |
| User management across all tenants | Platform Admin + L2/L3 Support |
| MCQ Bank (create, review, publish) | Content + SMEs |
| Notes (upload, structure, publish) | Content + Notes Editor |
| Video Library (YouTube curation) | Video & Learning — Phase 1 |
| Video Production Pipeline | Video & Learning — Phase 2 (Production Team) |
| Exam Engine (live tests, timing) | Exam Operations |
| Exam Pre-configuration & Paper Setup | Exam Operations + Config Specialist |
| Exam Day Monitoring (74K concurrent) | Exam Operations + DevOps |
| Exam Integrity & Malpractice Detection | Exam Operations + Integrity Officer |
| Results & Rank Computation | Results Coordinator + Data |
| BGV for institution staff (POCSO) | BGV Division |
| AI-based MCQ Generation | AI/ML Engineer + AI Generation Manager |
| WhatsApp / SMS / Email Notifications | Notification Manager + Exam Ops |
| Billing & Subscriptions | Finance + Billing Admin |
| Analytics & MIS | Data & Analytics |
| DPDP / POCSO Compliance | Legal & Compliance |
| Infrastructure (Lambda, RDS, CDN, Memcached) | Engineering + DevOps |
| Incident Response (Exam Day) | Incident Manager + SRE |

---

## System Access Levels

| Level | Label | Can Do |
|---|---|---|
| 0 | No Platform Access | Internal tools only (HR, Marketing, Admin portals) |
| 1 | Read Only | Dashboards, reports, audit logs — no edits |
| 2 | Content Manager | Create, edit, approve content (MCQ, notes, videos) |
| 3 | Tenant Manager | Manage institutions, users, exams, subscriptions |
| 4 | Infrastructure | System config, DB access, deployments, security keys |
| 5 | Super Admin | Unrestricted — all data, all tenants, all modules |

---

## Division A — Executive Leadership (4 roles)

> Base URL: `/exec/` · Theme: Dark

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 1 | Platform Owner / CEO | 5 | Everything — full platform authority | — |
| 2 | Platform CTO | 5 | Tech architecture, infra, security, deployments | Commercial deals |
| 3 | Platform COO | 3 | Operations, SLAs, team management, support escalations | Infra config, billing |
| 4 | Platform CFO | 1 | Revenue reports, GST, Razorpay settlements | Any data edit |

---

## Division B — Product & Design (5 roles)

> Base URL: `/product/` · Theme: Dark

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 5 | Product Manager — Platform | 3 | Feature flags, plan config, release notes, product roadmap, A/B tests, announcements, mobile app config, revenue dashboard | Infra config, billing |
| 6 | Product Manager — Exam Domains | 3 | SSC/RRB/Board domain config, exam patterns, syllabus builder, test series management, domain analytics, question bank management | Content publish (Division D Approver only) |
| 7 | Product Manager — Institution Portal | 3 | School/college/coaching portal features, institution role config, portal templates, onboarding workflows, notification templates, white-label branding | Infra config |
| 8 | UI/UX Designer | 1 | Read-only — design review, component audit, design issue logging | All writes blocked |
| 9 | QA Engineer | 3 | Test all modules, create test tenants, validate flows, defect tracking, performance testing (74K load), student impersonation on test tenants | Production data edit |

---

## Division C — Engineering (8 roles)

> Base URL: `/engineering/` · Cache: Memcached (no Redis) · DB: PostgreSQL 15 · 2,051 schemas

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 10 | Platform Admin | 5 | All tenant management, user provisioning, system config, emergency overrides | Nothing blocked |
| 11 | Backend Engineer | 4 | API config, Lambda service deployments, DB migrations, Celery beat, service health | Billing config |
| 12 | Frontend Engineer | 4 | HTMX templates, CDN cache invalidation, R2/S3 static assets, Core Web Vitals | DB access |
| 13 | Mobile Engineer — Flutter | 4 | Flutter builds, Hive encryption, FCM config, app store submissions, APNs/keystore | DB access, secret rotation |
| 14 | DevOps / SRE Engineer | 4 | AWS Lambda, ECS, RDS, CI/CD, auto-scaling, rollbacks, on-call, AWS cost monitoring, DNS/SSL cert management | Content, billing |
| 15 | Database Administrator | 4 | PostgreSQL all 2,051 schemas, backups, migrations, query tuning, PITR, PgBouncer | Business config |
| 16 | Security Engineer | 4 | JWT secret rotation, KMS, WAF rules, CERT-In reports, DPDP breach coordination, VAPT scheduling | Content, billing |
| 17 | AI / ML Engineer | 4 | MCQ generation pipeline, LLM model config, prompt versioning, AI API cost management | Content approval |

---

## Division D — Content & Academics (13 roles)

> Base URL: `/content/`
> Each SME owns their subject end-to-end.
> One wrong question at 74K concurrent = mass rank distortion across all institutions.
> **Only the Question Approver (Role 29) can publish MCQs — enforced at model layer, not just UI.**

| # | Role | Level | Subject Scope | Can Publish MCQs? | Can Publish Notes? |
|---|---|---|---|---|---|
| 18 | Content Director | 2 | All subjects, all exam types — pipeline oversight | No — Approver gate is absolute | No (can approve notes if toggle enabled) |
| 19 | SME — Mathematics | 2 | Arithmetic, Algebra, Geometry, Data Interpretation, Calculus | No | No |
| 20 | SME — Physics | 2 | Mechanics, Optics, Electricity, Modern Physics | No | No |
| 21 | SME — Chemistry | 2 | Organic, Inorganic, Physical Chemistry | No | No |
| 22 | SME — Biology | 2 | Botany, Zoology, Human Physiology | No | No |
| 23 | SME — English | 2 | Grammar, Reading Comprehension, Vocabulary, Error Spotting | No | No |
| 24 | SME — General Knowledge | 2 | Current Affairs, Polity, History, Geography, Economy | No | No |
| 25 | SME — Reasoning | 2 | Verbal, Non-Verbal, Logical, Analytical Reasoning | No | No |
| 26 | SME — Computer Science | 2 | IT Fundamentals, Programming, Digital Literacy | No | No |
| 27 | SME — Regional Language | 2 | Telugu, Hindi, Urdu for State Board exams | No | No |
| 28 | Question Reviewer | 2 | All subjects — quality check, factual accuracy, language, formatting | No — sends back or forward to Approver | No |
| 29 | Question Approver | 2 | All subjects — **final publish gate** | **Yes — sole MCQ publish authority** | No |
| 30 | Notes Editor | 2 | Structures, formats, tags all faculty-uploaded notes | No | **Yes — notes only** |

---

## Division E — Video & Learning (11 roles)

> Base URL: `/content/video/`
> Phase 1 (Roles 31–33): YouTube curation and channel management.
> Phase 2 (Roles 82–89): In-house video production pipeline.
> Every MCQ in the question bank can have a corresponding explanatory video from this division.

### Phase 1 — Curation & Channel

| # | Role | Level | Owns |
|---|---|---|---|
| 31 | Video Curator | 2 | Map YouTube videos → subject → topic → exam type taxonomy |
| 32 | Playlist Manager | 2 | Create structured learning paths per syllabus and exam type |
| 33 | YouTube Channel Manager | 2 | EduForge official channel — uploads, playlists, metadata management |

### Phase 2 — Production Pipeline

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 82 | Content Producer — Video | 2 | End-to-end production pipeline management, commission briefs, SLA ownership, final publish trigger | Cannot approve scripts (Script Reviewer 84 owns that) |
| 83 | Video Scriptwriter | 2 | Author scripts from MCQ briefs, incorporate SME-provided explanations | Cannot approve own scripts; cannot upload animation or edit assets |
| 84 | Script Reviewer | 2 | Review scripts for factual accuracy, pedagogy, language quality; approve or return | Cannot author scripts; cannot publish |
| 85 | Motion Graphics / Animation Artist | 2 | Create animated explainer videos from approved scripts; upload animation exports | Cannot approve own work; cannot publish to YouTube |
| 86 | Graphics Designer — Video | 2 | Thumbnails, lower-thirds, chapter cards, intro/outro motion assets | Cannot upload animation or final edit files |
| 87 | Video Editor | 2 | Assemble final video from animation + VO + graphics; colour grade; export at spec | Cannot upload subtitle files; cannot publish |
| 88 | Subtitle & Localisation Editor | 2 | Add subtitles (EN + HI, TE, UR regional languages); verify timing sync | Cannot approve final video; cannot upload animation or edit assets |
| 89 | Video Quality Reviewer | 2 | Final QA gate — accuracy, A/V quality, subtitle sync, spec compliance; PASS or FAIL | Cannot publish directly; PASS routes to Publish Queue for Producer (82) |

---

## Division F — Exam Day Operations (7 roles)

> Base URL: `/ops/exam/`
> Most critical division on exam day — 74,000 students submit simultaneously.
> This team runs the war room. Every action here is irreversible at scale.

| # | Role | Level | Owns | Critical Action |
|---|---|---|---|---|
| 34 | Exam Operations Manager | 3 | Monitor all live exams, pause/extend duration, war room authority | Pause exam for all tenants |
| 35 | Exam Support Executive | 3 | First-response support for student/institution issues during live exam window | Override stuck/frozen session |
| 36 | Results Coordinator | 3 | Trigger rank computation, review results before publish, answer key management | Approve result publish |
| 37 | Notification Manager | 3 | WhatsApp/SMS/Email templates, result broadcasts, OTP routing, TRAI DLT compliance | Send bulk notification to 74K students |
| 38 | Incident Manager — Exam Day | 4 | Infrastructure escalation to DevOps, war room coordination, emergency scaling decisions | Emergency Lambda scale-up |
| 108 | Exam Configuration Specialist | 3 | Pre-exam setup — timing, question paper assignment, negative marking rules, per-institution configs | Lock exam configuration for launch |
| 109 | Exam Integrity Officer | 3 | Malpractice detection, proctor flag triage, integrity case management, legal escalation | Invalidate exam session (suspected malpractice) |

---

## Division G — Background Verification (4 roles)

> Base URL: `/bgv/`
> POCSO Act 2012 — mandatory BGV for all institution staff with minor access.
> Any unverified staff member found = direct legal liability for EduForge.
> ~28,000 staff across 1,900+ institutions · NCPCR mandatory reporting within 24 hours.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 39 | BGV Manager | 3 | BGV policy, vendor onboarding & config, API key rotation, institution escalation, compliance tracker, POCSO oversight, compliance report export | Cannot process individual verifications (Executive scope) |
| 40 | BGV Executive | 3 | Process assigned BGV requests, document review & upload, vendor submission, result recording, case notes | Cannot approve FLAGGED results; cannot view institution-level compliance; cannot configure vendors |
| 41 | POCSO Compliance Officer | 1 | Read-only audit of BGV coverage across all institutions; NCPCR mandatory annual report generation | All writes blocked — cannot escalate, log communications, or approve any decision |
| 92 | BGV Operations Supervisor | 3 | Approve FLAGGED/INCONCLUSIVE verification decisions, queue assignment across executives, SLA monitoring, bulk vendor submission | Cannot configure vendors or system settings; cannot self-approve own submissions |

---

## Division H — Data & Analytics (5 roles)

> Base URL: `/analytics/`
> All analytics reads from pre-aggregated tables — never live cross-tenant scans.
> Nightly Celery aggregation jobs run across all 2,050 tenant schemas.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 42 | Analytics Manager | 1 | Platform-wide MIS, anomaly alerts, institution churn reporting, report template approval and publish, AI cost oversight | No data edits; cannot trigger pipeline runs or AI batches |
| 43 | Data Engineer | 4 | Analytics schema DDL, Celery aggregation pipeline operations, manual re-runs, data freshness monitoring, SQL explorer, warehouse management | Cannot approve AI MCQs; cannot approve report templates; no business configuration |
| 44 | Data Analyst | 1 | Student performance analysis, institution health investigation, question quality flagging, dropout signal analysis, export requests | No data edits; no pipeline management; no AI pipeline access; cannot send CSM notifications |
| 45 | AI Generation Manager | 3 | AI MCQ batch creation, model config and prompt management, MCQ quality review before Division D, cost tracking | Cannot approve MCQs for publish (Division D Approver only); cannot modify existing question bank; cannot trigger analytics pipelines |
| 46 | Report Designer | 1 | Institution-facing MIS report template design, section configuration, preview and testing, delivery scheduling | No data edits; cannot publish templates (Analytics Manager approval required); cannot trigger manual deliveries |

---

## Division I — Customer Support (7 roles)

> Base URL: `/support/`
> L1 → L2 → L3 escalation with hard SLA enforcement.
> Exam-day peak: ~18,000–25,000 tickets in a 48-hour window.

| # | Role | Level | Handles | SLA |
|---|---|---|---|---|
| 47 | Support Manager | 3 | Team management, SLA config, escalation rules, cross-division coordination, full ticket access | — |
| 48 | L1 Support Executive | 3 | Login, OTP, basic navigation, student and institution admin queries | < 2 hours |
| 49 | L2 Support Engineer | 3 | Bug investigation, log analysis, DB read queries, technical ticket resolution | < 8 hours |
| 50 | L3 Support Engineer | 4 | Code-level fixes, DB writes (under approval), hotfixes, rollbacks | < 24 hours |
| 51 | Onboarding Specialist | 3 | New institution onboarding pipeline, portal setup guidance, admin training coordination | Per onboarding SLA |
| 52 | Training Coordinator | 2 | Create training docs and KB articles (needs approval), conduct training sessions for institution admins | Scheduled |
| 90 | Support Quality Lead | 3 | Random-sample ticket quality audits, CSAT trend monitoring, L1 agent coaching, KB gap identification, weekly quality report | Ongoing |

---

## Division J — Customer Success (6 roles)

> Base URL: `/csm/`
> Portfolio: 2,050 institutions · ₹18Cr–₹90Cr ARR.
> Health scores recomputed nightly from exam frequency, engagement depth, support burden, payment health, and relationship recency.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 53 | Customer Success Manager | 3 | Institution health scores, retention risk management, renewal pipeline, playbook governance, NPS programme, portfolio strategy | Billing config, infra config |
| 54 | Account Manager | 3 | Existing institution relationships, upsell, expansion seats, renewal co-ownership | Cannot send bulk surveys; cannot approve playbook templates |
| 55 | Escalation Manager | 3 | Critical institution complaints, SLA breach handling, cross-division war-room coordination for account-threatening incidents | Cannot approve content; cannot modify billing |
| 56 | Renewal Executive | 1 | Track subscription expiry, send renewal reminders, update renewal stage to COMMITTED | Cannot close/win renewals (AM or CSM must confirm); no data writes outside renewal module |
| 93 | Customer Success Analyst | 1 | Health score model maintenance, churn signal analysis, portfolio cohort analytics, NPS/CSAT data analysis, weekly CS data pack | No customer-facing comms; no playbook execution; no billing access |
| 94 | Implementation Success Manager | 3 | First-90-day post-onboarding success, time-to-value tracking, go-live readiness, first EBR facilitation (handoff from Div I #51) | Billing config; renewal ownership passes to Account Manager at day 90; no L2/L3 queue access |

---

## Division K — Sales & Business Development (10 roles)

> Base URL: `/group1/k/`
> Pipeline: 2,050 institutions across 4 segments.
> Sales cycles: 3–8 weeks (schools/coaching), 8–24 weeks (groups/govt).

| # | Role | Level | Territory / Scope | Can Do | Cannot Do |
|---|---|---|---|---|---|
| 57 | B2B Sales Manager | 3 | All segments — pricing approvals, deal sign-off | Full pipeline visibility; approve pricing exceptions; set quotas; assign territories; all reports | Billing config; infra config |
| 58 | Sales Executive — Schools | 3 | 1,000 schools | Own leads — create, log activities, advance stages, schedule demos | Access other execs' leads; approve pricing; create demo tenants |
| 59 | Sales Executive — Colleges | 3 | 800 intermediate colleges | Same as #58 | Same as #58 |
| 60 | Sales Executive — Coaching | 3 | 100 coaching centres (5K–15K members each) | Same as #58 | Same as #58 |
| 61 | Partnership Manager | 3 | State board govt contracts, coaching chain MoUs | Manage all partnerships; upload MoUs; track renewals; log partner activities | Demo tenant management; channel partner commissions; billing |
| 62 | Demo Manager | 3 | All segments — free trial tenant lifecycle | Create/reset/extend/deactivate demo tenants; link to leads; seed data; generate access links | Edit production tenants; access billing; approve deals |
| 63 | Channel Partner Manager | 1 | Reseller/partner network — commission tracking | View partner performance; log interactions; commission reports | Commission approval (Sales Manager approves); onboard without Manager approval |
| 95 | Sales Operations Analyst | 1 | Platform-wide — CRM data quality, pipeline reporting | Read all pipeline; quota reports; win/loss analysis; territory map; export reports | Any pipeline edits; no customer-facing actions; no territory reassignment |
| 96 | Pre-Sales / Solutions Engineer | 3 | Large deals (>₹2L ARR) and government tenders | Technical discovery; RFP/tender responses; PoC tenant deployment; document feature gaps | Cannot close deals (Sales Exec owns); cannot approve pricing; no commission management |
| 97 | Inside Sales Executive | 3 | Inbound queue — website leads, marketing-sourced, trial activations | Manage inbound leads; qualify and assign; first contact; schedule demos; PROSPECT→CONTACTED | Cannot access outbound pipeline of other execs; no pricing approvals; no demo tenant creation |

---

## Division L — Marketing & Growth (8 roles)

> Base URL: `/marketing/` (internal Marketing Operations portal)
> Roles 64–68 have Level 0 for the EduForge student/institution platform — they operate external tools (Meta Ads, Google Search Console, YouTube Studio).
> All 8 roles access the `/marketing/` portal per their role matrix.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 64 | Marketing Manager | 0 | Brand strategy; approve all content, assets, campaigns; quarterly budget allocation; full portal access | EduForge platform config; billing; infra; sales pipeline edits |
| 65 | SEO / Content Executive | 0 | Blog, landing pages, exam prep articles for organic traffic; keyword tracking; GSC monitoring | Approve own content; approve brand assets; paid ad config |
| 66 | Social Media Manager | 0 | YouTube, Instagram, Twitter — student community; post scheduling; platform analytics | Performance ad budget; content publishing approval; brand asset upload |
| 67 | Performance Marketing Exec | 0 | Google Ads, Meta Ads — institution decision-maker targeting; UTM config; A/B test campaigns | Content approval; brand asset upload; attribution model config |
| 68 | Brand Manager | 0 | Visual identity per domain (SSC brand ≠ School brand); asset upload, versioning, deprecation; brand compliance review | Performance ad management; content authoring; social post scheduling |
| 98 | Marketing Analyst | 1 | Attribution model config (First/Last/Linear); CAC/ROAS/CPL reporting; conversion funnel analytics; channel mix analysis; lead quality scoring; weekly data pack | No campaign edits; no content edits; no asset uploads; no customer-facing comms |
| 99 | Content Strategist | 2 | Editorial calendar CRUD; content brief creation and assignment; keyword cluster strategy; content performance review; co-approve content with Marketing Manager | Performance ad management; brand asset upload; social scheduling; no EduForge platform writes |
| 100 | Email & CRM Marketing Executive | 0 | Drip sequences, email template authoring, contact list management, send scheduling, open/click/bounce analytics, WhatsApp broadcast scripts | Cannot send to >10K contacts without Manager approval; no sales financial data; no platform config |

---

## Division M — Finance & Billing (8 roles)

> Base URL: `/finance/`
> ARR: ₹18Cr–₹90Cr · ~2,050 invoices/month · GST: SAC 9993 (18%) · Payment gateway: Razorpay.
> Overdue rate: 3–5% (~60–100 institutions). GSTR-1 due 11th, GSTR-3B due 20th of following month.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 69 | Finance Manager | 1 | Revenue P&L oversight, Razorpay reconciliation sign-off, investor reporting, refund approvals >₹10K, write-off decisions, AR escalation resolution | Cannot edit invoices directly (Billing Admin scope); cannot configure plan tiers (Pricing Admin scope) |
| 70 | Billing Admin | 3 | Invoice generation, subscription plan assignment, invoice edits, refund request creation, account suspension/reactivation, bulk invoice dispatch | Cannot approve refunds >₹10K (Finance Manager required); cannot configure plan tiers (Pricing Admin scope) |
| 71 | Accounts Receivable Exec | 1 | Outstanding dues tracking, reminder dispatch, promise-to-pay logging, 0–60 day overdue follow-up, AR aging report review | No invoice writes; cannot issue demand notices or suspend accounts; read-only on all financial records |
| 72 | GST / Tax Consultant | 1 | SAC 9993 compliance, CGST/SGST/IGST computation per invoice, GSTR-1/3B/9 filing, TDS 194J tracking, Razorpay TCS reconciliation | Cannot edit invoices or subscriptions; no access to pricing config or refund processing |
| 73 | Refund Processing Exec | 3 | Validate refund eligibility, process approved refunds via Razorpay API, track refund_id and status, handle failed refunds | Cannot approve refunds >₹10K; cannot create refund requests (Billing Admin or Finance Manager creates them) |
| 74 | Pricing Admin | 3 | Subscription tier configuration (create/edit/archive plans), institution-specific discounts, promo code lifecycle, pricing change history | Cannot assign plans to institutions (Billing Admin); cannot approve discounts >20% (Finance Manager must approve) |
| 101 | Finance Analyst | 1 | ARR/MRR waterfall (new/expansion/contraction/churn), P&L variance, investor deck data, cohort revenue analysis, NRR/GRR modelling, revenue forecast, segment-wise attribution | No data edits anywhere; read-only across all finance modules; aggregated analytics export only (not raw records) |
| 102 | Collections Executive | 3 | Outbound dunning calls for 60+ day overdue accounts, demand notice generation and dispatch, payment plan negotiation, suspension coordination with Billing Admin, escalation to Finance Manager for write-off | Cannot write off invoices; cannot approve refunds; no access to subscriptions, pricing config, or GST module |

---

## Division N — Legal & Compliance (6 roles)

> Base URL: `/legal/`
> DPDP Act 2023 — DSR resolution mandatory within **30 days**.
> CERT-In — cyber incident reporting mandatory within **6 hours**.
> POCSO Act 2012 — NCPCR reporting mandatory within **24 hours**.
> TRAI DLT — sender ID EDUFGE must be continuously active; lapse = OTP failure for 7.6M students.
> 2,050 institution contracts (MSA + DPA + SLA each) = ~6,150+ contract records.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 75 | Legal Officer | 1 | Institution contracts (creation, review, termination), ToS & Privacy Policy lifecycle, POCSO legal oversight, DPDP legal opinions, document repository, co-approval of privacy policy publications | No data edits on platform; no billing config; cannot log POCSO incidents (Reporting Officer scope) |
| 76 | Data Privacy Officer (DPO) | 1 | DPDP Act 2023 compliance, DSR resolution (30-day clock), breach coordination (72h DPDP notification), consent coverage oversight, sub-processor register, data flow register, privacy policy co-approval | No data edits; cannot configure system; cannot resolve DSRs without proper assessment; cannot terminate contracts |
| 77 | Regulatory Affairs Exec | 1 | TRAI DLT entity registration & renewal (sender ID EDUFGE), DLT template management, CERT-In filing, MeitY intermediary compliance, state board regulatory filings | No data edits; cannot approve breach reports (DPO/Legal scope); no contract or POCSO module access |
| 78 | POCSO Reporting Officer | 1 | Mandatory POCSO incident intake, NCPCR submission within 24 hours, police FIR coordination, child welfare committee liaison, annual NCPCR compliance report, accused-BGV flag coordination with Division G | Cannot access any non-POCSO modules; cannot log incidents without Legal Officer notification; cannot access victim data without re-authentication |
| 103 | Contract Coordinator | 2 | End-to-end contract workflow: instantiate from approved templates, send for e-signature (DigiSign), follow-up on unsigned contracts, expiry tracking, renewal initiation, contract filing | Cannot create or modify contract templates (Legal Officer owns); cannot sign off on contracts with `requires_legal_review=true`; cannot terminate contracts; no POCSO/DSR/filing access |
| 104 | Data Compliance Analyst | 1 | DSR intake triage (log, assign to DPO), data flow register maintenance, consent coverage reporting, DPDP compliance KPI tracking, weekly compliance data pack, PIA documentation support | Cannot resolve or reject DSRs (DPO only); cannot approve breach notifications; cannot create regulatory filings; no POCSO access; all platform data read-only |

---

## Division O — HR & Administration (6 roles)

> Base URL: `/hr/` (internal HR portal only — zero EduForge platform access for all O roles)
> At Phase 4 scale (100–150 EduForge employees across multiple cities), talent, payroll, compliance, culture, and L&D each require a dedicated owner.

| # | Role | Level | Owns | Cannot Do |
|---|---|---|---|---|
| 79 | HR Manager | 0 | HR strategy & policy, hiring approvals, payroll sign-off, statutory compliance oversight, HR analytics, POSH committee chair, HR vendor management | Cannot process payroll directly (Payroll Executive executes); cannot deploy code or manage infra |
| 80 | Recruiter | 0 | Full-cycle talent acquisition: JD publishing, sourcing, interview coordination, offer rollout, ATS management, campus hiring | Cannot approve offers (HR Manager approves); cannot onboard (Onboarding Specialist scope) |
| 81 | Office Administrator | 0 | Facilities management, office vendor payments, asset register (laptops, furniture, access cards), travel & accommodation bookings, petty cash | Cannot process payroll; no access to HR records or candidate data |
| 105 | Payroll & Compliance Executive | 0 | Monthly payroll processing (earnings, deductions, net pay), PF/ESI/PT challan filing, TDS deposit and quarterly returns, Form 16 generation, salary register, F&F settlement, multi-state labour law compliance | Cannot approve payroll (HR Manager approves before disbursal); cannot create or modify employee records; no performance or L&D data access |
| 106 | HR Business Partner | 0 | OKR framework rollout, performance review cycles (annual, mid-year, probation), PIP initiation and tracking, culture pulse and eNPS surveys, D&I initiatives, exit interview programme, HRBP for technical divisions (C, D, E, F) | Cannot approve payroll; cannot post job openings (Recruiter owns); cannot configure system access (DevOps #14 owns) |
| 107 | L&D Coordinator | 0 | Training needs assessment, training calendar management, LMS administration, external vendor-led training procurement, certification tracking, skills matrix, induction programme, mandatory compliance training (POSH, data privacy, POCSO awareness) | Cannot approve training budget >₹50K (HR Manager approves); cannot create or approve performance reviews; no payroll access |

> Internal IT for EduForge employees (laptops, GitHub access, VPN) is handled by DevOps Engineer (#14) via an IT request workflow coordinated with Office Administrator (#81).

---

## Full Role Count Summary

| Division | Count | Notes |
|---|---|---|
| A — Executive Leadership | 4 | Roles 1–4 |
| B — Product & Design | 5 | Roles 5–9 |
| C — Engineering | 8 | Roles 10–17 |
| D — Content & Academics | 13 | Roles 18–30 |
| E — Video & Learning | 11 | Roles 31–33 (Phase 1) + 82–89 (Phase 2) |
| F — Exam Day Operations | 7 | Roles 34–38 (original) + #108 Config Specialist + #109 Integrity Officer |
| G — Background Verification | 4 | Roles 39–41 + #92 BGV Ops Supervisor |
| H — Data & Analytics | 5 | Roles 42–46 |
| I — Customer Support | 7 | Roles 47–52 + #90 Support Quality Lead |
| J — Customer Success | 6 | Roles 53–56 + #93 CS Analyst + #94 Implementation Success Manager |
| K — Sales & Business Development | 10 | Roles 57–63 + #95 Sales Ops Analyst + #96 Pre-Sales Engineer + #97 Inside Sales Exec |
| L — Marketing & Growth | 8 | Roles 64–68 + #98 Marketing Analyst + #99 Content Strategist + #100 Email & CRM Exec |
| M — Finance & Billing | 8 | Roles 69–74 + #101 Finance Analyst + #102 Collections Executive |
| N — Legal & Compliance | 6 | Roles 75–78 + #103 Contract Coordinator + #104 Data Compliance Analyst |
| O — HR & Administration | 6 | Roles 79–81 + #105 Payroll & Compliance Exec + #106 HR Business Partner + #107 L&D Coordinator |
| **Total** | **108** | |

---

## Headcount by Phase

| Phase | Students on Platform | Approx EduForge Team Size |
|---|---|---|
| Launch (Phase 1) | 0 – 50K | 15–20 people |
| Growth (Phase 2) | 50K – 2L | 30–40 people |
| Scale (Phase 3) | 2L – 10L | 60–80 people |
| Mature (Phase 4) | 10L – 25L | 100–150 people |

---

*Last updated: 2026-03-21 · Total: 108 roles · 15 divisions*
