# EduForge — Module 02: Multi-Tenancy

> Every institution on EduForge is fully independent in look and feel —
> own homepage, own branding, own layout — but runs on the same platform underneath.
> Think Shopify: every store looks different, same engine powers all.

---

## What is a Tenant?

A tenant is one institution or one institution group registered on EduForge.

| Tenant Type | Example |
|---|---|
| Single branch school | DPS Delhi — one campus |
| Single branch college | ABC Engineering College |
| Single branch coaching | Resonance Kota |
| Institution group | DPS Group — 12 campuses under one account |
| College group | Manipal Group — multiple colleges |

---

## What Each Tenant Gets

| Item | Example |
|---|---|
| Own subdomain | `dps-delhi.eduforge.in` |
| Own custom domain (paid) | `portal.dpsedu.in` |
| Own homepage layout | their sections, their order, their content |
| Own login page | "Welcome to DPS Delhi" — not EduForge branding |
| Own logo, colors, font | full branding control |
| Own navigation menu | school shows hostel, coaching shows batches |
| Own announcement board | their notices only, never another institution's |
| Own enabled modules | hostel on/off, transport on/off, per agreement |
| Own academic calendar | their holidays, their year start month |

---

## Tenant Size Tiers — Shard Assignment

| Tier | Students | Shard Type |
|---|---|---|
| Small | < 500 | Shared shard — many tenants together |
| Medium | 500 – 50,000 | Shared shard — few tenants |
| Large | 50,000 – 3,00,000 | Dedicated shard — one tenant only |
| Enterprise | 3,00,000+ | Multiple dedicated shards |

- System assigns shard **automatically** when tenant is created
- New tenant lands on the least-full available shard
- When tenant crosses a tier threshold → system **auto-migrates** to next tier
- No manual step — fully automatic promotion

---

## Central Tenant Registry

Every request on EduForge (student login, teacher attendance, super-admin view) first checks the central tenant registry to find which shard holds that tenant's data.

| tenant_id | tenant_slug | shard_id | db_host | status |
|---|---|---|---|---|
| uuid-001 | dps-delhi | shard-3 | db3.eduforge.internal | active |
| uuid-002 | abc-coaching | shard-3 | db3.eduforge.internal | active |
| uuid-003 | xyz-college | shard-12 | db12.eduforge.internal | suspended |

- Stored in a central DB (not on any shard)
- Cached in memory on every server — refreshed every 15 minutes
- Single lookup → goes directly to correct shard — never scans all shards

---

## Subdomain & Custom Domain Routing

```
Request arrives → dps-delhi.eduforge.in
       │
       ▼
Cloudflare DNS resolves → EduForge server
       │
       ▼
FastAPI middleware reads host header → extracts "dps-delhi"
       │
       ▼
Looks up central tenant registry → finds shard-3
       │
       ▼
All queries go to shard-3 only
```

### Custom Domain

- Institution adds a CNAME record pointing to EduForge
- Cloudflare auto-provisions SSL certificate — free, automatic
- Available on paid plans only

### Suspended Tenant Domain

- Subdomain stays live but shows a "This institution's account is suspended" page
- No login, no data access

---

## Tenant Feature Flags

- All module flags (hostel, transport, library, etc.) are controlled by **EduForge only**
- Based on the agreement signed with the institution
- Tenant admin cannot enable or disable modules
- New platform features in pilot → EduForge enables per selected tenant only

| Module | Who Controls |
|---|---|
| Hostel management | EduForge (plan-based) |
| Transport tracking | EduForge (plan-based) |
| Library management | EduForge (plan-based) |
| WhatsApp add-on | EduForge (paid add-on) |
| Pilot / beta features | EduForge only |
| Branding (logo, colors) | Tenant admin |
| Academic year config | Tenant admin |
| Staff & student data | Tenant admin |

---

## Tenant Plans & Quotas

- Pricing is per agreement between EduForge and each institution
- Based on number of students per year
- Larger institutions pay less per student (negotiated rate)

| Plan | Max Students | Max Staff | Storage |
|---|---|---|---|
| Starter | 500 | 50 | 5 GB |
| Growth | 5,000 | 500 | 50 GB |
| Scale | 50,000 | 5,000 | 500 GB |
| Enterprise | Unlimited | Unlimited | Custom |

### Limit Behaviour

| Stage | Trigger | Action |
|---|---|---|
| Soft limit (90%) | Nearing student limit | Warning banner shown to institution admin |
| Hard limit reached | Student limit crossed | Plan **auto-upgrades** to next tier |
| Storage soft limit | 80% storage used | Warning to admin |
| Storage hard limit | 100% storage | File uploads blocked — admin notified |

---

## Cross-Tenant Rules

- A student can be enrolled in School A (one tenant) AND Coaching B (different tenant) — allowed
- Parent sees children **per institution only** — no cross-institution unified view
- If two children are in the same institution → parent sees both in one app
- No cross-tenant data sharing at any level

---

## Super-Admin Access

EduForge super-admin has two modes:

### Mode 1 — Platform Analytics (Real-Time)

- Every write event (enrolment, fee, exam) publishes to SQS
- Central Platform Analytics DB consumes events and updates counters in real-time
- Super-admin sees: total students, revenue, enrollments across all tenants — instant
- Never queries shards directly for analytics

### Mode 2 — Drill-Down (Raw Tenant Data)

- Super-admin searches for a specific tenant or student
- System looks up tenant registry → finds correct shard
- Queries that shard directly → returns raw records
- PostgreSQL RLS bypassed for EduForge super-admin role only

---

## Row-Level Security (RLS)

- PostgreSQL RLS enforced on all tenant tables
- Every query is automatically restricted to the current tenant's data at DB level
- Even if a developer forgets `WHERE tenant_id = :tid` — DB blocks cross-tenant access
- EduForge super-admin role bypasses RLS — can see all tenants

---

## Shard Migration — Zero Downtime

Triggered automatically when shard reaches 80% capacity or tenant crosses tier threshold.

```
Step 1 — Copy data
  Tenant data copied from old shard to new shard in background
  Old shard still fully live — users feel nothing

Step 2 — Dual write
  New writes go to both old and new shard simultaneously
  No data loss risk

Step 3 — Verify sync
  System confirms new shard matches old shard exactly

Step 4 — Switch registry
  Central tenant registry updated → new shard becomes active
  Takes milliseconds

Step 5 — Clean up
  Old shard data for this tenant deleted after 24-hour grace period
```

- Migration runs during **night low-traffic window** only
- No exam sessions run at night — no conflicts
- Users experience zero downtime, no logout

---

## Tenant Onboarding — Step by Step

EduForge team creates all tenants — no self-signup.

```
Step 1 — EduForge creates tenant record
  Name, type (school / college / coaching / group), subdomain

Step 2 — Auto-provisioning (under 5 minutes)
  ├── Assign shard (least-full available)
  ├── Create DB schema on assigned shard
  ├── Create CDN namespace on Cloudflare R2
  ├── Provision subdomain xyz.eduforge.in
  └── Create default config (placeholder logo, default colors)

Step 3 — EduForge configures tenant
  ├── Upload institution logo
  ├── Set brand colors
  ├── Enable agreed modules (hostel, transport, etc.)
  └── Set plan and student quota

Step 4 — EduForge creates first admin user
  Institution admin receives login credentials via email

Step 5 — Institution admin logs in
  ├── Completes branding (homepage layout, announcements)
  ├── Sets academic year and holidays
  ├── Adds staff and students
  └── Goes live
```

---

## Tenant Lifecycle — States

| State | Trigger | Access |
|---|---|---|
| Provisioning | Tenant just created | No access yet — setup in progress |
| Active | Setup complete, payment current | Full access — all users |
| Warning | Payment 7 days overdue | Full access + warning banner to admin |
| Suspended | Payment 30 days overdue | Institution admin login only — read-only |
| Terminated | Institution requests exit | All access blocked |
| Archived | Post-termination | No access — data in cold storage |

### Suspension Details

- Students, parents, teachers → fully blocked
- Institution admin → can login, read-only view only
- No new data can be entered (no attendance, no fees, no exams)
- Subdomain shows suspended page to blocked users

### Termination & Data Retention

| What Tenant Is Told | Internal EduForge Policy |
|---|---|
| Data kept for 1 month | Data moved to cold archive DB |
| After 1 month — deleted | Retained internally for up to 2 years |
| No data export provided | EduForge team handles archive — for legal/audit |

---

## DB Schema — Tenant Tables (Central DB)

> All tenant metadata lives in the central DB, not on shards.

**platform.tenants**

| Column | Type | Notes |
|---|---|---|
| id | UUID | Primary key |
| name | TEXT | "DPS Delhi" |
| slug | TEXT | "dps-delhi" — used in subdomain |
| type | TEXT | school / college / coaching / group |
| shard_id | TEXT | Current assigned shard |
| db_host | TEXT | DB host for this shard |
| status | TEXT | active / warning / suspended / terminated |
| plan | TEXT | starter / growth / scale / enterprise |
| max_students | INTEGER | Current plan limit |
| custom_domain | TEXT | "portal.dpsedu.in" — nullable |
| logo_url | TEXT | CDN URL |
| primary_color | TEXT | Hex code |
| enabled_modules | TEXT[] | ['hostel', 'transport', 'library'] |
| academic_year_start | INTEGER | Month number — 6 for June |
| whatsapp_enabled | BOOLEAN | Default false |
| whatsapp_wallet | NUMERIC | Prepaid balance |
| created_at | TIMESTAMPTZ | |
| suspended_at | TIMESTAMPTZ | Nullable |
| terminated_at | TIMESTAMPTZ | Nullable |

---

## Forms — Always API, Never CDN

All forms (registration, fee payment, exam, admission) are served from the API — never CDN.

| Content | Source | Reason |
|---|---|---|
| Exam questions | API / DB | Stale CDN could skip questions |
| Fee payment form | API / DB | Amount must be real-time |
| Admission form | API / DB | Mandatory fields can change |
| Registration form | API / DB | Validations must be current |
| Timetable (view only) | CDN | Display only — stale acceptable |
| Study notes | CDN | Static content |
| Published results | CDN | Immutable after publish |

> Rule: If user submits data → API. If user only reads → CDN.
