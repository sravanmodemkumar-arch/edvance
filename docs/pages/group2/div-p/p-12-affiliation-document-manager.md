# P-12 — Affiliation Document Manager

> **URL:** `/group/audit/affiliation/documents/`
> **File:** `p-12-affiliation-document-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Affiliation Compliance Officer (Role 125, G1) — primary operator

---

## 1. Purpose

The Affiliation Document Manager is the centralised document vault for every paper, certificate, NOC, and proof required for board affiliation across all branches of the Institution Group. In Indian education, affiliation is a document-intensive process — CBSE alone requires 25–40 distinct documents per school for initial affiliation and renewal. Losing a single document — a fire safety NOC that expired, a building stability certificate that wasn't digitised, a teacher qualification certificate that the branch "had somewhere" — can delay affiliation renewal by 6–12 months and put 500–3,000 students' board exam eligibility at risk.

The problems this page solves:

1. **Document scatter:** In a 30-branch group, affiliation documents live in physical files at the branch principal's office, scanned PDFs on someone's laptop, WhatsApp forwards between the admin and the compliance officer, and sometimes in a shared Google Drive that nobody remembers the password to. When CBSE inspection happens and the inspector asks for the building stability certificate, the principal scrambles for 45 minutes while the inspector waits. This page creates a single, searchable, branch-wise document repository with every required document catalogued.

2. **Expiry management:** Many affiliation documents have expiry dates — fire safety NOC (1 year), building stability certificate (5 years), FSSAI licence for school canteen (5 years), pollution control board certificate (varies), trade licence (annual), society registration renewal (5 years). A 30-branch group is tracking 200–400 expiring documents. Without automated alerts, expired documents are discovered only when the CBSE inspector points them out — which means affiliation is at risk.

3. **Document completeness gap:** CBSE requires specific documents: school recognition order from state government, NOC from state education department, land document (sale deed/lease deed for ≥ 30 years), building completion certificate, fire safety NOC from Chief Fire Officer, water and sanitation certificate, building stability certificate from empanelled structural engineer, audited accounts (3 years), fee structure approved by Fee Regulatory Committee (in applicable states), teacher qualification certificates for every teacher, and more. Each branch must have 100% of these documents on file. The document manager shows per-branch completeness percentage and highlights exact gaps.

4. **Version control:** Documents get renewed — a new fire NOC replaces the old one, a new building stability certificate supersedes the previous. Branches sometimes upload the wrong version, or the old expired version is still showing as "current." The manager maintains version history, marks the active version, archives previous versions, and prevents duplicate uploads of the same document.

5. **Inspection readiness:** When a CBSE/State Board inspection team visits, they ask for documents in a specific order per their checklist. The "Inspection Pack" feature generates a pre-ordered document bundle (PDF or ZIP) matching the board's inspection checklist sequence — so the principal can hand over a complete, organised pack in minutes, not hours.

**Scale:** 5–50 branches · 25–40 document types per board · 3–5 board types · 200–500 total documents under active management · 50–100 expiring annually · 100–300 document uploads per year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Affiliation Compliance Officer | 125 | G1 | Full — upload, verify, tag, archive, generate packs | Primary operator |
| Group Internal Audit Head | 121 | G1 | Read — document completeness for audit | Cross-functional |
| Group Inspection Officer | 123 | G3 | Read + Upload — upload documents collected during visits | Field uploads |
| Group ISO / NAAC Coordinator | 124 | G1 | Read — cross-reference for quality certification | Coordination |
| Group Compliance Data Analyst | 127 | G1 | Read — document completeness metrics for MIS | Reporting |
| Group Process Improvement Coordinator | 128 | G3 | Read — document gaps feed CAPA items | Remediation link |
| Group CEO / Chairman | — | G4/G5 | Read + Override — can approve exceptions | Final authority |
| Branch Principal | — | G3 | Read (own branch) + Upload (own branch) | Primary document source |

> **Access enforcement:** `@require_role(min_level=G1, division='P')`. Branch Principals see only their own branch's documents. Upload: 125, 123, Branch Principal. Verify/approve: 125, G4/G5. Archive: 125.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Audit & Quality  ›  Affiliation  ›  Document Manager
```

### 3.2 Page Header
```
Affiliation Document Manager                     [+ Upload Document]  [Generate Inspection Pack]  [Bulk Upload]  [Export]
Affiliation Compliance Officer — S. Padmavathi
Sunrise Education Group · 28 branches · 847 documents on file · 92% complete · 14 expiring within 90 days
```

### 3.3 Filter Bar (below header)
```
Branch: [All / Select Branch ▼]    Board: [All / CBSE / ICSE / BSEAP / BSETS ▼]
Category: [All / Statutory / Infrastructure / Academic / Financial / Safety ▼]
Status: [All / Valid / Expiring Soon / Expired / Missing / Under Review ▼]
[Search by document name / type]                                        [Reset Filters]
```

### 3.4 KPI Summary Bar
Eight cards in a scrollable horizontal strip:

| # | KPI | Source | Colour Logic |
|---|---|---|---|
| 1 | Total Documents | Count of all uploaded docs | Neutral blue |
| 2 | Document Completeness | % branches with 100% required docs | ≥ 95% green · 80–94% amber · < 80% red |
| 3 | Valid Documents | Count currently valid (not expired) | Green |
| 4 | Expiring in 90 Days | Count with expiry ≤ 90 days from today | ≤ 5 green · 6–15 amber · > 15 red |
| 5 | Expired Documents | Count past expiry and not renewed | 0 green · 1–5 amber · > 5 red |
| 6 | Missing Documents | Required docs with no upload | 0 green · 1–10 amber · > 10 red |
| 7 | Under Review | Uploaded but not yet verified | Neutral blue |
| 8 | Branches 100% Ready | Count of branches with all docs valid + complete | = total branches green · else amber |

### 3.5 Tab Navigation

Four tabs below the KPI bar:

```
[Document Repository]    [Branch Completeness Matrix]    [Expiry Calendar]    [Inspection Packs]
```

---

### Tab 1 — Document Repository (default)

The master document list. Flat table with powerful filters. Each row is one document instance (one document for one branch).

**Table columns:**

| # | Column | Width | Content |
|---|---|---|---|
| 1 | Branch | 140px | Branch name + code |
| 2 | Board | 70px | CBSE / ICSE / BSEAP / BSETS |
| 3 | Document Category | 120px | Statutory · Infrastructure · Academic · Financial · Safety |
| 4 | Document Type | 180px | E.g., "Fire Safety NOC", "Building Stability Certificate", "School Recognition Order" |
| 5 | Document Number | 120px | Certificate/NOC number |
| 6 | Issued By | 140px | Issuing authority (e.g., "Chief Fire Officer, Hyderabad") |
| 7 | Issue Date | 90px | dd-MMM-yyyy |
| 8 | Expiry Date | 90px | dd-MMM-yyyy · red text if expired · amber if ≤ 90 days |
| 9 | Status | 90px | Badge — Valid (green) · Expiring Soon (amber) · Expired (red) · Under Review (blue) · Missing (grey) |
| 10 | Uploaded By | 110px | User who uploaded + date |
| 11 | Verified | 80px | ✅ Verified / ⏳ Pending / ❌ Rejected |
| 12 | Version | 50px | v1, v2, v3… |
| 13 | Actions | 80px | 👁 View · ⬇ Download · 🔄 Replace |

**Row interaction:** Click → opens Document Detail Drawer (right, 780px).

**Sorting:** By branch (default), expiry date, status, document type. Click column header to sort.

**Bulk actions toolbar** (visible when rows selected):
```
☐ Select All    [Verify Selected]  [Archive Selected]  [Download Selected as ZIP]
```

**Pagination:** 50 rows per page.

---

### Tab 2 — Branch Completeness Matrix

A matrix view showing document readiness per branch. The primary tool for identifying gaps.

**Matrix structure:**

| Branch | Fire NOC | Building Stability | School Recognition | Land Document | … (30+ columns) | Completeness % |
|---|---|---|---|---|---|---|
| Sunrise Begumpet | ✅ Valid | ✅ Valid | ✅ Valid | ✅ Valid | … | 100% |
| Sunrise Kukatpally | ✅ Valid | ⚠️ Expiring | ✅ Valid | ❌ Missing | … | 82% |
| Sunrise Miyapur | ❌ Expired | ✅ Valid | ❌ Missing | ✅ Valid | … | 68% |

**Cell states:**
- ✅ **Valid** (green) — Document uploaded, verified, not expired
- ⚠️ **Expiring** (amber) — Valid but expiring within 90 days
- ❌ **Expired** (red) — Document expired, renewal pending
- ❌ **Missing** (dark red) — Required but no document uploaded at all
- 🔵 **Under Review** (blue) — Uploaded but not yet verified by compliance officer
- ➖ **Not Required** (grey) — This document type not applicable for this board/branch

**Cell click:** Opens upload/view modal for that specific branch + document type combination.

**Row summary (rightmost column):** Completeness percentage with colour coding — 100% green, 80–99% amber, < 80% red.

**Column summary (bottom row):** "Group-wide" percentage — how many branches have this specific document valid.

**Board filter:** Radio buttons above matrix — `CBSE | ICSE | BSEAP | BSETS | All`. Matrix columns change per board (CBSE has different required docs than state boards).

**Export:** `[Export Matrix as Excel]` — generates branch × document matrix with status colours preserved.

---

### Tab 3 — Expiry Calendar

A calendar view (FullCalendar.js, month view) showing document expiry dates and renewal deadlines.

**Calendar events:**
- **Red dot:** Document expires on this date
- **Amber dot:** 90-day advance warning for expiry
- **Green dot:** Document renewed on this date
- **Blue dot:** CBSE/board inspection scheduled (from P-07)

**Event click:** Opens Document Detail Drawer.

**Right sidebar (alongside calendar):**

**Upcoming Expiries panel (scrollable list):**

| # | Days Left | Document | Branch | Expiry Date | Action |
|---|---|---|---|---|---|
| 1 | 12 days | Fire Safety NOC | Sunrise Miyapur | 07-Apr-2026 | [Upload Renewal] |
| 2 | 23 days | FSSAI Licence | Sunrise Begumpet | 18-Apr-2026 | [Upload Renewal] |
| 3 | 45 days | Trade Licence | Sunrise Kukatpally | 10-May-2026 | [Upload Renewal] |

Sorted by soonest expiry first. Colour-coded: ≤ 30 days red, 31–60 amber, 61–90 yellow.

**Overdue panel (collapsed by default, red header):**
Lists all currently expired documents with days overdue. Each row has `[Escalate]` button that sends email/notification to Branch Principal + Zone Director.

---

### Tab 4 — Inspection Packs

Pre-assembled document bundles for board inspections. When a CBSE/ICSE/State Board inspection is upcoming, the compliance officer generates an "Inspection Pack" — a complete, ordered set of all required documents matching the board's inspection checklist.

**Pack list table:**

| # | Column | Content |
|---|---|---|
| 1 | Branch | Branch name |
| 2 | Board | CBSE / ICSE / BSEAP |
| 3 | Pack Type | Initial Affiliation / Renewal / Extension / Upgrade |
| 4 | Generated Date | When the pack was last generated |
| 5 | Documents Included | e.g., "38 / 42" with progress bar |
| 6 | Completeness | Percentage with colour |
| 7 | Missing Docs | Count of documents not yet uploaded |
| 8 | Pack Status | Draft · Ready · Submitted · Returned |
| 9 | Actions | [Regenerate] · [Download PDF] · [Download ZIP] · [View Details] |

**Generate New Pack button:** `[+ Generate Inspection Pack]` → opens modal to select branch + board + pack type → system automatically assembles all matching documents in the board's required order.

**Pack detail view (drawer):**
- Ordered checklist matching the board's inspection proforma
- Each item shows: document name, status (✅ included / ❌ missing), file preview thumbnail
- Drag-and-drop reorder if needed
- Missing items highlighted with "Upload Now" button
- Cover page with institution details, affiliation number, school UDISE code
- Table of contents auto-generated

---

## 4. KPI Summary Bar

(Defined in Section 3.4 above)

---

## 5. Sections

| # | Section | Location | Purpose |
|---|---|---|---|
| 1 | Document Repository | Tab 1 | Master list of all documents across all branches |
| 2 | Branch Completeness Matrix | Tab 2 | Gap analysis — which branches are missing which documents |
| 3 | Expiry Calendar | Tab 3 | Time-based view of document lifecycles |
| 4 | Inspection Packs | Tab 4 | Board-inspection-ready document bundles |
| 5 | Document Detail Drawer | Right drawer | Full document view with metadata, history, preview |
| 6 | Upload Document Modal | Modal | Document upload with metadata entry |
| 7 | Bulk Upload Modal | Modal | CSV-mapped batch upload for multiple documents |
| 8 | Version History Panel | Within drawer | All versions of a document with diff highlights |

---

## 6. Drawers & Modals

### Drawer 1 — Document Detail Drawer (right, 780px)

**Trigger:** Click any document row in Tab 1 or any cell in Tab 2.

**Header:**
```
Document Detail — Fire Safety NOC                              [✕]
Sunrise Begumpet · CBSE · Safety Category
```

**Sections within drawer:**

**Section A — Document Preview (top half)**
- Embedded PDF/image viewer for the uploaded document
- If PDF: rendered inline with zoom, page navigation
- If image (JPG/PNG): displayed with zoom
- `[Download Original]` `[Print]` buttons

**Section B — Metadata**

| Field | Value |
|---|---|
| Document Type | Fire Safety NOC |
| Category | Safety |
| Document Number | FSN/2025/HYD/4523 |
| Issued By | Chief Fire Officer, GHMC, Hyderabad |
| Issue Date | 15-Mar-2025 |
| Expiry Date | 14-Mar-2026 |
| Days Until Expiry | 354 days (or "Expired 12 days ago" in red) |
| Applicable Board | CBSE, BSEAP |
| Branch | Sunrise Begumpet |
| UDISE Code | 36110300501 |
| Uploaded By | R. Suresh (Branch Admin) · 16-Mar-2025 |
| Verified By | S. Padmavathi (Compliance Officer) · 17-Mar-2025 |
| Version | v2 (current) |
| File Size | 1.2 MB |
| File Type | PDF |

**Section C — Verification**
```
Status: ✅ Verified
Verified by: S. Padmavathi · 17-Mar-2025
Notes: "Original document sighted during Begumpet visit. NOC number matches fire station records."
```
If unverified:
```
Status: ⏳ Pending Verification
[✅ Verify]  [❌ Reject]  [💬 Request Re-upload]
Rejection reason (if rejecting): [________________]
```

**Section D — Version History**

| Version | Uploaded | By | Expiry | Status | Action |
|---|---|---|---|---|---|
| v2 (current) | 16-Mar-2025 | R. Suresh | 14-Mar-2026 | Active | [View] |
| v1 (archived) | 12-Mar-2020 | M. Venkat | 11-Mar-2025 | Expired | [View] |

**Section E — Related Items**
- Linked to: P-11 CBSE Affiliation (Requirement #17: Fire Safety NOC)
- CAPA item: None (or link to CAPA if gap was raised)
- Inspection reference: "Verified during inspection on 20-Feb-2025 by K. Ramesh"

**Section F — Actions**
```
[Upload New Version]  [Archive]  [Link to Requirement]  [Send Reminder to Branch]
```

---

### Modal 1 — Upload Document

**Trigger:** `[+ Upload Document]` button or `[Upload Now]` from completeness matrix gaps.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Dropdown (searchable) | Yes | Pre-filled if opened from branch context |
| Board | Multi-select checkbox | Yes | CBSE, ICSE, BSEAP, BSETS — document may apply to multiple boards |
| Document Category | Dropdown | Yes | Statutory · Infrastructure · Academic · Financial · Safety |
| Document Type | Dropdown (filtered by category) | Yes | E.g., Fire Safety NOC, Building Stability Certificate |
| Document Number | Text | No | Certificate/licence number |
| Issued By | Text | No | Issuing authority name |
| Issue Date | Date picker | Yes | — |
| Expiry Date | Date picker | Conditional | Required for expiring documents (fire NOC, FSSAI, etc.); optional for permanent docs (land deed) |
| File Upload | Drag-drop zone | Yes | PDF, JPG, PNG. Max 10 MB. |
| Notes | Textarea | No | Context — "Renewed after GHMC fire audit on 10-Mar-2025" |
| Replace Existing? | Checkbox | No | If checked, archives the current version and makes this the new active version |

**Validation:**
- Duplicate check: If same branch + document type already has an active version → warning: "This branch already has a valid Fire Safety NOC (v2, expires 14-Mar-2026). Upload as new version?"
- File type check: Only PDF, JPG, PNG accepted
- File size check: Max 10 MB per file
- Expiry date must be after issue date

**Actions:** `[Upload]` `[Cancel]`

---

### Modal 2 — Bulk Upload

**Trigger:** `[Bulk Upload]` button.

**Step 1 — Download Template:**
- Download CSV template with columns: Branch Code, Board, Document Category, Document Type, Document Number, Issued By, Issue Date (DD-MM-YYYY), Expiry Date (DD-MM-YYYY), Filename
- Instructions sheet explains each column

**Step 2 — Upload CSV + Files:**
- Upload completed CSV
- Upload ZIP file containing all document files (named to match Filename column in CSV)
- System validates: CSV format, file matches, date formats, required fields

**Step 3 — Review & Confirm:**
- Preview table showing all documents to be uploaded with validation status
- ✅ Valid rows ready for upload
- ❌ Error rows (missing file, invalid date, unknown branch code) — highlighted with error message
- `[Upload Valid (34 of 38)]` `[Fix Errors & Re-upload]` `[Cancel]`

**Post-upload:** Toast "34 documents uploaded successfully. 4 errors — download error report."

---

### Modal 3 — Generate Inspection Pack

**Trigger:** `[+ Generate Inspection Pack]` from Tab 4.

**Form fields:**

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Dropdown | Yes | Select branch for inspection |
| Board | Dropdown | Yes | CBSE / ICSE / BSEAP / BSETS |
| Pack Type | Dropdown | Yes | Initial Affiliation / Renewal / Extension / Upgrade / Annual Verification |
| Inspection Date | Date picker | No | Expected date — shown on cover page |
| Include Cover Page | Checkbox (default checked) | No | Auto-generated cover with institution details |
| Include Table of Contents | Checkbox (default checked) | No | Auto-generated TOC |
| Watermark | Dropdown | No | None / "CONFIDENTIAL" / "FOR INSPECTION ONLY" / Custom text |

**Preview:** After clicking `[Generate Preview]`, system shows ordered document list:
```
1. School Recognition Order ............. ✅ Included (v3, 12-Jan-2024)
2. NOC from State Education Dept ........ ✅ Included (v1, 05-Aug-2021)
3. Land Document (Sale Deed) ............ ✅ Included (v1, original)
4. Building Completion Certificate ...... ✅ Included (v2, 20-Mar-2023)
5. Fire Safety NOC ...................... ❌ EXPIRED (v2, expired 14-Mar-2026)
6. Building Stability Certificate ....... ✅ Included (v1, 10-Jun-2024)
...
38. Audited Accounts (FY 2024-25) ....... ❌ MISSING
```

**Gap alert:** If any documents are missing or expired, amber warning: "5 of 42 documents are missing or expired. Pack will be incomplete."

**Actions:** `[Generate Pack (PDF)]` `[Generate Pack (ZIP)]` `[Cancel]`

---

### Modal 4 — Send Reminder / Escalation

**Trigger:** `[Send Reminder to Branch]` from drawer or `[Escalate]` from expiry calendar.

**Form:**
```
To:         [Branch Principal — R. Suresh]  [Branch Admin — K. Latha]  [+ Add recipient]
Subject:    Auto-filled: "Document Required: Fire Safety NOC — Sunrise Miyapur — Expiring 07-Apr-2026"
Message:    Auto-filled template with document details, expiry date, and upload instructions
Priority:   [Normal / Urgent / Critical]
Escalate:   ☐ Copy to Zone Director   ☐ Copy to CEO   ☐ Copy to Internal Audit Head
Deadline:   [Date picker — by when must the document be uploaded]
```

**Actions:** `[Send]` `[Cancel]`

---

## 7. Charts

### Chart 1 — Document Completeness by Branch (horizontal bar)
- **Type:** Horizontal bar chart (Chart.js 4.x)
- **X-axis:** Completeness percentage (0–100%)
- **Y-axis:** Branch names (sorted ascending by completeness)
- **Colour:** Bars coloured by band — green ≥ 95%, amber 80–94%, red < 80%
- **Threshold line:** Vertical dashed line at 100% (target)
- **Hover:** Branch name, percentage, missing count
- **Location:** Below KPI bar (visible on all tabs) or within Tab 2 header
- **API:** `GET /api/v1/group/{id}/audit/affiliation/documents/charts/completeness-by-branch/`

### Chart 2 — Expiry Timeline (stacked area)
- **Type:** Stacked area chart (Chart.js 4.x)
- **X-axis:** Months (next 12 months)
- **Y-axis:** Count of documents expiring
- **Stacks:** Document category — Statutory (red), Safety (orange), Infrastructure (blue), Academic (green), Financial (purple)
- **Purpose:** Shows when expiry peaks will hit, allowing proactive renewal planning
- **Hover:** Month, count per category, total
- **Location:** Tab 3 sidebar top
- **API:** `GET /api/v1/group/{id}/audit/affiliation/documents/charts/expiry-timeline/`

### Chart 3 — Document Status Distribution (doughnut)
- **Type:** Doughnut chart (Chart.js 4.x)
- **Segments:** Valid (green), Expiring Soon (amber), Expired (red), Missing (dark grey), Under Review (blue)
- **Centre text:** Total document count + overall valid %
- **Hover:** Status label, count, percentage
- **Location:** Tab 1 right sidebar (if space) or KPI bar expansion
- **API:** `GET /api/v1/group/{id}/audit/affiliation/documents/charts/status-distribution/`

### Chart 4 — Category-wise Completeness (radar)
- **Type:** Radar chart (Chart.js 4.x)
- **Axes:** 5 categories — Statutory, Infrastructure, Academic, Financial, Safety
- **Series:** Group average (solid fill) vs target (100%, dashed outline)
- **Purpose:** Shows which document categories have the most gaps across the group
- **Hover:** Category, group average %, gap from target
- **Location:** Tab 2 top, next to completeness matrix
- **API:** `GET /api/v1/group/{id}/audit/affiliation/documents/charts/category-completeness/`

---

## 8. Toast Messages

| Action | Toast | Type |
|---|---|---|
| Document uploaded | "Fire Safety NOC uploaded for Sunrise Begumpet — pending verification" | Success (green) |
| Document verified | "Fire Safety NOC verified — Sunrise Begumpet now 100% complete" | Success (green) |
| Document rejected | "Building Stability Certificate rejected — re-upload requested from Sunrise Miyapur" | Warning (amber) |
| Document archived | "Fire Safety NOC v1 archived — v2 is now the active version" | Info (blue) |
| Bulk upload complete | "34 documents uploaded successfully · 4 errors (download error report)" | Success + Info |
| Inspection pack generated | "CBSE Inspection Pack for Sunrise Begumpet generated — 38/42 documents included" | Success (green) |
| Inspection pack incomplete | "Pack has 4 missing documents — not inspection-ready" | Warning (amber) |
| Reminder sent | "Document reminder sent to R. Suresh (Sunrise Miyapur) — deadline: 01-Apr-2026" | Info (blue) |
| Duplicate upload warning | "Sunrise Begumpet already has a valid Fire NOC (v2). Replace existing?" | Warning (amber) |
| Upload validation error | "File exceeds 10 MB limit — please compress or split" | Error (red) |
| Expiry alert | "14 documents expiring within 30 days — review required" | Warning (amber) |
| Verification overdue | "8 documents uploaded > 7 days ago still pending verification" | Warning (amber) |

---

## 9. Empty States

| Scenario | Illustration | Message | CTA |
|---|---|---|---|
| No documents uploaded (fresh group) | Folder with dotted outline | "No affiliation documents uploaded yet. Start by uploading your branches' key documents — fire NOC, recognition order, building stability certificate." | `[+ Upload First Document]` `[Bulk Upload from CSV]` |
| No documents for selected branch | Empty shelf | "No documents on file for {branch name}. Upload required affiliation documents to track compliance." | `[+ Upload Document]` |
| No expiring documents (Tab 3) | Calendar with green checkmark | "No documents expiring in the next 90 days. All documents are current." | — (positive state) |
| No inspection packs generated (Tab 4) | Package with dotted outline | "No inspection packs generated yet. Create a pack when a board inspection is approaching." | `[+ Generate Inspection Pack]` |
| Filter returns zero results | Magnifying glass | "No documents match your filters. Try adjusting the branch, board, or status filter." | `[Reset Filters]` |
| Bulk upload — no valid rows | Spreadsheet with red X | "No valid rows found in the CSV. Please check the template format and re-upload." | `[Download Template]` `[Re-upload]` |

---

## 10. Loader States

| Element | Loader Type | Duration |
|---|---|---|
| Page initial load | Skeleton: 8 KPI cards + table rows | < 1s target |
| KPI bar | 8 grey pulse cards → populated | < 500ms |
| Document repository table | 10 skeleton rows → data | < 1s |
| Branch completeness matrix | Grid skeleton with pulsing cells | < 1.5s (large matrix) |
| Expiry calendar | Calendar skeleton (grey blocks) | < 1s |
| Document preview (in drawer) | Spinner centred in preview area + "Loading document…" | Depends on file size (1–5s for 5 MB PDF) |
| Inspection pack generation | Progress bar: "Generating pack… 18/42 documents assembled" | 3–10s depending on count |
| Bulk upload processing | Progress bar: "Processing… 12/38 files validated" | 5–20s depending on batch size |
| Chart rendering | Grey chart skeleton → Chart.js render | < 500ms |
| Export (Excel/ZIP) | Spinner on button + "Preparing download…" | 2–10s |

---

## 11. API Endpoints

All endpoints prefixed: `/api/v1/group/{group_id}/audit/affiliation/documents/`

| # | Method | Endpoint | Purpose | Role |
|---|---|---|---|---|
| 1 | GET | `/` | List all documents (paginated, filterable) | G1+ |
| 2 | GET | `/{doc_id}/` | Document detail with metadata + version history | G1+ |
| 3 | POST | `/` | Upload new document | 125, 123, Branch Principal |
| 4 | PATCH | `/{doc_id}/` | Update document metadata (number, issuer, dates) | 125 |
| 5 | DELETE | `/{doc_id}/` | Soft-delete / archive a document | 125, G4+ |
| 6 | POST | `/{doc_id}/versions/` | Upload new version of existing document | 125, 123, Branch Principal |
| 7 | GET | `/{doc_id}/versions/` | List all versions of a document | G1+ |
| 8 | GET | `/{doc_id}/versions/{version_id}/download/` | Download specific version file | G1+ |
| 9 | POST | `/{doc_id}/verify/` | Mark document as verified | 125 |
| 10 | POST | `/{doc_id}/reject/` | Reject document with reason | 125 |
| 11 | GET | `/completeness-matrix/` | Branch × document type matrix | G1+ |
| 12 | GET | `/completeness-matrix/?board={board}` | Board-filtered completeness matrix | G1+ |
| 13 | GET | `/expiry-calendar/` | Documents expiring in date range | G1+ |
| 14 | GET | `/expiring/?days={n}` | Documents expiring within N days | G1+ |
| 15 | GET | `/missing/` | All required documents not yet uploaded | G1+ |
| 16 | POST | `/bulk-upload/` | Upload CSV + ZIP for batch processing | 125 |
| 17 | GET | `/bulk-upload/{job_id}/status/` | Check bulk upload processing status | 125 |
| 18 | POST | `/inspection-packs/` | Generate inspection pack for branch + board | 125 |
| 19 | GET | `/inspection-packs/` | List all generated inspection packs | G1+ |
| 20 | GET | `/inspection-packs/{pack_id}/` | Pack detail with document checklist | G1+ |
| 21 | GET | `/inspection-packs/{pack_id}/download/` | Download pack as PDF or ZIP | G1+ |
| 22 | POST | `/reminders/` | Send document reminder to branch | 125, 128 |
| 23 | GET | `/charts/completeness-by-branch/` | Chart 1 data | G1+ |
| 24 | GET | `/charts/expiry-timeline/` | Chart 2 data | G1+ |
| 25 | GET | `/charts/status-distribution/` | Chart 3 data | G1+ |
| 26 | GET | `/charts/category-completeness/` | Chart 4 data | G1+ |
| 27 | GET | `/export/` | Export document list as Excel | G1+ |
| 28 | GET | `/kpis/` | KPI bar aggregates | G1+ |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../documents/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#doc-content` | `innerHTML` | `hx-trigger="click"` |
| Document repository table | Tab 1 load | `hx-get=".../documents/?page=1"` | `#doc-table-body` | `innerHTML` | Paginated |
| Filter change | Filter select/input | `hx-get=".../documents/?branch={}&status={}"` | `#doc-table-body` | `innerHTML` | `hx-trigger="change"` debounced 300ms |
| Document detail drawer | Row click | `hx-get=".../documents/{id}/"` | `#right-drawer` | `innerHTML` | 780px drawer |
| Upload document | Form submit | `hx-post=".../documents/"` | `#upload-result` | `innerHTML` | Toast + table refresh |
| Verify document | Button click | `hx-post=".../documents/{id}/verify/"` | `#doc-{id}-status` | `innerHTML` | Inline badge update |
| Reject document | Form submit | `hx-post=".../documents/{id}/reject/"` | `#doc-{id}-status` | `innerHTML` | Toast + badge update |
| Upload new version | Form submit | `hx-post=".../documents/{id}/versions/"` | `#version-list` | `innerHTML` | Toast + version list refresh |
| Branch completeness matrix | Tab 2 load | `hx-get=".../documents/completeness-matrix/"` | `#matrix-content` | `innerHTML` | Large grid |
| Board filter (matrix) | Radio change | `hx-get=".../documents/completeness-matrix/?board={board}"` | `#matrix-content` | `innerHTML` | Board-specific matrix |
| Expiry calendar | Tab 3 load | `hx-get=".../documents/expiry-calendar/"` | `#calendar-content` | `innerHTML` | FullCalendar.js init |
| Generate inspection pack | Form submit | `hx-post=".../documents/inspection-packs/"` | `#pack-result` | `innerHTML` | Progress bar → toast |
| Bulk upload | Form submit | `hx-post=".../documents/bulk-upload/"` | `#bulk-result` | `innerHTML` | Progress bar → result |
| Send reminder | Form submit | `hx-post=".../documents/reminders/"` | `#reminder-result` | `innerHTML` | Toast |
| Chart load | Tab/section shown | `hx-get` chart endpoint | `#chart-{name}` | `innerHTML` | Canvas + Chart.js |
| Pagination | Page click | `hx-get` with page param | `#doc-table-body` | `innerHTML` | — |
| Export | Button click | `hx-get=".../documents/export/"` | — | — | Direct download trigger |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
