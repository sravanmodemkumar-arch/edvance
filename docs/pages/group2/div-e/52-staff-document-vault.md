# 52 — Staff Document Vault

- **URL:** `/group/hr/documents/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Document Vault is the secure, centralised repository for all official documents belonging to staff members across the group. Every staff member's employment documentation is maintained here, ensuring that Group HR has verified, accessible copies of all required documents regardless of which branch the staff member is posted at. This eliminates the fragmented, branch-specific paper filing systems that create compliance gaps during audits.

The mandatory document set for each staff member includes: Aadhaar Card (government identity proof), PAN Card (tax identity), Degree Certificates for all academic qualifications claimed, Experience Letters from all prior employers (cross-referenced against the BGV process), Police Verification Certificate (mandatory for staff working with children — POCSO regulatory requirement), POCSO Training Certificate (current valid certificate from approved training provider), Passport-sized Photograph, Bank Account Proof (cancelled cheque or bank passbook copy), PF Nomination and Declaration Form (EPFO compliance), ESI Registration document (applicable for eligible staff), Signed Employment Contract (including role, grade, salary, and posting details), and Medical Fitness Certificate (from a registered medical officer — required for all new joiners).

Documents are stored in Cloudflare R2 object storage — not in the application database. The database stores document metadata only: file name, upload date, uploader, verifier, verification status, and the R2 object key. When a user requests to view a document, the API generates a time-limited signed URL (valid for 15 minutes) that grants direct browser access to the file in R2. This design ensures that document access is auditable, that links cannot be shared indefinitely, and that file storage costs do not burden the relational database.

Documents have a lifecycle: Pending Verification (uploaded but not yet reviewed by HR), Verified (HR has confirmed authenticity), Rejected (HR has found the document unacceptable — wrong document, poor quality, suspected forgery), and Re-Requested (rejected and staff has been asked to resubmit). Documents with an expiry date (certificates, police verification) are monitored for upcoming expiry — the system alerts HR 90 days before expiry and 30 days before. Missing critical documents (Aadhaar, Degree Certificate, Signed Contract) trigger an automated alert on the staff member's record and on this page's KPI bar.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Manager | G3 | Full access — view, upload, verify, re-request | Primary operator |
| Group HR Director | G3 | Full access — all actions + bulk export | Oversight |
| Group BGV Manager | G3 | Read-only — specific document types (Experience Letters, Police Verification) | BGV coordination |
| Group POCSO Coordinator | G3 | Read-only — POCSO Training Certificates only | Compliance verification |
| Branch Principal | G3 | Read-only — own branch staff documents (metadata only, not file content) | Cannot view actual files |
| All other roles | — | No access | Page not rendered |

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Portal › HR & Staff › Staff Document Vault
```

### 3.2 Page Header

- **Title:** Staff Document Vault
- **Subtitle:** Centralised secure document repository — Cloudflare R2 storage, signed URL access
- **Primary CTA:** `Upload Document` (for specific staff member — HR Manager / Director)
- **Secondary CTA:** `Export Document Status Report` (CSV — staff document completion report)
- **Header badge:** Count of staff with missing critical documents shown in red

### 3.3 Alert Banner (conditional)

- **Red:** `[N] staff members are missing critical documents (Aadhaar / Degree / Contract). Immediate action required.` Action: `View List`
- **Amber:** `[N] documents expire within 90 days. Collect renewed documents before expiry.` Action: `View Expiring`
- **Amber:** `[N] documents are pending HR verification.` Action: `Review Pending`
- **Blue:** `[N] re-requested documents have not been resubmitted by staff for > 14 days.`
- **Green:** All staff documents complete and verified — shown when no active alerts

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Staff with All Documents Complete | Count where all mandatory documents are Verified and not expired | Green always | Filter table to complete staff |
| Staff with Missing Critical Docs | Count where Aadhaar OR Degree OR Contract is missing or Rejected | Red if > 0, else grey | Filter to incomplete staff |
| Documents Pending HR Verification | Count of documents with status = Pending Verification | Amber if > 0, else grey | Filter to pending verification |
| Documents Expiring in 90 Days | Count of documents with expiry_date within 90 days | Amber if > 0, else grey | Filter to expiring docs |
| Total Documents Stored | Total count of all document records across all staff | Blue always | No drill-down |
| Re-Requests Outstanding | Count of documents in Re-Requested status with no new upload > 14 days | Amber if > 0, else grey | Filter to outstanding re-requests |

---

## 5. Main Table — Staff Document Status Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link — opens document checklist drawer) | Yes (A–Z) | Yes — text search |
| Branch | Text | Yes | Yes — dropdown |
| Role | Text | Yes | Yes — dropdown |
| Docs Submitted / Total | Progress indicator (e.g., "10/12") | Yes | Yes — completion range |
| Missing Critical Docs | Badge: None (green) / [N] Missing (red) | No | Yes — toggle |
| Verification Status | Badge: All Verified / Pending Verification / Has Rejected | No | Yes — dropdown |
| Last Updated | Date (most recent document upload or verification action) | Yes | Yes — date range |
| Documents Expiring Soon | Badge: None / [N] Expiring (amber) | No | Yes — expiring toggle |
| Actions | Icon buttons: View Checklist / Upload Document / Re-Request Document | No | No |

### 5.1 Filters

- **Branch:** Multi-select dropdown
- **Role Category:** Teaching / Non-Teaching / All
- **Document Completion:** All Documents Complete / Missing Critical / Missing Non-Critical / All
- **Verification Status:** All Verified / Has Pending / Has Rejected / All
- **Expiring in 90 Days:** Toggle — Yes / All
- **Re-Request Outstanding:** Toggle — Yes / All
- **Reset Filters** button

### 5.2 Search

Text search on Staff Name. Min 2 characters, 400 ms debounce.

### 5.3 Pagination

Server-side. Default 20 rows per page. Options: 10 / 20 / 50. "Showing X–Y of Z staff members."

---

## 6. Drawers

### 6.1 View Staff Document Checklist

Triggered by clicking staff name or View Checklist action. Wide drawer.

**Displays:**
- Staff profile header: Name, photo thumbnail, branch, designation, employee ID
- Document checklist table:
  | Document Type | Required | Upload Date | Uploaded By | Verification Status | Verified By | Expiry Date | Actions |
- Each row has: View (opens signed URL in new tab), Verify, Reject, Re-Request buttons (role-dependent)
- Missing mandatory documents shown with red "Not Uploaded" badge
- Expired documents shown with red "Expired" badge
- Upload history for re-submitted documents (collapsible version history per document type)

### 6.2 Upload Document

Triggered by Upload Document action or from within the checklist drawer.

**Fields:**
- Staff Name (searchable dropdown, or auto-filled from context)
- Branch (auto-filled)
- Document Type (dropdown — all 12 mandatory document types + "Other" for optional)
- File Upload (PDF or image — JPEG/PNG; max 10 MB per file)
- Issue Date (date picker — date on the document)
- Expiry Date (date picker — required for certificates and police verification; optional for others)
- Uploaded By (auto-filled: current user)
- Remarks (textarea, optional)

**Validation:** File type must be PDF, JPEG, or PNG. Max size 10 MB. Expiry date must be > issue date if provided.

**Backend:** On submit → API generates pre-signed PUT URL for R2 → Frontend uploads file directly to R2 → On success, API stores metadata in database.

**Submit:** `Upload` → POST `/api/hr/documents/upload-intent/` (gets signed upload URL) → Direct upload to R2 → POST `/api/hr/documents/confirm/` (confirms upload and stores metadata)

### 6.3 Verify Document

Triggered from checklist. Single-action drawer.

**Fields:**
- Document ID (locked)
- Document Type (locked)
- Staff Name (locked)
- Document preview: rendered thumbnail or "View Document" button (opens signed URL)
- Verification Decision (radio: Verified / Rejected)
- If Rejected → Rejection Reason (dropdown: Wrong Document / Poor Quality / Suspected Forgery / Expired / Name Mismatch / Other) + Notes (textarea, required)
- Verified By (auto-filled: current user)
- Verification Date (auto-set to today)

**Submit:** `Confirm Verification` → PATCH `/api/hr/documents/{id}/verify/`

### 6.4 Re-Request Document

**Fields:**
- Staff Name (locked)
- Document Type (locked)
- Re-Request Reason (dropdown mirrors rejection reasons)
- Message to Staff (textarea — this message is sent as an in-app notification and logged on the document record)
- Deadline for Resubmission (date picker, defaults to 14 days from today)
- Notify Branch Principal: checkbox (default checked)

**Submit:** `Send Re-Request` → POST `/api/hr/documents/{id}/re-request/`

---

## 7. Charts

No dedicated charts on this page. Document compliance statistics are visible on the HR Analytics Dashboard (page 47) and HR Manager Dashboard (page 02).

---

## 8. Toast Messages

| Trigger | Type | Message |
|---|---|---|
| Document uploaded | Success | "[Document Type] uploaded for [Staff Name]. Pending HR verification." |
| Document verified | Success | "[Document Type] for [Staff Name] verified." |
| Document rejected | Warning | "[Document Type] for [Staff Name] rejected. Reason: [reason]." |
| Re-request sent | Info | "Re-request sent to [Staff Name] for [Document Type]. Deadline: [date]." |
| Signed URL generated | Info | "Document link generated. Link expires in 15 minutes." |
| Upload file size error | Error | "File exceeds 10 MB limit. Please upload a smaller file." |
| File type error | Error | "Only PDF, JPEG, and PNG files are accepted." |
| Server error | Error | "Failed to process document. Please retry or contact support." |

---

## 9. Empty States

**No staff in table:**
> Icon: folder with person
> "No staff records found."
> "Staff appear here once they are added to the Staff Directory."

**Staff has no documents uploaded:**
> "No documents uploaded for [Staff Name] yet."
> "Use 'Upload Document' to begin collecting this staff member's documents."
> CTA: `Upload Document`

**Filtered results return nothing:**
> Icon: magnifying glass
> "No staff match your current filters."
> CTA: `Reset Filters`

---

## 10. Loader States

- Page load: Skeleton KPI cards + skeleton table rows
- Checklist drawer open: Spinner while document metadata loads for staff member
- Document view (signed URL generation): Loading spinner on "View Document" button (2–4 seconds for URL generation)
- Upload progress: Progress bar showing file upload to R2 (percentage complete)
- Verification action: Inline spinner on Verify/Reject buttons during PATCH request

---

## 11. Role-Based UI Visibility

| UI Element | HR Manager | HR Director | BGV Manager | POCSO Coordinator | Branch Principal |
|---|---|---|---|---|---|
| Upload Document action | Visible | Visible | Hidden | Hidden | Hidden |
| Verify / Reject actions | Visible | Visible | Hidden | Hidden | Hidden |
| Re-Request action | Visible | Visible | Hidden | Hidden | Hidden |
| View Document (signed URL) | Visible | Visible | Visible (specific types) | Visible (POCSO cert) | Hidden |
| Export Document Status | Visible | Visible | Hidden | Hidden | Hidden |
| All branches in table | Yes | Yes | Yes (read-only) | Yes (read-only) | Own branch only (metadata only) |
| Delete document | Hidden | Hidden | Hidden | Hidden | Hidden — no deletion |

---

## 12. API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/hr/documents/` | Paginated staff document status list |
| GET | `/api/hr/documents/{staff_id}/checklist/` | Full document checklist for one staff member |
| POST | `/api/hr/documents/upload-intent/` | Get pre-signed R2 PUT URL for upload |
| POST | `/api/hr/documents/confirm/` | Confirm upload and store metadata |
| PATCH | `/api/hr/documents/{id}/verify/` | Verify or reject a document |
| POST | `/api/hr/documents/{id}/re-request/` | Create re-request for document |
| GET | `/api/hr/documents/{id}/signed-url/` | Generate 15-minute signed GET URL |
| GET | `/api/hr/documents/kpis/` | KPI summary bar data |
| GET | `/api/hr/documents/export/` | Export document completion status CSV |

---

## 13. HTMX Patterns

| Interaction | HTMX Attribute | Behaviour |
|---|---|---|
| Table load | `hx-get` on page render | Fetches staff document status list |
| Filter/search change | `hx-get` + `hx-include` | Re-fetches filtered table |
| Pagination | `hx-get` on page buttons | Fetches page N |
| Checklist drawer open | `hx-get` + `hx-target="#drawer"` | Loads staff checklist detail |
| Upload intent | `hx-post` + `hx-target="#upload-status"` | Gets signed URL; JS handles R2 upload |
| Upload confirm | `hx-post` on confirm step + `hx-target="#checklist-table"` | Refreshes checklist after confirmed upload |
| Verify/Reject form | `hx-patch` + `hx-target="#doc-row-{id}"` | Updates document row verification status |
| Re-request form | `hx-post` + `hx-target="#doc-row-{id}"` | Updates document status to Re-Requested |
| KPI bar refresh | `hx-get` on `#kpi-bar` after any upload or verification | Reloads KPI counts |
| Toast | `hx-swap-oob` on `#toast-container` | Out-of-band toast injection |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
