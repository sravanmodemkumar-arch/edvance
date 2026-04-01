# L-06 — Brand Asset Library

**Route:** `GET /marketing/brand/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Brand Manager (#68), Marketing Manager (#64)
**Also sees:** SEO Exec (#65), Social Media Manager (#66), Performance Marketing Exec (#67) — read + download; Content Strategist (#99) — read + download; no access for Analyst (#98), Email Exec (#100)

---

## Purpose

Single source of truth for EduForge's brand identity across 7 domains (SSC · RRB · BOARD · INTERMEDIATE · COACHING · GROUPS · CORPORATE). At 2,050 institutions across diverse markets, brand consistency is a revenue signal — schools trust a polished identity; coaching owners need domain-specific assets that don't bleed into each other. The Brand Manager uploads, versions, and deprecates assets. All internal team members who create customer-facing materials download from here rather than maintaining local copies that drift out of date. Brand approval is the gate between upload and team visibility.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Asset grid | `mktg_brand_asset` WHERE is_deprecated=false AND approved_by_id IS NOT NULL | 30 min |
| Pending approval panel | `mktg_brand_asset` WHERE approved_by_id IS NULL | 5 min |
| Deprecated assets | `mktg_brand_asset` WHERE is_deprecated=true | 30 min |
| Asset version history | `mktg_brand_asset` WHERE is_current_version=false AND parent_asset_id = this asset | 30 min |
| Asset usage stats | `mktg_asset_download_log` GROUP BY asset_id for last 30 days | 60 min |

`?nocache=true` available to Brand Manager (#68) and Marketing Manager (#64).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?domain` | `ssc`, `rrb`, `board`, `intermediate`, `coaching`, `groups`, `corporate` | `all` | Active domain tab |
| `?type` | asset_type enum | `all` | Filter by asset type |
| `?q` | string ≥ 2 chars | — | Search on asset name |
| `?pending` | `1` | — | Show only pending approval assets (Brand Manager + Manager only) |
| `?deprecated` | `1` | — | Show deprecated assets archive |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/brand-asset-grid/` | Asset grid | Domain tab change + filter change | `#l-brand-grid` |
| `htmx/l/brand-pending/` | Pending approval panel | Page load; 5-min refresh | `#l-brand-pending` |
| `htmx/l/asset-detail/{id}/` | Asset detail drawer | Asset card click | `#l-asset-drawer` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  BRAND ASSET LIBRARY                                  [+ Upload Asset]  │
├─────────────────────────────────────────────────────────────────────────┤
│  DOMAIN TABS                                                            │
│  [All] [SSC] [RRB] [Board/School] [Intermediate] [Coaching] [Groups]   │
│  [Corporate EduForge]                                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  ASSET TYPE FILTER                                                      │
│  [All Types] [Logo] [Color Palette] [Typography] [Presentation]         │
│  [Social Template] [Banner] [Icon Set] [Photography] [Guidelines]       │
├─────────────────────────────────────────────────────────────────────────┤
│  [🔍 Search asset name...]                    [Pending Approval (2) ⚠]  │
├─────────────────────────────────────────────────────────────────────────┤
│  ASSET GRID (responsive card grid)                                      │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐      │
│  │ [thumb] │  │ [thumb] │  │ [thumb] │  │ [thumb] │  │ [thumb] │      │
│  │ SSC Logo│  │ SSC Color│  │ SSC Pres│  │ SSC Soc.│  │ SSC Icon│      │
│  │  v2.1   │  │ Palette │  │ Template│  │ Template│  │  Set    │      │
│  │ SVG/PNG │  │  PDF    │  │  PPTX  │  │  ZIP   │  │  ZIP   │      │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └─────────┘      │
├─────────────────────────────────────────────────────────────────────────┤
│  Showing 24 of 48 assets   [Load more]                                  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Domain Tabs

| Tab | Description |
|---|---|
| All | All assets across all domains |
| SSC | SSC CGL / CHSL / MTS brand — orange primary |
| RRB | RRB NTPC / Group D brand — blue primary |
| Board / School | CBSE / State Board school identity — green primary |
| Intermediate | Intermediate college exam brand — purple primary |
| Coaching | Coaching centre-facing brand — red-amber primary |
| Groups | Institution group-facing brand — slate primary |
| Corporate EduForge | Master brand — EduForge corporate identity used in B2B sales, investor comms, job postings |

Each domain has its own complete brand kit. A social post for SSC must use SSC assets — cross-domain mixing is a brand compliance failure.

---

## Asset Type Filter

Secondary filter row below domain tabs. Multi-select.

| Type | Icon | Description |
|---|---|---|
| LOGO | 🔵 | Primary logo, wordmark, icon-only variants |
| COLOR_PALETTE | 🎨 | Brand colour palette with HEX / RGB / CMYK codes |
| TYPOGRAPHY | Aa | Font files + usage guidelines |
| PRESENTATION_TEMPLATE | 📊 | PowerPoint / Google Slides templates for sales and EBR presentations |
| SOCIAL_TEMPLATE | 📱 | Sized Canva / Figma templates for Instagram, YouTube thumbnails, Twitter headers |
| BANNER_TEMPLATE | 🖼 | Web banners (Google Display sizes), email headers |
| ICON_SET | ✦ | Subject / feature icons for use in platform UI, presentations |
| PHOTOGRAPHY | 📷 | Approved stock / in-house photography per domain |
| BRAND_GUIDELINES | 📄 | Full brand usage PDF per domain |

---

## Asset Card

Each asset in the grid is a card:

```
┌───────────────────────────────────────┐
│                                       │
│         [Asset Thumbnail or           │
│          Icon Preview for PDF/PPTX]   │
│                                       │
├───────────────────────────────────────┤
│  SSC Logo — Primary                   │
│  Version 2.1 · SVG + PNG             │
│  Approved by Vandana M.               │
│  12 downloads (30d)                   │
├───────────────────────────────────────┤
│  [Download ↓]  [···]                  │
└───────────────────────────────────────┘
```

- **[Download ↓]:** Opens format selector (if multiple formats available: PNG/SVG/PDF). Downloads from Cloudflare R2 signed URL (TTL 60 seconds). Logs to `mktg_asset_download_log`.
- **[···] Context menu:** [View Details] [New Version] [Deprecate] [Delete] — visibility depends on role
- **Deprecated assets:** Greyed out card with orange "DEPRECATED" banner. Not shown by default (need `?deprecated=1`).
- **Pending approval:** Card has amber "PENDING APPROVAL" banner. Only visible to Brand Manager + Marketing Manager.

---

## Asset Detail Drawer

Slides in from the right on card click.

```
┌──────────────────────────────────────────────────────────────────┐
│  SSC Logo — Primary                                  [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Domain: SSC · Type: LOGO · Version: 2.1                         │
│  Formats: SVG · PNG (1200px) · PNG (400px)                       │
│  File size: 48 KB (SVG)                                          │
│  Uploaded by: Vandana M. (Brand Manager)  ·  15 Mar 2026         │
│  Approved by: Vandana M. + Marketing Manager  ·  16 Mar 2026     │
├──────────────────────────────────────────────────────────────────┤
│  [Asset preview — large]                                         │
│                                                                  │
│  Usage note:                                                     │
│  "Use only on white or SSC-orange (#E8521A) backgrounds.         │
│   Minimum size: 40px height. Do not distort or recolour."        │
├──────────────────────────────────────────────────────────────────┤
│  VERSION HISTORY                                                 │
│  v2.1  Current  ·  15 Mar 2026  (this file)                      │
│  v2.0  Deprecated  ·  01 Feb 2026  [Download v2.0]              │
│  v1.0  Deprecated  ·  12 Sep 2025  [Download v1.0]              │
├──────────────────────────────────────────────────────────────────┤
│  DOWNLOAD                                                        │
│  [SVG]  [PNG 1200px]  [PNG 400px]                                │
├──────────────────────────────────────────────────────────────────┤
│  Brand Manager / Manager actions:                                │
│  [Upload New Version]  [Deprecate This Asset]                    │
└──────────────────────────────────────────────────────────────────┘
```

**Version history:** Old versions retained in R2 and accessible to download. `is_current_version = false` for previous versions. Previous versions are not shown in the main grid — only accessible from the current asset's drawer.

**`mktg_brand_asset.parent_asset_id`:** FK back to the original asset ID when a new version is uploaded, forming a version chain.

---

## Upload Asset Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Upload Brand Asset                                  [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Asset name*       [SSC Logo — Primary                      ]    │
│  Domain*           [SSC                                   ▼]     │
│  Asset type*       [Logo                                  ▼]     │
│  File format*      [SVG                                   ▼]     │
│                                                                  │
│  Upload file*      [🖼 Drop file here or click to browse    ]    │
│                    Accepted: PNG, SVG, PDF, PPTX, FIGMA, ZIP    │
│                    Max size: 50MB                                │
│                                                                  │
│  Additional format (optional)                                   │
│  [Upload PNG export for teams without SVG tools          ]      │
│                                                                  │
│  Version*          [2.1                                     ]    │
│  Is this a new version of an existing asset?                    │
│  [Yes — link to existing asset: _____________ ▼]                │
│                                                                  │
│  Usage notes       [Optional — max 500 chars                ]    │
│                                                                  │
│  [Cancel]                              [Upload for Approval]     │
└──────────────────────────────────────────────────────────────────┘
```

POST to `/marketing/brand/upload/`. File uploaded directly to Cloudflare R2 via pre-signed POST URL. `mktg_brand_asset` row created with `approved_by_id = NULL`.

**Approval flow after upload:**
1. Brand Manager uploads → status visible to Brand Manager + Marketing Manager as PENDING
2. Brand Manager self-approves OR Marketing Manager approves → `approved_by_id` set → asset visible to all permitted roles
3. Brand Manager can approve their own uploads for day-to-day assets; Marketing Manager approval required for domain Brand Guidelines PDFs and presentation templates

---

## Pending Approval Panel

Visible to Brand Manager (#68) and Marketing Manager (#64). Shown as an alert badge [Pending Approval (2) ⚠] in the filter row.

```
┌──────────────────────────────────────────────────────────────────┐
│  PENDING APPROVAL (2 assets)                                     │
│                                                                  │
│  SSC Brand Kit v2.1  (uploaded by Vandana M., 5h ago)           │
│  [Preview]  [Approve]  [Request Changes]                         │
│                                                                  │
│  RRB Social Templates — Instagram Set  (uploaded 1d ago)        │
│  [Preview]  [Approve]  [Request Changes]                         │
└──────────────────────────────────────────────────────────────────┘
```

**[Approve]:** PATCH `/marketing/brand/{id}/approve/`. Sets `approved_by_id`. Asset becomes visible to all permitted roles.

**[Request Changes]:** Opens comment input. Comment stored in `mktg_asset_review_note`. Notification sent to uploader.

---

## Deprecation

**[Deprecate This Asset]:** Opens dialog:

```
Deprecate "SSC Logo v1.0"?
Deprecation reason: [__________________________]
This asset will be hidden from the main library.
Team members who downloaded it will not be notified.
[Cancel]  [Deprecate]
```

PATCH `/marketing/brand/{id}/deprecate/`. Sets `is_deprecated=true`, `deprecation_reason`. Asset remains in R2 and accessible via version history but hidden from the main grid.

---

## Asset Download Log

`mktg_asset_download_log` tracks all downloads for usage analytics.

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| asset_id | FK mktg_brand_asset | ON DELETE CASCADE |
| downloaded_by_id | FK auth_user | |
| downloaded_at | timestamptz | NOT NULL DEFAULT now() |
| format | varchar(10) | Which format was downloaded (PNG / SVG / etc.) |

---

## Role-Based UI

| Element | 64 Manager | 65 SEO Exec | 66 Social | 67 Perf. Mktg | 68 Brand Mgr | 99 Content Strat. |
|---|---|---|---|---|---|---|
| View approved assets | Yes | Yes | Yes | Yes | Yes | Yes |
| Download assets | Yes | Yes | Yes | Yes | Yes | Yes |
| Upload assets | Yes | No | No | No | Yes | No |
| Approve assets | Yes | No | No | No | Yes (own) | No |
| Deprecate assets | Yes | No | No | No | Yes | No |
| View pending approval | Yes | No | No | No | Yes | No |
| View version history | Yes | Yes | Yes | Yes | Yes | Yes |
| Download old versions | Yes | Yes | Yes | Yes | Yes | Yes |
| View download stats | Yes | No | No | No | Yes | No |

---

## Empty States

| Condition | Message |
|---|---|
| No assets for selected domain | "No brand assets uploaded for this domain yet. [+ Upload Asset]" |
| No assets match filter | "No assets match your search." |
| No pending approvals | "No assets pending approval." |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

**Toasts on this page:** asset uploaded, asset approved, asset rejected (with note), asset deprecated, asset restored, version uploaded, download logged, bulk download started, brand non-compliance flagged — see L-00 §2.

**Skeleton states:** Asset grid tiles shimmer during initial load and filter change. Pending Approval panel shows 3 skeleton cards during HTMX load. Version History list shows shimmer rows.

**Download URL expiry:** R2 signed GET URLs expire after 60 seconds. If a user clicks [Download] and the pre-signed URL has expired (e.g., slow connection), the server issues a fresh URL on demand — the download link calls `/marketing/brand/assets/{id}/download-url/` which returns a new 60-second URL and immediately redirects. No stale URL is ever surfaced in the browser.

**Figma export failure:** If Figma API export fails during "Import from Figma" (L-05 or L-06 use cases), inline error inside the upload drawer: "Figma export failed — the file may have been moved or access revoked. Try downloading from Figma and uploading directly." No toast (error stays in drawer until dismissed).

**Version upload conflict:** If two Brand Managers upload a new version of the same asset simultaneously, optimistic lock on `mktg_brand_asset.updated_at` — second upload receives: ERROR toast "This asset was updated by another user. Please refresh and try again."

---

## Missing Spec Closes (Audit)

**Asset type approval matrix (full):**

| Asset Type | Who Can Approve |
|---|---|
| LOGO | Brand Manager (#68) |
| COLOUR_PALETTE | Brand Manager (#68) |
| TYPOGRAPHY_GUIDE | Brand Manager (#68) |
| ICON_SET | Brand Manager (#68) |
| SOCIAL_TEMPLATE | Brand Manager (#68) |
| EMAIL_TEMPLATE | Brand Manager (#68) |
| AD_BANNER | Brand Manager (#68) |
| PRESENTATION_TEMPLATE | Marketing Manager (#64) only |
| BRAND_GUIDELINES | Marketing Manager (#64) only |
| VIDEO_INTRO_OUTRO | Brand Manager (#68) |

For PRESENTATION_TEMPLATE and BRAND_GUIDELINES: Brand Manager sees the asset but [Approve] button is disabled with tooltip "Approval requires Marketing Manager."

**Version comparison spec:**
Brand Manager can select two versions from the Version History list → [Compare Versions] opens a side-by-side modal:
- Image assets: left panel = older version, right panel = newer version, with pixel-diff overlay toggle
- Document / template assets: diff shown as field-level change list (metadata only — no full content diff)
- Version comparison modal route: `GET /marketing/brand/assets/{id}/compare/?v1={version_number}&v2={version_number}`

**Bulk download:**
Select multiple assets via grid checkboxes → [Download Selected] button appears in grid header.
- Server zips selected files (R2 keys) into a temporary archive with 10-minute expiry
- POST to `/marketing/brand/assets/bulk-download/` → returns presigned R2 URL for zip file
- Max 50 assets per bulk download; if > 50 selected, WARNING toast "Maximum 50 assets per download. First 50 selected will be downloaded."
- Zip filename: `eduforge_brand_assets_{domain}_{YYYY-MM-DD}.zip`

**`mktg_asset_review_note` usage in UI:**
When Brand Manager submits [Reject], opens inline form:
```
┌──────────────────────────────────────────────┐
│  Reject Asset                     [Close ×]  │
│  Reason for rejection*                        │
│  [Enter compliance issue or revision note ]  │
│  [Cancel]                       [Reject]      │
└──────────────────────────────────────────────┘
```
POST to `/marketing/brand/assets/{id}/reject/` with `note` field.
Creates row in `mktg_asset_review_note` with `action='REJECTED'` and `note` text.
Notification to asset uploader: email + in-app: "Your asset '{name}' was rejected by Brand Manager: {note}. Please upload a revised version."

**Deprecation flow (full spec):**
[Deprecate] available to Brand Manager + Marketing Manager for APPROVED assets.
→ Confirmation dialog: "Deprecate '{name}'? Users will be warned this asset is outdated but can still download it."
→ PATCH `/marketing/brand/assets/{id}/deprecate/` → sets `status = 'DEPRECATED'`
→ Asset card shows amber "DEPRECATED" banner overlay
→ Download still allowed but warning dialog: "This asset is deprecated. A newer version may be available. [View Latest Version →] [Download Anyway]"
→ Notification to all users who downloaded this asset in the last 90 days (from `mktg_asset_download_log`): in-app only: "Brand asset '{name}' has been deprecated. Please use the updated version."

**`mktg_asset_download_log` schema:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| asset_id | FK mktg_brand_asset | ON DELETE SET NULL |
| asset_version | varchar(20) | Snapshot of version at download time |
| downloaded_by_id | FK auth_user | |
| downloaded_at | timestamptz | NOT NULL DEFAULT now() |
| format | varchar(20) | e.g., `PNG`, `PDF`, `SVG`, `FIGMA_EXPORT` |
| ip_address | inet | For audit only; never surfaced in UI |

Download stats visible to Brand Manager + Marketing Manager only (role-based — see Role-Based UI table).

**Asset search full spec:**
- Search bar: ILIKE on `mktg_brand_asset.name` + `mktg_brand_asset.tags` (jsonb array, cast to text)
- Debounce: 300ms; min 2 chars
- Results update asset grid via HTMX partial (`htmx/l/brand-asset-grid/`)
- No separate search results page — grid updates in place

**Asset tagging:**
Upload drawer includes optional Tags field: comma-separated free-text tags stored as jsonb array in `mktg_brand_asset.tags`. Brand Manager can edit tags on existing assets via Asset Detail Drawer → [Edit Tags] inline input.

**`mktg_brand_asset` table full schema reference:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| asset_type | varchar(30) | See approval matrix above |
| domain | varchar(20) | Exam domain enum OR `CORPORATE` |
| file_r2_key | varchar(1000) | NOT NULL |
| file_format | varchar(20) | `PNG`, `SVG`, `PDF`, `MP4`, `FIGMA`, etc. |
| version | varchar(20) | DEFAULT `1.0`; increment on new version upload |
| status | varchar(20) | `PENDING` · `APPROVED` · `REJECTED` · `DEPRECATED` |
| approved_by_id | FK auth_user | NULL until approved |
| approved_at | timestamptz | |
| uploaded_by_id | FK auth_user | NOT NULL |
| uploaded_at | timestamptz | NOT NULL DEFAULT now() |
| updated_at | timestamptz | NOT NULL DEFAULT now() |
| tags | jsonb | Array of string tags |
| figma_file_id | varchar(200) | If asset originated from Figma |
| figma_node_id | varchar(200) | Figma frame/component node |
| description | text | Optional notes from uploader |

**Domain tab counts:**
Each domain tab badge shows count of APPROVED assets for that domain only (excludes PENDING/DEPRECATED). Pending count shown separately in the Pending Approval panel badge.

**Figma-originated assets:**
If `figma_file_id` is populated, Asset Detail Drawer shows a "Figma source" badge with a [Open in Figma ↗] link (deep link to Figma using `figma_file_id` + `figma_node_id`). Format: `https://www.figma.com/file/{file_id}?node-id={node_id}`.

**Bulk approval (Manager only):**
Marketing Manager can select multiple PENDING assets → [Approve Selected] bulk action.
→ Confirmation: "Approve {N} assets?"
→ POST `/marketing/brand/assets/bulk-approve/` with list of asset IDs
→ Each asset status set to APPROVED; uploader notified for each
→ SUCCESS toast: "{N} assets approved."
