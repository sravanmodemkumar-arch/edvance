# [03] — RTI Request Manager

> **URL:** `/group/legal/rti/`
> **File:** `n-03-rti-request-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group RTI Officer (Role 110, G1) — Right to Information Act 2005 request tracking and response management

---

## 1. Purpose

The RTI Request Manager handles the complete lifecycle of Right to Information Act 2005 requests received by the Institution Group. Under the RTI Act, any citizen can seek information from public authorities (including educational institutions receiving government aid or affiliation). The Group RTI Officer is the designated Public Information Officer (PIO) responsible for receiving, processing, and responding to all RTI applications within the legally mandated 30-day window (extendable to 45 days for requests involving third-party information).

Failure to respond within the deadline triggers automatic deemed-refusal status, entitling applicants to file First Appeals and Second Appeals to the Central/State Information Commission. Contempt proceedings and penalties of up to ₹25,000 (imposed on the PIO personally) can result from wilful non-compliance. This page ensures the Group RTI Officer never misses a deadline and maintains a full, auditable record of every request, response, and appeal.

The page also handles First Appellate Authority (FAA) appeals — where the applicant challenges the initial response — and tracks any Second Appeals filed with the Information Commission. All request details, response documents, and correspondence are stored in immutable audit-log format.

Scale: 5–50 branches · 5–100 RTI requests per year group-wide · 30-day statutory response window · Appeals tracked per request

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Advises on complex RTI responses externally |
| Group Compliance Manager | 109 | G1 | Read — Full Page | Oversight; views all requests and responses |
| Group RTI Officer | 110 | G1 | Read — Full Page + Upload Response | Primary user; uploads response documents |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | No role in RTI |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | Read — Limited | Views requests touching personal data/DPDP scope |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Full Page | Monitors requests that become appeals/litigation |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,110,113,128], min_level=G1)` on all views and API endpoints. G4/G5 have full read access.
>
> **Response upload:** Only Role 110 (RTI Officer) can upload response documents. G3 (Contract Admin) has no access. G4/G5 can upload in exceptional circumstances.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  RTI Request Manager
```

### 3.2 Page Header
```
RTI Request Manager                             [+ Record New Request]  [Export ↓]
Group RTI Officer — [Officer Name]
[Group Name] · [N] Requests This Year · [N] Pending · Last updated: [datetime]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any request overdue (> 30 days, no response) | "[N] RTI request(s) are overdue — response deadline passed. Immediate action required — RTI Act s.7(1)." | Critical (red) |
| Any request due within 5 days | "[N] RTI request(s) have response deadlines within 5 days." | High (amber) |
| Any First Appeal pending > 30 days | "[N] First Appeal(s) are pending response beyond 30-day FAA deadline." | High (amber) |
| Any Second Appeal filed with Information Commission | "Active Second Appeal(s) pending before State/Central Information Commission. Legal review recommended." | Medium (yellow) |
| New RTI request received today | "New RTI request received today — [Requester Name / Anonymous]. Review and assign." | Info (blue) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Requests (This FY) | Count | COUNT rti_requests WHERE fy = current_fy | Blue (static) | `#kpi-total-rti` |
| 2 | Pending Response | Count | COUNT WHERE status IN ('received','in_progress') | Red if any overdue within the set, Amber > 3, Green ≤ 3 | `#kpi-pending` |
| 3 | Overdue | Count | COUNT WHERE due_date < TODAY AND status != 'responded' | Red if > 0, Green = 0 | `#kpi-overdue` |
| 4 | Responded On Time | Count (this FY) | COUNT WHERE responded_date ≤ due_date | Green | `#kpi-on-time` |
| 5 | Requests — Information Denied | Count (this FY) | COUNT WHERE response_type = 'denial' | Amber if > 20% of total | `#kpi-denied` |
| 6 | First Appeals Active | Count | COUNT rti_appeals WHERE stage = 'first_appeal' AND status = 'open' | Red if > 0, Green = 0 | `#kpi-appeals` |
| 7 | Second Appeals (Info Commission) | Count | COUNT rti_appeals WHERE stage = 'second_appeal' AND status = 'open' | Red if > 0, Green = 0 | `#kpi-second-appeals` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/rti/kpis/"` with `hx-trigger="load, every 300s"` → `hx-target="#kpi-bar"` → `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 RTI Request List (Main Table)

All RTI requests received by the group. Primary working view for the RTI Officer.

**Search:** Free-text search on request ID, requester name, subject, branch concerned. Debounced 350ms.

**Filters:**
- Status: `All` · `Received` · `In Progress` · `Responded` · `Overdue` · `Denied` · `Transferred` · `Deemed Refusal`
- Branch Concerned: dropdown of all branches + "Group Level"
- Period: FY selector (current and last 3 FYs)
- Response Type: `All` · `Full Disclosure` · `Partial Disclosure` · `Denial` · `Transfer` · `No Information Held`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text (monospace) | Yes | Auto-generated: RTI-YYYY-NNNN |
| Received Date | Date | Yes | Date application was received by the group |
| Requester | Text | Yes | Requester name or "Anonymous" |
| Subject | Text | Yes | 80-char summary of information requested |
| Branch Concerned | Text | Yes | Which branch the request relates to, or "Group Level" |
| Due Date | Date | Yes | Received + 30 days; amber < 5d, red if passed |
| Days Left | Badge | Yes | Integer; red if negative (overdue) |
| Status | Badge | Yes | Received (grey) / In Progress (blue) / Responded (green) / Overdue (red) / Denied (orange) / **Deemed Refusal** (dark red — auto-set after 30-day deadline passes without response, per RTI Act s.7(2)) |
| Response Type | Badge | No | Full / Partial / Denial / Transfer / NIL — shown only when status = Responded/Denied |
| First Appeal | Badge | No | Shows if appeal filed: Pending / Decided |
| Actions | Buttons | No | [View] · [Upload Response] (Role 110 only) |

**Default sort:** Due Date ASC (most urgent first)
**Pagination:** Server-side · Default 25/page · Page size selector: 25/50/100

---

### 5.2 Appeals Register

Tracks First Appeals and Second Appeals for requests where the applicant challenged the response.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| RTI Request ID | Link | Yes | Links to parent request |
| Appeal Stage | Badge | Yes | First Appeal / Second Appeal (Info Commission) |
| Appeal Date | Date | Yes | Date appeal was filed |
| Appellant | Text | Yes | Requester name |
| FAA / Authority | Text | Yes | First Appellate Authority or Information Commission name |
| Due Date | Date | Yes | 30 days from appeal receipt for FAA response |
| Status | Badge | Yes | Pending / Decided / Dismissed / Penalty Imposed |
| Outcome | Text | No | Summary of appeal decision |
| Penalty Imposed | Currency | No | If any CIC/SIC penalty imposed; red if > 0 |

**Default sort:** Due Date ASC
**Pagination:** Server-side · Default 25/page

---

## 6. Drawers & Modals

### 6.1 Drawer: `rti-request-detail` (720px, right-slide)
Opens on [View] button or row click.

- **Tabs:** Overview · Correspondence · Documents · Response · Appeals · Timeline
- **Overview tab:**
  - Request ID, Received Date, Requester Name, Requester Contact (email/postal — masked to RTI Officer and above)
  - Subject of Information Request (full text)
  - Branch Concerned, Information Sought (full description)
  - Due Date (30 days), Extended Due Date (if third-party involved: +15 days), Days Remaining
  - PIO Assigned (RTI Officer name), Status badge
  - Fee Paid (if applicable — RTI fee ₹10 for general; BPL applicants exempt)
- **Correspondence tab:** All correspondence with requester (received letters, sent responses, acknowledgements) listed chronologically with download links
- **Documents tab:** All uploaded documents — original application, acknowledgement, response document, supporting records provided. Each: filename, upload date, uploader, file size, Download button
- **Response tab:**
  - Response Type selector (Full / Partial / Denial / Transfer / NIL)
  - If Denial: Exemption Section cited (RTI Act ss.8–9)
  - Response document upload (PDF only, max 20MB) — **only Role 110 and G4/G5**
  - Response date, mode of dispatch (email/post/in-person)
  - "Mark as Responded" button → changes status to Responded and logs timestamp
- **Appeals tab:** Any First Appeal or Second Appeal filed; outcome; penalty if any
- **Timeline tab:** Immutable audit log — every status change, document upload, user action with timestamp and user name

### 6.2 Modal: `record-rti-request` (620px)
Used to record a newly received RTI application.

| Field | Type | Required | Validation |
|---|---|---|---|
| Received Date | Date picker | Yes | Cannot be future date |
| Requester Name | Text | Yes | "Anonymous" option |
| Requester Contact | Text | No | Email or postal address |
| Subject | Text (80 chars) | Yes | Brief summary |
| Information Requested | Textarea | Yes | Full text of request; min 20 chars |
| Branch Concerned | Select (all branches + Group Level) | Yes | |
| Fee Paid | Toggle (Yes/No) | Yes | If Yes: amount field appears |
| Application Document | File upload | No | PDF/image, max 10MB |
| Notes | Textarea | No | Internal notes |

**Footer:** Cancel · Save Draft · Submit (calculates due date = received + 30d automatically)

### 6.3 Modal: `upload-rti-response` (560px)
Used by RTI Officer to record the response sent.

| Field | Type | Required | Validation |
|---|---|---|---|
| Response Date | Date picker | Yes | Cannot be future; cannot be before received date |
| Response Type | Select | Yes | Full Disclosure / Partial Disclosure / Denial / Transfer / No Information Held |
| Exemption Section (if Denial) | Select | Conditional | RTI Act s.8(1)(a) through s.9; multi-select |
| Transfer Authority (if Transfer) | Text | Conditional | Department/officer to whom transferred |
| Response Mode | Select | Yes | Email / Registered Post / In-Person |
| Response Document | File upload | Yes | PDF only, max 20MB |
| Notes | Textarea | No | Internal notes |

**Footer:** Cancel · Upload Response (POST → marks request as Responded)

---

## 7. Charts

### 7.1 RTI Response Timeline Compliance (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "RTI Response Rate — On Time vs Overdue (Last 12 Months)" |
| Data | Per month: count responded on time vs overdue |
| X-axis | Month (MMM YY) |
| Y-axis | Number of requests |
| Colour | On Time = `#22C55E`, Overdue = `#EF4444` |
| Tooltip | "[Month]: [N] on time · [N] overdue" |
| API endpoint | `GET /api/v1/group/{id}/legal/rti/response-rate-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-rti-response-rate"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Requests by Branch (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "RTI Requests by Branch — Current FY" |
| Data | Count of requests per branch (top 15; remainder grouped as "Others") |
| X-axis | Request count |
| Y-axis | Branch name |
| Colour | `#3B82F6` (single colour) |
| Tooltip | "[Branch]: [N] requests this FY" |
| API endpoint | `GET /api/v1/group/{id}/legal/rti/requests-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-rti-by-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| New request recorded | "RTI Request [RTI-YYYY-NNNN] recorded. Response due by [date]." | Success | 5s |
| Response uploaded | "Response uploaded for [RTI-YYYY-NNNN]. Request marked as Responded." | Success | 4s |
| Overdue alert | "RTI request [RTI-YYYY-NNNN] is now overdue — [N] days past deadline." | Error | 8s |
| Draft saved | "Draft saved for [RTI-YYYY-NNNN]." | Info | 3s |
| Export triggered | "Generating RTI register export…" | Info | 3s |
| Export ready | "RTI register export ready. Click to download." | Success | 6s |
| Filter applied | "Showing [N] requests: [filter description]" | Info | 2s |
| Validation error | "Please complete all required fields before submitting." | Error | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No RTI requests received this FY | `inbox` | "No RTI Requests This Year" | "No Right to Information requests have been received by the group this financial year." | Record First Request |
| Filter returns no matches | `search` | "No Matching Requests" | "No RTI requests match the selected filters." | Clear Filters |
| No appeals on record | `scale` | "No Appeals Filed" | "No First or Second Appeals have been filed against any RTI response." | — |
| All requests responded on time | `check-circle` | "Fully Compliant" | "All RTI requests have been responded to within the 30-day deadline." | View Archive |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI shimmer cards + 8-row table skeleton |
| Table search/filter change | Spinner overlay on table body; existing rows dimmed to 50% opacity |
| KPI auto-refresh | Shimmer pulse on card values only (not card shell) |
| Drawer open | Right-slide skeleton: tab bar + content area shimmer |
| Chart load (both charts) | Grey canvas placeholder with centred spinner |
| Upload response | Submit button spinner + disabled state |
| Export generation | Toast with "Generating…" progress indicator |

---

## 11. Role-Based UI Visibility

| Element | RTI Officer (110, G1) | Compliance Mgr (109, G1) | Legal Dispute (128, G1) | DPO (113, G1) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| Request list (all) | Visible | Visible | Visible | DPO-scope only | Visible |
| Appeals Register | Visible | Visible | Visible | Not visible | Visible |
| [+ Record New Request] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Upload Response] button | Visible | Not visible | Not visible | Not visible | Visible |
| Requester contact details | Visible (masked) | Visible (masked) | Visible (masked) | Not visible | Visible |
| Denial exemption section field | Visible | Visible (read-only) | Visible (read-only) | Not visible | Visible |
| Export button | Visible | Visible | Not visible | Not visible | Visible |
| Charts | Both visible | Both visible | Not visible | Not visible | Both visible |
| Timeline tab in drawer | Visible | Visible | Visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/rti/` | G1+ | Paginated RTI request list |
| POST | `/api/v1/group/{id}/legal/rti/` | Role 110, G4+ | Create new RTI request record |
| GET | `/api/v1/group/{id}/legal/rti/{req_id}/` | G1+ | Single request detail |
| POST | `/api/v1/group/{id}/legal/rti/{req_id}/response/` | Role 110, G4+ | Upload response document |
| GET | `/api/v1/group/{id}/legal/rti/kpis/` | G1+ | KPI summary bar values |
| GET | `/api/v1/group/{id}/legal/rti/appeals/` | G1+ | Appeals register list |
| GET | `/api/v1/group/{id}/legal/rti/response-rate-trend/` | G1+ | Chart data: monthly response rate |
| GET | `/api/v1/group/{id}/legal/rti/requests-by-branch/` | G1+ | Chart data: count by branch |
| POST | `/api/v1/group/{id}/legal/rti/export/` | G1+ | Trigger async export |
| GET | `/api/v1/group/{id}/legal/rti/{req_id}/timeline/` | G1+ | Audit timeline for one request |

### Query Parameters for RTI Request List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: request ID, requester name, subject |
| `status` | string | received / in_progress / responded / overdue / denied / transferred |
| `branch_id` | integer | Filter to specific branch |
| `response_type` | string | full / partial / denial / transfer / nil |
| `fy` | string | Financial year e.g. `2025-26`; defaults to current |
| `overdue_only` | boolean | true = show only overdue requests |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100; default 25 |
| `sort` | string | due_date / received_date / status / branch |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="kpi-bar">` | GET `.../rti/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table initial load | `<tbody id="rti-table-body">` | GET `.../rti/` | `#rti-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search requests | Search input | GET `.../rti/?q={value}` | `#rti-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Filter by status | Status chip buttons | GET `.../rti/?status={val}` | `#rti-table-body` | `innerHTML` | `hx-trigger="click"` |
| Filter by branch | Branch dropdown | GET `.../rti/?branch_id={id}` | `#rti-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open request drawer | Row click / [View] button | GET `.../rti/{req_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Drawer timeline tab | Tab click in drawer | GET `.../rti/{req_id}/timeline/` | `#drawer-tab-content` | `innerHTML` | Lazy-loaded on tab click |
| Open response upload modal | [Upload Response] button | GET `/htmx/legal/rti/{req_id}/response-form/` | `#modal-container` | `innerHTML` | Rendered as modal |
| Submit response | Response upload form | POST `.../rti/{req_id}/response/` | `#rti-row-{req_id}` | `outerHTML` | Row refreshes with new status |
| Load appeals table | `<tbody id="appeals-table-body">` | GET `.../rti/appeals/` | `#appeals-table-body` | `innerHTML` | `hx-trigger="load"` |
| Chart load | Both chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET `.../rti/?page={n}` | `#rti-table-body` | `innerHTML` | Replaces body only |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
