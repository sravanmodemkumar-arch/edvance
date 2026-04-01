# G-08 — Division Config

> **Route:** `/bgv/config/`
> **Division:** G — Background Verification
> **Primary Role:** BGV Manager (39) — full control over BGV policy settings
> **Supporting Roles:** POCSO Compliance Officer (41) — read; Platform Admin (10) — full
> **File:** `g-08-division-config.md`
> **Priority:** P2 — must be configured before BGV operations begin; infrequent changes thereafter

---

## 1. Page Name & Route

**Page Name:** Division Config
**Route:** `/bgv/config/`
**Part-load routes:**
- `/bgv/config/?part=verification-policy` — verification policy tab
- `/bgv/config/?part=document-requirements` — document requirements tab
- `/bgv/config/?part=sla-config` — SLA configuration tab
- `/bgv/config/?part=notification-config` — notification defaults tab
- `/bgv/config/?part=compliance-thresholds` — compliance thresholds tab
- `/bgv/config/?part=data-retention` — data retention & SCWC config tab
- `/bgv/config/?part=change-log` — change log tab

---

## 2. Purpose

G-08 is the settings page for Division G's operational policies. It controls the `bgv_operational_config` singleton and propagates settings to verification SLAs, compliance status calculations, renewal triggers, document requirements, and notification behaviours.

**Who needs this page:**
- BGV Manager (39) — configures BGV policy; adjusts for regulatory changes or vendor changes
- Platform Admin (10) — emergency overrides
- POCSO Compliance Officer (41) — reads to verify policy aligns with NCPCR requirements

**When is it used:**
- Initial platform setup (before first BGV request)
- Regulatory change (e.g. government extends BGV validity from 3 to 5 years)
- New document requirement mandated by law
- Vendor SLA change (contract renegotiation)
- Threshold adjustment after compliance audit

---

## 3. Tabs

| Tab | Label |
|---|---|
| 1 | Verification Policy |
| 2 | Document Requirements |
| 3 | SLA Configuration |
| 4 | Notification Config |
| 5 | Compliance Thresholds |
| 6 | Data Retention & SCWC Config |
| 7 | Change Log |

---

## 4. Section-Wise Detailed Breakdown

---

### Tab 1 — Verification Policy

Core BGV policy settings.

#### Section A — Validity & Renewal

| Setting | Control | Default | Notes |
|---|---|---|---|
| BGV validity period (years) | Number input | 3 | How long a CLEAR verification is valid before renewal required. Min 1, max 10. Regulatory default: 3 years per POCSO Act advisory. |
| Renewal reminder lead time (days) | Number input | 30 | How many days before expiry to send renewal reminder to institution. Min 7, max 90. |
| Second renewal reminder (days before expiry) | Number input | 7 | Second reminder sent this many days before expiry. 0 = disabled. |
| Grace period after expiry (days) | Number input | 0 | Platform policy: 0 grace — expired = non-compliant immediately. Can be set to max 14 days only with Platform Admin approval. |
| Auto-create renewal requests | Toggle (locked ON) | ON | Platform policy — system automatically creates renewal `bgv_verification` when lead time reached. Cannot be disabled. |

**Warning note:** "Changing BGV validity period applies only to new verifications marked CLEAR after the change. Existing CLEAR verifications retain their original expiry dates. Run a renewal pipeline audit (G-07 Tab 4) after changing this setting."

#### Section B — Re-Verification Triggers

| Setting | Control | Default | Notes |
|---|---|---|---|
| Auto-trigger re-verification on institution role change | Toggle | ON | If institution portal reports a staff role change that affects minor access, auto-creates RE_VERIFICATION request. |
| Auto-trigger re-verification on adverse media alert | Toggle | OFF | If ON: manual flag from BGV Executive creates a RE_VERIFICATION (aggressive setting — use with care). |
| Re-verification required after INCONCLUSIVE | Toggle (locked ON) | ON | Platform policy — INCONCLUSIVE result always triggers re-verification with a different vendor. Cannot be disabled. |

#### Section C — POCSO Specific Policy

| Setting | Control | Default | Notes |
|---|---|---|---|
| NCPCR reporting deadline (hours) | Number input (locked) | 24 | Platform policy per POCSO Act 2012. Cannot be changed. Shown for reference only. |
| POCSO case auto-create from vendor POCSO flag | Toggle (locked ON) | ON | When vendor result has `pocso_flag = true`, system auto-creates POCSO case. Cannot be disabled. |
| Suspend staff access on POCSO case creation | Toggle | OFF | If ON: staff institution portal access suspended automatically on POCSO case creation (before review). Aggressive. BGV Manager review required before enabling. |
| POCSO case closure requires NCPCR confirmation | Toggle (locked ON) | ON | Cannot close a POCSO case without `ncpcr_reported = true`. Platform policy. |

#### Section D — Vendor Defaults

| Setting | Control | Default | Notes |
|---|---|---|---|
| Default vendor | Searchable select | — | Pre-selected in G-02 vendor submission modal. Only ACTIVE + HEALTHY vendors shown. If default vendor is DOWN at submission time, operator must select manually. |
| Default checks | Multi-select checkboxes | CRIMINAL · ADDRESS · POLICE_CLEARANCE | Check types pre-selected in G-02 vendor modal for new verifications. Can be overridden per verification. |

**[Save Verification Policy]** ✅ "Verification policy saved — applies to new verifications" toast 4s.

---

### Tab 2 — Document Requirements

Configure which documents are required per verification type and institution type.

#### Document Requirements Matrix (Editable)

Rows = Document Types. Columns = Verification scope combinations.

| Document Type | INITIAL (All) | RENEWAL (All) | RE_VERIFICATION | Schools Only | Coaching Only |
|---|---|---|---|---|---|
| Government Photo ID (Aadhar/Passport/Voter ID) | ✅ Required | ✅ Required | ✅ Required | — | — |
| Address Proof | ✅ Required | Optional | ✅ Required | — | — |
| Police Clearance Certificate | ✅ Required | ✅ Required | ✅ Required | — | — |
| Court Clearance Certificate | Optional | — | ✅ Required | — | — |
| Prior Employer NOC | Optional | — | Optional | — | — |
| Education Certificate | Optional | — | — | ✅ Required | — |
| Recent Photograph | ✅ Required | ✅ Required | ✅ Required | — | — |

Each cell is a select: Required / Optional / Not Required.

**[Add Document Type]** — adds a new row. Fields: Document name, description, file types allowed (PDF/JPG/PNG), max size (MB).

**[Remove Document Type]** — only if no existing verifications use this document type.

**Validation:** At least one "Required" document per verification type.

**[Save Document Requirements]** — confirmation: "Changes apply to new verifications only. Existing in-progress verifications retain their original document checklist. Confirm?" ✅ "Document requirements saved" toast 4s.

---

### Tab 3 — SLA Configuration

SLA targets for each stage of the verification process.

#### Internal SLA Targets (BGV Team)

These are EduForge BGV team targets — independent of vendor SLA.

**SLA calculation method:** `sla_uses_working_days = true` by default. Working days = Monday–Friday IST, excluding Indian national public holidays. If set to false, SLA is calculated in calendar hours/days.

| Stage | SLA Target | Control | Default | Notes |
|---|---|---|---|---|
| Document collection (from request to docs complete) | Working days | Number input | 5 | If institution hasn't uploaded documents within N working days: overdue alert in G-02. |
| Document review (from docs received to ready for vendor) | Working hours | Number input | 4 | BGV Executive review SLA. |
| Vendor submission (from ready to vendor sent) | Working hours | Number input | 2 | Time from READY_FOR_VENDOR to VENDOR_SENT. |
| Result review (from vendor returned to final result) | Working hours | Number input | 8 | BGV Executive + Supervisor review after vendor returns result. |
| FLAGGED notification to institution | Hours | Number input | 24 | After Supervisor approves FLAGGED: BGV Manager must notify institution within N hours. Calendar hours (not working hours) — urgency. |
| SLA calculation mode | Toggle | Working days (ON) | ON = working days Mon–Fri IST; OFF = calendar days/hours. |

**Validation:** Each SLA must be ≥ 1 (except document collection which is in days, min 1).

#### Platform-Total SLA (End-to-End)

Calculated automatically:
`Total SLA = document_collection_days × 24h + document_review_hours + vendor_sla_hours + result_review_hours`

Shown as read-only: "Expected end-to-end turnaround: **~{N} working days** (at default vendor SLA)."

**SLA escalation:** If a verification breaches an internal SLA stage:
- Overdue in G-02 queue
- In-app notification to BGV Ops Supervisor (92)
- BGV Manager notified if overdue by 2× the SLA

**[Save SLA Config]** ✅ "SLA targets updated — applies to new verifications" toast 4s.

---

### Tab 4 — Notification Config

Controls for BGV-related notifications sent to institution admins.

#### Notification Templates

| Notification | Channel | Template | Editable |
|---|---|---|---|
| BGV request created (new staff) | In-app | Fixed system message | No |
| Document reminder (first) | In-app + Email | Custom template | Yes |
| Document reminder (second — 5 days after first) | In-app | Fixed | No |
| Renewal reminder (lead time) | In-app + Email | Custom template | Yes |
| Second renewal reminder (7 days) | In-app | Fixed | No |
| BGV CLEAR notification | In-app | Fixed system message | No |
| BGV FLAGGED notification | In-app + Email (formal) | Custom template | Yes |
| POCSO case — institution notification | Email + Formal Notice | Custom template | Yes — Legal review recommended |

For editable templates: textarea with variables (`{institution_name}`, `{staff_ref}`, `{expiry_date}`, etc.). Variable list shown inline.

**[Save Notification Config]** ✅ "Notification templates saved" toast 4s.

#### Notification Delivery Settings

| Setting | Control | Default |
|---|---|---|
| Enable email notifications | Toggle | ON |
| Email from address | Text | `bgv@eduforge.com` |
| Enable in-app notifications | Toggle (locked ON) | ON — cannot be disabled |
| Send notification copy to BGV Manager | Toggle | ON |

---

### Tab 5 — Compliance Thresholds

Thresholds that determine institution `compliance_status` in G-04 and G-01.

#### Compliance Status Rules

| Setting | Control | Default | Notes |
|---|---|---|---|
| COMPLIANT threshold (coverage %) | Number (locked) | 100 | Platform policy — only 100% is COMPLIANT per POCSO Act. Cannot be lowered. |
| AT_RISK lower bound (coverage %) | Number input | 80 | If `coverage_pct` is between this and 99%: AT_RISK. Must be < 100 and > NON_COMPLIANT threshold. |
| NON_COMPLIANT upper bound (coverage %) | Number input | 79 | If `coverage_pct` ≤ this value: NON_COMPLIANT. Must be < AT_RISK lower bound. |
| Include EXPIRED in non-compliant calculation | Toggle (locked ON) | ON | Expired verifications count against coverage. Cannot be disabled. |
| Auto-escalate NON_COMPLIANT after (days) | Number input | 14 | If institution remains NON_COMPLIANT for N days: auto-sets compliance_status = ESCALATED and notifies Customer Success. 0 = disabled. |

**Validation:** AT_RISK lower bound > NON_COMPLIANT upper bound (otherwise gap in thresholds).

**Impact note:** "Threshold changes apply immediately. All `bgv_institution_compliance` records are recomputed on next nightly Celery run or immediately via [Recalculate Now]."

**[Recalculate Compliance Now]** (BGV Manager, Platform Admin): Triggers immediate Celery task `recalculate_bgv_institution_compliance`. Progress shown: "Recalculating {N} institutions…" ✅ "Compliance status recalculated for all institutions" toast when complete.

**[Save Compliance Thresholds]** ✅ "Compliance thresholds saved" toast 4s.

#### Automation Task Health (read-only)

Live status of Celery tasks powering Division G automation.

| Task | Schedule | Last Run | Next Run | Status |
|---|---|---|---|---|
| `update_bgv_institution_compliance` | Nightly 23:00 IST | {datetime} | Next 23:00 IST | ✅ OK / ❌ FAILED |
| `snapshot_bgv_compliance_trend` | Nightly 23:30 IST | {datetime} | Next 23:30 IST | ✅ OK / ❌ FAILED |
| `check_bgv_vendor_health` | Every 30 minutes | {datetime} | {datetime} | ✅ OK / ❌ FAILED |
| `auto_create_bgv_renewals` | Nightly 01:00 IST | {datetime} | Next 01:00 IST | ✅ OK / ❌ FAILED |
| `monitor_pocso_case_sla` | Hourly | {datetime} | {datetime} | ✅ OK / ❌ FAILED |
| `auto_escalate_noncompliant_institutions` | Nightly 07:00 IST | {datetime} | Next 07:00 IST | ✅ OK / ❌ FAILED |
| `notify_manager_flagged_pending` | Hourly | {datetime} | {datetime} | ✅ OK / ❌ FAILED |
| `retry_failed_vendor_submissions` | Hourly | {datetime} | {datetime} | ✅ OK / ❌ FAILED |
| `archive_and_purge_old_bgv_records` | Monthly (1st, 03:00 IST) | {datetime} | Next 1st 03:00 | ✅ OK / ❌ FAILED |

Stale detection: if `last_run` > 2× expected interval and task hasn't run: ⚠️ amber "Expected to run — may be delayed."

Refreshed every 60s via HTMX.

[View Celery Logs] (Platform Admin only): read-only log drawer, last 20 executions per task.

#### Celery Task Reference

**`notify_manager_flagged_pending`** — Hourly
- **Inputs:** Verifications where `status = AWAITING_SUPERVISOR_REVIEW` and `updated_at < now() - result_review_sla_hours`
- **Outputs:** In-app notification to BGV Manager (39): "FLAGGED verification {staff_ref} at {institution} has been awaiting Supervisor approval for {N}h. SLA: {flagged_notify_sla_hours}h."
- **Dedup:** Only one notification per verification per 4-hour window. Clears when `status` transitions out of AWAITING_SUPERVISOR_REVIEW.

**`retry_failed_vendor_submissions`** — Hourly
- **Inputs:** Verifications where `status = VENDOR_SENT` AND `last_submission_error IS NOT NULL` AND `submission_attempt_count < 3`
- **Outputs:** Retries vendor API call; on success: clears `last_submission_error`; on failure: increments `submission_attempt_count`. If `submission_attempt_count = 3`: status reverts to `READY_FOR_VENDOR`, in-app alert sent to assigned BGV Executive and BGV Ops Supervisor: "Vendor submission failed after 3 attempts for {staff_ref}. Manual resubmission required."
- **Dedup:** Exponential backoff: attempt 1 at 1h, attempt 2 at 2h, attempt 3 at 4h from first failure.

**`auto_create_bgv_renewals`** — Nightly 01:00 IST
- **Inputs:** `bgv_staff` where `current_verification.expiry_date ≤ today + bgv_operational_config.renewal_lead_days` AND no active RENEWAL or RE_VERIFICATION in progress (`bgv_verification.status NOT IN (DOCUMENTS_PENDING, DOCUMENTS_RECEIVED, READY_FOR_VENDOR, VENDOR_SENT, VENDOR_RETURNED, AWAITING_SUPERVISOR_REVIEW)`)
- **Outputs:** Creates `bgv_verification` (type: RENEWAL, status: DOCUMENTS_PENDING, assigned_to_id: NULL). Sends notification to institution admin. Sends in-app summary to BGV Ops Supervisor (92): "{N} renewal requests created tonight — {M} queued for assignment."

**`update_bgv_institution_compliance`** — Nightly 23:00 IST + real-time triggers
- **Real-time trigger:** Fires on `bgv_verification.final_result` change (CLEAR / FLAGGED / INCONCLUSIVE / CANCELLED) and on `bgv_staff.bgv_status` change. Recalculates only the affected institution's `bgv_institution_compliance` record.
- **Nightly full pass:** Recalculates all institutions — catches expiry rollovers, deactivated staff, bulk imports from the day.
- Memcached cache for G-04/G-01: invalidated on real-time trigger; TTL 5 min otherwise.

---

### Tab 6 — Data Retention & SCWC Config

#### Section A — Data Retention Policy

DPDPA 2023 compliance. Controls when BGV records are purged or anonymised. Celery `archive_and_purge_old_bgv_records` runs monthly.

| Record Type | Retention | Control | Default | Notes |
|---|---|---|---|---|
| CLEAR verifications (after expiry) | Years | Number input | 3 | Documents purged from R2 at expiry + N years. Record anonymised (name → [REDACTED]). |
| FLAGGED verifications (non-POCSO) | Years | Number input | 5 | — |
| INCONCLUSIVE verifications | Years | Number input | 3 | — |
| POCSO cases (post-closure) | Years (locked) | 10 | Regulatory minimum — cannot be reduced. Record retained, anonymised only on court order. |
| Vendor API transaction logs | Years | Number input | 2 | Payload hash purged; counts retained for performance reports. |
| Audit log entries | Years (locked) | 7 | Cannot be reduced — legal requirement. |

**Note on purge process:** Purge replaces `bgv_staff.full_name` with `[REDACTED]`, removes all `bgv_document.file_url` references (R2 files deleted), and logs a `DATA_PURGED` entry in `bgv_audit_log`. Counts and outcome data are retained for compliance reporting.

**[Save Retention Config]** ✅ "Retention policy saved" toast 4s.

#### Section B — State Child Welfare Committee (SCWC) Contacts

POCSO cases require SCWC notification per the institution's state jurisdiction. Configure SCWC contact info per state.

| Column | Notes |
|---|---|
| State | Indian state name |
| SCWC Name | Full committee name |
| Contact Email | — |
| Portal URL | SCWC reporting portal URL (if available) |
| Notes | Any special reporting procedures |

**[+ Add State SCWC]** — add a row for a state. [Edit] [Delete] per row.

Minimum required: states where EduForge has registered institutions. BGV Manager and POCSO Officer should review against current institution distribution.

**[Save SCWC Config]** ✅ "SCWC contacts saved" toast 3s.

---

### Tab 7 — Change Log

Read-only audit trail of all configuration changes.

#### Filter Bar

| Filter | Control |
|---|---|
| Tab | Multiselect: Verification Policy · Document Requirements · SLA · Notifications · Compliance Thresholds |
| Changed By | Role label filter |
| Date Range | — |

#### Change Log Table

| Column | Sortable | Notes |
|---|---|---|
| Timestamp | Yes (default: DESC) | — |
| Tab / Setting | No | e.g. "Verification Policy — BGV Validity Period" |
| Change | No | "{Before} → {After}" |
| Changed By | No | Role label (DPDPA) |

Pagination: 25 rows. [Export Change Log CSV].

---

## 5. Data Model Reference

**`bgv_operational_config`** — singleton; one record. All fields from all tabs stored here.

| Field | Type | Notes |
|---|---|---|
| `id` | int | Always 1 |
| `validity_years` | int | — |
| `renewal_lead_days` | int | — |
| `second_reminder_days` | int | — |
| `expiry_grace_days` | int | — |
| `doc_collection_sla_days` | int | — |
| `doc_review_sla_hours` | int | — |
| `vendor_submission_sla_hours` | int | — |
| `result_review_sla_hours` | int | — |
| `flagged_institution_notify_sla_hours` | int | — |
| `at_risk_threshold_pct` | decimal | Lower bound for AT_RISK |
| `noncompliant_threshold_pct` | decimal | Upper bound for NON_COMPLIANT |
| `auto_escalate_noncompliant_days` | int | 0 = disabled |
| `auto_suspend_on_pocso_create` | boolean | — |
| `notify_email_enabled` | boolean | — |
| `notify_copy_to_manager` | boolean | — |
| `updated_at` | timestamptz | — |
| `updated_by_id` | FK → auth.User | — |

**`bgv_document_requirement`** — one row per document type per verification scope.

**`bgv_config_log`** — change log entries (same structure as `exam_operational_config_log`).

---

## 6. Access Control

| Gate | Rule |
|---|---|
| Page access | BGV Manager (39), POCSO Compliance Officer (41), Platform Admin (10) |
| Edit all settings | BGV Manager (39), Platform Admin (10) |
| Read-only | POCSO Compliance Officer (41) |
| "Read-only access" banner | POCSO Compliance Officer (41) |
| Locked settings (platform policy) | Visible but non-editable for all roles. Tooltip: "This is a platform policy and cannot be changed." |
| [Recalculate Compliance Now] | BGV Manager (39), Platform Admin (10) |
| [View Celery Logs] | Platform Admin (10) only |

---

## 7. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| BGV validity reduced (e.g. 3 years → 2 years) | Warning: "Reducing validity period will not retroactively expire existing CLEAR verifications. Only new CLEAR verifications will receive {N}-year expiry." |
| AT_RISK threshold set ≥ NON_COMPLIANT threshold | Validation block: "AT_RISK lower bound ({N}%) must be greater than NON_COMPLIANT threshold ({M}%)." |
| Document requirement added when in-progress verifications exist | Warning: "This document type will only be required for verifications created after this change. {N} in-progress verifications will not require it." |
| Grace period set > 14 days by non-Platform Admin | Blocked: "Grace period cannot exceed 14 days per POCSO Act compliance policy. Contact Platform Admin." |
| Celery task FAILED | Red badge in automation health panel. In-app notification to BGV Manager (39) and Platform Admin (10). |
| Config saved during active BGV processing | Settings saved immediately. Toasts note where applicable that changes affect new verifications only. |
| POCSO locked settings modified attempt | Fields are visually locked (`opacity-60 cursor-not-allowed` with lock icon). Tooltip: "This is a POCSO Act platform policy." Even Platform Admin cannot change these specific locked fields. |

---

## 8. UI Patterns

### Forms with Validation
- Required fields: red border + "Required" on blur
- Range errors: "Must be between {min} and {max}"
- Interdependency errors: inline per field
- Locked fields: `opacity-60 cursor-not-allowed` with lock icon + tooltip

### Toasts
| Action | Toast |
|---|---|
| Verification policy saved | ✅ "Verification policy saved — applies to new verifications" (4s) |
| Document requirements saved | ✅ "Document requirements saved" (4s) |
| SLA targets saved | ✅ "SLA targets updated" (4s) |
| Notification config saved | ✅ "Notification templates saved" (4s) |
| Compliance thresholds saved | ✅ "Compliance thresholds saved" (4s) |
| Compliance recalculated | ✅ "Compliance status recalculated for all institutions" (5s) |

### Loading States
- Each tab: form skeleton (label + input shimmer × 6 rows)
- Automation health panel: table row shimmer × 6

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Two-column form (label left, input right) |
| Tablet | Single-column form |
| Mobile | Single-column; read-only recommendation banner: "Settings are best edited on desktop" |

---

*Page spec complete.*
*G-08 covers: 6-tab config page → verification policy (validity, renewal lead, POCSO-locked rules) → document requirements matrix (per verification type and institution type) → internal SLA targets per stage → notification templates and delivery settings → compliance status thresholds with live recalculate → automation task health panel (6 Celery tasks) → change log.*
