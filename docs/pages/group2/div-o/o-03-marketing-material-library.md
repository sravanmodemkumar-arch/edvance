# O-03 — Marketing Material Library

> **URL:** `/group/marketing/brand/materials/`
> **File:** `o-03-marketing-material-library.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary uploader/manager

---

## 1. Purpose

The Marketing Material Library is the centralised digital asset management (DAM) system for all marketing collateral used across every branch in the group. Every brochure, poster, newspaper ad creative, WhatsApp image, video testimonial, prospectus PDF, flex banner design, pamphlet artwork, and social media post template lives here — uploaded once by the Content Coordinator at group HQ, downloaded hundreds of times by branch staff across 5–50 locations.

In Indian education groups, the marketing material problem is acute. During peak admission season (January–April), every branch needs:
- Newspaper ad artwork customised with branch name, address, and phone number
- WhatsApp images for parent broadcasts — scholarship exam dates, fee structures, topper photos
- Flex banner designs for school gate, nearby junctions, and auto-rickshaw backs
- Prospectus PDFs for walk-in parents
- Video testimonials of toppers for YouTube and Instagram

Without a centralised library, branches create their own materials — with wrong logos, inconsistent messaging, outdated fee structures, and unapproved claims ("100% results!" when actual pass rate is 94%). This page eliminates that chaos by being the ONLY source from which branches can download marketing materials.

The library supports versioning (v1, v2, v3 of the same creative), branch-specific customisation (same design, different branch details via variable fields), approval workflows (Content Coordinator uploads → Campaign Manager or G4/G5 approves → published to branches), and download tracking (who downloaded what, when, from which branch).

**Scale:** 5–50 branches · 200–2,000 active materials · 50–500 new uploads per admission season · 10,000–50,000 downloads per season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Marketing Director | 114 | G0 | No Platform Access | Approves creatives externally |
| Group Brand Manager | 115 | G0 | No Platform Access | Creates designs externally |
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — upload, edit, version, approve, archive | Primary library manager |
| Group Admissions Campaign Manager | 119 | G3 | Read + Download + Approve (final) | Approves materials before publish |
| Group Topper Relations Manager | 120 | G3 | Read + Download | Downloads topper-related materials |
| Group Admission Telecaller Executive | 130 | G3 | Read + Download (limited) | Downloads call scripts, fee sheets |
| Group Admission Data Analyst | 132 | G1 | Read only | View analytics; no download |
| Branch Principal | — | G3 | Read + Download (own branch materials) | Filtered to branch-relevant items |
| Branch Admin Staff | — | G2 | Read + Download (own branch materials) | Primary branch-level downloader |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Upload/edit: `role_id IN (131) OR level >= G4`. Approve: `role_id IN (119, 131) OR level >= G4`. Branch users see only materials tagged to their branch or marked "All Branches".

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Brand & Content  ›  Marketing Material Library
```

### 3.2 Page Header
```
Marketing Material Library                     [Upload Material]  [Bulk Upload]  [Download Report]
Content Coordinator — Meena Raghavan
Sunrise Education Group · 847 active materials · 12,340 downloads this season
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Materials pending approval > 10 | "[N] materials pending approval. Review and approve to make them available to branches." | Medium (yellow) |
| Any material with outdated fee structure | "[N] material(s) contain fee structures from previous year. Update immediately." | High (amber) |
| Admission season starting within 30 days | "Admission season starts [Date]. Ensure all campaign materials are uploaded and approved." | Info (blue) |
| Storage usage > 80% of plan limit | "Storage usage at [X]% of plan limit. Archive old materials or upgrade storage." | Medium (yellow) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Materials | Integer | COUNT(materials) WHERE status = 'published' | Static blue | `#kpi-active` |
| 2 | Pending Approval | Integer | COUNT(materials) WHERE status = 'pending_approval' | Red > 10, Amber 5–10, Green < 5 | `#kpi-pending` |
| 3 | Downloads (This Month) | Integer | COUNT(downloads) WHERE month = current | Static green | `#kpi-downloads-month` |
| 4 | Most Downloaded | Text | material.name WHERE download_count = MAX in current month | Static blue | `#kpi-top-material` |
| 5 | New This Month | Integer | COUNT(materials) WHERE created_at within current month | Static blue | `#kpi-new-month` |
| 6 | Storage Used | GB + % | SUM(file_size) / storage_limit × 100 | Green < 70%, Amber 70–90%, Red > 90% | `#kpi-storage` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/materials/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Filter & Search Bar

**Search:** Full-text search across material name, description, tags. Debounced 350ms.

**Filters (horizontal bar):**

| Filter | Type | Options |
|---|---|---|
| Category | Dropdown | Brochure / Poster / Newspaper Ad / WhatsApp Image / Video / Flex Banner / Pamphlet / Prospectus / Social Media / Standee / Call Script / Fee Sheet / Certificate / Other |
| Campaign | Dropdown | All / [List of campaigns from O-08] |
| Branch | Dropdown | All Branches / [Specific branch] |
| Stream | Dropdown | All / MPC / BiPC / MEC / CEC / HEC / Foundation / General |
| Status | Dropdown | All / Published / Pending Approval / Draft / Archived |
| Medium | Dropdown | Print / Digital / Video / Document |
| Season | Dropdown | Current Season / [Previous seasons] |
| Language | Dropdown | English / Telugu / Hindi / Tamil / Kannada / Bilingual |

**View toggle:** Grid view (default — visual cards) / List view (table format)

**Sort options:** Newest First (default) / Most Downloaded / Name A-Z / Recently Updated

### 5.2 Material Grid (Default View)

Card-based grid layout showing material thumbnails. 4 columns on desktop, 2 on tablet, 1 on mobile.

**Card Layout:**

```
┌────────────────────────────────┐
│  ┌──────────────────────────┐  │
│  │                          │  │
│  │    [Thumbnail Preview]   │  │
│  │       (240×180 px)       │  │
│  │                          │  │
│  └──────────────────────────┘  │
│                                │
│  📰 Newspaper Ad — Feb Blitz   │
│  Category: Newspaper Ad        │
│  Campaign: February Blitz      │
│  Branch: All Branches          │
│  Language: Telugu + English     │
│                                │
│  v2.1 · PDF · 4.2 MB          │
│  Downloads: 142 · ⭐ Popular   │
│                                │
│  [Preview]  [Download]         │
│  Status: ✅ Published          │
└────────────────────────────────┘
```

**Card Fields:**
- Thumbnail: auto-generated preview (images: actual thumbnail; PDFs: first page render; videos: frame grab; docs: file icon + type badge)
- Material name (max 2 lines, ellipsis)
- Category badge (colour-coded)
- Campaign name (if linked)
- Branch scope: "All Branches" or specific branch name
- Language badge(s)
- Version number · File format · File size
- Download count · Popularity badge (if top 10% downloads)
- Status badge: Published (green) / Pending (amber) / Draft (grey) / Archived (red strikethrough)
- Action buttons: [Preview] [Download]

**Pagination:** Infinite scroll with "Load more" button · 24 cards per load

### 5.3 Material List View (Alternative)

Table format for users who prefer a compact listing.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Thumbnail | Image (60×45 px) | No | Mini preview |
| Material Name | Text | Yes | Click opens detail drawer |
| Category | Badge | Yes | Colour-coded |
| Campaign | Text | Yes | Campaign name or "—" |
| Branch | Text | Yes | "All" or branch name |
| Language | Badge(s) | Yes | EN / TE / HI / TA / KN |
| Format | Badge | Yes | PDF / PNG / JPG / MP4 / DOCX |
| Size | Text | Yes | File size in MB |
| Version | Text | Yes | e.g., "v2.1" |
| Downloads | Integer | Yes | Total download count |
| Status | Badge | Yes | Published / Pending / Draft / Archived |
| Uploaded | Date | Yes | Upload date |
| Actions | Buttons | No | [Preview] [Download] [⋮ More] |

**Default sort:** Uploaded DESC (newest first)
**Pagination:** Server-side · 50 per page

### 5.4 Category Quick-Nav

Horizontal scrollable row of category tiles at the top of the content area. Each tile shows:
- Category icon (📰 Newspaper / 📱 WhatsApp / 🎬 Video / 📄 Brochure / 🪧 Flex / 📋 Prospectus / etc.)
- Category name
- Count of active materials in category
- Click filters the grid/list to that category

### 5.5 Approval Queue (Content Coordinator & Campaign Manager only)

Separate tab/section showing materials in "Pending Approval" status. Displayed above the main grid when there are items awaiting review.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Thumbnail | Image (60×45 px) | Preview |
| Material Name | Text | Click opens detail |
| Category | Badge | Type of material |
| Uploaded By | Text | User who uploaded |
| Upload Date | Date | When submitted for approval |
| Days Pending | Integer | Days since upload; red if > 3 |
| Actions | Buttons | [Preview] [Approve ✅] [Reject ❌] [Edit ✏️] |

**Approve action:** Changes status to 'published'; material becomes visible to all branches; toast confirmation
**Reject action:** Opens rejection modal with reason field; status changes to 'rejected'; notification sent to uploader

---

## 6. Drawers & Modals

### 6.1 Modal: `upload-material` (640px)
- **Title:** "Upload Marketing Material"
- **Fields:**
  - Material name (text, required, max 120 chars)
  - Category (dropdown, required — see filter list)
  - Sub-category (dropdown, optional — e.g., for Newspaper Ad: Quarter Page / Half Page / Full Page)
  - Campaign (dropdown, optional — link to campaign from O-08)
  - Branch scope (radio): All Branches / Specific Branches (multi-select)
  - Stream (multi-select): MPC / BiPC / MEC / CEC / HEC / Foundation / General
  - Language (multi-select, required): English / Telugu / Hindi / Tamil / Kannada
  - Medium (dropdown): Print / Digital / Video / Document
  - File upload (drag-and-drop zone)
    - Accepted: PNG, JPG, SVG, PDF, AI, PSD, MP4, MOV, DOCX, XLSX, PPTX
    - Max single file: 100 MB (video), 50 MB (others)
    - Multiple files allowed (creates one material per file, or bundle as single material)
  - Version notes (textarea, optional — "What changed from previous version")
  - Tags (tag input — free-form, comma-separated)
  - Description / usage instructions (textarea, optional)
  - Auto-approve (toggle, G4/G5 only — skips approval queue)
  - Notify branches on publish (toggle, default ON)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Behaviour:** POST to `/api/v1/group/{id}/marketing/materials/` → Cloudflare R2 upload → thumbnail auto-generated → toast

### 6.2 Modal: `bulk-upload` (640px)
- **Title:** "Bulk Upload Materials"
- **Fields:**
  - ZIP file upload (drag-and-drop, max 500 MB)
  - Default category (dropdown — applied to all files in ZIP)
  - Default campaign (dropdown, optional)
  - Default branch scope (radio): All Branches / Specific
  - Default language (multi-select)
  - Auto-name from filename (toggle, default ON — file name becomes material name)
- **Behaviour:** POST → unzips server-side → creates individual material records → progress bar → summary toast: "[N] materials uploaded, [M] failed"
- **Access:** Role 131 (G2) or G4/G5 only

### 6.3 Drawer: `material-detail` (720px, right-slide)
Opens when clicking any material card or row.

- **Tabs:** Preview · Details · Versions · Downloads · Branch Customisation · Notes

- **Preview tab:**
  - Full-size preview: images rendered inline; PDFs via embedded viewer; videos via HTML5 player; documents show first page render + download button
  - Zoom controls for images/PDFs
  - For videos: play/pause, duration, quality selector

- **Details tab:**
  - Material name, category, sub-category
  - Campaign link (clickable → O-08)
  - Branch scope (list of branches if specific)
  - Stream tags, language tags
  - File format, file size, dimensions (if image/video), duration (if video)
  - Uploaded by, upload date, last modified
  - Status + status history (draft → pending → published)
  - Tags
  - Description / usage instructions
  - Direct download URL (copyable — for sharing via WhatsApp/email)

- **Versions tab:**
  - Version history table: Version # · Date · Uploaded By · Notes · File Size · [Download] [Restore]
  - "Restore" reverts to a previous version (G2+ only)

- **Downloads tab:**
  - Download log table: User · Branch · Date · IP · Format
  - Download count by branch (mini bar chart)

- **Branch Customisation tab:**
  - Shows which branches have customised copies of this material
  - Variable fields that differ per branch: branch name, address, phone number, principal name
  - "Generate for Branch" button → creates branch-specific PDF with variables replaced

- **Notes tab:**
  - Internal notes (editable by G2+)
  - Approval notes / rejection reason (if applicable)

- **Footer:** [Download] [Edit] [New Version] [Archive] [Delete] (actions per role level)

### 6.4 Modal: `reject-material` (480px)
- **Title:** "Reject Material"
- **Fields:**
  - Rejection reason (dropdown): Incorrect branding / Wrong fee structure / Outdated information / Poor quality / Unapproved claims / Other
  - Additional notes (textarea)
- **Buttons:** Cancel · Reject
- **Behaviour:** PATCH status → 'rejected' → notification to uploader

### 6.5 Modal: `generate-branch-copy` (560px)
- **Title:** "Generate Branch-Specific Material"
- **Description:** "Create a customised copy of this material with branch-specific details."
- **Fields:**
  - Select branch (dropdown)
  - Variable fields auto-populated from branch record:
    - Branch Name: [auto-filled, editable]
    - Branch Address: [auto-filled, editable]
    - Phone Number: [auto-filled, editable]
    - Principal Name: [auto-filled, editable]
    - Admission Helpline: [auto-filled, editable]
  - Output format: PDF / PNG
- **Buttons:** Cancel · Generate
- **Behaviour:** POST → server-side template rendering → download link in toast
- **Access:** G2+ or branch staff with `material_download` permission

---

## 7. Charts

### 7.1 Downloads Over Time (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Material Downloads — Last 6 Months" |
| Data | Monthly download count |
| X-axis | Month |
| Y-axis | Download count |
| Colour | `#3B82F6` (blue) |
| Tooltip | "[Month]: [N] downloads" |
| API endpoint | `GET /api/v1/group/{id}/marketing/materials/analytics/downloads-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-downloads-trend"` |
| Export | PNG |

### 7.2 Top 10 Materials (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Top 10 Most Downloaded Materials — Current Season" |
| Data | Top 10 materials by download count |
| X-axis | Download count |
| Y-axis | Material name (truncated to 30 chars) |
| Colour | Gradient `#3B82F6` → `#93C5FD` |
| Tooltip | "[Material]: [N] downloads across [M] branches" |
| API endpoint | `GET /api/v1/group/{id}/marketing/materials/analytics/top-materials/` |
| HTMX | `hx-get` on load → `hx-target="#chart-top-materials"` |
| Export | PNG |

### 7.3 Category Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Materials by Category" |
| Data | Count of active materials per category |
| Colour | Distinct palette per category |
| Tooltip | "[Category]: [N] materials ([X]%)" |
| API endpoint | `GET /api/v1/group/{id}/marketing/materials/analytics/category-distribution/` |
| HTMX | `hx-get` on load → `hx-target="#chart-category-dist"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Material uploaded | "Material '[Name]' uploaded — pending approval" | Success | 3s |
| Material approved | "Material '[Name]' approved and published to [N] branches" | Success | 4s |
| Material rejected | "Material '[Name]' rejected. Uploader notified." | Info | 3s |
| Material archived | "Material '[Name]' archived. No longer visible to branches." | Info | 3s |
| Material restored | "Material '[Name]' restored to Version [X]" | Success | 3s |
| Bulk upload complete | "[N] materials uploaded successfully. [M] pending approval." | Success | 5s |
| Bulk upload partial fail | "[N] uploaded, [M] failed (unsupported format or size limit). Review errors." | Warning | 8s |
| Branch copy generated | "Branch-specific copy for [Branch] ready. Click to download." | Success | 6s |
| Download started | "Downloading '[Name]'…" | Info | 2s |
| Delete confirmed | "Material '[Name]' permanently deleted." | Info | 3s |
| Upload failed — size | "File exceeds size limit ([X] MB max). Compress and retry." | Error | 5s |
| Upload failed — format | "Unsupported format. Accepted: PNG, JPG, SVG, PDF, AI, PSD, MP4, MOV, DOCX" | Error | 5s |
| Storage limit warning | "Storage at [X]%. Archive unused materials to free space." | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No materials uploaded | 📁 | "Library is Empty" | "Upload your first marketing material — brochure, poster, or WhatsApp image." | Upload Material |
| No materials in category | 📂 | "No [Category] Materials" | "No materials found in this category. Upload one to get started." | Upload Material |
| No results for search/filter | 🔍 | "No Materials Found" | "Try adjusting your search or filters. Check archived materials." | Clear Filters |
| No pending approvals | ✅ | "All Caught Up" | "No materials pending approval. All uploaded materials have been reviewed." | — |
| No downloads yet | 📥 | "No Downloads Recorded" | "Materials will show download stats once branches start using them." | — |
| Branch user — no materials for branch | 🏫 | "No Materials Available" | "No marketing materials have been published for your branch yet. Contact Group HQ." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI shimmer cards + filter bar placeholder + 12 card-shaped shimmer blocks (4×3 grid) |
| Grid card load (infinite scroll) | 4 new shimmer card blocks appended to grid |
| List view table load | Table skeleton: 10 shimmer rows |
| Material detail drawer | Right-slide skeleton: large preview placeholder + 5 tab placeholders |
| File upload progress | Progress bar inside modal: "Uploading [filename]… [X]%" with file size indicator |
| Bulk upload progress | Progress bar + file counter: "Processing file [N] of [M]… [X]%" |
| Branch copy generation | Modal spinner: "Generating branch copy for [Branch]…" |
| Thumbnail generation | Card shows grey placeholder with "Generating preview…" text until thumbnail ready |
| Chart load | Chart placeholder with grey canvas + "Loading analytics…" |
| Search results | Grid/list body replaced with shimmer while results load |

---

## 11. Role-Based UI Visibility

| Element | Content Coord (131, G2) | Campaign Mgr (119, G3) | Topper Mgr (120, G3) | Telecaller (130, G3) | Data Analyst (132, G1) | Branch Staff (G2/G3) | G4/G5 |
|---|---|---|---|---|---|---|---|
| All 6 KPI Cards | All visible | All visible | Downloads + Active only | — | All visible | Downloads only | All visible |
| Upload Button | Visible | Not visible | Not visible | Not visible | Not visible | Not visible | Visible |
| Bulk Upload Button | Visible | Not visible | Not visible | Not visible | Not visible | Not visible | Visible |
| Approval Queue | Visible + Approve/Reject | Visible + Approve only | Not visible | Not visible | Not visible | Not visible | Visible + Approve |
| Material Grid/List | All materials (all statuses) | Published + Pending | Published only | Published (scripts/fees only) | Published only | Published (own branch) | All materials |
| Download Button | Visible | Visible | Visible | Visible (limited) | Not visible | Visible | Visible |
| Edit/Archive Buttons | Visible | Not visible | Not visible | Not visible | Not visible | Not visible | Visible |
| Version History | Visible | Read only | Not visible | Not visible | Not visible | Not visible | Visible |
| Download Analytics | Visible | Visible | Not visible | Not visible | Visible | Not visible | Visible |
| Branch Customisation | Visible + Generate | Read only | Not visible | Not visible | Not visible | Generate (own branch) | Visible + Generate |
| Charts | All visible | All visible | Not visible | Not visible | All visible | Not visible | All visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/materials/` | G1+ | List materials (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/materials/{material_id}/` | G1+ | Single material detail |
| POST | `/api/v1/group/{id}/marketing/materials/` | G2+ | Upload new material |
| PUT | `/api/v1/group/{id}/marketing/materials/{material_id}/` | G2+ | Update material metadata |
| DELETE | `/api/v1/group/{id}/marketing/materials/{material_id}/` | G4+ | Permanently delete material |
| PATCH | `/api/v1/group/{id}/marketing/materials/{material_id}/status/` | G2+ | Change status (approve/reject/archive/restore) |
| POST | `/api/v1/group/{id}/marketing/materials/bulk-upload/` | G2+ | Bulk upload via ZIP |
| GET | `/api/v1/group/{id}/marketing/materials/{material_id}/download/` | G2+ | Download material file |
| GET | `/api/v1/group/{id}/marketing/materials/{material_id}/versions/` | G1+ | Version history |
| POST | `/api/v1/group/{id}/marketing/materials/{material_id}/versions/` | G2+ | Upload new version |
| PATCH | `/api/v1/group/{id}/marketing/materials/{material_id}/versions/{ver}/restore/` | G2+ | Restore previous version |
| GET | `/api/v1/group/{id}/marketing/materials/{material_id}/downloads/` | G1+ | Download log |
| POST | `/api/v1/group/{id}/marketing/materials/{material_id}/branch-copy/` | G2+ | Generate branch-specific copy |
| GET | `/api/v1/group/{id}/marketing/materials/kpis/` | G1+ | KPI card values |
| GET | `/api/v1/group/{id}/marketing/materials/analytics/downloads-trend/` | G1+ | Monthly download trend |
| GET | `/api/v1/group/{id}/marketing/materials/analytics/top-materials/` | G1+ | Top 10 downloaded |
| GET | `/api/v1/group/{id}/marketing/materials/analytics/category-distribution/` | G1+ | Category breakdown |
| GET | `/api/v1/group/{id}/marketing/materials/pending/` | G2+ | Pending approval queue |

### Query Parameters — Material List

| Parameter | Type | Description |
|---|---|---|
| `category` | string | Filter by category |
| `campaign_id` | integer | Filter by linked campaign |
| `branch_id` | integer | Filter by branch scope |
| `stream` | string | Filter by stream |
| `status` | string | published / pending / draft / archived |
| `medium` | string | print / digital / video / document |
| `language` | string | en / te / hi / ta / kn |
| `season_id` | integer | Filter by admission season |
| `search` | string | Full-text search |
| `sort` | string | created_at / downloads / name / updated_at |
| `order` | string | asc / desc |
| `page` | integer | Page number |
| `page_size` | integer | Items per page (default: 24 grid / 50 list, max: 100) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../materials/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Material grid load | `<div id="material-grid">` | `hx-get=".../materials/?view=grid"` | `#material-grid` | `innerHTML` | `hx-trigger="load"` |
| Infinite scroll | Sentinel element at grid bottom | `hx-get=".../materials/?page={n+1}"` | `#material-grid` | `beforeend` | `hx-trigger="revealed"` |
| Category filter | Category tile click | `hx-get=".../materials/?category={cat}"` | `#material-grid` | `innerHTML` | `hx-trigger="click"` |
| Multi-filter apply | Filter dropdowns | `hx-get` with all filter params | `#material-grid` | `innerHTML` | `hx-trigger="change"` |
| Search | Search input | `hx-get=".../materials/?search={q}"` | `#material-grid` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| View toggle (grid/list) | Toggle buttons | `hx-get=".../materials/?view={mode}"` | `#material-content` | `innerHTML` | `hx-trigger="click"` |
| Sort change | Sort dropdown | `hx-get=".../materials/?sort={field}&order={dir}"` | `#material-grid` | `innerHTML` | `hx-trigger="change"` |
| Material detail drawer | Card / row click | `hx-get=".../materials/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Approve material | Approve button | `hx-patch=".../materials/{id}/status/" (body: status=published)` | `#approval-row-{id}` | `outerHTML` | Row removed from queue + toast |
| Reject material | Reject modal submit | `hx-patch=".../materials/{id}/status/" (body: status=rejected)` | `#approval-row-{id}` | `outerHTML` | Row removed + toast |
| Upload material | Upload form submit | `hx-post=".../materials/"` | `#upload-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Bulk upload | Bulk form submit | `hx-post=".../materials/bulk-upload/"` | `#bulk-upload-progress` | `innerHTML` | Progress polling |
| Branch copy generate | Generate form submit | `hx-post=".../materials/{id}/branch-copy/"` | `#branch-copy-result` | `innerHTML` | Returns download link |

---

## 14. File Storage & CDN

| Aspect | Implementation |
|---|---|
| Storage | Cloudflare R2 — bucket: `{group_slug}-marketing-materials` |
| Path structure | `/{group_id}/materials/{year}/{category}/{material_id}/{version}/{filename}` |
| Thumbnail generation | Server-side on upload: 240×180 crop for grid, 60×45 for list, 480×360 for preview |
| Video thumbnail | FFmpeg frame grab at 2-second mark |
| PDF thumbnail | First page rendered as PNG via pdf2image |
| CDN delivery | Cloudflare CDN with 24-hour cache; cache-busted on version update |
| Access control | Signed URLs with 1-hour expiry for downloads; public thumbnails |
| Max file sizes | Image: 50 MB · PDF: 50 MB · Video: 100 MB · Document: 20 MB · ZIP (bulk): 500 MB |
| Virus scan | ClamAV scan on upload; quarantine if infected; toast error to uploader |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
