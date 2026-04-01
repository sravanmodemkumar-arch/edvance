# Page 22 — Test Tenant Manager

**URL:** `/portal/product/test-tenants/`
**Permission:** `product.manage_test_tenants`
**Priority:** P2
**Roles:** QA Engineer, PM Platform, PM Institution Portal, UI/UX Designer

---

## Purpose

Manages isolated test institution accounts (tenants) used for QA testing, feature verification, UI review testing, onboarding simulation, and client demos. Each test tenant is a fully functional institution portal with seeded data, feature flag overrides, and access to the complete platform stack — completely isolated from production data and traffic. Without this page, QA would test in shared environments where one engineer's changes break another's test run.

Core responsibilities:
- Provision new test tenants in under 2 minutes with any combination of institution type, plan tier, and seed data scenario
- Manage tenant lifecycle: Active → Paused → Expired → Deleted
- Configure feature flag overrides per tenant for isolated flag state testing
- Seed realistic test data (students, exams, results, announcements, fee records)
- Share tenant access with internal team members, external clients, and UI reviewers
- Schedule automatic tenant cleanup to prevent stale tenant accumulation (max 50 active at any time)
- Track tenant resource usage (storage, compute costs)
- Save and restore named snapshots for repeatable test scenarios
- Environment selection: test tenants can target Staging, UAT, or Pre-Production

**Scale context:**
- 1,000 schools × avg 1,000 students; 800 colleges × avg 500 students; 100 coaching centres × avg 10,000 students
- Test tenants must be able to simulate all institution types at realistic scale
- Max 50 active test tenants at any time (infrastructure limit)
- Tenant provisioning: target < 2 minutes for small (50 students), < 5 minutes for large (5,000+ students)

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Test Tenant Manager"              [New Tenant]  [Import Config]│
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 5 cards                                            │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Active Tenants · Paused · Expired · Templates · Audit Log      │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 5 Cards

| # | Label | Value | Colour | Click Action |
|---|---|---|---|---|
| 1 | Active Tenants | Count of currently active tenants (max 50) | Amber if > 40 | Opens Active tab |
| 2 | Expiring Soon | Active tenants expiring within 7 days | Amber if > 0 | Filters Active to expiring |
| 3 | Storage Used | Total GB across all active tenants | Amber if > 80% limit | — |
| 4 | Shared Externally | Tenants with active external (client) access links | — | Filters Active |
| 5 | Created This Month | New tenants provisioned this month vs last month | Delta badge | — |

---

## Tab 1 — Active Tenants

### Toolbar

| Control | Options |
|---|---|
| Search | Tenant name or ID |
| Institution Type | All / School / College / Coaching / Group |
| Plan Tier | All / Starter / Standard / Professional / Enterprise |
| Purpose | All / QA Testing / Feature Verification / UI Review / Client Demo / Load Testing / Onboarding Simulation |
| Environment | All / Staging / UAT / Pre-Production |
| Created By | Filter by team member name |
| Expiry window | All / Expiring today / Expiring within 3 days / Expiring within 7 days |

### Tenant Table — 11 columns

| Column | Detail |
|---|---|
| Tenant Name | Descriptive name (e.g. "SSC Coaching — Pro Tier — Mar 26") |
| Institution Type | Badge: School · College · Coaching · Group |
| Plan Tier | Badge: Starter · Standard · Professional · Enterprise |
| Purpose | Badge |
| Environment | Badge |
| Created By | Avatar + name |
| Created On | Date (DD Mon YYYY) |
| Expires | Date + countdown: "5d left" (amber < 3d, red < 24h) |
| Access | "Private" badge · "Shared (X users)" · "External link active" |
| Flag Overrides | Count of active feature flag overrides on this tenant |
| Actions | Open Portal · Configure · Share · Extend · Pause · Delete |

Clicking any row (outside action buttons) → opens Tenant Detail Drawer.

**"Open Portal" action:** Opens tenant's institution portal in new tab, pre-logged-in as the tenant admin user. Most-used action — placed first in the actions column.

**"Extend" action:** Quick-extends expiry by 7 days without opening full drawer.

**Colour coding of Expires column:**
- > 7 days: default muted text
- 3–7 days: amber text
- < 3 days: orange text + clock icon
- < 24 hours: red text + blinking dot

**Pagination:** Showing X–Y of Z tenants · page pills · per-page selector (10 / 25 / 50)

---

## Tab 2 — Paused Tenants

Tenants manually paused. All scheduled background jobs, automated emails, and Celery tasks are suspended. Data fully retained. Institution portal accessible in read-only mode.

**When to pause:** A QA engineer wants to hold a complex test scenario mid-state without the auto-expiry clock deleting it overnight.

**Same table as Active** with these differences:
- "Days Paused" column replaces "Expires" column
- Auto-delete warning shown if paused for > 25 days (full deletion at 30 days)
- Actions: Resume · Delete (no Pause action on already paused tenant)
- "Resume" restores all background tasks and resets expiry to original duration from resume date

---

## Tab 3 — Expired Tenants

Tenants past expiry date. Read-only portal access for 7 days post-expiry, then permanent deletion.

### Expired Tenant Table

Same columns as active, plus:
- **Expired On:** date
- **Data Deletion In:** countdown (red if < 24h)
- Actions: **Reactivate** (extends expiry by 14 days from today) · **Export Data** · **Permanently Delete**

### Permanent Delete Confirmation Modal

- Warning: "This will permanently delete [Tenant Name], all test data (X students, Y exams, Z results), and all access links. This cannot be undone."
- Text confirmation field: type the exact tenant name to confirm
- "Permanently Delete" button (red, enabled only after correct text entered)

---

## Tab 4 — Templates

Pre-configured tenant blueprints for common testing scenarios. Selecting a template auto-fills the New Tenant form and seeds appropriate data. Reduces setup from 15 minutes to under 2 minutes.

### Template Grid (3-column cards)

Each template card shows:
- Template name (bold)
- Institution type + Plan tier badges
- Seed data summary: "X students · Y exams · Z results"
- Purpose badge
- Last used: relative date
- Created by
- Actions: Create Tenant from This Template · Edit · Duplicate

### Complete Template Library

**QA & Testing Templates:**

| Template Name | Type | Tier | Students | Exams | Domains | Purpose |
|---|---|---|---|---|---|---|
| Starter School — Clean | School | Starter | 50 | 5 | SSC | Testing Starter limitations and upgrade prompts |
| Standard College — Mid Size | College | Standard | 200 | 15 | RRB, NEET | Testing Standard feature set |
| Professional Coaching — Full | Coaching | Professional | 1,000 | 50 | SSC, RRB, IBPS | Full Professional feature testing |
| Enterprise Coaching — Max Scale | Coaching | Enterprise | 5,000 | 200 | All 8 domains | Enterprise, API access, custom domain testing |
| Group Admin — Multi Institution | Group | Enterprise | 10,000 (5 child institutions) | 500 | All 8 | Group-level admin and rollup analytics testing |
| New Onboarding — Zero Data | School | Starter | 0 | 0 | None | Onboarding workflow from scratch |
| School — Mid Academic Year | School | Professional | 500 | 40 | AP Board, TS Board | Mid-cycle school testing with attendance history |
| Coaching — SSC Batch Cycle | Coaching | Standard | 2,000 | 100 | SSC | SSC coaching centre typical state |

**Client Demo Templates:**

| Template Name | Type | Tier | Description |
|---|---|---|---|
| Demo — School Showcase | School | Professional | Rich data, multiple batches, strong analytics, active leaderboard |
| Demo — Coaching Empire | Coaching | Enterprise | 3,000 students, all domains, revenue dashboard, AI features enabled |
| Demo — College Group | Group | Enterprise | 3 colleges, group-level reports, 1,500 combined students |

**Load Testing Templates:**

| Template Name | Type | Tier | Students | Purpose |
|---|---|---|---|---|
| Load Base — 5K Students | Coaching | Enterprise | 5,000 | Baseline for load test scenario seeding |
| Load Base — 15K Students | Coaching | Enterprise | 15,000 | Near-maximum coaching centre scale load test |

### Template Edit Drawer (560px)

**Fields:**
- Template name and description
- Institution type and plan tier
- Seed data configuration:
  - Student count (slider: 0–15,000)
  - Exam count (slider: 0–500)
  - Results: generate for all students (score distribution: Normal / Skewed High / Skewed Low / Custom percentile distribution)
  - Announcements: count (0–20)
  - Fee records: generate fee history (Yes/No)
  - Domains to subscribe (multi-select from all 8 domains)
- Feature flag overrides: list of flags to override with their values
- Default expiry duration: 7 / 14 / 30 days
- Default environment: Staging / UAT / Pre-Production

---

## Tenant Detail Drawer (720px)

### Drawer Header
- Tenant name (large) + type badge + plan badge
- Status badge (Active / Paused / Expiring Soon)
- Expiry countdown + "Extend 7 days" quick button
- "Open Portal →" button (opens portal in new tab)
- "Open Admin →" button (opens Django admin for this tenant's data)
- Close (×)

### Drawer Tab 1 — Overview

**4 Stat Cards:**
- Students seeded: count
- Exams: count (draft / scheduled / completed breakdown)
- Storage used: X MB of Y MB limit
- Last accessed: relative time + who accessed

**Configuration Details table:**

| Field | Value |
|---|---|
| Institution Type | School / College / Coaching / Group |
| Plan Tier | Starter / Standard / Professional / Enterprise |
| Purpose | QA Testing / Feature Verification / etc. |
| Environment | Staging / UAT / Pre-Production |
| From Template | Template name or "Custom" |
| Provisioned | Date and time + duration to provision |
| Provisioned By | Admin name |
| Expiry | Date and time |

**Credentials Panel (initially masked):**
- "Show Credentials" button → reveals:
  - Admin username and password
  - Sample student username and password (for testing student-side flows)
  - Portal URL (clickable)
  - Django admin URL

**Domains Subscribed:**
- List of subscribed domains with exam count per domain

---

### Drawer Tab 2 — Feature Flag Overrides

All feature flags for this tenant that differ from production defaults.

**Override Table:**

| Flag Name | Production Default | This Tenant Value | Override Reason | Set By | Override Expires |
|---|---|---|---|---|---|
| enable_webcam_proctoring | false (disabled) | true (enabled) | Testing proctoring E2E flow | Deepa Menon | — (permanent for tenant lifetime) |
| new_result_page_v2 | 5% rollout | 100% (forced on) | UI review of new result page | Priya Sharma | 22 Mar 2026 |
| ai_question_generator | false | true | Enterprise demo for client pitch | Rahul Nair | — |
| mobile_offline_exam | 20% rollout | 0% (forced off) | Testing without offline mode | Arjun Kumar | — |

**"Add Flag Override" form:**
- Feature flag selector: searchable dropdown showing all flags from Feature Flags page (page 02)
- Shows current production rollout % when selected
- Override value: Enabled (100%) / Disabled (0%) / Custom % (slider 0–100)
- Reason (required, max 200 chars)
- Expires: Permanent for tenant lifetime / Custom date

**"Clear All Overrides" button:** Resets tenant to production flag state (with confirmation).

---

### Drawer Tab 3 — Seed Data Management

**Current Data Summary:**

| Entity | Count | Actions |
|---|---|---|
| Students | 1,000 | Add More · Clear All |
| Batches | 8 | Add More |
| Exams | 50 | Add More · Clear Attempts |
| Test Attempts | 24,500 | Clear All Attempts |
| Announcements | 12 | Clear |
| Fee Records | 980 | Clear |

**Seeding Actions:**

| Action | Description | Params |
|---|---|---|
| Add Students | Generate N fake students with realistic Indian names, emails, mobile numbers | Count (1–5,000) · Roll number prefix |
| Seed Exam Attempts | Generate attempts for all students in a specific exam | Score distribution · Completion rate % |
| Seed Fee Records | Generate fee collection history | Amount range · Date range |
| Clear All Attempts | Wipe every test attempt (useful before a clean test run) | Confirmation required |
| Reset to Snapshot | Restore tenant to a saved snapshot state | Select from snapshot list |
| Create Snapshot | Save current full tenant state as a named restore point | Name + description |
| Wipe All Data | Delete all student data, exams, results, announcements | Typed confirmation required |

**Snapshot Management Table:**

| Snapshot Name | Created By | Created On | Description | Student Count | Exam Count | Actions |
|---|---|---|---|---|---|---|
| Baseline — empty | System | Tenant creation | Zero data, clean portal | 0 | 0 | Restore |
| After initial import | Deepa Menon | 15 Mar | 1,000 students imported, no exams | 1,000 | 0 | Restore |
| Pre-exam state | Deepa Menon | 16 Mar | 50 exams scheduled, no attempts yet | 1,000 | 50 | Restore |
| Full exam cycle | Deepa Menon | 18 Mar | All exams complete, results published | 1,000 | 50 | Restore |
| Demo ready | Rahul Nair | 20 Mar | Leaderboard populated, analytics full | 1,000 | 50 | Restore |

Restoring a snapshot: confirmation modal showing "This will replace current tenant data with the selected snapshot. Current data will be lost."

---

### Drawer Tab 4 — Access & Sharing

**Internal Team Access:**

| Name | Role | Access Level | Added By | Added On | Last Accessed | Actions |
|---|---|---|---|---|---|---|
| Deepa Menon | QA Engineer | Admin (creator) | — | — | 2h ago | — |
| Priya Sharma | UI/UX Designer | Read-only | Deepa Menon | 15 Mar | Yesterday | Remove |
| Rahul Nair | PM Portal | Admin | Deepa Menon | 16 Mar | 3h ago | Downgrade · Remove |

**Access Levels:**
- **Admin:** Full drawer access — can configure flags, seed data, manage access, extend expiry
- **Read-only:** Portal access only — can open and use the institution portal but cannot change configurations in this drawer

**"Add Internal User" form:**
- Email search (searches SRAV team members)
- Access level: Admin / Read-only
- "Add" button

**External Access Links (Client Demo Sharing):**

External links give non-SRAV users (clients, prospects) time-limited access to the tenant's institution portal. They see only the portal — not this management drawer.

| Link | Created By | Created On | Expires | Times Accessed | Last Accessed | Status | Actions |
|---|---|---|---|---|---|---|---|
| Link-A (masked URL) | Rahul Nair | 18 Mar | 25 Mar, 5pm | 4 | Yesterday | Active | Revoke |
| Link-B (masked URL) | Rahul Nair | 15 Mar | 22 Mar, 5pm | 1 | 3 days ago | Expired | Renew |

**"Create External Link" form:**
- Link label (e.g. "Apex Academy Demo — Mar 2026")
- Expiry: 24h / 3 days / 7 days / Custom date
- Optional password protection (shared with client separately)
- Access scope: Full admin + student portal / Admin portal only / Student portal only
- "Generate Link" button → shows generated URL with copy button

**Link security notes:** External links do not expose credentials — they create a session-authenticated access path. Revoking the link immediately invalidates all sessions created via that link.

---

### Drawer Tab 5 — Activity Log

Complete chronological audit of everything that happened to this tenant.

| Timestamp | Action | Performed By | Details |
|---|---|---|---|
| 20 Mar 14:30 | Tenant created | Deepa Menon | From template: "Enterprise Coaching — Max Scale" |
| 20 Mar 14:32 | Provisioning complete | System | 5,000 students, 200 exams seeded in 4m 12s |
| 20 Mar 14:35 | Flag override added | Deepa Menon | enable_webcam_proctoring → true |
| 20 Mar 15:00 | Portal accessed | Deepa Menon | Admin portal login |
| 20 Mar 16:20 | Internal access added | Deepa Menon | Priya Sharma (read-only) |
| 21 Mar 10:00 | Snapshot created | Deepa Menon | "Pre-exam state" snapshot |
| 21 Mar 11:30 | Portal accessed | Priya Sharma | Student portal reviewed (UI check) |
| 22 Mar 09:00 | Seed data: exam attempts | Deepa Menon | Generated results for Exam #12, normal distribution |
| 22 Mar 14:00 | External link created | Rahul Nair | "Apex Academy Demo" link, expires 25 Mar |

---

## New Tenant Modal (4-step wizard)

### Step 1 — Institution Profile

| Field | Options |
|---|---|
| Tenant Name | Required, max 60 chars. Auto-suggest: "[Type] — [Tier] — [Purpose] — [Date]" |
| Institution Type | School · College · Coaching · Group |
| Plan Tier | Starter · Standard · Professional · Enterprise |
| Purpose | QA Testing · Feature Verification · UI Review · Client Demo · Load Testing · Onboarding Simulation |
| Target Environment | Staging · UAT · Pre-Production |

**From template:** Toggle. If on: template selector dropdown (searches templates). Pre-fills all fields below. PM can still override individual fields after selecting template.

---

### Step 2 — Data Configuration

| Field | Options |
|---|---|
| Student Count | Slider 0–15,000. Warning at > 10,000: "Provisioning may take 8–12 minutes" |
| Exam Count | Slider 0–500 |
| Generate Results | Yes / No. If Yes: score distribution selector |
| Score Distribution | Normal (mean 55%) · Skewed High (mean 72%) · Skewed Low (mean 38%) · Custom (enter mean + std dev) |
| Domains to Subscribe | Multi-select: SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI |
| Include Fee Records | Yes / No. If Yes: generates 12 months of fee collection history |
| Include Announcements | Yes / No. If Yes: generates 10 realistic announcements |
| Include Attendance | Yes / No. If Yes: generates 90-day attendance records |

---

### Step 3 — Expiry & Access

| Field | Options |
|---|---|
| Expiry Duration | 7 days · 14 days · 30 days · Custom date |
| Initial Access | Private (creator only) · Share with team (multi-select from team directory) |
| Access Level for Shared | Admin · Read-only |
| Notify on Expiry | Email list (comma-separated, defaults to creator's email) |
| Auto-extend | Yes (extend by 7 days once, if any activity in last 24h) / No |

---

### Step 4 — Review & Create

Full summary of all configuration choices. Shows:
- Institution: Type · Plan · Purpose · Environment
- Data: X students · Y exams · Score distribution
- Expiry: date
- Access: who has access
- Estimated provisioning time (calculated based on student + exam count)

**"Create Tenant" button:** Triggers async Celery provisioning task. Modal shows a provisioning progress indicator. User receives in-portal notification when complete. They can dismiss the modal and continue working.

**Provisioning progress steps (shown in modal):**
1. Creating institution account
2. Applying plan features
3. Seeding students
4. Seeding exams and patterns
5. Generating test attempts and results
6. Applying feature flag overrides
7. Setting up admin credentials
8. Finalising access permissions
9. Complete

---

## Tab 5 — Audit Log

Global audit log for all test tenant management actions across the team.

### Filters

- Date range (default: last 30 days)
- Team member name
- Tenant name
- Action type: Created / Provisioned / Extended / Paused / Resumed / Deleted / Snapshot Created / Snapshot Restored / Flag Override Added / External Link Created / External Link Revoked / Data Seeded

### Audit Table

| Timestamp | Actor | Action | Tenant | Detail |
|---|---|---|---|---|
| 20 Mar 14:30 | Deepa Menon | Tenant Created | Enterprise Coaching — Mar26 | From template, 5K students, 200 exams |
| 20 Mar 14:35 | Deepa Menon | Flag Override | Enterprise Coaching — Mar26 | enable_webcam_proctoring → true |
| 19 Mar 10:15 | Rahul Nair | External Link Created | Demo School — Client | Link expires 26 Mar, password protected |
| 18 Mar 09:30 | Priya Sharma | Snapshot Restored | Standard College QA | Restored "Pre-exam state" snapshot |

CSV export. Pagination: 25 / 50 / 100 per page.

---

## Resource Usage Monitor

Shown as a panel at the bottom of Active Tenants tab (collapsible).

### Resource Summary

| Resource | Used | Limit | % Used | Status |
|---|---|---|---|---|
| Active Tenants | 38 | 50 | 76% | ✓ Healthy |
| Total Storage | 142 GB | 200 GB | 71% | ✓ Healthy |
| Celery Workers (provisioning) | 2 | 8 | 25% | ✓ Healthy |
| DB Schemas (isolated per tenant) | 38 | 50 | 76% | ✓ Healthy |

**Largest Tenants by Storage:**

| Tenant | Storage Used | Institution Type | Students | Created |
|---|---|---|---|---|
| Load Base — 15K Students | 18.4 GB | Coaching | 15,000 | 1 week ago |
| Enterprise Coaching — Max Scale | 12.1 GB | Coaching | 5,000 | 3 days ago |
| Demo — Coaching Empire | 8.9 GB | Coaching | 3,000 | 5 days ago |

"Clean Up Old Tenants" button: opens modal showing all tenants not accessed in > 10 days, with option to delete them in bulk.

---

## Tenant Capacity Planning

Provisioning time estimates based on data configuration:

| Student Count | Exam Count | Estimated Provisioning | Celery Workers Needed |
|---|---|---|---|
| 0–100 | 0–10 | < 1 minute | 1 |
| 100–500 | 10–50 | 1–3 minutes | 1 |
| 500–2,000 | 50–100 | 3–6 minutes | 2 |
| 2,000–5,000 | 100–200 | 6–10 minutes | 4 |
| 5,000–10,000 | 200–400 | 10–15 minutes | 4 |
| 10,000–15,000 | 400–500 | 15–25 minutes | 8 |

At max capacity (15,000 students, 500 exams, with results): provisioning can take up to 25 minutes. Provision during off-peak hours (not during active testing windows).

---

## Notification Rules

| Event | Recipient | Channel |
|---|---|---|
| Tenant provisioned (complete) | Creator | In-App |
| Tenant expiring in 3 days | Creator + shared admins | In-App + Email |
| Tenant expiring in 24 hours | Creator | In-App + Email |
| Tenant auto-expired and deleted | Creator | Email |
| External link accessed (first time) | Link creator | In-App |
| Capacity warning: > 45 active tenants | PM Platform | In-App |
| Storage warning: > 85% used | PM Platform | In-App |

---

## Integration Points

| Page | Integration |
|---|---|
| Page 02 — Feature Flags | Feature flag overrides in tenants source their flag list from Feature Flags. Changes to flag defaults in production are reflected in tenant override dropdowns. |
| Page 16 — Portal Templates | "Test on Test Tenant" action in Dashboard Layout editor uses this page to push preview layout to a selected tenant. |
| Page 17 — Onboarding Workflow | Onboarding simulation tenants use the zero-data template. Onboarding step completion is tracked the same as production. |
| Page 21 — QA Dashboard | QA test runs can target test tenant environments. Test run environment selector includes tenant-specific environments. |
| Page 24 — Performance Test Dashboard | Load Testing templates are the source of seed data for performance test scenarios. Performance tests run against load test tenants. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Max 50 active tenants | Hard limit with warning at 40 | Infrastructure cost control; database schema per tenant is resource-intensive |
| Auto-expiry (default 14 days) | Mandatory, configurable | Prevents accumulation of forgotten tenants consuming storage and compute indefinitely |
| Snapshot system | Save/restore full tenant state | Test repeatability without re-provisioning; critical for regression testing complex scenarios |
| External sharing via time-limited tokens | Not sharing credentials | Client demos need portal access; sharing SRAV admin credentials is a security risk |
| Admin vs read-only access | Two distinct internal access levels | Designers and PMs need portal access but shouldn't change QA test data or flag overrides |
| Paused state | Separate from expired | QA might need to hold a complex mid-test state overnight; pause preserves it without triggering expiry |
| Async provisioning | Celery background task | Seeding 15,000 students + 500 exams takes 15–25 minutes; must not block the UI |
| Feature flag overrides per tenant | Isolated from production flags | Testing a specific flag state without risking the 1,950+ production institutions |
| Score distribution options | Normal / High / Low / Custom | Different test scenarios need different population distributions; one-size does not fit all |
| Activity log | Per-tenant audit trail | Multiple engineers use the same tenant; log shows who changed what and when |
| DB schema isolation | Separate schema per tenant | Prevents cross-tenant data leakage during testing; allows clean deletion without affecting other tenants |
| Resource usage monitor | Always-visible panel | Teams self-regulate tenant creation when they can see total consumption approaching limits |
| Student impersonation | Separate tab in drawer | QA must be able to log in as a real student account on the test tenant to validate full student-facing flows end-to-end; sharing student credentials is a security risk |

---

## G3 Amendment — Student Impersonation

### Impersonate Tab (in Test Tenant Drawer — Tab 5 after Reset)

**Purpose:** Allows QA Engineers to temporarily log in as a specific student or teacher account within a test tenant to validate flows from the institution user's perspective. This is the only way to verify that features such as exam submission, result pages, WhatsApp notifications, and leaderboards work correctly for end users without accessing production data.

**How it works:**
1. QA opens the tenant drawer → clicks "Impersonate" tab
2. Search field: type student name or email — shows matching accounts in this tenant
3. Each result row: Student name · Class/Batch · Account status · Last login
4. Click **[Impersonate →]** button on any row
5. 2FA verification prompt: "Enter your 6-digit code to start impersonation session"
6. After 2FA: student portal opens in a **new browser tab** with a persistent red impersonation banner at the top: "⚠ Impersonation active — logged in as Priya Sharma (Class 10A) · [End Session]"
7. QA can perform any student-facing action: take an exam, view results, check notifications
8. Session auto-expires after **30 minutes** — student portal shows "Impersonation session expired" and tab closes
9. QA can end the session manually by clicking [End Session] in the banner

**Audit logging:** Every impersonation session is recorded in the audit log with: QA engineer name, student account impersonated, tenant name, session start time, session end time, and a list of page URLs visited during the session.

**Business rules:**
- Only QA Engineers can impersonate — PM roles cannot
- Cannot impersonate admin or teacher accounts (student accounts only) — prevents privilege escalation risk
- Cannot impersonate on production tenants — only test tenants
- A maximum of 2 simultaneous impersonation sessions per QA engineer (prevents accidental confusion between sessions)
- If the student account being impersonated has an active exam in progress, a warning is shown: "This student has an exam in progress. Starting impersonation may interfere with their session." Confirmation required.

**Teacher Impersonation (separate):** A "Teacher" sub-tab allows impersonating teacher/HOD accounts for testing class management flows. Same 2FA + audit log + 30-minute expiry rules apply. Teacher impersonation requires an additional permission: `qa.impersonate_teacher`.

**Impersonation History Table:**

| Session ID | Impersonated Account | Account Type | QA Engineer | Started | Duration | Ended By |
|---|---|---|---|---|---|---|
| IMP-2026-03-20-001 | Priya Sharma (Class 10A) | Student | Deepa Menon | 14:30 | 12 min | Manual [End Session] |
| IMP-2026-03-20-002 | Raj Kumar (Batch B) | Student | Deepa Menon | 15:05 | 30 min | Auto-expiry |
| IMP-2026-03-19-005 | Mrs. Lakshmi (Teacher) | Teacher | Arjun (QA) | 11:20 | 8 min | Manual |

**Role-based visibility:** Only QA Engineers see the Impersonate tab. PM and Designer roles do not see this tab at all.

---

## Amendment G10 — Test Data Tab

**Gap:** QA engineers have no systematic way to manage reusable test data. Currently, test tenants are created from scratch or with ad-hoc scripts. There are no named fixtures, no safe way to use anonymized production snapshots, and no data generators for edge cases (1M student tenant, multilingual content, zero-score boundary, etc.).

### New Tab: "Test Data"

Added to the Tab Bar after `Impersonate`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ TEST DATA                                          [+ Create Fixture] [Generate]│
│ Named data fixtures · anonymised prod snapshots · data generators               │
├─────────────────────────────────────────────────────────────────────────────────┤
│ Sub-tabs: [Fixtures] [Prod Snapshots] [Generators] [Data Catalog]              │
├─────────────────────────────────────────────────────────────────────────────────┤
│ FIXTURES TAB                                                                    │
│                                                                                 │
│ Named, reusable datasets that can be applied to any test tenant                │
│                                                                                 │
│ ┌────────────────────────────────────────────────────────────────────────────┐  │
│ │ Fixture: "SSC Coaching — 500 Students, 3 Batches, 20 Exams"               │  │
│ │ Size: 1.2 MB · Created: Deepa (QA) · 2026-03-10 · Used on: 3 tenants     │  │
│ │ Contents: 500 student accounts, 3 teacher accounts, 20 exams,              │  │
│ │           150 exam results, 2 promo codes, plan: Pro                       │  │
│ │ [Apply to Tenant] [Download JSON] [Edit Metadata] [Delete]                │  │
│ ├────────────────────────────────────────────────────────────────────────────┤  │
│ │ Fixture: "Edge Case — Zero Score Boundary"                                 │  │
│ │ Size: 45 KB · Created: Arjun (QA) · 2026-02-28 · Used on: 1 tenant       │  │
│ │ Contents: 10 students with score=0, score=0.01, score=null results        │  │
│ │ [Apply to Tenant] [Download JSON] [Edit Metadata] [Delete]                │  │
│ ├────────────────────────────────────────────────────────────────────────────┤  │
│ │ Fixture: "Enterprise — Multi-branch, 1200 Students"                        │  │
│ │ Size: 4.8 MB · Created: Deepa (QA) · 2026-03-15 · Used on: 2 tenants     │  │
│ │ Contents: 1 group institution, 4 branches, 1200 students, 50 teachers,    │  │
│ │           100 exams, plan: Enterprise, custom domain configured            │  │
│ │ [Apply to Tenant] [Download JSON] [Edit Metadata] [Delete]                │  │
│ └────────────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Prod Snapshots Sub-tab

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ PROD SNAPSHOTS                                      [Request New Snapshot]      │
│ Anonymised copies of real production data for realistic testing                 │
│ All PII removed before storage — no raw names, emails, or mobile numbers        │
├───────────────────────────────────────┬──────────┬──────────────┬───────────────┤
│ Snapshot                              │ Size     │ Created      │ Actions       │
├───────────────────────────────────────┼──────────┼──────────────┼───────────────┤
│ SSC Coaching Anon (1,245 students)    │ 18.4 MB  │ 2026-03-01   │ [Apply] [DL] │
│ NEET Institute Anon (880 students)    │ 12.1 MB  │ 2026-02-15   │ [Apply] [DL] │
│ School District Anon (3,400 students) │ 52.7 MB  │ 2026-01-31   │ [Apply] [DL] │
├───────────────────────────────────────┴──────────┴──────────────┴───────────────┤
│ Request new snapshot: Select institution type → request sent to Platform Ops   │
│ Platform Ops runs anonymisation pipeline before making snapshot available here  │
│ Anonymisation: Names → Faker-generated, Emails → anon@test.srav.in,           │
│                Mobiles → 9000000001 sequence, Aadhaar → 0000000000000          │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Generators Sub-tab

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ DATA GENERATORS                                                                  │
│ Programmatic data generation for specific test scenarios                         │
├──────────────────────────────────────────────────────────────────────────────────┤
│ Available Generators:                                                            │
│                                                                                 │
│ ○ Student Bulk Generator                                                        │
│   Count: [____] · Plan: [Pro ▼] · Domain: [SSC ▼] · With results: [✅]        │
│                                                                                 │
│ ○ Exam Series Generator                                                         │
│   Exams: [____] · Questions per exam: [____] · Domain: [All ▼]                 │
│   Include: [Live exams ✅] [Draft exams ✅] [Upcoming ✅]                       │
│                                                                                 │
│ ○ Boundary / Edge Case Generator                                                │
│   Scenario: [Max students per exam (50,000) ▼]                                 │
│   Generates: tenant with single exam, 50,000 student slots, 0 results          │
│                                                                                 │
│ ○ Multilingual Content Generator                                                │
│   Languages: [Hindi ✅] [Tamil ✅] [Telugu ✅] [English ✅]                    │
│   Questions per language: [____]                                                │
│                                                                                 │
│ ○ Billing / Payment History Generator                                           │
│   Months of history: [____] · Include failed payments: [✅]                    │
│   Include promo redemptions: [✅]                                               │
│                                                                                 │
│ Target tenant: [Select test tenant ▼]    [Generate Data]                       │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Models Added

```python
class TestDataFixture(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    s3_key = models.CharField(max_length=500)
    size_bytes = models.BigIntegerField()
    contents_summary = models.JSONField(
        default=dict,
        help_text='e.g. {students: 500, exams: 20, results: 150}'
    )
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    times_applied = models.PositiveIntegerField(default=0)


class TestDataFixtureApplication(models.Model):
    """Audit log of which fixture was applied to which tenant."""
    fixture = models.ForeignKey(
        TestDataFixture, on_delete=models.CASCADE, related_name='applications'
    )
    tenant = models.ForeignKey(
        'TestTenant', on_delete=models.CASCADE, related_name='fixture_applications'
    )
    applied_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    applied_at = models.DateTimeField(auto_now_add=True)
    overwrite_existing = models.BooleanField(default=False)


class ProdSnapshot(models.Model):
    STATUS = [
        ('requested', 'Requested'),
        ('anonymising', 'Anonymising'),
        ('ready', 'Ready'),
        ('failed', 'Failed'),
    ]
    label = models.CharField(max_length=200)
    source_institution_type = models.CharField(max_length=50)
    student_count = models.IntegerField()
    s3_key = models.CharField(max_length=500, blank=True)
    size_bytes = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=15, choices=STATUS, default='requested')
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    ready_at = models.DateTimeField(null=True, blank=True)
    anonymisation_log = models.TextField(blank=True)
```

**Security:** Prod snapshots require `qa.access_prod_snapshots` permission (separate from general test data). All snapshot download links are pre-signed S3 URLs expiring in 1 hour. Snapshots auto-deleted from S3 after 90 days. Snapshot data never applied to production tenants — validator checks `tenant.is_test == True` before applying.

