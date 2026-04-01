# Module 40 — Document Management

## 1. Purpose

Every institution in India operates under an obligation to collect, verify, and retain dozens of categories of documents — student admission proofs, staff qualifications, compliance certificates, affiliation orders, NAAC/NIRF evidence, and regulatory filings. These documents are the evidentiary foundation for accreditation, audits, court proceedings, scholarship disbursements, and routine administration. Physical document rooms are fire hazards, require manual tracking, and make audit-readiness a seasonal scramble.

EduForge Module 40 is the centralised, tenant-isolated document repository covering all three entity types — students, staff, and the institution itself. It handles mobile camera capture (with ML-based edge detection), OCR indexing (AWS Textract), fraud detection signals, expiry tracking, compliance export packages for CBSE/NAAC/AICTE/NIRF/AISHE, version control, legal hold, and DPDPA-compliant retention. Every document access event is logged. No document is publicly accessible; all access is via pre-signed URLs with appropriate expiry.

---

## 2. Document Taxonomy

### 2.1 Student Documents

| Document Type | Mandatory For | Validity |
|---|---|---|
| Proof of Date of Birth (Birth Cert / TC / Aadhaar) | All enrolments | Permanent |
| Proof of Address | Hostel / RTE / Scholarship | Permanent |
| Passport-size photograph | All enrolments | Annual renewal |
| Transfer Certificate (received) | School / College transfer | Permanent |
| Previous academic mark sheets | All enrolments | Permanent |
| Caste certificate (SC/ST/OBC/EWS) | Reserved category benefits | Permanent |
| Income certificate | Scholarship / fee concession | 1 year |
| UDID (Disability ID) | CWSN students | Permanent |
| Medical fitness certificate | Hostel / sports | 1 year |
| Vaccination record | Hostel admission | Per schedule |
| Blood group certificate | All hostel students | Permanent |
| Guardian ID proof (parent Aadhaar) | Minor students | Permanent |
| Passport + visa | International students | Visa expiry |
| Migration certificate | University transfers | Permanent |
| Entrance exam scorecard | Merit-based admission | Permanent |
| Sports / achievement certificates | Bonus-mark admission | Permanent |
| Anti-ragging undertaking | All (UGC 2009) | Annual |
| POCSO awareness acknowledgement | Hostel students | Annual |

### 2.2 Staff Documents

| Document Type | Mandatory For | Validity |
|---|---|---|
| Appointment letter | All staff | Permanent |
| Joining report | All staff | Permanent |
| Police verification certificate | School / hostel staff (POCSO) | 3 years |
| Previous employer relieving letters | All teaching staff | Permanent |
| All qualification certificates | Teaching staff | Permanent |
| CTET / TET certificate | School teachers (RTE S.23) | Lifetime |
| NET / SET / SLET certificate | College / university teachers | Lifetime |
| Medical fitness certificate | Hostel wardens, bus drivers | 1 year |
| Training / CPD certificates | All staff | Per course |
| Contract / bond documents | Bonded staff | Duration of bond |
| PAN card copy | All staff (TDS) | Permanent |
| Aadhaar card copy | All staff (ESI/PF) | Permanent |

### 2.3 Institutional / Compliance Documents

| Document Type | Authority | Renewal |
|---|---|---|
| Society / Trust / Company registration | ROC / Charity Commissioner | Periodic |
| GST registration certificate | GSTN | Permanent |
| PAN / TAN of institution | Income Tax | Permanent |
| Land deed / lease agreement | Registrar | Per lease |
| Building plan approval | Municipal authority | Permanent |
| NOC from fire department | Fire department | Annual |
| DEO / BEO recognition order | State education dept | — |
| Board affiliation certificate | CBSE / ICSE / State | Per cycle |
| UGC recognition | UGC | Permanent |
| AICTE approval | AICTE | Annual |
| NAAC accreditation | NAAC | 5 years |
| FSSAI license | FSSAI | 1 year |
| Motor vehicle permits | RTO | Annual |
| POCSO committee constitution | Institution | Annual |
| Anti-ragging committee constitution | Institution (UGC) | Annual |
| ICC constitution (POSH 2013) | Institution | Annual |
| DPDPA data processor agreements | Institution | Per contract |
| Annual audit report | CA-certified | Annual |
| Insurance policies | Insurer | Annual |

---

## 3. Storage Architecture

### 3.1 R2 Bucket Layout

```
documents/
  {tenant_id}/
    students/
      {student_id}/
        dob_proof/
          {doc_uuid}.pdf
        photograph/
          {doc_uuid}.jpg
        tc_received/
          {doc_uuid}.pdf
        ...
    staff/
      {staff_id}/
        police_verification/
          {doc_uuid}.pdf
        qualifications/
          {doc_uuid}.pdf
        ...
    institution/
      compliance/
        {doc_uuid}.pdf
      affiliation/
        {doc_uuid}.pdf
      ...
    thumbnails/
      {doc_uuid}_thumb.jpg        # First-page JPEG for preview
    temp_zips/
      {job_id}.zip                # 24-hour TTL — bulk downloads
```

Private bucket — zero public access. All access via pre-signed URLs.

### 3.2 Pre-Signed URL Policy

| Document Category | View URL Expiry | Download URL Expiry |
|---|---|---|
| Student documents | 1 hour | 24 hours |
| Staff documents | 1 hour | 24 hours |
| Institution compliance | 4 hours | 48 hours |
| Bulk ZIP | — | 24 hours (then R2 object deleted) |

Pre-signed URLs include an IP binding check at the CDN layer — URL cannot be used from a different IP than the one that requested it.

### 3.3 Format Handling

| Input Format | Processing | Archival Format |
|---|---|---|
| PDF | None | PDF (unchanged) |
| JPG / PNG | Quality optimisation (JPEG 85%) | JPG |
| HEIC (iOS) | Lambda convert to JPEG | JPG |
| Multi-page JPG set (camera scan) | Merged to single PDF via img2pdf | PDF |

File size limit: 5 MB per document (configurable per tenant, max 20 MB).

### 3.4 Thumbnail Generation

For every new document upload:
- Lambda extracts page 1 (PDF) or the image itself
- Resized to 300×420px JPEG using Pillow
- Stored at `thumbnails/{doc_uuid}_thumb.jpg`
- Served via Cloudflare CDN with 30-day Cache-Control
- In-app document list renders thumbnails without any signed URL overhead

---

## 4. Mobile Camera Capture (Flutter)

### 4.1 Document Scanner Module

The Flutter app embeds Google ML Kit Document Scanner:

1. User selects entity + document type
2. Camera opens with overlay grid for alignment
3. ML Kit detects document edges → auto-crops to bounding box
4. Sharpness check (Laplacian variance): if σ < 100, user is prompted "Image is blurry — retake?"
5. Multi-page: after each page, "Add page" or "Done"
6. All captured pages combined into a single PDF before upload

### 4.2 Image Enhancement Pipeline (Lambda)

```python
# OpenCV pipeline on upload Lambda
img = cv2.imread(path)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# Deskew
angle = compute_skew(gray)
img = rotate(img, angle)
# Binarise for text documents
img = cv2.adaptiveThreshold(gray, 255,
    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
    cv2.THRESH_BINARY, 11, 2)
# Auto-contrast
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
img = clahe.apply(gray)
```

Enhancement is bypassed for photograph type documents (preserves natural colours).

### 4.3 Offline Queue

If the device has no connectivity:
- Documents captured and stored in Flutter Hive local DB (encrypted)
- Upload queue resumes automatically when connectivity restored
- Upload queue badge shown on home screen: "3 documents pending upload"

---

## 5. OCR & Indexing (AWS Textract)

### 5.1 OCR Pipeline

```
Document uploaded to R2
        ↓
SQS message → OCR Lambda
        ↓
AWS Textract AnalyzeDocument API call
        ↓
Extracted text + field key-value pairs stored in doc_ocr_results table
        ↓
PostgreSQL full-text index (tsvector) updated on documents table
        ↓
Fraud detection rules applied on extracted fields (Section 6)
```

Textract confidence score stored per page; pages with average confidence < 70% flagged for "Manual OCR Review."

### 5.2 Full-Text Search

PostgreSQL `tsvector` index on `documents.ocr_text` enables:
- Search by content: "find all staff with NET certificate from [university]"
- Filter by field value: "students with income < ₹1,00,000" (extracted from income certificate)
- Partial match: fuzzy name search across all documents

Search results show thumbnail + document type + entity name + match snippet.

### 5.3 OCR Data Storage

```sql
CREATE TABLE doc_ocr_results (
  id              UUID PRIMARY KEY,
  document_id     UUID NOT NULL REFERENCES documents(id),
  page_number     INT NOT NULL,
  raw_text        TEXT,
  key_value_pairs JSONB,      -- {"Name": "Arjun Mehta", "DOB": "15/03/2008"}
  confidence      NUMERIC,    -- avg page confidence 0-100
  textract_job_id TEXT,
  processed_at    TIMESTAMPTZ
);
```

---

## 6. Fraud Detection Engine

All signals are advisory — no auto-rejection. Flags routed to admin review queue.

### 6.1 Format Validation Rules

| Check | Rule | Flag Level |
|---|---|---|
| Aadhaar format | 12 numeric digits; Verhoeff checksum | Warning |
| PAN format | Regex `[A-Z]{5}[0-9]{4}[A-Z]{1}` | Warning |
| DOB cross-check | DOB in document vs. admission form — delta > 30 days | Warning |
| Name fuzzy match | Jaro-Winkler similarity < 0.85 | Info |
| Document date | Issue date in the future | Error |
| Income cert age | Issued > 1 year ago (for scholarship) | Warning |

### 6.2 Duplicate Detection

```sql
-- Detect duplicate Aadhaar across students
SELECT aadhaar_number, COUNT(DISTINCT student_id) as count
FROM doc_ocr_results
WHERE key_value_pairs->>'aadhaar_number' IS NOT NULL
  AND tenant_id = :tenant_id
GROUP BY aadhaar_number
HAVING COUNT(DISTINCT student_id) > 1;
```

Duplicate Aadhaar → immediate alert to Super Admin and Principal with both student records listed.

### 6.3 Photo Face Match

- Student passport photo on admission (document type: PHOTOGRAPH) is the reference
- When an ID proof with an embedded photo is uploaded (e.g., Aadhaar card image), AWS Rekognition `CompareFaces` is called
- Confidence < 80% → "Photo mismatch" flag for admin review
- Rekognition call is optional (configurable per tenant — adds ≈ ₹0.001 per comparison)

### 6.4 EXIF Metadata Forensics

For uploaded JPG/PNG documents:
- EXIF `DateTimeOriginal` checked — if file was created today on a computer (not scanned), flagged as "Possibly not a genuine scan"
- Software field checked — Photoshop / GIMP identified and flagged
- Flags are purely informational; admin reviews

### 6.5 Fraud Flag Handling

```
Document uploaded
      ↓
Fraud detection Lambda runs (async, post-upload)
      ↓
Flags written to doc_fraud_flags table
      ↓
Admin sees flag badges on document in verification queue
      ↓
Admin investigates → verifies physical original OR rejects document
      ↓
Flag resolution logged (investigated_by, resolution, notes)
```

All fraud flags and resolutions logged to Module 42 (DPDPA & Audit Log) as high-priority security events.

---

## 7. Document Verification Workflow

### 7.1 Verification Status Machine

```
NOT_VERIFIED → PENDING_REVIEW → VERIFIED
                             → REJECTED (reason required)
VERIFIED → EXPIRED (when expiry date passes)
REJECTED → NOT_VERIFIED (after re-upload)
```

### 7.2 Verification Methods

| Method | When Used | Logged As |
|---|---|---|
| Physical original checked | Physical document seen in office | "Original Seen" |
| Self-attested copy | Accepted per regulation | "Self-Attested" |
| Notarised copy | Required for duplicate TC affidavit | "Notarised — Notary No. [X]" |
| DigiLocker pull | Document fetched via DigiLocker API | "DigiLocker Pull" |
| Gazette notification | Name-change documents | "Gazette [date]" |
| Online portal verification | Aadhaar UIDAI portal, CBSE board result portal | "Online Verified" |

### 7.3 Document-Type-Specific Rules

Configured in document type registry:

```json
{
  "doc_type": "income_certificate",
  "verification_rules": [
    {"rule": "max_age_days", "value": 365, "severity": "warning"},
    {"rule": "issuing_authority_in", "value": ["Tehsildar", "MRO", "SDM"], "severity": "warning"}
  ],
  "required_for": ["scholarship", "fee_concession", "rte_admission"]
}
```

### 7.4 "Original Seen" Locking

Once a document is marked "Original Seen — Verified":
- Verification status cannot be downgraded without Super Admin action (prevents collusion-based fraud)
- Any attempt to change triggers an alert to Super Admin
- Exception: expiry downgrade (auto, based on date) is permitted

### 7.5 Bulk Verification Session

Admin can enter a bulk verification session:
- Screen shows one document at a time
- Admin clicks "Verified" / "Rejected" / "Skip" with keyboard shortcuts
- Can add a remark before proceeding
- Session completes when queue is empty; summary shown (e.g., "Verified: 43, Rejected: 2, Skipped: 5")

---

## 8. Document Expiry Management

### 8.1 Expiry Registry

```sql
CREATE TABLE doc_type_config (
  doc_type        TEXT PRIMARY KEY,
  display_name    TEXT NOT NULL,
  validity_days   INT,             -- NULL = permanent
  validity_from   TEXT,            -- 'issue_date' or 'ocr_extracted_expiry'
  alert_days      INT[] DEFAULT ARRAY[90, 30, 7],  -- alert at these days before expiry
  entity_types    TEXT[],          -- ['student', 'staff', 'institution']
  required_for    TEXT[]           -- downstream action codes that gate on this doc
);
```

### 8.2 Expiry Dashboard

```
┌──────────────────────────────────────────────────────────────┐
│  Document Expiry Alert Centre                                │
├──────────────────┬──────────────────┬────────────┬──────────┤
│  Document Type   │  Entity          │  Expires   │  Status  │
├──────────────────┼──────────────────┼────────────┼──────────┤
│  Medical Fitness │  Ramesh (Driver) │  3 days ⚠️ │  Active  │
│  FSSAI License   │  Institution     │  12 days   │  Active  │
│  NOC Fire Dept   │  Institution     │  45 days   │  Active  │
│  Police Verif.   │  Meena (Hostel)  │  67 days   │  Active  │
└──────────────────┴──────────────────┴────────────┴──────────┘
```

### 8.3 Expiry Alert Automation

Nightly job checks all verified documents with `expires_at` set:
- 90-day alert: email to institution admin
- 30-day alert: push notification to HR / admin + email
- 7-day alert: push + SMS to HR / admin
- Expired: document status auto-changed to EXPIRED; downstream gates re-triggered

---

## 9. Document Requests (Internal)

### 9.1 Sending a Document Request

Admin selects entity (student/staff) + document type + deadline + message:

```
To:      [Class X-A students — all] ← individual or group
Request: Caste Certificate (for scholarship season)
Deadline: 2026-04-15
Note:    "Please upload a current caste certificate issued after Jan 2025."
[Send Request]
```

### 9.2 Downstream Blocking

Document types can be configured to block specific actions when missing or unverified:

```json
{
  "doc_type": "medical_fitness",
  "blocks_on_missing": ["hostel_check_in"],
  "blocks_on_unverified": ["hostel_check_in"]
}
```

When the student tries to check into the hostel (Module 28), the system checks document status and blocks if the gate is not cleared, showing "Upload and get your medical certificate verified to complete check-in."

### 9.3 Request Tracking

```
Batch Request Sent: "Caste Certificate" — Class X-A (120 students)

Progress:
  Uploaded & Verified   : 87  ████████████████████░░░
  Uploaded, Pending     : 14  ████░░░░░░░░░░░░░░░░░░░
  Not Uploaded — Overdue:  8  ⚠️
  Not Uploaded — On time: 11
```

Overdue students auto-reminded via push + SMS.

---

## 10. Compliance Export Packages

### 10.1 CBSE Affiliation Renewal Package

CBSE mandates specific documents renamed to their naming convention. The export package:
1. Queries all institution documents tagged `cbse_affiliation_required = true`
2. Renames each file per CBSE's convention (e.g., `01_Society_Registration.pdf`, `02_Land_Documents.pdf`)
3. Packages into ZIP with a `Checklist.txt` showing which documents are present / missing
4. Missing document names highlighted in red — admin prompted to upload before exporting

### 10.2 NAAC Criterion-Wise Export

NAAC 2022 framework has 7 criteria. Documents tagged to criteria via `doc_naac_criteria` array field:

| Criterion | Example Documents Tagged |
|---|---|
| 4.1 — Physical Facilities | Building plan, NOC Fire, RPwD certificate |
| 4.2 — Library | OPAC software invoice, N-LIST subscription |
| 5.2 — Student Welfare | Anti-ragging committee, POCSO committee |
| 6.2 — Governance | Trust registration, audit reports, ICC constitution |
| 6.3 — Faculty | TET/NET certificates, CPD records |

Export: per-criterion ZIP with `Criterion_4.1_Physical_Facilities.zip` etc.

### 10.3 Other Packages

| Package | Trigger | Contents |
|---|---|---|
| NIRF Survey | Annual ranking cycle | Infrastructure, faculty qualification, financial docs |
| AISHE Return | Annual AISHE filing | Recognition order, affiliation cert, land docs |
| AICTE Annual | Technical college annual approval | AICTE approval, faculty list, lab equipment |
| Legal / Court | On demand | Redacted export — removes PII not relevant to matter |
| Insurance Claim | On demand | Incident documents, insurance policy, inventory records |

### 10.4 Legal Document Redaction

For court / external proceedings:
1. Admin selects documents to include
2. Admin selects which PII fields to redact (name, Aadhaar, address)
3. Lambda applies black-box redaction using pikepdf on specified page regions (extracted from OCR bounding boxes)
4. Redacted PDF generated as a new document (original unchanged)
5. Redacted document marked with `is_redacted = true` + `redaction_purpose` + `shared_with`

---

## 11. Version Control

Every document has a `version` integer. On replacement:

```
v1 → v2 (new upload)
     ↓
v1 archived: status = ARCHIVED, archived_at = now()
v2 becomes active
```

Version history visible in document detail:

```
[Current] v2 — Medical Fitness Certificate — Verified — Expires Mar 2027
[Archived] v1 — Medical Fitness Certificate — Expired — Expired Mar 2026
             → Uploaded 10 Mar 2025 | Verified by Meera S. on 12 Mar 2025
```

Admin can restore a previous version (rare; in case of erroneous replacement — logs the restore action with reason).

---

## 12. RBAC Matrix

| Action | Student | Parent | Clerk | HR Officer | HOD | Principal | Compliance Officer | Super Admin |
|---|---|---|---|---|---|---|---|---|
| Upload own documents | ✅ | ✅ (child) | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Upload staff documents | ❌ | ❌ | ❌ | ✅ | ✅ (dept) | ✅ | ❌ | ✅ |
| Upload institutional docs | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| View own documents | ✅ | ✅ (child) | — | — | — | — | — | — |
| View student documents | ❌ | ❌ | ✅ | ❌ | ❌ | ✅ | ✅ | ✅ |
| View staff documents | ❌ | ❌ | ❌ | ✅ | ✅ (dept) | ✅ | ✅ | ✅ |
| Verify documents | ❌ | ❌ | ✅ | ✅ | ✅ (dept) | ✅ | ✅ | ✅ |
| Reject documents | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Send document requests | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Generate compliance packages | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Place legal hold | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |
| View fraud flags | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 13. Database Schema

```sql
-- Core document registry
CREATE TABLE documents (
  id                UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id         UUID NOT NULL REFERENCES tenants(id),
  entity_type       TEXT NOT NULL,    -- student, staff, institution
  entity_id         UUID NOT NULL,    -- FK to students/staff/institution
  doc_type          TEXT NOT NULL,    -- caste_certificate, police_verif etc.
  display_name      TEXT NOT NULL,
  version           INT NOT NULL DEFAULT 1,
  status            TEXT NOT NULL DEFAULT 'NOT_VERIFIED',
  -- NOT_VERIFIED / PENDING_REVIEW / VERIFIED / REJECTED / EXPIRED / ARCHIVED
  r2_path           TEXT NOT NULL,
  thumbnail_r2_path TEXT,
  file_size_bytes   INT,
  mime_type         TEXT,
  page_count        INT,
  issue_date        DATE,
  expires_at        DATE,
  issuing_authority TEXT,
  verification_method TEXT,
  verified_by_id    UUID REFERENCES staff(id),
  verified_at       TIMESTAMPTZ,
  rejection_reason  TEXT,
  ocr_text          TEXT,             -- full-text searchable
  ocr_confidence    NUMERIC,
  is_duplicate      BOOLEAN DEFAULT FALSE,
  is_redacted       BOOLEAN DEFAULT FALSE,
  redaction_purpose TEXT,
  legal_hold        BOOLEAN DEFAULT FALSE,
  uploaded_by_id    UUID REFERENCES users(id),
  uploaded_at       TIMESTAMPTZ DEFAULT now(),
  naac_criteria     TEXT[],           -- ["4.1", "6.2"]
  cbse_required     BOOLEAN DEFAULT FALSE,
  aicte_required    BOOLEAN DEFAULT FALSE,
  metadata          JSONB,
  created_at        TIMESTAMPTZ DEFAULT now(),
  updated_at        TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_doc_entity ON documents(tenant_id, entity_type, entity_id);
CREATE INDEX idx_doc_type ON documents(tenant_id, doc_type);
CREATE INDEX idx_doc_status ON documents(status);
CREATE INDEX idx_doc_expires ON documents(expires_at) WHERE expires_at IS NOT NULL;
CREATE INDEX idx_doc_ocr_text ON documents USING GIN (to_tsvector('english', ocr_text));

-- Document version history
CREATE TABLE document_versions (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id     UUID NOT NULL REFERENCES documents(id),
  version         INT NOT NULL,
  r2_path         TEXT NOT NULL,
  status          TEXT NOT NULL,      -- snapshot of status at archive time
  verified_by_id  UUID REFERENCES staff(id),
  verified_at     TIMESTAMPTZ,
  archived_at     TIMESTAMPTZ DEFAULT now(),
  archive_reason  TEXT,               -- "Annual renewal" / "Admin restore"
  archived_by_id  UUID REFERENCES staff(id)
);

-- Fraud flags
CREATE TABLE doc_fraud_flags (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id     UUID NOT NULL REFERENCES documents(id),
  flag_type       TEXT NOT NULL,      -- aadhaar_format, dob_mismatch, duplicate_aadhaar, photo_mismatch, exif_suspicious
  severity        TEXT NOT NULL,      -- info, warning, error
  details         JSONB,              -- flag-specific context
  raised_at       TIMESTAMPTZ DEFAULT now(),
  resolved        BOOLEAN DEFAULT FALSE,
  resolved_by_id  UUID REFERENCES staff(id),
  resolved_at     TIMESTAMPTZ,
  resolution_note TEXT
);

-- Document requests
CREATE TABLE doc_requests (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  doc_type        TEXT NOT NULL,
  requested_by_id UUID NOT NULL REFERENCES staff(id),
  target_scope    TEXT NOT NULL,      -- individual / class / batch / all_staff
  target_ids      UUID[],             -- specific entity IDs; null = scope-wide
  message         TEXT,
  deadline        DATE NOT NULL,
  status          TEXT DEFAULT 'ACTIVE',  -- ACTIVE / CLOSED / CANCELLED
  created_at      TIMESTAMPTZ DEFAULT now()
);

CREATE TABLE doc_request_items (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id      UUID NOT NULL REFERENCES doc_requests(id),
  entity_id       UUID NOT NULL,
  entity_type     TEXT NOT NULL,
  status          TEXT DEFAULT 'PENDING',  -- PENDING / UPLOADED / VERIFIED / OVERDUE
  document_id     UUID REFERENCES documents(id),
  reminded_count  INT DEFAULT 0,
  last_reminded_at TIMESTAMPTZ
);

-- Compliance export jobs
CREATE TABLE compliance_export_jobs (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  export_type     TEXT NOT NULL,      -- CBSE_AFFILIATION / NAAC / NIRF / AISHE / AICTE / LEGAL
  parameters      JSONB,
  status          TEXT DEFAULT 'QUEUED',
  zip_r2_path     TEXT,
  zip_expires_at  TIMESTAMPTZ,
  missing_docs    JSONB,              -- list of doc types not found
  initiated_by_id UUID REFERENCES staff(id),
  created_at      TIMESTAMPTZ DEFAULT now(),
  completed_at    TIMESTAMPTZ
);

-- Document access audit log
CREATE TABLE doc_access_log (
  id            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  document_id   UUID NOT NULL REFERENCES documents(id),
  accessed_by_id UUID REFERENCES users(id),
  access_type   TEXT NOT NULL,      -- VIEW / DOWNLOAD / VERIFY / REJECT / SHARE / REDACT
  accessed_at   TIMESTAMPTZ DEFAULT now(),
  ip_address    INET,
  user_agent    TEXT,
  purpose       TEXT                -- scholarship / verification / compliance-export / court
);

-- Legal holds
CREATE TABLE doc_legal_holds (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id       UUID NOT NULL REFERENCES tenants(id),
  entity_type     TEXT,             -- null = institution-wide hold
  entity_id       UUID,
  hold_reason     TEXT NOT NULL,
  placed_by_id    UUID NOT NULL REFERENCES users(id),
  placed_at       TIMESTAMPTZ DEFAULT now(),
  lifted_by_id    UUID REFERENCES users(id),
  lifted_at       TIMESTAMPTZ,
  lift_reason     TEXT
);
```

---

## 14. API Reference

### 14.1 Upload & Management

```
POST   /api/v1/documents/upload/                    # Upload document (multipart)
GET    /api/v1/documents/{id}/                      # Document metadata
GET    /api/v1/documents/{id}/view-url/             # Pre-signed view URL
GET    /api/v1/documents/{id}/download-url/         # Pre-signed download URL
DELETE /api/v1/documents/{id}/                      # Delete (subject to retention)
GET    /api/v1/documents/{id}/versions/             # Version history
POST   /api/v1/documents/{id}/restore/{version}/    # Restore previous version
```

### 14.2 Verification

```
PATCH  /api/v1/documents/{id}/verify/               # Verify document
PATCH  /api/v1/documents/{id}/reject/               # Reject with reason
GET    /api/v1/documents/verification-queue/        # Pending verification queue
POST   /api/v1/documents/bulk-verify/               # Bulk verify session submit
GET    /api/v1/documents/{id}/fraud-flags/          # Fraud flags for document
PATCH  /api/v1/documents/{id}/fraud-flags/{flag_id}/resolve/  # Resolve flag
```

### 14.3 Search & Listing

```
GET    /api/v1/documents/search/?q=&doc_type=&status=&entity_id=   # Search
GET    /api/v1/documents/expiry-dashboard/?days=90                 # Expiry view
GET    /api/v1/documents/completeness/?class_id=&doc_type=         # Completeness report
POST   /api/v1/documents/bulk-download/                            # ZIP job creation
GET    /api/v1/documents/bulk-download/{job_id}/url/               # ZIP URL
```

### 14.4 Compliance Export

```
POST   /api/v1/compliance-export/                  # Start export job
GET    /api/v1/compliance-export/{job_id}/         # Job status
GET    /api/v1/compliance-export/{job_id}/download-url/  # ZIP URL
```

### 14.5 Document Requests

```
POST   /api/v1/doc-requests/                       # Send request
GET    /api/v1/doc-requests/{id}/progress/         # Completion tracking
PATCH  /api/v1/doc-requests/{id}/close/            # Close request
GET    /api/v1/doc-requests/my-pending/            # Student/staff pending requests
```

---

## 15. Analytics & Reports

### 15.1 Document Operations Dashboard

```
┌──────────────────────────────────────────────────────┐
│  Document Management — Academic Year 2025-26         │
├─────────────────────┬────────┬──────────┬────────────┤
│  Category           │ Total  │ Verified │ Pending    │
├─────────────────────┼────────┼──────────┼────────────┤
│  Student Documents  │ 12,480 │  11,920  │  560 (4%)  │
│  Staff Documents    │  1,840 │   1,760  │   80 (4%)  │
│  Institution Docs   │    120 │     112  │    8 (7%)  │
└─────────────────────┴────────┴──────────┴────────────┘
```

### 15.2 Key Metrics Tracked

| Metric | Target |
|---|---|
| Student document completeness (required set) | ≥ 95% |
| Verification turnaround time | < 2 working days |
| Fraud flag false-positive rate | < 10% (calibration) |
| OCR confidence (average) | ≥ 85% |
| Expiry documents with 30-day warning coverage | 100% |
| Compliance package generation time | < 3 minutes |

### 15.3 Rejection Rate by Document Type

High rejection rates for a specific document type indicate:
- Unclear instructions to students/staff on what to upload
- Common fraud attempt (auto-generated documents)
- Outdated templates being submitted (e.g., old income cert format)

Report used to improve upload guidance and fraud detection rule calibration.

### 15.4 Storage & Cost Report

```
Monthly Document Storage Cost
  R2 Storage (12,440 documents, avg 1.2 MB)  : ₹  180
  Lambda (OCR trigger, thumbnail gen)         : ₹   34
  AWS Textract (OCR calls)                    : ₹  210
  AWS Rekognition (photo match, if enabled)   : ₹   88
  ─────────────────────────────────────────────────────
  Total                                       : ₹  512
  Per-document cost                           : ₹ 0.04
```

---

## 16. DPDPA 2023 Compliance

### 16.1 Consent & Purpose Limitation

At admission, student/parent consents to document storage for:
- Enrollment verification
- Scholarship processing
- Compliance and accreditation
- Emergency medical (blood group, vaccination)

Caste certificate is accessible ONLY to roles with `scholarship_processing` or `rte_admission` permissions — not to class teachers or transport staff.

### 16.2 Retention Schedule

| Document Category | Retention Period | Post-Retention Action |
|---|---|---|
| Student enrollment docs | 5 years after leaving (10 in some states) | Anonymise → delete from R2 |
| Staff employment docs | 7 years after leaving | Anonymise → delete |
| Staff qualification certs | 7 years after leaving | Delete |
| Institution compliance docs | Permanent | Archive to cold storage tier |
| Medical fitness certs | 7 years (NMC for medical colleges) | Delete |
| Document access logs | 3 years | Delete IP; retain access type + cert_id |

### 16.3 Right to Erasure

Student submits erasure request:
1. System identifies all documents for the student
2. Legally exempt documents (TC received, enrollment record) — flagged as non-erasable with legal basis
3. Non-exempt documents scheduled for deletion within 30 days
4. Erasure confirmation email sent to student
5. Erasure event logged with document IDs (for audit, without PII)

### 16.4 Third-Party Sub-Processors

| Sub-processor | Purpose | Data Shared | DPA |
|---|---|---|---|
| AWS Textract | OCR on document images | Document images | AWS DPA (stored in institutional docs) |
| AWS Rekognition | Photo face match | Face images | AWS DPA |
| Cloudflare R2 | Document storage | Encrypted document bytes | Cloudflare DPA |

DPDPA Section 16: cross-border data transfer notice (AWS Textract may process in non-India regions) disclosed in privacy policy and informed to users at consent collection.

### 16.5 Data Minimization Enforcement

The document type registry controls which documents can be requested for which entity types and purposes. Admin cannot add arbitrary document types through the UI — additions require Super Admin approval with stated purpose. This prevents institutions from over-collecting PII under the guise of "document management."

---

## 17. Cross-Module Integration Map

| Module | Integration |
|---|---|
| Module 04 — Institution Onboarding | Institution document types configured at setup; compliance doc requirements seeded per institution type |
| Module 07 — Student Enrolment | Required documents list for admission; enrollment blocked if mandatory docs not verified |
| Module 08 — Staff Management & BGV | Staff qualification and BGV documents stored here; Module 08 reads verification status |
| Module 19 — Exam Proctoring | Admit card photo sourced from document store (PHOTOGRAPH type) |
| Module 24 — Fee Structure | Scholarship income cert gate — fee concession unlocked only when income cert is VERIFIED |
| Module 28 — Hostel | Medical fitness cert gate for hostel check-in; vaccination record check |
| Module 29 — Transport | Driver license and vehicle permit documents stored here; expiry tracked |
| Module 30 — Library | INFLIBNET N-LIST subscription document stored as institutional doc |
| Module 32 — Student Welfare | UDID certificate for CWSN — Module 32 reads verification status for IEP |
| Module 35 — Notifications | Push notifications for verification status changes, expiry alerts, document requests |
| Module 36 — WhatsApp | Document request messages; expiry alerts via WhatsApp |
| Module 37 — Email | Verification status emails; compliance package download links |
| Module 38 — SMS | Document request SMS; expiry reminder SMS |
| Module 39 — Certificates | Received TC stored here; DigiLocker-pulled documents stored here |
| Module 42 — DPDPA & Audit Log | All document access events, fraud flags, legal holds, erasure requests logged |

---

*Module 40 — Document Management — EduForge Platform Specification*
*Version 1.0 | 2026-03-26*
