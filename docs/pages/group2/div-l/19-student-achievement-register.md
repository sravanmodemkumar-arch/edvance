# 19 — Student Achievement Register

> **URL:** `/group/sports/achievements/`
> **File:** `19-student-achievement-register.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Sports Director (Role 97, G3) · Group Sports Coordinator (Role 98, G3) · Group Cultural Activities Head (Role 99, G3) · Group NSS/NCC Coordinator (Role 100, G3) · Group Library Head (Role 101, G2 — view only) · Group Chairman / CEO (G5/G4 — view only)

---

## 1. Purpose

Master register of all student co-curricular achievements across the entire group — sports, cultural, NSS/NCC, literary, science competitions, external competitions, and state/national/international representations. Serves as the single source of truth for student achievement records across all branches.

**Primary use cases for this data:**
1. State and national competition nominations — coordinators identify eligible students from verified records
2. Topper showcase and brand ambassador selection — used by Group Marketing (Division O) to identify high-achieving students for promotional content
3. Scholarship recommendations — feeds into Division C (Finance/Scholarships) workflow
4. Annual report and inspection compliance — complete, auditable, evidence-backed achievement register

**Scale:** 500–5,000 achievement records per academic year across all branches.

**Achievement Categories:**

| Category | Who Manages | Colour Badge |
|---|---|---|
| Sports | Sports Director / Sports Coordinator | Blue |
| Cultural | Cultural Activities Head | Purple |
| NSS / NCC | NSS/NCC Coordinator | Olive |
| Literary | Sports Coordinator / Cultural Head | Teal |
| Science | All coordinators | Orange |
| External Competition | All coordinators | Yellow |
| State Representation | All coordinators | Indigo |
| National Representation | All coordinators | Red |
| International | All coordinators | Gold |
| Other | All coordinators | Grey |

**Achievement Levels:** School/Branch · District · State · National · International · Online/Virtual

---

## 2. Role Access

| Role | Level | Access | Scope |
|---|---|---|---|
| Group Sports Director | G3 | Full — create, edit, verify, delete sports achievements; view all categories | All branches |
| Group Sports Coordinator | G3 | Full — create, edit, verify sports achievements; view all | All branches |
| Group Cultural Activities Head | G3 | Full — create, edit, verify cultural + literary achievements; view all | All branches |
| Group NSS/NCC Coordinator | G3 | Full — create, edit, verify NSS/NCC achievements; view all | All branches |
| Group Library Head | G2 | View only — read all achievements; no create/edit/delete | All branches |
| Group Chairman / CEO | G5/G4 | View only — read all achievements; Top Achievers section prominent | All branches |
| Group Analytics Director (Div M) | G1 | View only — no create/edit/delete | All branches |
| Group MIS Officer | G1 | View only — no create/edit/delete | All branches |
| All other roles | — | No access | — |

> **Access enforcement:** `@require_role('sports_director', 'sports_coordinator', 'cultural_head', 'nss_ncc_coordinator', 'library_head', 'chairman', 'ceo', 'analytics_director', 'mis_officer')` with server-side action gating per role (view-only roles see no create/edit/delete/verify controls).

> **Category-level gating (server-side):** Cultural Head cannot create/edit Sports records; NSS/NCC Coordinator cannot create/edit Cultural records. Category field in create/edit forms is pre-filtered to the logged-in coordinator's domain. Sports Director has full cross-category access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Achievements  ›  Student Achievement Register
```

### 3.2 Page Header
- **Title:** `Student Achievement Register`
- **Subtitle:** `[Current Academic Year] · [N] Achievements · [N] Students · Last updated [timestamp]`
- **Right controls (role-gated):**
  - `+ Add Achievement` (Sports Director, Sports Coordinator, Cultural Head, NSS/NCC Coordinator)
  - `Bulk Import` (same roles)
  - `Advanced Filters`
  - `Export Register ↓` (all roles with page access)

### 3.3 Alert Banners

| Condition | Banner Text | Severity |
|---|---|---|
| Unverified State/National/International records > 0 | "[N] State/National/International achievements have no uploaded evidence and remain unverified. Evidence is required for official nominations." | Red |
| Records pending verification > 14 days | "[N] achievements have been pending verification for more than 14 days." | Amber |
| Certificates not generated for verified records | "[N] verified achievements have no generated certificate. Generate certificates for the annual report." | Amber |

---

## 4. KPI Summary Bar

Five KPI cards in a responsive row. All metrics reflect the currently selected Academic Year filter (default: current AY). HTMX-loaded on page load; refreshes when any achievement is created, edited, verified, or deleted.

| # | Card | Metric | Colour Rule |
|---|---|---|---|
| 1 | Total Achievements This AY | Count of all achievement records in selected AY | Blue always |
| 2 | Students with Achievement | Count of unique students across all records in selected AY | Teal always |
| 3 | State / National Representations | Count of records with Level = State or National or International | Indigo; red if 0 |
| 4 | Certificates Generated | Count of records with certificate_generated = true | Green if > 0; grey if 0 |
| 5 | Achievements Pending Verification | Count of records with verified = false | Red if > 0; green = 0 |

---

## 5. Sections

### 5.1 Achievement Register

Primary content of the page. Full-feature table with sorting, selection, and filtering.

#### Search
Full-text search across: student name, roll number, competition name, branch name. Debounce 300 ms, minimum 2 characters.

#### Filter Drawer
Active filter chips appear below the search bar.

| Filter | Type | Options |
|---|---|---|
| Category | Multi-select | Sports / Cultural / NSS/NCC / Literary / Science / External Competition / State Representation / National Representation / International / Other |
| Level | Multi-select | School/Branch / District / State / National / International / Online/Virtual |
| Branch | Multi-select | All active branches |
| Verified Status | Multi-select | Verified / Pending Verification |
| Evidence | Radio | All / Evidence Uploaded / Evidence Missing |
| Date Range | Date range picker | Event date From – To |
| Academic Year | Single-select | Current AY (default) / previous AYs (up to 5 years) |
| Class | Multi-select | Class 6 / Class 7 / Class 8 / Class 9 / Class 10 / Class 11 / Class 12 / Integrated |
| Position / Award | Multi-select | 1st / 2nd / 3rd / Participation / Best in Category / Special Award / Certificate of Excellence |

#### Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Full name; click opens `achievement-detail` drawer |
| Roll Number | ✅ | Branch-issued roll number |
| Branch | ✅ | Branch name |
| Class | ✅ | e.g., "Class 11 MPC" |
| Category | ✅ | Colour badge per category (see section 1 table) |
| Achievement Title | ✅ | Truncated at 55 chars; full title on hover |
| Level | ✅ | Badge: School/Branch (grey) / District (blue) / State (indigo) / National (red) / International (gold) / Online (teal) |
| Event / Competition Name | ✅ | Text; truncated at 45 chars |
| Date | ✅ | DD-MMM-YYYY (event date) |
| Position / Award | ✅ | 1st (gold) / 2nd (silver) / 3rd (bronze) / Participation (grey) / Special (purple) / Certificate (teal) — colour badge |
| Verified? | ✅ | Verified (green badge) / Pending (amber badge) |
| Evidence | ❌ | Icon: ✅ uploaded (green) / ❌ missing (red) |
| Actions | ❌ | View · Edit · Verify · Delete (role-gated) |

**Default sort:** Date DESC.
**Pagination:** Server-side, 25 rows/page.
**Row highlight:** National/International level records have a subtle gold left border. Pending + no evidence rows have a dashed red left border.

---

### 5.2 Top Achievers (This Academic Year)

Compact ranked section displayed below or to the right of the main table (responsive). Shows the top 10 students by level-weighted achievement score.

**Ranking formula (level-weighted score):** International (×5) + National (×4) + State (×3) + District (×2) + School/Branch (×1) + Online/Virtual (×1) — total weighted score per student, descending.

| Column | Notes |
|---|---|
| Rank | 1–10; trophy icon for rank 1 |
| Student Name | Full name |
| Branch | Branch name |
| Class | |
| Total Achievements | Count of records |
| Highest Level | Highest level badge for this student |
| Weighted Score | Calculated score |
| View | Link — filters main register to this student |

Visible to all roles with page access. Library Head and Chairman see this section prominently.

---

### 5.3 Unverified Achievements Alert Section

Appears only when unverified records exist. Displayed as a collapsible amber section above the main table.

**Header:** "⚠ [N] Achievements Pending Verification — State/National/International evidence required"

**Contents:** Compact table (max 10 rows shown; "View All" link filters main table to Pending):

| Column | Notes |
|---|---|
| Student Name | |
| Branch | |
| Category | Badge |
| Achievement Title | Truncated |
| Level | Badge |
| Date | |
| Days Pending | Red text if > 14 days |
| Actions | Verify · Upload Evidence · View |

**Collapsed by default** if fewer than 5 unverified records; **expanded by default** if 5 or more.

---

## 6. Drawers & Modals

### 6.1 Drawer — `achievement-create` (480px, right side)

Triggered by **+ Add Achievement** button.

**Tabs:** Student · Achievement · Evidence

---

#### Tab 1 — Student

| Field | Type | Validation |
|---|---|---|
| Student Name | Text input | Required; min 2, max 100 characters |
| Roll Number | Text input | Required; min 2, max 30 characters |
| Branch | Single-select | Required; lists all active branches |
| Class | Single-select | Required; Class 6 / Class 7 / Class 8 / Class 9 / Class 10 / Class 11 / Class 12 / Integrated |
| Student Type | Single-select | Required; Day Scholar / Hosteler |
| Team Achievement? | Toggle | Default OFF; if ON, enables Team Members sub-section — up to 20 additional student entries (Name + Roll Number each), all sharing the same achievement record |

---

#### Tab 2 — Achievement

| Field | Type | Validation |
|---|---|---|
| Category | Single-select | Required; options filtered by role (Cultural Head sees Cultural/Literary; NSS/NCC Coordinator sees NSS/NCC; Sports Director sees all) |
| Achievement Title | Text input | Required; min 5, max 200 characters |
| Event / Competition Name | Text input | Required; min 3, max 200 characters |
| Organising Body | Text input | Optional; max 150 characters |
| Event Date | Date picker | Required; cannot be a future date |
| Level | Single-select | Required; School/Branch / District / State / National / International / Online/Virtual |
| Position / Award | Single-select | Required; 1st Place / 2nd Place / 3rd Place / Participation / Best in Category / Special Award / Certificate of Excellence |
| Score / Marks | Text input | Optional; max 50 characters; e.g., "95/100", "47 pts" |
| Notes | Textarea | Optional; max 300 characters |

---

#### Tab 3 — Evidence

| Field | Type | Validation |
|---|---|---|
| Certificate Upload | File picker | Conditionally required: mandatory for Level = State / National / International; optional for District and below; accepted: PDF / JPG / PNG; max 10 MB; uploaded to Cloudflare R2 |
| Media Coverage Link | URL input | Optional; news article, YouTube video, social media post |
| Coach / Teacher Reference | Text input | Optional; name of accompanying teacher or coach |
| Medical Fitness Certificate | File picker | Conditionally required: mandatory for Level = State / National / International AND Category = Sports (state sports authorities mandate this for all nominated athletes); accepted: PDF / JPG / PNG; max 5 MB; uploaded to Cloudflare R2. Banner shown: "Medical Fitness Certificate is required for state/national/international sports nominations." |
| Flag for Marketing | Toggle | Optional; default OFF; only Sports Director (all categories) and Cultural Head (cultural/literary); shown only for Level = State / National / International; when ON — triggers in-platform notification to Group Marketing Director (Role 114) and Topper Relations Manager (Role 120) with student details for brand ambassador / topper showcase consideration |
| Mark as Verified | Toggle | Default OFF; only Sports Director, Cultural Head, NSS/NCC Coordinator for their categories can toggle ON |

> **Evidence requirement note:** If Level = State/National/International is selected in Tab 2, a banner appears at the top of Tab 3: `"Certificate upload is required for State, National, and International level achievements."`

**Footer:** `Cancel` · `Save Achievement`

**Submit enablement:** Save button active once Tab 1 and Tab 2 required fields are valid. Tab 3 blocks submission only if Level requires a certificate and none has been uploaded.

---

### 6.2 Drawer — `achievement-detail` (480px, right side)

Triggered by clicking Student Name in the table or **View** in Actions column.

**Tabs:** Overview · Evidence · History

---

#### Tab 1 — Overview

Full read-only display of all fields from the Student and Achievement tabs, arranged in a two-column field grid.

If record is Verified: shows verifier name, role, and verification timestamp below the Achievement Title.

**Action buttons in drawer header (role-gated):**
- `Edit` — opens `achievement-edit` drawer (coordinators for their own category; Sports Director for all)
- `Verify` — marks record as Verified; requires evidence to be uploaded (same coordinator roles)
- `Delete` — opens `delete-confirm` modal (Sports Director only)

---

#### Tab 2 — Evidence

| Element | Detail |
|---|---|
| Certificate viewer | If PDF: embedded pdf.js viewer; if image: full-width image display; if none uploaded: "No certificate uploaded" empty state |
| Upload Evidence button | Shown for edit-access roles when no certificate is present; opens file picker; uploads directly to Cloudflare R2 via pre-signed URL |
| Media Coverage Link | Clickable link opening in new tab; if absent: "No media link added" |
| Coach / Teacher Reference | Text display |

---

#### Tab 3 — History

Immutable audit log of all actions on this record.

| Column | Notes |
|---|---|
| Timestamp | DD-MMM-YYYY HH:MM |
| Actor | Name + Role |
| Action | Created / Edited / Evidence Uploaded / Verified / Unverified / Deleted (soft) |
| Changed Fields | Comma-separated list of changed fields (on edits) |

Entries cannot be edited or deleted.

---

### 6.3 Drawer — `achievement-edit` (480px, right side)

Triggered by **Edit** in Actions column.

Identical 3-tab structure to `achievement-create`, pre-filled with existing values.

**Header note:** "Editing this record. All changes are logged in the audit history."

If the record is already Verified, an amber warning banner at the top of Tab 1 reads: `"This achievement is verified. Editing will reset its status to Pending Verification until re-verified."`

**Footer:** `Cancel` · `Save Changes`

---

### 6.4 Modal — `bulk-import` (480px, centred)

Triggered by **Bulk Import** button.

| Element | Detail |
|---|---|
| Instructions | Step-by-step: Download template → Fill in data (one row per achievement) → Upload completed file |
| Download Template | `Download Excel Template ↓` — pre-formatted .xlsx with required columns and dropdown validations |
| Upload File | File picker; accepts .xlsx only; max 5 MB |
| Preview | After upload: first 10 rows in a preview table; total row count; errors highlighted in red (wrong dropdown values, missing required fields, invalid dates) |
| Import options | Radio: Import All Valid Rows Only / Import All (skip invalid rows) |
| Import button | `Import [N] Achievements` — disabled if 0 valid rows |

**Behaviour on import:** Rows are created as Pending Verification. Evidence must be uploaded individually from each record's detail drawer. Import supports up to 200 rows per file.

**Footer:** `Cancel` · `Import [N] Achievements`

---

### 6.5 Modal — `delete-confirm` (380px, centred)

Triggered by **Delete** button in `achievement-detail` drawer header (Sports Director only).

| Element | Detail |
|---|---|
| Warning heading | "Delete this achievement record?" |
| Student + Achievement | Full student name · Achievement title |
| Consequence statement | "This record will be permanently deleted. This action cannot be undone. Any certificates generated from this record will also be removed." |
| Confirm checkbox | "I confirm I want to permanently delete this achievement record." — Required |

**Footer:** `Cancel` · `Delete` (destructive — red button)

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button (top-right corner of each chart card).

Charts are displayed in a 2×2 responsive grid below the main register. On mobile they stack to single column.

### 7.1 Achievements by Category (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Achievements by Category — [Selected AY]" |
| Data | One segment per category; count of achievement records |
| Legend | Right side; label + count |
| Centre label | Total achievements count |
| Tooltip | "[Category]: [N] achievements ([X]%)" |
| Colours | 10-colour colorblind-safe palette matching category badge colours |
| API endpoint | `GET /api/v1/group/{group_id}/sports/achievements/charts/by-category/` |
| HTMX | Loaded on page load; refreshes on AY filter change |

### 7.2 Achievement Level Distribution (Vertical Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar |
| Title | "Achievements by Level — [Selected AY]" |
| X-axis | Level labels in order: School/Branch → District → State → National → International → Online/Virtual |
| Y-axis | Count |
| Bar colours | Per level: grey / blue / indigo / red / gold / teal |
| Tooltip | "[Level]: [N] achievements" |
| API endpoint | `GET /api/v1/group/{group_id}/sports/achievements/charts/by-level/` |
| HTMX | Loaded on page load; refreshes on AY filter change |

### 7.3 Top 10 Branches by Achievement Count (Horizontal Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Top 10 Branches by Achievement Count — [Selected AY]" |
| Y-axis | Branch names (top 10 by total records, sorted DESC) |
| X-axis | Count of achievement records |
| Bar colour | Indigo gradient |
| Tooltip | "[Branch]: [N] achievements" |
| Interactivity | Clicking a bar filters the main register to that branch |
| API endpoint | `GET /api/v1/group/{group_id}/sports/achievements/charts/top-branches/` |
| HTMX | Loaded on page load; refreshes on AY filter change |

### 7.4 Monthly Achievement Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Achievements Recorded Per Month — Last 6 Months" |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Count of achievement records created in that month |
| Line colour | Blue with filled area below line |
| Data points | Circular markers on each month |
| Tooltip | "[Month]: [N] achievements recorded" |
| API endpoint | `GET /api/v1/group/{group_id}/sports/achievements/charts/monthly-trend/` |
| HTMX | Loaded on page load |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Achievement created | "Achievement for [Student Name] added successfully." | Success |
| Achievement created (evidence required) | "Achievement added. Upload evidence to verify State/National/International records." | Warning |
| Achievement edited | "Achievement updated. Status reset to Pending Verification." | Info |
| Achievement verified | "Achievement for [Student Name] verified successfully." | Success |
| Achievement deleted | "Achievement record deleted." | Info |
| Evidence uploaded | "Evidence uploaded successfully for [Student Name]." | Success |
| Bulk import completed | "Import complete: [N] achievements added, [E] rows had errors." | Success / Warning |
| Export triggered | "Export is being prepared. Download will begin shortly." | Info |
| Validation error — evidence required | "Certificate upload is required for State, National, and International level achievements." | Error |
| Validation error — required fields | "Please complete all required fields before saving." | Error |
| Delete confirmation missing | "Please confirm the deletion before proceeding." | Error |
| Verify failed — no evidence | "Cannot verify: no evidence certificate has been uploaded for this record." | Error |

---

## 9. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No achievements this AY | "No achievements recorded for this academic year." | "Start adding student achievements to build the group register." | `+ Add Achievement` button (role-gated) |
| No results for current filters | "No achievements match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No results for search | "No achievements found for '[query]'." | "Try searching by student name, roll number, or competition name." | — |
| No unverified achievements | "All achievements are verified." | — | — |
| Top Achievers — no data | "No achievements recorded yet for this academic year." | "Achievements will appear here once added." | — |
| Evidence tab — no certificate | "No certificate uploaded." | "Upload a certificate to enable verification of this record." | `Upload Evidence` button (role-gated) |
| History tab — no entries | "No history entries yet." | — | — |
| Chart — no data | "No data available for the selected period." | — | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 5 KPI cards + alert section placeholder + table (10 grey rows × 13 columns) + 4 chart placeholders |
| KPI bar refresh | Each KPI card shows individual shimmer while refreshing |
| Filter / search apply | Table body spinner overlay; KPI cards refresh after table resolves |
| Drawer open | Drawer skeleton: tab bar + 5 grey field blocks per tab |
| Evidence upload in drawer | Progress bar in Tab 3; field blocked during upload |
| Bulk import — file upload & preview | Spinner in modal content area; resolves to preview table |
| Bulk import — processing | Progress bar in modal: "[N] of [M] rows imported…" |
| Individual chart load | Per-chart skeleton (grey rounded rectangle with spinner) |
| Export generation | Button spinner + "Preparing…" label; button disabled until download ready |

---

## 11. Role-Based UI Visibility

| UI Element | Sports Director (97) | Sports Coordinator (98) | Cultural Head (99) | NSS/NCC Coord (100) | Library Head (101) | Chairman / CEO (G5/G4) |
|---|---|---|---|---|---|---|
| View achievement register | ✅ All | ✅ All | ✅ All | ✅ All | ✅ All (view only) | ✅ All (view only) |
| KPI Summary Bar | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Alert banners | ✅ | ✅ | ✅ | ✅ | ✅ (view) | ✅ (view) |
| Top Achievers section | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Unverified alert section | ✅ | ✅ | ✅ | ✅ | ✅ (view only) | ❌ |
| + Add Achievement | ✅ All categories | ✅ Sports only | ✅ Cultural + Literary | ✅ NSS/NCC only | ❌ | ❌ |
| Bulk Import | ✅ | ✅ (own category) | ✅ (own category) | ✅ (own category) | ❌ | ❌ |
| Edit achievement | ✅ All categories | ✅ Sports only | ✅ Cultural + Literary | ✅ NSS/NCC only | ❌ | ❌ |
| Verify achievement | ✅ | ✅ (own category) | ✅ (own category) | ✅ (own category) | ❌ | ❌ |
| Delete achievement | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |
| Export Register | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| All 4 charts | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 12. API Endpoints

### Base URL: `/api/v1/group/{group_id}/sports/achievements/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/sports/achievements/` | List achievements (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/sports/achievements/` | Create new achievement record | Sports Director / Coordinator / Cultural Head / NSS/NCC Coord |
| GET | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/` | Retrieve full achievement detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/` | Edit achievement record | Category-gated coordinators; Sports Director = all |
| DELETE | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/` | Soft-delete achievement record | Sports Director only |
| POST | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/verify/` | Mark achievement as verified | Category-gated coordinators |
| POST | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/evidence/` | Upload evidence file to Cloudflare R2 | Category-gated coordinators |
| GET | `/api/v1/group/{group_id}/sports/achievements/{achievement_id}/history/` | Retrieve immutable audit history | JWT + role check |
| POST | `/api/v1/group/{group_id}/sports/achievements/bulk-import/` | Bulk import via Excel template | Category-gated coordinators |
| GET | `/api/v1/group/{group_id}/sports/achievements/bulk-import/{job_id}/status/` | Poll import job status | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/top-achievers/` | Top 10 students by weighted score | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/unverified/` | Pending verification summary | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/export/` | Export filtered register as CSV/XLSX | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/charts/by-category/` | Chart 7.1 data | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/charts/by-level/` | Chart 7.2 data | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/charts/top-branches/` | Chart 7.3 data | JWT + role check |
| GET | `/api/v1/group/{group_id}/sports/achievements/charts/monthly-trend/` | Chart 7.4 data | JWT + role check |
| POST | `/api/v1/group/{group_id}/sports/achievements/r2-presign/` | Generate pre-signed R2 URL for evidence upload | Category-gated coordinators |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `category` | str[] | Category slugs |
| `level` | str[] | Level values |
| `branch` | int[] | Branch IDs |
| `verified` | bool | true = Verified only; false = Pending only |
| `evidence` | bool | true = evidence uploaded; false = missing |
| `date_from` | date | Event date range start |
| `date_to` | date | Event date range end |
| `academic_year` | str | AY slug (e.g., `2025-26`) |
| `class_grade` | str[] | Class/grade values |
| `position` | str[] | Position/award values |
| `search` | str | Student name, roll number, competition name, branch |
| `sort_by` | str | Column field name; prefix `-` for descending |
| `page` | int | Page number (default 1) |
| `page_size` | int | Default 25, max 100 |

---

## 13. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| KPI bar load | `hx-get="/api/.../achievements/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | KPI bar populated on page load |
| KPI bar refresh | `hx-trigger="achievementChanged from:body"` `hx-target="#kpi-bar"` | Refreshes after create / edit / verify / delete |
| Unverified section load | `hx-get="/api/.../achievements/unverified/"` `hx-trigger="load"` `hx-target="#unverified-section"` | Loaded independently on page load |
| Search input | `hx-get="/api/.../achievements/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#achievements-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../achievements/"` `hx-trigger="change"` `hx-target="#achievements-table-body"` `hx-include="#filter-form"` | Table body + KPI bar refresh |
| AY filter change | `hx-get="/api/.../achievements/"` `hx-trigger="change"` `hx-target="#achievements-table-body"` `hx-include="#filter-form"` followed by custom JS dispatching `ayChanged` event to trigger chart + KPI refreshes | Table + KPI + charts all refresh |
| Pagination | `hx-get="/api/.../achievements/?page={n}"` `hx-target="#achievements-table-body"` `hx-push-url="true"` | Page swap with URL update |
| Achievement detail drawer open | `hx-get="/api/.../achievements/{achievement_id}/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Drawer opens; Overview tab default |
| Drawer tab switch | `hx-get="/api/.../achievements/{achievement_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` | Tab content swapped |
| History tab load | `hx-get="/api/.../achievements/{achievement_id}/history/"` `hx-trigger="click[tab='history']"` `hx-target="#drawer-tab-content"` | Loaded on tab click |
| Create drawer open | `hx-get="/ui/achievements/create-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Empty 3-tab drawer slides in |
| Create submit | `hx-post="/api/.../achievements/"` `hx-target="#achievements-table-body"` `hx-swap="afterbegin"` `hx-on::after-request="closeDrawer(); fireToast(); refreshKpi();"` | New row prepended |
| Edit drawer open | `hx-get="/ui/achievements/{achievement_id}/edit-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Pre-filled drawer slides in |
| Edit submit | `hx-patch="/api/.../achievements/{achievement_id}/"` `hx-target="#achievement-row-{achievement_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeDrawer(); fireToast(); refreshKpi();"` | Row updated in-place |
| Verify action | `hx-post="/api/.../achievements/{achievement_id}/verify/"` `hx-target="#achievement-row-{achievement_id}"` `hx-swap="outerHTML"` `hx-on::after-request="fireToast(); refreshKpi();"` | Row Verified badge updates; KPI refreshes |
| Evidence upload (in drawer) | `hx-post="/api/.../achievements/{achievement_id}/evidence/"` `hx-target="#evidence-status-{achievement_id}"` `hx-encoding="multipart/form-data"` | Evidence icon in table row updates to ✅ |
| Bulk import file upload (preview) | `hx-post="/ui/achievements/bulk-import/preview/"` `hx-trigger="change"` `hx-target="#import-preview-table"` `hx-encoding="multipart/form-data"` | Preview table renders with validation results |
| Bulk import confirm | `hx-post="/api/.../achievements/bulk-import/"` `hx-target="#achievements-table-body"` `hx-on::after-request="closeModal(); fireToast(); refreshKpi();"` | Rows imported; table refreshes |
| Delete confirm submit | `hx-delete="/api/.../achievements/{achievement_id}/"` `hx-target="#achievement-row-{achievement_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeModal(); fireToast(); refreshKpi();"` | Row removed |
| Top Achievers load | `hx-get="/api/.../achievements/top-achievers/"` `hx-trigger="load"` `hx-target="#top-achievers-section"` | Loaded independently |
| Chart load | `hx-get="/api/.../achievements/charts/{chart_slug}/"` `hx-trigger="load"` `hx-target="#chart-{chart_slug}"` | Each chart loaded independently on page load |
| Chart bar click → filter | JavaScript `Chart.js onClick` → dispatches HTMX request: `hx-get="/api/.../achievements/?branch={branch_id}"` `hx-target="#achievements-table-body"` | Chart 7.3 bar click filters main table |
| Export trigger | `hx-get="/api/.../achievements/export/"` `hx-include="#filter-form"` `hx-trigger="click"` `hx-target="#export-status"` | Export job triggered; button shows spinner |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
