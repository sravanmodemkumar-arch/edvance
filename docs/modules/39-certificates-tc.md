# Module 39 — Certificates & TC

## 1. Purpose

Every educational institution in India is legally obligated to issue several categories of documents — Transfer Certificate (TC), Bonafide / Enrollment Certificate, Character Certificate, Migration Certificate, and various achievement / participation certificates — at defined timescales and in board-mandated formats. Beyond the statutory requirement, these documents are the primary proof of a student's academic history, and any delay, loss, or forgery has real consequences: a child blocked from a new admission, a student denied a scholarship, a graduate unable to start employment.

EduForge Module 39 is the centralised certificate lifecycle engine across all 16 institution types. It handles request intake, multi-department clearance workflows, WeasyPrint PDF rendering with institution branding, QR-based public verification, DigiLocker / ABC / NAD push, DPDPA-compliant storage and retention, and analytics that feed the Early Warning System (dropout signal via TC issuance rate). Every certificate generated is immutable, hash-verified, and permanently archived in Cloudflare R2.

---

## 2. Certificate Taxonomy

### 2.1 Statutory Certificates

| Certificate | Trigger | Who Approves | Legal Basis |
|---|---|---|---|
| Transfer Certificate (TC) | Student leaving institution | Principal | RTE Act S.4, S.6; State Board Rules |
| Migration Certificate | Student moving between universities | Registrar / Controller of Exams | UGC Guidelines |
| Bonafide / Enrollment | On student request | Auto / Clerk | Scholarship/Railway/Bank norms |
| Character Certificate | On student request | Principal / HOD | Employment / Admission |
| Leaving Certificate | Vocational / ITI exit | Principal | NCVT guidelines |
| No-Objection Certificate | Student competition / internship | HOD | Institutional policy |

### 2.2 Achievement & Participation Certificates

| Certificate | Source Data | Bulk Support |
|---|---|---|
| Academic Rank (1st / 2nd / 3rd) | Module 21 Results | Yes — auto on result publish |
| Subject-Wise Excellence | Module 21 | Yes |
| Sports Participation / Achievement | Sports module records / manual | Yes |
| Cultural Event Participation | Event management records | Yes |
| Science Fair / Olympiad | Manual entry | Yes |
| NSS / NCC / Scout Service | Manual entry | Yes |
| Mock Test Performance (Coaching) | Module 22 Test Series | Yes |
| Course Completion (Coaching) | Batch completion flag | Yes |
| Batch Rank (Coaching, opt-in) | Module 22 | Yes |

### 2.3 Academic / Progression Certificates

| Certificate | Institution Type | Remarks |
|---|---|---|
| Provisional Degree Certificate | University / College | Pending convocation |
| Degree / Diploma Certificate | University / Polytechnic | Post-convocation |
| Official Transcript | University / College | Per application |
| Internship Completion | All types | Institution-issued, not company |
| Early-Completion Certificate | Coaching (self-paced) | Learner finishes ahead of schedule |

---

## 3. TC Compliance & Format Engine

### 3.1 State Board Format Registry

TC format is NOT uniform across India. Each board mandates specific fields, layout, and language requirements. The format registry maps tenant `board_affiliation` to the correct TC template:

| Board | Key Mandatory Fields | Regional Language |
|---|---|---|
| CBSE | Board Roll Number, Subjects List, Passing Status | Hindi (optional) |
| ICSE | Council Roll Number, Year of Passing | English only |
| SSC (Andhra / Telangana) | Aadhaar Number, Caste, Religion | Telugu |
| SSLC (Karnataka / Kerala / TN) | EMIS / UDISE code, Mother Tongue | Kannada / Malayalam / Tamil |
| NIOS | Stream, Credit Accumulation | Hindi / English |
| CBSE Class XII | Stream, Elective Subjects | — |
| State University | Enrollment No., CPI/SGPA | Regional |

The format registry is seeded with known board formats and is editable by Super Admin. Tenant admins select their board affiliation during onboarding (Module 04); the engine auto-selects the correct TC template.

### 3.2 Mandatory TC Fields (All Boards)

```
- Student full name (as per admission records)
- Father's / Guardian's name
- Date of Birth (DD/MM/YYYY)
- Admission date
- Class / Standard at time of leaving
- Date of leaving
- Medium of instruction
- Conduct grade (A = Exemplary / B = Good / C = Satisfactory / D = Poor)
- Cumulative attendance percentage
- Whether the student has paid all dues (Yes / No)
- Board roll number (if allocated)
- Subjects studied (list)
- Reason for leaving (Transfer / Parent request / Completed course / Expelled / Other)
- TC serial number
- Date of issue
- Principal's signature and institution seal
```

### 3.3 TC Status Machine

```
DRAFT → CLEARANCE_PENDING → ALL_CLEARED → APPROVED → GENERATED → ISSUED
                                                    ↓
                                               CANCELLED  (student returns)
                                               REVOKED    (fraud suspected)
                                               DUPLICATE  (re-issue after loss)
```

Expelled students have conduct grade D auto-populated; principal must manually confirm before TC generation.

### 3.4 Bilingual TC

For state board institutions requiring bilingual TC:

- PDF is rendered as a two-column layout: English (left) / Regional language (right)
- Regional language fonts (Noto Serif for all Indian scripts) embedded in PDF
- Language pair configured in tenant settings: `primary_language = "en"`, `secondary_language = "te"` (Telugu)
- Institution name, address, and principal name translated at tenant setup (stored, not auto-translated)
- Student name transliteration via Unicode NFC normalisation — manual override available

---

## 4. TC Clearance Engine

### 4.1 Clearance Department Configuration

Clearance departments are configurable per institution type. Defaults:

| Institution Type | Default Clearance Departments |
|---|---|
| School (Day) | Fee, Library |
| School (Residential) | Fee, Library, Hostel, Transport |
| College / University | Fee, Library, Hostel, Lab, Sports, Department |
| Coaching | Fee |
| Polytechnic / ITI | Fee, Library, Lab, Hostel |

Institution admin can add / remove departments from the clearance matrix.

### 4.2 Clearance Workflow

1. TC request submitted by student/parent
2. System checks for active enrollment; if enrolled, clearance workflow triggers
3. Each clearance department receives a notification: "TC clearance required for [Student Name], Class [X]"
4. Auto-clearance rule: if a department has zero records for this student (e.g., student never borrowed from library), clearance is auto-granted within 5 minutes with note "No records — auto-cleared"
5. Department staff reviews and either:
   - **Clears** — optionally adds remarks (e.g., "Fine of ₹50 collected — Receipt #R-0293")
   - **Blocks** — adds reason (e.g., "2 books not returned")
6. Clearance deadline: 3 working days per department
7. On deadline breach: escalation notification sent to Principal
8. All departments cleared → TC approval unlocked in Principal's queue

### 4.3 Clearance Dashboard

```
┌────────────────────────────────────────────────────────┐
│  TC Clearance — Pending (12 students)                  │
├──────────────┬──────────┬──────────┬────────┬──────────┤
│ Student      │ Class    │ Days Open│ Status │ Depts    │
├──────────────┼──────────┼──────────┼────────┼──────────┤
│ Arjun Mehta  │ X-A      │ 2        │ 3/5 ✓  │ Fee ⏳   │
│ Priya Sharma │ XII-B    │ 4 ⚠️     │ 4/5 ✓  │ Lab ⏳   │
└──────────────┴──────────┴──────────┴────────┴──────────┘
```

Bottleneck heatmap — which department has the longest average clearance time — visible to Principal.

### 4.4 RTE Exception

RTE-tagged students (Module 07): dues-gate **disabled** by law. TC must be issued even if fees are unpaid. System detects RTE tag and skips fee clearance department automatically, with a logged note "RTE student — fee clearance bypassed per RTE S.4".

---

## 5. PDF Generation Pipeline

### 5.1 Technology

- **WeasyPrint 60+** running in AWS Lambda (512 MB, 30s timeout)
- Template stored as HTML + CSS in Cloudflare R2: `templates/{tenant_id}/{cert_type}/{template_version}.html`
- Dynamic field injection via Jinja2 before WeasyPrint render
- Output format: **PDF/A-1b** (ISO 19005-1) — long-term archival compliant
- All fonts embedded in PDF (not referenced externally) — guaranteed rendering on any viewer

### 5.2 QR Code Embedding

- QR code generated using `qrcode` Python library
- QR payload: `https://verify.{tenant_domain}/cert/{cert_uuid}` — short, stable URL
- QR image embedded as base64 in the HTML before rendering
- QR size: 3 cm × 3 cm in footer of certificate
- Certificate serial number and SHA-256 hash (truncated to 16 chars) printed below QR in 7pt font

### 5.3 Digital Signature (Image-Based)

- Principal / HOD signature image uploaded at onboarding (Module 04) — stored in R2
- Signature image fetched at render time and injected into template
- Institution seal / stamp image similarly injected
- True DSC (Digital Signature Certificate) integration — planned for Phase 2 (uses pyhanko library)

### 5.4 Template Versioning

Each template record:
```json
{
  "template_id": "tmpl_tc_cbse_en_v3",
  "cert_type": "TC",
  "board": "CBSE",
  "language": "en",
  "version": 3,
  "active": true,
  "r2_path": "templates/global/tc/cbse_en_v3.html"
}
```

When a template is updated (version incremented), historical certificates retain the version used at issuance (`cert.template_version` stored). Re-download always regenerates from the original template version to ensure the document is identical to what was issued.

### 5.5 Certificate Hash & Immutability

```python
# After WeasyPrint renders PDF bytes:
cert_hash = hashlib.sha256(pdf_bytes).hexdigest()
# Store in DB: certs.content_hash
# Embed in footer: first 16 chars
# Upload to R2: certs/{tenant}/{year}/{type}/{cert_uuid}.pdf
```

On re-download:
```python
pdf_bytes = r2.get(cert.r2_path)
live_hash = hashlib.sha256(pdf_bytes).hexdigest()
assert live_hash == cert.content_hash, "INTEGRITY_FAILURE"
```

Any R2-side corruption detected immediately on download attempt.

---

## 6. Certificate Storage & Delivery

### 6.1 R2 Storage Layout

```
certs/
  {tenant_id}/
    {academic_year}/         # e.g., 2025-26
      tc/
        {cert_uuid}.pdf
      bonafide/
        {cert_uuid}.pdf
      achievement/
        {cert_uuid}.pdf
      bulk_zips/
        {job_id}.zip         # 24-hour TTL then deleted
```

Private bucket — zero public access. All downloads via pre-signed URLs.

### 6.2 Pre-Signed URL Policy

| Certificate Type | URL Expiry | Notes |
|---|---|---|
| TC | Non-expiring | Legal document; may need re-download years later |
| Migration Certificate | Non-expiring | Legal |
| Degree / Diploma | Non-expiring | Legal |
| Bonafide | 30 days | Short-lived; re-generate on expiry |
| Character | 30 days | — |
| Participation / Achievement | 1 year | Re-generate on expiry |
| Bulk ZIP | 24 hours | Deleted from R2 after TTL |

### 6.3 Delivery Channels

| Channel | Trigger | Module |
|---|---|---|
| In-app Download Centre | Always | This module |
| Email (PDF attachment) | On issuance | Module 37 |
| WhatsApp (media message) | On issuance (if opted in) | Module 36 |
| Push Notification | On issuance | Module 35 |
| SMS (link to download) | On status change | Module 38 |
| DigiLocker | Student-initiated push | Section 8 |

---

## 7. QR Verification Portal

### 7.1 Public Portal

URL pattern: `https://verify.{tenant_domain}/cert/{cert_uuid}`

No login required. Served from Cloudflare CDN — static page with one API call.

Response card displayed:

```
┌─────────────────────────────────────────┐
│  ✅  Certificate Verified               │
│                                         │
│  Type:         Transfer Certificate     │
│  Issued by:    Delhi Public School      │
│  Student:      A*** M***a               │ ← masked
│  Date Issued:  15 Mar 2026              │
│  Status:       VALID                    │
│                                         │
│  This certificate was issued by         │
│  EduForge-powered institution.          │
└─────────────────────────────────────────┘
```

Student name masked to first name + last-name initial for privacy on the public portal.

### 7.2 Verification Status Codes

| Status | Meaning |
|---|---|
| VALID | Certificate exists, hash matches, not revoked |
| CANCELLED | TC cancelled after student re-admission |
| REVOKED | Principal revoked due to fraud suspicion |
| DUPLICATE | This is a duplicate issue; original exists |
| TAMPERED | Hash mismatch — PDF content modified after issuance |
| NOT_FOUND | UUID not in system — likely forged QR |

TAMPERED and NOT_FOUND trigger an internal alert to Super Admin.

### 7.3 Bulk Verification API

For receiving institutions (e.g., a university verifying a TC batch):

```
POST /api/v1/verify/bulk
Authorization: Bearer {api_key}
{
  "cert_ids": ["uuid1", "uuid2", "uuid3"]
}
```

Rate-limited: 100 requests / minute per API key. API key issued via Module 51 (B2B API Portal).

### 7.4 Verification Audit Log

Every QR scan / API call logged:

```sql
CREATE TABLE cert_verification_log (
  id              UUID PRIMARY KEY,
  cert_id         UUID REFERENCES certificates(id),
  verified_at     TIMESTAMPTZ NOT NULL,
  requester_ip    INET,
  user_agent      TEXT,
  result          TEXT, -- VALID / TAMPERED / NOT_FOUND etc.
  api_key_id      UUID -- null for portal scans
);
```

---

## 8. DigiLocker & National Repositories

### 8.1 DigiLocker Push

DigiLocker Pull API (v2) used to push institution-issued documents to student's DigiLocker locker:

1. Student grants OAuth consent on DigiLocker — EduForge redirects to DigiLocker OAuth flow
2. Consent token stored (encrypted at rest) in `student_integrations` table
3. On certificate issuance, Lambda function calls DigiLocker Document API with:
   - Document type (certificate category)
   - PDF binary
   - Student's Aadhaar-linked DigiLocker account (matched via mobile number or Aadhaar)
4. DigiLocker responds with issue document ID — stored in `certificates.digilocker_id`
5. If push fails: queued for retry (SQS); student notified to push manually from Download Centre

Consent model:
- Consent given per student — persists until revoked
- Student can revoke from Settings → Connected Services
- Revocation triggers deletion of consent token; previously pushed documents remain in DigiLocker (DigiLocker rule)

### 8.2 DigiLocker Pull (Receiving)

During TC-received verification in Module 07 (enrollment of a new student):
- Admin enters TC number and issuing school's DigiLocker-registered name
- EduForge calls DigiLocker Pull API to fetch the TC PDF directly from issuing institution's locker
- Bypasses physical TC requirement where both institutions are DigiLocker-registered

### 8.3 APAAR ID / ABC

- APAAR ID (Academic Bank of Credits ID) stored in student profile (Module 07)
- On course completion certificate issuance (coaching / college):
  - Credit units submitted to ABC registry via UGC ABC API
  - ABC transaction ID stored in `certificates.abc_txn_id`
- ABC credit summary visible in student's Download Centre alongside certificates

### 8.4 National Academic Depository (NAD)

- University-tier tenants can upload degree/diploma PDFs to NAD via NAD API
- NAD returns a permanent document ID — stored and displayed to student
- NAD upload triggered after Principal marks "Degree Awarded" in the academic record

---

## 9. Request Portal (Student / Parent)

### 9.1 Request Form

```
Certificate Type:    [Transfer Certificate ▾]
Purpose:            [New School Admission ▾]
Urgency:            ● Standard (3 working days)
                    ○ Urgent (1 working day) — ₹100 processing fee
Number of Copies:   [1] (for TC: locked at 1)
Delivery Preference: ✅ Email  ✅ WhatsApp  ✅ Download Centre
Additional Note:    [___________________]
[Submit Request]
```

Purpose dropdown codes drive analytics (scholarship, bank, passport, railway, sports, electoral, employment, other).

### 9.2 Active Enrollment Gate

Certain certificates require the student to be in active status:
- Bonafide — requires ACTIVE enrollment
- Character — requires ACTIVE or COMPLETED (graduated)
- TC — requires ACTIVE (cannot request TC if already left)
- Achievement — available to ACTIVE or ALUMNI

### 9.3 Self-Service Auto-Approval

Certificates that bypass the approval queue:

| Certificate | Auto-Approval Condition |
|---|---|
| Bonafide | Student is ACTIVE, ≤ 3 requests this academic year |
| Participation | Event record exists in system |
| Course Completion (Coaching) | Batch marked complete, attendance ≥ 75% |

Auto-approved certificates are generated and delivered within 60 seconds of request.

### 9.4 Request Status Tracking

```
[Submitted] → [Clearance Pending] → [All Cleared] → [Approved] → [Generating] → [Issued]
                     ↓ (TC)
             [Clearance Blocked — Library: 2 books pending]
```

Real-time status via push notification (Module 35) and in-app badge on Certificates section.

---

## 10. Bulk Certificate Generation

### 10.1 Bulk Triggers

| Trigger | Certificates Generated | Initiator |
|---|---|---|
| Result publish (Module 21) | Achievement certificates for top-N per class | Automated |
| Exam session close (Module 19) | Participation certificates for all examinees | Admin-triggered |
| Batch completion (Module 22) | Course completion certificates | Admin-triggered |
| Annual scholarship season | Bonafide for entire class/batch | Admin-triggered |
| Event completion | Participation certificates from event roster | Admin-triggered |

### 10.2 Bulk Job Pipeline

```
Admin clicks "Generate Bulk Certificates"
        ↓
Validation: Check all students have required data fields
        ↓
Job created in bulk_cert_jobs table; status = QUEUED
        ↓
SQS message → Lambda workers (up to 10 parallel)
        ↓
Each Lambda: renders PDF, uploads to R2, logs cert record
        ↓
Job progress: WebSocket event to admin browser (% complete)
        ↓
Failures collected in bulk_cert_failures (student_id, reason)
        ↓
On completion: ZIP created, admin notified; email/WhatsApp dispatch begins
```

### 10.3 Failure Handling

Common failures and auto-remediation suggestions:

| Failure | Cause | Suggested Fix |
|---|---|---|
| Missing DOB | Student profile incomplete | Link to student edit form |
| Missing signature image | Principal signature not uploaded | Link to Settings → Signatures |
| Template missing | Board format not configured | Link to Template Manager |
| PDF render timeout | Complex multilingual layout | Retry with simplified template |

Admin can fix data and retry individual failed records without re-running the entire batch.

### 10.4 Bulk Download ZIP

- ZIP created in Lambda after all PDFs generated
- File naming: `{roll_number}_{student_name_sanitized}_{cert_type}.pdf`
- ZIP stored in R2 with 24-hour TTL
- Bulk dispatch: SES + WhatsApp sends run as background SQS jobs
- Dispatch progress shown in admin panel: "1,247 / 1,380 emails sent"

---

## 11. Custom Certificate Builder

### 11.1 Purpose

Schools run dozens of events — interschool quiz, annual day, science expo, robotics competition — each requiring a custom certificate. The builder allows admin to define new certificate types without engineering support.

### 11.2 Builder Interface

- Template Designer: WYSIWYG editor (TipTap-based) for certificate body text
- Available placeholders: `{{student_name}}`, `{{class}}`, `{{event_name}}`, `{{date}}`, `{{rank}}`, `{{score}}`, `{{institution_name}}`, `{{principal_name}}`
- Custom fields: admin defines event-specific fields (e.g., "Category", "Score out of 100")
- Background image upload: R2-stored; rendered behind text
- Preview mode: renders a sample PDF with dummy data
- Save as new certificate type; appears in student request dropdown and bulk generation

### 11.3 Custom Series Numbering

Custom certificates use a separate series: `EVT-{event_code}-2025-26-XXXX`

Custom certificates are included in the QR verification portal with type label "Custom Award — {event_name}".

---

## 12. Duplicate TC Process

### 12.1 Workflow

When a student reports a lost or damaged TC:
1. Student submits Duplicate TC request with reason (Lost / Damaged)
2. System flags: if original TC is ISSUED, duplicate request enters admin queue
3. Admin checks if a police FIR / notarised affidavit has been submitted — document uploaded to system
4. After admin approval, TC is regenerated from original template version with all original data
5. PDF rendered with large diagonal "DUPLICATE" watermark (red, 40% opacity)
6. TC register updated: "Duplicate TC issued on [date], Affidavit No. [X]"
7. QR verification shows status "DUPLICATE — Original issued [original date]"
8. Original TC UUID remains; a new certificate record created with `is_duplicate = true`, `original_cert_id = UUID`

---

## 13. Analytics & Reports

### 13.1 Certificate Operations Dashboard

```
┌──────────────────────────────────────────────────────────┐
│  Certificates — This Academic Year                       │
├──────────────┬──────────────┬────────────┬───────────────┤
│  Type        │  Issued      │  Pending   │  Avg. Days    │
├──────────────┼──────────────┼────────────┼───────────────┤
│  TC          │  47          │  3         │  4.2 days     │
│  Bonafide    │  1,240       │  0         │  0.1 days     │
│  Character   │  89          │  2         │  2.1 days     │
│  Achievement │  3,420       │  —         │  0.02 days    │
│  Custom      │  678         │  —         │  0.01 days    │
└──────────────┴──────────────┴────────────┴───────────────┘
```

### 13.2 TC Dropout Signal

TC issuance rate by class / month feeds Module 32 (Student Welfare) Early Warning System:

- ≥ 3 TC requests in a class in a month → EWS trigger: "Dropout cluster detected in [Class X]"
- Principal alerted; counsellor assigned
- Useful for detecting cohort-level issues (teacher conflict, fee pressure, bullying)

### 13.3 Clearance Bottleneck Report

```
Department Clearance Times (Average, Last 12 Months)
Library    ████████████████  3.2 days   ← longest
Fee        ████             0.8 days
Hostel     ██████████       2.1 days
Lab        ██               0.4 days
```

Principal uses this to identify which department needs process improvement or staffing.

### 13.4 Cost Report

```
Monthly Certificate Cost Breakdown
  R2 Storage (PDFs)        : ₹  120
  Lambda (PDF render)      : ₹   43
  SES Email delivery       : ₹   88
  WhatsApp certificate msg : ₹  340
  DigiLocker API calls     : ₹    0  (free tier)
  ────────────────────────────────
  Total                    : ₹  591  (1,847 certs issued)
  Per-certificate cost     : ₹ 0.32
```

### 13.5 Key Metrics Tracked

| Metric | Target |
|---|---|
| TC issuance within 15 working days | ≥ 99% |
| Bonafide auto-approval success rate | ≥ 98% |
| PDF generation failure rate | < 0.1% |
| QR verification latency | < 500 ms P99 |
| DigiLocker push success rate | ≥ 95% |
| Bulk generation throughput | ≥ 100 certs / minute |

---

## 14. DPDPA 2023 & Retention Compliance

### 14.1 Data Classification

Certificates contain Personally Identifiable Information classified under DPDPA 2023:

| Field | Classification | Storage |
|---|---|---|
| Student name | PII | In certificate PDF + DB |
| Date of birth | Sensitive PII | In TC PDF + DB |
| Attendance % | Educational record | DB |
| Conduct grade | Educational record | DB |
| Aadhar in TC (some states) | Sensitive PII | Masked to last 4 digits |
| Address (bonafide) | PII | In PDF + DB |

### 14.2 Retention Schedule

| Certificate Type | Retention Period | Post-Retention Action |
|---|---|---|
| Transfer Certificate | 10 years (state mandate) | Archive to cold storage; do not delete |
| Migration Certificate | 10 years | Archive |
| Degree / Diploma | Permanent | Never delete |
| Bonafide | 5 years | Anonymise student fields after 5 years |
| Character | 5 years | Anonymise |
| Achievement / Participation | 5 years | Anonymise |
| Verification logs | 3 years | Delete IP, retain cert_id + result |

System runs a nightly retention job that flags records approaching retention expiry for Super Admin review before action.

### 14.3 Right to Erasure Handling

- **TC, Migration, Degree** — exempt from erasure under DPDPA (legal obligation to retain); system displays this reason if student submits erasure request
- **Bonafide, Character** — erased after retention period; PDF deleted from R2; DB fields anonymised
- **Verification logs** — IP addresses deleted after 3 years; cert_id retained for integrity

### 14.4 Access Rights

- Student — download own certificates (no request needed); view own request history
- Parent — download certificates for minor children
- No role — can view another student's certificate content (only type/date metadata via admin tools)
- Admin — can view metadata (type, date, status) but not certificate PDF content unless Principal role

### 14.5 Third-Party Sharing Log

If the institution integrates a third-party verification service, every API call that retrieves certificate data must be logged under DPDPA Article 6 (purpose of processing):

```sql
CREATE TABLE cert_third_party_access (
  id              UUID PRIMARY KEY,
  cert_id         UUID REFERENCES certificates(id),
  accessed_at     TIMESTAMPTZ NOT NULL,
  third_party     TEXT,           -- DigiLocker / NAD / B2B partner
  purpose         TEXT,           -- enrollment-verification / scholarship etc.
  data_shared     JSONB           -- fields shared (NOT the PDF content)
);
```

---

## 15. Database Schema

```sql
-- Certificate records
CREATE TABLE certificates (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL REFERENCES tenants(id),
  student_id        UUID NOT NULL REFERENCES students(id),
  cert_type         TEXT NOT NULL,          -- TC, BONAFIDE, CHARACTER, ACHIEVEMENT, etc.
  cert_number       TEXT NOT NULL,          -- TC-2025-26-0047
  academic_year     TEXT NOT NULL,          -- 2025-26
  purpose           TEXT,                   -- bank, scholarship, new-admission, etc.
  status            TEXT NOT NULL DEFAULT 'ISSUED',  -- ISSUED, CANCELLED, REVOKED, DUPLICATE
  is_duplicate      BOOLEAN DEFAULT FALSE,
  original_cert_id  UUID REFERENCES certificates(id),
  template_version  TEXT NOT NULL,
  content_hash      TEXT NOT NULL,          -- SHA-256 of PDF
  r2_path           TEXT NOT NULL,
  issued_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
  issued_by_id      UUID REFERENCES staff(id),
  expires_at        TIMESTAMPTZ,            -- for bonafide/character
  digilocker_id     TEXT,                   -- DigiLocker document ID
  abc_txn_id        TEXT,                   -- ABC registry transaction
  nad_doc_id        TEXT,                   -- NAD document ID
  metadata          JSONB,                  -- type-specific fields (rank, event, etc.)
  created_at        TIMESTAMPTZ DEFAULT now(),
  updated_at        TIMESTAMPTZ DEFAULT now()
);

CREATE UNIQUE INDEX idx_cert_number ON certificates(tenant_id, cert_type, cert_number);
CREATE INDEX idx_cert_student ON certificates(student_id);
CREATE INDEX idx_cert_status ON certificates(status);

-- Certificate series counters
CREATE TABLE cert_series (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id     UUID NOT NULL REFERENCES tenants(id),
  campus_id     UUID REFERENCES campuses(id),
  cert_type     TEXT NOT NULL,
  academic_year TEXT NOT NULL,
  last_number   INT NOT NULL DEFAULT 0,
  prefix        TEXT NOT NULL,
  UNIQUE (tenant_id, campus_id, cert_type, academic_year)
);

-- Certificate requests
CREATE TABLE cert_requests (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  student_id      UUID NOT NULL REFERENCES students(id),
  requested_by_id UUID REFERENCES users(id),
  cert_type       TEXT NOT NULL,
  purpose         TEXT,
  urgency         TEXT DEFAULT 'standard',   -- standard, urgent
  status          TEXT DEFAULT 'PENDING',    -- PENDING, CLEARANCE, APPROVED, REJECTED, GENERATING, ISSUED
  rejection_reason TEXT,
  cert_id         UUID REFERENCES certificates(id),
  requested_at    TIMESTAMPTZ DEFAULT now(),
  issued_at       TIMESTAMPTZ,
  delivery_email  BOOLEAN DEFAULT TRUE,
  delivery_whatsapp BOOLEAN DEFAULT FALSE,
  metadata        JSONB
);

-- TC clearance workflow
CREATE TABLE tc_clearances (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id      UUID NOT NULL REFERENCES cert_requests(id),
  department      TEXT NOT NULL,    -- FEE, LIBRARY, HOSTEL, LAB, TRANSPORT, SPORTS
  status          TEXT DEFAULT 'PENDING',   -- PENDING, AUTO_CLEARED, CLEARED, BLOCKED
  cleared_by_id   UUID REFERENCES staff(id),
  cleared_at      TIMESTAMPTZ,
  remarks         TEXT,
  deadline        DATE NOT NULL,
  escalated       BOOLEAN DEFAULT FALSE
);

-- Bulk generation jobs
CREATE TABLE bulk_cert_jobs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  cert_type       TEXT NOT NULL,
  total           INT NOT NULL,
  success_count   INT DEFAULT 0,
  fail_count      INT DEFAULT 0,
  status          TEXT DEFAULT 'QUEUED',    -- QUEUED, RUNNING, DONE, PARTIAL
  zip_r2_path     TEXT,
  zip_expires_at  TIMESTAMPTZ,
  initiated_by_id UUID REFERENCES staff(id),
  started_at      TIMESTAMPTZ,
  completed_at    TIMESTAMPTZ,
  parameters      JSONB
);

CREATE TABLE bulk_cert_failures (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  job_id      UUID NOT NULL REFERENCES bulk_cert_jobs(id),
  student_id  UUID REFERENCES students(id),
  reason      TEXT NOT NULL,
  retried     BOOLEAN DEFAULT FALSE
);

-- Verification audit log
CREATE TABLE cert_verification_log (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cert_id       UUID REFERENCES certificates(id),
  verified_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
  requester_ip  INET,
  user_agent    TEXT,
  result        TEXT NOT NULL,    -- VALID, CANCELLED, REVOKED, TAMPERED, NOT_FOUND
  api_key_id    UUID
);

-- Custom certificate types
CREATE TABLE custom_cert_types (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  type_code       TEXT NOT NULL,
  display_name    TEXT NOT NULL,
  template_r2_path TEXT NOT NULL,
  custom_fields   JSONB,          -- [{name, label, type, required}]
  series_prefix   TEXT NOT NULL,
  active          BOOLEAN DEFAULT TRUE,
  created_at      TIMESTAMPTZ DEFAULT now()
);
```

---

## 16. API Reference

### 16.1 Student-Facing Endpoints

```
GET    /api/v1/certificates/               # Download Centre — all issued certs
POST   /api/v1/certificates/requests/      # Submit new certificate request
GET    /api/v1/certificates/requests/{id}/ # Request status
GET    /api/v1/certificates/{id}/download/ # Get pre-signed download URL
GET    /api/v1/certificates/{id}/share/    # Get shareable pre-signed URL
POST   /api/v1/certificates/{id}/digilocker-push/  # Push to DigiLocker
```

### 16.2 Admin Endpoints

```
GET    /api/v1/admin/cert-requests/                    # Request queue
PATCH  /api/v1/admin/cert-requests/{id}/approve/       # Approve
PATCH  /api/v1/admin/cert-requests/{id}/reject/        # Reject with reason
GET    /api/v1/admin/tc-clearances/{request_id}/       # Clearance status
PATCH  /api/v1/admin/tc-clearances/{id}/clear/         # Clear department
POST   /api/v1/admin/bulk-certs/                       # Start bulk job
GET    /api/v1/admin/bulk-certs/{job_id}/              # Job progress
GET    /api/v1/admin/bulk-certs/{job_id}/download/     # ZIP pre-signed URL
PATCH  /api/v1/admin/certificates/{id}/revoke/         # Revoke certificate
GET    /api/v1/admin/cert-analytics/                   # Analytics dashboard
```

### 16.3 Public Verification

```
GET    /api/v1/public/verify/{cert_uuid}/   # QR verification — no auth
POST   /api/v1/public/verify/bulk/          # Bulk verification — API key
```

### 16.4 Department Clearance Portal

```
GET    /api/v1/dept/tc-clearances/          # Dept's pending clearance queue
PATCH  /api/v1/dept/tc-clearances/{id}/    # Clear / block
```

---

## 17. RBAC Matrix

| Action | Student | Parent | Class Teacher | Clerk | HOD / Principal | Super Admin |
|---|---|---|---|---|---|---|
| Request certificate | ✅ (self) | ✅ (child) | ❌ | ❌ | ❌ | ❌ |
| View own certificates | ✅ | ✅ (child) | ❌ | ❌ | ❌ | ❌ |
| View any student cert metadata | ❌ | ❌ | ✅ (own class) | ✅ | ✅ | ✅ |
| Approve certificate request | ❌ | ❌ | ✅ (bonafide, own class) | ✅ (bonafide) | ✅ (all) | ✅ |
| Clear TC department | ❌ | ❌ | ❌ | ✅ (own dept) | ✅ | ✅ |
| Generate bulk certificates | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Revoke certificate | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| View verification log | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Create custom cert type | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Upload signature image | ❌ | ❌ | ❌ | ❌ | ✅ (own) | ✅ |

---

## 18. Cross-Module Integration Map

| Module | Integration Point |
|---|---|
| Module 04 — Institution Onboarding | TC format / board selection; principal signature; institution seal; campus TC series |
| Module 07 — Student Enrolment | Student data fields for certificates; TC triggers profile status → LEFT; TC-received flag for incoming students |
| Module 21 — Results & Report Cards | Achievement certificate auto-generation on result publish; bonafide during exam season |
| Module 22 — Test Series (Coaching) | Course completion and batch rank certificates |
| Module 24 — Fee Structure | Urgent certificate fee collection; dues-gate for TC |
| Module 28 — Hostel | Hostel clearance department in TC workflow |
| Module 30 — Library | Library clearance department; fine status in clearance |
| Module 32 — Student Welfare | TC issuance rate feeds EWS dropout signal |
| Module 35 — Notifications (FCM) | Push notification on certificate issuance and status change |
| Module 36 — WhatsApp | Certificate PDF delivery via WhatsApp media message |
| Module 37 — Email / SES | Certificate email delivery with PDF attachment |
| Module 38 — SMS & OTP | Status-change SMS for TC processing milestones |
| Module 42 — DPDPA & Audit Log | All certificate PII access events logged for compliance |
| Module 51 — B2B API Portal | Bulk verification API key issuance |

---

*Module 39 — Certificates & TC — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
