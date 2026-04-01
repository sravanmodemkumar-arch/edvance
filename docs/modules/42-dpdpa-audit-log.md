# Module 42 — DPDPA & Audit Log

## 1. Purpose

The Digital Personal Data Protection Act, 2023 (DPDPA) is India's foundational data protection statute. For EduForge — processing personal data of 50 million students, their parents, and 5+ million staff across 16 institution types — compliance is not a checkbox exercise. At that scale, EduForge qualifies as a Significant Data Fiduciary (SDL) with mandatory DPBI registration, a full-time Data Protection Officer, annual DPIA, and statutory audit obligations. More critically, roughly 90% of EduForge's users are under 18 — meaning the entire platform operates under the heightened child-data provisions of DPDPA Section 9.

Module 42 serves two interconnected purposes:

1. **DPDPA Compliance Engine** — consent management, rights fulfilment (access, correction, erasure, grievance, nomination), privacy notices, sub-processor registry, breach notification, children's data controls, and the DPDPA compliance dashboard.

2. **Audit Log** — the tamper-proof, append-only, hash-chained system-of-record for every sensitive action across all 57 modules. The audit log is the evidentiary foundation for DPBI inquiries, CERT-In reporting, ISO 27001, SOC 2, and internal forensic investigations.

These two are inseparable: every DPDPA rights action is itself an audit event, and the audit log is itself subject to DPDPA governance.

---

## 2. DPDPA Legal Framework

### 2.1 Roles & Responsibilities

| Role | Definition | Who in EduForge |
|---|---|---|
| Data Principal | Person whose personal data is processed | Student, parent, staff, alumni, enquiry lead |
| Data Fiduciary | Determines purpose and means of processing | EduForge (platform) + each institution (tenant) |
| Significant Data Fiduciary (SDL) | Data Fiduciary notified by DPBI based on scale/sensitivity | EduForge (50M users) |
| Data Processor | Processes data on behalf of Data Fiduciary | AWS, Cloudflare, WhatsApp BSP, SMS providers, DigiLocker |
| Data Protection Board (DPBI) | Regulatory authority | Government of India |

Two-tier structure: EduForge (platform) is simultaneously:
- Data Fiduciary for platform-wide processing (authentication, analytics, platform operations)
- Data Processor for institution-specific data (the institution is the controller)

### 2.2 SDL Obligations

As an SDL (when notified by DPBI based on scale):

| Obligation | EduForge Mechanism |
|---|---|
| Appoint Data Protection Officer | Full-time DPO; contact published in app + website |
| Conduct DPIA (Data Protection Impact Assessment) | Annual; for all high-risk processing categories |
| Undergo independent data audit | Annual; audit evidence from audit log |
| Maintain data flows map | Data inventory table (Section 4) |
| Register with DPBI | Registration document stored in Module 40 |
| Publish DPO contact | App Settings → Privacy; website footer; all privacy notices |

### 2.3 Applicable Statutes

| Statute | Key Obligation for EduForge |
|---|---|
| DPDPA 2023 | Core data protection obligations; rights of data principals; breach notification |
| IT Act 2000, S.43A | Security of sensitive personal data (superseded by DPDPA but compliance maintained) |
| IT Act S.70B | CERT-In incident reporting within 6 hours of cybersecurity incident |
| DPDP Rules 2025 (draft) | Implementing rules for consent verification, breach format, rights timelines |
| POCSO Act 2012 | Children's data — specific context; see Module 41 |
| RTE Act 2009 | Student data rights in school context |

---

## 3. Children's Data (DPDPA Section 9)

### 3.1 Child Definition & Coverage

DPDPA S.9: any person under 18 is a "child." All students under 18 — which is the majority of EduForge's user base — are in this category. Processing their data requires verifiable parental consent.

### 3.2 Verifiable Parental Consent

Standard checkbox consent is insufficient. EduForge implements:

**Primary method — OTP to registered parent mobile:**
1. Parent mobile number collected at enrollment (Module 09)
2. OTP sent to parent mobile
3. Parent enters OTP on enrollment form
4. OTP verification = consent verification record

**Alternative — Aadhaar-based KYC:**
1. Parent performs Aadhaar OTP-based KYC on DigiLocker
2. Consent record linked to Aadhaar KYC transaction ID

**Special case — same mobile for parent and student:**
Common in rural areas. Flagged at enrollment; admin manually records consent confirmation with parent present (paper consent form scanned and stored in Module 40).

### 3.3 Restrictions on Children's Data

Per DPDPA S.9(3), regardless of consent:

| Prohibited Processing | Applicable Module | EduForge Control |
|---|---|---|
| Targeted advertising | None — no advertising on platform | N/A |
| Behavioural tracking for commercial purposes | Module 47 (AI Analytics) | AI features in restricted mode for under-18 users |
| Profiling that harms child | Module 47 | DPIA required before activation per tenant |
| Tracking geolocation for non-educational purpose | Module 29 (Transport) | Location data used only for route tracking; not stored beyond 7 days |

### 3.4 Age Transition (Student Turns 18)

1. System detects age milestone from DOB (nightly job)
2. Student receives notification: "You are now 18. You can now manage your own data consent."
3. Parent receives notification: "Your child has turned 18. Their data consent will transfer to them within 90 days."
4. 90-day transition window: student activates their own consent management
5. After 90 days: parent's consent authority revoked; student's own consent is now the legal basis
6. Parent access to student data restricted to what the student explicitly authorises (via sharing settings)

---

## 4. Data Inventory

The data inventory is the foundation of DPDPA compliance — mapping every data category to its purpose, legal basis, and retention.

### 4.1 Data Categories

| Category | Examples | Sensitivity | Legal Basis |
|---|---|---|---|
| Identification | Name, DOB, photo, Aadhaar | PII | Consent / Legal Obligation |
| Academic | Marks, attendance, exam results, assignments | PII | Consent + Educational Purpose |
| Financial | Fee records, payment details, salary | Sensitive PII | Consent + Legal Obligation |
| Health | Blood group, medical fitness, vaccination | Sensitive PII | Consent + Vital Interest |
| Biometric | Fingerprint (attendance), face (proctoring) | Sensitive PII — Biometric | Explicit Consent |
| Location | GPS (transport), hostel entry/exit | PII | Consent + Safety |
| Behavioural | App usage, login patterns | Pseudonymous | Legitimate Interest |
| Communication | Message content, email body | PII | Consent |
| Compliance | POCSO incidents, disciplinary records | Sensitive PII | Legal Obligation |

### 4.2 Purpose Registry

Every processing activity documented:

```sql
CREATE TABLE data_inventory (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  data_category   TEXT NOT NULL,
  data_field      TEXT NOT NULL,         -- specific field name
  source_module   TEXT NOT NULL,
  processing_purpose TEXT NOT NULL,
  legal_basis     TEXT NOT NULL,         -- consent / legal_obligation / vital_interest / public_task / legitimate_interest
  legal_basis_ref TEXT,                  -- specific law/section
  processors      TEXT[],                -- sub-processors involved
  retention_days  INT NOT NULL,
  post_retention  TEXT NOT NULL,         -- DELETE / ANONYMISE / ARCHIVE
  cross_border    BOOLEAN DEFAULT FALSE, -- data leaves India
  last_reviewed   DATE NOT NULL,
  reviewed_by_id  UUID REFERENCES users(id)
);
```

### 4.3 Data Minimisation Enforcement

API endpoint request/response schemas are validated against the data inventory:
- No field is collected that isn't in the inventory for that purpose
- Orphaned data (incomplete workflows abandoned for > 90 days) auto-deleted by retention job
- Pseudonymisation: `student_id` UUID used as primary key across all joins; name/Aadhaar only in PII tables accessed via restricted APIs

---

## 5. Consent Management

### 5.1 Consent Architecture

```
Enrollment Form
      ↓
Purpose-by-purpose consent checklist (no omnibus checkbox)
      ↓
Each item:
  [✅] Enrollment administration (required — cannot opt out)
  [✅] Academic reporting (required — cannot opt out)
  [✅] Fee collection (required — cannot opt out)
  [✅] Communication via push notification, email, SMS
  [✅] Transport GPS tracking
  [ ] AI-powered personalised learning recommendations ← opt-in
  [ ] Sharing anonymised academic data for research ← opt-in
      ↓
OTP verification (parental, for under-18)
      ↓
Consent record created for each purpose
```

Consent for "required" purposes cannot be withheld (service cannot be rendered otherwise) — this is disclosed in the privacy notice; legal basis = contractual necessity / legal obligation.

### 5.2 Consent Record

```sql
CREATE TABLE consent_records (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL REFERENCES tenants(id),
  data_principal_id UUID NOT NULL REFERENCES users(id),
  minor_student_id  UUID REFERENCES students(id),   -- if consent is parental
  purpose           TEXT NOT NULL,
  status            TEXT NOT NULL DEFAULT 'ACTIVE',  -- ACTIVE / WITHDRAWN / EXPIRED
  given_by_id       UUID NOT NULL REFERENCES users(id),
  given_at          TIMESTAMPTZ NOT NULL DEFAULT now(),
  given_via         TEXT NOT NULL,     -- OTP / AADHAAR_KYC / PAPER_UPLOADED / IN_APP
  privacy_notice_version TEXT NOT NULL,
  withdrawn_at      TIMESTAMPTZ,
  withdrawal_reason TEXT
);
```

### 5.3 Consent Dashboard (Data Principal View)

```
My Data Consents
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Purpose                            Status      Given On
─────────────────────────────────────────────────────────
Enrollment administration          Required    12 Apr 2025
Academic reporting                 Required    12 Apr 2025
Fee collection                     Required    12 Apr 2025
Push notifications                 ✅ Active   12 Apr 2025  [Withdraw]
Email communications               ✅ Active   12 Apr 2025  [Withdraw]
Transport GPS tracking             ✅ Active   12 Apr 2025  [Withdraw]
AI personalised recommendations    ❌ Opted out              [Opt in]
Research data sharing              ❌ Not given              [Opt in]

[Download Consent History PDF]
```

### 5.4 Consent Withdrawal Handling

On withdrawal for a non-required purpose:
1. Processing for that purpose stops within 24 hours (system flag prevents further processing)
2. Data collected solely for that purpose scheduled for deletion within 30 days
3. Withdrawal acknowledged via push + email
4. Audit event: CONSENT_WITHDRAWN — WARNING severity

On withdrawal of a required purpose (rare — e.g., student wants to leave):
1. System flags account for deactivation review
2. Admin contacted to understand context (may be a TC request)
3. Cannot unilaterally process withdrawal of required purposes without student status change

### 5.5 Re-Consent Workflow

When privacy notice is updated with new/changed purposes:
1. New version published in system
2. All active users receive: push notification + email — "Our privacy notice has been updated. Please review and confirm your preferences."
3. App displays consent re-confirmation screen at next login
4. Cannot dismiss without reviewing (not a blocking popup — can be deferred 3 times, then blocks on 4th login)
5. Consent confirmed → new consent record created with new version tag
6. Users who don't re-confirm within 30 days → non-required new purposes auto-suspended

---

## 6. Rights of Data Principals

### 6.1 Rights Request Portal

Accessible from: App → Settings → Privacy → My Rights

```
Your Data Rights
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[📋 Request my data]  See all personal data we hold about you

[✏️  Correct my data]  Report an inaccuracy

[🗑️  Erase my data]   Request deletion of your data

[⬅️  Withdraw Consent] Manage your consent preferences

[💬 File a Grievance] Report a data protection concern

[👤 Nominate someone] Authorise someone to act on your behalf
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Your open requests: 0
DPO contact: dpo@{institution-domain}
DPBI: https://dpboard.gov.in
```

### 6.2 Access Request

Timeline: 30 days (DPDPA-mandated).

System auto-generates a structured PDF covering all 57 modules:

```
Data Access Report — Arjun Mehta (Student)
Generated: 26 Mar 2026

1. Identity & Enrollment
   Fields: Full name, DOB, Aadhaar (masked), address, photo
   Purpose: Enrollment administration
   Retention: Until leaving + 5 years
   Shared with: CBSE (board reporting), DigiLocker (at your consent)

2. Academic Records
   Fields: Marks (all terms), attendance %, assignments, exam results
   Purpose: Academic reporting
   Retention: Until leaving + 5 years

3. Fee Records
   Fields: Invoice amounts, payment dates, receipt numbers
   Purpose: Fee collection
   Retention: 8 years (GST compliance)

[... continues for all data categories ...]

4. Communication Logs
   Fields: Push notification delivery status (no message content)
   Purpose: Service delivery
   Retention: 2 years

[Data shared with third parties: listed with purpose and date range]
```

### 6.3 Erasure Request Outcome

Returned to data principal as a structured response:

| Data Category | Action | Legal Basis for Retention (if applicable) |
|---|---|---|
| Marketing preferences | ERASED (28 Apr 2026) | — |
| Push notification history | ERASED (28 Apr 2026) | — |
| Fee receipts | RETAINED | CGST Act S.35 — 8 years mandatory |
| Transfer Certificate | RETAINED | State Education Act — 10 years |
| Academic results | RETAINED | Legal record for student benefit |
| POCSO incident record | RETAINED | POCSO legal hold — 7 years from closure |

### 6.4 Grievance Process

```
Grievance Submitted → Acknowledged within 48 hours (auto)
                    → DPO reviews → Responds within 30 days
                    → If unresolved at 30 days: escalation alert to DPO
                    → Data principal notified they may file with DPBI
                    → DPBI complaint link provided in-app
```

All grievances logged; DPO tracks resolution SLA on compliance dashboard.

### 6.5 Nomination

Data principal nominates a trusted person (next of kin / guardian) to exercise rights on their behalf:

```sql
CREATE TABLE data_principal_nominations (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  data_principal_id UUID NOT NULL REFERENCES users(id),
  nominee_name    TEXT NOT NULL,
  nominee_phone   TEXT NOT NULL,
  nominee_relation TEXT,
  verified        BOOLEAN DEFAULT FALSE,
  created_at      TIMESTAMPTZ DEFAULT now()
);
```

Nominee verification: admin calls nominee phone to confirm willingness. Nomination used if data principal is deceased (death certificate uploaded) or incapacitated.

---

## 7. Audit Log Architecture

### 7.1 Design Principles

1. **Append-only** — PostgreSQL row-level security + trigger prevents UPDATE and DELETE on `audit.events`
2. **Audit-first** — audit write is in the same transaction as the operational write; if audit fails, operational write rolls back
3. **Hash-chained** — each event contains the hash of the previous event; tampering detectable
4. **Universally emitted** — all 57 modules use `emit_audit_event()` SDK function; no module bypasses the log
5. **Cannot be disabled** — no tenant admin can disable audit logging; disabling attempt itself generates a CRITICAL event

### 7.2 Event Schema

```sql
-- Separate schema with restricted write access
CREATE SCHEMA audit;

CREATE TABLE audit.events (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_ref       TEXT NOT NULL UNIQUE,     -- AUD-2026-0001234567
  tenant_id       UUID NOT NULL,
  user_id         UUID,                     -- null for system-generated events
  session_id      UUID,
  action          TEXT NOT NULL,
  -- AUTH: LOGIN_SUCCESS / LOGIN_FAILURE / LOGOUT / OTP_SENT / OTP_FAILED /
  --       DEVICE_ADDED / SESSION_EXPIRED / ACCOUNT_LOCKED / PASSWORD_RESET
  -- DATA: CREATE / READ / UPDATE / DELETE / EXPORT / BULK_EXPORT
  -- CONSENT: CONSENT_GIVEN / CONSENT_WITHDRAWN / CONSENT_RENEWED
  -- RIGHTS: ACCESS_REQUEST / ERASURE_REQUEST / CORRECTION_REQUEST / GRIEVANCE_FILED
  -- SECURITY: FRAUD_FLAG_RAISED / RATE_LIMIT_BREACH / HASH_CHAIN_FAILURE / BREACH_DETECTED
  -- ADMIN: ROLE_ASSIGNED / PERMISSION_CHANGED / CONFIG_CHANGED / LEGAL_HOLD_PLACED
  module          TEXT NOT NULL,
  resource_type   TEXT NOT NULL,
  resource_id     UUID,
  before_state    JSONB,
  after_state     JSONB,
  ip_address      INET,
  user_agent      TEXT,
  severity        TEXT NOT NULL DEFAULT 'INFO',
  -- INFO / NOTICE / WARNING / CRITICAL
  metadata        JSONB,
  prev_hash       TEXT NOT NULL,
  event_hash      TEXT NOT NULL GENERATED ALWAYS AS (
                    encode(sha256(
                      (event_ref || tenant_id::text || COALESCE(user_id::text,'') ||
                       action || module || resource_type || prev_hash)::bytea
                    ), 'hex')
                  ) STORED,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT now()
) PARTITION BY RANGE (created_at);

-- Monthly partitions created automatically
-- Row-level security: only audit service account can INSERT; no UPDATE/DELETE for any role
```

### 7.3 SDK Emission Function

Every module calls:

```python
from core.audit import emit_audit_event

await emit_audit_event(
    tenant_id=request.tenant_id,
    user_id=request.user.id,
    session_id=request.session_id,
    action="UPDATE",
    module="fee",
    resource_type="fee_structure",
    resource_id=fee_structure.id,
    before_state=before_state_dict,
    after_state=after_state_dict,
    ip_address=request.client.host,
    user_agent=request.headers.get("User-Agent"),
    severity="NOTICE",
    metadata={"changed_fields": ["amount", "due_date"]}
)
```

The function is synchronous within the database transaction — event written before the caller's transaction commits.

### 7.4 Before/After State Diffs

For UPDATE events, the system computes a human-readable diff at query time:

```python
def compute_diff(before: dict, after: dict) -> list[dict]:
    changes = []
    for key in set(before.keys()) | set(after.keys()):
        if before.get(key) != after.get(key):
            changes.append({
                "field": key,
                "from": before.get(key),
                "to": after.get(key)
            })
    return changes
```

Displayed in audit log viewer as: "Changed `amount` from ₹12,000 to ₹13,500; changed `due_date` from 15 Apr to 30 Apr"

---

## 8. Audit Log Integrity — Hash Chain

### 8.1 Chain Structure

```
Event 1: prev_hash = "0000...0000" (genesis)
         event_hash = SHA-256("AUD-0000001|tenant|user|CREATE|student|...")

Event 2: prev_hash = event_hash of Event 1
         event_hash = SHA-256("AUD-0000002|...|" + prev_hash)

Event 3: prev_hash = event_hash of Event 2
         ...
```

### 8.2 Daily Anchor

At midnight UTC, the hash of the last event of the day is written to a versioned, immutable R2 object:
`audit-anchors/{tenant_id}/{YYYY-MM-DD}.sha256`

These anchor files cannot be overwritten (R2 object lock). This provides an externally verifiable checkpoint — even if the database is compromised, the R2 anchors prove what the chain looked like at each day-end.

### 8.3 Verification Tool

```
Hash Chain Verification
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Tenant: Delhi Public School
Date range: 01 Mar 2026 → 26 Mar 2026
Events in range: 147,382

Re-computing hashes... ████████████████████ 100%

Result: ✅ Chain intact — no tampering detected

Anchor match check:
  01 Mar 2026: R2 anchor ✅ matches DB
  15 Mar 2026: R2 anchor ✅ matches DB
  25 Mar 2026: R2 anchor ✅ matches DB
```

Chain failure → CRITICAL alert to DPO and Super Admin; automatic CERT-In incident draft generated.

### 8.4 Audit-First Guarantee

```python
async with db.transaction():
    # Step 1: Write audit event
    await db.execute(INSERT_AUDIT_EVENT, event_data)
    # Step 2: Write operational data
    await db.execute(UPDATE_FEE_STRUCTURE, fee_data)
    # If Step 1 fails → transaction rolls back → fee structure NOT updated
    # If Step 2 fails → transaction rolls back → audit event NOT written
    # Either both happen or neither happens
```

---

## 9. Breach Detection Engine

### 9.1 Rules-Based Detection (Real-Time)

Events processed through detection rules in < 5 seconds:

| Rule | Trigger | Severity |
|---|---|---|
| Bulk student profile access | > 200 READ events in 1 hour by one user | WARNING |
| Anomalous data export | Export volume > 10× user's 30-day average | CRITICAL |
| Off-hours sensitive access | Payroll / POCSO access between 11 PM–5 AM from new IP | WARNING |
| Mass OTP failures | > 50 OTP_FAILED events in 10 minutes | CRITICAL |
| Hash chain failure | `compute_chain_hash()` verification fails | CRITICAL |
| Bulk SMS/email campaign | > 10,000 messages sent without approval flag | WARNING |
| Role escalation attempt | Access to resource beyond assigned role | CRITICAL |
| New device + sensitive action | First login from device + immediate payroll access | WARNING |

### 9.2 ML Anomaly Detection

User access pattern baseline: rolling 30-day average of access events per module per time-of-day.
Deviation > 3 sigma from baseline → anomaly flag.

Examples caught:
- Teacher who normally accesses 30 profiles/day suddenly accessing 800 in one day
- Admin who never accesses salary data suddenly downloads entire payroll report
- API key that normally makes 100 calls/hour suddenly making 10,000 calls

ML model retrained weekly. False positive whitelist: legitimate bulk operations (payroll processing, annual result export) can be pre-approved and whitelisted.

### 9.3 Alert Routing

| Severity | Channels | Recipients |
|---|---|---|
| INFO | None | — |
| NOTICE | None | — |
| WARNING | Email | DPO |
| CRITICAL | Push + SMS + Email | DPO + Super Admin |

---

## 10. Breach Incident Management

### 10.1 Breach Incident Lifecycle

```
BREACH_DETECTED (event or manual discovery)
      ↓
Breach incident created: breach_id, discovered_at
72-hour DPBI notification clock starts
      ↓
DPO assesses: personal data involved? → YES → DPBI notification required
              personal data involved? → NO  → CERT-In only (if cyber incident)
      ↓
Containment actions: account suspend, sessions invalidate, API key revoke
      ↓
DPBI notification submitted (within 72 hours)
      ↓
Data principal notification (push + email to affected users)
      ↓
Post-breach report: root cause, remediation, lessons learned
      ↓
CLOSED: all actions documented; evidence stored for DPBI audit
```

### 10.2 DPBI Notification Template

```
To: Data Protection Board of India
From: [DPO Name], EduForge / [Institution]
Date: [datetime]
Ref: BREACH-2026-0001

1. Nature of the personal data breach:
   [Unauthorised access to student fee records due to SQL injection in fee payment API]

2. Categories and approximate number of data principals concerned:
   Fee records: approximately 1,240 students of [Institution Name]

3. Categories and approximate number of personal data records concerned:
   Invoice amounts, payment dates: ~4,800 records

4. Likely consequences of the breach:
   Financial data exposed; risk of targeted phishing

5. Measures taken or proposed to address the breach:
   - Compromised API endpoint patched at 14:23 on [date]
   - All sessions invalidated
   - Affected users notified at 15:00 on [date]
   - Security scan of all APIs initiated

DPO: [Name] | Contact: [email] | DPBI Registration: [ID]
```

### 10.3 Data Principal Notification

```
Subject: Important security notice from [Institution Name]

Dear Arjun,

We are writing to let you know about a security incident that may have
affected your data.

What happened: On [date], we discovered unauthorised access to our
fee payment system.

What data was involved: Your fee invoice amounts and payment dates.

What we have done: We have patched the vulnerability, invalidated all
active sessions, and are conducting a full security review.

What you should do: No action is required. If you notice any suspicious
activity, contact us at [support email].

We apologise for this incident and are committed to protecting your data.

Data Protection Officer: [name]
Contact: dpo@[institution-domain]
```

---

## 11. Data Retention Automation

### 11.1 Retention Registry

```sql
CREATE TABLE retention_registry (
  data_category     TEXT NOT NULL,
  source_module     TEXT NOT NULL,
  retention_days    INT NOT NULL,
  legal_basis       TEXT NOT NULL,
  legal_basis_ref   TEXT,
  post_retention    TEXT NOT NULL,    -- DELETE / ANONYMISE / ARCHIVE
  PRIMARY KEY (data_category, source_module)
);

-- Sample entries:
INSERT INTO retention_registry VALUES
('student_pii',         'enrollment',    1825, 'consent + school record',   'RTE Act', 'ANONYMISE'),
('fee_invoice',         'fee',           2920, 'legal_obligation',          'CGST S.35', 'ARCHIVE'),
('payroll_record',      'payroll',       2920, 'legal_obligation',          'IT Act', 'ARCHIVE'),
('pocso_incident',      'pocso',         2555, 'legal_obligation',          'POCSO Act', 'LEGAL_HOLD'),
('audit_log',           'audit',         2555, 'legal_obligation',          'DPDPA', 'ARCHIVE'),
('communication_log',   'notifications', 730,  'legitimate_interest',       NULL, 'ANONYMISE'),
('session_token',       'auth',          1,    'service_delivery',          NULL, 'DELETE'),
('otp_hash',            'auth',          1,    'service_delivery',          NULL, 'DELETE'),
('app_logs',            'infra',         90,   'operational_necessity',     NULL, 'DELETE');
```

### 11.2 Retention Job

Nightly (2 AM IST):
1. Scan all tables for records where `created_at + retention_days < NOW()`
2. Check for legal holds — skip held records
3. Queue non-held records for DPO review
4. DPO reviews within 7 days: approve deletion, extend hold with reason, or mark for legal hold
5. Approved records: soft-deleted (flagged) → hard-deleted 30 days later → R2 files deleted → deletion certificate generated

### 11.3 Deletion Certificate

```json
{
  "certificate_id": "DEL-CERT-2026-04-001",
  "tenant_id": "uuid",
  "data_category": "push_notification_logs",
  "records_deleted": 48200,
  "deleted_at": "2026-04-15T02:15:00Z",
  "approved_by_dpo": "dpo@institution.in",
  "r2_objects_deleted": 0,
  "retention_policy_applied": "730 days",
  "certificate_hash": "sha256:..."
}
```

Certificate stored permanently in Module 40 (institutional documents). It is itself an audit event (DELETION_CERTIFICATE_GENERATED).

---

## 12. Sub-Processor Registry

### 12.1 Current Sub-Processors

```sql
CREATE TABLE sub_processor_registry (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name            TEXT NOT NULL,
  service         TEXT NOT NULL,
  data_categories TEXT[] NOT NULL,
  countries       TEXT[] NOT NULL,
  dpa_document_id UUID REFERENCES documents(id),
  dpa_signed_date DATE,
  dpa_review_due  DATE,
  active          BOOLEAN DEFAULT TRUE,
  notes           TEXT
);
```

| Sub-Processor | Service | Data Categories | Countries | DPA Status |
|---|---|---|---|---|
| AWS (RDS, Lambda, SES, Textract, Rekognition) | Core infra, OCR, email | All categories | India (ap-south-1); US for Textract/Rekognition | ✅ Signed |
| Cloudflare (R2, CDN) | Storage, CDN | Documents, media, thumbnails | Global (CDN nodes) | ✅ Signed |
| Gupshup / Kaleyra | WhatsApp Business API | Phone number, message content | India | ✅ Signed |
| Twilio / Kaleyra | SMS | Phone number, message content | India / Global | ✅ Signed |
| DigiLocker (CDAC / MeitY) | Document push/pull | Student academic docs | India | ✅ Signed |
| Razorpay / PhonePe | Payment processing | Payment metadata (no card data stored) | India | ✅ Signed |

### 12.2 Sub-Processor Change Protocol

1. New sub-processor identified → legal team reviews DPA
2. DPA signed → added to registry → Module 40 storage
3. All tenants notified 30 days before activation: "We are adding [X] as a data processor. [Link to privacy notice update]"
4. Privacy notice updated with new sub-processor
5. Change logged as CONFIGURATION_CHANGE — CRITICAL severity in audit log

---

## 13. DPDPA Compliance Dashboard

### 13.1 Platform-Level (Super Admin / DPO View)

```
EduForge DPDPA Compliance Dashboard — 2025-26
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Consent Coverage
  Users with valid consent records    : 99.7%
  Users with overdue re-consent       :  0.3% (230 users)

Rights Requests SLA (30-day target)
  Fulfilled on time                   : 98.2%
  Breached SLA                        :  1.8% (4 requests)

Breach Notification SLA (72-hour target)
  All breaches notified within 72h    : ✅ 100% (2 incidents this year)

Sub-Processor DPA Currency
  DPAs reviewed in last 12 months     : 6 / 6 (100%)

Audit Log Chain Integrity
  Last verified                       : 26 Mar 2026 02:15
  Chain status                        : ✅ Intact

Retention Compliance
  Records within policy               : 99.9%
  DPO review queue (pending)          : 12 records

Children's Data (Under-18)
  Parental consent on file            : 99.8% of minor students
  Age transition pending (recently 18): 43 students
```

### 13.2 Institution-Level (Principal / Institution DPO)

Institution sees the same metrics scoped to their tenant, plus:
- Open rights requests for their students/staff
- Staff consent acknowledgement rates
- Document retention status
- POCSO incident data access events (count only)

---

## 14. CERT-In Compliance

### 14.1 Mandatory Reporting (IT Act S.70B)

Cybersecurity incidents — system intrusions, data exfiltration, malware, DDoS — must be reported to CERT-In within **6 hours** of knowledge.

CERT-In incident types applicable to EduForge:
- Unauthorised access to student data
- Ransomware on any EduForge server
- DDoS disrupting access to platform
- Targeted intrusion (APT activity)

### 14.2 CERT-In Notification

Structured notification template pre-filled from breach incident:
- Incident type (from CERT-In taxonomy)
- Date and time of discovery
- Systems affected
- Attack vector (if known)
- Data categories affected
- Containment actions taken
- Contact person

Submitted via CERT-In online portal; acknowledgement reference stored in breach incident record.

### 14.3 Log Retention for CERT-In

CERT-In mandates specific log types be retained for 180 days (IT (CERT-In) Amendment Rules 2022):
- Application logs
- API gateway logs
- Authentication logs
- Network/firewall logs

EduForge retains audit logs (90-day for app logs; 7-year for audit events). CERT-In-mandated 180-day retention for security logs stored in R2 with lock.

---

## 15. RBAC Matrix

| Action | Data Principal (Student/Parent/Staff) | Institution Admin | Institution DPO | Super Admin |
|---|---|---|---|---|
| View own consent dashboard | ✅ | ❌ | ❌ | ❌ |
| Withdraw own consent | ✅ | ❌ | ❌ | ❌ |
| Submit rights request | ✅ | ❌ | ❌ | ❌ |
| View rights request queue | ❌ | ❌ | ✅ | ✅ |
| Respond to rights request | ❌ | ❌ | ✅ | ✅ |
| View audit log (tenant-scoped) | ❌ | ❌ | ✅ | ✅ |
| View audit log (all tenants) | ❌ | ❌ | ❌ | ✅ |
| Verify hash chain | ❌ | ❌ | ✅ | ✅ |
| Create breach incident | ❌ | ❌ | ✅ | ✅ |
| Approve DPBI notification | ❌ | ❌ | ✅ | ✅ |
| View retention queue | ❌ | ❌ | ✅ | ✅ |
| Approve deletion | ❌ | ❌ | ✅ | ✅ |
| Place legal hold | ❌ | ❌ | ❌ | ✅ |
| Grant external auditor access | ❌ | ❌ | ✅ (tenant) | ✅ |
| Manage sub-processor registry | ❌ | ❌ | ❌ | ✅ |

---

## 16. API Reference

```
# Consent management
GET    /api/v1/privacy/consent/                     # Own consent state
PATCH  /api/v1/privacy/consent/{purpose}/withdraw/  # Withdraw consent
GET    /api/v1/privacy/consent/history/             # Consent history PDF

# Rights requests
POST   /api/v1/privacy/rights-requests/             # Submit request
GET    /api/v1/privacy/rights-requests/{id}/        # Status
GET    /api/v1/privacy/access-report/               # Data access PDF (auto-generated)

# DPO queue
GET    /api/v1/dpo/rights-requests/                 # Pending requests
PATCH  /api/v1/dpo/rights-requests/{id}/respond/    # Respond to request
GET    /api/v1/dpo/compliance-dashboard/            # Compliance scores
GET    /api/v1/dpo/retention-queue/                 # Retention review queue
PATCH  /api/v1/dpo/retention-queue/{id}/approve/    # Approve deletion

# Breach management
POST   /api/v1/dpo/breaches/                        # Create breach incident
GET    /api/v1/dpo/breaches/{id}/                   # Breach detail
PATCH  /api/v1/dpo/breaches/{id}/notify-dpbi/       # Log DPBI notification
PATCH  /api/v1/dpo/breaches/{id}/close/             # Close breach incident

# Audit log
GET    /api/v1/audit/events/                        # Paginated audit log (DPO/Super Admin)
GET    /api/v1/audit/events/{id}/                   # Single event
GET    /api/v1/audit/hash-chain/verify/             # Verify chain integrity
POST   /api/v1/audit/external-auditor/grant/        # Grant time-limited auditor access

# Sub-processor
GET    /api/v1/privacy/sub-processors/              # Registry (public-facing)
PUT    /api/v1/admin/sub-processors/{id}/           # Update DPA status (Super Admin)
```

---

## 17. Analytics

### 17.1 Audit Log Analytics

| Metric | Purpose |
|---|---|
| Daily audit event volume per module | Baseline; spike detection |
| Top 10 accessed student profiles (admin) | Identifies undue monitoring |
| Rights request volume and type | DPBI reporting; operational planning |
| Consent withdrawal rate by purpose | Product feedback; which features users distrust |
| Breach detection rule fire rate | Precision monitoring; false positive calibration |
| DPO response SLA compliance | Rights fulfilment performance |

### 17.2 Anomaly Alerts Board

```
Anomaly Alerts — Last 7 Days
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ WARNING [24 Mar 14:31]: User admin@school.in accessed 180 student profiles in 45 minutes
   → Investigated: bulk ID card preparation (whitelisted 24 Mar 15:00)

ℹ️ INFO    [25 Mar 09:12]: Consent re-confirmation campaign — 12,400 events in 2 hours
   → Expected: system re-consent workflow triggered by privacy notice update

✅ No CRITICAL alerts in last 7 days
```

---

## 18. Cross-Module Integration Map

| Module | Audit Events Emitted |
|---|---|
| Module 01 — Auth | LOGIN / LOGOUT / OTP / DEVICE / SESSION events |
| Module 03 — RBAC | ROLE_ASSIGNED / PERMISSION_CHANGED |
| Module 07–09 — Profiles | PROFILE_READ / PROFILE_UPDATED / AADHAAR_ACCESSED |
| Module 17–20 — Exam | PAPER_ACCESSED / PROCTORING_DATA_STORED / ANSWER_KEY_VIEWED |
| Module 21–23 — Results | RESULT_PUBLISHED / MARKS_OVERRIDDEN / RESULT_VIEWED |
| Module 24–26 — Fee | INVOICE_GENERATED / PAYMENT_RECORDED / FEE_STRUCTURE_CHANGED |
| Module 27 — Payroll | SALARY_COMPUTED / PAYSLIP_ACCESSED / BANK_DETAILS_VIEWED |
| Module 28–29 — Hostel/Transport | GPS_DATA_ACCESSED / HOSTEL_SOS_TRIGGERED |
| Module 35–38 — Communications | BULK_PUSH_SENT / BULK_EMAIL_SENT / BULK_SMS_SENT |
| Module 39 — Certificates | CERT_ISSUED / CERT_REVOKED / VERIFICATION_ATTEMPT |
| Module 40 — Documents | DOCUMENT_VIEWED / DOCUMENT_DOWNLOADED / FRAUD_FLAG_RAISED |
| Module 41 — POCSO | INCIDENT_CREATED / INCIDENT_VIEWED / VICTIM_IDENTITY_ACCESSED |
| Module 42 — This module | CONSENT_GIVEN / RIGHTS_REQUEST / BREACH_CREATED / DELETION_APPROVED |

Every module in EduForge contributes to the single `audit.events` table. The audit log is the cross-cutting accountability layer of the entire platform.

---

*Module 42 — DPDPA & Audit Log — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
