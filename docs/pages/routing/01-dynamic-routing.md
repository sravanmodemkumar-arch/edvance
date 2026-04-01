# EduForge — Dynamic Routing Specification
## All Pages Render Based on Route + Role + Institution Context

> Every URL on EduForge is dynamic.
> The SAME route renders completely different content based on:
>   1. Which institution's subdomain you're on (`[slug].eduforge.in`)
>   2. Who you are (your role + access level)
>   3. What URL parameters are present (`/students/123`, `/exams/456`)
>
> This document is the single source of truth for how routes work across all 10 groups.

---

## Core Concepts

### Concept 1 — Domain-Based Multi-Tenancy

Every institution has its OWN domain. Content changes completely based on the domain:
```
www.narayana.ac.in           → Narayana's portal (their branding, their data)
www.xyz-school.com           → XYZ School's portal
ssc.eduforge.in              → SSC Exam Domain (EduForge-owned)
admin.eduforge.in            → EduForge internal admin
```

> See full domain architecture: [02-domain-based-multitenancy.md](02-domain-based-multitenancy.md)

Each institution also gets a free EduForge subdomain (`narayana.eduforge.in`) that works alongside their custom domain. The domain IS the tenant — it determines branding, data, and available features.

### Concept 2 — Role-Based Rendering

The SAME route `/home` renders differently per role:

| Route | Who | What They See |
|---|---|---|
| `/home` | Principal | Full school management dashboard |
| `/home` | Class Teacher | Their class only — attendance, marks, messages |
| `/home` | Student | Personal dashboard — marks, tests, attendance |
| `/home` | Parent | Their children's summary |

### Concept 3 — Route Guards

Every route has 3 layers of protection before rendering:
```
Request to route
      │
      ▼
[Guard 1] Auth check — is user logged in? → if not → /login
      │
      ▼
[Guard 2] Tenant check — does this slug exist + subscription active? → if not → /suspended
      │
      ▼
[Guard 3] Permission check — does user's role allow this route? → if not → /403
      │
      ▼
[Render] Dynamic content based on role context
```

---

## URL Architecture — All Portals

### URL Pattern Rules

```
[tenant-slug].[domain]/[module]/[sub-module]/[entity-id]/[action]

Examples:
xyz-school.eduforge.in/students                     → student list
xyz-school.eduforge.in/students/1042                → student profile (roll 1042)
xyz-school.eduforge.in/students/1042/performance    → performance tab
xyz-school.eduforge.in/exams/new                    → create exam
xyz-school.eduforge.in/exams/567/results            → exam 567 results
xyz-school.eduforge.in/exams/567/results?class=12   → filtered by class 12
```

### URL Parameter Types

| Type | Syntax | Example | Contains |
|---|---|---|---|
| Tenant slug | subdomain | `xyz-school.eduforge.in` | Which institution |
| Resource ID | path segment | `/students/1042` | Which entity |
| Action | path segment | `/exams/567/edit` | What to do |
| Filters | query string | `?class=12&stream=mpc` | How to filter data |
| Tab | query string | `?tab=performance` | Which tab open |
| Page | query string | `?page=3&per_page=25` | Pagination state |
| Modal | query string | `?modal=add-student` | Open modal directly |
| Drawer | query string | `?drawer=student&id=1042` | Open drawer directly |

> **Shareable URLs:** All state is in the URL. Copy-paste URL = same view for anyone with access.

---

## Full Route Map — Per Portal

### Platform Admin (`admin.eduforge.in`)

| Route | Page | Min Level | Notes |
|---|---|---|---|
| `/` → redirect | — | — | Redirects to `/home` |
| `/login` | Login | Public | Auth page |
| `/verify-otp` | OTP | Public | Auth page |
| `/2fa` | 2FA | Public (post-OTP) | Level 4/5 only |
| `/home` | Platform dashboard | L1 | War room on exam day |
| `/institutions` | Institution list | L3 | All tenants |
| `/institutions/new` | Add institution | L3 | Onboarding wizard |
| `/institutions/:slug` | Institution detail | L3 | View/edit institution |
| `/institutions/:slug/users` | Institution users | L3 | Staff list |
| `/institutions/:slug/exams` | Institution exams | L3 | Their exam history |
| `/institutions/:slug/billing` | Institution billing | L3 | Subscription, invoices |
| `/users` | All users (all tenants) | L3 | Global user search |
| `/users/:id` | User profile | L3 | View/edit any user |
| `/content/mcq` | MCQ Bank | L2 | Filter by subject/exam |
| `/content/mcq/new` | Create MCQ | L2 | New question form |
| `/content/mcq/:id` | MCQ detail | L2 | View/edit/review |
| `/content/mcq/:id/review` | Review MCQ | L2 | Reviewer workflow |
| `/content/notes` | Notes library | L2 | All notes |
| `/content/videos` | Video library | L2 | YouTube mapped content |
| `/exams` | Exam list | L3 | All scheduled exams |
| `/exams/new` | Create exam | L3 | Schedule new exam |
| `/exams/:id` | Exam detail | L3 | Live monitor on exam day |
| `/exams/:id/results` | Exam results | L3 | Rank, analytics |
| `/exams/:id/monitor` | Live monitor | L4 | War room per exam |
| `/bgv` | BGV dashboard | L3 | Pending verifications |
| `/bgv/:request-id` | BGV request | L3 | Process verification |
| `/analytics` | Analytics overview | L1 | Platform MIS |
| `/analytics/revenue` | Revenue analytics | L1 | Finance view |
| `/analytics/exams` | Exam analytics | L1 | Test performance |
| `/support/tickets` | Support tickets | L3 | All open tickets |
| `/support/tickets/:id` | Ticket detail | L3 | Conversation thread |
| `/billing/invoices` | All invoices | L3 | Per institution |
| `/billing/plans` | Subscription plans | L4 | Plan config |
| `/settings/platform` | Platform settings | L4 | System config |
| `/settings/security` | Security settings | L4 | JWT, KMS, WAF |
| `/audit-log` | Audit log | L4 | All actions logged |
| `/ai/pipeline` | AI MCQ pipeline | L4 | Generation jobs |

---

### School Portal (`[slug].eduforge.in`)

| Route | Page | Role Context | What Changes by Role |
|---|---|---|---|
| `/home` | Home/Dashboard | ALL roles | Sections, KPIs, quick actions change completely |
| `/students` | Student list | Staff (Principal → Teacher) | Teacher sees only their class. Principal sees all. |
| `/students/new` | Add student | L3+ | Only admin roles can add |
| `/students/:id` | Student profile | Staff + Parent | Parent sees only their child. Staff sees all. |
| `/students/:id/performance` | Performance tab | Staff + Student + Parent | Student sees own only. Staff sees all. |
| `/students/:id/attendance` | Attendance tab | Same as above | |
| `/students/:id/fees` | Fee tab | Accountant + Admin + Parent | Student sees view-only. Parent can pay. |
| `/students/:id/documents` | Documents tab | Admin + Student | Student sees own certs. Admin manages. |
| `/staff` | Staff list | L4+ | Principal, HOD, Admin only |
| `/staff/new` | Add staff | L4+ | |
| `/staff/:id` | Staff profile | L3+ | Own profile (L1), others need L3+ |
| `/classes` | Class list | L3+ | |
| `/classes/:id` | Class detail | L3+ | Teacher sees only their class |
| `/classes/:id/students` | Class students | L3+ | |
| `/classes/:id/attendance` | Mark attendance | L3 (class teacher) | Only their assigned class |
| `/exams` | Exam list | L3+ | Teacher sees their subject exams only |
| `/exams/new` | Schedule exam | L3+ | Subject teacher creates for their subject |
| `/exams/:id` | Exam detail | L3+ | |
| `/exams/:id/questions` | Question paper | L2+ | |
| `/exams/:id/monitor` | Live monitor | L3+ | On exam day |
| `/exams/:id/results` | Results | L3+ | Published after approval |
| `/exams/:id/results/analytics` | Results analytics | L3+ | |
| `/attendance` | Attendance overview | L3+ | Class teacher sees their class |
| `/attendance/daily` | Daily attendance | L3+ | |
| `/attendance/reports` | Attendance reports | L3+ | |
| `/fees` | Fee management | Accountant + Admin | |
| `/fees/collect` | Collect fee | Accountant | |
| `/fees/defaulters` | Fee defaulters | Accountant + Principal | |
| `/fees/receipts` | Receipts | Accountant | |
| `/timetable` | Timetable | L2+ | Teacher sees their schedule. Student sees class timetable. |
| `/timetable/edit` | Edit timetable | L4+ | |
| `/content/notes` | Notes | L2+ | Teacher sees subject notes only |
| `/content/videos` | Videos | L2+ | |
| `/notifications/send` | Send notification | L3+ | |
| `/reports` | MIS reports | L3+ | |
| `/settings` | Portal settings | L4+ | Principal, Admin only |
| `/hostel` | Hostel management | Warden + Admin | Only if hostel feature enabled |
| `/transport` | Transport management | Transport manager + Admin | Only if transport enabled |

**Student-specific routes (same portal, student role):**

| Route | What Student Sees |
|---|---|
| `/home` | Personal dashboard — attendance, marks, schedule |
| `/students/:own-id` | Own profile — view only |
| `/students/:own-id/performance` | Own performance charts |
| `/exams` | Only published exams they can take |
| `/exams/:id/attempt` | Take the exam |
| `/timetable` | Their class timetable only |
| `/content/notes` | Notes published for their class/subject |
| `/content/videos` | Videos for their stream/class |
| `/fees` | Own fee statement — can pay |

---

### Coaching Portal (`[slug].eduforge.in/coaching`)

| Route | Page | Role Context |
|---|---|---|
| `/home` | Coaching dashboard | Director sees revenue + all batches. Faculty sees own batches. |
| `/batches` | Batch list | Director sees all. Faculty sees assigned. |
| `/batches/new` | Create batch | L4+ |
| `/batches/:id` | Batch detail | |
| `/batches/:id/students` | Batch students | Faculty + Admin |
| `/batches/:id/attendance` | Batch attendance | Faculty (own batch) |
| `/batches/:id/schedule` | Batch schedule | Faculty + Admin |
| `/students` | All students | Director + Admin see all. Faculty see batch-only. |
| `/students/:id` | Student profile | |
| `/mock-tests` | Test series list | |
| `/mock-tests/new` | Create test | L3+ |
| `/mock-tests/:id` | Test detail | |
| `/mock-tests/:id/monitor` | Live monitor | Exam day |
| `/mock-tests/:id/results` | Results + ranks | |
| `/mock-tests/:id/analytics` | Analytics | Director + Faculty |
| `/fees` | Fee management | Accountant + Director |
| `/counselling` | Counsellor dashboard | Counsellors only |
| `/counselling/at-risk` | At-risk students | |
| `/hostel` | Hostel (if residential) | Warden + Admin |
| `/reports` | MIS reports | Director + Admin |

---

### Exam Domain (`ssc.eduforge.in`, `rrb.eduforge.in`, etc.)

| Route | Page | Access |
|---|---|---|
| `/` | Domain landing page | Public (not logged in) |
| `/login` | Login | Public |
| `/register` | Self-register | Public |
| `/home` | Aspirant dashboard | Authenticated |
| `/tests` | Test series list | Free: sees limited. Premium: all. |
| `/tests/:id` | Test detail | |
| `/tests/:id/attempt` | Take test | Free: 5/month. Premium: unlimited. |
| `/tests/:id/results` | My result | After submit |
| `/tests/:id/results/analysis` | Detailed analysis | Premium only |
| `/tests/:id/results/solutions` | Solutions | Premium only |
| `/rankings` | National leaderboard | All |
| `/rankings?exam=ssc-cgl` | Exam-specific rank | |
| `/profile` | My profile | |
| `/profile/performance` | Performance history | |
| `/profile/weak-topics` | Weak topic analysis | Premium |
| `/profile/ai-plan` | AI study plan | Premium |
| `/subscription` | Plans + upgrade | |
| `/subscription/checkout` | Pay + activate | |

---

### Parent Portal (`parent.eduforge.in`)

| Route | Page | Dynamic by |
|---|---|---|
| `/home` | Unified parent dashboard | Number of children, their institutions |
| `/children` | My children list | Their enrolled children |
| `/children/:student-id` | Child detail | Which child, which institution |
| `/children/:student-id/attendance` | Child's attendance | School or Coaching attendance |
| `/children/:student-id/marks` | Child's marks | Institution-specific |
| `/children/:student-id/fees` | Child's fee status | Can pay here |
| `/children/:student-id/timetable` | Child's schedule | |
| `/children/:student-id/performance` | Performance charts | |
| `/fees` | All fees — all children | Unified payment screen |
| `/fees/pay` | Pay fees | Razorpay checkout |
| `/notifications` | All notifications | All children + all institutions |
| `/messages` | Messages | Teacher messages per child |
| `/profile` | Parent profile | |

---

### B2B Partner Portal (`partners.eduforge.in`)

| Route | Page | Role |
|---|---|---|
| `/home` | Partner dashboard | API usage, student count, billing |
| `/api-keys` | API key management | Partner Admin |
| `/api-keys/new` | Generate new key | |
| `/webhooks` | Webhook config | |
| `/webhooks/new` | Add webhook | |
| `/docs` | API documentation | All |
| `/usage` | API usage analytics | |
| `/usage/logs` | API call logs | |
| `/billing` | Partner billing | |
| `/sandbox` | Sandbox environment | Dev team |
| `/students` | Synced students | Per integration |
| `/results` | Test results feed | Per integration |

---

## Dynamic Content Rules (Per Route)

### Rule 1 — Route Guards (Applied to ALL routes)

```
Every route check (in order):

1. isAuthenticated?
   NO → redirect /login?next=[current-url]

2. isTokenValid?
   NO → show session-expired overlay ([07-session-expired.md])

3. isTenantActive?
   NO → redirect /tenant-suspended

4. hasRoutePermission(user.role, route)?
   NO → show /403 page with "Contact admin for access"

5. isFeatureEnabled(tenant, feature)?
   NO → show feature-not-enabled card inline (not redirect)

6. hasSubscription(required_tier)?
   NO → show upgrade prompt (not redirect — inline CTA)

7. ✅ Render content
```

### Rule 2 — API Call Per Route

Every page on mount makes ONE primary API call:
```
GET /api/v1/page-data
  ?route=[current-route]
  &tenant=[slug]
  &role=[user.role]
  &entity_id=[path param if any]
  &filters=[query params]

Response: {
  page_title,
  breadcrumb,
  sections: [...],          // which sections to render
  permissions: {...},        // what actions allowed on this page
  data: {...},               // page-specific data
  metadata: {...}            // pagination, counts etc.
}
```

The response tells the frontend EXACTLY what to render. The frontend is a thin renderer.

### Rule 3 — Section Visibility (Same Page, Different Roles)

Each page section has a `visible_to` config:

```json
{
  "page": "student-profile",
  "sections": [
    {
      "id": "personal-info",
      "visible_to": ["all"],
      "editable_by": ["principal", "admin", "student-own"]
    },
    {
      "id": "academic-performance",
      "visible_to": ["all"],
      "editable_by": ["subject-teacher", "admin"]
    },
    {
      "id": "fee-details",
      "visible_to": ["accountant", "principal", "parent", "student-own"],
      "editable_by": ["accountant"]
    },
    {
      "id": "disciplinary-notes",
      "visible_to": ["principal", "class-teacher"],
      "editable_by": ["class-teacher", "principal"],
      "hidden_from": ["student", "parent"]
    },
    {
      "id": "bgv-status",
      "visible_to": ["platform-admin", "bgv-team"],
      "editable_by": ["bgv-team"]
    }
  ]
}
```

### Rule 4 — Navigation Adapts to Role

Sidebar nav items are built dynamically from the user's permissions:

```
Backend returns: user.allowed_routes = ["/home", "/students", "/classes/:id/attendance", "/timetable"]

Frontend builds sidebar with ONLY these items.
A class teacher never sees "/fees" or "/settings" in their sidebar.
```

### Rule 5 — Action Buttons Adapt to Role

Same page — different action buttons per role:

| Page | Principal | Subject Teacher | Student |
|---|---|---|---|
| `/exams/:id` | [Edit] [Delete] [Publish Results] [View Analytics] | [View Questions] [View Results] | [Take Exam] or [View My Results] |
| `/students/:id` | [Edit Profile] [Suspend] [Download TC] | [View Performance] [Message] | [Edit own profile] |
| `/fees` | [Mark Paid] [Send Reminder] [Export] | — | [Pay Now] [View Receipt] |

---

## Route-to-Component Rendering Map

```
Route: /students/:id

Frontend receives route params: { slug: "xyz-school", id: "1042" }
Frontend reads: user.role = "class-teacher", user.assigned_class = "12A"

Decision tree:
  Is id the current user's own student id? NO
  Is student in user's assigned class? YES (student is in 12A)
  What can class teacher see?
    → PersonalInfoSection (read-only)
    → AttendanceSection (can edit — their class)
    → AcademicSection (read-only — not their subject)
    → FeeSection (hidden)
    → DisciplinarySection (can view + add note)
    → DocumentsSection (hidden)

Frontend renders:
  <StudentProfile
    sections={["personal", "attendance", "academic", "disciplinary"]}
    editPermissions={{ attendance: true, disciplinary: true }}
    hiddenSections={["fees", "documents"]}
    studentId={1042}
    tenantSlug="xyz-school"
  />
```

---

## Dynamic Route Parameters — Reference Table

| Parameter | Where | Type | Example |
|---|---|---|---|
| `slug` | Subdomain | String | `xyz-school` in `xyz-school.eduforge.in` |
| `:id` | Path | Integer or UUID | `/students/1042` |
| `:exam-id` | Path | UUID | `/exams/f3a2c1-...` |
| `:class` | Query | String | `?class=12A` |
| `:stream` | Query | String | `?stream=mpc` |
| `:subject` | Query | String | `?subject=mathematics` |
| `:status` | Query | String | `?status=active,pending` |
| `:page` | Query | Integer | `?page=3` |
| `:per_page` | Query | Integer | `?per_page=25` |
| `:sort` | Query | String | `?sort=attendance_asc` |
| `:tab` | Query | String | `?tab=performance` |
| `:drawer` | Query | String | `?drawer=student&id=1042` |
| `:modal` | Query | String | `?modal=add-student` |
| `:search` | Query | String | `?search=ravi+kumar` |
| `:date` | Query | Date string | `?date=2024-03-15` |
| `:from` | Query | Date string | `?from=2024-01-01&to=2024-03-31` |
| `:period` | Query | String | `?period=this-month` |

---

## 403 — Permission Denied Page

> Shown when user's role does not have access to a route.

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│              🔒                                            │
│                                                            │
│   You don't have access to this page                       │
│                                                            │
│   Your role ([Role Name]) does not have permission         │
│   to view [page name].                                     │
│                                                            │
│   If you need access, contact your administrator.          │
│                                                            │
│   [← Go to Dashboard]          [Contact Admin]            │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

- Shows user's current role
- Shows which page they tried to access
- Does NOT show WHY they don't have access (security)
- Logs the unauthorized access attempt (audit trail)

---

## 404 — Page Not Found

> Shown when route exists but entity (student, exam etc.) does not.

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│              🔍                                            │
│                                                            │
│   This page doesn't exist                                  │
│                                                            │
│   The [student/exam/record] you're looking for was         │
│   either deleted or never existed.                         │
│                                                            │
│   [← Go Back]              [Go to Dashboard]              │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

---

## Tenant Suspended Page

> Shown on any route when the institution's subscription is inactive.

```
┌────────────────────────────────────────────────────────────┐
│  [Institution Logo]                                        │
│                                                            │
│              ⏸                                            │
│                                                            │
│   [Institution Name] portal is currently suspended         │
│                                                            │
│   Reason: Subscription expired on [date]                   │
│                                                            │
│   Institution admins: Contact EduForge to renew.          │
│   Staff & Students: Your data is safe and will be         │
│   restored when subscription is renewed.                   │
│                                                            │
│   EduForge Support: 1800-XXX-XXXX                         │
│   Reference: [Tenant ID]                                   │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

- Students cannot access anything — but their data is preserved
- Only institution admin can log in (limited) to view billing and renew
