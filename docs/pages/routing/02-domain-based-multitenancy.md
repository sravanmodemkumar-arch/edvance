# EduForge — Domain-Based Multi-Tenancy
## Each Institution Has Its OWN Domain. Content Changes Based on Domain.

> `www.narayana.ac.in` → Narayana's portal (their branding, their students, their data)
> `www.srichaitanya.edu.in` → Sri Chaitanya's portal (their branding, their data)
> `www.xyz-school.com` → XYZ School's portal
>
> Same EduForge engine. Different domain = completely different experience.
> The domain IS the institution. Everything resolves from it.

---

## How It Works — Domain Resolution Flow

```
User types: www.narayana.ac.in
                  │
                  ▼
        DNS (managed by institution)
        CNAME: www.narayana.ac.in → proxy.eduforge.in
                  │
                  ▼
        Cloudflare / EduForge Edge
        Reads: Host header = "www.narayana.ac.in"
                  │
                  ▼
        Domain Lookup Table:
        SELECT tenant_slug FROM domains
        WHERE domain = 'www.narayana.ac.in'
        → slug: "narayana", type: "coaching", tier: "enterprise"
                  │
                  ▼
        Load tenant config:
        {
          name: "Narayana Educational Institutions",
          logo_url: "r2.eduforge.in/narayana/logo.png",
          primary_color: "#C62828",
          favicon: "r2.eduforge.in/narayana/favicon.ico",
          features: ["hostel", "transport", "tsp", "coaching"],
          custom_domain: "www.narayana.ac.in",
          eduforge_subdomain: "narayana.eduforge.in"
        }
                  │
                  ▼
        Render: Narayana's portal
        Title: "Narayana Coaching — Login"
        Logo: Narayana logo
        Color: Narayana red
        Data: Narayana students/staff/exams only
```

---

## Domain Types

### Type 1 — EduForge Default Subdomain (All institutions get this free)

```
narayana.eduforge.in         → Narayana's portal (default)
xyz-school.eduforge.in       → XYZ School's portal (default)
ssc.eduforge.in              → SSC Exam Domain (EduForge-owned)
admin.eduforge.in            → Platform Admin (EduForge internal)
```

- Auto-created when institution is onboarded
- Format: `[institution-slug].eduforge.in`
- Always works, even if custom domain is added later

### Type 2 — Custom Domain (Institution's own domain)

```
www.narayana.ac.in           → Same as narayana.eduforge.in
www.srichaitanya.edu.in      → Same as srichaitanya.eduforge.in
portal.xyzschool.com         → Same as xyz-school.eduforge.in
tests.narayana.ac.in         → Narayana's TSP portal
```

- Institution adds their domain in portal settings
- Institution's IT team adds CNAME: `their-domain → proxy.eduforge.in`
- EduForge issues SSL certificate (via Let's Encrypt / Cloudflare) automatically
- Custom domain works alongside EduForge subdomain — both remain active

### Type 3 — TSP Custom Domain

```
www.narayana-tests.com       → Narayana's white-label test series (no EduForge branding)
tests.srichaitanya.in        → Sri Chaitanya's TSP
mocktest.abccoaching.com     → ABC Coaching's TSP
```

- On TSP portals: EduForge branding can be fully hidden (white-label)
- "Powered by EduForge" shown only if operator permits it

---

## Domain → Content Mapping Table

| Domain | Institution | Portal Type | Branding | Features Available |
|---|---|---|---|---|
| `www.narayana.ac.in` | Narayana | Coaching + TSP | Narayana logo, red | Batches, mock tests, TSP, hostel |
| `narayana.eduforge.in` | Narayana | Same | Same | Same (both domains, same portal) |
| `www.xyz-school.com` | XYZ School | School | XYZ logo, blue | Classes, attendance, exams, fees |
| `portal.apresidential.gov.in` | AP Residential Schools | School (Govt) | Govt logo, AP green | Classes, attendance, reports, RTE |
| `ssc.eduforge.in` | EduForge (owned) | Exam Domain | EduForge SSC branding | Mock tests, rankings, subscriptions |
| `narayana-tests.com` | Narayana (TSP) | White-label TSP | Narayana only, NO EduForge | Test series, results, certificates |
| `admin.eduforge.in` | EduForge internal | Platform Admin | EduForge branding | Everything — all tenants |
| `partners.eduforge.in` | EduForge (B2B) | Partner Portal | EduForge branding | API keys, webhooks, usage |

---

## What Changes Per Domain

When a user visits any domain, EVERYTHING adapts:

### Visual Identity

| Element | How It Changes |
|---|---|
| Browser tab title | "[Institution Name] — [Page Name]" |
| Favicon | Institution's icon |
| Logo (top-left) | Institution's logo |
| Primary color | Institution's brand color (buttons, links, active states) |
| Background pattern | Subtle pattern using brand color |
| Login page left panel | Institution name, city, today's live stats |
| Email notifications | "From: [Institution Name] via EduForge" |
| WhatsApp messages | "[Institution Name]: ..." |
| PDF certificates | Institution logo + letterhead |
| PDF invoices | Institution name + address |
| Copyright footer | "© [Institution Name]. Powered by EduForge" (or hide EduForge for TSP) |

### Content

| Element | How It Changes |
|---|---|
| Student data | Only students of this institution |
| Staff data | Only staff of this institution |
| Exam data | Only exams created in this institution |
| Fee data | This institution's fee structure |
| Timetable | This institution's schedule |
| Notifications | This institution's announcements |
| MCQ bank | Shared EduForge bank + this institution's private questions |
| Analytics | Only this institution's data |
| Branding in student reports | Institution name + logo |

### Features (Enabled per institution plan)

| Feature | Controlled by | Example |
|---|---|---|
| Hostel management | Institution has hostel enabled | Residential schools/coaching only |
| Transport tracking | Transport feature enabled | Schools with buses |
| TSP (test series) | TSP plan purchased | Coaching with own test series |
| AI study plan | Premium tier | Premium institutions only |
| Advanced analytics | Enterprise plan | Large coaching chains |
| Parent portal | Feature enabled | Enabled by default, can be disabled |
| Online fee payment | Razorpay account linked | Institution must set up Razorpay |
| DigiLocker integration | Govt. institutions | Certificate issuance via DigiLocker |
| RTE quota tracking | School type = govt/aided | RTE feature visible only to govt schools |

---

## Domain Setup — Institution Onboarding

### Step 1 — EduForge assigns default subdomain

When institution is onboarded:
```
Slug auto-generated from name:
"Narayana Educational Institutions" → "narayana"
Portal live at: narayana.eduforge.in
```

### Step 2 — Institution adds custom domain (optional)

Institution admin goes to Settings → Custom Domain:

```
┌────────────────────────────────────────────────────────────────────┐
│  Custom Domain Setup                                               │
│                                                                    │
│  Your EduForge subdomain:  narayana.eduforge.in  (always active)  │
│                                                                    │
│  Add your own domain:                                              │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │  www.narayana.ac.in                                        │   │
│  └────────────────────────────────────────────────────────────┘   │
│  [Verify & Add Domain]                                             │
│                                                                    │
│  ─────────────────────────────────────────────────────────────    │
│  DNS Setup Instructions (share with your IT team):                │
│                                                                    │
│  Add this CNAME record to your domain's DNS:                       │
│  Type: CNAME                                                       │
│  Name: www  (or @ for root domain)                                 │
│  Value: proxy.eduforge.in                                          │
│  TTL: Auto                                                         │
│                                                                    │
│  After adding DNS, click [Verify DNS →]                            │
│  SSL certificate will be issued automatically (1–2 minutes)       │
│                                                                    │
│  Status: ⏳ Awaiting DNS propagation (can take up to 48 hours)    │
└────────────────────────────────────────────────────────────────────┘
```

### Step 3 — Verification + SSL

| Step | What Happens |
|---|---|
| Institution saves domain | Domain stored as `pending` in `tenants.custom_domains` table |
| EduForge verifies | Checks CNAME points to `proxy.eduforge.in` |
| DNS verified | Status → `verified` |
| SSL issued | Let's Encrypt / Cloudflare SSL cert issued automatically |
| Domain goes live | Status → `active`. Both domains work simultaneously. |
| Failure | If DNS not set up correctly after 72hr → notification sent to institution admin |

---

## Multiple Domains — Same Institution

An institution can have multiple custom domains pointing to the same portal:

```
www.narayana.ac.in          → Main portal
students.narayana.ac.in     → Student-facing (same portal, opens in student role view)
staff.narayana.ac.in        → Staff-facing (same portal, prompts staff login)
tests.narayana.ac.in        → TSP portal (separate — Narayana's white-label test series)
```

Each domain can have a `default_view` setting:
- `students.narayana.ac.in` → auto-routes student logins, hides staff login CTA
- `staff.narayana.ac.in` → shows staff login, hides student registration

---

## Domain-Based API Resolution

Every API call from the frontend sends the domain in the header:

```http
GET /api/v1/home
Host: www.narayana.ac.in
Authorization: Bearer [jwt-token]
X-EduForge-Domain: www.narayana.ac.in
```

Backend middleware:
```python
async def resolve_tenant(request: Request):
    domain = request.headers.get("host")  # "www.narayana.ac.in"
    tenant = await db.tenants.find_by_domain(domain)
    if not tenant:
        raise HTTPException(404, "Unknown domain")
    request.state.tenant = tenant
    request.state.tenant_slug = tenant.slug  # "narayana"
    return tenant
```

All subsequent DB queries are automatically scoped to `tenant.slug`:
```python
students = await db.students.filter(tenant_slug=request.state.tenant_slug).all()
# Returns ONLY Narayana's students — never leaks to other tenants
```

---

## Frontend Domain Resolution

```javascript
// On app init — detect current domain and load tenant config
const domain = window.location.hostname  // "www.narayana.ac.in"

const tenantConfig = await fetch('/api/v1/tenant/config', {
  headers: { 'X-EduForge-Domain': domain }
})

// Response:
{
  name: "Narayana Educational Institutions",
  slug: "narayana",
  logo_url: "...",
  primary_color: "#C62828",
  favicon_url: "...",
  portal_type: "coaching",
  features: ["batches", "mock_tests", "tsp", "hostel"],
  custom_domain: "www.narayana.ac.in",
  meta_title: "Narayana Portal",
  meta_description: "Narayana's student and staff portal"
}

// Apply to document:
document.title = tenantConfig.name
document.querySelector('link[rel=icon]').href = tenantConfig.favicon_url
document.documentElement.style.setProperty('--primary', tenantConfig.primary_color)
// ... apply all tokens
```

---

## Security — Data Isolation Per Domain

**Most critical rule: No data from Tenant A ever appears on Tenant B's domain.**

| Security Layer | How |
|---|---|
| JWT scoped to tenant | JWT payload contains `tenant_slug`. Token for narayana.ac.in does NOT work on abc-school.com |
| DB queries tenant-filtered | Every query: `WHERE tenant_slug = :current_tenant` — enforced by middleware |
| API validation | Every endpoint validates `jwt.tenant_slug === request.tenant_slug` |
| R2/S3 assets | Files stored in `/{tenant_slug}/` prefix. Signed URLs scoped to tenant. |
| Audit logs | Every data access logged with tenant_slug, user_id, IP |
| Test in CI | Automated tests verify tenant isolation — Tenant A token cannot fetch Tenant B data |

---

## Domain Routing — Summary

```
Any Domain (www.college.com / www.school.com / ssc.eduforge.in)
      │
      ▼
EduForge Edge (Cloudflare)
Reads Host header → looks up tenant in DB
      │
      ▼
Tenant Config Loaded
{ name, slug, logo, color, features, type }
      │
      ▼
User visits /login → sees THEIR institution's login page
User verified → sees THEIR institution's data
Every page → renders with THEIR branding
Every API → returns THEIR data only
      │
      ▼
Result: www.narayana.ac.in  = Narayana's portal
        www.xyz-school.com  = XYZ School's portal
        (Same engine. Different world.)
```
