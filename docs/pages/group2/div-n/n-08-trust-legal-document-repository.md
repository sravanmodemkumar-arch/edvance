# [08] — Trust & Legal Document Repository

> **URL:** `/group/legal/documents/`
> **File:** `n-08-trust-legal-document-repository.md`
> **Template:** `portal_base.html` (light theme — restricted)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — secure vault for trust deeds, land documents, NOCs, 12A/80G certificates

---

## 1. Purpose

The Trust & Legal Document Repository is a centralised, encrypted document vault for all foundational and statutory legal documents of the Institution Group. These documents are the legal bedrock of the organisation: the Trust Deed establishes the group's legal existence; the Society Registration Certificate and 12A/80G certificates underpin tax exemptions; land documents (sale deeds, lease agreements) establish property rights for campuses; and NOCs (No Objection Certificates) from state authorities are prerequisites for CBSE affiliation.

Unlike operational documents (contracts, RTI responses), these are foundational documents that are infrequently accessed but must be preserved with complete version history, access audit logging, and tamper-evident storage. Loss or inaccessibility of a Trust Deed during a regulatory inspection or court proceeding can be catastrophic.

All documents are encrypted at rest using AES-256. Every download is logged immutably. Documents are stored in Cloudflare R2 with India data residency. The repository also stores document expiry data (for documents requiring periodic renewal like 12A/80G) and sends alerts before expiry.

Scale: 1 Trust entity + 5–50 branch locations · 20–200 foundational documents · Infrequently accessed but high-stakes

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Holds physical originals; provides certified copies externally |
| Group Compliance Manager | 109 | G1 | Read — Full Repository | Primary user; views, downloads, tracks expiry |
| Group RTI Officer | 110 | G1 | Read — Limited | Access only to documents relevant to RTI disclosures |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | References documents for filings externally |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant |
| Group Contract Administrator | 127 | G3 | Upload + Manage — All Categories | Uploads new documents, updates versions, records expiry |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Documents relevant to disputes | Views land, trust deed if a dispute relates to them |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,110,127,128], min_level=G1)`. G5 (Chairman) has full access. G4 (CEO) has read access.
>
> **Security:** All downloads logged in `legal_doc_access_log`. Failed access attempts alerted to G5.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Trust & Legal Document Repository
```

### 3.2 Page Header
```
Trust & Legal Document Repository              [Upload Document]  [Export Index ↓]
Group Contract Administrator — [Name]  |  Compliance Manager — [Name]
[Group Name] · [N] Documents · [N] Expiring (90d) · Last updated: [datetime]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| 12A/80G certificate expiry within 90 days | "12A / 80G Certificate expiring in [N] days. File renewal application with Income Tax dept immediately." | Critical (red) |
| Society Registration renewal due | "Society Registration renewal due in [N] days at [State] Registrar." | High (amber) |
| FCRA Registration lapsing | "FCRA Registration valid until [date] — [N] days remaining. Renew to continue receiving foreign funds." | High (amber) |
| Any document with no expiry date set (requires review) | "[N] document(s) have no expiry date set. Review to confirm renewal requirements." | Medium (yellow) |
| Trust Deed not uploaded | "Trust Deed document is not uploaded. This is a critical legal document — upload required." | Critical (red) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Documents | Count | COUNT all documents with status != 'archived' | Blue | `#kpi-total-docs` |
| 2 | Expiring (90 Days) | Count | COUNT WHERE expiry_date BETWEEN TODAY AND TODAY+90 | Red > 3, Amber 1–3, Green = 0 | `#kpi-expiring-90` |
| 3 | Expired | Count | COUNT WHERE expiry_date < TODAY AND status = 'active' | Red if > 0, Green = 0 | `#kpi-expired` |
| 4 | Documents — Latest Version | Count | COUNT WHERE is_latest_version = True AND verified = True | Green if = total; Amber if some unverified | `#kpi-verified` |
| 5 | Awaiting Upload | Count | COUNT required_document_types WHERE no document uploaded | Red > 0, Green = 0 | `#kpi-awaiting` |
| 6 | Last 30 Days Downloads | Count | COUNT document_access_log WHERE action='download' AND date >= TODAY-30 | Blue (audit metric) | `#kpi-downloads` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/documents/kpis/"` with `hx-trigger="load"`.

---

## 5. Sections

### 5.1 Document Repository (Main Table)

All legal documents, filterable by category and branch.

**Search:** Document name, category, branch name. Debounced 350ms.

**Filters:**
- Category: `All` · `Trust Deed` · `Society Registration` · `12A / 80G` · `FCRA` · `Land Documents` · `NOC` · `Essentiality Certificate` · `CBSE Docs` · `Court Orders` · `Other`
- Branch / Entity Level: `Group Level` + all branches
- Status: `Active` · `Expiring Soon` · `Expired` · `Archived`
- Has Expiry: `Yes` · `No`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | |
| Document Name | Text | Yes | Descriptive name e.g. "Trust Deed — Original 1994" |
| Category | Badge | Yes | Colour-coded by category |
| Entity / Branch | Text | Yes | Group Level or specific branch/campus |
| Version | Text | Yes | e.g., v1.0, v2.1 |
| Issue Date | Date | Yes | Date document was issued / executed |
| Expiry Date | Date | Yes | Red if < 30d, amber if < 90d; "N/A" if perpetual |
| Status | Badge | Yes | Active / Expiring / Expired / Archived |
| Verified | Badge | Yes | Verified ✅ / Pending Verification ⚠️ |
| Last Downloaded | Date | No | Date of most recent download (audit) |
| Actions | Buttons | No | [View] · [Download] · [Upload Version] (Role 127) |

**Default sort:** Expiry Date ASC (most urgent first), then Document Name
**Pagination:** Server-side · Default 25/page

---

### 5.2 Required Documents Checklist

A checklist of all required foundational documents with upload status. Helps identify gaps.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Document Type | Text | e.g., "Trust Deed", "12A Certificate", "PAN Card — Trust" |
| Required For | Text | "All groups" or "College branches only" |
| Status | Badge | Uploaded ✅ / Missing ❌ / Expired ⚠️ |
| Last Upload Date | Date | Date most recent version was uploaded |
| Actions | Button | [Upload] if missing (Role 127) · [View] if uploaded |

---

## 6. Drawers & Modals

### 6.1 Drawer: `document-detail` (680px, right-slide)
- **Tabs:** Overview · Document · Version History · Access Log
- **Overview tab:**
  - Document Name, Category, Entity/Branch, Description
  - Issue Date, Issuing Authority, Document Reference Number
  - Expiry Date, Renewal Alert Lead Time (e.g., "Alert 90 days before expiry")
  - Status badge, Verified badge, Uploaded By, Upload Date
  - Notes (editable by Role 127 only)
- **Document tab:** PDF viewer (embedded or inline preview) + [Download] button (audited)
- **Version History tab:** All uploaded versions — version label, upload date, uploaded by, file size, [Download Previous Version] (Role 127, G4+ only)
- **Access Log tab (Role 127, G4, G5 only):** Immutable log of all accesses — date/time, user, action (viewed/downloaded)

### 6.2 Modal: `upload-document` (620px)
Used by Contract Administrator to upload a new document or new version.

| Field | Type | Required | Validation |
|---|---|---|---|
| Document Name | Text | Yes | Min 10 chars; descriptive |
| Category | Select | Yes | |
| Entity / Branch | Select | Yes | Group Level or specific branch |
| Document Date | Date picker | Yes | Issue / execution date |
| Version Label | Text | No | e.g., "v1.0" or "Amendment 2024" |
| Has Expiry | Toggle | Yes | |
| Expiry Date | Date picker | Conditional | Required if Has Expiry = Yes |
| Renewal Alert Lead Time | Select | Conditional | 30 / 60 / 90 / 180 days before expiry |
| Document File | File upload | Yes | PDF only, max 50MB |
| Issuing Authority | Text | No | |
| Reference / Registration Number | Text | No | |
| Notes | Textarea | No | |
| Verified | Toggle | No | Mark if document is verified original/certified copy |

**Footer:** Cancel · Upload Document
**On success:** Document appears in table; if category = Trust Deed and no previous Trust Deed existed, alert to G5.

### 6.3 Modal: `export-index` (480px)
Exports a document index (not the documents themselves) as PDF/Excel — listing all docs with metadata.
- **Fields:** Category filter, Branch filter, Include expired toggle, Format
- **Buttons:** Cancel · Export Index

---

## 7. Charts

### 7.1 Documents by Category (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Documents by Category" |
| Data | Count per document category |
| Colour | Each category distinct |
| Tooltip | "[Category]: [N] documents" |
| API endpoint | `GET /api/v1/group/{id}/legal/documents/by-category/` |
| HTMX | `hx-get` on load → `hx-target="#chart-docs-by-category"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Document uploaded | "Document '[Name]' uploaded successfully." | Success | 4s |
| Document downloaded | "Downloading '[Name]'… (access logged)" | Info | 3s |
| New version uploaded | "New version uploaded for '[Name]'. Previous version archived." | Success | 4s |
| Expiry alert | "'[Document]' expires in [N] days. Initiate renewal." | Warning | 6s |
| Export index triggered | "Generating document index export…" | Info | 3s |
| Validation error | "Please complete all required fields." | Error | 4s |
| Upload error | "Upload failed. File must be PDF, max 50MB." | Error | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| Repository empty | `folder` | "Repository Empty" | "No legal documents uploaded yet. Start by uploading the Trust Deed." | Upload Document (Role 127) |
| Category filter returns no docs | `search` | "No Documents in This Category" | "No documents of type [Category] have been uploaded." | Upload Document (Role 127) |
| All documents current | `check-circle` | "All Documents Current" | "No documents are expiring or overdue for renewal." | View Full Repository |
| Required checklist all green | `shield-check` | "All Required Documents On File" | "Every required foundational document has been uploaded." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI cards + 8-row table skeleton |
| Table filter/search | Spinner overlay + rows dimmed |
| Chart load | Grey canvas + centred spinner |
| Drawer open | Right-slide skeleton |
| Document upload | Progress bar in modal (0–100%) |
| Document download (large file) | Button spinner while preparing download |
| Access log tab | Shimmer rows while loading audit data |

---

## 11. Role-Based UI Visibility

| Element | Contract Admin (127, G3) | Compliance Mgr (109, G1) | RTI Officer (110, G1) | Legal Dispute (128, G1) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| Full document table | Visible | Visible | RTI-relevant only | Dispute-relevant only | Visible |
| Required checklist | Visible | Visible | Not visible | Not visible | Visible |
| [Upload Document] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Upload Version] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Download] button | Visible (audited) | Visible (audited) | Visible (audited) | Visible (audited) | Visible (audited) |
| Version History tab | Full (can download old) | Read-only (no old download) | Not visible | Not visible | Full |
| Access Log tab | Not visible | Not visible | Not visible | Not visible | Visible (G4/G5 only) |
| Charts | Visible | Visible | Not visible | Not visible | Visible |
| Export index | Visible | Visible | Not visible | Not visible | Visible |
| Alert banners | All | All | Not visible | Land/Trust only | All |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/documents/` | G1+ | Paginated document list |
| POST | `/api/v1/group/{id}/legal/documents/` | Role 127, G4+ | Upload new document |
| GET | `/api/v1/group/{id}/legal/documents/{doc_id}/` | G1+ | Document detail |
| POST | `/api/v1/group/{id}/legal/documents/{doc_id}/version/` | Role 127, G4+ | Upload new version |
| GET | `/api/v1/group/{id}/legal/documents/{doc_id}/download/` | G1+ (audited) | Secure download URL (pre-signed R2) |
| GET | `/api/v1/group/{id}/legal/documents/kpis/` | G1+ | KPI summary |
| GET | `/api/v1/group/{id}/legal/documents/checklist/` | G1+ | Required documents checklist |
| GET | `/api/v1/group/{id}/legal/documents/by-category/` | G1+ | Category donut chart data |
| GET | `/api/v1/group/{id}/legal/documents/{doc_id}/access-log/` | G4+ | Immutable access audit log |
| POST | `/api/v1/group/{id}/legal/documents/export-index/` | G1+ | Export document index |

### Query Parameters for Document List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: document name, category |
| `category` | string | trust_deed / society_reg / 12a_80g / fcra / land / noc / essentiality / cbse / court_order / other |
| `entity` | string | group / branch_{id} |
| `status` | string | active / expiring / expired / archived |
| `has_expiry` | boolean | true / false |
| `expiry_within_days` | integer | Documents expiring within N days |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50; default 25 |
| `sort` | string | expiry_date / document_name / category / issue_date |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | GET `.../documents/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Table load | `<tbody id="docs-table-body">` | GET `.../documents/` | `#docs-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET `.../documents/?q={v}` | `#docs-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Category filter | Category chips | GET `.../documents/?category={v}` | `#docs-table-body` | `innerHTML` | `hx-trigger="click"` |
| Status filter | Status chips | GET `.../documents/?status={v}` | `#docs-table-body` | `innerHTML` | `hx-trigger="click"` |
| Open drawer | [View] / row click | GET `.../documents/{doc_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Upload modal | [Upload Document] | GET `/htmx/legal/documents/upload-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Checklist load | `<div id="required-checklist">` | GET `.../documents/checklist/` | `#required-checklist` | `innerHTML` | `hx-trigger="load"` |
| Chart load | Chart container | GET `.../documents/by-category/` | `#chart-docs-by-category` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET `.../documents/?page={n}` | `#docs-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
