# C-21 — Feature Flag Manager

> **Route:** `/engineering/feature-flags/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Backend Engineer (Role 11) · DevOps/SRE (Role 14)
> **Read Access:** Frontend Engineer (Role 12)
> **File:** `c-21-feature-flags.md`
> **Priority:** P1
> **Status:** ✅ Spec done — G22 (new page)

---

## 1. Page Name & Route

**Page Name:** Feature Flag Manager
**Route:** `/engineering/feature-flags/`
**Part-load routes:**
- `/engineering/feature-flags/?part=kpi` — flag health KPI strip
- `/engineering/feature-flags/?part=flags` — flag inventory table
- `/engineering/feature-flags/?part=drawer&flag_id={id}` — flag detail drawer (feature-flag-drawer)
- `/engineering/feature-flags/?part=audit` — flag change audit log

---

## 2. Purpose (Business Objective)

The Feature Flag Manager provides a centralised portal for enabling, disabling, and progressively rolling out platform features without code deployments. In a multi-tenant SaaS platform serving 2,050 institutions and up to 7.6M students, the ability to toggle a feature for a single institution, a percentage of users, or a specific environment is critical for safe rollout and emergency response.

Without feature flags, every feature enable or disable requires a code deploy — a 15–30 minute process that cannot be done during exam windows. A feature flag can toggle in seconds, constrained only by Memcached TTL and the next Lambda cold start.

**Business goals:**
- Enable safe, incremental feature rollouts without code deployments
- Allow per-tenant overrides so a feature can be enabled for one institution before platform-wide rollout
- Support boolean flags (on/off), rollout flags (percentage-based), and variant flags (A/B/C value variants)
- Gate production flag changes behind 2FA to prevent accidental toggles
- Full audit trail of every flag change with before/after state and actor identity
- Emergency disable: any flag can be turned off for all tenants in < 30 seconds

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: create · edit · toggle · delete flags · production 2FA gates |
| Backend Engineer (11) | Level 4 | Full: create · edit · toggle flags (staging/pre-prod without 2FA; production requires 2FA) |
| DevOps / SRE (14) | Level 4 | Full: create · edit · toggle flags · emergency disable in production |
| Frontend Engineer (12) | Level 4 — Read | View flag list + current values; cannot toggle |

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Flag Health

**Purpose:** Instant overview of flag health and recent changes.

**Header elements:**
- H1 "Feature Flag Manager"
- Active flags count: "48 active flags · 12 in rollout"
- Recent changes badge: "3 flags changed in last 1h"
- "New Flag" button (Admin / Backend / DevOps)
- "Emergency Disable All" button (Admin only · 2FA required · disables all flags simultaneously — for catastrophic rollout events)
- Environment selector: Staging · Pre-production · Production (tab strip; default = Production)

**Health Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ All flags healthy | Green | "48 flags active · 0 errors · No recent emergency changes" |
| ⚠ Rollout in progress | Amber | "3 flags currently in active rollout — monitor for error rate changes" |
| 🚨 Emergency disable active | Red | "Emergency disable triggered by {actor} at {time} — all flags OFF" |

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Total Flags | Count of all non-archived flags | — |
| Active (Global On) | Flags enabled for all tenants | — |
| In Rollout | Flags at 1–99% rollout | — |
| Per-Tenant Overrides | Count of flags with at least one tenant override | — |
| Flags Changed Today | Count of flag state changes today | > 10 = amber (unusual change volume) |
| Evaluation Errors (1h) | Count of flag SDK errors in last 1h | > 0 = amber |

---

### Section 3 — Flag Inventory Table

**Purpose:** Complete list of all feature flags with current state across environments.

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Flag Key | Machine-readable key used in code (e.g., `new_exam_ui_v2`) | ✅ |
| Name | Human-readable name | ✅ |
| Type | Boolean · Rollout (%) · Variant (A/B/C) | ✅ |
| Category | Feature (user-facing) · Infrastructure (internal) · Experiment (A/B test) · Kill switch | ✅ |
| Team Group | Frontend · Backend · Mobile · AI · Experimental | ✅ |
| Staging | Current value in Staging environment | — |
| Pre-prod | Current value in Pre-production | — |
| Production | Current value in Production | — |
| Rollout % | For rollout flags: current production rollout percentage | ✅ |
| Tenant Overrides | Count of tenants with non-default value | — |
| Owner | Backend engineer responsible | ✅ |
| Last Changed | Timestamp of last production change | ✅ |
| Changed By | Who made the last change | — |
| Status | ✅ Active · 🗄 Archived | ✅ |

**Flag Type Icons:**
- Boolean: toggle icon
- Rollout: percentage/dial icon
- Variant: fork icon

**Row click:** Opens feature-flag-drawer (see Section 4).

**Filter bar:**
- Type: All / Boolean / Rollout / Variant
- Category: All / Feature / Infrastructure / Experiment / Kill switch
- Team Group: All / Frontend / Backend / Mobile / AI / Experimental
- Production state: All / ON / OFF / Partial (rollout)
- Has tenant overrides: toggle
- Owner: dropdown filter
- Search: flag key or name

**Inline quick-toggle:**
- For boolean flags in the current environment: a toggle switch shown directly in the Production column
- Toggling production flags: requires 2FA confirmation modal (even for quick-toggle)
- Non-production environments: toggle without 2FA

---

### Section 4 — Feature Flag Detail Drawer (feature-flag-drawer)

**Purpose:** Full configuration and history for a single feature flag.

**Drawer Width:** 480px
**Tabs:** Flag Config · Tenant Overrides · Rollout % · History

---

#### Tab 1 — Flag Config

**Flag metadata:**

| Field | Value | Editable |
|---|---|---|
| Flag Key | `new_exam_ui_v2` | ❌ (immutable after creation) |
| Name | "New Exam UI Version 2" | ✅ |
| Type | Boolean | ❌ (immutable — changing type requires creating a new flag) |
| Category | Feature | ✅ |
| Team Group | Backend | ✅ (Frontend / Backend / Mobile / AI / Experimental) |
| Description | "Enables the redesigned exam-taking interface with split-panel layout." | ✅ |
| Owner | Rohan (Backend Engineer) | ✅ |
| Linked Ticket / PR | GitHub issue or PR URL | ✅ optional |
| Expected Removal | Date when this flag should be auto-disabled (see below) | ✅ optional |
| Auto-disable on expiry | Toggle: if enabled, flag is automatically turned OFF in all environments when Expected Removal date passes | ✅ optional |
| Linked Deployment | C-05 Lambda deployment that auto-enables this flag on successful deploy | ✅ optional |
| Created By | Priya (Admin) | ❌ |
| Created At | Jan 15, 2026 | ❌ |

**Environment values:**

Three rows — Staging · Pre-production · Production:

| Environment | Value | Last Changed | Changed By | Override |
|---|---|---|---|---|
| Staging | ✅ ON | 3 days ago | Rohan (Backend) | "Toggle" button |
| Pre-production | ✅ ON | 1 day ago | Rohan (Backend) | "Toggle" button |
| Production | ❌ OFF | 5 days ago | Priya (Admin) | "Toggle" button (2FA) |

**Variant config (for Variant-type flags only):**
- Variant options: list of named variants with their values (e.g., control = "v1", treatment_a = "v2_blue", treatment_b = "v2_green")
- Default variant: which variant is served when no rollout or tenant override applies
- Per-variant value: string · number · boolean · JSON

**Kill switch note (for Kill switch category):**
- Red banner: "This flag is a Kill Switch. Disabling it will turn OFF the associated feature for ALL tenants simultaneously. Exercise with extreme caution."

**Flag Expiry Auto-Disable:**

When "Auto-disable on expiry" is enabled and an Expected Removal date is set:
- A Celery beat task (`portal.tasks.feature_flags.expire_flags`) runs daily at 02:00 UTC
- Any flag with `auto_disable_on_expiry = True` and `expected_removal_date < today` is automatically turned OFF in all environments
- On auto-disable: the flag's `platform_flag_audit_log` gets an entry with `action = "auto_disabled_on_expiry"` and `actor = "system"`
- Email notification sent to the flag Owner and Platform Admin: "Flag `{key}` was automatically disabled — expected removal date {date} has passed. Please clean up from code."
- The flag is NOT deleted — it remains in archived state for code cleanup tracking
- Flags without `auto_disable_on_expiry` enabled show Expected Removal as a reminder label only (amber highlight when overdue, no auto-action)

**Save/Toggle actions:**
- "Save" for metadata changes (no 2FA)
- "Toggle {env}" for environment toggles: staging/pre-prod = no 2FA; production = 2FA modal with "Type flag key to confirm" field
- For rollout and variant flags: toggle button is replaced by "Edit rollout %" and "Edit variant" links that open the respective tabs

---

#### Tab 2 — Tenant Overrides

**Purpose:** Show which tenants have a non-default value for this flag, and allow adding/editing/removing overrides.

**Tenant Overrides Table:**

| Tenant Name | Schema | Override Value | Override Set By | Override Set At | Note | Actions |
|---|---|---|---|---|---|---|
| Vibrant Academy | tenant_001_vibrant | ✅ ON (early access) | Rohan (Backend) | Jan 20, 2026 | "Pilot tenant for new UI" | Edit · Remove |
| Alpha Coaching | tenant_099_alpha | ❌ OFF (disabled) | Priya (Admin) | Feb 1, 2026 | "Tenant reported performance issues" | Edit · Remove |

**Adding a tenant override:**
- "Add Tenant Override" button → inline form:
  - Tenant: search by name or schema
  - Override value: ON / OFF (for boolean); percentage (for rollout); variant select (for variant)
  - Note: reason (required — audit trail)
  - 2FA required for production overrides

**Removing a tenant override:**
- Confirmation modal: "Remove override — {tenant} will revert to the global production value ({current global value})"

**Bulk override:**
- "Apply override to multiple tenants" → search multi-select + value + note + 2FA

---

#### Tab 3 — Rollout %

**Visible only for Rollout-type flags.**

**Purpose:** Configure the gradual rollout percentage for this flag.

**Rollout status:**

| Environment | Current % | Target % | Rolling Since |
|---|---|---|---|
| Production | 15% | 100% | Jan 22, 2026 |
| Pre-production | 100% | 100% | Jan 10, 2026 |
| Staging | 100% | 100% | Jan 5, 2026 |

**Rollout % editor (for production):**
- Slider: 0% – 100%
- Current value: 15%
- "Scheduled increase" toggle: set automatic step increases (e.g., +10% every 24h if no error rate spike)
- Manual override: set specific % immediately
  - ≤ 50% total rollout: 2FA required (Backend / DevOps / Admin can approve own change)
  - > 50% total rollout: **Platform Admin approval required** — change is submitted as a "Rollout Approval Request"; Backend/DevOps engineers can propose but cannot self-approve; Platform Admin receives an in-app notification and email; the rollout is applied only after explicit Admin approval; stored in `platform_flag_rollout_approvals` table
- Preview: "At 15%, approximately 307 of 2,050 tenants see this feature (based on deterministic hash of tenant_schema_name)"

**Rollout algorithm:**
The rollout % is evaluated deterministically per tenant using a hash function on the tenant schema name (not random per request). This ensures consistency: a tenant either always sees the feature or never does at a given rollout %, without session-to-session inconsistency.

**Rollout schedule:**

If scheduled increases are enabled:
| Scheduled Step | Target % | Trigger Date | Condition |
|---|---|---|---|
| Step 1 | 25% | Jan 25, 2026 | Error rate < 0.5% in Step 0 |
| Step 2 | 50% | Feb 1, 2026 | Error rate < 0.5% in Step 1 |
| Step 3 | 100% | Feb 8, 2026 | Error rate < 0.5% in Step 2 |

**Auto-rollback:**
- Optional: if error rate rises above threshold during a scheduled step, rollout is automatically paused and previous % is restored
- Threshold: configurable (default: > 1% error rate increase vs baseline)

---

#### Tab 4 — History

**Purpose:** Immutable audit log of all changes to this flag.

**History Table:**

| Timestamp | Actor | Action | Environment | Before | After | Note |
|---|---|---|---|---|---|---|
| 2h ago | Priya (Admin) | Toggle | Production | OFF | ON | "Enabling for all production — rollout complete" |
| 1 day ago | Rohan (Backend) | Add tenant override | Production | — | Vibrant: ON | "Early access pilot" |
| 3 days ago | Priya (Admin) | Toggle | Pre-production | OFF | ON | "Tested successfully in preprod" |
| 5 days ago | Rohan (Backend) | Created flag | — | — | Created | "New exam UI flag" |

**Entries are immutable** — no delete or edit of history records.

---

### Section 5 — Flag Audit Log

**Purpose:** Cross-flag audit view showing all flag changes in chronological order — for security reviews and incident investigations.

**Route:** `/engineering/feature-flags/?part=audit`

**Audit Log Table:**

| Timestamp | Flag Key | Actor | Action | Environment | Before | After | Note |
|---|---|---|---|---|---|---|---|
| 2h ago | new_exam_ui_v2 | Priya (Admin) | Toggle | Production | OFF | ON | "Full rollout" |
| 3h ago | ai_suggestions_beta | Rohan (Backend) | Rollout % | Production | 10% | 25% | "Step 2 rollout" |
| 5h ago | experimental_billing_flow | Priya (Admin) | Emergency disable | Production | ON | OFF | "Billing error reports from 3 tenants" |

**Filters:** Flag key · Actor · Action type · Environment · Date range

**Export:** CSV or PDF — for security audits and CERT-In incident investigations.

---

## 5. User Flow

### Flow A — Progressive Rollout of New Exam UI

1. Backend Engineer creates flag `new_exam_ui_v2` (Boolean type, Category: Feature)
2. Enables in Staging → tests for 3 days
3. Enables in Pre-production → QA team tests with realistic data
4. Adds tenant override for Vibrant Academy (pilot tenant) in Production → ON
5. Monitors error rates + user feedback from Vibrant Academy for 7 days
6. Creates rollout plan: 10% → 25% → 50% → 100% over 4 weeks
7. Changes flag type to Rollout, sets production to 10%
8. Scheduled steps trigger automatically as error rate stays low
9. At 100%: enables globally; schedules flag archival in 30 days (code cleanup)

### Flow B — Emergency Kill Switch

1. Billing team reports: new payment flow has a bug causing double charges
2. DevOps opens Feature Flag Manager → finds `experimental_billing_flow`
3. Emergency: clicks production toggle → 2FA modal → types flag key → confirms
4. Flag disabled for all tenants in < 30 seconds
5. Error reports stop within 2 minutes (Lambda cold starts with new flag value)
6. Incident created in C-18 with flag change as root cause event
7. Flag stays disabled until bug is fixed; flag history shows emergency action

### Flow C — Per-Tenant Early Access

1. A large institution (Sunrise Academy) requests early access to the AI suggestions feature
2. Admin opens `ai_suggestions_beta` flag → Tenant Overrides tab
3. "Add Tenant Override" → selects tenant_042_sunrise → value: ON → note: "Enterprise early access agreement"
4. Sunrise Academy users see AI suggestions; all other tenants see off state
5. After 30 days: global production rollout begins; per-tenant override becomes redundant
6. Override removed; global rollout % catches Sunrise Academy automatically

---

## 6. Component Structure (Logical)

```
FeatureFlagManagerPage
├── PageHeader
│   ├── PageTitle
│   ├── EnvironmentSelector (Staging / Pre-prod / Production)
│   ├── ActiveFlagsCount
│   ├── NewFlagButton
│   ├── EmergencyDisableButton (Admin · 2FA)
│   └── HealthBanner
├── KPIStrip × 6
├── FlagInventoryTable
│   ├── FilterBar
│   └── FlagRow × N (with inline quick-toggle for boolean flags)
├── FeatureFlagDrawer (480px)
│   └── DrawerTabs
│       ├── FlagConfigTab
│       ├── TenantOverridesTab
│       ├── RolloutPercentTab (rollout-type flags only)
│       └── HistoryTab
└── FlagAuditLog
    ├── FilterBar
    └── AuditTable (cross-flag view)
```

---

## 7. Data Model (High-Level)

### platform_feature_flags

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_key | VARCHAR(100) | unique; machine-readable; immutable after creation |
| name | VARCHAR(200) | human-readable |
| type | ENUM | boolean/rollout/variant |
| category | ENUM | feature/infrastructure/experiment/kill_switch |
| description | TEXT | |
| owner_id | UUID FK → platform_staff | |
| linked_ticket_url | VARCHAR(512) | nullable |
| expected_removal_date | DATE | nullable |
| status | ENUM | active/archived |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |

### platform_flag_environment_values

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| environment | ENUM | staging/pre_production/production |
| enabled | BOOLEAN | for boolean and rollout flags |
| rollout_pct | SMALLINT | 0–100; for rollout flags; NULL for boolean |
| variant_default | VARCHAR(100) | for variant flags; NULL for non-variant |
| updated_by | UUID FK → platform_staff | |
| updated_at | TIMESTAMPTZ | |
| Unique | (flag_id, environment) | |

### platform_flag_variant_options

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| variant_key | VARCHAR(100) | e.g., "control", "treatment_a" |
| variant_value | JSONB | any value type |

### platform_flag_tenant_overrides

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| tenant_schema | VARCHAR(80) | |
| environment | ENUM | staging/pre_production/production |
| enabled | BOOLEAN | nullable (for boolean/rollout flags) |
| rollout_pct | SMALLINT | nullable (for rollout flags — per-tenant %) |
| variant_key | VARCHAR(100) | nullable (for variant flags) |
| note | TEXT | required |
| set_by | UUID FK → platform_staff | |
| set_at | TIMESTAMPTZ | |
| Unique | (flag_id, tenant_schema, environment) | |

### platform_flag_audit_log (immutable)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| flag_key | VARCHAR(100) | denormalised (flag may be archived later) |
| actor_id | UUID FK → platform_staff | |
| action | ENUM | created/toggled/rollout_changed/override_added/override_removed/archived/emergency_disabled/auto_disabled_on_expiry/deployment_auto_enabled |
| environment | ENUM | nullable |
| before_state | JSONB | snapshot of relevant field before change |
| after_state | JSONB | snapshot of relevant field after change |
| note | TEXT | nullable |
| twofa_verified | BOOLEAN | |
| created_at | TIMESTAMPTZ | set by DB trigger; immutable |

### platform_flag_rollout_schedule

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| step_number | SMALLINT | |
| target_pct | SMALLINT | |
| trigger_at | TIMESTAMPTZ | when this step should auto-execute |
| condition | VARCHAR(200) | description of error rate condition |
| error_rate_threshold_pct | DECIMAL(5,2) | auto-pause if exceeded |
| status | ENUM | pending/executed/paused/skipped |
| executed_at | TIMESTAMPTZ | nullable |

### platform_flag_rollout_approvals

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| requested_by | UUID FK → platform_staff | Backend or DevOps engineer |
| requested_pct | SMALLINT | proposed rollout % |
| reason | TEXT | required |
| status | ENUM | pending/approved/rejected |
| reviewed_by | UUID FK → platform_staff | Platform Admin only |
| reviewed_at | TIMESTAMPTZ | nullable |
| review_note | TEXT | nullable |
| created_at | TIMESTAMPTZ | |

### platform_flag_deployment_links

Stores the linkage between a feature flag and a C-05 Lambda deployment that should auto-enable it.

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| flag_id | UUID FK → platform_feature_flags | |
| environment | ENUM | staging/pre_production/production |
| lambda_function_name | VARCHAR(200) | function that triggers the auto-enable |
| auto_enable_on_success | BOOLEAN | if true, flag is turned ON when deployment health check passes |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |

**C-05 Deployment Integration:**

When a deployment link is configured on a flag:
- In C-05 Service Deployment Manager, after a Lambda deployment completes successfully (all health checks pass), a post-deploy webhook calls the feature flag API to enable the linked flag in the specified environment
- The flag's `platform_flag_audit_log` records `action = "deployment_auto_enabled"` with `actor = "system"` and `note = "Auto-enabled by deployment {deployment_id} of {function_name}"`
- If the deployment health check fails, the flag is not enabled and the deployment failure is noted in the audit log
- In C-21, the "Linked Deployment" field on the Flag Config tab shows the linked function name and environment with a link back to C-05
- In C-05, the Deployment detail drawer shows "Post-deploy flag actions" — a read-only list of flags that will be auto-enabled on success

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Flag key format | Lowercase letters, numbers, and underscores only · min 3 chars · max 100 chars · must be unique across all environments · immutable after creation |
| Production toggle | 2FA required for all production environment changes (toggle, rollout %, override add/remove) |
| Emergency disable all | Admin only · 2FA · type "DISABLE ALL FLAGS" to confirm · C-18 incident auto-created |
| Rollout % increase | > 50% total production rollout requires Platform Admin approval via `platform_flag_rollout_approvals`; Backend/DevOps can propose, not self-approve |
| Variant flag type | Cannot change flag type after creation — archive old flag and create new one |
| Tenant override note | Required (min 10 chars) for all production overrides |
| Rollout schedule | Minimum 2 steps; scheduled trigger_at must be in the future |
| Flag archival | Cannot archive a flag that has active tenant overrides (remove overrides first) · cannot archive a flag with rollout < 100% or > 0% in production |
| Flag key collision | System checks for collision with existing archived flags (to prevent resurrection of a different concept under the same key) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| Production 2FA gate | Every production environment change requires TOTP validation regardless of who makes it; prevents accidental toggles |
| Audit log immutability | `platform_flag_audit_log` is INSERT-only at application layer; DB-level role restrictions same as `platform_security_audit_log` (C-13 G24) |
| Emergency disable | Creates C-18 incident automatically + logs to security audit trail |
| Flag value in SDK | Flag values cached in Memcached (30s TTL); Lambda functions read from Memcached on each request; no direct DB read on hot path |
| No flag values in client JS | Flag evaluation is server-side only; client receives rendered HTML with feature visible/hidden, not the flag value itself; prevents client-side flag override |
| Flag key as contract | Flag keys are referenced in code; changing key meaning without code deploy is an anti-pattern; description field documents the intended semantic |
| Access log | All read access to the Feature Flag Manager is logged via Django request logging (who viewed which flag, when) |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| Flag toggled during active exam | System warns: "There are currently {n} active exam sessions. Toggling exam-related flags may affect in-progress exams." DBA confirms with "I understand — proceed" checkbox before 2FA |
| Two admins toggle same flag simultaneously | PostgreSQL row-level UPDATE lock (SELECT FOR UPDATE); second toggle sees the updated state; audit log has two consecutive entries |
| Flag key referenced in code but deleted from manager | Archived flags return their last-set value (not an error); deletion from DB is never allowed — only archival |
| Rollout schedule step fires during exam window | Celery beat checks `platform:active_exam_count` ORM field before executing scheduled rollout step; if active exams > 0, step is deferred by 30 min and retried |
| Emergency disable called but Memcached unavailable | System writes disabled state to DB; Lambda fallback on Memcached miss reads DB directly (with 5s timeout and circuit breaker); flag disable propagates on next Lambda cold start |
| Tenant override set for a tenant that is suspended | System warns "tenant_042 is currently suspended. Override will be applied but will have no effect until tenant is unsuspended." |
| Flag with rollout = 0% but enabled = true | This is valid: enabled = true means "flag exists and is ON for overriding tenants"; rollout_pct = 0 means no tenants get it globally |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| Flag evaluation on hot path | Lambda functions read flag values from Memcached (30s TTL per {flag_key, environment, tenant_schema} composite key); fallback to DB on cache miss; < 2ms on cache hit |
| Cache invalidation on toggle | On any flag change: Celery task calls cache.delete for affected keys (flag_key + environment + all tenant_schema keys with overrides); Memcached has no pub/sub so explicit delete per key; < 1s propagation for affected tenants |
| Flag inventory table (48 flags) | Loaded all at once; no pagination needed at current scale; < 50ms DB query |
| Tenant overrides at scale | `platform_flag_tenant_overrides` indexed on (flag_id, environment); for 2,050 possible tenants per flag: max 2,050 rows per flag, trivial query |
| Audit log growth | `platform_flag_audit_log` is append-only; indexed on (flag_id, created_at); cross-flag audit log indexed on (created_at, actor_id); archived to S3 Glacier after 2 years |
| Rollout % evaluation | Deterministic hash of tenant_schema_name modulo 100; compared to rollout_pct; < 0.1ms per evaluation; no DB query needed at evaluation time |
