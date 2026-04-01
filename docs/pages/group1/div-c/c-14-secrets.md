# C-14 — Secret & Key Manager

> **Route:** `/engineering/secrets/`
> **Division:** C — Engineering
> **Primary Role:** Platform Admin (Role 10) · Security Engineer (Role 16) · DevOps/SRE (Role 14)
> **File:** `c-14-secrets.md`
> **Priority:** P0 — Required before any credential-holding service goes live
> **Status:** ⬜ Amendment pending — G7 (OAuth App Registry tab) · G8 (Mobile Keys tab) · G18 (Rotation Compliance tab) · G19 (JWT Compromise Response section)

---

## 1. Page Name & Route

**Page Name:** Secret & Key Manager
**Route:** `/engineering/secrets/`
**Part-load routes:**
- `/engineering/secrets/?part=kpi` — secrets health KPI
- `/engineering/secrets/?part=inventory` — secret inventory table
- `/engineering/secrets/?part=drawer&secret_id={id}` — secret detail drawer
- `/engineering/secrets/?part=rotation-schedule` — rotation schedule calendar
- `/engineering/secrets/?part=rotation-history` — rotation audit history
- `/engineering/secrets/?part=kms-panel` — AWS KMS CMK panel

---

## 2. Purpose (Business Objective)

The Secret & Key Manager is the master inventory and rotation control centre for every sensitive credential the platform uses. From JWT signing keys to Razorpay API keys, from RDS master credentials to FCM server keys — all are catalogued here with their rotation schedules, current health, and AWS Secrets Manager sync status.

The most critical capability on this page is the rotation trigger: a compromised JWT signing key must be rotated within minutes, not hours. This page provides a 2FA-gated, one-click rotation mechanism that handles the full lifecycle: generate new secret → update in AWS Secrets Manager → notify dependent services → confirm propagation.

Key management failure is the most common cause of high-severity security incidents in cloud systems. This page makes the invisible visible: every secret has an owner, an expiry, a rotation schedule, and a propagation status.

**Business goals:**
- Complete inventory of all platform secrets with zero unknown/untracked secrets
- Automated rotation reminders 30 days before expiry
- 2FA-gated emergency rotation within minutes of compromise detection
- AWS Secrets Manager sync status verification for every secret
- KMS Customer Master Key management for data encryption
- Audit trail of every secret creation, rotation, and access event

---

## 3. User Roles

| Role | Access Level | Permissions |
|---|---|---|
| Platform Admin (10) | Level 5 | Full: view inventory (masked) · trigger rotation · view rotation history · manage KMS |
| Security Engineer (16) | Level 4 | Full: view inventory (masked) · trigger rotation · view rotation history · manage KMS |
| DevOps / SRE (14) | Level 4 | View inventory (masked) · trigger rotation for infra secrets · view rotation history |

> **Critical:** No role on this page can view the actual secret value. Values are always masked. Secret values are only accessible to the services that consume them via AWS Secrets Manager SDK at runtime.

---

## 4. Section-Wise Detailed Breakdown

---

### Section 1 — Page Header & Secrets Health

**Purpose:** Instant health verdict on the entire secret estate.

**Secrets Health Banner:**

| State | Colour | Text |
|---|---|---|
| ✅ All secrets healthy | Green | "42 secrets · All within rotation schedule · No expiring in < 30 days" |
| ⚠ Rotation due | Amber | "3 secrets due for rotation in < 30 days" |
| 🚨 Secret expired or compromised | Red | "1 secret expired · Emergency rotation required" |

**Header elements:**
- H1 "Secret & Key Manager"
- Secrets health banner
- Total secrets count: "42 secrets tracked"
- "Add Secret" button (Admin/Security)
- "Run Rotation Audit" button → scans all secrets for expiry + Secrets Manager sync status
- Last audit: "Rotation audit: 2 days ago · All healthy"

---

### Section 2 — KPI Strip

**KPI Cards:**

| Card | Metric | Alert |
|---|---|---|
| Total Secrets | Count in registry | — |
| Expiring < 30 days | Secrets with expiry within 30 days | > 0 = amber |
| Expiring < 7 days | Secrets with expiry within 7 days | > 0 = red |
| Rotation Overdue | Secrets past scheduled rotation date | > 0 = red |
| AWS Secrets Manager Sync | Secrets not synced to Secrets Manager | > 0 = red |
| KMS Keys Enabled | All CMKs in enabled state | Any disabled = amber |

---

### Section 3 — Secret Inventory Table

**Purpose:** Complete catalogue of all platform secrets with health status and metadata.

**Table Columns:**

| Column | Description | Sortable |
|---|---|---|
| Secret Name | Human-readable name | ✅ |
| Category | Signing key · Database · Third-party API · Encryption · OAuth · Infrastructure | ✅ |
| Service(s) | Which Lambda functions/services use this secret | — |
| AWS Secrets Manager ARN | Short ARN (last 30 chars visible) | — |
| KMS Key | Which CMK encrypts this secret | — |
| Last Rotated | Date of last rotation | ✅ |
| Rotation Schedule | Monthly / Quarterly / Annually / Never (with justification) | ✅ |
| Next Rotation Due | Date | ✅ |
| Expiry | If the secret has a hard expiry (API keys, certificates) | ✅ |
| Days to Expiry | Number (colour: green > 90 · amber 30–90 · red < 30) | ✅ |
| Secrets Manager Sync | ✅ Synced · ⚠ Stale · ❌ Not synced | — |
| Status | ✅ Healthy · ⚠ Rotation due · 🚨 Expired · 🔴 Compromised | ✅ |

**Secret Categories and Examples:**

| Category | Examples |
|---|---|
| JWT Signing Keys | `jwt-access-signing-key` · `jwt-refresh-signing-key` |
| Database Credentials | `rds-master-password` · `rds-readonly-password` · `pgbouncer-auth-password` |
| AWS KMS CMKs | `platform-data-cmk` · `platform-tenant-media-cmk` · `mobile-hive-aes-key-ref` |
| Third-party API Keys | `razorpay-key-id` · `razorpay-key-secret` · `fcm-server-key` · `ses-smtp-password` · `sentry-dsn` |
| OAuth Secrets | `google-oauth-client-secret` · `saml-sp-private-key` |
| Infrastructure | `cloudflare-api-token` · `github-actions-pat` · `pagerduty-integration-key` |
| Mobile | `hive-aes-256-key` · `ios-push-cert-p8` · `android-keystore-ref` |
| AI/ML | `openai-api-key` · `anthropic-api-key` · `google-ai-api-key` |

**Filter Bar:**
- Category filter
- Status filter (Healthy / Rotation Due / Expired / Compromised)
- Service filter (which service uses this secret)
- Sort: next rotation due · days to expiry · last rotated

**No secret values shown anywhere in the table.** The table contains only metadata.

---

### Section 4 — Secret Detail Drawer

**Purpose:** Full detail for a single secret without ever exposing the value.

**Drawer Width:** 560px
**Tabs:**

---

#### Tab 1 — Current Secret Details

**Fields:**

| Field | Value | Notes |
|---|---|---|
| Secret Name | `jwt-access-signing-key` | |
| Description | "HMAC-SHA256 key for signing JWT access tokens" | |
| Category | JWT Signing Key | |
| AWS Secrets Manager ARN | `arn:aws:secretsmanager:ap-south-1:...` | Full ARN shown |
| KMS Encryption Key | `platform-data-cmk (alias/platform-data)` | |
| Secret Type | String · JSON · Binary | |
| Value | `••••••••••••••••••••` (always masked) | Never shown |
| Value Length | "512-bit key (64 bytes)" | Metadata only |
| Consuming Services | `auth-service-login · auth-service-token · auth-service-refresh` | |
| Owner | Priya Sharma (Security Engineer) | |
| Created At | Jan 2024 | |
| Created By | Arjun Mehta (Platform Admin) | |
| Last Rotated | Feb 2026 (via automated rotation) | |
| Next Rotation Due | May 2026 | |
| Rotation Schedule | Quarterly | |
| Hard Expiry | None | |
| Secrets Manager Sync | ✅ Synced · Version AWSCURRENT | |
| Last Sync Verified | 2h ago | |

**Actions (Security/Admin):**
- "Trigger Rotation" (primary action — see Section 6)
- "Update Description" (inline edit · no 2FA)
- "Change Owner" (inline select)
- "Change Rotation Schedule" (select + 2FA)
- "Mark as Compromised" (red button · 2FA · triggers emergency rotation workflow)

---

#### Tab 2 — Rotation History

**Purpose:** Immutable log of all rotation events for this secret.

**Columns:**

| Column | Description |
|---|---|
| Timestamp | Rotation completed at |
| Triggered By | Manual (actor name) · Automated (Celery beat) · Emergency (reason) |
| Method | AWS Secrets Manager automatic · Platform manual rotation |
| Previous Version | Short fingerprint of old value (first 8 chars of hash — not the value) |
| New Version | Short fingerprint of new value |
| Propagation | Services that received the new value + confirmation timestamps |
| 2FA Verified | ✅ / — (automated) |

**Retention:** Full rotation history retained permanently (security audit requirement)

---

#### Tab 3 — Propagation Status

**Purpose:** Confirm that all services consuming this secret have received the latest version.

**Table:**

| Service | Last Fetched Version | Fetched At | Status |
|---|---|---|---|
| auth-service-login | AWSCURRENT | 4 min ago | ✅ Current |
| auth-service-token | AWSCURRENT | 3 min ago | ✅ Current |
| auth-service-refresh | AWSPREVIOUS (stale) | 2h ago | ⚠ Stale |

**Propagation mechanism:**
- Lambda functions fetch secrets at cold start (cached locally for function lifetime)
- After rotation: stale services use `AWSPREVIOUS` version (still valid during overlap window)
- Overlap window: 2h (both AWSCURRENT and AWSPREVIOUS valid simultaneously)
- After overlap: `AWSPREVIOUS` deleted; stale services must cold-start to get new version

**"Force restart affected services" action:**
- Flushes Lambda warm pool for all consuming services (sets reserved concurrency to 0 → restores immediately)
- Forces cold starts → services fetch AWSCURRENT on next invocation
- 2FA required

---

### Section 5 — Rotation Schedule Calendar

**Purpose:** Month view of all upcoming secret rotation events.

**Calendar Layout:**
- Month view (default) · List view toggle
- Each rotation event: chip on the date it's due
- Colour: green (> 30 days away) · amber (< 30 days) · red (< 7 days) · black (overdue)

**Calendar Entries:**

| Secret | Due Date | Type | Status |
|---|---|---|---|
| jwt-refresh-signing-key | Mar 25, 2026 | Quarterly rotation | 🟡 Due in 5 days |
| rds-master-password | Apr 1, 2026 | Quarterly rotation | ✅ Due in 12 days |
| razorpay-key-secret | Apr 15, 2026 | Annual review | ✅ Due in 26 days |

**Upcoming this month summary card:**
- "4 rotations due in March 2026 — 1 overdue"
- Quick links to each overdue/upcoming secret

**Notification settings:**
- Email notification to secret owner: 30 days before · 7 days before · day-of
- Configurable per secret or platform-wide

---

### Section 6 — Secret Rotation Workflow

**Purpose:** Guided, safe rotation of any secret — from normal scheduled rotation to emergency rotation.

**Trigger:** "Trigger Rotation" button in secret detail drawer

**Two rotation paths:**

---

#### Path A — Standard Rotation

Used for: Scheduled quarterly/annual rotations

**Step 1 — Review:**
- Current secret metadata shown
- "Rotation type: Standard (scheduled)"
- "Services that will be affected: auth-service (3 Lambda functions)"
- "Overlap window: 2 hours (both old and new value valid simultaneously)"
- Warning if active exams: "2 exams currently in progress. Students mid-exam use active JWT tokens. Standard rotation uses overlap window — existing tokens remain valid. Safe to proceed."

**Step 2 — Method:**
- AWS Secrets Manager automatic rotation (Lambda rotation function): recommended for DB credentials + API keys that support automated rotation
- Platform-managed rotation: for secrets that require manual key generation (e.g., JWT signing keys — must generate cryptographically secure random bytes)

**Step 3 — 2FA Confirmation:**
- TOTP input
- "Rotate Secret" button

**On rotation:**
- New value generated (either by AWS Lambda rotation function or platform Celery job)
- AWS Secrets Manager version: new value = AWSCURRENT · old value = AWSPREVIOUS
- Overlap window (2h): both versions valid simultaneously for consuming services
- Propagation tracking in Tab 3 updates
- Rotation history entry created

---

#### Path B — Emergency Rotation

Used for: Suspected or confirmed secret compromise

**Trigger:** "Mark as Compromised" button OR from C-13 Security Ops threat alert

**Key differences from standard rotation:**
- **No overlap window** — old secret value invalidated immediately
- All consuming services force-restarted (Lambda warm pool flushed)
- All active sessions using JWT signed with compromised key: invalidated (bulk-insert all active JTIs into `platform_jwt_denied_tokens` ORM deny-list)
- CERT-In assessment triggered: "Was this secret compromise a data breach? If any student/staff data was accessed using this compromised credential, CERT-In notification required."
- C-18 incident automatically created

**Step 1 — Compromise Assessment:**
- Compromise type: Exposed in code · Leaked to logs · Phishing · Insider threat · Unknown
- Estimated time of compromise (date-time picker)
- "How many accounts may have been affected?" (estimate for CERT-In/DPDPA)

**Step 2 — 2FA (both Admin + Second Approver):**
- Emergency rotation requires dual-admin approval (same pattern as emergency data wipe in C-01)
- Second approver notified immediately via email + platform alert

**Step 3 — Execute:**
- System actions (all atomic):
  1. Generate new secret value
  2. Update AWS Secrets Manager (AWSCURRENT)
  3. Set old value to AWSPENDING (will be deleted in 15 min — no overlap window for emergency)
  4. Flush Lambda warm pools for all consuming services
  5. Bulk-invalidate all active sessions (for JWT keys only): bulk-insert all active JTIs into `platform_jwt_denied_tokens` ORM deny-list
  6. Create C-18 incident
  7. Log to CERT-In incident log (if applicable)
  8. Notify all consuming service owners via email

**Duration:** Emergency rotation completes in < 5 minutes (fast path)

---

### Section 7 — AWS KMS Customer Master Key Panel

**Purpose:** Manage the AWS KMS CMKs used to encrypt all secrets and data-at-rest.

**CMK Inventory:**

| Key Alias | Key ID (short) | Purpose | Status | Key Rotation | Last Rotation | Created |
|---|---|---|---|---|---|---|
| alias/platform-data | key-abc123 | Encrypts all Secrets Manager secrets | ✅ Enabled | ✅ Annual (auto) | Jan 2026 | Jan 2023 |
| alias/platform-rds | key-def456 | RDS storage encryption | ✅ Enabled | ✅ Annual (auto) | Jan 2026 | Jan 2023 |
| alias/platform-s3 | key-ghi789 | S3 bucket encryption (non-public) | ✅ Enabled | ✅ Annual (auto) | Jan 2026 | Jan 2023 |
| alias/platform-tenant-media | key-jkl012 | Tenant uploaded media encryption | ✅ Enabled | ✅ Annual (auto) | Jan 2026 | Jan 2023 |
| alias/mobile-hive-aes | key-mno345 | Flutter Hive AES-256 key material | ✅ Enabled | Manual (annual) | Jan 2026 | Jan 2023 |

**CMK Status Badges:**
- Enabled ✅
- Disabled ⚠ (no decryption possible — data locked)
- Pending deletion 🚨 (highly destructive — cannot be undone)

**Actions per CMK (Admin/Security):**
- "Enable/Disable" → 2FA required · Disable warning: "Disabling this key will prevent all services from decrypting data encrypted with it. This will break the platform."
- "Schedule key deletion" → Admin only · 2FA · minimum 7-day grace period · warning: "IRREVERSIBLE: All data encrypted with this key will be permanently inaccessible after deletion."
- "View key policy" → IAM policy JSON (read-only view)
- "View key usage" → Count of cryptographic operations/day (CloudWatch KMS metrics)

**Key rotation status:**
- AWS KMS automatic annual rotation: enabled/disabled toggle
- When rotation occurs: new key material generated; old key material retained for decryption of existing data; new encryptions use new material
- Manual rotation: only for keys that need to be rotated on non-annual schedule

**KMS audit (CloudTrail):**
- "View KMS usage in CloudTrail" → filtered CloudTrail events for this key (Decrypt, Encrypt, GenerateDataKey operations)
- Anomaly detection: unusual Decrypt volume for a key → Security Engineer alerted

---

### Section 8 — Dependency Map

**Purpose:** Show which services depend on which secrets — "what breaks if this secret is rotated?"

**Visualization:**
- Directed graph: secrets (circle nodes, colour by category) → services (square nodes)
- Click a secret node → highlights all dependent services
- Click a service node → highlights all secrets it depends on

**Use cases:**
- Pre-rotation: "If I rotate razorpay-key-secret, which services will need cold starts?" → 2 services highlighted
- Incident response: "The auth-service is failing — which secrets does it depend on?" → 4 secrets highlighted

**Table view alternative (for those who prefer tables over graphs):**

| Secret | Consuming Services | Lambda Functions | ECS Services |
|---|---|---|---|
| jwt-access-signing-key | auth-service | auth-service-login, auth-service-token, auth-service-refresh | — |
| rds-master-password | All DB-touching services | 12 Lambda functions | celery-worker (via Django) |
| razorpay-key-secret | billing-service | billing-service-order, billing-service-webhook | — |

---

## 5. User Flow

### Flow A — Quarterly JWT Key Rotation

1. Security Engineer receives rotation reminder: "jwt-access-signing-key due in 5 days"
2. Opens `/engineering/secrets/` → finds secret in table (amber status)
3. Clicks row → drawer opens → "Trigger Rotation"
4. Step 1: reviews affected services (3 auth Lambda functions)
5. Step 2: method = Platform-managed (generate 512-bit random key)
6. Step 3: TOTP entered → "Rotate Secret" clicked
7. New key generated; AWS Secrets Manager updated
8. Propagation tab: all 3 services still on AWSPREVIOUS (Lambda haven't cold-started yet)
9. 2h overlap window: both old and new JWT keys valid
10. After 2h: AWSPREVIOUS deleted; all Lambda cold-start with new key
11. Rotation history: entry created with fingerprint comparison

### Flow B — Emergency Rotation After Key Leak

1. Developer accidentally commits JWT signing key to GitHub (detected by git-secrets hook)
2. Security Engineer opens C-13 → creates security incident
3. Navigates to C-14 → finds `jwt-access-signing-key`
4. Clicks "Mark as Compromised" → describes: "Exposed in git commit abc123"
5. Dual-admin approval: second admin approves via email link
6. Emergency rotation executes:
   - New key generated in < 1s
   - Old key invalidated immediately (no overlap window)
   - All 74,000 active JWT tokens invalidated (bulk-inserted into `platform_jwt_denied_tokens` deny-list)
   - Lambda warm pools flushed
   - Students logged out → must re-login
7. Duration: ~4 min total
8. CERT-In assessment: key leak without confirmed data access → file informational report

### Flow C — Pre-Exam Secrets Health Check

1. DevOps runs rotation audit before major exam day
2. All 42 secrets: ✅ synced to Secrets Manager
3. KMS panel: all 5 CMKs enabled
4. Calendar: no rotations due in next 24h (good — no planned disruption)
5. Razorpay key: 84 days until expiry (green — no action needed)
6. JWT key: next rotation in 22 days (green — safe for exam)
7. DevOps confirms: "All secrets healthy — exam day green"

---

## 6. Component Structure (Logical)

```
SecretKeyManagerPage
├── PageHeader
│   ├── SecretsHealthBanner
│   ├── PageTitle
│   ├── AddSecretButton
│   └── RunRotationAuditButton
├── KPIStrip × 6
├── SecretInventoryTable
│   ├── FilterBar
│   └── SecretRow × 42
│       └── (all columns — values always masked)
├── SecretDetailDrawer (560px)
│   └── DrawerTabs
│       ├── CurrentDetailsTab
│       ├── RotationHistoryTab
│       └── PropagationStatusTab
├── RotationWorkflow (inline modal/panel)
│   ├── PathA_StandardRotation (3 steps)
│   └── PathB_EmergencyRotation (3 steps + dual-admin approval)
├── RotationScheduleCalendar
│   ├── MonthView / ListView toggle
│   └── UpcomingRotationSummaryCard
├── KMSPanel
│   ├── CMKInventoryTable
│   └── CMKDetailActions
└── DependencyMap
    ├── GraphView
    └── TableView (alternative)
```

---

## 7. Data Model (High-Level)

### platform_secret_registry

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| secret_name | VARCHAR(100) | human-readable name |
| description | TEXT | |
| category | ENUM | jwt/database/api_key/kms/oauth/infra/mobile/ai |
| aws_secrets_manager_arn | VARCHAR(512) | full ARN |
| kms_key_alias | VARCHAR(100) | |
| consuming_services | JSONB | array of service names + Lambda function names |
| owner_id | UUID FK → platform_staff | |
| rotation_schedule | ENUM | monthly/quarterly/annual/manual/never |
| last_rotated_at | DATE | |
| next_rotation_due | DATE | computed |
| hard_expiry | DATE | nullable |
| rotation_method | ENUM | aws_automatic/platform_managed |
| status | ENUM | healthy/rotation_due/expired/compromised |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |

### platform_secret_rotation_log (immutable)

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| secret_id | UUID FK | |
| rotation_type | ENUM | standard/emergency |
| triggered_by | UUID FK → platform_staff | nullable (automated) |
| approved_by | UUID FK → platform_staff | nullable (dual-admin for emergency) |
| twofa_verified | BOOLEAN | |
| previous_version_fingerprint | CHAR(16) | SHA256 of old value, first 16 chars |
| new_version_fingerprint | CHAR(16) | SHA256 of new value, first 16 chars |
| propagation_status | JSONB | per-service propagation timestamps |
| certIn_triggered | BOOLEAN | |
| reason | TEXT | nullable (for emergency/compromised) |
| created_at | TIMESTAMPTZ | immutable |

---

## 8. Validation Rules

| Rule | Detail |
|---|---|
| Standard rotation | 2FA required for all rotations regardless of schedule |
| Emergency rotation | Dual-admin approval (two separate TOTP submissions) · reason required · cannot be bypassed |
| KMS key deletion schedule | Minimum 7-day waiting period; cannot be shortened · Admin only |
| KMS key disable | 2FA + "disable during exam hours" blocked (blocks all decryption) |
| Rotation during active exam | Standard rotation: allowed (overlap window protects in-flight JWTs) · Emergency rotation: allowed with warning "All 74K active sessions will be terminated" |
| Adding new secret | Must have: name · description · category · Secrets Manager ARN · owner · rotation schedule |
| Secret value viewing | Blocked for all roles on this page — value only accessible via AWS Secrets Manager SDK at service runtime |
| Rotation schedule "Never" | Requires written justification (min 50 chars) · Security Engineer approval |
| Overlap window for emergency | Cannot be set; always zero (immediate invalidation) |

---

## 9. Security Considerations

| Control | Detail |
|---|---|
| Secret values never displayed | Enforced at API layer: endpoint returns metadata only; actual secret value never included in API response; AWS Secrets Manager GetSecretValue never called from this page |
| AWS IAM scope | `secretsmanager:DescribeSecret` + `secretsmanager:GetSecretValue` (for metadata only, not value) + `secretsmanager:RotateSecret`; cannot ListSecrets outside platform namespace (resource-level IAM restriction) |
| KMS key usage audit | All KMS API calls logged to CloudTrail; anomaly detection on unusual Decrypt volume |
| Rotation log immutability | `platform_secret_rotation_log` INSERT-only; same pattern as audit logs throughout platform |
| Dual-admin emergency rotation | Prevents single-admin social engineering or coercion; both approval tokens delivered via separate email |
| Propagation force-restart | Lambda warm pool flush logs to `platform_infra_events` (C-08 audit trail) |
| Session invalidation on JWT rotation | Bulk-insert all active JTIs into `platform_jwt_denied_tokens` ORM deny-list; JWT middleware checks deny-list on every request; students must re-login — this is expected behaviour for emergency rotation |
| SAML private key rotation | Requires coordination with Google Workspace admin (SAML metadata must be updated externally); system provides step-by-step instructions in rotation wizard |

---

## 10. Edge Cases (System-Level)

| Scenario | Handling |
|---|---|
| AWS Secrets Manager unavailable during rotation | Rotation fails gracefully; old secret remains valid; "Rotation failed — Secrets Manager API unavailable. Retry when resolved." + alert to Security team |
| Lambda service doesn't pick up new secret after overlap window | "Force restart" button in Propagation tab; Celery job flushes warm pool; service will fetch new secret on next cold start |
| Rotation triggered for a secret that doesn't support AWS automatic rotation | System falls back to "Platform-managed rotation" — generates new value locally, stores in Secrets Manager manually |
| KMS key accidentally disabled | System detects "Decrypt failed" errors in Lambda CloudWatch logs within 5 min; C-18 auto-incident created; Security Engineer alerted; re-enable requires 2FA |
| Compromise detected for RDS master password | Emergency rotation + all DB connection pools closed (PgBouncer restart) + all Django worker processes restarted (new DB credentials fetched) + full outage for ~3 min |
| Secret with no consuming services | Amber flag: "No services listed as consumers. Verify this secret is still needed or archive it." |
| Rotation reminder email bounces (owner email changed) | Platform sends to Platform Admin as fallback; system prompts to update owner on secrets with bounced notifications |

---

## 11. Performance & Scaling Strategy

| Concern | Strategy |
|---|---|
| 42 secrets inventory (small scale) | All 42 secrets loaded at once; no pagination needed; full page load < 100ms |
| AWS Secrets Manager API calls | `DescribeSecret` (metadata only) called for each of 42 secrets; batched; cached in Memcached 5 min |
| Rotation audit (on-demand) | Celery job: 42 × DescribeSecret + GetSecretRotationStatus + Secrets Manager sync check; completes in < 30s |
| Propagation status polling | Draws from C-04 / C-05 Lambda cold-start telemetry; no new API calls needed |
| Emergency rotation < 5 min | All steps async via Celery; UI polls job status every 5s; critical path (generate + Secrets Manager update) < 10s; Lambda flush + ORM deny-list bulk insert run in parallel |
| KMS metrics | CloudWatch `AWS/KMS` namespace; batched with other CloudWatch calls; 5 min cache |
| Dependency graph rendering | Rendered server-side (Graphviz or D3 pre-computed SVG); 42 secrets × ~3 services each = small graph; render < 200ms |

---

## 12. Amendment — G7: OAuth App Registry Tab

**Assigned gap:** G7 — C-14 stores OAuth client secrets but has no registry of OAuth apps with scopes, redirect URIs, owner, last-used timestamp, or revocation capability.

**Where it lives:** New tab added to the existing page. The page gains a top-level tab strip: **Secrets** (existing sections) · **OAuth Apps** (new) · **Mobile Keys** (G8) · **Rotation Compliance** (G18).

---

### OAuth App Registry Tab

**Purpose:** Provide a complete registry of all OAuth 2.0 applications that have been granted access to the platform's OAuth endpoints — including Google OAuth for staff login, any third-party integrations using OAuth, and SAML SP configurations. Give the Security Engineer the ability to review active apps, audit scope grants, rotate client secrets, and revoke apps that are no longer needed.

**OAuth App Inventory Table:**

| Column | Description |
|---|---|
| App Name | Human-readable name (e.g., "Google OAuth — Staff Login") |
| Client ID | Masked: first 8 chars + `••••` |
| Type | OAuth 2.0 (Authorization Code) · OAuth 2.0 (Client Credentials) · SAML SP |
| Scopes Granted | List of OAuth scopes: openid · profile · email · custom scopes |
| Redirect URIs | Registered callback URIs (count shown; expand to view all) |
| Owner | Platform staff responsible for this app |
| Last Used | Timestamp of last successful OAuth token exchange |
| Status | Active · Inactive (> 90 days no use) · Revoked |
| Client Secret | Always masked · "Rotate Secret" action |
| Actions | View detail · Rotate secret · Revoke app |

**Registered OAuth Apps (typical inventory):**

| App | Type | Purpose |
|---|---|---|
| Google OAuth — Staff Login | OAuth 2.0 Auth Code | Staff SSO via Google Workspace |
| Razorpay Webhook Receiver | OAuth 2.0 Client Credentials | Razorpay payment webhooks |
| GitHub Actions — CI/CD | OAuth 2.0 Client Credentials | CI/CD pipeline platform API access |
| Sentry Error Reporting | OAuth 2.0 Client Credentials | Error tracking integration |
| HackerOne Bug Bounty | OAuth 2.0 Client Credentials | HackerOne platform API |

**OAuth App Detail Drawer (oauth-app-drawer, 560px):**

Tabs: Details · Scope Audit · Token History

**Tab — Details:**
- Full client ID (unmasked after 2FA challenge)
- All registered redirect URIs (editable list — add/remove with 2FA)
- Allowed grant types
- Token lifetime: access token TTL + refresh token TTL
- PKCE required: Yes / No
- Owner + created by + created at

**Tab — Scope Audit:**
- List of all scopes this app is allowed to request
- Per-scope: last used · frequency · "Remove scope" action (2FA)
- Unused scopes (> 90 days not requested): amber badge — "Consider removing"

**Tab — Token History:**
- Last 50 token exchange events: timestamp · actor · scope requested · token lifetime · IP
- "Any suspicious token requests?" — flag for Security Engineer review

**Add New OAuth App:**
"Register New App" button → modal:
- App name + description + owner
- Type selector
- Redirect URI(s)
- Scopes to grant (multi-select from allowed scope list)
- Client secret auto-generated (shown once at registration — never again); stored in Secrets Manager

**Revoke App:**
- Confirmation modal: "Revoking this app will immediately invalidate all tokens issued to it. Any service using this app will stop working. Confirm?"
- 2FA required
- On revoke: all active tokens for this client ID invalidated (ORM deny-list insert); client marked "Revoked" in registry

**Data model:**

**platform_oauth_apps**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| app_name | VARCHAR(200) | |
| client_id | VARCHAR(100) | unique |
| client_secret_arn | VARCHAR(512) | Secrets Manager ARN (never stored in DB) |
| type | ENUM | auth_code/client_credentials/saml_sp |
| redirect_uris | JSONB | array of URIs |
| scopes_granted | JSONB | array of scope strings |
| owner_id | UUID FK → platform_staff | |
| status | ENUM | active/inactive/revoked |
| last_used_at | TIMESTAMPTZ | nullable |
| created_by | UUID FK → platform_staff | |
| created_at | TIMESTAMPTZ | |
| revoked_at | TIMESTAMPTZ | nullable |
| revoked_by | UUID FK → platform_staff | nullable |

---

## 13. Amendment — G8: Mobile Keys Tab

**Assigned gap:** G8 — Mobile Engineer (Role 13) has zero access to C-14, but Mobile Engineers own the Hive AES-256 key and FCM server key and need to see rotation schedules to plan mobile app releases. A key rotation without Mobile Engineer awareness causes the app to fail decryption of locally stored data.

**Where it lives:** New read-only tab added to the Secret & Key Manager page (alongside OAuth App Registry). Mobile Engineer (Role 13) is granted access to this tab only — all other tabs remain restricted to Security/Admin/DevOps.

---

### Mobile Keys Tab

**Purpose:** Provide Mobile Engineers with read-only visibility into the rotation schedule and health of secrets that directly affect mobile app functionality. Mobile Engineers do not need to see all platform secrets — only those that require mobile release coordination.

**Access:** Mobile Engineer (Role 13) — read-only. Security Engineer (Role 16) + Admin (Role 10) — full view (same as their existing access to main Secrets tab).

**Mobile-Relevant Secrets Table:**

Filtered view showing only secrets in the `mobile` category and third-party secrets consumed by mobile apps:

| Secret Name | Purpose | Last Rotated | Next Rotation Due | Days to Rotation | Rotation Impact on Mobile | Status |
|---|---|---|---|---|---|---|
| hive-aes-256-key | Flutter Hive local DB encryption | Jan 2026 | Jan 2027 | 286 days | ⚠ HIGH — app must ship key update before rotation or local data unreadable | ✅ Healthy |
| ios-push-cert-p8 | iOS APNs push notification certificate | Jan 2026 | Jan 2027 | 286 days | Medium — rotation causes push gap until new cert deployed | ✅ Healthy |
| android-keystore-ref | Android signing keystore reference | Jan 2023 | Manual only | — | ⚠ HIGH — keystore rotation requires Play Store re-submission | ✅ Active |
| fcm-server-key | Firebase Cloud Messaging server key | Jan 2026 | Jan 2027 | 286 days | Medium — rotation requires FCM project key update | ✅ Healthy |

**Rotation Impact Legend (shown as help text):**
- HIGH: Mobile app release required before or simultaneous with key rotation — coordinate with Security Engineer at least 2 weeks before rotation date
- Medium: Service degradation possible during rotation; coordinate timing
- Low: Transparent to mobile app; no release coordination needed

**"Request Rotation Delay" button (Mobile Engineer only):**
If a rotation is due but a new mobile app release is not yet deployed, the Mobile Engineer can request a brief delay:
- Opens a request form: reason + proposed new rotation date (max 30-day extension)
- Request sent to Security Engineer for approval via platform notification
- Security Engineer approves/rejects from their Secrets view
- Approved delays recorded in `platform_secret_registry` and shown in the rotation calendar

**Rotation Coordination Checklist (shown 30 days before rotation due):**
The tab displays a coordination checklist for each upcoming HIGH-impact rotation:
- New app version with updated key support: deployed to App Store / Play Store?
- Minimum app version enforced (via force-update prompt)?
- Old key material will be retained in Secrets Manager AWSPREVIOUS for overlap window?
- Confirm with Security Engineer: rotation window selected outside exam hours?

**No secret values shown** — same masking policy as the rest of C-14. Mobile Engineers see only metadata.

---

## 14. Amendment — G18: Rotation Compliance Tab

**Assigned gap:** G18 — C-14 shows per-secret rotation history but has no aggregate view: overall compliance %, which secrets are overdue, secrets that have never been rotated. No bulk rotation trigger for overdue items.

**Where it lives:** New tab in the Secret & Key Manager page (alongside OAuth Apps and Mobile Keys).

---

### Rotation Compliance Tab

**Purpose:** Give the Security Engineer an aggregate compliance view across all secrets — not just individual secret health, but the platform's overall rotation discipline. Drive the compliance percentage to 100% before audits, and provide a bulk rotation trigger to clear overdue items efficiently.

**Compliance Summary Banner:**

Large top-of-tab banner showing the overall rotation compliance score:

- Overall compliance: **87%** (37/42 secrets within schedule)
- Broken down by category:
  - JWT Signing Keys: 100% (2/2)
  - Database Credentials: 100% (4/4)
  - Third-party API Keys: 75% (6/8 — 2 overdue)
  - OAuth Secrets: 100% (3/3)
  - Infrastructure: 67% (4/6 — 2 never rotated)
  - Mobile: 80% (4/5)
  - AI/ML Keys: 50% (2/4 — 2 overdue)

Colour: green ≥ 95% · amber 80–94% · red < 80%

---

**Compliance Detail Table:**

All secrets listed with compliance-focused columns:

| Secret Name | Category | Rotation Schedule | Last Rotated | Overdue By | Never Rotated | Compliance Status |
|---|---|---|---|---|---|---|
| jwt-access-signing-key | JWT | Quarterly | Feb 2026 | — | No | ✅ Compliant |
| cloudflare-api-token | Infrastructure | Annual | — | — | Yes | ❌ Never rotated |
| openai-api-key | AI/ML | Quarterly | Sep 2025 | 5 months | No | ❌ 5 months overdue |
| github-actions-pat | Infrastructure | Annual | Jan 2025 | 2 months | No | ❌ 2 months overdue |

**Status Values:**
- ✅ Compliant — rotated within schedule
- ⚠ Due soon — rotation due in < 30 days
- ❌ Overdue — past scheduled rotation date
- ❌ Never rotated — secret has never been rotated since creation (and rotation schedule is not "Never")
- ℹ Rotation = Never — justification on file (excluded from compliance %)

**Bulk Actions:**

"Trigger rotation for all overdue secrets" button:
- Only enabled for Security Engineer or Admin
- Opens confirmation modal listing all overdue secrets (names + overdue duration)
- User can uncheck specific secrets to exclude from bulk rotation
- On confirm: Celery job triggers standard rotation for each selected secret sequentially (not parallel — reduces simultaneous Lambda cold-start impact)
- Progress shown: "Rotating {n}/{total} overdue secrets"
- Each rotation requires 2FA — bulk rotation uses a single TOTP entry that covers all items in the batch (Security Engineer confirms once for the batch)
- Rotation history entry created per secret with "bulk_rotation_batch_{batch_id}" tag

**Compliance History Chart:**
- Monthly compliance % trend for the last 12 months (line chart)
- Shows improvement/regression over time
- Target line at 95% (platform compliance SLA)

**Audit Export:**
"Export compliance report" → CSV or PDF:
- All secrets with last rotation date, schedule, compliance status
- Overall compliance % + category breakdown
- Generated-by + timestamp + SHA-256 hash of report (for audit integrity)
- Used for annual VAPT evidence and internal security audits

---

## 15. Amendment — G19: JWT Compromise Response Section

**Assigned gap:** G19 — No guided workflow for responding to JWT signing key compromise. Security Engineer must manually execute 6 steps with no coordination or audit trail.

**Where it lives:** New dedicated section within the Secret Detail Drawer (Section 4) for JWT signing key secrets specifically. When a drawer is opened for a secret in the `jwt` category, an additional tab appears: **Compromise Response**.

---

### JWT Compromise Response Tab (in Secret Detail Drawer)

**Visible only for:** Secrets with `category = jwt` (jwt-access-signing-key, jwt-refresh-signing-key)

**Purpose:** Guide the Security Engineer through a structured, audited 6-step response to a JWT signing key compromise. Each step is checked off in sequence; partial completion is saved so the engineer can hand off to another admin without losing progress.

---

**Incident Context (top of tab):**

Before starting the response, the engineer documents the incident:
- Compromise type: Exposed in code · Leaked to logs · Phishing · Insider threat · Compromised service · Unknown
- Estimated time of compromise: date-time picker (used to scope affected sessions)
- Estimated blast radius: "Sessions created after {compromise time} may use tokens signed with the compromised key"
- Linked C-18 incident: select existing incident or "Create new incident" (auto-fills incident title)

---

**6-Step Response Checklist:**

Each step shows: status (Not started / In progress / Complete) · completed by · completed at · notes field

**Step 1 — Revoke compromised key (Emergency Rotation)**

- Triggers the Emergency Rotation workflow (Path B in Section 6)
- No overlap window — old key immediately invalidated in AWS Secrets Manager
- New key generated and deployed to AWSCURRENT
- Lambda warm pools flushed for all consuming services
- Step marked complete when Secrets Manager confirms new version active

**Step 2 — Bulk-invalidate affected sessions**

- Scope: all JTIs issued after the estimated compromise time
- Query: `platform_jwt_denied_tokens` + active session table — identify all tokens issued after compromise timestamp
- Batch-insert into `platform_jwt_denied_tokens` ORM deny-list with `expires_at` = now + 15 days
- Progress display: "Invalidating {n} tokens issued after {compromise_time}"
- On complete: all affected users must re-authenticate
- Step marked complete when batch insert confirmed

**Step 3 — Force re-login notification**

- Affected user count shown: "~12,400 sessions will be terminated"
- Notification options:
  - In-app message on next page load: "Your session has been reset due to a security update. Please log in again." (default — no detail about compromise)
  - Email notification: option to send SES email to all affected accounts
- "Send notification" button → Celery task sends notifications
- Step marked complete when notification Celery task completes

**Step 4 — CERT-In incident log**

- Checklist prompt: "Was any student or staff data accessed using the compromised key?"
  - Yes → CERT-In report required (6-hour deadline countdown starts from compromise time, not detection time)
  - No → Log as "contained — no confirmed data access" in CERT-In incident log
  - Unknown → Treat as Yes (conservative approach) — CERT-In report required
- "Open CERT-In Report Generator" button → links to C-13 G17 workflow pre-filled with this incident
- Step marked complete when CERT-In assessment documented (even if "No report needed")

**Step 5 — DPO email notification (if DPDPA breach)**

- If CERT-In step assessed as breach: DPDPA 72-hour notification also triggered
- DPO email draft: pre-filled from linked C-18 incident + step 1-2 data
- "Send DPO notification" → sends SES email to Data Protection Officer
- "Mark DPO notified" → if sent externally (outside platform)
- Step marked complete when DPO notification logged

**Step 6 — Verify new key rollout**

- Propagation status check: all consuming Lambda services must be on AWSCURRENT
- Shows Propagation Status tab data (same as Tab 3 in Secret Detail Drawer)
- All services must show "AWSCURRENT" status before step can be marked complete
- If any service still on AWSPREVIOUS after Lambda flush: "Force restart" button available here too
- Final verification: "Test JWT generation and validation" → platform generates a test JWT with new key + validates it (sanity check that new key is functioning correctly)
- Step marked complete when all services show AWSCURRENT + test JWT passes

---

**Completion:**

When all 6 steps are complete:
- Summary shown: "JWT compromise response complete — Duration: 22 min · All 6 steps verified"
- "Close response" button → archives the 6-step record to `platform_jwt_compromise_responses` table
- Linked C-18 incident auto-updated: "JWT compromise response complete" note added

**Data model:**

**platform_jwt_compromise_responses**

| Field | Type | Notes |
|---|---|---|
| id | UUID PK | |
| secret_id | UUID FK → platform_secret_registry | |
| incident_id | UUID FK → platform_security_incidents | nullable |
| compromise_type | ENUM | code_exposure/log_leak/phishing/insider/compromised_service/unknown |
| estimated_compromise_at | TIMESTAMPTZ | |
| tokens_invalidated | INTEGER | count of JTIs invalidated in step 2 |
| certIn_required | BOOLEAN | assessed in step 4 |
| dpdpa_required | BOOLEAN | assessed in step 5 |
| steps_completed | JSONB | per-step: status/completed_by/completed_at/notes |
| started_by | UUID FK → platform_staff | |
| started_at | TIMESTAMPTZ | |
| completed_at | TIMESTAMPTZ | nullable |
| total_duration_seconds | INTEGER | nullable |
