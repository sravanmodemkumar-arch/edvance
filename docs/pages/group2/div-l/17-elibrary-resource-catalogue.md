# 17 — E-Library Resource Catalogue

> **URL:** `/group/library/catalogue/`
> **File:** `17-elibrary-resource-catalogue.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Library Head (Role 101, G2) — full access

---

## 1. Purpose

Full catalogue management page for the central group e-library. The Library Head curates the complete digital resource library across all branches — adding, editing, classifying, archiving, and versioning resources. Resources are stored in Cloudflare R2 (PDFs, EPUB, DOCX, ZIP, MP4) or linked externally (YouTube, Google Drive, or any URL). Students and staff at branches access resources through their branch portals; this page is the administrative back-end from which the Library Head controls the entire catalogue.

Scale: 500–10,000 resources across 20–50 branches.

**Resource Types supported:**

| Type | Delivery | Notes |
|---|---|---|
| E-Book | File (PDF / EPUB) | Standard text resource |
| Video Lecture | File (MP4) or External URL (YouTube) | Duration shown in metadata |
| Question Bank | File (PDF / DOCX) | Tagged by subject + exam relevance |
| Past Paper | File (PDF) | Tagged by year + board |
| Reference Material | File or URL | Encyclopaedias, references |
| Revision Notes | File (PDF / DOCX) | Concise summaries |
| Worksheet | File (PDF / DOCX / ZIP) | Printable or fillable |
| Audio Lecture | File (MP3 / M4A) | Podcast-style lectures |
| Image / Diagram Set | File (ZIP of images) | Science diagrams, maps |
| Interactive Content | External URL | H5P, Genially, Google Sites |

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Library Head | G2 | Full — create, edit, classify, distribute, archive, restore versions, export | Primary owner; all branches |
| All other Group roles | — | No access to this page | Resources surfaced via branch portal |

> **Access enforcement:** `@require_role('group_library_head')` on all views and API endpoints for this page.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Library  ›  E-Library Resource Catalogue
```

### 3.2 Page Header
- **Title:** `E-Library Resource Catalogue`
- **Subtitle:** Stats Bar (see note below — replaces KPI cards)
- **Right controls:** `+ Add Resource` · `Bulk Import` · `Advanced Filters` · `Export List ↓`

> **Stats Bar** — Four inline non-clickable metrics displayed in a single row directly below the page title:
>
> | Metric | Label | Notes |
> |---|---|---|
> | Total Resources | All resources in catalogue (all statuses) | Plain number |
> | Active | Status = Active | Green text |
> | Archived | Status = Archived | Grey text |
> | Added This Month | Created in current calendar month | Blue text |
>
> Rendered as: `Total Resources: 4,821 · Active: 4,102 · Archived: 689 · Added This Month: 43`
> HTMX-loaded on page load; no colour thresholds; all non-clickable.

### 3.3 Alert Banners

| Condition | Banner Text | Severity |
|---|---|---|
| Resources pending review (Draft) > 20 | "[N] resources are in Draft status and have not been distributed to any branch. Review and publish or archive." | Amber |
| Storage approaching 80 % of R2 quota | "R2 storage usage is at [X]%. Consider archiving unused resources or contacting support to increase quota." | Amber |
| Bulk import job completed | "Bulk import completed: [N] resources added, [E] errors. View import log." | Info (dismissible) |
| Bulk import job failed | "Bulk import failed. [E] rows had errors. Download error report to review." | Red (dismissible) |
| Resource expiry (access expiry within 7 days) | "[N] distribution assignments expire within 7 days. Review and renew on the Distribution page." | Amber |

---

## 4. KPI Summary Bar

> **Note:** This page intentionally omits a KPI summary bar with cards. The Library Head Dashboard (page 05) hosts KPI cards for the library. Instead, a compact inline Stats Bar appears directly below the page title as described in section 3.2 above. HTMX refreshes the Stats Bar numbers whenever a resource is added, edited, archived, or restored.

---

## 5. Sections

### 5.1 Resource Catalogue

Primary content of the page. Full-feature table with sorting, selection, filtering, and bulk actions.

#### Search
Full-text search across: title, subject, tags, author/source, publisher. Debounce 300 ms, minimum 2 characters. HTMX replaces table body without full page reload.

#### Filter Drawer
Accessed via `Advanced Filters` button. Filter chips appear below the search bar when active.

| Filter | Type | Options |
|---|---|---|
| Type | Multi-select | E-Book / Video Lecture / Question Bank / Past Paper / Reference Material / Revision Notes / Worksheet / Audio Lecture / Image/Diagram Set / Interactive Content |
| Subject | Multi-select | Mathematics / Physics / Chemistry / Biology / English / Telugu / Hindi / Social Studies / Commerce / Computer Science / Accountancy / Economics / Other |
| Class / Grade | Multi-select | Class 6 / Class 7 / Class 8 / Class 9 / Class 10 / Class 11 / Class 12 / Integrated / All Classes |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / HEC / IIT Foundation / General |
| Language | Multi-select | Telugu / English / Hindi / Other |
| Status | Multi-select | Active / Archived / Draft |
| Curriculum | Single-select | CBSE / State AP / State TS / Both / All |
| Difficulty | Multi-select | Beginner / Intermediate / Advanced |
| Exam Relevance | Multi-select | JEE / NEET / EAMCET / SSC / Board Exam / NTSE / Olympiad |
| Distributed | Radio | All / Distributed (Yes) / Not Distributed (No) |
| Added Date Range | Date range picker | From – To |

**Clear All Filters** button resets all filters and removes all chips. Each active filter renders as a dismissible chip.

#### Table Columns

| Column | Sortable | Notes |
|---|---|---|
| ☐ Select | ❌ | Checkbox; select-all in header |
| Title | ✅ | Truncated at 60 chars; full title on hover; click opens `resource-edit` drawer |
| Type | ✅ | Colour badge: E-Book (blue) / Video Lecture (purple) / Question Bank (teal) / Past Paper (orange) / Revision Notes (green) / Worksheet (yellow) / Audio Lecture (pink) / Other types (grey) |
| Subject | ✅ | Up to 3 tags; "+N more" tooltip for overflow |
| Class / Grade | ✅ | Tags |
| Stream | ✅ | Tags; blank if not applicable |
| Language | ✅ | Badge |
| File / Link | ❌ | Icon only: 📄 (PDF/file on R2) · 🎬 (Video) · 🔗 (External URL); hover shows file size for R2 files |
| Distributed To | ✅ | Integer count of branches with active assignment; click triggers inline tooltip listing branch names |
| Downloads | ✅ | Cumulative total across all branches and all time |
| Status | ✅ | Active (green) / Archived (grey) / Draft (amber) badge |
| Added On | ✅ | DD-MMM-YYYY |
| Actions | ❌ | Edit · Distribute · Preview · Archive (or Restore if Archived) |

**Default sort:** Added On DESC.
**Pagination:** Server-side, 25 rows/page.
**Row shading:** Archived rows have 50% opacity; Draft rows have a dashed left border (amber).

### 5.2 Bulk Actions Panel

Appears as a sticky bar above the table when one or more rows are selected.

| Element | Detail |
|---|---|
| Selection badge | "[N] resource(s) selected" — updates in real-time as rows are checked |
| Distribute to Branches | Opens `distribution-assign` drawer (from page 18) in context, pre-filled with selected resource IDs |
| Archive Selected | Inline confirmation: "Archive [N] resources? Students at all branches will immediately lose access." [Confirm] [Cancel] |
| Export List | Downloads CSV of selected rows (all visible columns) |
| Clear Selection | Deselects all; panel hides |

---

## 6. Drawers & Modals

### 6.1 Drawer — `resource-create` (680px, right side)

Triggered by **+ Add Resource** button.

**Tabs:** Metadata · File · Classification · Access

---

#### Tab 1 — Metadata

| Field | Type | Validation |
|---|---|---|
| Title | Text input | Required; min 3, max 200 characters |
| Description | Textarea | Optional; max 500 characters; character counter shown |
| Type | Single-select | Required; options: all 10 resource types |
| Author / Source | Text input | Optional; max 150 characters |
| Publisher | Text input | Optional; max 150 characters |
| Publication Year | Year picker | Optional; range 1950 – current year |
| Language | Single-select | Required; Telugu / English / Hindi / Other |
| Tags | Multi-tag input | Optional; comma-separated; max 20 tags; each tag max 30 chars |

---

#### Tab 2 — File

| Field | Type | Validation |
|---|---|---|
| Upload File | File picker | Optional (but required if no External URL); accepted: PDF / MP4 / DOCX / EPUB / ZIP; max 500 MB; upload goes directly to Cloudflare R2 via pre-signed URL; progress bar shown during upload |
| External URL | URL input | Optional (but required if no file uploaded); supports YouTube / Google Drive / any HTTPS URL; validated as well-formed URL |
| Thumbnail | Image picker | Optional; JPG / PNG only; max 2 MB; recommended 800×600 px; preview shown after selection |
| File Size | Text (auto-populated) | Read-only; populated automatically after file upload; blank if external URL |
| R2 Storage Path | Text (auto-populated) | Read-only; shown after upload; e.g., `group/{group_id}/library/{uuid}/filename.pdf` |

> **Validation rule:** At least one of Upload File or External URL is required. If both are provided, the uploaded file takes precedence for delivery; the URL is stored as an alternate link.

---

#### Tab 3 — Classification

| Field | Type | Validation |
|---|---|---|
| Subject | Multi-select | Required; at least 1 subject; options: Mathematics / Physics / Chemistry / Biology / English / Telugu / Hindi / Social Studies / Commerce / Computer Science / Accountancy / Economics / Other |
| Class / Grade | Multi-select | Required; at least 1; Class 6 / Class 7 / Class 8 / Class 9 / Class 10 / Class 11 / Class 12 / Integrated / All Classes |
| Stream | Multi-select | Optional; MPC / BiPC / MEC / CEC / HEC / IIT Foundation / General |
| Difficulty | Single-select | Optional; Beginner / Intermediate / Advanced |
| Curriculum Alignment | Single-select | Optional; CBSE / State Board AP / State Board TS / Both / All |
| Exam Relevance | Multi-select | Optional; JEE / NEET / EAMCET / SSC / Board Exam / NTSE / Olympiad |

---

#### Tab 4 — Access

| Field | Type | Validation |
|---|---|---|
| Access Type | Radio | Required; All Branches / Selected Branches / Draft Only (not distributed) |
| Select Branches | Multi-select | Conditional — required when Access Type = Selected Branches; lists all active branches |
| Access Expiry | Date picker | Optional; blank = permanent access; if set, must be a future date |
| Student Access | Toggle | Default ON; if OFF, only staff can access at branch level |
| Staff Only Mode | Toggle | Default OFF; if ON, students cannot see this resource regardless of Student Access toggle |

> If Access Type = Draft Only: the resource is saved and catalogued but not distributed to any branch. It appears in the catalogue with Status = Draft.

**Footer:** `Cancel` · `Add to Catalogue`

**Submit enablement:** The Add to Catalogue button is disabled until Tab 1 (Metadata) fields that are required are valid AND Tab 2 (File) has at least one of file or URL AND Tab 3 (Classification) required fields are valid. Tab 4 defaults are sufficient; no required fields block submission.

---

### 6.2 Drawer — `resource-edit` (680px, right side)

Triggered by clicking the Title link in the table or **Edit** in the Actions column.

Identical 4-tab structure to `resource-create`, pre-filled with existing values.

> **Version note** — displayed at the top of the Metadata tab as an informational banner:
> `"Editing this resource will create Version [N+1]. All previous versions are retained and restorable via the Version History drawer."`

**Footer:** `Cancel` · `View Version History` · `Save Changes`

On save: a version record is written with a snapshot of changed fields, the Library Head's user ID, and a timestamp.

---

### 6.3 Modal — `resource-preview` (560px, centred)

Triggered by **Preview** in the Actions column.

| Element | Detail |
|---|---|
| Resource title (heading) | Full title |
| Metadata summary | Type badge · Subject tags · Class tags · Language · Added On |
| Content area | For PDF/R2 files: embedded pdf.js viewer (scrollable, paginated); For YouTube URLs: responsive iframe embed; For other external URLs: "Open in new tab" link button with domain shown; For audio: HTML5 audio player |
| Footer buttons | `Edit Resource` (opens `resource-edit` drawer) · `Distribute Resource` (opens distribution-assign drawer on page 18 pre-filled) · `Close` |

---

### 6.4 Drawer — `resource-version-history` (400px, right side)

Triggered by **View Version History** button in `resource-edit` drawer footer.

**Header:** Resource title · "Version History ([N] versions)"

**Content:** Chronological timeline (newest version at top).

| Column | Notes |
|---|---|
| Version # | e.g., v1, v2, v3 |
| Changed Fields | Comma-separated list of field names that were changed from previous version |
| Changed By | Full name + role |
| Date | DD-MMM-YYYY HH:MM |
| Restore | Button — Library Head only; confirms before restoring: "Restore v[N]? Current version will become v[N+1] with the restored content." |

Current version row is highlighted in green with a "Current" badge.

If only one version exists: renders a single row with "Original" label and no Restore button.

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button (top-right corner).

Charts are displayed in a 3-column responsive grid below the main table. On mobile/tablet they stack to single column.

### 7.1 Resource Count by Type (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Active Resources by Type" |
| Data | One segment per resource type; count of Status = Active resources of that type |
| Legend | Right side; type label + count |
| Centre label | Total active count |
| Tooltip | "[Type]: [N] resources ([X]%)" |
| Colours | 10-colour palette (colorblind-safe): blue, orange, teal, red, purple, yellow, green, pink, brown, grey |
| API endpoint | `GET /api/v1/group/{group_id}/library/catalogue/charts/by-type/` |
| HTMX | Loaded on page load; refreshed when a resource status changes |

### 7.2 Additions Per Month (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Resources Added Per Month (Last 6 Months)" |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Count of resources created in that month (all statuses) |
| Bar colour | Indigo |
| Tooltip | "[Month]: [N] resources added" |
| API endpoint | `GET /api/v1/group/{group_id}/library/catalogue/charts/additions-per-month/` |
| HTMX | Loaded on page load |

### 7.3 Subject Coverage (Horizontal Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Active Resources by Subject" |
| Y-axis | Subject names (all subjects present in catalogue), sorted by count DESC |
| X-axis | Resource count |
| Bar colour | Teal gradient |
| Tooltip | "[Subject]: [N] active resources" |
| Notes | Shows only subjects with at least 1 active resource; max 15 subjects shown; "Other" groups remainder |
| API endpoint | `GET /api/v1/group/{group_id}/library/catalogue/charts/by-subject/` |
| HTMX | Loaded on page load |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Resource created | "Resource '[Title]' added to the catalogue." | Success |
| Resource updated (new version) | "Resource '[Title]' updated. Version [N+1] created." | Success |
| Resource archived | "Resource '[Title]' has been archived." | Info |
| Resource restored from archive | "Resource '[Title]' restored to Active status." | Success |
| Version restored | "Version [N] of '[Title]' restored. New version [N+1] created." | Success |
| Bulk archive success | "[N] resources archived successfully." | Info |
| Bulk archive partial | "[N] resources archived. [E] could not be archived (active assignments exist)." | Warning |
| Distribute action triggered | "Opening distribution assignment for [N] resource(s)." | Info |
| File upload in progress | "Uploading file to R2… [X]% complete." | Info (updates via progress bar) |
| File upload success | "File uploaded to R2 successfully." | Success |
| File upload failed | "File upload failed. Please check your connection and try again." | Error |
| Bulk import started | "Bulk import in progress. You will be notified when complete." | Info |
| Bulk import completed | "Bulk import complete: [N] resources added, [E] errors." | Success / Warning |
| Export triggered | "Export is being prepared. Download will begin shortly." | Info |
| Validation error | "Please complete all required fields before saving." | Error |
| File + URL missing | "Please upload a file or enter an external URL before saving." | Error |
| R2 quota warning | "R2 storage is at [X]%. Archive unused resources to free space." | Warning |

---

## 9. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No resources in catalogue | "Your e-library is empty." | "Start building the catalogue by adding your first resource." | `+ Add Resource` button |
| No results for current filters | "No resources match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No results for search | "No resources found for '[query]'." | "Try a different title, subject, or tag." | — |
| No archived resources | "No archived resources." | "Resources you archive will appear here." | — |
| Version history — single version | "This resource has only one version." | "Edits will create additional versions here." | — |
| Preview modal — external URL with no embed | "This resource links to an external page." | "Click the button below to open it in a new tab." | `Open Resource ↗` button |
| Chart — no data | "No data available." | "Resources will appear here once added." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: stats bar placeholder (4 grey pill metrics) + table (10 grey rows × 13 columns) + 3 chart placeholders (grey rectangles) |
| Filter / search apply | Table body spinner overlay; stats bar refreshes after table resolves |
| Drawer open (create / edit) | Drawer skeleton: tab bar + 5 grey field blocks per tab |
| File upload | Progress bar with percentage within the File tab; field blocked during upload |
| Preview modal open | Spinner centred in content area; resolves to viewer or embed |
| Version history drawer open | Skeleton: 4 grey timeline rows |
| Chart load | Individual chart skeleton (grey rounded rectangle with spinner) per chart |
| Bulk import processing | Full-width info banner: "Import in progress… [N] rows processed" — updates via WebSocket or polling |
| Export generation | Button spinner + "Preparing…" label; button disabled until download ready |

---

## 11. Role-Based UI Visibility

| UI Element | Library Head (101) | All Other Roles |
|---|---|---|
| Entire page | ✅ Full access | ❌ No access — 403 |
| Stats Bar | ✅ | ❌ |
| + Add Resource button | ✅ | ❌ |
| Bulk Import button | ✅ | ❌ |
| Advanced Filters | ✅ | ❌ |
| Export List | ✅ | ❌ |
| Edit action | ✅ | ❌ |
| Distribute action | ✅ | ❌ |
| Preview action | ✅ | ❌ |
| Archive / Restore action | ✅ | ❌ |
| Bulk Actions panel | ✅ | ❌ |
| Version History drawer | ✅ | ❌ |
| Restore version button | ✅ | ❌ |
| All charts | ✅ | ❌ |

---

## 12. API Endpoints

### Base URL: `/api/v1/group/{group_id}/library/catalogue/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/library/catalogue/` | List resources (paginated, filtered) | JWT + Library Head role |
| POST | `/api/v1/group/{group_id}/library/catalogue/` | Create new resource record | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/` | Retrieve full resource detail | Library Head |
| PATCH | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/` | Update resource (creates new version) | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/archive/` | Archive resource | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/restore/` | Restore archived resource to Active | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/versions/` | List all versions for a resource | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/{resource_id}/versions/{version_id}/restore/` | Restore a historical version | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/bulk-archive/` | Archive multiple resources by ID list | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/bulk-import/` | Bulk import via Excel template | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/bulk-import/{job_id}/status/` | Poll bulk import job status | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/export/` | Export filtered list as CSV | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/stats/` | Stats bar data (4 metrics) | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/charts/by-type/` | Chart 7.1 data | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/charts/additions-per-month/` | Chart 7.2 data | Library Head |
| GET | `/api/v1/group/{group_id}/library/catalogue/charts/by-subject/` | Chart 7.3 data | Library Head |
| POST | `/api/v1/group/{group_id}/library/catalogue/r2-presign/` | Generate pre-signed R2 upload URL for file upload | Library Head |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `type` | str[] | Resource type slugs |
| `subject` | str[] | Subject slugs |
| `class_grade` | str[] | Class/grade values |
| `stream` | str[] | Stream slugs |
| `language` | str[] | Language values |
| `status` | str[] | `active`, `archived`, `draft` |
| `curriculum` | str | Curriculum alignment value |
| `difficulty` | str[] | `beginner`, `intermediate`, `advanced` |
| `exam_relevance` | str[] | Exam relevance tags |
| `distributed` | bool | true = distributed to at least 1 branch |
| `date_from` | date | Added On range start |
| `date_to` | date | Added On range end |
| `search` | str | Full-text search across title, subject, tags, author |
| `sort_by` | str | Column field name; prefix `-` for descending |
| `page` | int | Page number (default 1) |
| `page_size` | int | Default 25, max 100 |

---

## 13. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Search input | `hx-get="/api/.../catalogue/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#catalogue-table-body"` `hx-include="#filter-form"` | Table body replaced on keystroke with 300 ms debounce |
| Filter apply | `hx-get="/api/.../catalogue/"` `hx-trigger="change"` `hx-target="#catalogue-table-body"` `hx-include="#filter-form"` | Table refreshes; filter chips re-render; stats bar reloads |
| Clear filter chip | `hx-get="/api/.../catalogue/"` `hx-trigger="click"` `hx-target="#catalogue-table-body"` `hx-include="#filter-form"` | Chip removed; table refreshes |
| Pagination | `hx-get="/api/.../catalogue/?page={n}"` `hx-target="#catalogue-table-body"` `hx-push-url="true"` | Page swap with URL update |
| Column sort click | `hx-get="/api/.../catalogue/?sort_by={field}"` `hx-target="#catalogue-table-body"` `hx-include="#filter-form"` | Table body replaced with sorted data |
| Stats bar load | `hx-get="/api/.../catalogue/stats/"` `hx-trigger="load"` `hx-target="#stats-bar"` | Stats bar populated on page load |
| Stats bar refresh | `hx-trigger="resourceSaved from:body"` `hx-target="#stats-bar"` | Refreshes after any create/edit/archive/restore |
| Resource create drawer open | `hx-get="/api/.../catalogue/create-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Drawer slides in from right with empty form |
| Resource edit drawer open (Title click) | `hx-get="/api/.../catalogue/{resource_id}/edit-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Drawer slides in pre-filled |
| Drawer tab switch | `hx-get="/api/.../catalogue/{resource_id}/edit-form/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped without closing drawer |
| Resource create submit | `hx-post="/api/.../catalogue/"` `hx-target="#catalogue-table-body"` `hx-swap="afterbegin"` `hx-on::after-request="closeDrawer(); fireToast(); refreshStatsBar();"` | New row prepended; drawer closes; toast fires; stats bar refreshes |
| Resource edit submit | `hx-patch="/api/.../catalogue/{resource_id}/"` `hx-target="#resource-row-{resource_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeDrawer(); fireToast(); refreshStatsBar();"` | Row updated in-place |
| Archive single resource | `hx-post="/api/.../catalogue/{resource_id}/archive/"` `hx-target="#resource-row-{resource_id}"` `hx-swap="outerHTML"` `hx-confirm="Archive this resource? All branch distribution access will be removed."` | Row updated to Archived state |
| Restore single resource | `hx-post="/api/.../catalogue/{resource_id}/restore/"` `hx-target="#resource-row-{resource_id}"` `hx-swap="outerHTML"` | Row updated to Active state |
| Row checkbox select | `hx-trigger="change"` `hx-target="#bulk-actions-bar"` `hx-get="/ui/bulk-bar/?selected={ids}"` | Bulk actions bar appears / updates count |
| Bulk archive submit | `hx-post="/api/.../catalogue/bulk-archive/"` `hx-target="#catalogue-table-body"` `hx-include="#selected-ids"` `hx-on::after-request="clearSelection(); fireToast();"` | Selected rows archived; table refreshes |
| Version history drawer open | `hx-get="/api/.../catalogue/{resource_id}/versions/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Version history drawer loads |
| Restore version submit | `hx-post="/api/.../catalogue/{resource_id}/versions/{version_id}/restore/"` `hx-confirm="Restore version [N]? Current version will become v[N+1]."` `hx-target="#resource-row-{resource_id}"` `hx-swap="outerHTML"` | Version restored; row updated |
| Preview modal open | `hx-get="/api/.../catalogue/{resource_id}/preview/"` `hx-target="#modal-container"` `hx-trigger="click"` | Modal renders with pdf.js or embed |
| Chart load | `hx-get="/api/.../catalogue/charts/{chart_slug}/"` `hx-trigger="load"` `hx-target="#chart-{chart_slug}"` | Each chart loaded independently on page load |
| Export trigger | `hx-get="/api/.../catalogue/export/"` `hx-include="#filter-form"` `hx-trigger="click"` `hx-target="#export-status"` | Export job triggered; response contains download URL |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
