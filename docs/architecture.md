# EduForge — System Architecture

## Platform Overview

| Property | Value |
|---|---|
| Type | Multi-tenant SaaS |
| Market | India (EdTech) |
| Portals | School · College · Coaching · SSC · RRB · State Boards |
| Peak Load | 74,000 concurrent exam submissions |
| Scale Target | 25,00,000 students |
| Cost Target | Rs. 0.60/student/year at scale |

---

## Multi-Domain Architecture

```
eduforge.in                          → Platform homepage / B2B landing

# Institution Portals
{school}.schools.eduforge.in         → Each school's own portal
{college}.colleges.eduforge.in       → Each college's own portal
{group}.group.eduforge.in            → Institution group dashboard
{coaching}.coaching.eduforge.in      → Coaching centre portal

# Exam Domains (separate branding per board)
ssc.eduforge.in                      → SSC CGL, CHSL, MTS, CPO
rrb.eduforge.in                      → RRB NTPC, Group D, JE, ALP
ap.eduforge.in                       → AP State Board (Inter, SSC)
ts.eduforge.in                       → Telangana State Board
upsc.eduforge.in                     → UPSC CSE, CAPF
banking.eduforge.in                  → IBPS, SBI, RBI
```

---

## Services

| Service | Port | Runtime | Responsibility |
|---|---|---|---|
| identity | 8001 | AWS Lambda | Auth, JWT, OTP, Users, Institutions |
| portal | 8002 | ECS Fargate | School/College/Coaching portals, Attendance, Fees |
| exam | 8003 | AWS Lambda | Mock tests, MCQ engine, submissions, ranks |
| notification | 8004 | AWS Lambda | WhatsApp, SMS, Email, Push |
| billing | 8005 | AWS Lambda | Subscriptions, Razorpay, GST, refunds |
| ai | 8006 | AWS Lambda | MCQ generation, doubt solving, study plans |
| analytics | 8007 | AWS Lambda | Reports, MIS, dashboards |

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────┐
│                  CLOUDFLARE EDGE                          │
│   CDN · R2 Storage · WAF · DDoS Protection · DNS         │
│   Serves: Questions · Results · Certificates · Notes     │
│   Cost per request: Rs.0  ← serves 99% of all reads     │
└─────────────────────────┬────────────────────────────────┘
                          │ Cache MISS only
                          ▼
┌──────────────────────────────────────────────────────────┐
│                  AWS API GATEWAY                          │
│          Rate limiting · Routing · HTTPS                 │
└───┬──────┬──────┬──────┬──────┬──────┬───────────────────┘
    │      │      │      │      │      │
    ▼      ▼      ▼      ▼      ▼      ▼
IDENTITY PORTAL  EXAM  NOTIF BILLING  AI
FastAPI  Django FastAPI FastAPI FastAPI FastAPI
Lambda  Fargate Lambda Lambda Lambda  Lambda
    │      │      │      │      │      │
    └──────┴──────┴──────┴──────┴──────┘
                      │
          ┌───────────▼───────────┐
          │    PostgreSQL RDS     │
          │  One cluster, 7       │
          │  schemas              │
          └───────────────────────┘
                      │
          ┌───────────▼───────────┐
          │       AWS SQS         │
          │  Async between        │
          │  services (no Redis)  │
          └───────────────────────┘
```

---

## Exam Engine — IndexedDB Architecture

```
STEP 1 — Session Start (1 Lambda call)
  POST /api/v1/exam/session/start
  Returns: {session_id, r2_url, salt, duration_seconds}

STEP 2 — Download Questions (0 Lambda calls)
  Browser fetches from Cloudflare CDN — Rs.0, <100ms

STEP 3 — Encrypt + Store (0 server calls)
  Key = HKDF(JWT + salt + test_id)  — never sent to server
  Encrypt with AES-256-GCM via Web Crypto API
  Store in IndexedDB

STEP 4 — Exam in Progress (0 server calls)
  All state in IndexedDB: answers, flags, timer, progress
  Auto-backup every 30 seconds

STEP 5 — Submit (1 Lambda call)
  POST /api/v1/exam/session/{id}/submit
  Score computed async via SQS worker

STEP 6 — Results served from CDN — Rs.0

Total Lambda calls for 100-question exam: 2
```

---

## Key Architecture Decisions

| Decision | Reason | Saving |
|---|---|---|
| Cloudflare R2 over AWS S3 | Zero egress cost | Rs. 56+ lakh/year at 1L users |
| No Redis | PostgreSQL handles OTP + rate limits | Rs. 16,800/year |
| Stateless JWT | No network call to validate token | 1 Lambda call saved per request |
| IndexedDB exam engine | 98% fewer Lambda calls during exam | Major cost reduction |
| ECS Fargate for portal only | HTMX needs always-on container | Only portal needs it |
| SQS for async writes | Batch 100 writes into 1 DB call | Reduces DB load at peak |
