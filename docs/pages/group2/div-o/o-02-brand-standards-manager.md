# O-02 — Brand Standards & Guidelines

> **URL:** `/group/marketing/brand/standards/`
> **File:** `o-02-brand-standards-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary editor; G4/G5 approves

---

## 1. Purpose

The Brand Standards & Guidelines page is the single source of truth for the group's visual identity across all branches. In a large education group with 20–50 branches spread across multiple districts or states, brand consistency is a constant battle. Every branch principal wants to print their own flex banners, every local coordinator designs their own admission pamphlet in a neighbourhood printing shop, and the result is 50 different versions of the group's logo — wrong colours, wrong fonts, stretched images, misspelt taglines.

This page solves that problem by providing a centralised, version-controlled brand asset library with strict guidelines that every branch must follow. It covers: logo usage (primary, secondary, monochrome, minimum size), colour palette (primary, secondary, accent — with exact hex/RGB/CMYK values), typography (heading font, body font, sizes), signage specifications (gate board dimensions, classroom nameplate specs, bus branding template), stationery templates (letterhead, visiting card, ID card), and digital templates (social media post sizes, email signatures, WhatsApp display picture).

For a group like Narayana with 300+ branches or Sri Chaitanya with 200+, this page is used daily by the Content Coordinator (Role 131) to upload approved assets and by branch-level staff to download correct versions. The platform enforces that only approved assets are available for download — no branch can upload their own modified version.

**Scale:** 5–50 branches · 20–100 brand assets · 5–15 signage types · Updated 2–4 times per year (major revisions)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Marketing Director | 114 | G0 | No Platform Access | Approves brand guidelines externally |
| Group Brand Manager | 115 | G0 | No Platform Access | Creates guidelines in external tools (Adobe, Canva) |
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — upload, edit, version, archive assets | Primary platform editor |
| Group Admissions Campaign Manager | 119 | G3 | Read + Download | Can download assets; cannot modify |
| Group Topper Relations Manager | 120 | G3 | Read + Download | Can download for topper campaigns |
| Group Admission Telecaller Executive | 130 | G3 | No access | Not relevant to telecalling |
| Group Admission Data Analyst | 132 | G1 | Read only | View guidelines; no download |
| Branch Principal | — | G3 | Read + Download | Downloads approved assets for local use |
| Branch IT Admin | — | G3 | Read + Download | Downloads for portal/digital use |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Upload/edit restricted to `role_id IN (131)` or `level >= G4`. Download requires `level >= G2` or branch staff with `brand_download` permission.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Brand & Content  ›  Brand Standards & Guidelines
```

### 3.2 Page Header
```
Brand Standards & Guidelines                    [Upload Asset]  [Version History]  [Download Brand Kit]
Content Coordinator — Meena Raghavan
Sunrise Education Group · Last updated: 14-Feb-2026 · Version: 3.2
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Brand guidelines updated in last 7 days | "Brand guidelines updated on [Date] — Version [X]. All branches must download updated assets." | Info (blue) |
| Any branch failed brand compliance audit (O-05) | "[N] branch(es) have brand compliance issues. Review Brand Compliance Audit." | Medium (yellow) |
| Logo file format updated | "Primary logo updated — all previous versions are deprecated. Download new files immediately." | High (amber) |

---

## 4. KPI Summary Bar (5 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Brand Assets | Integer | COUNT(brand_assets) WHERE status = 'active' | Static blue | `#kpi-total-assets` |
| 2 | Current Version | Text | Latest brand_guideline_version | Static blue | `#kpi-version` |
| 3 | Last Updated | Date | MAX(updated_at) from brand_assets | Amber if > 6 months ago | `#kpi-last-updated` |
| 4 | Branch Downloads (This Month) | Integer | COUNT(downloads) WHERE month = current | Static green | `#kpi-downloads` |
| 5 | Compliance Score | Percentage | AVG(branch_brand_compliance_score) across all branches | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-compliance` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/brand/standards/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Logo Usage Guidelines

Displays all approved logo variants with usage rules.

**Logo Variants Table:**

| Column | Type | Notes |
|---|---|---|
| Variant | Text | Primary, Secondary, Monochrome, Favicon, Square (Social), Watermark |
| Preview | Image thumbnail (120px) | Visual preview of the logo |
| Format | Badges | PNG, SVG, PDF, AI (multiple formats per variant) |
| Min Size | Text | Minimum pixel/mm dimensions for this variant |
| Background | Badge | Light BG Only / Dark BG Only / Transparent / Any |
| Usage Notes | Text | Where and how this variant should be used |
| Download | Button group | Individual format buttons: [PNG] [SVG] [PDF] [AI] |

**Usage Rules Panel (expandable):**

| Rule | Description |
|---|---|
| Clear Space | Minimum clear space around logo = 50% of logo height on all sides |
| Minimum Size | Print: 25mm width · Screen: 80px width · Below this, use favicon variant |
| Do Not | Stretch, rotate, add shadows, change colours, place on busy backgrounds, add outlines |
| Co-branding | When appearing with partner logos, group logo must be equal or larger size |
| Branch Name | Branch name appears below logo in specified font, never inside the logo |

### 5.2 Colour Palette

**Primary Colours Table:**

| Column | Type | Notes |
|---|---|---|
| Colour Name | Text | e.g., "Sunrise Blue", "Trust Gold", "Scholar White" |
| Swatch | Colour box (48×48px) | Visual colour preview |
| Hex | Text | e.g., `#1E40AF` |
| RGB | Text | e.g., `30, 64, 175` |
| CMYK | Text | e.g., `83, 63, 0, 31` (for print) |
| Pantone | Text | e.g., `PMS 2728 C` (for signage/printing vendors) |
| Usage | Text | "Primary brand colour — headers, buttons, signage backgrounds" |

**Colour Categories:**
- **Primary Colours** (2–3): Main brand colours used in logos, headers, CTAs
- **Secondary Colours** (2–3): Supporting colours for backgrounds, cards, dividers
- **Accent Colours** (1–2): Highlights, badges, alerts
- **Neutral Colours** (3–4): Text, backgrounds, borders — grey scale
- **Stream Colours** (4–6): MPC = blue, BiPC = green, MEC = amber, CEC = purple, HEC = teal, Foundation = orange

### 5.3 Typography

**Font Specifications Table:**

| Column | Type | Notes |
|---|---|---|
| Usage | Text | Heading / Subheading / Body / Caption / Button |
| Font Family | Text | e.g., "Poppins", "Noto Sans", "Roboto" |
| Weight | Text | Bold (700) / Semibold (600) / Regular (400) / Light (300) |
| Size (Web) | Text | e.g., 32px / 24px / 16px / 12px / 14px |
| Size (Print) | Text | e.g., 28pt / 20pt / 12pt / 9pt / 11pt |
| Line Height | Text | e.g., 1.3 / 1.4 / 1.6 / 1.5 / 1.4 |
| Colour | Hex ref | References colour palette above |
| Sample | Rendered text | "The quick brown fox…" in specified style |

**Font Files Section:**
- Download links for all font files (.ttf, .woff2, .otf)
- Google Fonts links (if applicable)
- Telugu/Hindi font specifications for regional materials

### 5.4 Signage Specifications

**Signage Types Table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Signage Type | Text | Yes | e.g., "Main Gate Board", "Classroom Nameplate", "Bus Side Panel" |
| Dimensions | Text | Yes | Width × Height in feet/inches or mm |
| Material | Text | No | ACP, Flex, Vinyl, Acrylic, LED backlit |
| Template | Download button | No | Downloads approved template file (AI/PSD/PDF) |
| Placement Photo | Thumbnail | No | Reference photo showing correct installation |
| Specifications | Expandable | No | Detailed specs: font sizes, logo position, colour codes, mounting instructions |
| Last Updated | Date | Yes | When this template was last revised |

**Signage Types Covered:**

| Type | Details |
|---|---|
| Main Gate Board | Group logo + Branch name + Affiliations (CBSE/ICSE) + Contact |
| Building Facade Banner | Large flex/ACP — building front branding |
| Classroom Door Nameplate | Class + Section + Teacher name |
| Staff Room Nameplate | Department name |
| Corridor Direction Signs | Arrows + Room names |
| Bus Side Panel | Both sides — logo + name + helpline number |
| Bus Rear Panel | Logo + tagline + admission helpline |
| Auto-Rickshaw Back Panel | Smaller format — logo + branch + phone |
| Hoarding (20×10 ft) | Outdoor advertising — admission campaign template |
| Hoarding (30×15 ft) | Highway/main road — larger format |
| Flex Banner (3×6 ft) | Indoor/outdoor event banners |
| Standee (6×2.5 ft) | Reception area / event standees |
| Pamphlet (A5) | Admission pamphlet — front + back template |
| Brochure (A4 tri-fold) | Detailed brochure template |

### 5.5 Stationery Templates

**Stationery Items:**

| Item | Template Format | Download | Notes |
|---|---|---|---|
| Letterhead (A4) | PDF + DOCX | [Download] | Group letterhead — branch name variable |
| Visiting Card | AI + PDF | [Download] | Standard layout — name, designation, branch, contact |
| Student ID Card | AI + PDF | [Download] | Front: photo, name, class, blood group. Back: school address, emergency contact |
| Staff ID Card | AI + PDF | [Download] | Front: photo, name, designation, employee ID. Back: school address |
| Fee Receipt | PDF | [Download] | Standardised receipt format across branches |
| Transfer Certificate | PDF | [Download] | TC template with group branding |
| Envelope (DL) | AI + PDF | [Download] | Standard envelope with logo + address |
| Envelope (A4) | AI + PDF | [Download] | Large envelope for certificates |
| Certificate Template | AI + PDF | [Download] | Achievement / participation / merit certificate |
| Attendance Register Cover | PDF | [Download] | Branded cover for physical registers |

### 5.6 Digital Templates

**Digital Asset Specifications:**

| Asset | Dimensions | Format | Usage |
|---|---|---|---|
| WhatsApp Display Picture | 640×640 px | PNG | Group/branch WhatsApp Business profile |
| WhatsApp Status | 1080×1920 px | PNG/JPG | Admission campaign status images |
| Instagram Post (Square) | 1080×1080 px | PNG/JPG | Feed posts |
| Instagram Story | 1080×1920 px | PNG/JPG | Stories / Reels cover |
| Facebook Cover | 820×312 px | PNG/JPG | Page cover photo |
| YouTube Thumbnail | 1280×720 px | PNG/JPG | Video thumbnails |
| Email Signature | 600×200 px | HTML + PNG | Staff email signatures |
| Website Banner | 1920×600 px | PNG/JPG | Homepage hero banner |
| Google My Business | 720×720 px | PNG/JPG | GMB profile + cover |
| Newspaper Ad (Quarter Page) | 13cm × 20cm | PDF (300 DPI) | Standard newspaper ad size |
| Newspaper Ad (Half Page) | 26cm × 20cm | PDF (300 DPI) | Half-page format |
| Newspaper Ad (Full Page) | 26cm × 40cm | PDF (300 DPI) | Full-page format |

Each row has a [Download Template] button providing the blank template with brand elements pre-placed.

---

## 6. Drawers & Modals

### 6.1 Modal: `upload-asset` (560px)
- **Title:** "Upload Brand Asset"
- **Fields:**
  - Asset name (text, required)
  - Category (dropdown): Logo / Colour / Typography / Signage / Stationery / Digital / Other
  - Sub-category (dropdown, dependent on category)
  - File upload (drag-and-drop, max 50 MB per file, multiple files allowed)
  - Accepted formats: PNG, SVG, PDF, AI, PSD, DOCX, XLSX, TTF, WOFF2, OTF, MP4
  - Version number (auto-incremented, editable)
  - Description / usage notes (textarea)
  - Replace existing asset (toggle — if ON, select asset to replace from dropdown)
  - Notify all branches (toggle — sends notification that asset was updated)
- **Buttons:** Cancel · Upload
- **Access:** Role 131 (G2) or G4/G5 only
- **Behaviour:** POST to `/api/v1/group/{id}/marketing/brand/assets/` → uploads to Cloudflare R2 → toast "Asset uploaded successfully"

### 6.2 Modal: `version-history` (640px)
- **Title:** "Brand Guidelines — Version History"
- **Columns:** Version · Date · Updated By · Changes Summary · Download
- **Rows:** All previous versions, newest first
- **Each row:** Download link to download the full brand kit as it was at that version
- **Behaviour:** GET `/api/v1/group/{id}/marketing/brand/versions/`

### 6.3 Drawer: `asset-detail` (640px, right-slide)
Opens when clicking any asset row.
- **Tabs:** Preview · Details · Download History · Notes
- **Preview tab:** Full-size preview of the asset (image render for PNG/SVG; PDF viewer for PDF; file icon for others)
- **Details tab:** Name, category, version, uploaded by, upload date, file size, format, dimensions (if image), usage notes
- **Download History tab:** Table of all downloads — user, branch, date, format downloaded
- **Notes tab:** Internal notes (editable by G2+; read-only for others)
- **Footer:** [Download] [Replace] [Archive] buttons (Replace and Archive: G2+ only)

### 6.4 Modal: `download-brand-kit` (480px)
- **Title:** "Download Complete Brand Kit"
- **Description:** "Download all current brand assets as a single ZIP file."
- **Options:**
  - Include all categories (default) OR select specific: Logo / Colours / Typography / Signage / Stationery / Digital
  - Include brand guidelines PDF (toggle, default ON)
  - Include font files (toggle, default ON)
- **Buttons:** Cancel · Download ZIP
- **Behaviour:** POST → generates ZIP asynchronously → download link via toast

---

## 7. Charts

### 7.1 Asset Downloads by Branch (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Brand Asset Downloads — Last 30 Days by Branch" |
| Data | Download count per branch |
| X-axis | Count |
| Y-axis | Branch name |
| Colour | `#3B82F6` (blue) uniform |
| Tooltip | "[Branch]: [N] downloads in last 30 days" |
| API endpoint | `GET /api/v1/group/{id}/marketing/brand/analytics/downloads-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-downloads-branch"` |
| Export | PNG |

### 7.2 Downloads by Category (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Downloads by Asset Category — Last 30 Days" |
| Data | Download count per category |
| Segments | Logo / Signage / Stationery / Digital / Typography / Other |
| Colour | Distinct palette per category |
| Tooltip | "[Category]: [N] downloads ([X]%)" |
| API endpoint | `GET /api/v1/group/{id}/marketing/brand/analytics/downloads-by-category/` |
| HTMX | `hx-get` on load → `hx-target="#chart-downloads-category"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Asset uploaded | "Brand asset '[Name]' uploaded successfully — Version [X]" | Success | 3s |
| Asset replaced | "Asset '[Name]' updated to Version [X]. Previous version archived." | Success | 4s |
| Asset archived | "Asset '[Name]' archived. No longer available for download." | Info | 3s |
| Brand kit download started | "Generating brand kit ZIP — download will start shortly" | Info | 3s |
| Brand kit ready | "Brand kit ready. Click to download (size: [X] MB)" | Success | 8s |
| Branch notification sent | "All branches notified about brand guidelines update" | Success | 3s |
| Upload failed (size limit) | "File exceeds 50 MB limit. Compress and retry." | Error | 5s |
| Upload failed (format) | "Unsupported file format. Accepted: PNG, SVG, PDF, AI, PSD, DOCX, TTF, WOFF2" | Error | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No brand assets uploaded | 🎨 | "No Brand Assets Yet" | "Upload your group's logo, colour palette, and templates to get started." | Upload First Asset |
| No signage templates | 🪧 | "No Signage Templates" | "Upload signage specifications so branches can order correct signboards." | Upload Signage Template |
| No digital templates | 📱 | "No Digital Templates" | "Add social media and digital ad templates for consistent online branding." | Upload Digital Template |
| No downloads recorded | 📥 | "No Downloads Yet" | "Downloads will be tracked here once branches start using brand assets." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: 5 KPI shimmer cards + section placeholders |
| Logo section load | 6 image placeholder rectangles (120px) with grey shimmer |
| Colour palette load | 8 colour swatch placeholders (48×48) |
| Signage table load | Table skeleton: 5 shimmer rows |
| Asset detail drawer | Right-slide skeleton with image placeholder + 3 tabs |
| File upload | Progress bar inside modal: "Uploading… [X]%" |
| Brand kit generation | Modal: progress bar "Generating ZIP… [X]%" |
| Chart load | Chart placeholder with grey canvas |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/brand/standards/` | G1+ | Full brand standards page data |
| GET | `/api/v1/group/{id}/marketing/brand/standards/kpis/` | G1+ | KPI card values |
| GET | `/api/v1/group/{id}/marketing/brand/assets/` | G1+ | List all active brand assets |
| GET | `/api/v1/group/{id}/marketing/brand/assets/{asset_id}/` | G1+ | Single asset detail |
| POST | `/api/v1/group/{id}/marketing/brand/assets/` | G2+ | Upload new asset |
| PUT | `/api/v1/group/{id}/marketing/brand/assets/{asset_id}/` | G2+ | Replace/update asset |
| DELETE | `/api/v1/group/{id}/marketing/brand/assets/{asset_id}/` | G4+ | Archive asset (soft delete) |
| GET | `/api/v1/group/{id}/marketing/brand/assets/{asset_id}/download/` | G2+ | Download asset file |
| GET | `/api/v1/group/{id}/marketing/brand/versions/` | G1+ | Version history list |
| POST | `/api/v1/group/{id}/marketing/brand/kit/download/` | G2+ | Generate brand kit ZIP |
| GET | `/api/v1/group/{id}/marketing/brand/analytics/downloads-by-branch/` | G1+ | Download analytics by branch |
| GET | `/api/v1/group/{id}/marketing/brand/analytics/downloads-by-category/` | G1+ | Download analytics by category |

### Query Parameters — Asset List

| Parameter | Type | Description |
|---|---|---|
| `category` | string | Filter: logo, colour, typography, signage, stationery, digital |
| `format` | string | Filter by file format: png, svg, pdf, ai, docx |
| `search` | string | Full-text search on asset name and description |
| `sort` | string | name, category, updated_at, downloads (default: updated_at) |
| `order` | string | asc / desc (default: desc) |

---

## 12. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../brand/standards/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Asset list load | `<div id="asset-sections">` | `hx-get=".../brand/assets/?category=all"` | `#asset-sections` | `innerHTML` | `hx-trigger="load"` |
| Category filter | Category tab buttons | `hx-get=".../brand/assets/?category={cat}"` | `#asset-sections` | `innerHTML` | `hx-trigger="click"` |
| Asset detail drawer | Asset row click | `hx-get=".../brand/assets/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Upload asset | Upload form submit | `hx-post=".../brand/assets/"` | `#upload-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Download asset | Download button click | `hx-get=".../brand/assets/{id}/download/"` | — | — | Direct download (no HTMX swap) |
| Search assets | Search input | `hx-get=".../brand/assets/?search={q}"` | `#asset-sections` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
