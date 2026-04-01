# C-01 — Tenant Manager

> **Route:** `/engineering/tenants/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10, Level 5)
> **Read Access:** Backend Engineer (Role 11) · DevOps/SRE (Role 14) · DBA (Role 15) · Security Engineer (Role 16)
> **File:** `c-01-tenant-manager.md`
> **Priority:** P0 — Platform cannot run without tenant provisioning
> **Status:** ⬜ Amendment pending — G29 (Tenant Storage Quota)

---

## 1. Page Name & Route

**Page Name:** Tenant Manager
**Route:** `/engineering/tenants/`
**Part-load routes:**
- `/engineering/tenants/?part=table` — tenant list table
- `/engineering/tenants/?part=kpi` — KPI strip
- `/engineering/tenants/?part=drawer&tenant_id={id}` — tenant detail drawer
- `/engineering/tenants/?part=provision-modal` — new tenant provision modal
- `/engineering/tenants/?part=progress&job_id={id}` — Celery provisioning progress

---

## 2. Purpose (Business Objective)

The Tenant Manager is the single authoritative console for the full lifecycle of all 2,050 institution tenants on the platform. It allows Platform Admins to provision new tenants (each a dedicated PostgreSQL schema), assign subscription plans, configure institution metadata, suspend portals, hard-delete tenants with a 30-day grace window, and execute emergency data wipes for DPDPA compliance.

Every action on this page has the highest blast radius in the entire system — a suspend affects all students at that institution, a delete permanently removes 2M+ rows, and an emergency wipe triggers CERT-In obligations. Accordingly, every destructive operation is gated behind 2FA, queued as a Celery async job with real-time progress reporting, and written to an immutable audit log.

**Business goals this page serves:**
- Onboard new institutions in < 25 minutes (Celery provisioning SLA)
- Maintain full visibility into health and status of all 2,050 tenants
- Enable instant suspension of a compromised portal without data loss
- Satisfy DPDPA Article 8 data erasure obligations with an auditable wipe trail
- Give DBA and DevOps read access to schema inventory without giving write power

---

## 3. User Roles

| Role | Access Level | What They Can Do |
|---|---|---|
| Platform Admin (10) | Level 5 — Full | Provision · Edit · Suspend · Reinstate · Delete · Emergency wipe · Impersonate tenant admin |
| Backend Engineer (11) | Level 4 — Read | View tenant list · View tenant config · Cannot modify |
| DevOps / SRE (14) | Level 4 — Read | View tenant list · Schema health check results · Cannot modify |
| DBA (15) | Level 4 — Read | View schema names · connection counts · Cannot modify |
| Security Engineer (16) | Level 4 — Read | View suspension history · audit log · Cannot modify |

> All write operations: Platform Admin only. All writes: 2FA-gated. All writes: immutable audit log entry created.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Action Bar

**Purpose:** Establish page context, expose primary create action, and show last-refresh timestamp.

**User Interaction:**
- "Provision New Tenant" button — opens the 4-step provision modal
- Page title "Tenant Manager" with institution count badge ("2,050 tenants")
- Last refreshed timestamp with manual refresh button
- Quick link to Schema Health Report (C-11)

**UI Components:**
- H1 page title with badge counter
- Primary CTA button (Provision New Tenant) — disabled for non-Admin roles
- Secondary button (Refresh) with spinner on load
- Breadcrumb: Engineering → Tenant Manager
- Timestamp: "Last updated: 2 min ago"

**Data Flow:**
- Page load triggers `GET /engineering/tenants/?part=kpi` and `GET /engineering/tenants/?part=table` simultaneously via HTMX on page mount
- Tenant count badge queries `SELECT COUNT(*) FROM platform_tenants` on the shared schema
- Refresh reloads both KPI and table parts

**Role-Based Behavior:**
- Platform Admin: "Provision New Tenant" button visible and active
- All other roles: button hidden; replaced with read-only notice banner ("You have read-only access to tenant data")

**Edge Cases:**
- If total tenant count > 2,050 (data anomaly) — show amber badge with exclamation and link to DBA dashboard
- If last-refresh > 10 min — show stale data warning in amber

**Performance Considerations:**
- Tenant count badge served from Memcached (django.core.cache, key `platform:tenant_count`) with 60s TTL
- Full page load target: < 400ms (table lazy-loaded after KPI strip)

**Mobile Behavior:**
- Action bar stacks vertically on < 768px
- "Provision" button full width on mobile

**Accessibility Notes:**
- Refresh button has `aria-label="Refresh tenant list"`
- Badge counter has `aria-live="polite"` for screen reader announcements

---

### Section 2 — KPI Strip

**Purpose:** Give at-a-glance health of the entire tenant estate at page load.

**User Interaction:**
- Read-only strip; clicking a KPI card filters the table below (e.g., click "Suspended" → table filters to suspended tenants)
- Each card shows metric + 7-day trend arrow

**UI Components:**
- 6 KPI cards in a horizontal scrollable strip
- Each card: label · value · trend indicator (↑↓ or flat) · subtle sparkline (7 days)
- Color coding: green (healthy) · amber (warning) · red (critical)

**KPI Cards:**

| Card | Metric | Source | Refresh |
|---|---|---|---|
| Total Tenants | 2,050 | `platform_tenants` COUNT | 60s Memcached |
| Active | Count where `status = active` | `platform_tenants` | 60s Memcached |
| Suspended | Count where `status = suspended` | `platform_tenants` | 60s Memcached |
| Provisioning | Count where `status = provisioning` | Celery job queue | 30s poll |
| Schema Errors | Schemas failing health check | C-11 health job | 5 min Memcached |
| New This Month | Tenants provisioned in last 30 days | `provisioned_at` filter | 5 min Memcached |

**Data Flow:**
- KPI strip loaded via `GET /engineering/tenants/?part=kpi`
- HTMX polls `part=kpi` every 60s with guard `[!document.querySelector('.drawer-open,.modal-open')]`
- All values served from Memcached (django.core.cache); populated by background Celery beat task every 60s

**Role-Based Behavior:**
- Same KPI strip visible to all roles with access to this page
- Platform Admin: KPI cards are clickable filters
- Read-only roles: KPI cards are visual-only (no click-to-filter)

**Edge Cases:**
- Suspended count > 0 → amber highlight on Suspended card
- Schema Errors > 0 → red highlight + tooltip "Contact DBA team"
- If Celery is down and provisioning count cannot be fetched → card shows "--" with amber icon

**Performance Considerations:**
- All 6 metrics fetched in a single Memcached `get_many` call (< 5ms)
- If Memcached unavailable: fallback direct DB query (slower, amber indicator shown)

**Mobile Behavior:**
- Cards scroll horizontally on mobile; shows 3 cards visible with scroll hint

**Accessibility Notes:**
- Each KPI card has `role="status"` and `aria-label` describing the metric and value
- Trend arrows have screen-reader text ("up 12% from last week")

---

### Section 3 — Search, Filter & Sort Bar

**Purpose:** Allow Platform Admins and read-only engineers to quickly locate specific tenants among 2,050 records.

**User Interaction:**
- Full-text search box: searches across institution name · subdomain · admin email · schema name
- Dropdown filters: Institution Type · Plan · Status · Region · Provisioned Date range
- Sort controls: Name A–Z · Provisioned Date · Plan · Status · Student Count
- Active filter chips displayed below bar with individual × dismiss buttons
- "Clear all filters" link

**UI Components:**
- Search input with debounce (300ms) and magnifier icon
- 5 filter dropdowns (multi-select where applicable)
- Date range picker for "Provisioned between"
- Sort dropdown
- Active filter chip row
- Result count: "Showing 47 of 2,050 tenants"

**Filter Options:**

| Filter | Values |
|---|---|
| Institution Type | School · College · Institution Group · Coaching Center · All |
| Plan | Free · Starter · Growth · Enterprise · Custom |
| Status | Active · Suspended · Provisioning · Pending Deletion · Wiped |
| Region | North · South · East · West · Northeast · Central |
| Provisioned | Last 7 days · Last 30 days · Last 90 days · Custom range |

**Data Flow:**
- Search: `GET /engineering/tenants/?part=table&q={term}&type={type}&plan={plan}&status={status}`
- Debounce: 300ms after last keystroke before request fires
- URL state: all active filters reflected in URL query params (shareable filtered view)
- Server-side filtering against PostgreSQL `platform_tenants` table using indexed columns

**Role-Based Behavior:**
- All roles with page access see the same filters
- Search and filter are always available regardless of role

**Edge Cases:**
- Search with zero results: show empty state with "No tenants match your search. Try adjusting filters."
- Very long institution name in search results: truncated at 45 chars with tooltip for full name
- Special characters in search (SQL injection prevention): input sanitized server-side; also client-side validation strips `<>"'`

**Performance Considerations:**
- Search uses PostgreSQL `pg_trgm` trigram indexes on `name`, `subdomain`, `admin_email`
- Full 2,050-row table scan avoided by indexed filter columns
- Partial search results streamed via HTMX swap with `settle` transition

**Mobile Behavior:**
- Filters collapsed into "Filters" expandable panel on mobile
- Search bar always visible at top on mobile

**Accessibility Notes:**
- Search input has `aria-label="Search tenants by name, subdomain, or email"`
- Each filter dropdown has visible label and `aria-expanded` attribute
- Active filter chips have `aria-label="Remove {filter name} filter"`

---

### Section 4 — Tenant List Table

**Purpose:** Primary data surface showing all tenants with key status indicators and quick-action controls.

**User Interaction:**
- Click row → opens tenant detail drawer (720px right-side)
- Platform Admin: inline quick-action menu (⋮) per row with: View · Edit · Suspend / Reinstate · Delete · Impersonate
- Checkbox column for bulk operations (Platform Admin only)
- Infinite scroll (100 rows per page, scroll to load next batch)

**UI Components:**
- Sortable table with sticky header
- Row: institution logo thumbnail (32×32) · columns below
- Status badge with colour coding
- Quick-action ⋮ menu per row
- Bulk action toolbar (appears when rows selected)
- Loading skeleton rows on initial load

**Table Columns:**

| Column | Description | Sortable | Width |
|---|---|---|---|
| (checkbox) | Bulk select | — | 40px |
| Institution | Logo + Name + Subdomain | ✅ A–Z | 240px |
| Type | School / College / Group / Coaching | ✅ | 110px |
| Plan | Badge (Free/Starter/Growth/Enterprise/Custom) | ✅ | 100px |
| Status | Badge (Active/Suspended/Provisioning/Pending Delete/Wiped) | ✅ | 120px |
| Students | Count (live from tenant schema) | ✅ | 90px |
| Admin Email | Primary institution admin email | — | 180px |
| Provisioned | Date (DD MMM YYYY) | ✅ | 110px |
| Actions | ⋮ quick-action menu | — | 60px |

**Status Badge Colours:**
- Active → green
- Suspended → amber
- Provisioning → blue (pulsing)
- Pending Deletion → red (30-day countdown shown in tooltip)
- Wiped → grey strikethrough

**Data Flow:**
- Table loaded via `GET /engineering/tenants/?part=table`
- 100 rows per page; next batch loaded on scroll via HTMX `hx-trigger="revealed"`
- Student count per tenant: cached in Memcached per-tenant key; stale if > 24h shown with grey italic
- Sort: query param `sort=name&dir=asc` passed to backend

**Role-Based Behavior:**
- Platform Admin: checkbox column visible · ⋮ menu with all actions
- Read-only roles: no checkbox · ⋮ menu shows only "View" option

**Bulk Action Toolbar (Platform Admin only — appears on row selection):**
- Bulk Suspend (with confirmation modal)
- Bulk Export (CSV of selected tenants' metadata)
- Bulk Plan Change (opens plan selector modal)
- Selected count badge: "3 tenants selected"
- Deselect all link

**Edge Cases:**
- Tenant currently in provisioning state: all action menu items disabled except "View progress"
- Tenant in Pending Deletion with < 48h remaining: row highlighted red; "Delete Now" button in ⋮ menu
- Admin email bouncing (detected from SES bounce webhook): amber envelope icon next to email
- Schema health failure for a tenant: row shows amber warning icon in Institution column with tooltip

**Performance Considerations:**
- Table uses virtual scrolling for rows beyond viewport (no DOM bloat with 2,050 rows)
- Student counts loaded asynchronously after table renders (non-blocking)
- Memcached stores tenant list snapshot (key `platform:tenant_list`) refreshed every 120s
- Table render target: < 200ms from data receipt

**Mobile Behavior:**
- Table collapses to card view on < 768px
- Each card shows: Logo · Name · Type · Status badge · Provisioned date · Tap for drawer
- Horizontal scroll disabled on mobile; columns prioritised (hide Plan and Admin Email on < 480px)

**Accessibility Notes:**
- `<table>` with `role="grid"` and `aria-rowcount` set to total tenant count
- Sortable column headers have `aria-sort="ascending/descending/none"`
- Status badges have `role="status"` and descriptive `aria-label` ("Status: Active")
- Checkbox column: `aria-label="Select tenant {name}"` per row
- Keyboard: Tab to navigate rows · Enter to open drawer · Space to select checkbox

---

### Section 5 — Tenant Detail Drawer

**Purpose:** Full tenant profile view and edit surface, opened from any tenant row click.

**Drawer Width:** 720px
**Trigger:** Row click or "View" in ⋮ menu
**Close:** × button · Escape key · click outside drawer

**Tabs inside drawer:**

---

#### Tab 1 — Config

**Purpose:** View and edit all tenant configuration fields.

**Fields displayed:**

| Field | Type | Editable |
|---|---|---|
| Institution Name | Text | ✅ Admin |
| Institution Type | Select | ✅ Admin |
| Subdomain | Text (unique) | ✅ Admin (with subdomain conflict check) |
| Custom Domain | Text | ✅ Admin |
| Primary Admin Email | Email | ✅ Admin |
| Subscription Plan | Select (with upgrade/downgrade rules) | ✅ Admin |
| Region | Select (North/South/East/West/Northeast/Central) | ✅ Admin |
| Time Zone | Select | ✅ Admin |
| Language Default | Select (en/hi/te/ur/ta/kn) | ✅ Admin |
| Max Student Seats | Number (plan-enforced ceiling) | ✅ Admin |
| Storage Quota (GB) | Number (plan-enforced) | ✅ Admin |
| Logo URL | File upload (S3 presigned) | ✅ Admin |
| Status | Read-only badge | — |
| Schema Name | Read-only (auto-generated) | — |
| Provisioned At | Read-only date | — |
| Last Admin Login | Read-only timestamp | — |

**Save behaviour:** "Save Changes" button triggers 2FA challenge modal → on confirm → `PATCH /api/tenants/{id}/` → success toast "Tenant updated" → drawer refreshes config tab

**Subdomain conflict check:** On blur of subdomain field → inline async check `GET /api/tenants/subdomain-check/?value={subdomain}` → red inline error if taken

**Plan downgrade rules:**
- Cannot downgrade if current student count exceeds target plan's seat limit
- Downgrade warning modal: "This tenant has 4,200 students. Growth plan allows 3,000. Downgrade will suspend 1,200 excess student accounts. Confirm?"
- Downgrade requires 2FA regardless of admin confirmation

**Role-Based Behavior:**
- Platform Admin: all fields editable · Save Changes button visible
- Read-only roles: all fields read-only · Save Changes button hidden

**Edge Cases:**
- Subdomain already in use → inline red error on field · Save button disabled until resolved
- Logo upload exceeds 2MB → client-side validation error before upload attempt
- Email field change → confirmation step: "A verification email will be sent to the new admin email. The old admin retains access until new admin verifies."

---

#### Tab 2 — Schema

**Purpose:** Technical view of the tenant's PostgreSQL schema for DBA and DevOps reference.

**Fields displayed:**

| Field | Value |
|---|---|
| Schema Name | `tenant_{id}_{slug}` (e.g., `tenant_042_stjohns`) |
| Schema Size | Live from `pg_total_relation_size` |
| Table Count | Count of tables in schema |
| Total Rows | Estimated from `pg_stat_user_tables` |
| Connection Count | Live from PgBouncer pool |
| Last Vacuum | Autovacuum last run timestamp per critical table |
| Migration Version | Latest applied Django migration name |
| Pending Migrations | Count of unapplied migrations (link to C-12) |
| Index Health | Flagged indexes (bloated/missing) count (link to C-11) |
| Schema Created At | Timestamp |

**Quick Actions (Platform Admin only):**
- "Run Schema Health Check" → triggers async schema health scan → shows inline progress spinner → results refresh tab on completion
- "View in Database Dashboard" → deep-link to C-11 pre-filtered to this schema
- "Force Vacuum" → 2FA-gated → triggers manual VACUUM ANALYZE on this tenant's schema → queued as Celery job

**Data Flow:**
- Tab content loaded lazily on tab click via `GET /engineering/tenants/?part=drawer-schema&tenant_id={id}`
- Schema size and connection count: live from PostgreSQL information_schema + PgBouncer stats API
- Results cached 5 min per tenant; "Refresh" button available for fresh pull

**Role-Based Behavior:**
- Platform Admin: Quick Actions available
- DBA / DevOps: View only; no quick action buttons
- Backend / Security: Read only; connection count and migration version visible

**Edge Cases:**
- Schema not yet created (tenant in Provisioning state) → show provisioning progress bar instead of schema fields
- Schema creation failed (Celery job errored) → show red error banner with error message and "Retry Provisioning" button (Admin only)
- Pending migrations > 0 → amber warning with count and link to C-12

---

#### Tab 3 — Usage

**Purpose:** Consumption metrics for the tenant against their plan limits.

**Metrics displayed:**

| Metric | Current | Limit | Bar |
|---|---|---|---|
| Student Seats Used | 4,200 | 5,000 | Blue progress bar (84%) |
| Staff Accounts | 18 | 50 | Blue |
| Storage Used (GB) | 12.4 | 20 | Blue (amber > 80%) |
| API Calls This Month | 184,000 | 250,000 | Blue (amber > 80%) |
| Exam Submissions (30d) | 24,600 | Unlimited | Informational |
| Questions in Bank | 8,200 | 10,000 | Blue |
| Active Courses | 42 | 100 | Blue |
| Monthly Emails Sent | 3,200 | 5,000 | Blue |
| SMS Sent (30d) | 400 | 1,000 | Blue |
| WhatsApp Messages (30d) | 600 | 2,000 | Blue |

**Bar Colour Rules:**
- < 80% → blue
- 80–94% → amber (with tooltip "Approaching limit")
- ≥ 95% → red (with tooltip "Near limit — upgrade recommended")
- 100% → red pulsing (with "Limit reached" banner)

**Usage Trend Charts:**
- Line chart: Student count over last 6 months
- Line chart: API calls over last 30 days (daily buckets)
- Bar chart: Exam submissions per month (last 6 months)

**Data Flow:**
- Usage data: per-tenant Memcached counters + daily S3 aggregated snapshots
- Charts: pre-computed JSON from Celery daily aggregation job
- Tab loads via `GET /engineering/tenants/?part=drawer-usage&tenant_id={id}`
- Refresh interval: 10 min (poll guard active when drawer open)

**Quick Actions (Admin only):**
- "Override Limit" → opens mini-form to set temporary limit override (requires 2FA + expiry date)
- "Export Usage Report" → generates CSV/PDF → background job → download link in notification bell

**Edge Cases:**
- Any metric at 100% → red banner at top of tab: "Storage limit reached. Tenant uploads blocked. Upgrade required."
- Usage data not yet available for new tenants (provisioned < 24h) → greyed out metrics with "Data available after 24 hours"
- Storage overflow: if tenant exceeds quota due to race condition → auto-suspend file upload endpoint for that tenant; admin notified

---

#### Tab 4 — Audit

**Purpose:** Immutable, tamper-proof log of every platform admin action performed on this tenant.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | ISO 8601 with timezone |
| Actor | Platform Admin name + email + IP address |
| Action | Human-readable action label |
| Before State | JSON snapshot (collapsible) |
| After State | JSON snapshot (collapsible) |
| 2FA Verified | ✅ / ❌ badge |
| Job ID | Celery job ID for async actions (link to job log) |

**Action Types logged:**
- Tenant provisioned
- Config field changed (field name · old value → new value)
- Plan upgraded / downgraded
- Tenant suspended
- Tenant reinstated
- Soft-delete initiated (30-day grace started)
- Hard delete executed
- Emergency data wipe initiated
- Emergency data wipe completed
- Impersonation session started
- Impersonation session ended
- Limit override applied
- Schema health check run
- Force vacuum triggered

**Pagination:** 25 entries per page · newest first

**Filters:** Action type · Date range · Actor

**Export:** "Export Audit Log" → CSV download (Admin + Security roles only)

**Data Flow:**
- Audit log stored in `platform_audit_log` table (shared schema, immutable — no UPDATE/DELETE allowed via application layer)
- Loaded via `GET /engineering/tenants/?part=drawer-audit&tenant_id={id}&page={n}`
- Cannot be cleared, modified, or hidden by any platform role including Platform Admin

**Role-Based Behavior:**
- All roles with page access can view audit tab
- Export button visible to Platform Admin and Security Engineer only

**Edge Cases:**
- Audit log for a wiped tenant: log entries retained even after data wipe (CERT-In compliance requirement)
- Very old tenants (pre-2022): may have incomplete audit entries — shown with disclaimer banner

---

### Section 6 — Provision New Tenant Modal

**Purpose:** Guided 4-step wizard to provision a brand-new tenant on the platform.

**Trigger:** "Provision New Tenant" button (Platform Admin only)
**Modal Size:** 680px wide · step-indicator at top · 2FA required on final step

---

#### Step 1 of 4 — Institution Details

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Institution Name | Text | Required · 3–120 chars · unique |
| Institution Type | Select | Required: School / College / Institution Group / Coaching Center |
| Primary Admin Email | Email | Required · unique · real email format |
| Primary Admin Name | Text | Required · 2–100 chars |
| Region | Select | Required: North/South/East/West/Northeast/Central |
| Time Zone | Select | Default: Asia/Kolkata |
| Language Default | Select | Default: en |
| Phone (optional) | Phone | E.164 format |

**Inline validations:**
- Institution name uniqueness: async check on blur
- Admin email uniqueness: async check on blur (cannot share email with existing staff/admin)

---

#### Step 2 of 4 — Subdomain & Domain

**Fields:**

| Field | Type | Validation |
|---|---|---|
| Subdomain | Text | Required · auto-suggested from institution name (slugified) · 3–63 chars · lowercase alphanumeric + hyphens · unique |
| Custom Domain (optional) | Text | Valid FQDN format · DNS verification required after provisioning |
| Custom Domain SSL | Toggle | Auto Let's Encrypt once DNS verified |

**Subdomain preview:** Shows live preview URL as user types → `https://{subdomain}.platform.in`
**Conflict check:** Real-time async check; red inline error if taken; suggest alternatives

---

#### Step 3 of 4 — Plan & Limits

**Fields:**

| Field | Type |
|---|---|
| Subscription Plan | Select (Free / Starter / Growth / Enterprise / Custom) |
| Plan Start Date | Date picker |
| Plan End Date | Date picker (blank = no expiry) |
| Billing Contact Email | Email |
| GST Number (optional) | Text (15-char GSTIN format validation) |
| Notes / Internal Reference | Textarea (internal — not shown to tenant) |

**Plan limits preview:** When plan selected → shows read-only limits table (seats · storage · API quota · email quota)
**Custom plan:** If "Custom" selected → additional fields for each limit appear (number inputs)

---

#### Step 4 of 4 — Review & Confirm (2FA-gated)

**Review screen:**
- Summary card with all details entered in Steps 1–3
- Checklist of what will be created:
  - ✅ PostgreSQL schema: `tenant_{id}_{slug}`
  - ✅ Django migration run on new schema
  - ✅ Admin account created + welcome email queued
  - ✅ Subdomain DNS record registered
  - ✅ Cloudflare WAF rule applied for new subdomain
  - ✅ Memcached keys initialised for plan limits
  - ✅ S3 prefix created: `tenants/{id}/`
  - ✅ Plan limits written to platform config

**2FA prompt:** TOTP input field. On valid TOTP → "Provision Tenant" button activates.

**Provision action:**
- Submits `POST /api/tenants/provision/`
- Modal transitions to provisioning progress view (Section 7)
- Modal stays open showing progress; user must not be blocked from other work while waiting

---

### Section 7 — Provisioning Progress Tracker

**Purpose:** Real-time progress display while Celery async provisioning job runs (SLA: 15–25 minutes).

**Trigger:** Immediately after Step 4 confirm in provision modal

**UI Components:**
- Step-by-step progress stepper (8 steps)
- Per-step: ✅ Done · ⏳ In Progress (spinner) · ⬜ Pending · ❌ Failed
- Elapsed time counter
- Estimated time remaining (based on average of last 10 provisioning jobs)
- Live log output (last 5 log lines, auto-scrolling, truncated)
- "Keep working — we'll notify you when done" dismiss option

**Provisioning Steps:**

| Step | Label | Typical Duration |
|---|---|---|
| 1 | Create PostgreSQL schema | 2–5s |
| 2 | Run Django migrations (2,051st schema) | 45–90s |
| 3 | Seed default data (plans · roles · config) | 10–20s |
| 4 | Create admin account + send welcome email | 5–10s |
| 5 | Register subdomain in DNS / Cloudflare | 10–20s |
| 6 | Apply WAF rules for subdomain | 5–10s |
| 7 | Initialise Memcached keys + plan limits | 2–5s |
| 8 | Create S3 prefix + default assets | 3–8s |

**Data Flow:**
- Progress polled via `GET /engineering/tenants/?part=progress&job_id={id}` every 5s
- Poll guard: continues even if drawer-open (provisioning is critical; must not miss failure)
- Backend: Celery job publishes step status to Memcached key `provision:job:{id}:status`
- On completion: modal shows success state with "View New Tenant" button
- On failure: modal shows failed step with error message + "Retry from failed step" button (Admin only)

**Notification on dismiss:**
- If user dismisses modal during provisioning → in-app notification bell shows job progress
- On completion: notification bell alert + email to triggering admin

**Error recovery:**
- If step 2 (migrations) fails → "Retry Provisioning" button → restarts from step 2 (idempotent)
- If step 5 (DNS) fails → provisioning marked partial-success; admin notified; DNS can be registered manually
- If any step fails → Celery marks job `FAILURE` → audit log entry created with failure details

---

### Section 8 — Suspend / Reinstate Flow

**Purpose:** Put a tenant portal into read-only mode (suspend) without data loss, or reverse the suspension.

**Trigger:** "Suspend" in ⋮ quick-action menu or tenant detail drawer

**Suspend Modal:**
- Warning banner: "Suspending this tenant will immediately lock out all students, teachers, and institution admins. The portal becomes read-only. Exam in progress will be paused."
- Shows count of current active sessions: "147 users currently online"
- Reason field (required — select from: Payment overdue · Terms violation · Legal hold · Admin request · Security investigation · Other)
- Notes field (internal — min 20 chars)
- Custom message to institution admin (optional — sent via email)
- Suspension duration: Indefinite (default) · 7 days · 30 days · 90 days (auto-reinstate on expiry)
- 2FA input field
- "Confirm Suspend" button

**On suspend:**
- `POST /api/tenants/{id}/suspend/` with reason + notes + duration
- Memcached key `tenant:{id}:status` set to `suspended` immediately → all portal requests return 503 with suspension message
- Active exam submissions: graceful pause (current answers saved; exam timer paused)
- Active admin sessions for that tenant: terminated within 30s (session invalidated via Memcached)
- Institution primary admin: email notification with reason + "Contact support" link
- Audit log entry created

**Reinstate Flow:**
- "Reinstate" in ⋮ menu → confirmation modal (no 2FA required for reinstate, but reason field required)
- On reinstate: Memcached key cleared → portal active within 30s → institution admin email notification

**Edge Cases:**
- Attempt to suspend a tenant currently in provisioning state: blocked with "Cannot suspend while provisioning is in progress"
- Exam in progress at time of suspension: exam auto-submits current answers after 60s grace period; students shown "Exam interrupted" message
- Suspension during scheduled exam window: system warns admin with alert "This tenant has exams scheduled in 2 hours. Confirm suspend?"
- Auto-reinstate on expiry: Celery beat task checks suspended tenants every hour; reinstates on expiry; audit log entry

---

### Section 9 — Soft Delete & Hard Delete Flow

**Purpose:** Initiate and execute controlled tenant deletion with 30-day recovery grace period.

**Trigger:** "Delete" in ⋮ menu — requires 2FA

**Soft Delete (initiation):**
- Modal with triple-confirmation:
  1. Checkbox: "I understand this will begin the 30-day deletion grace period"
  2. Checkbox: "I confirm this institution has consented to deletion (DPDPA Article 8)"
  3. Type institution name in text field to confirm
- 2FA input
- "Begin Deletion" button

**On soft delete initiation:**
- Tenant status → `pending_deletion`
- Portal suspended immediately (same as suspend flow)
- 30-day grace timer begins → stored as `delete_at` timestamp
- All institution-level backups created: S3 snapshot of schema + media files
- Institution primary admin: certified email with deletion timeline and "Cancel deletion" link (valid 28 days)
- Daily: automated email to institution admin with countdown (30, 14, 7, 3, 1 day)
- Audit log entry

**Cancel during grace period:**
- "Cancel Deletion" button visible in tenant list (Admin) and in institution admin's email link
- On cancel → status returns to `suspended` → admin must manually reinstate

**Hard Delete (at grace period end or forced):**
- Automatically triggered by Celery beat at `delete_at` timestamp
- Or: Admin can force hard delete before grace ends (requires a second 2FA + reason "Force early deletion — legal/compliance requirement")
- Actions on hard delete:
  - PostgreSQL schema: `DROP SCHEMA tenant_{id} CASCADE`
  - S3 prefix: `aws s3 rm s3://bucket/tenants/{id}/ --recursive`
  - Memcached keys for tenant: cleared (django.core.cache delete_many with tenant prefix)
  - Platform_tenants row: status → `deleted` (soft row retained for audit trail)
  - Cloudflare WAF rule for subdomain: removed
  - DNS record: removed
  - All active sessions (if any): terminated
  - Celery jobs for tenant: purged
  - Audit log entry: created (retained permanently per CERT-In requirement)

**Edge Cases:**
- Hard delete of a tenant with pending financial disputes: blocked — red banner "Open billing dispute. Resolve in Billing before deletion."
- Hard delete of a tenant with CERT-In incident open: blocked — amber banner "Active security incident. Security Engineer must clear before deletion."
- Admin email to institution bounces: system flags admin email as bounced; sends to secondary contact if available; else records failed delivery in audit log

---

### Section 10 — Emergency Data Wipe

**Purpose:** DPDPA Article 8 / court order compliance: complete data erasure beyond normal deletion.

**Access:** Platform Admin only · Level 5 · Requires dual-admin approval

**Trigger:** "Emergency Data Wipe" — only available in tenant detail drawer Config tab for tenants already in `deleted` status OR via special emergency workflow

**Dual-Admin Approval:**
- Initiating admin submits wipe request with legal justification (court order number / DPA instruction reference)
- Second platform admin receives email notification with approve/deny link (valid 4 hours)
- Both admins must complete 2FA
- If second admin not available within 4h: escalation email to all Level 5 admins

**What wipe does beyond hard delete:**
- S3 Glacier archives for this tenant: deletion markers set
- All backup snapshots: deleted (RDS snapshot deleted, S3 backup prefix deleted)
- Audit log entries: PII fields anonymised (actor names redacted to "anonymised_admin"), action types retained
- DPDPA erasure certificate: auto-generated PDF with all deletion timestamps, stored in compliance S3 prefix (retained 7 years)
- CERT-In notification: if wipe is breach-related, 6-hour notification timer starts

**Post-wipe:**
- Tenant status → `wiped`
- Row in `platform_tenants` retained with all PII fields nullified: name → "[DELETED]", email → "[DELETED]", schema → "[DELETED]"
- Wipe completion email to both approving admins + compliance officer email

---

### Section 11 — Tenant Impersonation

**Purpose:** Allow Platform Admin to view any tenant's portal exactly as the institution admin sees it — for debugging, support, and QA.

**Access:** Platform Admin only · 2FA-gated · 30-minute auto-expiry

**Trigger:** "Impersonate Admin" in ⋮ menu or tenant drawer Config tab

**2FA gate:** TOTP input required → reason field (min 30 chars) required

**On impersonation start:**
- Platform creates a scoped session token with `impersonation: true` flag + `expires_at: +30min` + `impersonating_tenant_id`
- Opens new browser tab with tenant portal: `https://{subdomain}.platform.in/admin/`
- Impersonation banner displayed permanently at top of tenant portal (cannot be hidden): "⚠ Impersonation session — Platform Admin: {name} — Ends in {timer}"
- All actions performed during impersonation: logged under impersonating admin's identity in tenant audit log + platform audit log

**Restrictions during impersonation:**
- Cannot access billing or payment data within tenant portal
- Cannot trigger exams or publish results
- Cannot modify student PII
- Cannot export student data
- Read-only access to most tenant sections (same as view-only mode)

**Auto-expiry:**
- At 30 min: session token invalidated server-side → browser tab shows "Impersonation session expired" banner → redirect to tenant login page
- Celery beat task checks expired impersonation sessions every 30s

**Audit log entry includes:** Start time · end time · all page URLs visited (captured via middleware) · reason entered · tenant impersonated

---

## 5. User Flow

### Flow A — Provision New Tenant

1. Platform Admin lands on `/engineering/tenants/`
2. Sees KPI strip (2,050 tenants · 2,041 active · 3 suspended)
3. Clicks "Provision New Tenant"
4. Modal Step 1: fills institution name "St. Xavier's College", type "College", admin email
5. Modal Step 2: subdomain auto-suggested "st-xaviers-college" → confirmed
6. Modal Step 3: selects "Growth" plan, billing email entered
7. Modal Step 4: reviews summary · enters TOTP · clicks "Provision Tenant"
8. Progress tracker shows 8-step provisioning (completes in ~18 min)
9. On success: "View New Tenant" button → drawer opens for new tenant
10. Tenant list refreshes → St. Xavier's College visible with "Active" status

### Flow B — Suspend a Tenant for Payment

1. Admin searches "Sunrise" → finds "Sunrise Academy" (Growth plan, 3,200 students)
2. Clicks ⋮ → "Suspend"
3. Modal shows: 42 users currently online · reason select "Payment overdue"
4. Types internal notes · sets 30-day duration · enters TOTP
5. Confirms → portal suspended immediately
6. Audit log entry created · institution admin receives email
7. After 30 days: Celery auto-reinstates · admin notified

### Flow C — Read-Only Engineer Investigating

1. DevOps engineer logs in, navigates to `/engineering/tenants/`
2. No "Provision" button visible; read-only notice shown
3. Searches for tenant "Navdeep Public School"
4. Clicks row → drawer opens in read-only mode (Config · Schema · Usage · Audit)
5. Reviews Schema tab: sees 2 pending migrations, links to C-12
6. All action menu items in drawer show only "View" — no edit/suspend/delete

---

## 6. Component Structure (Logical)

```
TenantManagerPage
├── PageHeader
│   ├── PageTitle (with TenantCountBadge)
│   ├── ProvisionButton (Admin only)
│   └── RefreshButton
├── KPIStrip
│   ├── KPICard × 6 (Total · Active · Suspended · Provisioning · SchemaErrors · NewThisMonth)
│   └── KPISparklinesLayer
├── SearchFilterBar
│   ├── SearchInput (debounced 300ms)
│   ├── TypeFilter
│   ├── PlanFilter
│   ├── StatusFilter
│   ├── RegionFilter
│   ├── DateRangeFilter
│   ├── SortDropdown
│   └── ActiveFilterChips
├── TenantTable
│   ├── TableHeader (sortable columns)
│   ├── TableBody (virtual scroll, 100 rows/page)
│   │   └── TenantRow × N
│   │       ├── BulkCheckbox (Admin only)
│   │       ├── InstitutionCell (logo + name + subdomain)
│   │       ├── TypeCell
│   │       ├── PlanBadge
│   │       ├── StatusBadge
│   │       ├── StudentCount
│   │       ├── AdminEmail
│   │       ├── ProvisionedDate
│   │       └── QuickActionMenu
│   └── BulkActionToolbar (appears on selection)
├── TenantDetailDrawer (720px)
│   ├── DrawerHeader (tenant name + status badge + close)
│   ├── DrawerTabs
│   │   ├── ConfigTab
│   │   ├── SchemaTab
│   │   ├── UsageTab
│   │   └── AuditTab
│   └── DrawerFooter (action buttons per role)
├── ProvisionModal (4-step wizard)
│   ├── StepIndicator
│   ├── Step1_InstitutionDetails
│   ├── Step2_SubdomainDomain
│   ├── Step3_PlanLimits
│   ├── Step4_ReviewConfirm (2FA gate)
│   └── ProvisioningProgressView
├── SuspendModal
├── SoftDeleteModal
├── EmergencyWipeModal (dual-admin)
└── ImpersonationLauncher
```

---

## 7. Data Model (High-Level)

### platform_tenants (shared schema)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| name | VARCHAR(120) | unique |
| institution_type | ENUM | school/college/group/coaching |
| subdomain | VARCHAR(63) | unique · lowercase |
| custom_domain | VARCHAR(255) | nullable |
| admin_email | VARCHAR(255) | unique |
| admin_name | VARCHAR(100) | |
| plan | ENUM | free/starter/growth/enterprise/custom |
| plan_start | DATE | |
| plan_end | DATE | nullable |
| region | ENUM | north/south/east/west/northeast/central |
| timezone | VARCHAR(50) | default Asia/Kolkata |
| default_language | CHAR(5) | BCP 47 |
| schema_name | VARCHAR(80) | unique · immutable after creation |
| status | ENUM | active/suspended/provisioning/pending_deletion/deleted/wiped |
| suspended_reason | VARCHAR(100) | nullable |
| suspended_at | TIMESTAMPTZ | nullable |
| suspended_until | TIMESTAMPTZ | nullable |
| delete_at | TIMESTAMPTZ | nullable (soft delete expiry) |
| provisioned_at | TIMESTAMPTZ | |
| provisioned_by | UUID FK → platform_staff | |
| notes | TEXT | internal |
| gstin | CHAR(15) | nullable |
| billing_email | VARCHAR(255) | |
| logo_url | VARCHAR(512) | nullable |
| max_seats | INTEGER | plan-derived |
| storage_quota_gb | INTEGER | plan-derived |

### platform_provisioning_jobs

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| tenant_id | UUID FK | |
| status | ENUM | queued/running/success/failed/partial |
| celery_task_id | VARCHAR(255) | |
| initiated_by | UUID FK → platform_staff | |
| initiated_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| current_step | INTEGER | 1–8 |
| step_statuses | JSONB | `{1: done, 2: in_progress, 3: pending…}` |
| error_message | TEXT | nullable |
| retry_count | SMALLINT | default 0 |

### platform_audit_log (immutable)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| tenant_id | UUID FK | |
| actor_id | UUID FK → platform_staff | |
| actor_ip | INET | |
| action | VARCHAR(100) | enum-like string |
| before_state | JSONB | nullable |
| after_state | JSONB | nullable |
| twofa_verified | BOOLEAN | |
| job_id | UUID | nullable (for async actions) |
| created_at | TIMESTAMPTZ | immutable · no UPDATE allowed |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| Institution name | 3–120 chars · unique across platform · no special chars except `.,'-&()` |
| Subdomain | 3–63 chars · lowercase alphanumeric + hyphens · cannot start/end with hyphen · unique |
| Admin email | Valid RFC 5322 · unique across platform_tenants + platform_staff |
| GSTIN | Exactly 15 chars · regex: `^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$` |
| Custom domain | Valid FQDN · no IP addresses · no wildcard |
| Plan downgrade | Current student count ≤ target plan seat limit |
| Suspension notes | Min 20 chars |
| Suspension reason | Must select from enum list · no free text for reason field |
| Provision 2FA | Valid TOTP within ±30s window · max 3 attempts before lockout |
| Hard delete | Must enter exact institution name in confirmation field |
| Emergency wipe | Requires second admin approval + legal justification field (min 50 chars) |
| Impersonation reason | Min 30 chars |
| Limit override | Expiry date required · cannot exceed 180 days |

---

## 9. Security Considerations

| Control | Implementation |
|---|---|
| 2FA on all destructive ops | TOTP validated server-side via `pyotp`; must pass within current 30s window; max 3 attempts |
| Audit log immutability | `platform_audit_log` has DB-level trigger preventing UPDATE/DELETE; application layer enforces INSERT-only |
| Role enforcement | All endpoints check `request.user.role == PLATFORM_ADMIN` server-side; role stored in signed JWT; re-checked on every request |
| Impersonation isolation | Impersonation tokens scoped to single tenant; cannot escalate to platform level from within impersonation session |
| Hard delete DPDPA | Erasure certificate generated and retained per DPDPA Article 8; copy held in compliance S3 prefix with lifecycle policy (7 years) |
| CERT-In breach link | Emergency wipe triggering CERT-In 6h countdown: automated incident creation in C-18 |
| Schema DROP guard | `DROP SCHEMA` executed only via Celery worker with dedicated DB role having DROP permission; application DB role cannot DROP schemas |
| IP logging | Actor IP logged on every audit entry; if IP changes mid-session → re-authentication required |
| Bulk action rate limit | Maximum 50 tenants in a single bulk operation; larger batches rejected with error |
| Secret access | DB credentials for schema operations fetched from AWS Secrets Manager at job runtime; never stored in app environment |
| SSRF prevention | Custom domain input validated against internal IP ranges; `169.254.0.0/16`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` blocked |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Celery worker down during provisioning | Celery retry with exponential backoff (3 retries); after 3 failures: alert to DevOps via C-18 incident; partial schema cleaned up |
| Subdomain conflict race condition | DB unique constraint as final guard; optimistic lock check done in application layer first; if constraint violation: return 409 with "Subdomain taken" |
| PostgreSQL schema limit | PostgreSQL has no hard schema count limit; however, monitoring alert set at 2,500 schemas (amber) and 2,800 (red) to give time for DB capacity planning |
| Network partition during hard delete | S3 deletion is idempotent; schema drop confirmed via subsequent query; Memcached key cleanup is best-effort (Celery retry); audit log entry marked `partial_delete` if any step incomplete |
| Admin email domain MX failure | SES delivery tracked; if welcome email bounces → amber flag on tenant row; notification to Platform Admin |
| Concurrent suspension + deletion | DB-level row lock on `platform_tenants` during status change; second operation returns 409 "Another operation is in progress" |
| Large tenant deletion (> 500GB schema) | Hard delete uses `DROP SCHEMA ... CASCADE` inside a Celery job; Celery timeout extended to 2h for large schemas; admin notified of extended duration |
| GST number change | Triggers notification to billing team; GST change requires approval from Finance division (Div D) |
| PgBouncer pool exhaustion during provisioning | New tenant's schema connections reserved only after step 6 completes; PgBouncer pool not impacted during provisioning |
| Tenant count badge race (cache vs DB) | Memcached cache invalidated on every tenant status change; if cache miss: DB query used with Memcached repopulation |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 2,050-tenant table render | Server-side pagination (100/page) + virtual scroll in browser; never load all 2,050 rows to DOM |
| KPI strip freshness | Memcached (django.core.cache) with 60s TTL; Celery beat refreshes every 55s to prevent cache miss |
| Student count per tenant | Async load after table render; cached 24h per tenant; stale indicator if > 24h |
| Search across 2,050 tenants | `pg_trgm` trigram GIN indexes on searchable columns; search < 50ms P99 |
| Provisioning throughput | Celery worker concurrency = 10; can provision 10 tenants simultaneously; each takes 15–25 min; throughput = ~25 new tenants/hour |
| Drawer tab lazy loading | Each tab loaded on click via HTMX; reduces initial drawer load to < 100ms |
| Audit log table scale | `platform_audit_log` partitioned by `created_at` (monthly partitions); index on `tenant_id + created_at`; old partitions archived to S3 after 12 months |
| Impersonation session cleanup | Celery beat checks and cleans expired impersonation tokens every 30s; no manual cleanup needed |
| Peak exam day impact | Tenant Manager is internal engineering tool; isolated from exam submission path; no performance dependency on exam load |
| Read-only engineer access | Read queries served from PostgreSQL read replica to offload primary; write operations routed to primary only |

---

## Amendment — G29: Tenant Schema Storage Quota

**Gap addressed:** Platform Admin had no visibility into per-tenant schema storage size or quota thresholds. No alerts existed when a tenant approached storage limits; the first signal was a hard disk-full error affecting all tenants sharing the RDS instance.

### Changes to Tenant List Table (Section 4)

A **Storage** column is added to the tenant list table between "Students" and "Admin Email":

| Column | Description | Width |
|---|---|---|
| Storage | Current schema size · quota · % bar | 130px |

**Bar colour rules:**
- < 70% → green
- 70–90% → amber ("Approaching storage limit")
- > 90% → red ("Near storage limit — upgrade plan")
- 100% → red pulsing + row highlight ("Storage full — uploads blocked")

Storage size sourced from `pg_total_relation_size` (ORM annotation via `select_related` + raw SQL aggregate); cached 5 min per tenant in Memcached.

### Changes to Tenant Detail Drawer (Section 5) — Storage Tab

A fifth tab **Storage** is added to the tenant-detail-drawer after the Audit tab.

**Storage tab displays:**

| Section | Content |
|---|---|
| Quota summary | Current size · quota (GB) · % used · bar with colour coding |
| Top-10 tables by size | Table name · data size · index size · total — sorted by total descending |
| Index sizes | Aggregated index size for tenant's schema |
| Quota editor | GB input field (plan minimum enforced) · Save (2FA-gated) · "Reset to plan default" link |
| Alert config | Daily alert threshold (default 80%) · alert recipient (primary admin email or platform admin email) |
| Per-plan defaults | Starter: 2 GB · Growth: 10 GB · Pro: 25 GB · Enterprise: custom (shown as read-only reference) |

**Quota edit save action:** `PATCH /api/tenants/{id}/storage-quota/` → 2FA challenge → success toast → Memcached cache invalidated for this tenant's storage metric.

### Background Jobs

- **Daily Celery beat task** (`check_tenant_storage_quotas`): runs at 02:00 IST — queries `pg_total_relation_size` for all 2,050 tenant schemas using a single raw SQL batch query (avoids 2,050 individual queries) → writes results to `platform_tenant_storage` table (tenant_id · size_bytes · checked_at) → for each tenant exceeding 80% threshold: sends email alert to platform admin + institution primary admin.
- **Auto read-only at 100%:** If any tenant reaches 100% quota → Celery task marks tenant `storage_full=True` → portal file upload and media storage endpoints return 413 for that tenant → institution admin notified immediately.

### Data Model Addition

**platform_tenant_storage** table (shared schema):

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| tenant_id | UUID FK → platform_tenants | |
| size_bytes | BIGINT | latest measured size |
| quota_bytes | BIGINT | current quota (may differ from plan default if overridden) |
| checked_at | TIMESTAMPTZ | last measurement timestamp |
| alert_sent_at | TIMESTAMPTZ | nullable — last alert sent (prevents duplicate alerts) |
| storage_full | BOOLEAN | default False |
