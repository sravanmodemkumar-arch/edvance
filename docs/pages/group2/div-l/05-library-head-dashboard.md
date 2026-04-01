# 05 — Library & Learning Resources Head Dashboard

> **URL:** `/group/library/head/`
> **File:** `05-library-head-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Library & Learning Resources Head (Role 101, G2) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Library & Learning Resources Head. Manages the central group-level e-library and all digital learning resources distributed to branches. The Library Head curates and categorizes resources (e-books, video lectures, question banks, reference materials, past papers, revision notes), controls which branches have access to which resources, monitors usage analytics, and processes resource requests from branch librarians.

**Access level G2 (Group Content):** The Library Head can upload and manage shared content across all branches. They cannot configure branch portals, manage users, or access financial/HR data.

Scale: 500–10,000 digital resources in catalogue · 20–50 branches · 50–500 resource access requests per month · 5,000–50,000 student digital resource accesses per month.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Library & Learning Resources Head | 101 | G2 | Full — catalogue management, distribution, analytics | Exclusive dashboard |
| Group Academic Director (Div B) | — | G3 | View catalogue and usage analytics | Read-only |
| Branch Librarian | — | Branch G2 | View resources assigned to their branch only | Branch-scoped |
| Group Chairman / CEO | — | G5 / G4 | View via Governance Reports | Not this URL |
| All others | — | — | — | Redirected |

> **Access enforcement:** `@require_role('library_learning_head')` with server-side action gating. View-only roles see no create, edit, distribute, archive, or fulfil controls.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Library & Learning Resources Head Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                        [+ Add Resource]  [Export Usage Report ↓]
[Group Name] — Library & Learning Resources Head · Last login: [date time]
[N] Resources in Catalogue  ·  [N] Branches with Access  ·  [N] Downloads This Month
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with zero resource access this month | "[N] branch(es) have not accessed any resources this month." | Amber |
| Resource access expiry approaching | "[N] resource distribution assignment(s) expire within 7 days." | Amber |
| Resource request awaiting approval | "[N] new resource requests from branches are pending." | Amber |
| Storage quota above 80% | "Group digital storage is at [N]% capacity. Review and archive unused resources." | Amber |

---

## 4. KPI Summary Bar (6 cards)

Six KPI cards in a responsive row. All metrics reflect the currently selected Academic Year (default: current AY). Each card is HTMX-loaded independently; OOB swap occurs when the AY selector changes.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Resources | Active resources in central catalogue | COUNT of resources where status = Active | Blue always | `#kpi-card-1` |
| 2 | Branches with Active Access | Branches with at least 1 resource distributed | COUNT of branches with ≥ 1 non-expired distribution assignment | Green = all · Yellow = 1–3 without access · Red = 4+ | `#kpi-card-2` |
| 3 | Downloads This Month | Total resource download/access events this month | SUM of access_event records where month = current calendar month | Blue always | `#kpi-card-3` |
| 4 | Pending Resource Requests | Requests from branch librarians for new resources | COUNT of resource_requests where status = Pending | Green = 0 · Yellow 1–5 · Red > 5 | `#kpi-card-4` |
| 5 | Resources Added This Month | New resources added to catalogue in current month | COUNT of resources where created_at month = current calendar month | Blue always | `#kpi-card-5` |
| 6 | Expiring Assignments (7d) | Distribution assignments expiring within 7 days | COUNT of distribution_assignments where expiry_date ≤ today + 7 days | Green = 0 · Yellow > 0 | `#kpi-card-6` |

**HTMX:** Each card uses `hx-trigger="load"` `hx-get="/api/v1/group/{id}/library/head/kpi/"` targeting its own `hx-target` (per card above) with `hx-swap="outerHTML"`. Auto-refresh: `hx-trigger="every 5m"` on `#kpi-bar`. On AY selector change, custom JS fires `htmx.trigger('#kpi-bar', 'ayChanged')` which triggers an OOB swap refreshing all 6 cards simultaneously.

**Drill-down:** Card 1 → E-Library Catalogue page 17 · Card 2 → Content Distribution page 18 · Card 3 → Analytics page 20 · Card 4 → Section 5.3 · Card 5 → E-Library Catalogue page 17 · Card 6 → Content Distribution page 18.

---

## 5. Sections

### 5.1 Recently Added Resources

> New catalogue entries from the last 30 days.

**Display:** Table — max 10 rows, "View All →" to page 17.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Resource Title | Text + link | ✅ | Opens `resource-edit` drawer |
| Type | Badge | ✅ | E-Book · Video Lecture · Question Bank · Past Paper · Reference · Revision Notes · Worksheet |
| Subject | Badge | ✅ | e.g. Mathematics · Physics · English |
| Class | Badge | ✅ | Class 6–12 · Integrated |
| Added On | Date | ✅ | |
| Distributed To | Number | ✅ | Count of branches with access |
| Downloads | Number | ✅ | Total accesses since added |
| Actions | — | ❌ | [Edit] · [Distribute] · [Archive] |

**[Distribute] action:** Opens the `resource-distribute` modal (480px, centred). See Section 6.5.

---

### 5.2 Branch Access Overview

> Which branches have access to how many resources.

**Search:** Branch name. Debounce 300ms.

**Filters:** State, Access Level (High/Medium/Low), Resources Count.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text + link | ✅ | |
| City | Text | ✅ | |
| Resources Assigned | Number | ✅ | Total resources distributed to branch |
| Downloads (Month) | Number | ✅ | This month's accesses |
| Last Access | Date + relative | ✅ | Red if > 30 days |
| Expiring Soon | Number | ✅ | Assignments expiring in 7 days — badge if > 0 |
| Actions | — | ❌ | View Assigned · Renew Expiring |

**Default sort:** Downloads (Month) ascending (least active first).

**Pagination:** 25/page.

---

### 5.3 Resource Request Queue

> Branch librarians requesting addition of new resources to the catalogue.

**Display:** Table — max 8 rows, "View All" link.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | ✅ | e.g. RR-2026-015 |
| Branch | Text | ✅ | |
| Resource Title / Description | Text | ✅ | What the branch needs |
| Type Requested | Badge | ✅ | E-Book · Video · Question Bank · etc. |
| Subject / Class | Text | ❌ | |
| Requested By | Text | ❌ | Branch librarian name |
| Days Pending | Number | ✅ | Red if > 14 |
| Actions | — | ❌ | [Fulfil] [Decline] [View] |

**[Fulfil] flow:**
1. Clicking [Fulfil] opens the `resource-create` drawer (680px) with request details pre-filled: Title, Type, Subject/Class are populated from the request record.
2. A blue informational banner appears at the top of the drawer: **"Fulfilling request [RR-XXXX] from [Branch Name] — resource will be auto-distributed to this branch on save."**
3. The Access tab is pre-set to "Selected Branches Only" with the requesting branch pre-selected. The Library Head may add additional branches but cannot remove the requesting branch.
4. On successful drawer submit: the resource is added to the catalogue, access is automatically granted to the requesting branch (and any additionally selected branches), the request status changes from Pending to Fulfilled, and a success toast fires.

**[Decline]:** Opens `request-decline` modal — reason field (min 20 chars) + alternative suggestion (optional).

---

### 5.4 Top Resources by Usage (this month)

**Display:** Compact ranked list — top 8 resources.

**Fields per item:** Rank · Resource title · Type badge · Subject · Downloads this month · Trend vs last month (↑↓).

**"View Full Analytics →"** link to page 20.

---

## 6. Drawers & Modals

### 6.1 Drawer: `resource-create` — Add New Resource
- **Trigger:** [+ Add Resource] header button · [Fulfil] in request queue
- **Width:** 680px
- **Tabs:** Metadata · File · Classification · Access

When opened via [Fulfil], a banner at the top of the drawer (above the tab bar) reads:
> **"Fulfilling request [RR-XXXX] from [Branch Name] — resource will be auto-distributed to this branch on save."**

#### Tab: Metadata
| Field | Type | Required | Validation |
|---|---|---|---|
| Title | Text | ✅ | Min 3, max 200 chars |
| Description | Textarea | ❌ | Max 500 chars |
| Resource Type | Select | ✅ | E-Book · Video Lecture · Question Bank · Past Paper · Reference · Revision Notes · Worksheet · Audio |
| Author / Source | Text | ❌ | Max 150 chars |
| Publisher | Text | ❌ | |
| Publication Year | Year | ❌ | |
| Language | Select | ✅ | Telugu · English · Hindi · Other |
| Tags | Multi-input | ❌ | Freeform tags — comma-separated |

#### Tab: File
| Field | Type | Required | Validation |
|---|---|---|---|
| Upload File | File upload | Conditional | PDF/MP4/DOCX/ZIP — max 500MB per file |
| External URL | URL | Conditional | If hosted externally (YouTube/Drive) — required if no file uploaded |
| Thumbnail | Image upload | ❌ | JPG/PNG, max 2MB, recommended 800×600 |
| File Size (auto) | Read-only | — | Auto-calculated |

> One of File or External URL is required.

#### Tab: Classification
| Field | Type | Required | Validation |
|---|---|---|---|
| Subject | Multi-select | ✅ | Mathematics · Physics · Chemistry · Biology · English · Telugu · Social Studies · Commerce · Computer Science · etc. |
| Class / Grade | Multi-select | ✅ | Class 6 · 7 · 8 · 9 · 10 · 11 · 12 · Integrated |
| Stream | Multi-select | ❌ | MPC · BiPC · MEC · CEC · HEC · IIT Foundation |
| Difficulty Level | Select | ❌ | Beginner · Intermediate · Advanced |
| Curriculum Alignment | Select | ❌ | CBSE · State Board (AP) · State Board (TS) · Both |
| Exam Relevance | Multi-select | ❌ | JEE · NEET · EAMCET · SSC CGL · Board Exam |

#### Tab: Access
| Field | Type | Required | Validation |
|---|---|---|---|
| Access Type | Radio | ✅ | All Branches · Selected Branches Only · Restricted |
| Select Branches | Multi-select | Conditional | If Selected Branches chosen |
| Access Expiry | Date | ❌ | Leave blank = permanent |
| Student Access | Toggle | ✅ | Default On — students can access |
| Staff Only | Toggle | ❌ | Only teachers / faculty can access |

**Submit:** "Add to Catalogue" — disabled until Metadata + File + Classification tabs valid.
**On success:** Resource added to catalogue, access assigned per Tab settings, auto-distribution to requesting branch (if via Fulfil flow), toast fires.

---

### 6.2 Drawer: `resource-edit`
- **Width:** 680px — same 4 tabs, pre-filled
- **Version note in Metadata tab:** "Editing this resource creates a new version. Previous version retained."

---

### 6.3 Modal: `request-decline`
- **Width:** 420px
- **Fields:** Decline reason (required, min 20 chars) · Alternative resource suggestion (optional, links to catalogue search)
- **Buttons:** [Decline Request] (danger) + [Cancel]

---

### 6.4 Modal: `resource-archive`
- **Width:** 380px
- **Content:** "Archive [Resource Title]? It will no longer appear in branch access lists."
- **Buttons:** [Archive] (warning yellow) + [Cancel]

---

### 6.5 Modal: `resource-distribute`
- **Width:** 480px
- **Trigger:** [Distribute] action in Section 5.1 recently-added table
- **Title:** "Distribute [Resource Title]"

| Field | Type | Required | Notes |
|---|---|---|---|
| Select Branches | Multi-select | ✅ | All active branches; searchable; shows current distribution status per branch |
| Access Type | Radio | ✅ | Full Access · View Only · Download Disabled |
| Expiry Date | Date picker | ❌ | Leave blank = permanent access |

- **Submit button:** "Distribute to [N] Branch(es)" — disabled until at least one branch selected.
- **On success:** Distribution assignments created for selected branches; toast fires; "Distributed To" count in Section 5.1 table updates via OOB swap.

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button (top-right corner of each chart card).

### 7.1 Monthly Download Trend (last 6 months)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Monthly Resource Downloads — Last 6 Months" |
| X-axis | Last 6 months (MMM YYYY) |
| Y-axis | Access count |
| Line colour | Blue with filled area below line |
| Tooltip | "[Month]: Total accesses: [N] · Unique resources: [N] · Unique branches: [N]" |
| Empty state | "No download data available for the selected period." |
| API endpoint | `GET /api/v1/group/{id}/library/analytics/monthly-downloads/` |
| HTMX trigger | `hx-trigger="load"` `hx-get="…/library/analytics/monthly-downloads/"` `hx-target="#chart-monthly-downloads"` `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Resource Distribution by Type

| Property | Value |
|---|---|
| Chart type | Doughnut |
| Title | "Resources by Type — Catalogue" |
| Segments | E-Book · Video Lecture · Question Bank · Past Paper · Reference · Revision Notes · Other |
| Centre label | Total resources |
| Tooltip | "[Type]: [N] resources ([X]%)" |
| Empty state | "No resources in catalogue yet." |
| API endpoint | `GET /api/v1/group/{id}/library/analytics/type-distribution/` |
| HTMX trigger | `hx-trigger="load"` `hx-get="…/library/analytics/type-distribution/"` `hx-target="#chart-type-distribution"` `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Resource added | "Resource [Title] added to catalogue. Access assigned to [N] branches." | Success | 4s |
| Resource updated | "Resource [Title] updated. Version [N] saved." | Success | 4s |
| Resource archived | "[Title] archived and removed from branch access." | Warning | 6s |
| Request fulfilled | "Resource request [RR-XXXX] fulfilled. [Branch] notified and access granted." | Success | 4s |
| Request declined | "Request declined. Branch notified with reason." | Success | 4s |
| Distribution saved | "[Title] distributed to [N] branch(es)." | Success | 4s |
| File too large | "File exceeds 500MB limit. Compress or use an external URL." | Warning | 6s |
| Export started | "Usage report generating…" | Info | 4s |
| Validation error — required fields | "Please complete all required fields before saving." | Error | 6s |
| API error | "Something went wrong. Please try again or contact support." | Error | 8s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No resources in catalogue | `library-empty` | "Catalogue is empty" | "Add your first digital resource to the central library" | [+ Add Resource] |
| No pending requests | `inbox-check` | "No resource requests pending" | "Branch requests for new resources will appear here" | — |
| No downloads this month | `chart-empty` | "No access activity this month" | "Resource download data will appear once branches start accessing the library" | — |
| No recently added resources | `upload-empty` | "No resources added recently" | "Resources added in the last 30 days will appear here" | [+ Add Resource] |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: 6 KPI cards + resources table (5 rows) + branch table (5 rows) + request table (5 rows) + 2 chart placeholders |
| Table filter/search | Inline skeleton rows |
| Resource create drawer open | Spinner in drawer |
| File upload (in drawer) | Progress bar in file upload field |
| Submit resource | Spinner in submit button |
| KPI auto-refresh | Shimmer on card values |
| Distribute modal open | Spinner in modal |
| Chart load | Per-chart skeleton (grey rounded rectangle with spinner) |

---

## 11. Role-Based UI Visibility

| Element | Library Head G2 (101) | Academic Dir G3 (read) | Others |
|---|---|---|---|
| Page | ✅ | ✅ read-only via own dashboard | ❌ redirect |
| [+ Add Resource] header button | ✅ | ❌ | ❌ |
| [Fulfil] / [Decline] requests | ✅ | ❌ | ❌ |
| [Distribute] on resources | ✅ | ❌ | ❌ |
| [Edit] on catalogue resources | ✅ | ❌ | ❌ |
| [Archive] on resources | ✅ | ❌ | ❌ |
| [Export Usage Report] | ✅ | ✅ | ❌ |
| Branch access table (view) | ✅ | ✅ | ❌ |

> G2 can manage content; cannot access user provisioning, finance, compliance, or HR pages.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/library/head/dashboard/` | JWT (G2 Library) | Full dashboard |
| GET | `/api/v1/group/{id}/library/head/kpi/` | JWT (G2) | KPI auto-refresh |
| GET | `/api/v1/group/{id}/library/resources/?recent=true&days=30` | JWT (G2) | Recently added resources |
| GET | `/api/v1/group/{id}/library/branches/access/` | JWT (G2) | Branch access overview |
| GET | `/api/v1/group/{id}/library/requests/?status=pending` | JWT (G2) | Resource request queue |
| POST | `/api/v1/group/{id}/library/resources/` | JWT (G2) | Add resource to catalogue |
| PUT | `/api/v1/group/{id}/library/resources/{rid}/` | JWT (G2) | Update resource |
| POST | `/api/v1/group/{id}/library/resources/{rid}/archive/` | JWT (G2) | Archive resource |
| POST | `/api/v1/group/{id}/library/resources/{rid}/distribute/` | JWT (G2) | Distribute resource to branches |
| POST | `/api/v1/group/{id}/library/requests/{reqid}/fulfil/` | JWT (G2) | Fulfil resource request (creates resource + auto-distributes) |
| POST | `/api/v1/group/{id}/library/requests/{reqid}/decline/` | JWT (G2) | Decline request with reason |
| GET | `/api/v1/group/{id}/library/resources/top-usage/?month=current` | JWT (G2) | Top 8 resources this month |
| GET | `/api/v1/group/{id}/library/analytics/monthly-downloads/` | JWT (G2) | Download trend chart data |
| GET | `/api/v1/group/{id}/library/analytics/type-distribution/` | JWT (G2) | Catalogue type distribution chart data |

**`POST /api/v1/group/{id}/library/resources/{rid}/distribute/` — request body:**

| Field | Type | Required | Notes |
|---|---|---|---|
| `branch_ids` | int[] | ✅ | IDs of branches to distribute to |
| `access_type` | str | ✅ | `full` · `view_only` · `no_download` |
| `expiry_date` | date | ❌ | ISO 8601 date string; null = permanent |

**Response:** `{ "created": N, "updated": N, "branches": [...] }` — number of new and updated distribution assignments.

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load | `load` | GET `.../library/head/kpi/` | `#kpi-bar` | `innerHTML` | Fires on page load |
| KPI auto-refresh | `every 5m` | GET `.../library/head/kpi/` | `#kpi-bar` | `innerHTML` | Keeps metrics live |
| KPI OOB on AY change | `ayChanged from:body` | GET `.../library/head/kpi/?ay={ay}` | `#kpi-bar` | `outerHTML` | OOB swap — all 6 cards |
| Branch access table search | `input delay:300ms` | GET `.../library/branches/access/?q=` | `#branch-table-body` | `innerHTML` | Debounced search |
| Branch table pagination | `click` | GET `.../library/branches/access/?page={n}` | `#branch-table-section` | `innerHTML` | Server-side pagination |
| Request queue filter | `click` | GET `.../library/requests/?status=pending&filters=` | `#request-table-section` | `innerHTML` | Filter chip apply |
| Open resource create drawer | `click` | GET `.../library/resources/create-form/` | `#drawer-body` | `innerHTML` | Via [+ Add Resource] |
| Open resource-create (Fulfil) | `click` | GET `.../library/requests/{id}/fulfil-form/` | `#drawer-body` | `innerHTML` | Pre-fills from request; shows banner |
| Submit resource form | `submit` | POST `.../library/resources/` | `#drawer-body` | `innerHTML` | Validates tabs before enable |
| Archive confirm submit | `click` | POST `.../library/resources/{rid}/archive/` | `#resource-row-{rid}` | `outerHTML` | Removes row; fires toast |
| Open distribute modal | `click` | GET `.../library/resources/{rid}/distribute-form/` | `#modal-body` | `innerHTML` | Via [Distribute] in table |
| Submit distribute modal | `submit` | POST `.../library/resources/{rid}/distribute/` | `#modal-body` | `innerHTML` | On success: OOB swap updates distributed-to count |
| Chart 7.1 load | `load` | GET `.../library/analytics/monthly-downloads/` | `#chart-monthly-downloads` | `innerHTML` | Per-chart independent load |
| Chart 7.2 load | `load` | GET `.../library/analytics/type-distribution/` | `#chart-type-distribution` | `innerHTML` | Per-chart independent load |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
