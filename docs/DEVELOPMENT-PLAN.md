# EduForge — Ultra-Pro Development Plan (From Scratch)

> **Goal:** Build EduForge from spec to production — 5 crore students, ₹0.60/student/year.
> **Documentation:** 1,633 files, 482,950 lines of specs COMPLETE. Zero guesswork.
> **Approach:** Modules first (backend), Groups second (UI). Clean layered architecture.

---

## Architecture Summary

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CLOUDFLARE EDGE (₹0 egress)                      │
│  CDN · R2 Storage · WAF · DDoS · DNS · Workers (edge compute)         │
│  Serves: Questions · Results · Certificates · Notes · Videos · Static  │
│  99% of all reads served here — no Lambda/Fargate touched              │
└──────────────────────────────┬──────────────────────────────────────────┘
                               │ Cache MISS only (~1% of traffic)
                               ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     AWS API GATEWAY (ap-south-1)                        │
│  Rate limiting · JWT validation · Routing · HTTPS termination          │
└───┬──────┬──────┬──────┬──────┬──────┬──────────────────────────────────┘
    │      │      │      │      │      │
    ▼      ▼      ▼      ▼      ▼      ▼
┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
│IDENT.││PORTAL││ EXAM ││NOTIF.││BILL. ││  AI  │
│Fast  ││Django││Fast  ││Fast  ││Fast  ││Fast  │
│API   ││HTMX  ││API   ││API   ││API   ││API   │
│Lambda││Farg. ││Lambda││Lambda││Lambda││Lambda│
└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
   └───────┴───────┴───────┴───────┴───────┘
                       │
           ┌───────────▼───────────┐
           │   PostgreSQL 16 RDS   │
           │  7 schemas, 1 cluster │
           │  + Read replicas      │
           └───────────┬───────────┘
                       │
           ┌───────────▼───────────┐
           │     AWS SQS Queues    │
           │  Async: scoring,      │
           │  notifications, ranks │
           └───────────────────────┘
```

---

## Development Strategy: Modules First, Groups Second

```
WHY THIS ORDER:
  Module = backend (models, APIs, business logic, services)
  Group  = frontend (Django templates, HTMX, portal UI)

  Module 17 (Question Bank) is used by:
    Group 1 (Admin reviews MCQs)
    Group 5 (Coaching creates tests)
    Group 6 (Exam domain serves tests)
    Group 7 (TSP licenses content)
    Group 9 (Partners author questions)
    Group 10 (Students take tests)

  Build the module ONCE → 6 groups consume it via API.
  If you build UI-first, you'd rebuild the question model 6 times.

LAYER DIAGRAM:
  ┌──────────────────────────────────────────────────┐
  │  LAYER 2: GROUPS (Portal UI)                      │
  │  Group 1 → Group 2 → ... → Group 10              │
  │  Django templates + HTMX + partials               │
  │  Each group = one portal with its own views       │
  ├──────────────────────────────────────────────────  │
  │  LAYER 1: MODULES (Backend)                       │
  │  Module 00 → Module 01 → ... → Module 57          │
  │  Models + APIs + Services + Celery tasks          │
  │  Each module = one domain with its own endpoints  │
  ├──────────────────────────────────────────────────  │
  │  LAYER 0: FOUNDATION                              │
  │  PostgreSQL schemas + Docker + CI/CD + Auth       │
  │  The floor everything stands on                   │
  └──────────────────────────────────────────────────┘
```

---

## LAYER 0 — Foundation (Week 1–2)

> Before any module, the foundation must exist: database, auth, multi-tenancy, Docker.

### Week 1: Project Bootstrap

| # | Task | Spec | Service |
|---|---|---|---|
| 1 | PostgreSQL 16 — create 7 schemas | `database.md` | — |
| 2 | Docker Compose (PG + Django + FastAPI + pgAdmin) | `deployment.md` | — |
| 3 | Django project restructure (apps: core, auth) | `00-project-setup` | portal |
| 4 | FastAPI identity service scaffold | `01-auth` | identity |
| 5 | Environment config (.env, secrets) | `deployment.md` | — |
| 6 | CI/CD pipeline (GitHub Actions — lint, test) | `deployment.md` | — |

### Week 2: Auth & Multi-Tenancy

| # | Task | Spec | Service |
|---|---|---|---|
| 7 | OTP send/verify endpoints | `01-auth` | identity |
| 8 | JWT create/verify/refresh | `01-auth` | identity |
| 9 | Multi-tenant middleware (domain → tenant_id) | `02-multi-tenancy` | portal |
| 10 | Institution model + RBAC | `03-roles-permissions` | identity |
| 11 | User-institution-role linking (N:N:N) | `03-roles-permissions` | identity |
| 12 | Role-based home routing | `homes/home-routing.md` | portal |

**Deliverable:** OTP login → JWT → role detection → correct home page.

---

## LAYER 1 — Modules (Weeks 3–20)

> Build ALL 58 backend modules. Each module = models + API endpoints + services + Celery tasks.
> No UI. Pure backend. Every module gets tested independently via API docs (FastAPI /docs).

### Module Build Order — Grouped by Dependency

The 58 modules are organized into **8 dependency tiers**. Modules in the same tier can be built in parallel.

```
TIER 1: Core Identity & Setup (Modules 00–06)
  └→ TIER 2: People (Modules 07–09)
       └→ TIER 3: Daily Operations (Modules 10–16)
            └→ TIER 4: Exam Engine (Modules 17–23)
            └→ TIER 5: Finance (Modules 24–27)
            └→ TIER 6: Communication (Modules 34–40)
       └→ TIER 7: AI & Advanced (Modules 44–52)
  └→ TIER 8: Platform & Compliance (Modules 41–43, 53–57)
```

---

### TIER 1 — Core Identity & Setup (Weeks 3–4)

> Foundation models that every other module depends on.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 3 | 00 — Project Setup | `00-project-setup.md` | all | Base config, AWS, CDN |
| 3 | 01 — Auth & Identity | `01-auth.md` | identity | users, otps, sessions |
| 3 | 02 — Multi-Tenancy | `02-multi-tenancy.md` | identity | tenant config, schemas |
| 3 | 03 — Roles & Permissions | `03-roles-permissions.md` | identity | user_roles, permissions |
| 4 | 04 — Institution Onboarding | `04-institution-onboarding.md` | portal | institutions, branding |
| 4 | 05 — Academic Year & Calendar | `05-academic-year-calendar.md` | portal | academic_years, terms, holidays |
| 4 | 06 — Branch & Campus | `06-branch-campus-management.md` | portal | branches, campuses |

**API count: ~35 endpoints | Models: ~15 tables**

---

### TIER 2 — People (Weeks 5–6)

> Students, staff, parents — the humans in the system.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 5 | 07 — Student Enrolment & Profile | `07-student-enrolment-profile.md` | portal | students, enrollments, access_levels |
| 5 | 08 — Staff Management & BGV | `08-staff-management-bgv.md` | portal | staff, designations, bgv_records |
| 6 | 09 — Parent & Guardian | `09-parent-guardian-management.md` | portal | parents, child_links, consent |

**API count: ~40 endpoints | Models: ~12 tables**

---

### TIER 3 — Daily Operations (Weeks 7–9)

> What institutions do every day — attendance, timetable, homework, notes.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 7 | 10 — Timetable & Scheduling | `10-timetable-scheduling.md` | portal | timetables, slots, room_alloc |
| 7 | 11 — Attendance (School/College) | `11-attendance-school-college.md` | portal | attendance, periods |
| 7 | 12 — Attendance (Coaching/Batch) | `12-attendance-coaching-batch.md` | portal | batch_attendance |
| 8 | 13 — Attendance (Hostel) | `13-attendance-hostel.md` | portal | hostel_attendance, roll_calls |
| 8 | 14 — Homework & Assignments | `14-homework-assignments.md` | portal | assignments, submissions |
| 8 | 15 — Syllabus & Curriculum | `15-syllabus-curriculum-builder.md` | portal | syllabi, topics, coverage |
| 9 | 16 — Notes & Study Material | `16-notes-study-material.md` | portal | notes, categories, downloads |

**API count: ~55 endpoints | Models: ~20 tables**

---

### TIER 4 — Exam Engine (Weeks 10–13)

> The core product — mock tests, question bank, results, rankings. Most complex tier.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 10 | 17 — Question Bank & MCQ | `17-question-bank-mcq.md` | exam | questions, tags, quality_scores |
| 10 | 18 — Exam Paper Builder | `18-exam-paper-builder.md` | exam | papers, blueprints, sections |
| 11 | 19 — Exam Session & Proctoring | `19-exam-session-proctoring.md` | exam | sessions, proctoring_events |
| 11 | 20 — Submission & Auto-Grading | `20-exam-submission-auto-grading.md` | exam | attempts, answers, scoring |
| 12 | 21 — Results & Report Cards | `21-results-report-cards.md` | exam | results, rank_cards, reports |
| 12 | 22 — Test Series & Mock Tests | `22-test-series-mock-tests.md` | exam | test_series, schedules |
| 13 | 23 — Leaderboard & Rankings | `23-leaderboard-rankings.md` | exam | leaderboards, ranks, badges |

**API count: ~70 endpoints | Models: ~25 tables**

```
EXAM ENGINE ARCHITECTURE (IndexedDB — 2 Lambda calls per exam):

  START: POST /exam/session/start  ←  1 Lambda call
    ↓
  DOWNLOAD: Browser fetches from Cloudflare R2  ←  ₹0
    ↓
  DECRYPT: AES-256-GCM via Web Crypto API  ←  client-side
    ↓
  EXAM: All answers in IndexedDB  ←  0 server calls
    ↓
  SUBMIT: POST /exam/session/{id}/submit  ←  1 Lambda call
    ↓
  SCORE: SQS → async worker  ←  background
    ↓
  RESULTS: Served from CDN  ←  ₹0
```

---

### TIER 5 — Finance (Weeks 14–15)

> Fees, payments, payroll — money flows.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 14 | 24 — Fee Structure Management | `24-fee-structure-management.md` | billing | fee_structures, fee_heads |
| 14 | 25 — Fee Collection & Receipts | `25-fee-collection-receipts.md` | billing | payments, receipts |
| 14 | 26 — Fee Defaulters & Recovery | `26-fee-defaulters-recovery.md` | billing | defaulters, reminders |
| 15 | 27 — Staff Payroll & Salary | `27-staff-payroll-salary.md` | billing | payroll, salary_slips |
| 15 | 56 — Platform Billing & GST | `56-platform-billing-gst-invoicing.md` | billing | invoices, gst_filings |
| 15 | 57 — Payment Gateway (BYOG) | `57-payment-gateway-byog.md` | billing | razorpay_orders, refunds |

**API count: ~50 endpoints | Models: ~18 tables**

---

### TIER 6 — Communication (Weeks 16–17)

> Notifications across 4 channels + announcements + documents.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 16 | 34 — Announcements & Circulars | `34-announcements-circulars.md` | notification | announcements |
| 16 | 35 — Notifications (In-app + FCM) | `35-notifications-inapp-fcm.md` | notification | notifications, preferences |
| 16 | 36 — WhatsApp Add-on | `36-whatsapp-addon.md` | notification | wa_messages, wa_templates |
| 17 | 37 — Email (AWS SES) | `37-email-aws-ses.md` | notification | email_logs, templates |
| 17 | 38 — SMS & OTP | `38-sms-otp.md` | notification | sms_logs |
| 17 | 39 — Certificates & TC | `39-certificates-tc.md` | portal | certificates, verification |
| 17 | 40 — Document Management | `40-document-management.md` | portal | documents, categories |

**API count: ~45 endpoints | Models: ~15 tables**

---

### TIER 7 — AI & Advanced (Weeks 18–19)

> AI services, video learning, live classes, subscriptions, B2B marketplace.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 18 | 44 — Video Learning & Streaming | `44-video-learning-streaming.md` | portal | videos, playlists, progress |
| 18 | 45 — Live Classes | `45-live-classes.md` | portal | live_sessions, recordings |
| 18 | 46 — AI Doubt Solver | `46-ai-doubt-solver.md` | ai | doubts, answers, expert_routing |
| 18 | 47 — AI Performance Analytics | `47-ai-performance-analytics.md` | ai | weak_topics, projections |
| 19 | 48 — AI Content Generation | `48-ai-content-generation.md` | ai | generated_mcqs, review_queue |
| 19 | 49 — National Exam Catalog | `49-national-exam-catalog.md` | exam | exam_domains, exam_configs |
| 19 | 50 — Subscription & Access Control | `50-subscription-access-control.md` | billing | subscriptions, plans, trials |
| 19 | 51 — B2B API & Partner Portal | `51-b2b-api-partner-portal.md` | portal | partners, content_agreements |
| 19 | 52 — White-label TSP | `52-white-label-tsp-portal.md` | portal | tsp_configs, branding |

**API count: ~65 endpoints | Models: ~22 tables**

---

### TIER 8 — Platform & Compliance (Week 20)

> Remaining institution modules + platform management + compliance.

| Week | Module | Spec File | Service | Models |
|---|---|---|---|---|
| 20 | 28 — Hostel Management | `28-hostel-management.md` | portal | hostels, rooms, mess |
| 20 | 29 — Transport & GPS | `29-transport-gps-tracking.md` | portal | routes, vehicles, gps_logs |
| 20 | 30 — Library Management | `30-library-management.md` | portal | books, issues, fines |
| 20 | 31 — Admission & Enquiry CRM | `31-admission-enquiry-crm.md` | portal | enquiries, follow_ups |
| 20 | 32 — Counselling & Welfare | `32-counselling-student-welfare.md` | portal | welfare_events |
| 20 | 33 — PTM | `33-ptm-parent-teacher-meeting.md` | portal | ptm_slots, feedback |
| 20 | 41 — POCSO Compliance | `41-pocso-compliance.md` | portal | bgv_records, incidents |
| 20 | 42 — DPDPA & Audit Log | `42-dpdpa-audit-log.md` | portal | consent_log, audit_trail |
| 20 | 43 — Legal & Data Compliance | `43-legal-data-compliance.md` | portal | compliance_records |
| 20 | 53 — Platform Analytics | `53-platform-analytics-reports.md` | analytics | reports, dashboards |
| 20 | 54 — Feature Flags | `54-platform-settings-feature-flags.md` | portal | feature_flags, settings |
| 20 | 55 — Incident Management | `55-incident-management-sla.md` | portal | incidents, sla_tracking |

**API count: ~80 endpoints | Models: ~30 tables**

---

### LAYER 1 Summary

| Tier | Weeks | Modules | Endpoints | Tables |
|---|---|---|---|---|
| 0 (Foundation) | 1–2 | Setup + Auth | ~20 | ~8 |
| 1 (Core Identity) | 3–4 | 00–06 | ~35 | ~15 |
| 2 (People) | 5–6 | 07–09 | ~40 | ~12 |
| 3 (Daily Ops) | 7–9 | 10–16 | ~55 | ~20 |
| 4 (Exam Engine) | 10–13 | 17–23 | ~70 | ~25 |
| 5 (Finance) | 14–15 | 24–27, 56–57 | ~50 | ~18 |
| 6 (Communication) | 16–17 | 34–40 | ~45 | ~15 |
| 7 (AI & Advanced) | 18–19 | 44–52 | ~65 | ~22 |
| 8 (Platform) | 20 | 28–33, 41–43, 53–55 | ~80 | ~30 |
| **TOTAL** | **20 weeks** | **58 modules** | **~460 endpoints** | **~165 tables** |

After Week 20: **Every API endpoint works. Zero UI. Full test coverage. FastAPI /docs for every service.**

---

## LAYER 2 — Groups / Portal UI (Weeks 21–32)

> Now build the UI on top of the module APIs. Each group = Django views + HTMX templates.
> The backend is DONE. This layer is pure Django CBV + templates + HTMX partials.

### Group Build Order — By Importance

```
GROUP 1 (Platform Admin)  — Build first: you need admin tools to manage everything
  ↓
GROUP 3 (School)          — Highest institution count, validates daily ops modules
GROUP 4 (College)         — Similar to school, extends with placements/NAAC
GROUP 5 (Coaching)        — Batch model, test series focus
  ↓
GROUP 2 (Institution Group) — Chain management across Groups 3/4/5
  ↓
GROUP 6 (Exam Domain)     — SSC/Banking/Railways — consumer-facing
GROUP 10 (Student)        — 5cr students, unified portal — biggest scale
GROUP 8 (Parent)          — Read-only view of student data
  ↓
GROUP 9 (B2B Partner)     — Content marketplace
GROUP 7 (TSP White-label) — Advanced, depends on all other groups
```

---

### Weeks 21–23: Group 1 — Platform Admin Portal

| Week | Division | Pages | What It Covers |
|---|---|---|---|
| 21 | div-a Executive | 5 pages | CEO/CTO/COO/CFO dashboards |
| 21 | div-b Product & Design | 4 pages | Feature flags, release management |
| 21 | div-c Engineering | 18 pages | Tenant manager, deployments, DB admin |
| 22 | div-d Content & Academics | 13 pages | MCQ bank, notes, video curation |
| 22 | div-e Video & Learning | 3 pages | Video curator, playlist manager |
| 22 | div-f Exam Operations | 5 pages | Live exam monitoring, war room |
| 22 | div-g BGV | 3 pages | Background verification |
| 23 | div-h Data & Analytics | 5 pages | Platform MIS, data pipelines |
| 23 | div-i Customer Support | 6 pages | L1/L2/L3 support, tickets |
| 23 | div-j Customer Success | 4 pages | CSM, account health |
| 23 | div-k Sales & BD | 7 pages | Lead pipeline, institution onboarding |
| 23 | div-l Marketing | 5 pages | SEO, social, campaigns |
| 23 | div-m Finance & Billing | 6 pages | Revenue, GST, Razorpay settlements |
| 23 | div-n Legal & Compliance | 7 pages | DPDP, POCSO, regulatory |
| 23 | div-o HR & Admin | 5 pages | Internal staff management |

**Total: 245 page specs → ~100 Django views → ~300 HTMX partials**

---

### Weeks 24–26: Groups 3, 4, 5 — Institution Portals

| Week | Group | Pages | Focus |
|---|---|---|---|
| 24 | Group 3 — School | 260 pages | Attendance, marks, timetable, fees, parents |
| 25 | Group 4 — College | 95 pages | Semester, NAAC, placements, affiliations |
| 26 | Group 5 — Coaching | 131 pages | Batches, test series, performance, schedule |

---

### Week 27: Group 2 — Institution Group (Chain Admin)

| Week | Group | Pages | Focus |
|---|---|---|---|
| 27 | Group 2 — Institution Group | 625 pages | Multi-branch oversight, consolidated reports, group-level config |

---

### Weeks 28–30: Groups 6, 10, 8 — Consumer-Facing

| Week | Group | Pages | Focus |
|---|---|---|---|
| 28 | Group 6 — Exam Domain | 49 pages | SSC/Banking/Railways portal, test catalogue, domain config |
| 29 | Group 10 — Student | 30 pages | Unified dashboard, performance, tests, learning, fees |
| 30 | Group 8 — Parent | 28 pages | Child monitoring, fee payment, communication |

---

### Weeks 31–32: Groups 9, 7 — Marketplace

| Week | Group | Pages | Focus |
|---|---|---|---|
| 31 | Group 9 — B2B Content Partner | 27 pages | Question authoring, revenue, quality scoring |
| 32 | Group 7 — TSP White-label | 29 pages | Branded test platforms, content licensing |

---

### LAYER 2 Summary

| Weeks | Groups | Total Pages | Django Views | Templates |
|---|---|---|---|---|
| 21–23 | Group 1 (Admin) | 245 | ~100 | ~300 |
| 24–26 | Groups 3, 4, 5 (Institutions) | 486 | ~200 | ~500 |
| 27 | Group 2 (Chain Admin) | 625 | ~250 | ~600 |
| 28–30 | Groups 6, 10, 8 (Consumer) | 107 | ~50 | ~120 |
| 31–32 | Groups 9, 7 (Marketplace) | 56 | ~25 | ~60 |
| **TOTAL** | **10 groups** | **~1,519 pages** | **~625 views** | **~1,580 partials** |

---

## LAYER 3 — Scale, Mobile & Launch (Weeks 33–38)

### Weeks 33–34: Production Infrastructure

| Task | Details |
|---|---|
| Cloudflare R2 + CDN | Questions, results, certificates, notes → R2. Edge caching rules. |
| AWS production setup | RDS Multi-AZ, Lambda SAM deploy, ECS Fargate (2× tasks), SQS queues |
| Load testing | Locust — 74,000 concurrent exam submissions |
| Database optimization | Index tuning, PgBouncer, read replicas |
| Monitoring | Sentry + CloudWatch + Cloudflare Analytics + custom dashboards |

### Weeks 35–36: Flutter Mobile App

| Task | Details |
|---|---|
| Flutter project | iOS + Android, dark theme matching web |
| Auth + home | OTP login, biometric, JWT in Hive AES-256 |
| Student features | Dashboard, tests (offline-capable), notes, videos |
| Push notifications | FCM, notification preferences |
| App Store / Play Store | Submission, review, launch |

### Weeks 37–38: Security, Compliance & Launch

| Task | Details |
|---|---|
| Security audit | OWASP Top 10, IDOR prevention, penetration testing |
| DPDP Act compliance | Consent flows, data deletion pipeline, DPO setup |
| POCSO compliance | BGV audit, mandatory reporting verification |
| CERT-In readiness | 6-hour breach reporting, incident response plan |
| Soft launch | 10 pilot institutions → feedback → iterate → full launch |

---

## Complete Timeline

```
WEEK  1–2:  LAYER 0  Foundation (Auth, Multi-tenancy, Docker)
WEEK  3–20: LAYER 1  All 58 Modules (Backend — models, APIs, services)
WEEK 21–32: LAYER 2  All 10 Groups (UI — Django views, HTMX templates)
WEEK 33–38: LAYER 3  Scale + Mobile + Launch

              LAYER 0    LAYER 1 (Modules)        LAYER 2 (Groups)    LAYER 3
              ├──┤├──────────────────────┤├────────────────────────┤├────────┤
Week:         1  2  3  4  5 ... 15 ... 20  21 22 23 ... 28 ... 32  33 ... 38
              ▲                          ▲                        ▲          ▲
              │                          │                        │          │
           Login works           All APIs done            All UI done    LAUNCH
           OTP → JWT             460 endpoints            1,519 pages   5cr ready
```

---

## Infrastructure Cost Projections

| Phase | Students | Database | Compute | Cloudflare | Total/Month |
|---|---|---|---|---|---|
| Dev (Weeks 1–20) | 0–1K | db.t4g.micro (₹2,500) | 1× Fargate (₹3,000) | Free | ~₹8,000 |
| Beta (Weeks 21–32) | 1K–50K | db.t4g.medium (₹4,500) | 2× Fargate + Lambda | Pro (₹1,500) | ~₹25,000 |
| Launch (Weeks 33–38) | 50K–2L | db.t4g.large + replica | 4× Fargate + Lambda | Pro | ~₹55,000 |
| Scale | 2L–10L | db.r6g.large + 2 replicas | 8× Fargate | Business | ~₹1,50,000 |
| 5 Crore | 10L–5cr | Aurora Serverless v2 | Auto-scale | Enterprise | ~₹3,00,000+ |

**At 5cr: ₹3,00,000/month ÷ 5,00,00,000 = ₹0.72/student/year** ✅

---

## Key Architectural Decisions (Non-Negotiable)

| # | Decision | Reason |
|---|---|---|
| 1 | **Modules first, Groups second** | Backend is stable, UI changes often. Build once, consume everywhere. |
| 2 | **No Redis** | PostgreSQL + Cloudflare handles everything. Saves ₹16,800/year + ops. |
| 3 | **IndexedDB exam engine** | 2 Lambda calls/exam vs 200. At 74K concurrent = ₹300/day vs ₹30,000/day. |
| 4 | **Cloudflare R2 over S3** | Zero egress. S3 at 5cr students = ₹56L/year egress alone. |
| 5 | **Django HTMX over React** | Zero JS bundle. Faster on ₹8K phones than React hydration. |
| 6 | **Schema-per-service** | 1 PostgreSQL cluster, 7 schemas. Cross-schema JOINs for analytics. |
| 7 | **Stateless JWT** | No network call to validate. Saves 1 round-trip per Lambda invocation. |
| 8 | **SQS for async** | Scoring, notifications, ranks — zero ops, pay per message. |

---

## Testing Strategy

| Level | Tool | Target | When |
|---|---|---|---|
| Unit | pytest | 80%+ coverage per module | Every commit |
| Integration | pytest + httpx | API contract testing | Every PR |
| E2E | Playwright | Critical user journeys (10 groups) | Nightly |
| Load | Locust | 74,000 concurrent exam sessions | Week 33 |
| Security | OWASP ZAP | Top 10 vulnerabilities | Week 37 |

---

## Git Strategy

```
main                         ← production (always deployable)
├── develop                  ← integration
│   ├── feature/module-01-auth
│   ├── feature/module-17-question-bank
│   ├── feature/module-22-test-series
│   ├── feature/group-1-admin-portal
│   ├── feature/group-10-student-portal
│   └── ...
├── staging                  ← pre-prod testing
└── hotfix/*                 ← emergency fixes
```

Module branches: `feature/module-{nn}-{name}`
Group branches: `feature/group-{n}-{name}`

---

*Last updated: 2026-04-01 · EduForge Development Plan v2.0 — Modules First, Groups Second*
