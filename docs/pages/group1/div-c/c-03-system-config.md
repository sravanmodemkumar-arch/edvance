# C-03 — System Configuration

> **Route:** `/engineering/system-config/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10, Level 5) · DevOps/SRE (Role 14, Level 4)
> **Read Access:** Security Engineer (Role 16)
> **File:** `c-03-system-config.md`
> **Priority:** P1
> **Status:** ✅ Spec done — no amendment required

---

## 1. Page Name & Route

**Page Name:** System Configuration
**Route:** `/engineering/system-config/`
**Part-load routes:**
- `/engineering/system-config/?part=kpi` — system health KPI strip
- `/engineering/system-config/?part=section&key={section}` — individual config section panel
- `/engineering/system-config/?part=maintenance-status` — maintenance mode status bar
- `/engineering/system-config/?part=audit` — recent changes audit feed
- `/engineering/system-config/?part=kill-switch-panel` — emergency kill switch panel

---

## 2. Purpose (Business Objective)

System Configuration is the master control panel for all global platform-wide settings. Changes here propagate instantly to all 2,050 institution portals simultaneously — there is no "save draft" or "preview" stage before changes go live. This is the highest-blast-radius configuration page in the entire platform after the Tenant Manager.

A maintenance mode toggle from this page locks out every student, teacher, and institution admin across all 2,050 tenants within 30 seconds. A misconfigured session timeout can log out 74,000 concurrent exam takers mid-submission. A wrong CORS origin can break the entire API for all mobile clients.

Accordingly, every configuration change is: 2FA-gated (for destructive settings) · staged for 60-second review before activation · written to an immutable audit log · instantly reversible via a "Revert Last Change" action.

**Business goals:**
- Provide Platform Admin and DevOps a single pane for all global settings
- Enable instant maintenance mode for scheduled downtime without deployment
- Control all platform-wide security posture settings from one place
- Allow emergency kill switches for specific platform features without code changes
- Prevent accidental misconfiguration through staged-change review and revert capability

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Read + Edit all sections · Maintenance mode toggle · Kill switches · Emergency overrides |
| DevOps / SRE (14) | Level 4 | Read + Edit: AWS/infra-related sections only (Rate limits · Memcached TTLs · CORS · Session timeouts) · Cannot touch maintenance mode or kill switches |
| Security Engineer (16) | Level 4 — Read | View all sections · View audit log · Cannot edit |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & System Status Bar

**Purpose:** Immediate visibility into whether the platform is in a special operating mode (maintenance, degraded, emergency).

**System Status Banner (always visible at top of page):**

| State | Banner Colour | Text |
|---|---|---|
| Normal | Green | "All systems operational — 2,050 tenants live" |
| Maintenance Scheduled | Amber | "Scheduled maintenance: {date} {time} — {n} tenants affected" |
| Maintenance Active | Red pulsing | "⚠ MAINTENANCE MODE ACTIVE — All portals suspended since {time}" |
| Degraded | Amber | "Platform degraded — {service name} issues detected. See C-08." |
| Emergency | Red | "🚨 EMERGENCY MODE — Kill switch active: {feature name}" |

**Page Header:**
- H1 "System Configuration"
- Last updated timestamp: "Last change: 14 min ago by Arjun Mehta (Platform Admin)"
- "Revert Last Change" button (visible only if last change < 24h and no dependent changes since)
- "View Full Audit Log" link

**Role-Based Behavior:**
- Platform Admin: all controls visible
- DevOps: maintenance mode banner read-only; restricted section controls only
- Security Engineer: entire page read-only; no edit controls shown

**Edge Cases:**
- Multiple admins editing system config simultaneously: optimistic lock warning "Another admin edited this section 2 min ago. Your view may be stale. Refresh before saving."
- Config service unreachable: amber banner "Config service unavailable — showing last cached values. Changes cannot be saved."

---

### Section 2 — KPI Strip — System Health

**Purpose:** At-a-glance confirmation that the current system configuration is producing healthy outcomes.

**KPI Cards:**

| Card | Metric | Source | Alert |
|---|---|---|---|
| Active Tenants | Tenants with live portals | Memcached | < 2,040 = amber |
| Session Error Rate | Failed auth sessions / total (last 5 min) | CloudWatch | > 0.1% = red |
| API Error Rate (5xx) | 5xx rate across all Lambda | CloudWatch | > 0.5% = amber |
| Cache Hit Rate | Memcached hit / (hit+miss) ratio | ElastiCache metrics | < 85% = amber |
| Rate Limit Hits (5min) | Count of 429 responses | CloudWatch | > 100 = amber |
| Last Config Change | Time since last configuration change | Audit log | — |

**Data Flow:**
- KPI strip: `GET /engineering/system-config/?part=kpi` — 30s HTMX poll
- All metrics from CloudWatch Metrics API + ElastiCache Memcached stats
- Cached in Memcached 30s to avoid hammering CloudWatch API

---

### Section 3 — Maintenance Mode

**Purpose:** Instantly suspend all 2,050 institution portals for planned downtime or emergency.

**UI Layout:**
- Dedicated card at top of page body (above all other sections)
- Large toggle switch: OFF (green) / ON (red pulsing)
- Current status: "Maintenance mode: OFF — Last activated: 12 Jan 2026 02:00"
- Countdown timer (if scheduled): "Next scheduled maintenance: 3 days 4 hours"

**Toggle ON — Maintenance Mode Activation:**

Step 1 — Configure maintenance window (inline form on toggle click):
- Maintenance message to show on portals (textarea · pre-filled with default: "We're performing scheduled maintenance. We'll be back shortly.")
- Custom message per language (expandable: Hindi, Telugu, Tamil, Kannada, Urdu)
- Estimated duration: dropdown (15 min · 30 min · 1h · 2h · 4h · Custom)
- Scope: All tenants (default) · Select specific tenants (multi-select, for partial maintenance)
- Notify institution admins: Toggle (if ON → sends email to all affected primary admin emails via SES bulk send)
- Schedule for later: Toggle (if ON → date-time picker; if OFF → activates immediately)

Step 2 — 2FA confirmation (Platform Admin only; DevOps cannot activate maintenance mode):
- TOTP input
- Confirm button: "Activate Maintenance Mode"

**On activation:**
- Memcached key `platform:maintenance_mode` set to `{active: true, message: "...", activated_at: ..., activated_by: ...}` via django.core.cache
- All tenant portal requests → 503 response with maintenance page (served from CloudFront edge)
- Active exam submissions: graceful pause (current answers saved, timer paused)
- System status bar → red pulsing
- Audit log entry
- All in-progress API requests: allowed to complete (60s drain window) before 503 kicks in
- If notify enabled: SES bulk email to all institution admin emails within 5 min

**Toggle OFF — Deactivation:**
- Single-click (no 2FA required for deactivation — speed matters on recovery)
- Confirmation modal: "Deactivate maintenance mode? This will restore access to all {n} tenant portals."
- On confirm: Memcached key deleted → portals live within 30s
- Paused exams: timer resumes automatically; students shown "Maintenance complete — your exam has resumed"
- Audit log entry

**Partial Maintenance (specific tenants):**
- Only selected tenants suspended; others continue operating
- Useful for schema migrations on a subset of tenants
- Selected tenants shown in amber list on maintenance card: "3 tenants in maintenance"

**Edge Cases:**
- Attempt to activate maintenance during active live exam (> 1,000 concurrent submissions): red warning modal "74 exams currently in progress. Activating maintenance will pause them. Are you sure? Type CONFIRM to proceed."
- Maintenance accidentally left active > 4h: automated alert to all Level 5 admins + DevOps lead
- Scheduled maintenance window passes without deactivation: Celery beat sends reminder every 30 min

---

### Section 4 — Session & Authentication Settings

**Purpose:** Control platform-wide session behaviour and authentication policies.

**Settings in this section:**

| Setting | Default | Min | Max | Who Can Edit |
|---|---|---|---|---|
| Session timeout — Level 1-2 (minutes) | 480 (8h) | 30 | 1440 | Admin · DevOps |
| Session timeout — Level 3-4 (minutes) | 240 (4h) | 15 | 480 | Admin · DevOps |
| Session timeout — Level 5 (minutes) | 60 (1h) | 15 | 120 | Admin only |
| Student session timeout (minutes) | 720 (12h) | 60 | 1440 | Admin · DevOps |
| Student exam session timeout (minutes) | 240 | 60 | 480 | Admin · DevOps |
| Max concurrent sessions per staff | 3 | 1 | 10 | Admin · DevOps |
| Max concurrent sessions per student | 2 | 1 | 5 | Admin · DevOps |
| Failed login lockout threshold | 5 | 3 | 10 | Admin only |
| Failed login lockout duration (minutes) | 30 | 5 | 1440 | Admin only |
| Password expiry (days) — staff | 90 | 30 | 365 | Admin only |
| Require 2FA for Level | ≥ 3 | 1 | 5 | Admin only |
| JWT access token TTL (minutes) | 15 | 5 | 60 | Admin · DevOps |
| JWT refresh token TTL (days) | 7 | 1 | 30 | Admin · DevOps |
| Remember-me max duration (days) | 30 | 7 | 90 | Admin · DevOps |

**Save behaviour:**
- Inline "Save" button per section (not a global save — each section saves independently)
- Save for session timeouts: 60-second staged review panel (see Section 12)
- Save for lockout settings, 2FA level, JWT TTL: 2FA confirmation required

**Impact preview:**
- When session timeout field is changed: inline calculation shows "At this setting, a student who started an exam at 09:00 would be timed out at {time}. Exam sessions run up to 3h — consider setting ≥ 180 min."

**Edge Cases:**
- Setting student exam session timeout < exam max duration: red inline warning "This setting is shorter than the maximum configured exam duration (3h). Students may be logged out mid-exam."
- Reducing JWT access token TTL below 5 min: warning "Very short TTL increases API requests significantly. Verify Lambda throttle limits can handle increased token refresh rate."

---

### Section 5 — Global Rate Limits

**Purpose:** Platform-wide API rate limiting defaults — the floor that plan-level limits in Div B (04-plan-config) cannot go below.

**Settings Table:**

| Endpoint Category | Default Limit (req/min) | Max Configurable | Who Can Edit |
|---|---|---|---|
| General API (per tenant) | 500 | 5,000 | Admin · DevOps |
| Exam submit endpoint | 2,000 | 10,000 | Admin · DevOps |
| Auth endpoints (login/refresh) | 60 | 500 | Admin only |
| File upload endpoints | 30 | 200 | Admin · DevOps |
| Bulk data export endpoints | 10 | 100 | Admin · DevOps |
| Admin dashboard APIs | 300 | 2,000 | Admin · DevOps |
| Public content API (unauthenticated) | 100 | 1,000 | Admin · DevOps |
| Webhook delivery endpoints | 200 | 2,000 | Admin · DevOps |
| AI pipeline endpoints (internal) | 50 | 500 | Admin only |
| Platform engineering APIs (this div) | 1,000 | 5,000 | Admin only |

**Per-setting controls:**
- Current value input (number)
- Sparkline: 429 (rate-limit-hit) count over last 24h for that category
- "View in API Health Monitor" link (→ C-04 filtered to that category)

**Burst allowance setting:** Global burst multiplier (1x–3x, default 1.5x) applied to all limits for burst windows up to 30s

**Save:** Requires 2FA from Admin; DevOps can save without 2FA for their editable rows

**Edge Cases:**
- Lowering exam submit rate below current peak: red warning "Current peak on exam days is {n} req/min. Setting below this will throttle exam submissions."
- Auth endpoint rate limit lowered significantly: warning "This may block legitimate users during high-traffic login windows (exam day start)."

---

### Section 6 — CORS & Allowed Origins

**Purpose:** Control which origins can make cross-origin requests to the platform API.

**Origins List:**

| Origin | Type | Status | Added By | Added At |
|---|---|---|---|---|
| `https://*.platform.in` | Wildcard subdomain | ✅ Active | System | Provisioned |
| `https://admin.platform.in` | Exact | ✅ Active | System | Provisioned |
| `https://app.platform.in` | Exact | ✅ Active | System | Provisioned |
| Custom domain patterns | Per-tenant | Auto-added on custom domain verification | System | |

**Add Origin:**
- Text input + "Add" button
- Validation: must be valid HTTPS URL; HTTP blocked; IP addresses blocked; internal ranges blocked
- Requires 2FA (Admin only; DevOps cannot add CORS origins)

**Remove Origin:**
- Inline "Remove" button per row
- Confirmation modal: "Removing this origin will break all API requests from {origin}. Confirm?"
- 2FA required

**Wildcard rules:**
- `*.platform.in` allowed (tenant subdomains)
- `*` (global wildcard) is permanently blocked; cannot be added by any role
- Double-wildcard patterns blocked

**Data Flow:**
- CORS origins stored in `platform_system_config` table key `cors_allowed_origins` as JSONB array
- On save: Memcached key `platform:cors_origins` updated immediately (django.core.cache); Django CORS middleware reads from Memcached on each request
- Propagation: < 5s across all Lambda instances

**Edge Cases:**
- Adding origin that matches an existing wildcard: inline note "This origin is already covered by {existing wildcard rule}"
- Removing a wildcard that covers active tenant custom domains: warning lists affected tenant domains

---

### Section 7 — AWS SES Email Configuration

**Purpose:** Configure the platform's email sending identity, bounce handling, and per-category sending limits.

**Settings:**

| Setting | Value |
|---|---|
| Primary sender email | `noreply@platform.in` |
| Primary sender name | "MockTest Platform" |
| Bounce handling email | `bounces@platform.in` (SES feedback loop) |
| Complaint handling email | `complaints@platform.in` |
| SES sending region | ap-south-1 (Mumbai) |
| Daily send quota | Configured per SES account (shown read-only; increase via AWS console) |
| Sending rate (emails/sec) | SES account limit (shown read-only) |

**Email Category Controls:**

| Category | Template | Daily Limit | Status |
|---|---|---|---|
| Transactional (OTP, receipts) | System-managed | Unlimited (within SES quota) | ✅ |
| Welcome / Onboarding | System-managed | 2,050/day | ✅ |
| Exam notifications | Tenant-triggered | 500K/day | ✅ |
| Suspension notices | Admin-triggered | 500/day | ✅ |
| Marketing / Announcements | Div B Announcement Manager | 50K/day | ✅ |

**Bounce Rate Display:**
- Current bounce rate: {%} (SES suspends sending if > 5%)
- Complaint rate: {%} (SES suspends if > 0.1%)
- Amber alert at bounce rate > 3%; Red at > 4.5%

**DKIM / SPF Status:**
- DKIM: Verified ✅ / Not Verified ❌
- SPF: Verified ✅ / Not Verified ❌
- DMARC: Configured ✅ / Not Configured ❌
- Each shows last-verified date; "Re-verify" button available

**Edit controls:**
- Admin only for all SES settings
- DevOps: read-only view

---

### Section 8 — Memcached Cache Configuration

**Purpose:** Control Memcached (django.core.cache) TTL defaults across the platform.

**TTL Settings Table:**

| Cache Key Pattern | Default TTL | Min TTL | Max TTL | Who Can Edit |
|---|---|---|---|---|
| Tenant list snapshot | 120s | 30s | 600s | Admin · DevOps |
| Tenant status per tenant | 30s | 5s | 300s | Admin · DevOps |
| User session | 900s (15m) | 300s | 3600s | Admin · DevOps |
| Permission set per user | 30s | 10s | 120s | Admin only |
| API response cache (general) | 60s | 0 (disable) | 3600s | Admin · DevOps |
| Exam question set per tenant | 300s | 60s | 1800s | Admin · DevOps |
| Rate limit counter window | 60s | 10s | 300s | Admin · DevOps |
| KPI strip values | 60s | 15s | 300s | Admin · DevOps |
| Feature flag values | 30s | 5s | 120s | Admin only |
| AI pipeline result cache | 600s | 60s | 3600s | Admin only |

**Memcached cluster health (read-only display in this section):**
- ElastiCache Memcached cluster: node count + status badges (all green / degraded)
- Memory usage per node: MB used / MB total
- Hit rate: last 5 min (from ElastiCache CloudWatch metrics)
- Link: "View full details in C-08 Infrastructure Monitor"

**Save:** Each row has individual save; TTL changes take effect for new writes immediately; existing cached keys expire at their original TTL (Memcached does not support per-key TTL update on existing entries)

**Flush controls (Platform Admin only · 2FA required):**
- "Flush all caches" → `cache.clear()` via django.core.cache — clears all Memcached keys across the cluster
- "Flush session caches" → 2FA required + confirmation "This will log out all {n} active users" → targeted flush via `cache.delete_many(session_keys)` where session keys are tracked in `platform_active_sessions` table
- "Flush permission caches" → deletes permission cache keys from tracked permission key registry → immediate re-evaluation of all user permissions (use after bulk role changes)

**Edge Cases:**
- Setting permission cache TTL > 120s: amber warning "Permission changes will take up to {TTL}s to propagate. Recommended: ≤ 30s."
- Memcached cluster in degraded state when admin tries to save TTL: warning "Memcached unavailable. TTL change saved to DB but will not take effect until cache recovers."

---

### Section 9 — Feature Flag Master Override

**Purpose:** Emergency master switch for any platform feature, bypassing the per-tenant Feature Flag Manager (Div B, page 02).

**Layout:**
- Two-column layout: left = active feature flags list; right = master override controls

**Master Override Table:**

| Feature Area | Current State | Master Override | Override Set By | Override Expiry |
|---|---|---|---|---|
| AI MCQ Generation | Enabled | — | — | — |
| Exam Live Mode | Enabled | — | — | — |
| WhatsApp Notifications | Enabled | — | — | — |
| Parent Portal | Enabled | — | — | — |
| Custom Domains | Enabled | — | — | — |
| Mobile App API | Enabled | — | — | — |
| Razorpay Payments | Enabled | — | — | — |
| Result Publishing | Enabled | — | — | — |
| Student Import | Enabled | — | — | — |
| Bulk Export | Enabled | — | — | — |

**Override Actions (Admin only · 2FA required):**
- "Force OFF — All Tenants": disables feature for all 2,050 tenants regardless of their Feature Flag Manager settings
- "Force ON — All Tenants": enables feature for all tenants regardless
- "Clear Override": removes the master override; tenant-level settings resume control
- Override expiry: optional date-time (auto-clears on expiry via Celery beat)

**Override badge on Feature Flag Manager (Div B page 02):**
- When a master override is active, a red/amber badge appears on the feature in the Div B Feature Flag Manager: "Master override active — set in System Config"

**Audit:** Every override change logged with reason field (required · min 30 chars)

**Edge Cases:**
- Force-OFF of "Exam Live Mode" when exams in progress: red warning "74 exams currently live. Force-disabling exam mode will end all submissions immediately. Type CONFIRM."
- Override expiry passes while on-call engineer is handling incident: Celery sends 15-min warning before expiry; engineer can extend from C-18 incident page

---

### Section 10 — Emergency Kill Switches

**Purpose:** Nuclear options for platform-wide emergency response — disable entire service categories instantly.

**Access:** Platform Admin only · Dual-admin approval required (same as Emergency Data Wipe in C-01)

**Kill Switch Panel (distinct visual area — red border):**

| Kill Switch | Effect | Recovery |
|---|---|---|
| Suspend All New Tenant Registrations | Blocks `POST /api/tenants/provision/` | Manual re-enable |
| Suspend All Payment Processing | Blocks all Razorpay API calls; queues transactions | Manual re-enable |
| Suspend All External API Calls | Blocks SMS/WhatsApp/email sending · AI API · Webhook delivery | Manual re-enable |
| Suspend All File Uploads | Blocks `PUT /api/upload/*` across all tenants | Manual re-enable |
| Suspend All Student Logins (new) | Blocks new student sessions; existing sessions unaffected | Manual re-enable |
| Suspend All Exam Starts (new) | Blocks new exam sessions; in-progress exams continue | Manual re-enable |
| Read-Only Mode — All Tenants | All POST/PUT/PATCH/DELETE → 503; GET still works | Manual re-enable |
| Full Maintenance Mode | Same as Maintenance Mode toggle above (Section 3) | Manual re-enable |

**Activation flow:**
- Initiating admin clicks kill switch → selects reason from list + free text (min 50 chars)
- System sends approval request to all other Level 5 admins (email + platform alert)
- Second admin approves within 15 min (or initiating admin can override with double-TOTP)
- On activation: Memcached key `platform:kill_switch:{name}` set (django.core.cache); all Lambda functions read this key on cold start and warm invocation (cached 5s locally in Lambda)
- C-18 incident auto-created

**Active kill switches banner:**
- When any kill switch is active: red banner across ALL engineering pages (not just System Config): "🚨 Kill switch active: {name} — Active since {time} — Set by {admin}"

**Deactivation:**
- Single admin can deactivate (no dual approval needed for recovery — speed matters)
- No 2FA required for deactivation
- Audit log entry required

---

### Section 11 — Recent Changes Audit Feed

**Purpose:** Live feed of the last 20 configuration changes — quick reference for "what changed recently."

**Layout:** Right-side panel (or bottom of page on wide screens)
**Refresh:** Every 60s via HTMX poll

**Feed Entry Format:**
```
[14 min ago] Arjun Mehta (Admin)
Changed: Session timeout Level 3-4
240 min → 180 min
[View full audit entry]
```

**Feed Entry Colours:**
- Green: setting value increased (relaxed)
- Amber: setting value decreased (tightened)
- Red: kill switch activated · maintenance mode toggled · feature force-disabled

**"View Full Audit Log" link:** → opens full audit log drawer (same structure as staff and tenant audit logs)

**Full Audit Log Drawer:**
- Columns: Timestamp · Actor + IP · Section · Setting key · Before value · After value · 2FA verified
- Filters: Section · Actor · Date range
- Export: CSV (Admin + Security Engineer)
- Immutable: INSERT-only; no modify or delete

---

### Section 12 — Staged Change Review (60-second review window)

**Purpose:** Prevent accidental misconfiguration by introducing a 60-second review window before certain high-impact settings go live.

**Triggered by:** Session timeout changes · JWT TTL changes · Rate limit reductions · CORS origin removals · Feature flag force-OFF

**Review Panel (slides in from bottom — 240px tall):**
- "Pending change — goes live in: 60s" countdown timer
- Change summary: "Session timeout Level 3-4: 240 min → 180 min"
- Impact statement: "This affects {n} currently active sessions. 0 sessions will be terminated (timeout applies to new sessions only)."
- Two buttons: "Apply Now" (skip countdown) · "Cancel Change"
- If countdown reaches 0: change applies automatically

**Data Flow:**
- Pending change stored in Memcached key `platform:pending_config_change:{session_id}` with 90s TTL
- Countdown managed client-side (JS); Memcached key checked server-side on apply
- If admin closes browser during countdown: Memcached TTL expires; change does NOT apply; no partial state

**Edge Cases:**
- Two admins submit conflicting staged changes simultaneously: second change shows warning "Another change for this setting is pending. View it before applying."
- Admin session expires during 60s countdown: change cancelled; re-authentication required; change must be resubmitted

---

## 5. User Flow

### Flow A — Enable Maintenance Mode for Scheduled Migration

1. Platform Admin navigates to `/engineering/system-config/`
2. System status bar: green "All systems operational"
3. Scrolls to Maintenance Mode section — currently OFF
4. Clicks toggle → inline form: types maintenance message in English + Hindi translation
5. Sets duration: 2 hours
6. Scope: All tenants
7. Notify institution admins: ON
8. Schedules for: tomorrow 02:00 IST
9. Enters TOTP → confirms
10. Maintenance scheduled: amber banner "Scheduled maintenance: {tomorrow} 02:00"
11. At 02:00: Celery triggers auto-activation → all portals suspended
12. After migration: DevOps clicks "Deactivate" → portals live within 30s

### Flow B — Emergency Kill Payment Processing

1. Razorpay reports API issue (detected in C-04 API Health Monitor)
2. Platform Admin navigates to System Config → Kill Switches panel
3. Clicks "Suspend All Payment Processing"
4. Types reason: "Razorpay API returning 500s — suspending to prevent double-charge or failed payment data"
5. Approval request sent to second Level 5 admin
6. Second admin approves within 5 min
7. Kill switch activates: all payment endpoints return 503 with "Payments temporarily unavailable"
8. C-18 incident auto-created
9. After Razorpay confirms resolution: Admin clicks "Deactivate" → payments resume

### Flow C — DevOps Adjusting Rate Limits Pre-Exam

1. DevOps opens System Config
2. Navigates to Global Rate Limits section
3. Sees exam submit endpoint: currently 2,000 req/min
4. Checks sparkline: peak on last exam day was 1,800 req/min
5. Decides to increase to 3,000 to give headroom
6. Saves (DevOps can edit this without 2FA)
7. Staged review shows: "Rate limit increase: exam submit 2,000 → 3,000 req/min — applies in 60s"
8. Clicks "Apply Now"
9. Change propagates to all Lambda instances via Memcached within 5s
10. Audit log entry created

---

## 6. Component Structure (Logical)

```
SystemConfigPage
├── SystemStatusBar (always visible, full-width)
├── PageHeader
│   ├── PageTitle
│   ├── LastChangedInfo
│   ├── RevertLastChangeButton
│   └── ViewAuditLogLink
├── KPIStrip (system health metrics)
├── MaintenanceModeCard
│   ├── StatusToggle (large)
│   ├── MaintenanceConfigForm (inline, appears on toggle)
│   ├── ScheduledWindowDisplay
│   └── PartialMaintenanceTenantList
├── ConfigSections (tab-based or accordion)
│   ├── SessionAuthSection
│   ├── RateLimitsSection
│   ├── CORSOriginsSection
│   ├── SESEmailSection
│   ├── MemcachedCacheSection
│   ├── FeatureFlagOverrideSection
│   └── KillSwitchPanel (distinct red-border card)
├── RecentChangesAuditFeed (right sidebar)
├── StagedChangeReviewBar (slides from bottom when pending)
│   ├── CountdownTimer
│   ├── ChangeSummary
│   ├── ImpactStatement
│   └── ApplyNow / Cancel buttons
└── FullAuditLogDrawer (on-demand)
```

---

## 7. Data Model (High-Level)

### platform_system_config

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| config_key | VARCHAR(100) | unique · e.g., `session_timeout_level_3` |
| config_value | JSONB | flexible value type |
| section | VARCHAR(50) | e.g., `session_auth`, `rate_limits`, `cors` |
| updated_at | TIMESTAMPTZ | |
| updated_by | UUID FK → platform_staff | |
| previous_value | JSONB | stored for "revert last change" |
| is_sensitive | BOOLEAN | if true: value masked in audit log before-state |
| requires_twofa | BOOLEAN | |
| requires_staged_review | BOOLEAN | |

### platform_maintenance_windows

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| scheduled_at | TIMESTAMPTZ | nullable (null = immediate) |
| activated_at | TIMESTAMPTZ | nullable |
| deactivated_at | TIMESTAMPTZ | nullable |
| message | JSONB | `{en: "...", hi: "...", te: "..."}` |
| scope | JSONB | `{all: true}` or `{tenant_ids: [...]}` |
| duration_minutes | INTEGER | |
| notify_admins | BOOLEAN | |
| created_by | UUID FK → platform_staff | |

### platform_kill_switch_log

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| switch_key | VARCHAR(100) | |
| action | ENUM | activated/deactivated |
| reason | TEXT | min 50 chars |
| initiated_by | UUID FK → platform_staff | |
| approved_by | UUID FK → platform_staff | nullable |
| activated_at | TIMESTAMPTZ | |
| deactivated_at | TIMESTAMPTZ | nullable |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| Maintenance message | Required · max 500 chars · required in `en` locale minimum |
| CORS origin | Must be HTTPS · valid FQDN · no IP · no internal ranges · no global wildcard `*` |
| Session timeout values | Must respect hierarchy: Level 5 < Level 3-4 < Level 1-2 · student exam timeout < student session timeout |
| Rate limit values | Exam submit limit cannot be set below 500 req/min (hard floor) · Auth endpoint limit cannot be < 30 req/min |
| Memcached TTL | Permission cache TTL: max 120s (enforced) · Session TTL: min 300s (enforced — lower would log users out too aggressively) |
| JWT access token TTL | Min 5 min · Max 60 min · Must be < refresh token TTL |
| Kill switch reason | Min 50 chars · must select from reason category list first |
| Feature flag force-OFF reason | Min 30 chars |
| Staged change cancel | No confirmation needed — cancel is always safe |
| Revert last change | Only available within 24h of last change · blocked if 3+ changes made after the target change |
| Level 5 kill switch | Requires dual-admin approval unless initiating admin uses double-TOTP override (both TOTP codes from same device in 30s window) |

---

## 9. Security Considerations

| Control | Implementation |
|---|---|
| 2FA on destructive settings | Session timeout reduction, rate limit decrease, CORS removal, kill switches, maintenance mode: all require TOTP from Platform Admin |
| DevOps write scope | Role-based field-level access: `platform_staff.access_level = 4` restricts which `config_key` rows are editable; enforced server-side |
| Staged review race condition | Pending change stored in Memcached with actor's session ID; conflict detection if another admin has pending change for same key |
| Kill switch dual approval | Approval token sent via email; valid 15 min; one-time use; stored hashed in DB |
| Config value encryption | `is_sensitive = true` config values stored encrypted (AES-256-GCM) in DB; decrypted in memory only; never logged in plaintext |
| CORS wildcard prevention | `*` as CORS origin is blocked at DB level via CHECK constraint and application validation |
| Audit log immutability | Same INSERT-only `platform_audit_log` policy; platform_system_config `previous_value` column is application-set only; not user-editable |
| Propagation verification | After Memcached key update, backend performs read-after-write to confirm propagation; if mismatch: error returned to admin "Config save failed — verify in audit log" |
| Rate limit floor | Exam submit minimum floor (500 req/min) enforced via DB CHECK constraint; cannot be lowered via API regardless of role |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Memcached unavailable when maintenance mode activated | Fallback: write maintenance state to `platform_system_config` DB table; Lambda functions fall back to DB check every 30s; slight delay in propagation (30s vs 5s) |
| Config change during peak exam traffic | Warning overlay: "74,000 exam submissions in progress. Config changes will take effect within 5s. High-risk changes during peak traffic are discouraged." |
| Both Level 5 admins offline when kill switch needed | Double-TOTP override available: initiating admin enters TOTP twice within 30s window; treated as self-approving; logged as emergency override |
| Staged change window expires while reviewing impact | Automatic apply is intentional (60s is sufficient review); admin who wants to abort must actively click Cancel |
| Feature flag master override conflicts with A/B test | Master override takes absolute precedence; A/B test in Div B shows banner "Master override active — test data may be unreliable" |
| Maintenance mode deactivation fails (Memcached unavailable) | Manual fallback: DBA can update `platform:maintenance_mode` directly in `platform_system_config` DB table; or DevOps redeploys Lambda with env var `MAINTENANCE_OVERRIDE=false` |
| Multiple kill switches active simultaneously | System supports it; each kill switch is an independent Memcached key; active count shown in status bar: "3 kill switches active" |
| SES bounce rate spike during maintenance notification send | SES sending halted above 4.5% bounce rate; notification emails may not all be delivered; admin shown delivery status: "Notifications sent: 1,847/2,050 — 203 failed (SES limit)" |
| Revert last change with multiple dependent changes | Revert blocked if > 2 subsequent changes made; admin must manually identify and undo chain of changes |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Config propagation to 2,050 tenants | All tenant requests read config from Memcached (not DB); Memcached update is single operation; propagation is per-request on next read within TTL window — no broadcast needed |
| Maintenance mode activation latency | Memcached key set: < 5ms; Lambda warm instances pick up on next invocation (< 1s); cold starts: Lambda reads Memcached on init; full propagation: < 30s across all warm Lambda instances |
| Kill switch Lambda propagation | Lambda instances cache kill switch state locally for 5s; worst-case: 5s propagation; acceptable for emergency scenarios |
| Staged change countdown | Countdown timer client-side only (JS); server-side: Memcached key with 90s TTL as guard; no polling during 60s window |
| Config page load | All config values served from `platform_system_config` table (< 100 rows); full page load < 200ms; no heavy joins |
| Audit log scale | Config changes are infrequent (< 50/day); no partition needed; standard index on `section + created_at` sufficient |
| SES bulk notification on maintenance | 2,050 emails queued as Celery task batch (250/task × 9 tasks); delivered within 5 min; SES rate limit respected |
| Memcached flush operations | Full flush uses `cache.clear()` (django.core.cache); targeted session/permission flush uses `cache.delete_many()` with tracked key lists; non-blocking for other operations |
