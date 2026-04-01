# Division G — Background Verification: Pages List

> **Division:** G — Background Verification
> **Roles:** BGV Manager (39) · BGV Executive (40) · POCSO Compliance Officer (41) · BGV Operations Supervisor (92)
> **Cross-access:** Platform Admin (10) full access all pages · Legal Officer (75) read on G-06 G-07 · DPO (76) read on G-07 · POCSO Reporting Officer (78) full access G-06 G-07
> **Total pages:** 8
> **Scale:** 1,900+ institutions · ~28,000 staff members requiring BGV · POCSO Act 2012 mandatory compliance

**Critical context:**
Any EduForge institution staff member with minor access who passes an unverified BGV is a direct legal liability under POCSO Act 2012. A BGV Executive who marks CLEAR without vendor confirmation, or a POCSO case that goes unreported to NCPCR, exposes EduForge to criminal liability. This division owns the most sensitive personal data on the platform — name, ID documents, police records of real employees. Every action must be audited. Wrong decisions cannot be recalled from NCPCR.

---

## Scale Context

| Segment | Institutions | Avg Staff with Minor Access | Total Staff |
|---|---|---|---|
| Schools | 1,000 | ~15 | ~15,000 |
| Colleges | 800 | ~10 | ~8,000 |
| Coaching Centres | 100 | ~50 | ~5,000 |
| **Total** | **1,900+** | — | **~28,000+** |

**BGV load profile:**
- BGV valid for 3 years (configurable in G-08)
- ~9,300 renewals per year at steady state (28,000 ÷ 3)
- New institution onboarding: ~200/year → +~3,000 new BGV requests/year
- Peak queue: first 6 months post-launch — entire existing staff base needs initial verification
- Vendor turnaround: 3–7 working days per verification (typical)
- Documents required per staff: 3–5 (ID proof, address proof, police clearance, prior employer NOC, education certificate)

---

## Roles

| # | Role | Level | Division Scope |
|---|---|---|---|
| 39 | BGV Manager | 3 | BGV policy, vendor management, escalation to institutions, POCSO oversight |
| 40 | BGV Executive | 3 | Process BGV requests, document review, vendor submission, status updates |
| 41 | POCSO Compliance Officer | 1 | Audit BGV coverage across all institutions, NCPCR mandatory reporting, read-only |
| 92 | BGV Operations Supervisor | 3 | Approve FLAGGED decisions before institution notification; queue management; BGV Executive oversight |

**Role 92 rationale:** A BGV Executive (40) cannot unilaterally FLAG a staff member — that decision suspends employment and notifies the institution. A FLAGGED decision without supervisor review risks wrongful employment action and legal challenge. BGV Operations Supervisor (92) is the mandatory approval gate for all FLAGGED outcomes and POCSO auto-escalations before external notification.

---

## Pages

| Page | Name | Route | File | Priority |
|---|---|---|---|---|
| G-01 | BGV Dashboard | `/bgv/` | `g-01-bgv-dashboard.md` | P0 |
| G-02 | Staff Verification Queue | `/bgv/queue/` | `g-02-staff-verification-queue.md` | P0 |
| G-03 | Staff BGV Record | `/bgv/staff/{staff_id}/` | `g-03-staff-record.md` | P0 |
| G-04 | Institution Compliance Tracker | `/bgv/institutions/` | `g-04-institution-compliance-tracker.md` | P1 |
| G-05 | Vendor Management | `/bgv/vendors/` | `g-05-vendor-management.md` | P1 |
| G-06 | POCSO Case Management | `/bgv/pocso/` | `g-06-pocso-case-management.md` | P0 |
| G-07 | Compliance Reports | `/bgv/reports/` | `g-07-compliance-reports.md` | P1 |
| G-08 | Division Config | `/bgv/config/` | `g-08-division-config.md` | P2 |

---

## Role-to-Page Access Matrix

| Role | G-01 Dashboard | G-02 Queue | G-03 Staff Record | G-04 Institutions | G-05 Vendors | G-06 POCSO | G-07 Reports | G-08 Config |
|---|---|---|---|---|---|---|---|---|
| BGV Manager (39) | **Full** | Read + assign | Read + approve FLAGGED | **Full** | **Full** | Read + escalate | **Full** | **Full** |
| BGV Executive (40) | Read (own queue KPIs) | **Full** (own items) | **Full** (own items) | Read | — | Read (assigned cases) | Read | — |
| POCSO Compliance Officer (41) | Read (compliance tiles only) | — | Read | Read | — | **Full** | **Full** | — |
| BGV Ops Supervisor (92) | **Full** | **Full** | **Full** | Read | Read | Read + approve | Read | — |
| Platform Admin (10) | Full | Full | Full | Full | Full | Full | Full | Full |
| Legal Officer (75) | — | — | — | — | — | Read | Read | — |
| DPO (76) | — | — | — | — | — | — | Read | — |
| POCSO Reporting Officer (78) | — | — | — | — | — | **Full** | **Full** | — |

---

## Division G — Critical Action Ownership

| Action | Owner | Gate |
|---|---|---|
| Approve FLAGGED verification outcome | BGV Ops Supervisor (92) | Mandatory before institution notification |
| Send institution FLAGGED notification | BGV Manager (39) | After Supervisor approval |
| Auto-escalate POCSO flag → POCSO case | System (Celery) | When `pocso_flag = true` on vendor result |
| Report case to NCPCR | POCSO Compliance Officer (41) / POCSO Reporting Officer (78) | After case review |
| Notify institution of POCSO case | POCSO Compliance Officer (41) | After NCPCR report filed |
| Suspend institution staff access | BGV Manager (39) | After FLAGGED approval or POCSO case |
| Escalate non-compliant institution | BGV Manager (39) | When `compliance_status = NON_COMPLIANT` |
| Activate new BGV vendor | BGV Manager (39) | After API test passes |
| Export NCPCR mandatory annual report | POCSO Compliance Officer (41) | Annual — regulatory deadline |

---

## BGV Workflow — End to End

```
Institution submits BGV request (via portal) OR BGV Executive creates manually
        ↓
bgv_verification created — status: DOCUMENTS_PENDING
        ↓
Documents collected from institution (uploaded by BGV Executive or institution portal)
        ↓
BGV Executive reviews documents: complete / incomplete
        ↓ (incomplete)
Institution notified → document reminder → wait
        ↓ (complete)
BGV Executive submits to vendor → vendor_sent_at recorded
        ↓
Vendor processes (3–7 days SLA)
        ↓
Vendor returns result via webhook / API poll
        ↓ CLEAR ──────────────────────────────────────────────→ bgv_staff.bgv_status = CLEAR
        ↓ FLAGGED (non-POCSO)                                    expiry_date set
BGV Ops Supervisor reviews → approves / rejects FLAGGED decision
        ↓ approved FLAGGED
BGV Manager reviews → institution notified → employment action decision
        ↓ FLAGGED with POCSO offense
Celery auto-creates bgv_pocso_case → POCSO Compliance Officer alerted
        ↓
POCSO Officer reviews → NCPCR report filed → institution notified
        ↓
Case closed (employment action confirmed)
```

**Renewal workflow:**
- Celery nightly job: identifies verifications with `expiry_date ≤ today + 30 days`
- Creates renewal `bgv_verification` (type: RENEWAL) with status DOCUMENTS_PENDING
- Institution notified; existing CLEAR status retained until renewal result

---

## Integration Points — Division G

| Integration | Direction | What Flows |
|---|---|---|
| **Institution Portal** | Portal → G-02 | Institution submits BGV requests for staff; uploads documents |
| **Div C — Engineering** | G-05 → C | DevOps provisions vendor API credentials; webhook endpoints |
| **Div N — Legal & Compliance** | G-06 ↔ N | POCSO cases reviewed by Legal Officer (75); POCSO Reporting Officer (78) files NCPCR reports |
| **Div A — BGV Compliance (36)** | G-01 → A-36 | BGV compliance status rolled up to executive dashboard |
| **Div I — Customer Support** | G-04 → I | Non-compliant institution escalations handed to Customer Success for follow-up |
| **BGV Vendors (AuthBridge, IDfy, etc.)** | G-05 ↔ Vendors | Document verification, criminal record check, police clearance via vendor API |
| **NCPCR Portal** | G-06 → NCPCR | Mandatory POCSO case reporting; case reference numbers stored |
| **AWS S3 / R2** | G-03 ↔ Storage | Staff documents stored in private R2 bucket; signed URLs for access |

---

## Data Models — Division G (Shared Reference)

All Division G models live in the **`bgv` app** (shared schema). Staff documents stored in private R2 bucket — never public CDN.

---

### `bgv_staff`

The master record for a staff member requiring BGV.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `institution_id` | int | Institution reference |
| `institution_type` | varchar | Enum: `SCHOOL` · `COLLEGE` · `COACHING` |
| `staff_ref` | varchar(30) | Anonymised platform ref: `BGV-{inst_code}-{seq}`. Used in all DPDPA-sensitive UI. |
| `full_name` | varchar(200) | Encrypted at rest (AES-256). Decrypted only for authorised roles. |
| `role_title` | varchar(200) | Staff's job role at institution |
| `department` | varchar(200) | — |
| `date_of_joining` | date | — |
| `has_minor_access` | boolean | Whether this staff member has physical/digital access to minors |
| `bgv_status` | varchar | Enum: `NOT_INITIATED` · `DOCUMENTS_REQUESTED` · `DOCUMENTS_RECEIVED` · `UNDER_REVIEW` · `VENDOR_SENT` · `VENDOR_RETURNED` · `CLEAR` · `FLAGGED` · `INCONCLUSIVE` · `EXPIRED` · `SUSPENDED` |
| `current_verification_id` | FK → `bgv_verification` | Latest active verification |
| `person_id` | UUID | Nullable — shared across multiple `bgv_staff` records if same individual works at multiple institutions. Dedup key: `full_name_hash + date_of_joining`. If two institutions submit the same person (name + DOB match), system prompts BGV Executive: "Possible duplicate: {institution_name} has a matching staff record. Link as same person?" Linking shares verification history but keeps institution-specific BGV. POCSO flag on any linked record: all linked records flagged. |
| `institution_bgv_ref` | varchar(100) | Institution's own HR reference for this staff |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

---

### `bgv_verification`

One BGV run for a staff member. A staff member may have multiple verifications over time (initial, renewal, re-verification).

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `staff_id` | FK → `bgv_staff` | — |
| `verification_type` | varchar | Enum: `INITIAL` · `RENEWAL` · `RE_VERIFICATION` |
| `status` | varchar | Workflow state enum: `DOCUMENTS_PENDING` · `DOCUMENTS_RECEIVED` · `READY_FOR_VENDOR` · `VENDOR_SENT` · `VENDOR_RETURNED` · `AWAITING_SUPERVISOR_REVIEW` · `COMPLETE` · `CANCELLED`. Updated at each workflow stage. |
| `initiated_by_id` | FK → auth.User | BGV Executive (40) or system (Celery for renewal) |
| `initiated_at` | timestamptz | — |
| `assigned_to_id` | FK → auth.User | BGV Executive assigned to process this verification |
| `vendor_id` | FK → `bgv_vendor` | Nullable — set when sent to vendor |
| `vendor_request_ref` | varchar(100) | Vendor's tracking ID |
| `vendor_sent_at` | timestamptz | Nullable |
| `vendor_returned_at` | timestamptz | Nullable |
| `vendor_result` | varchar | Enum: `PENDING` · `CLEAR` · `FLAGGED` · `INCONCLUSIVE` · `ERROR` |
| `vendor_result_detail` | text | Vendor-provided result summary (normalized from vendor schema) |
| `vendor_result_document_url` | varchar | R2 private URL — vendor report PDF |
| `submission_attempt_count` | int | Default 0 — incremented on each vendor API call attempt |
| `last_submission_error` | text | Nullable — last vendor API error message; cleared on success |
| `pocso_flag` | boolean | Default false. Set via two paths: (1) vendor webhook sets `pocso_flag=true` in result → Celery auto-creates `bgv_pocso_case`; (2) BGV Ops Supervisor checks POCSO checkbox during FLAGGED approval → sets flag → Celery creates case. Deduplication: Celery checks for existing open case on same `staff_id + verification_id` before creating. |
| `pocso_offense_type` | varchar(300) | Nullable — filled when `pocso_flag = true` |
| `reviewed_by_id` | FK → auth.User | BGV Ops Supervisor who approved final decision |
| `reviewed_at` | timestamptz | Nullable |
| `final_result` | varchar | Enum: `PENDING` · `CLEAR` · `CLEAR_OVERRIDE` · `FLAGGED` · `INCONCLUSIVE` · `CANCELLED`. `CLEAR_OVERRIDE` = supervisor overrode vendor FLAGGED to CLEAR; flagged in audit log. |
| `doc_collection_sla_due_at` | timestamptz | Set at initiation: `initiated_at + bgv_config.doc_collection_sla_days` (working days). Used for overdue alert in G-02 Docs Pending tab. |
| `doc_review_sla_due_at` | timestamptz | Set when `status → DOCUMENTS_RECEIVED`: `+bgv_config.doc_review_sla_hours`. Used for overdue alert in G-02 Documents Received tab. |
| `vendor_submission_sla_due_at` | timestamptz | Set when `status → READY_FOR_VENDOR`: `+bgv_config.vendor_submission_sla_hours`. |
| `result_review_sla_due_at` | timestamptz | Set when `status → VENDOR_RETURNED`: `+bgv_config.result_review_sla_hours`. |
| `flagged_notify_sla_due_at` | timestamptz | Set when `status → AWAITING_SUPERVISOR_REVIEW`: `+bgv_config.flagged_notify_sla_hours`. Used by `notify_manager_flagged_pending` task. |
| `sla_due_at` | timestamptz | Overall end-to-end SLA: `initiated_at + sum of all stage SLAs + vendor.sla_hours`. Used for the SLA column in G-02 queue table countdown. |
| `expiry_date` | date | Nullable — set when `final_result IN (CLEAR, CLEAR_OVERRIDE)`; `clear_date + bgv_config.validity_years` |
| `renewal_notified` | boolean | Whether renewal reminder sent |
| `renewal_notified_at` | timestamptz | Nullable |
| `version` | int | Default 1 — incremented on each save; used for optimistic locking in supervisor approval modal |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |

---

### `bgv_document`

Documents submitted for a verification.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `verification_id` | FK → `bgv_verification` | — |
| `document_type` | varchar | Enum: `AADHAR` · `PAN` · `PASSPORT` · `VOTER_ID` · `POLICE_CLEARANCE` · `COURT_CLEARANCE` · `PRIOR_EMPLOYER_NOC` · `EDUCATION_CERTIFICATE` · `PHOTO_ID` · `OTHER` |
| `file_url` | varchar | R2 private bucket URL |
| `file_name` | varchar | Original filename |
| `file_size_kb` | int | — |
| `uploaded_by_id` | FK → auth.User | — |
| `uploaded_at` | timestamptz | — |
| `verified` | boolean | Default false |
| `verified_by_id` | FK → auth.User | BGV Executive who marked document as verified |
| `verified_at` | timestamptz | Nullable |
| `rejection_reason` | varchar(500) | Nullable — filled if document is rejected (expired, unclear, wrong type) |

---

### `bgv_vendor`

BGV verification service providers.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `name` | varchar(200) | e.g. "AuthBridge Research Services" |
| `code` | varchar(10) | Short code e.g. `AUTHB`, `IDFY` |
| `api_base_url` | varchar | — |
| `api_key_encrypted` | text | AES-256 encrypted at rest |
| `webhook_secret_encrypted` | text | HMAC secret for webhook signature verification |
| `status` | varchar | Enum: `ACTIVE` · `INACTIVE` · `SUSPENDED` |
| `sla_hours` | int | Expected turnaround (contractual SLA in hours) |
| `supported_checks` | varchar[] | Array: `CRIMINAL` · `ADDRESS` · `EMPLOYMENT` · `EDUCATION` · `POCSO_REGISTRY` · `COURT_RECORD` |
| `contact_name` | varchar | Account manager at vendor |
| `contact_email` | varchar | — |
| `contact_phone` | varchar | — |
| `last_health_check_at` | timestamptz | — |
| `health_status` | varchar | Enum: `HEALTHY` · `DEGRADED` · `DOWN` · `UNKNOWN` |
| `created_at` | timestamptz | — |
| `notes` | text | Internal notes (contract terms, known limitations) |

---

### `bgv_institution_compliance`

Materialised compliance snapshot per institution. Updated by Celery nightly and on any verification status change.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `institution_id` | int | — |
| `total_staff_with_minor_access` | int | — |
| `bgv_not_initiated` | int | — |
| `bgv_in_progress` | int | DOCUMENTS_REQUESTED through VENDOR_SENT |
| `bgv_complete_clear` | int | — |
| `bgv_flagged` | int | — |
| `bgv_expired` | int | `expiry_date < today` |
| `coverage_pct` | decimal(5,2) | `bgv_complete_clear / total_staff_with_minor_access × 100` |
| `compliance_status` | varchar | Enum: `COMPLIANT` · `AT_RISK` · `NON_COMPLIANT` · `ESCALATED` |
| `last_updated_at` | timestamptz | — |
| `escalated_at` | timestamptz | Nullable |
| `escalated_by_id` | FK → auth.User | Nullable |
| `escalation_note` | text | Nullable |

**Compliance status thresholds** (configurable in G-08):
- `COMPLIANT` — coverage_pct = 100% and no EXPIRED
- `AT_RISK` — coverage_pct ≥ 80% OR any EXPIRED in last 30 days
- `NON_COMPLIANT` — coverage_pct < 80%
- `ESCALATED` — manually escalated by BGV Manager

---

### `bgv_pocso_case`

POCSO Act 2012 — flagged staff with child protection offences.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `case_ref` | varchar(25) | Format: `POCSO-{YYYYMMDD}-{5-digit-seq}` e.g. `POCSO-20260321-00001` |
| `verification_id` | FK → `bgv_verification` | Source verification |
| `staff_id` | FK → `bgv_staff` | — |
| `offense_type` | varchar(300) | e.g. "Sexual assault under POCSO Section 4" |
| `offense_date` | date | Nullable — if known from vendor report |
| `offense_jurisdiction` | varchar(200) | Court/police jurisdiction |
| `source` | varchar | Enum: `BGV_VENDOR` · `MANUAL_FLAG` · `ANONYMOUS_TIP` |
| `action_status` | varchar | Enum: `OPEN` · `UNDER_REVIEW` · `INSTITUTION_NOTIFIED` · `NCPCR_REPORTED` · `POLICE_REPORTED` · `EMPLOYMENT_SUSPENDED` · `CLOSED` |
| `institution_notified` | boolean | Default false |
| `institution_notified_at` | timestamptz | Nullable |
| `institution_notification_method` | varchar | Enum: `EMAIL` · `IN_APP` · `PHONE_CALL` · `FORMAL_NOTICE` |
| `ncpcr_reported` | boolean | Default false |
| `ncpcr_ref` | varchar(100) | NCPCR case reference number; `PENDING` if report filed but ref not yet received |
| `ncpcr_reported_at` | timestamptz | Nullable |
| `police_reported` | boolean | Default false — FIR filed with local police per POCSO Section 19(1) |
| `fir_ref` | varchar(100) | FIR number from local police station |
| `fir_filed_at` | timestamptz | Nullable |
| `police_station` | varchar(200) | Police station name and jurisdiction |
| `scwc_reported` | boolean | Default false — State Child Welfare Committee notified per jurisdiction |
| `scwc_ref` | varchar(100) | SCWC reference number |
| `scwc_reported_at` | timestamptz | Nullable |
| `handled_by_id` | FK → auth.User | POCSO Compliance Officer (41) or POCSO Reporting Officer (78) |
| `created_at` | timestamptz | — |
| `updated_at` | timestamptz | — |
| `closed_at` | timestamptz | Nullable |
| `closure_reason` | text | Nullable |

---

### `bgv_audit_log`

Immutable audit trail for all BGV actions. Append-only — no updates or deletes.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `entity_type` | varchar | Enum: `STAFF` · `VERIFICATION` · `DOCUMENT` · `VENDOR` · `POCSO_CASE` · `INSTITUTION` · `CONFIG` |
| `entity_id` | UUID | — |
| `action` | varchar | e.g. `STATUS_CHANGED` · `DOCUMENT_UPLOADED` · `VENDOR_SENT` · `RESULT_RECEIVED` · `FLAGGED_APPROVED` · `POCSO_CASE_CREATED` · `NCPCR_REPORTED` · `ESCALATED` |
| `performed_by_id` | FK → auth.User | Nullable — null for system/Celery actions |
| `performed_at` | timestamptz | — |
| `old_value` | text | JSON-encoded previous state |
| `new_value` | text | JSON-encoded new state |
| `ip_hash` | varchar(64) | SHA-256 of actor's IP — privacy compliant |
| `note` | varchar(500) | Optional reason/comment |

---

### `bgv_vendor_transaction`

API transaction log for all vendor communications. Append-only.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `vendor_id` | FK → `bgv_vendor` | — |
| `verification_id` | FK → `bgv_verification` | Nullable — null for health-check pings |
| `direction` | varchar | Enum: `OUTBOUND` (to vendor) · `INBOUND` (webhook from vendor) |
| `endpoint` | varchar | API path called or webhook path received |
| `payload_hash` | varchar(64) | SHA-256 of request/response payload — stored for audit without PII exposure |
| `http_status` | int | HTTP response code |
| `result` | varchar | Enum: `SUCCESS` · `ERROR` · `TIMEOUT` |
| `duration_ms` | int | API call duration |
| `error_message` | text | Nullable — error detail if result = ERROR |
| `is_test` | boolean | Default false — true for test verification requests from G-05 |
| `created_at` | timestamptz | — |

---

### `bgv_institution_communication`

Log of all communications sent to or about an institution regarding BGV compliance.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `institution_id` | int | — |
| `communication_type` | varchar | Enum: `IN_APP` · `EMAIL` · `PHONE_CALL` · `FORMAL_NOTICE` |
| `subject` | varchar(300) | e.g. "Document reminder — 3 staff pending" |
| `notes` | text | Free text — for phone calls and meeting notes |
| `created_by_id` | FK → auth.User | — |
| `created_at` | timestamptz | — |

---

### `bgv_operational_config`

Singleton (always `id = 1`). All Division G policy settings. Fully documented in G-08.

| Field | Type | Notes |
|---|---|---|
| `id` | int | Always 1 |
| `validity_years` | int | BGV validity period (default 3) |
| `renewal_lead_days` | int | Renewal reminder lead time (default 30) |
| `second_reminder_days` | int | Second reminder (default 7; 0 = disabled) |
| `expiry_grace_days` | int | Grace after expiry (default 0; max 14) |
| `doc_collection_sla_days` | int | Working days for institution to upload docs (default 5) |
| `doc_review_sla_hours` | int | BGV Executive review SLA (default 4) |
| `vendor_submission_sla_hours` | int | READY_FOR_VENDOR → VENDOR_SENT (default 2) |
| `result_review_sla_hours` | int | Vendor result → final decision (default 8) |
| `flagged_notify_sla_hours` | int | Supervisor approves FLAGGED → Manager notifies institution (default 24) |
| `default_vendor_id` | FK → `bgv_vendor` | Pre-selected vendor in G-02 submission modal |
| `default_checks` | varchar[] | Default check types for new verifications |
| `at_risk_threshold_pct` | decimal | AT_RISK lower bound (default 80) |
| `noncompliant_threshold_pct` | decimal | NON_COMPLIANT upper bound (default 79) |
| `auto_escalate_noncompliant_days` | int | Auto-escalate after N days NON_COMPLIANT (0 = disabled; default 14) |
| `auto_suspend_on_pocso_create` | boolean | Suspend staff access on POCSO case creation (default false) |
| `notify_email_enabled` | boolean | (default true) |
| `notify_copy_to_manager` | boolean | (default true) |
| `sla_uses_working_days` | boolean | If true, SLA calculated in working days (Mon–Fri IST, excl. national holidays). Default true. |
| `data_retention_clear_years` | int | Retention for CLEAR verifications after expiry (default 3) |
| `data_retention_flagged_years` | int | Retention for FLAGGED (non-POCSO) verifications (default 5) |
| `data_retention_pocso_years` | int | Retention for POCSO cases post-closure (default 10; regulatory minimum) |
| `updated_at` | timestamptz | — |
| `updated_by_id` | FK → auth.User | — |

---

### `bgv_config_log`

Change log for all `bgv_operational_config` updates.

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | — |
| `tab` | varchar | Enum: `VERIFICATION_POLICY` · `DOCUMENT_REQUIREMENTS` · `SLA` · `NOTIFICATIONS` · `COMPLIANCE_THRESHOLDS` |
| `setting_key` | varchar | e.g. `validity_years` |
| `old_value` | text | JSON-encoded |
| `new_value` | text | JSON-encoded |
| `changed_by_id` | FK → auth.User | — |
| `changed_at` | timestamptz | — |
| `note` | varchar(300) | Optional reason |

---

### Data Retention Policy

DPDPA 2023 and POCSO Act 2012 mandate specific retention periods. Celery task `archive_and_purge_old_bgv_records` runs monthly on the 1st at 03:00 IST.

| Record Type | Retention Period | Action at Expiry |
|---|---|---|
| BGV documents (CLEAR verification, expired) | 3 years after verification expiry | Purge from R2; audit log entry retained |
| BGV verification records (CLEAR) | 3 years after expiry date | Anonymise PII fields; retain for compliance count |
| BGV verification records (FLAGGED, non-POCSO) | 5 years from `reviewed_at` | Anonymise PII; retain case outcome |
| BGV verification records (INCONCLUSIVE) | 3 years from `reviewed_at` | Anonymise PII |
| BGV documents (FLAGGED/POCSO) | 10 years from case closure | Retain in R2 cold storage |
| POCSO case records | 10 years from `closed_at` | Cannot be deleted; anonymise only on court order |
| Vendor API transaction logs | 2 years | Purge payload hash; retain counts for performance reports |
| Audit log entries | 7 years | Read-only; never deleted |

Archival: anonymised records replace `full_name` with `[REDACTED]` and remove `file_url` references. All purge events logged in `bgv_audit_log` with `action = DATA_PURGED`.

---

## Cross-Page Critical Workflows

### Workflow 1 — Initial Verification (Full Cycle)
1. Institution submits request via portal → `bgv_verification` created (status: `DOCUMENTS_PENDING`) → **G-02** queue
2. BGV Executive (40) collects documents → **G-03** document checklist → status: `DOCUMENTS_RECEIVED`
3. Documents complete → BGV Executive marks `READY_FOR_VENDOR` → selects vendor → submits → status: `VENDOR_SENT`
4. Vendor returns CLEAR → status: `VENDOR_RETURNED` → BGV Executive marks CLEAR → status: `COMPLETE` → `bgv_staff.bgv_status = CLEAR` → **G-04** coverage % updates
5. Vendor returns FLAGGED → status: `VENDOR_RETURNED` → BGV Executive submits for review → status: `AWAITING_SUPERVISOR_REVIEW`
6. BGV Ops Supervisor (92) approves FLAGGED → status: `COMPLETE` → BGV Manager (39) notified → institution notification within 24h SLA → **G-04** updated

### Workflow 2 — POCSO Flag (two paths)
**Path A — Vendor auto-flag:**
1. Vendor webhook delivers result with `pocso_flag = true`
2. Celery `create_pocso_case_from_verification` fires: checks for existing open case on same `staff_id + verification_id`; if none → creates `bgv_pocso_case` → status: `OPEN`
3. POCSO Officer (41) / Reporting Officer (78) alerted in-app → **G-06** POCSO queue

**Path B — Supervisor manual detection:**
1. Vendor result FLAGGED (without pocso_flag) → BGV Ops Supervisor reviewing in **G-03**
2. Supervisor checks "POCSO offense" checkbox → sets `bgv_verification.pocso_flag = true` + `pocso_offense_type`
3. On [Confirm Approval]: same Celery task fires with deduplication check

**Both paths then follow:**
4. Officer reviews case → **G-06** case detail
5. Files NCPCR report (< 24h) + FIR with local police + SCWC notification per jurisdiction
6. Institution notified → staff access suspended if applicable
7. Case closed with NCPCR ref + FIR ref + closure reason

### Workflow 3 — Renewal Pipeline
1. Celery `auto_create_bgv_renewals` (nightly 01:00 IST): identifies `bgv_staff` where `current_verification.expiry_date ≤ today + renewal_lead_days` AND no active RENEWAL/RE_VERIFICATION in progress
2. Creates `bgv_verification` (type: `RENEWAL`, status: `DOCUMENTS_PENDING`, assigned_to_id: NULL)
3. Institution admin notified via notification hub
4. Renewal appears in **G-02** queue as "RENEWAL DUE" with amber badge; distributed by Supervisor (92)
5. Processed same as initial; existing CLEAR status retained until renewal completes

### Workflow 4 — Institution Non-Compliance Escalation
1. **G-04** shows institution with `compliance_status = NON_COMPLIANT`
2. If `auto_escalate_noncompliant_days > 0`: Celery `auto_escalate_noncompliant_institutions` (nightly 07:00 IST) sets `compliance_status = ESCALATED` after N days
3. BGV Manager can also manually escalate → in-app alert to Customer Success Manager (53)
4. If unresolved after escalation: BGV Manager requests platform access restriction via Platform Admin (10)
5. Resolution: when institution reaches 100% coverage → `COMPLIANT`; escalation cleared automatically
