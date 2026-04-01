# 18 — Digital Content Distribution

> **URL:** `/group/library/distribution/`
> **File:** `18-digital-content-distribution.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Group Library Head (Role 101, G2) — full access

---

## 1. Purpose

Manages the lifecycle of resource distribution assignments — controlling which resources are accessible at which branches, for how long, and to whom. A distribution assignment is the formal link between one or more catalogue resources and one or more branches, with an optional expiry date and access configuration.

The Library Head uses this page to:
- Create new distribution assignments linking resources to branches
- Monitor the status of all active, expiring, and expired assignments
- Renew expiring or expired assignments in bulk
- Revoke access when resources are withdrawn or reassigned
- Handle incoming branch requests for specific resources
- Inspect the distribution matrix to identify under-served or over-served branches

Scale: Up to 10,000 resources × 50 branches; 50–500 new or renewed assignments per month.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Library Head | G2 | Full — create, edit, renew, revoke, export, fulfil requests | Primary owner; all branches |
| All other Group roles | — | No access to this page | Branch-level distribution managed by branch portals |

> **Access enforcement:** `@require_role('group_library_head')` on all views and API endpoints for this page.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Library  ›  Digital Content Distribution
```

### 3.2 Page Header
- **Title:** `Digital Content Distribution`
- **Subtitle:** Stats Bar (inline, replaces KPI cards — see section 4)
- **Right controls:** `+ New Assignment` · `Advanced Filters` · `Export Assignments ↓`

> **Stats Bar** — Four inline non-clickable metrics displayed in a single row directly below the page title:
>
> | Metric | Label | Colour |
> |---|---|---|
> | Total Active Assignments | Assignments where Status = Active and expiry is future (or permanent) | Green text |
> | Expiring This Week | Assignments expiring within 7 days | Amber text |
> | Expired (Not Renewed) | Assignments past expiry date with no renewal | Red text |
> | Pending Branch Requests | Requests with Status = Pending | Blue text |
>
> Rendered as: `Active Assignments: 1,204 · Expiring This Week: 18 · Expired: 43 · Pending Requests: 7`
> HTMX-loaded on page load; refreshes after any assignment action.

### 3.3 Alert Banners

| Condition | Banner Text | Severity |
|---|---|---|
| Expiring within 7 days > 0 | "[N] distribution assignment(s) expire within 7 days. Renew them to maintain student access." | Amber |
| Expired not renewed > 10 | "[N] assignments have expired and not been renewed. Students at affected branches have lost access." | Red |
| Branch requests pending > 14 days | "[N] branch resource requests have been pending for more than 14 days." | Amber |
| Bulk renew job completed | "Bulk renewal completed: [N] assignments renewed successfully." | Info (dismissible) |

---

## 4. KPI Summary Bar

> **Note:** This page intentionally omits a KPI card grid. The compact inline Stats Bar (described in section 3.2) is used instead, consistent with page 17's design. HTMX refreshes Stats Bar values on page load and after every assignment action (create, edit, renew, revoke).

---

## 5. Sections

### 5.1 Active Distribution Assignments

Primary view. Full-feature table showing all distribution assignments.

#### View Toggle
A segmented toggle control in the table header allows switching between two views:
- **Assignment List** (default) — row-per-assignment table described below
- **Branch Access Matrix** — described in section 5.2

#### Search
Search by resource title. Debounce 300 ms.

#### Filter Drawer
Active filter chips appear below search bar.

| Filter | Type | Options |
|---|---|---|
| Resource Type | Multi-select | All 10 resource types |
| Expiry Status | Multi-select | Active / Expiring This Week (≤ 7 days) / Expiring This Month (≤ 30 days) / Expired |
| Branch | Multi-select | All active branches |
| Access Type | Radio | All / All Branches / Selected Branches |
| Expiry Date Range | Date range picker | From – To |

#### Table Columns

| Column | Sortable | Notes |
|---|---|---|
| ☐ Select | ❌ | Checkbox for bulk operations |
| Resource Title | ✅ | Truncated at 55 chars; full title on hover; click opens assignment-edit drawer |
| Type | ✅ | Colour badge matching catalogue (page 17) |
| Assigned Branches | ✅ | Integer count; clicking the count opens an inline tooltip/popover listing branch names |
| Assigned On | ✅ | DD-MMM-YYYY |
| Expiry Date | ✅ | Green = Permanent (no expiry set); Yellow = expiring in 8–30 days; Amber = expiring in 1–7 days; Red = expired; shown as DD-MMM-YYYY or "Permanent" |
| Access Type | ✅ | "All Branches" (teal) / "Selected Branches" (blue) badge |
| Downloads | ✅ | Cumulative downloads attributed to this assignment across all assigned branches |
| Actions | ❌ | View · Edit · Renew · Revoke |

**Default sort:** Expiry Date ASC (soonest expiry / expired first).
**Pagination:** Server-side, 25 rows/page.
**Row shading:** Expired rows have a red left border and muted background; permanent rows have a green left border.
**Bulk action when rows selected:** `Bulk Renew Selected` button appears in sticky bar above the table.

---

### 5.2 Branch Access Matrix

Accessible via the view toggle in section 5.1.

Provides a high-level view of branch coverage by resource type.

**Layout:** Heat-table (colour-coded grid).
- **Rows:** All active branches (sorted alphabetically by branch name)
- **Columns:** All 10 resource types + an "Overall" column
- **Cell value:** Count of active resources of that type currently assigned to that branch
- **Cell colour:**
  - Green — ≥ 10 resources
  - Yellow/Orange — 1–9 resources
  - Grey / Red — 0 resources (no coverage)
- **Cell click:** Opens `branch-division-drilldown` drawer (480px) showing the specific resources assigned, their titles, expiry dates, and download counts for that branch + resource type combination

**Filters above matrix:** Branch State (multi-select) · Branch Type (Day School / Residential / Both)

**Legend:** Shown below matrix — Green (10+) · Yellow (1–9) · Red (0 — no coverage)

**Export:** `Export Matrix ↓` button exports the matrix as an Excel file with colour formatting.

---

### 5.3 Branch Resource Requests

Separate section below the distribution table. Accessible by scrolling or via a quick-link in the page header nav.

Branch librarians (branch-level role) can submit resource requests through their branch portal; they appear here for the Library Head to fulfil or decline.

#### Search
Search by request ID, branch name, resource title.

#### Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Type | Multi-select | All resource types |
| Status | Multi-select | Pending / Fulfilled / Declined |
| Priority | Multi-select | Low / Medium / High / Urgent |
| Date Submitted | Date range picker | From – To |
| Days Pending | Number range | Min – Max days |

#### Table Columns

| Column | Sortable | Notes |
|---|---|---|
| Request ID | ✅ | System-generated (e.g., LRQ-2026-00041) |
| Branch | ✅ | Branch name |
| Resource Requested | ✅ | Free-text description or title entered by branch; truncated at 60 chars |
| Type | ✅ | Resource type badge (as entered/selected by branch) |
| Subject | ✅ | Subject tags |
| Class | ✅ | Class/grade tags |
| Priority | ✅ | Low (grey) / Medium (blue) / High (orange) / Urgent (red) badge |
| Requested By | ✅ | Name + role of branch staff who submitted |
| Submitted Date | ✅ | DD-MMM-YYYY |
| Days Pending | ✅ | Integer; red text if > 14 days |
| Status | ✅ | Pending (blue) / Fulfilled (green) / Declined (grey) badge |
| Actions | ❌ | Fulfil · Decline · View |

**Default sort:** Days Pending DESC (most overdue first).
**Pagination:** Server-side, 25 rows/page.

---

## 6. Drawers & Modals

### 6.1 Drawer — `distribution-assign` (480px, right side)

Triggered by **+ New Assignment** button or **Distribute** action on page 17.

**Tabs:** Resource · Branches · Access

---

#### Tab 1 — Resource

| Field | Type | Validation |
|---|---|---|
| Select Resources | Searchable multi-select | Required; min 1 resource; search pulls from active catalogue (title + type + subject tags displayed per result); recent resources shown by default (last 20 added or last 20 distributed) |
| Quick Add from Recent | Expandable list | Optional; shows 10 most recently distributed resources as one-click add chips |
| Resource preview | Read-only area | Shows selected resource(s) as removable chips with type badge and subject tags |

---

#### Tab 2 — Branches

| Field | Type | Validation |
|---|---|---|
| Assign To | Radio | Required; All Branches / Selected Branches |
| Select Branches | Multi-select | Conditional — required when Assign To = Selected Branches; lists all active branches with state indicated |
| Preview | Read-only | Auto-updates: "[N] branches will receive access to [M] resources" |

---

#### Tab 3 — Access

| Field | Type | Validation |
|---|---|---|
| Access Start Date | Date picker | Required; defaults to today; cannot be a past date |
| Access Expiry Date | Date picker | Optional; blank = permanent access; must be after Access Start Date |
| Student Access | Toggle | Default ON |
| Staff Only Mode | Toggle | Default OFF; if ON, overrides Student Access |
| Notify Branch Staff? | Toggle | Default ON; sends WhatsApp + email notification to branch library staff when assignment is saved |

**Confirmation Preview (shown before final submit):**
> `"You are assigning [M] resources to [N] branches. [P] students will gain access. Access starts [date] and expires [date / never]. [Notification: Yes/No]."`
> Library Head must click **Confirm & Assign** to proceed, or **Back** to revise.

**Footer:** `Cancel` · `Review & Assign` → on click shows confirmation preview → `Confirm & Assign` + `Back`

---

### 6.2 Drawer — `assignment-edit` (480px, right side)

Triggered by **Edit** in the Actions column.

Identical 3-tab structure to `distribution-assign`, pre-filled with existing assignment values.

**Additional controls per tab:**
- Tab 1 (Resource): Add More Resources (opens resource search to append more) · Remove individual resources (× button on each chip)
- Tab 2 (Branches): Add Branches / Remove Branches from current assignment
- Tab 3 (Access): Modify expiry date, toggle notifications for the change

**Footer:** `Cancel` · `Save Changes`

---

### 6.3 Modal — `bulk-renew` (420px, centred)

Triggered by **Bulk Renew Selected** button (when rows selected) or **Renew** action on individual row.

| Field | Type | Validation |
|---|---|---|
| Selected assignments | Read-only | "[N] assignments selected for renewal" with resource title list (max 5 shown, "+N more" for overflow) |
| New Expiry Date | Date picker | Required; must be a future date; minimum today + 1 day |
| Notify Branches | Toggle | Default ON; sends notification to affected branches |
| Confirmation | Read-only text | "Renewing these assignments will extend access to [total students approx] students across [N] branches." |

**Footer:** `Cancel` · `Renew All`

---

### 6.4 Modal — `revoke-confirm` (380px, centred)

Triggered by **Revoke** in the Actions column.

| Element | Detail |
|---|---|
| Warning icon + heading | "Revoke Resource Access?" |
| Resource name | Full title of the resource |
| Impact statement | "Revoking access will remove this resource from [N] branches immediately. Students currently accessing this resource will lose access." |
| Notify branches | Toggle — default ON — sends notification to affected branches that access has been revoked |
| Reason for revocation | Single-select: Copyright Expiry / Resource Superseded / Error / Temporary Maintenance / Other | Optional |

**Footer:** `Cancel` · `Revoke Access` (destructive — red button)

---

### 6.5 Request Fulfil Flow

Triggered by **Fulfil** in the Branch Resource Requests table (section 5.3).

Opens the `distribution-assign` drawer (section 6.1) pre-configured:
- Tab 1: Resource search pre-filled with the request's title text; Library Head selects the matching resource(s) from catalogue
- Tab 2: The requesting branch pre-selected in "Selected Branches"
- Tab 3: Default access settings; Notify Branch Staff = ON

On successful assignment submit: the request record is automatically marked as Status = Fulfilled, the fulfil date is recorded, and the branch staff member who submitted the request receives a notification.

---

### 6.6 Modal — `request-decline` (380px, centred)

Triggered by **Decline** in the Branch Resource Requests table.

| Field | Type | Validation |
|---|---|---|
| Request ID | Read-only | |
| Branch | Read-only | |
| Resource requested | Read-only | |
| Decline reason | Textarea | Required; min 10, max 300 characters |
| Suggest alternative | Text input | Optional; Library Head can note a similar resource already available |
| Notify requester | Toggle | Default ON |

**Footer:** `Cancel` · `Decline Request`

---

### 6.7 Drawer — `branch-division-drilldown` (480px, right side)

Triggered by clicking a cell in the Branch Access Matrix (section 5.2).

**Header:** `[Branch Name] — [Resource Type] Resources`

**Tabs:** Summary · Details

#### Tab 1 — Summary
| Field | Notes |
|---|---|
| Branch name + state | Read-only |
| Resource type | Read-only badge |
| Total active resources assigned | Count |
| Total downloads from this branch | Cumulative |
| Oldest assignment date | DD-MMM-YYYY |
| Next expiry | Date of the earliest upcoming expiry for this branch + type combination |
| Status | Active / Partially Expiring / All Expired |

#### Tab 2 — Details
Table listing each resource of that type assigned to that branch:

| Column | Notes |
|---|---|
| Resource title | Truncated; link opens resource-edit drawer on page 17 |
| Assigned On | Date |
| Expiry Date | Colour-coded as per main table |
| Downloads (this branch) | Count |
| Actions | Edit Assignment · Renew · Revoke |

---

## 7. Charts

All charts use Chart.js 4.x, are fully responsive, use a colorblind-safe palette, include legend and tooltip with exact numbers, and each has a PNG export button.

Charts displayed in a 2-column responsive grid below the main sections.

### 7.1 Distribution Activity (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line |
| Title | "Assignment Activity — Last 6 Months" |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Count |
| Lines | Two lines: "New Assignments Created" (blue) · "Assignments Renewed" (green) |
| Data points | Markers on each month; tooltip shows both values |
| Tooltip | "[Month]: [N] created, [M] renewed" |
| API endpoint | `GET /api/v1/group/{group_id}/library/distribution/charts/activity/` |
| HTMX | Loaded on page load |

### 7.2 Top 10 Resources by Branch Coverage (Horizontal Bar Chart)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Top 10 Most Distributed Resources (Active Assignments)" |
| Y-axis | Resource titles (top 10 by branch count, sorted DESC) |
| X-axis | Number of branches with active assignment |
| Bar colour | Indigo |
| Tooltip | "[Resource title]: distributed to [N] branches" |
| Notes | Only active assignments counted; ties broken alphabetically |
| API endpoint | `GET /api/v1/group/{group_id}/library/distribution/charts/top-resources/` |
| HTMX | Loaded on page load; refreshes after any assignment change |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Assignment created | "Resources assigned to [N] branch(es) successfully." | Success |
| Assignment created + notification sent | "Resources assigned. Branch staff have been notified." | Success |
| Assignment edited | "Assignment updated successfully." | Success |
| Assignment renewed (single) | "Assignment renewed. New expiry: [date]." | Success |
| Bulk renew complete | "[N] assignments renewed successfully." | Success |
| Assignment revoked | "Access revoked for '[Resource]' from [N] branch(es)." | Info |
| Request fulfilled | "Request [ID] fulfilled. Branch has been notified." | Success |
| Request declined | "Request [ID] declined. Branch has been notified." | Info |
| Notification sent to branches | "Distribution notification sent to [N] branch(es)." | Info |
| Export triggered | "Export is being prepared. Download will begin shortly." | Info |
| Validation error (no resource) | "Please select at least one resource before saving." | Error |
| Validation error (no branches) | "Please select branches or choose 'All Branches'." | Error |
| Validation error (expiry past) | "Access expiry date must be in the future." | Error |
| Revoke confirmed | "Access revoked successfully. Affected branches have been notified." | Warning |

---

## 9. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No assignments at all | "No distribution assignments yet." | "Assign resources from the catalogue to branches to give students access." | `+ New Assignment` button |
| No results for current filters | "No assignments match the current filters." | "Try adjusting or clearing your filters." | `Clear Filters` button |
| No expiring assignments | "No assignments expiring soon." | "All active assignments have ample time remaining." | — |
| No branch requests | "No branch resource requests." | "Requests submitted by branch librarians will appear here." | — |
| Branch Access Matrix — no data for branch | "No resources assigned to this branch yet." | "Create a distribution assignment to give this branch access to catalogue resources." | `+ New Assignment` button |
| Branch drilldown drawer — no resources for type | "No [Type] resources assigned to this branch." | "Assign resources of this type from the catalogue." | `+ New Assignment` button |
| Chart — no activity data | "No assignment activity in the last 6 months." | "Activity data will appear once assignments are created." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: stats bar placeholder + table (10 grey rows × 9 columns) + request table (5 grey rows) + 2 chart placeholders |
| Filter / search apply | Table body spinner overlay; stats bar reloads after table resolves |
| View toggle (List ↔ Matrix) | Matrix skeleton: grey grid of rows × columns with spinner overlay |
| Drawer open | Drawer skeleton: tab bar + 4 grey field blocks |
| Branch drilldown drawer open | Skeleton: 2 tab headers + 5 grey field rows in Summary |
| Bulk renew modal open | Spinner in modal content area; resolves to form |
| Assignment save / renew | Spinner in drawer/modal footer + "Saving…" label; button disabled |
| Notification dispatch | Inline spinner in Access tab next to Notify toggle: "Sending notifications…" → "Sent" |
| Export generation | Button spinner + "Preparing…" label; button disabled until download ready |
| Matrix cell drilldown | Drawer skeleton while fetching branch + type data |

---

## 11. Role-Based UI Visibility

| UI Element | Library Head (101) | All Other Roles |
|---|---|---|
| Entire page | ✅ Full access | ❌ No access — 403 |
| Stats Bar | ✅ | ❌ |
| + New Assignment button | ✅ | ❌ |
| Export Assignments | ✅ | ❌ |
| Advanced Filters | ✅ | ❌ |
| View toggle (List / Matrix) | ✅ | ❌ |
| Edit assignment | ✅ | ❌ |
| Renew assignment | ✅ | ❌ |
| Revoke assignment | ✅ | ❌ |
| Bulk Renew button | ✅ | ❌ |
| Fulfil request | ✅ | ❌ |
| Decline request | ✅ | ❌ |
| Branch Access Matrix export | ✅ | ❌ |
| All charts | ✅ | ❌ |
| Branch drilldown drawer | ✅ | ❌ |

---

## 12. API Endpoints

### Base URL: `/api/v1/group/{group_id}/library/distribution/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/library/distribution/` | List all assignments (paginated, filtered) | JWT + Library Head role |
| POST | `/api/v1/group/{group_id}/library/distribution/` | Create new distribution assignment | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/{assignment_id}/` | Retrieve assignment detail | Library Head |
| PATCH | `/api/v1/group/{group_id}/library/distribution/{assignment_id}/` | Edit assignment (branches / expiry / access) | Library Head |
| POST | `/api/v1/group/{group_id}/library/distribution/{assignment_id}/renew/` | Renew single assignment with new expiry | Library Head |
| POST | `/api/v1/group/{group_id}/library/distribution/{assignment_id}/revoke/` | Revoke assignment | Library Head |
| POST | `/api/v1/group/{group_id}/library/distribution/bulk-renew/` | Renew multiple assignments | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/matrix/` | Branch × resource-type coverage matrix data | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/matrix/{branch_id}/{resource_type}/` | Drilldown: resources of given type assigned to given branch | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/stats/` | Stats bar data (4 metrics) | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/requests/` | List branch resource requests (paginated, filtered) | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/requests/{request_id}/` | Retrieve request detail | Library Head |
| POST | `/api/v1/group/{group_id}/library/distribution/requests/{request_id}/fulfil/` | Mark request as fulfilled (triggers assignment) | Library Head |
| POST | `/api/v1/group/{group_id}/library/distribution/requests/{request_id}/decline/` | Decline request with reason | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/export/` | Export assignments as CSV | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/charts/activity/` | Chart 7.1 data | Library Head |
| GET | `/api/v1/group/{group_id}/library/distribution/charts/top-resources/` | Chart 7.2 data | Library Head |

**Query parameters for list endpoint (assignments):**

| Parameter | Type | Description |
|---|---|---|
| `resource_type` | str[] | Resource type slugs |
| `expiry_status` | str[] | `active`, `expiring_soon`, `expiring_week`, `expired` |
| `branch` | int[] | Branch IDs |
| `access_type` | str | `all_branches` or `selected_branches` |
| `expiry_from` | date | Expiry range start |
| `expiry_to` | date | Expiry range end |
| `search` | str | Resource title |
| `sort_by` | str | Column field; prefix `-` for descending |
| `page` | int | Page number (default 1) |
| `page_size` | int | Default 25, max 100 |

---

## 13. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Stats bar load | `hx-get="/api/.../distribution/stats/"` `hx-trigger="load"` `hx-target="#stats-bar"` | Stats bar populated on page load |
| Stats bar refresh | `hx-trigger="assignmentChanged from:body"` `hx-target="#stats-bar"` | Refreshes after any assignment action |
| Search input | `hx-get="/api/.../distribution/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#assignments-table-body"` `hx-include="#filter-form"` | Table body replaced |
| Filter apply | `hx-get="/api/.../distribution/"` `hx-trigger="change"` `hx-target="#assignments-table-body"` `hx-include="#filter-form"` | Table + stats bar refresh |
| Pagination | `hx-get="/api/.../distribution/?page={n}"` `hx-target="#assignments-table-body"` `hx-push-url="true"` | Page swap with URL update |
| View toggle to matrix | `hx-get="/api/.../distribution/matrix/"` `hx-trigger="click"` `hx-target="#view-container"` | Table replaced with heat-table matrix |
| View toggle to list | `hx-get="/api/.../distribution/"` `hx-trigger="click"` `hx-target="#view-container"` `hx-include="#filter-form"` | Matrix replaced with list |
| Matrix cell click | `hx-get="/api/.../distribution/matrix/{branch_id}/{resource_type}/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Drilldown drawer opens |
| New assignment drawer open | `hx-get="/ui/distribution/assign-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Empty 3-tab drawer slides in |
| Edit assignment drawer open | `hx-get="/ui/distribution/{assignment_id}/edit-form/"` `hx-trigger="click"` `hx-target="#drawer-container"` | Pre-filled drawer slides in |
| Assignment save | `hx-post="/api/.../distribution/"` `hx-target="#assignments-table-body"` `hx-swap="afterbegin"` `hx-on::after-request="closeDrawer(); fireToast(); refreshStatsBar();"` | New row prepended |
| Assignment edit save | `hx-patch="/api/.../distribution/{assignment_id}/"` `hx-target="#assignment-row-{assignment_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeDrawer(); fireToast();"` | Row updated in-place |
| Single renew | `hx-post="/api/.../distribution/{assignment_id}/renew/"` `hx-target="#assignment-row-{assignment_id}"` `hx-swap="outerHTML"` `hx-on::after-request="fireToast();"` | Row updated with new expiry date |
| Revoke confirm | `hx-post="/api/.../distribution/{assignment_id}/revoke/"` `hx-target="#assignment-row-{assignment_id}"` `hx-swap="outerHTML"` `hx-confirm=""` (handled by custom modal) `hx-on::after-request="closeModal(); fireToast();"` | Row removed or marked revoked |
| Row checkbox select | `hx-trigger="change"` `hx-target="#bulk-actions-bar"` `hx-get="/ui/bulk-bar/?selected={ids}"` | Bulk Renew bar appears |
| Bulk renew submit | `hx-post="/api/.../distribution/bulk-renew/"` `hx-target="#assignments-table-body"` `hx-include="#selected-ids,#bulk-renew-form"` `hx-on::after-request="closeModal(); fireToast(); refreshStatsBar();"` | All selected rows updated |
| Request table load | `hx-get="/api/.../distribution/requests/"` `hx-trigger="load"` `hx-target="#requests-table-body"` | Loaded independently on page load |
| Request search/filter | `hx-get="/api/.../distribution/requests/"` `hx-trigger="keyup changed delay:300ms, change"` `hx-target="#requests-table-body"` `hx-include="#request-filter-form"` | Request table body replaced |
| Fulfil request | `hx-get="/ui/distribution/assign-form/?prefill_request={request_id}"` `hx-trigger="click"` `hx-target="#drawer-container"` | Pre-filled assign drawer opens |
| Decline request modal | `hx-get="/ui/distribution/requests/{request_id}/decline-form/"` `hx-trigger="click"` `hx-target="#modal-container"` | Decline modal opens |
| Decline request submit | `hx-post="/api/.../distribution/requests/{request_id}/decline/"` `hx-target="#request-row-{request_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeModal(); fireToast();"` | Row status updated to Declined |
| Chart load | `hx-get="/api/.../distribution/charts/{chart_slug}/"` `hx-trigger="load"` `hx-target="#chart-{chart_slug}"` | Each chart loaded independently |
| Export trigger | `hx-get="/api/.../distribution/export/"` `hx-include="#filter-form"` `hx-trigger="click"` `hx-target="#export-status"` | Export job triggered |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
