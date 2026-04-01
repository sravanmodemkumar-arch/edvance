# C-02 — Staff Account Manager

> **Route:** `/engineering/staff/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10, Level 5)
> **Read Access:** Security Engineer (Role 16)
> **File:** `c-02-staff-accounts.md`
> **Priority:** P1
> **Status:** ⬜ Amendment pending — G30 (Staff Escalation Tree)

---

## 1. Page Name & Route

**Page Name:** Staff Account Manager
**Route:** `/engineering/staff/`
**Part-load routes:**
- `/engineering/staff/?part=table` — staff list table
- `/engineering/staff/?part=kpi` — KPI strip
- `/engineering/staff/?part=drawer&staff_id={id}` — staff detail drawer
- `/engineering/staff/?part=create-modal` — new staff account modal
- `/engineering/staff/?part=access-review` — quarterly access review panel

---

## 2. Purpose (Business Objective)

The Staff Account Manager is the single authoritative console for managing all 81 platform staff accounts across 15 divisions. It governs who can log in to the platform's internal engineering and operations dashboards, what roles they carry, and whether their access is current and justified.

This page enforces the principle of least privilege across every level: each staff member gets exactly the access their role demands — no more. Quarterly access reviews enforce this over time as roles evolve. Every account provisioning and permission change is 2FA-gated and audit-logged.

Platform integrity depends on this page: a compromised staff account can affect all 2,050 tenants simultaneously. The Staff Account Manager is therefore treated with the same security rigor as the Tenant Manager.

**Business goals:**
- Provision new staff accounts with correct role assignment from Day 1
- Enforce 2FA for all staff at Level 3 and above
- Detect stale or unused accounts (no login > 90 days) before they become attack vectors
- Run quarterly access reviews to verify every account's continued need
- Provide Security Engineer read access for compliance auditing
- Meet DPDPA staff data handling obligations (staff PII managed within platform boundary)

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Create · Edit · Suspend · Reinstate · Delete · Reset 2FA · Unlock · Assign roles · Run access review |
| Security Engineer (16) | Level 4 — Read | View all accounts · View login history · View audit log · Export for compliance |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Action Bar

**Purpose:** Establish page context and expose primary create action.

**User Interaction:**
- "Create Staff Account" button — opens create modal (Platform Admin only)
- "Run Access Review" button — opens quarterly access review workflow (Admin only)
- Division filter quick-tabs: All · Div A · Div B · Div C … Div O (scrollable horizontal pill tabs)
- Last refreshed timestamp + manual refresh

**UI Components:**
- H1 title "Staff Account Manager" with total staff count badge ("81 accounts")
- Primary CTA: "Create Staff Account" (disabled for Security Engineer)
- Secondary CTA: "Run Access Review" with last-run date tooltip ("Last run: 47 days ago")
- Division filter tabs (horizontal pill scroll)
- Breadcrumb: Engineering → Staff Account Manager

**Data Flow:**
- Page load: `GET /engineering/staff/?part=kpi` + `GET /engineering/staff/?part=table` in parallel
- Staff count badge: Memcached (django.core.cache, key `platform:staff_count`) with 5-min TTL
- Division filter tab click: `GET /engineering/staff/?part=table&division={div}`

**Role-Based Behavior:**
- Platform Admin: all buttons visible and active
- Security Engineer: Create and Access Review buttons hidden; read-only notice shown

**Edge Cases:**
- Staff count drops below expected minimum (< 3 Platform Admins): red badge with alert "Minimum 3 Platform Admin accounts required for dual-approval workflows"
- Access review overdue (> 90 days since last review): amber banner across page header: "Quarterly access review overdue. Last run: {date}."

**Performance Considerations:**
- Staff count (81 accounts) is trivially small; no pagination needed for base table
- Division filter tabs trigger server-side filter via HTMX swap; < 100ms response expected

**Mobile Behavior:**
- Action bar stacks vertically on < 768px
- Division filter tabs scroll horizontally with touch

**Accessibility Notes:**
- Division filter tabs: `role="tablist"` with each tab as `role="tab"` and `aria-selected`
- CTA buttons: descriptive `aria-label`

---

### Section 2 — KPI Strip

**Purpose:** Instant health-of-staff-estate view at page load.

**KPI Cards:**

| Card | Metric | Alert Threshold | Colour |
|---|---|---|---|
| Total Staff | 81 | — | Neutral |
| Active | Count `status = active` | — | Green |
| Suspended | Count `status = suspended` | > 0 | Amber |
| 2FA Not Enrolled | Count `twofa_enrolled = false` AND `level ≥ 3` | > 0 | Red |
| Inactive (90d) | No login in last 90 days | > 0 | Amber |
| Access Review Due | Accounts not reviewed in > 90 days | > 0 | Amber |

**User Interaction:**
- Clicking a KPI card filters the table (Platform Admin only)
- Security Engineer: cards visible but not clickable

**Data Flow:**
- All 6 metrics: single Memcached `get_many` call; fallback to DB if cache miss
- Poll: `part=kpi` every 120s with HTMX poll guard

**Edge Cases:**
- "2FA Not Enrolled" > 0 for Level 4+ staff: escalated to red badge with tooltip "Level 4 staff without 2FA are a critical security risk. Enforce immediately."

---

### Section 3 — Search, Filter & Sort Bar

**Purpose:** Locate specific staff accounts among 81 records (trivially small, but filter pattern maintained for consistency).

**User Interaction:**
- Search: name · email · role title · division
- Filters: Division · Role Level · Status · 2FA Status · Last Login range

**Filter Options:**

| Filter | Values |
|---|---|
| Division | All · Div A through Div O (15 options) |
| Level | Level 1 · 2 · 3 · 4 · 5 |
| Status | Active · Suspended · Pending Setup · Locked |
| 2FA | Enrolled · Not Enrolled · Exempt |
| Last Login | Today · Last 7d · Last 30d · Last 90d · Never · Custom |

**UI Components:**
- Search input with 300ms debounce
- Filter dropdowns (5)
- Active filter chips with × dismiss
- Result count: "Showing 12 of 81 accounts"
- Sort: Name A–Z · Division · Level · Last Login · Created Date

**Data Flow:**
- Filter/search triggers `GET /engineering/staff/?part=table&q={q}&division={d}&level={l}&status={s}`
- URL reflects all active filters (shareable)

**Edge Cases:**
- Search with no results: empty state "No staff accounts match. Check spelling or clear filters."

---

### Section 4 — Staff List Table

**Purpose:** Complete roster of all platform staff with status indicators and quick-action controls.

**User Interaction:**
- Click row → opens staff detail drawer (640px)
- Platform Admin: inline ⋮ menu per row: View · Edit · Suspend · Reinstate · Reset 2FA · Unlock · Delete
- No bulk operations (staff account changes are individually deliberate — no mass operations)

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Avatar | Initials circle (colour per division) | — |
| Name | Full name | ✅ |
| Division | Div label + colour chip | ✅ |
| Role Title | Exact role title from platform-roles.md | ✅ |
| Level | Badge: 1–5 (colour: green L1-2 · blue L3 · amber L4 · red L5) | ✅ |
| Status | Active (green) · Suspended (amber) · Pending Setup (blue) · Locked (red) | ✅ |
| 2FA | ✅ Enrolled · ⚠ Not Enrolled · — Exempt | ✅ |
| Last Login | Relative time ("2h ago" · "3 days ago" · "Never") | ✅ |
| Login Count (30d) | Integer | — |
| Actions | ⋮ menu | — |

**Status Badge Definitions:**
- Active: account in good standing, can log in
- Pending Setup: created but staff has not completed profile + 2FA enrollment
- Locked: too many failed login attempts (auto-locked after 5 failures within 15 min)
- Suspended: manually suspended by Platform Admin

**Row Highlight Rules:**
- Red left border: Locked accounts
- Amber left border: 2FA not enrolled (Level ≥ 3)
- Grey italic text: No login in > 90 days

**Data Flow:**
- Table: `GET /engineering/staff/?part=table`
- 81 rows loaded at once (no pagination needed at this scale)
- Last login: from `platform_staff_sessions` table most recent row per staff
- Login count: Memcached counter (key `staff:{id}:login_count_30d`) reset monthly by Celery beat

**Role-Based Behavior:**
- Platform Admin: ⋮ menu with all actions; row clickable
- Security Engineer: ⋮ menu shows "View" only; row clickable for read-only drawer

**Edge Cases:**
- Account never logged in (Pending Setup > 30 days): amber indicator + ⋮ menu shows "Resend invite"
- Multiple failed logins from different IPs: anomaly flag icon on row with tooltip "Suspicious login pattern. Review in Security Ops."

**Mobile Behavior:**
- Table collapses to card list on < 768px
- Card: Avatar + Name + Role + Status + Last Login

**Accessibility Notes:**
- Level badge has `aria-label="Access level {n}"` for screen readers
- 2FA column cells: descriptive title attribute with full status explanation

---

### Section 5 — Staff Detail Drawer

**Purpose:** Complete profile, access config, login history, and audit log for a single staff account.

**Drawer Width:** 640px
**Trigger:** Row click or "View" in ⋮ menu

**Tabs inside drawer:**

---

#### Tab 1 — Profile & Access

**Purpose:** View and edit staff identity, role assignment, and access level.

**Fields:**

| Field | Type | Editable |
|---|---|---|
| Full Name | Text | ✅ Admin |
| Email Address | Email | ✅ Admin (with uniqueness check) |
| Phone (optional) | Phone | ✅ Admin |
| Division | Select (15 divisions) | ✅ Admin |
| Role Title | Text (from platform-roles.md) | ✅ Admin |
| Access Level | Select (1–5) | ✅ Admin (cannot assign level higher than own) |
| Employment Type | Select: Full-time · Part-time · Contractor · Intern | ✅ Admin |
| Join Date | Date | ✅ Admin |
| Manager | Select (staff lookup) | ✅ Admin |
| Profile Photo | File upload (S3, max 1MB, JPEG/PNG) | ✅ Admin |
| Status | Read-only badge | — |
| Created By | Read-only (Platform Admin name) | — |
| Created At | Read-only timestamp | — |

**Role Assignment Rules:**
- Cannot assign Level 5 (Platform Admin) to more than 5 staff total (system guard)
- Cannot assign a role level higher than the acting admin's own level
- Role change requires 2FA confirmation

**Save:** "Save Changes" → 2FA challenge (for level or role changes only) → `PATCH /api/staff/{id}/` → success toast → drawer config tab refreshes

**Edge Cases:**
- Email change: sends verification email to new address; old email retains access until verification
- Level downgrade (e.g., Level 4 → Level 3): all pages they cannot access at new level become inaccessible immediately (session doesn't need refresh — Memcached permission cache invalidated immediately on role change)
- Attempting to downgrade the last Level 5 admin: blocked with "Cannot downgrade — minimum 3 Level 5 Platform Admin accounts required"

---

#### Tab 2 — Authentication & Security

**Purpose:** Manage 2FA enrollment, SSO link, password reset, and account lock status.

**Sections:**

**2FA Status Panel:**
- Status: Enrolled (green) · Not Enrolled (red) · Exempt (with justification)
- Enrolled date and method (TOTP / Hardware key)
- "Force Re-enrollment" button (Admin) — resets 2FA; staff must re-enroll on next login
- "Mark as Exempt" toggle (Admin · requires written justification in notes field)
- Backup codes: status (generated / not generated) — Admin can trigger "Regenerate backup codes" (requires staff's manual confirmation step)

**SSO Panel (Google Workspace SAML):**
- SSO Status: Linked · Not Linked · SSO Email mismatch
- SSO Email: the Google Workspace email linked to this account
- "Unlink SSO" button (Admin) — forces password login only
- "Re-link SSO" — sends new SSO enrollment link to staff email

**Password Panel:**
- Last password change: timestamp
- "Send password reset link" button → email sent to staff
- Password policy: min 14 chars · 1 uppercase · 1 number · 1 special · no dictionary words · cannot reuse last 10 passwords

**Account Lock Panel:**
- Lock status: Unlocked · Locked (since {time}, reason: too many failed attempts)
- Failed attempt count (last 24h): `{n}/5`
- "Unlock Account" button (Admin · 2FA required for Level 4+ accounts)
- "Lock Account" manual button (Admin · for immediate security response · 2FA required)

**Active Sessions Panel:**
- List of active sessions: IP · device · browser · location (geo-IP) · started at · last active
- "Terminate Session" button per session (Admin only)
- "Terminate All Sessions" button (Admin · 2FA required)

**Data Flow:**
- 2FA status: `platform_staff.twofa_enrolled` + `platform_staff.twofa_method`
- Active sessions: `platform_staff_sessions` table filtered to `status = active` for this staff
- Geo-IP: `django-ipware` + MaxMind GeoLite2 DB

**Edge Cases:**
- Staff attempts login from new country → session flagged; Security Engineer alerted; staff must re-verify via email OTP before session is granted
- 2FA marked Exempt without justification in audit log → Security Engineer compliance alert raised

---

#### Tab 3 — Login History

**Purpose:** Full log of all login attempts for this staff account — successful and failed.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | ISO 8601 with timezone |
| Status | ✅ Success · ❌ Failed · ⚠ Suspicious |
| IP Address | With geo-location (City, Country) |
| Device | Browser + OS (parsed User-Agent) |
| 2FA Result | Passed · Failed · Bypassed (SSO) · Not required |
| Session Duration | For successful logins: how long session lasted |
| Termination Reason | Logout · Timeout · Admin-terminated · Session-expired |

**Filters:** Date range · Status (Success/Failed/Suspicious) · IP address
**Pagination:** 50 entries per page · newest first
**Export:** CSV download (Platform Admin + Security Engineer)

**Suspicious Flag Criteria (auto-flagged):**
- Login from new country (not seen in last 90 days)
- Login at unusual hour for this user (outside their typical ±2h window)
- Login from IP flagged in threat intelligence feed
- Successful login immediately after 4 failed attempts from same IP

**Data Flow:**
- `platform_staff_login_log` table with index on `staff_id + created_at`
- Geo-IP resolved at login time; stored denormalised in log row
- Suspicious flag: set by login middleware based on heuristic rules; cannot be cleared by admin

**Edge Cases:**
- Very old accounts: login history truncated at 12 months (older entries archived to S3 but not shown in UI)
- VPN usage: many entries from different IPs — not automatically flagged; Admin can mark an IP as "Known VPN" to suppress alerts

---

#### Tab 4 — Access Review

**Purpose:** Track the quarterly access review status for this specific account.

**Review Status Indicators:**
- Last reviewed: {date} by {reviewer name}
- Next review due: {date}
- Status: ✅ Justified · ⚠ Review Due · ❌ Not Reviewed (> 90 days)
- Reviewer notes (from last review)

**Review Action (Admin performing review):**
- "Mark as Reviewed — Access Justified" button → requires short note (min 20 chars) → logged
- "Recommend Access Change" → opens mini-form: proposed new level · new role · reason → sent as task to admin team
- "Recommend Suspension" → pre-fills suspension modal

**Review History Table:**
- Columns: Review Date · Reviewer · Decision · Notes
- Last 4 reviews shown (1 year of quarterly history)

**Data Flow:**
- `platform_access_reviews` table: `staff_id · reviewer_id · reviewed_at · decision · notes`
- Review due date: `last_reviewed_at + 90 days`
- Overdue reviews: Celery beat daily task → creates notifications for Platform Admin

---

#### Tab 5 — Audit Log

**Purpose:** Immutable log of all changes made to this staff account.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | ISO 8601 |
| Actor | Platform Admin name + email + IP |
| Action | Human-readable (e.g., "Access level changed: 3 → 4") |
| Before State | JSONB snapshot (collapsible) |
| After State | JSONB snapshot (collapsible) |
| 2FA Verified | ✅ / ❌ |

**Action Types Logged:**
- Account created
- Profile field changed (any field · old → new)
- Role / level changed
- 2FA enrolled / reset / exempted
- Account suspended / reinstated / deleted
- Account locked (auto) / unlocked (admin)
- Session terminated (by admin)
- Password reset triggered
- SSO linked / unlinked
- Access review completed
- Login attempt (success/fail) — separate table; linked from here

**Pagination:** 25 per page · newest first

---

### Section 6 — Create Staff Account Modal

**Purpose:** Provision a new platform staff account in a guided 3-step flow.

**Trigger:** "Create Staff Account" button (Platform Admin only)
**Modal Width:** 620px

---

#### Step 1 of 3 — Identity Details

**Fields:**

| Field | Validation |
|---|---|
| Full Name | Required · 2–100 chars |
| Work Email | Required · valid email · unique · must match Google Workspace domain if SSO enforced |
| Phone (optional) | E.164 format |
| Employment Type | Required: Full-time / Part-time / Contractor / Intern |
| Join Date | Required · date picker |
| Manager | Required · staff lookup autocomplete |
| Profile Photo (optional) | JPEG/PNG · max 1MB |

---

#### Step 2 of 3 — Role & Access

**Fields:**

| Field | Options |
|---|---|
| Division | Select from 15 divisions |
| Role Title | Text input (auto-complete from existing role titles in that division) |
| Access Level | Select: 1 · 2 · 3 · 4 (cannot create Level 5 via this form — Level 5 requires separate emergency flow) |
| 2FA Requirement | Auto-set: Levels 3–5 → Mandatory; Levels 1–2 → Encouraged |
| SSO Login | Toggle: Enable Google Workspace SSO for this account |
| Custom Permissions | Multi-select checklist of specific page-level overrides (rarely used; most access is role-derived) |

**Level 5 Guard:** Attempting to set Level 5 shows modal: "Level 5 (Platform Admin) accounts require a second Platform Admin approval. This account will be created at Level 4 pending approval." Approval request sent to all existing Level 5 admins.

**Access Preview:** When division + level selected → shows read-only table of pages this staff member will have access to (derived from access matrix in div-c-pages-list.md and equivalent for all other divisions)

---

#### Step 3 of 3 — Review & Send Invite

**Review Panel:**
- Summary of all details from Steps 1–2
- Preview of welcome email that will be sent
- Onboarding checklist shown to admin:
  - ✅ Account created
  - ✅ Welcome email sent with temporary password link (valid 48h)
  - ✅ 2FA enrollment required on first login (if Level 3+)
  - ✅ SSO enrollment link sent (if SSO enabled)
  - ✅ Audit log entry created

**"Create Account" button:** No 2FA required for Level 1–3 creation; 2FA required for Level 4 creation

**On creation:**
- `POST /api/staff/` → account created with `status = pending_setup`
- Welcome email sent via SES: contains temporary password reset link (valid 48h) + 2FA enrollment link
- Audit log entry created

**Edge Cases:**
- Welcome email bounces → amber flag on new account row; resend link available in ⋮ menu
- Staff doesn't complete setup in 48h → temporary link expires; admin can "Resend Invite" from ⋮ menu
- Email domain not in Google Workspace org → SSO toggle auto-disabled with inline note

---

### Section 7 — Suspend & Reinstate Flow

**Purpose:** Immediately revoke a staff member's platform access without permanently deleting the account.

**Trigger:** "Suspend" in ⋮ quick-action menu

**Suspend Modal:**
- Warning: "Suspending {name} will immediately terminate all active sessions and block future logins."
- Reason: Required select (Resignation · Leave of absence · Security investigation · Policy violation · Other)
- Notes: Required · min 30 chars
- Duration: Indefinite (default) · 7d · 30d · 90d (auto-reinstate on expiry)
- 2FA: Required for Level 4 accounts; not required for Level 1–3
- "Confirm Suspend" button

**On suspend:**
- `POST /api/staff/{id}/suspend/`
- All active sessions terminated immediately (Memcached session keys deleted)
- AWS SSO session revoked (if SSO linked)
- Status → `suspended`
- Notification: email to staff's manager
- Audit log entry

**Reinstate:** Confirmation modal · reason required · audit log entry · welcome-back email to staff

---

### Section 8 — Delete Staff Account Flow

**Purpose:** Permanently remove a staff account when the person leaves the organisation.

**Two-Phase Delete:**

**Phase 1 — Offboarding Checklist (shown before delete):**
Before deletion, system checks:
- [ ] Active sessions terminated
- [ ] Pending tasks/approvals reassigned
- [ ] Any content owned by this account reassigned (e.g., open incidents in C-18)
- [ ] Access review completed and documented

Any unchecked item blocks deletion until resolved.

**Phase 2 — Confirm Delete:**
- Type staff name to confirm
- Reason field (required · min 30 chars)
- 2FA required for Level 3+

**On delete:**
- Account status → `deleted`; row retained in DB for audit trail (PII fields NOT nullified — retained per employment records requirement, 7 years)
- All sessions terminated
- SSO unlinked
- Audit log entry

**Note:** Staff accounts are NOT hard-deleted at DB level (unlike tenants). The row is soft-deleted with `deleted_at` timestamp. PII retained for employment records under Indian labour law (7 years).

---

### Section 9 — Quarterly Access Review Workflow

**Purpose:** Structured process for Platform Admin to certify that every staff account's access level is still appropriate.

**Trigger:** "Run Access Review" button in page header

**Review Panel Layout (640px right-side panel):**
- Header: "Access Review — Q{n} {year}" with progress counter "12/81 reviewed"
- Progress bar: reviewed count / total
- Filter: Show All · Show Unreviewed · Show Flagged

**Staff Review Cards (one per unreviewed account):**
- Staff name + photo + division + role + level
- Last reviewed date
- Recent activity summary: "Last login: 3 days ago · Login count (30d): 47"
- Risk flags (if any): never logged in · inactive 60d+ · 2FA not enrolled · level changed recently
- Action buttons:
  - ✅ "Justify — No Change Needed" (with required notes field · min 20 chars)
  - ✏ "Modify — Recommend Change" (opens level/role edit form)
  - ⏸ "Flag for Discussion" (adds to flagged list for team review)
  - 🚫 "Recommend Suspension"

**Batch actions:**
- "Mark All Low-Risk as Justified" (for accounts with no flags, active in last 7 days, 2FA enrolled): bulk justify with single note
- Individual cards must be manually reviewed for any flagged account

**Review completion:**
- When 81/81 reviewed: "Complete Review" button appears
- On completion: `POST /api/staff/access-review/complete/` → review record created → next review due date set to +90 days → completion email sent to all Level 5 admins + Security Engineer

**Edge Cases:**
- New staff added mid-review: automatically added to review queue mid-process
- Review interrupted: progress saved; admin can resume later
- Review not completed within 5 days of starting: daily reminder email to admin

---

### Section 10 — Emergency Account Lock

**Purpose:** Instant security response — lock any staff account within seconds from the staff list.

**Trigger:** "Emergency Lock" — available as a top-level action in ⋮ menu (Platform Admin only)

**No confirmation required** for emergency lock (unlike normal suspend — speed is critical)
- One click → account locked immediately
- All sessions terminated within 5s (via Memcached session key deletion + background Celery job)
- AWS SSO session revoked
- Incident automatically created in C-18 with pre-filled description: "Emergency account lock: {staff name} — locked by {admin name} at {time}"
- Security Engineer notified via email + platform alert bell

**Rationale for no 2FA:** In a security emergency (e.g., stolen credentials), requiring 2FA adds critical seconds. Lock first; document later. The action is still logged with actor + timestamp + IP.

**Post-lock resolution:**
- Admin must document reason within 4h in the Security Ops (C-13) incident created
- Unlocking requires 2FA + written reason (standard unlock flow applies)

---

## 5. User Flow

### Flow A — Onboard New Backend Engineer

1. Platform Admin navigates to `/engineering/staff/`
2. Clicks "Create Staff Account"
3. Step 1: Name "Priya Sharma" · email `priya@platform.in` · Full-time · join date today
4. Step 2: Division C · Role "Backend Engineer" · Level 4 · SSO enabled
5. Access preview shows: C-04, C-05, C-09 with Full access; C-01, C-06, C-08, C-17, C-18 read-only
6. Step 3: Review + "Create Account"
7. Welcome email sent · account created with `pending_setup` status
8. Priya logs in → forced 2FA enrollment → completes setup → status → Active

### Flow B — Emergency Lock During Security Incident

1. Security Engineer sees suspicious login pattern for staff member "Ravi Kumar" in C-13
2. Alerts Platform Admin
3. Admin on `/engineering/staff/` — finds Ravi's row (highlighted with suspicious login flag)
4. Clicks ⋮ → "Emergency Lock"
5. Account locked in < 2s · all sessions terminated
6. C-18 incident auto-created · Security Engineer notified
7. Admin documents reason in C-13 within 4h
8. After investigation: Admin unlocks account or initiates deletion

### Flow C — Quarterly Access Review

1. Access review overdue banner appears (> 90 days since last review)
2. Admin clicks "Run Access Review"
3. Review panel shows 81 accounts · 0 reviewed
4. Batches the 60 low-risk active accounts with "Mark All Low-Risk as Justified"
5. Manually reviews 21 flagged accounts (inactive/2FA missing/level changed)
6. 3 accounts recommended for level downgrade → modifications submitted
7. 2 accounts recommended for suspension (inactive > 90 days)
8. All 81 reviewed → "Complete Review" clicked → record saved → next due in 90 days

---

## 6. Component Structure (Logical)

```
StaffAccountManagerPage
├── PageHeader
│   ├── PageTitle (with StaffCountBadge)
│   ├── CreateStaffButton (Admin only)
│   ├── RunAccessReviewButton (Admin only · overdue badge)
│   └── DivisionFilterTabs (All + 15 divisions)
├── KPIStrip
│   └── KPICard × 6
├── SearchFilterBar
│   ├── SearchInput
│   ├── DivisionFilter
│   ├── LevelFilter
│   ├── StatusFilter
│   ├── TwoFAFilter
│   ├── LastLoginFilter
│   └── ActiveFilterChips
├── StaffTable
│   ├── TableHeader (sortable)
│   └── StaffRow × 81
│       ├── AvatarCell
│       ├── NameCell
│       ├── DivisionChip
│       ├── RoleTitleCell
│       ├── LevelBadge
│       ├── StatusBadge
│       ├── TwoFAIndicator
│       ├── LastLoginCell
│       └── QuickActionMenu
├── StaffDetailDrawer (640px)
│   ├── DrawerHeader
│   └── DrawerTabs
│       ├── ProfileAccessTab
│       ├── AuthSecurityTab
│       ├── LoginHistoryTab
│       ├── AccessReviewTab
│       └── AuditLogTab
├── CreateStaffModal (3-step)
│   ├── Step1_Identity
│   ├── Step2_RoleAccess (with AccessPreviewTable)
│   └── Step3_ReviewInvite
├── SuspendModal
├── DeleteModal (with OffboardingChecklist)
├── AccessReviewPanel (right-side 640px)
│   ├── ReviewProgress
│   └── StaffReviewCard × N
└── EmergencyLockHandler (no modal — direct action)
```

---

## 7. Data Model (High-Level)

### platform_staff

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| full_name | VARCHAR(100) | |
| email | VARCHAR(255) | unique |
| phone | VARCHAR(20) | nullable |
| division | VARCHAR(10) | Div A–O |
| role_title | VARCHAR(150) | |
| access_level | SMALLINT | 1–5 |
| employment_type | ENUM | full_time/part_time/contractor/intern |
| join_date | DATE | |
| manager_id | UUID FK → self | nullable |
| photo_url | VARCHAR(512) | nullable |
| status | ENUM | active/suspended/pending_setup/locked/deleted |
| twofa_enrolled | BOOLEAN | default false |
| twofa_method | ENUM | totp/hardware_key/exempt/null |
| twofa_enrolled_at | TIMESTAMPTZ | nullable |
| sso_email | VARCHAR(255) | nullable (Google Workspace) |
| sso_linked | BOOLEAN | default false |
| failed_login_count | SMALLINT | reset after successful login |
| locked_at | TIMESTAMPTZ | nullable |
| last_login_at | TIMESTAMPTZ | nullable |
| suspended_at | TIMESTAMPTZ | nullable |
| suspended_until | TIMESTAMPTZ | nullable |
| deleted_at | TIMESTAMPTZ | nullable (soft delete) |
| created_by | UUID FK → self | Platform Admin who created |
| created_at | TIMESTAMPTZ | |

### platform_staff_sessions

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| staff_id | UUID FK | |
| session_token | VARCHAR(255) | hashed (SHA-256) |
| ip_address | INET | |
| user_agent | TEXT | |
| country | CHAR(2) | ISO 3166-1 alpha-2 |
| city | VARCHAR(100) | nullable |
| started_at | TIMESTAMPTZ | |
| last_active_at | TIMESTAMPTZ | |
| ended_at | TIMESTAMPTZ | nullable |
| termination_reason | ENUM | logout/timeout/admin_terminated/expired/locked |
| is_suspicious | BOOLEAN | default false |

### platform_access_reviews

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| staff_id | UUID FK | |
| reviewer_id | UUID FK → platform_staff | |
| review_cycle | VARCHAR(20) | e.g., "Q1-2026" |
| reviewed_at | TIMESTAMPTZ | |
| decision | ENUM | justified/modify/flag/suspend |
| notes | TEXT | min 20 chars |
| recommended_level | SMALLINT | nullable (if decision = modify) |

---

## 8. Validation Rules

| Field | Rule |
|---|---|
| Full name | 2–100 chars · letters, spaces, hyphens, apostrophes only |
| Work email | Valid RFC 5322 · unique across platform_staff · unique across platform_tenants admin_emails |
| Access level | 1–5 · cannot create Level 5 via standard flow · cannot assign higher than own level |
| Password (staff-set) | Min 14 chars · 1 uppercase · 1 number · 1 special · not in common password list · not matching last 10 |
| 2FA exemption | Requires written justification in notes (min 50 chars) · Level 4–5 cannot be exempted |
| Suspension notes | Min 30 chars |
| Delete confirmation | Must type exact full name of staff being deleted |
| Access review notes | Min 20 chars per reviewed account |
| Level 4 account creation | Requires 2FA from acting admin |
| Level 5 creation | Requires second Level 5 admin approval (separate approval workflow) |
| Manager field | Cannot assign self as manager |
| Employment type + join date | Join date cannot be in future for active accounts |

---

## 9. Security Considerations

| Control | Implementation |
|---|---|
| 2FA mandatory for Level 3+ | Enforced at login middleware; 2FA status checked on every authenticated request; if `twofa_enrolled = false` and `level ≥ 3` → redirect to forced enrollment before any page access |
| Session isolation | Each session has unique token; stored as hashed SHA-256 in DB; original token only lives in httponly cookie |
| Max Level 5 accounts | System guard: max 5 Level 5 accounts at any time; hard-blocked at DB trigger level |
| Minimum Level 5 count | Minimum 3 Level 5 accounts at all times (needed for dual-approval workflows); deletion blocked if would go below 3 |
| Emergency lock audit | Despite no 2FA on emergency lock, actor + IP + timestamp recorded; reason must be filed within 4h |
| Suspicious login detection | Login middleware checks country, time-of-day, IP reputation; flags logged; Security Engineer alerted |
| SSO token validation | SAML assertions validated against Google Workspace certificates; assertion replay prevented with `NotOnOrAfter` check |
| Access review overdue enforcement | After 90 days without review: amber banners; after 120 days: Level 5 admins emailed daily until review runs |
| Deleted account retention | Soft delete only; PII retained 7 years per Indian labour law; DB-level guard prevents hard delete of staff rows |
| Audit log immutability | Same `platform_audit_log` table as tenant manager; INSERT-only; no UPDATE/DELETE via application |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Only 1 Level 5 admin remaining | Deletion and suspension of that admin blocked; system requires bringing total to ≥ 3 before any Level 5 modifications |
| Staff with open incident assignments deleted | Deletion blocked; "Reassign 3 open incidents before deletion" checklist item shown with links |
| Google Workspace user suspended externally | SSO token invalidated by Google; staff cannot log in via SSO; platform account not automatically suspended; Security Engineer alerted to review |
| Concurrent login from 2 different countries | Flag raised; second session (from new country) prompted for email OTP before granted; both locations shown in active sessions panel |
| Access review in progress when new staff added | New account automatically appears in review queue; review counter updates to reflect new total |
| Staff changes email mid-review | New email verification required; account status → pending_verification; access unaffected during verification |
| 2FA backup code used | Logged as "2FA method: backup code"; Security Engineer notified; staff prompted to generate fresh backup codes |
| Celery beat access-review-overdue task fails | Manual fallback: Platform Admin can check `platform_access_reviews` last entry date from page header |
| Division renamed in platform-roles.md | Staff accounts retain old division string; admin must manually re-assign via batch edit (no auto-migration) |
| Contractor account after contract end | No automatic expiry; Manager responsible for notifying Platform Admin; system sends reminder email to manager 14 days before join_date + (employment type: contractor assumed 12-month term) |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 81 staff accounts | Trivially small; all rows loaded at once (no virtual scroll needed); no pagination in table |
| Login history query | Index on `staff_id + created_at`; 12-month rolling window; older data archived to S3 |
| Session check on every request | Sessions cached in Memcached with 15-min TTL; DB query only on cache miss; session check < 2ms P99 |
| Access review batch | 81 accounts processed in single DB query; all review cards rendered server-side; no lazy load needed |
| Geo-IP lookup | MaxMind GeoLite2 loaded into memory at worker startup; lookup < 0.5ms per login |
| Staff count badge | Memcached (django.core.cache) key `platform:staff_count`; TTL 5 min; invalidated on any account create/delete |
| Audit log query | Partition by month; index on `staff_id + created_at`; page load < 100ms for 25 entries |
| Emergency lock latency | Memcached session key deletion: < 5ms; worker picks up session invalidation within 1s; full lock propagation < 5s |
| SSO token validation | SAML cert cached in memory (24h); validation < 3ms per login request |
| Platform growth | If staff count grows beyond 200: add server-side pagination (25/page); access review workflow supports 500+ accounts without redesign (card-based) |

---

## Amendment — G30: Staff Escalation Tree

**Gap addressed:** On-call escalation chains for P0 Exam Day, Security Breach, Data Breach-DPDPA, and DB Emergency incidents existed only in a shared document outside the platform. "Out of Office" status was never reflected, leading to calls to unavailable engineers during incidents.

### New Tab — Escalation Tree (in Staff Detail Drawer → cross-account view, and as standalone section)

A sixth tab **Escalation Tree** is added to the Staff Account Manager page as a full-section panel (not inside the per-staff drawer — it covers all chains across the team).

**Accessed via:** "Escalation Trees" button in the page header action bar (visible to Platform Admin and Security Engineer).

**Panel layout (720px right-side panel):**

**5 Escalation Chains:**

| Chain | Trigger Scenario |
|---|---|
| P0 Exam Day | 74K exam submission degradation / complete outage during live exam |
| P1 Service Degradation | Non-exam-hour API latency / partial service degradation |
| Security Breach | Suspected or confirmed compromise of credentials, WAF bypass, or data exfiltration |
| Data Breach — DPDPA | Confirmed student PII exposure triggering 72h DPDPA notification obligation |
| DB Emergency | PostgreSQL primary down / replication failure / schema corruption |

**Per chain, the escalation tree shows:**

| Position | Fields |
|---|---|
| Primary on-call | Staff name · role · phone (Signal / WhatsApp / phone call) · email · OOO status |
| Secondary | Same fields |
| Tech Lead | Same fields |
| CTO / DPO | (CTO for P0/P1/DB; DPO for Security Breach/Data Breach) · same contact fields |

**OOO Toggle:** Each person in the tree has an "Out of Office" toggle (self-managed via their own profile, or toggled by Platform Admin). When OOO = true:
- That position shows amber "OOO" badge
- The escalation tree auto-shows the next available contact with a note "Primary unavailable — escalate to Secondary"
- The chain summary shows "Chain reachable: Yes / Partial / No" based on OOO coverage

**Send Test Alert:** Button per chain → fires a test notification (email + WhatsApp API call) to all non-OOO members in the chain → result shown inline: "✅ 3/4 contacts reached · ❌ 1/4 failed (phone unreachable)" → last-tested timestamp updated.

**Last tested timestamp:** Shown per chain with colour coding: green (< 30 days) · amber (30–60 days) · red (> 60 days). Monthly testing recommended.

**Integration with C-18:** When a P0 incident is created in C-18, the platform auto-triggers the corresponding escalation chain notification (configurable: P0 Exam Day chain auto-fires on any `severity = P0` incident with `category = exam-day`).

### Data Model Addition

**platform_escalation_chains** table (shared schema):

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| chain_type | ENUM | p0_exam_day / p1_degradation / security_breach / data_breach / db_emergency |
| position | SMALLINT | 1 = Primary · 2 = Secondary · 3 = Tech Lead · 4 = CTO/DPO |
| staff_id | UUID FK → platform_staff | |
| signal_number | VARCHAR(20) | nullable |
| whatsapp_number | VARCHAR(20) | nullable |
| is_ooo | BOOLEAN | default false |
| ooo_until | TIMESTAMPTZ | nullable |
| last_test_sent_at | TIMESTAMPTZ | nullable |
| last_test_result | JSONB | nullable — `{email: ok, whatsapp: failed}` |
| updated_by | UUID FK → platform_staff | |
| updated_at | TIMESTAMPTZ | |
