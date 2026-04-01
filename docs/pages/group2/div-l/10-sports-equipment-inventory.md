# 10 — Sports Equipment Inventory

> **URL:** `/group/sports/equipment/`
> **File:** `10-sports-equipment-inventory.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Sports Coordinator G3 (Role 98, full — manage inventory and approve branch requests) · Sports Director G3 (Role 97, view + approve large purchases)

---

## 1. Purpose

Group-wide inventory of sports equipment across all branches. Every branch maintains its own physical equipment — balls, bats, nets, protective gear, track and field apparatus, mats, and more — but the Sports Coordinator at group level oversees stock levels, condition grades, audit compliance, and procurement requests flowing up from branches. When a branch raises an equipment request, it goes to the Sports Coordinator for review and recommendation, who then forwards approved requests to the Group Procurement function. The Sports Director holds a view role on day-to-day inventory but must be looped in for large-value or urgent procurement decisions. Scale: 20–200 equipment types per branch × up to 50 branches = up to 10,000 equipment line items group-wide, making search, pagination, and branch-level filtering critical for usability. Last audit dates older than 180 days are flagged red to prompt branch-level re-auditing before tournaments.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Sports Director | 97 | G3 | View inventory + approve large purchase requests | Cannot create items or log maintenance; can approve procurement requests flagged as Urgent |
| Sports Coordinator | 98 | G3 | Full — create inventory items, log maintenance, approve or decline branch requests, recommend procurement | Primary operator of this page |
| Cultural Activities Head | 99 | G3 | No access | 403 on direct URL |
| NSS/NCC Coordinator | 100 | G3 | No access | 403 on direct URL |
| Library Head | 101 | G2 | No access | 403 on direct URL |
| Branch Sports Teacher | Branch staff | Branch | No access to this group page | Submits requests via branch portal only |
| All other roles | — | — | No access | 403 on direct URL |

> **Access enforcement:** Django decorator `@require_role(['sports_coordinator'])` on all write, maintenance-log, and request-management endpoints. `@require_role(['sports_director', 'sports_coordinator'])` on all read and KPI endpoints. Role 97 receives a server-rendered page with all create, edit, log-maintenance, and decline buttons omitted; only [View] and [Approve] (Urgent) are visible.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Sports & Extra-Curricular  ›  Sports Equipment Inventory
```

### 3.2 Page Header
```
Sports Equipment Inventory                    [+ Add Inventory Item]  [Export ↓]
[N] Item Types  ·  [N] Branches with Inventory  ·  [N] Requests Pending  ·  [N] Condemned Items
```

`[+ Add Inventory Item]` — opens `inventory-item-create` drawer (Role 98 only).
`[Export ↓]` — exports filtered inventory to XLSX/PDF; available to Roles 97 and 98.

**Subtitle bar:** Branch selector (multi-select; default = All Branches). Changing selection reloads Section 5.1 via HTMX. Sports Coordinator sees all branches; no restriction.

**Stats bar values:**
- **N Item Types** — count of distinct equipment line items group-wide across selected branches
- **N Branches with Inventory** — count of branches with at least one inventory record logged
- **N Requests Pending** — count of branch procurement requests with status = Pending
- **N Condemned Items** — count of inventory items where Condition = Condemned

### 3.3 Alert Banners

Stacked above the KPI bar. Each banner individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Condemned items in inventory (non-zero) | "[N] item(s) across [B] branch(es) are condemned and should be removed from active stock." | Red |
| Equipment requests overdue > 14 days | "[N] procurement request(s) have been pending for more than 14 days without a decision." | Red |
| Branch with zero equipment records | "[N] branch(es) have no equipment items logged in the inventory." | Amber |
| Maintenance due (items > 2 years old in poor condition) | "[N] item(s) purchased over 2 years ago are in Poor condition and are due for maintenance or replacement review." | Amber |
| Items not audited in > 180 days | "[N] item(s) have not been audited in more than 180 days. Schedule a branch audit." | Amber |
| No inventory items in system | "No equipment has been logged in the inventory. Add the first item to begin." | Blue |

---

## 4. KPI Summary Bar

Five cards displayed horizontally below the alert banners. Auto-refresh every 5 minutes via HTMX polling (`hx-trigger="every 5m"`).

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Item Types | Count of distinct equipment line items across selected branches | `COUNT(DISTINCT item_name + branch_id)` from inventory table, filtered by branch selector | Blue (neutral) | `#kpi-total-items` |
| 2 | Items Due for Replacement | Count of items where Condition = Poor or Condemned | `COUNT(*) WHERE condition IN ('poor','condemned')` | Red if > 0; Green if 0 | `#kpi-replacement` |
| 3 | Pending Requests | Count of branch procurement requests in Pending status | `COUNT(*) WHERE request_status = 'pending'` | Red if > 5; Amber if 1–5; Green if 0 | `#kpi-pending-requests` |
| 4 | Branches with Zero Equipment Logged | Count of branches with no inventory records | `COUNT(branches) WHERE equipment_count = 0` | Red if > 0; Green if 0 | `#kpi-zero-branches` |
| 5 | Items Under Maintenance | Count of items with an open maintenance log (not yet resolved) | `COUNT(*) WHERE maintenance_status = 'open'` | Amber if > 0; Green if 0 | `#kpi-maintenance` |

**KPI bar HTMX:** `<div id="kpi-bar" hx-get="/api/v1/group/{gid}/sports/equipment/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`. Each card shimmers on first load.

---

## 5. Sections

### 5.1 Equipment Inventory

**Display note:** Main inventory table below the KPI bar. Shows all equipment items for the branches selected in the subtitle bar selector. Row selection enabled for bulk export.

**Search:** Item name, sport name, branch name. Debounce 300 ms. Cleared with × icon.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches in group |
| Sport | Multi-select | All sports (dynamic from sport master) |
| Category | Multi-select | Ball Equipment · Protective Gear · Track & Field · Net · Goal · Mat · Other |
| Condition | Multi-select | Good · Fair · Poor · Condemned |
| Stock Level | Select | All · Normal · Low (< 50% of standard quantity) · Critical (≤ 2 units) |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Item Name | Text + link | Yes | Opens `inventory-item-detail` modal (read-only view) |
| Sport | Badge (colour-coded) | Yes | |
| Category | Text | Yes | |
| Branch | Text + link | Yes | Links to branch detail page |
| Quantity Total | Number | Yes | Total items logged |
| Quantity Available | Number | Yes | Total minus items in maintenance or condemned |
| Condition | Badge | Yes | Good (green) · Fair (yellow) · Poor (orange) · Condemned (red) |
| Last Audit Date | Date | Yes | Red text if > 180 days ago; "Never" if no audit logged |
| Actions | Button group | No | View · Edit · Log Maintenance · Request Procurement |

**Action notes:**
- View — always visible to Roles 97 and 98; opens 480 px item detail modal (read-only)
- Edit — Role 98 only; opens `inventory-item-create` drawer in edit mode
- Log Maintenance — Role 98 only; opens `maintenance-log` modal pre-filled with item details
- Request Procurement — Role 98 only; opens `equipment-request` drawer pre-filled with item details

**Default sort:** Condition ascending (Condemned first, then Poor, then Fair, then Good) so worst-condition items surface first.

**Pagination:** Server-side · 25 rows per page.

---

### 5.2 Pending Equipment Requests

**Display note:** Separate table section below Section 5.1. Header: "Branch Equipment Requests — [N] Pending". Shows all branch-originated procurement requests awaiting Coordinator decision. Always visible when Pending count > 0; collapsible when count = 0.

**Search:** Item name, branch name. Debounce 300 ms.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Priority | Multi-select | Urgent · Normal |
| Sport | Multi-select | All sports |

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Text | No | Auto-generated reference (e.g. REQ-2026-0041) |
| Branch | Text | Yes | |
| Item Requested | Text | Yes | |
| Sport | Badge | Yes | |
| Quantity | Number | Yes | |
| Justification | Text (truncated) | No | First 80 characters; [More] expands inline |
| Priority | Badge | Yes | Urgent (red) · Normal (grey) |
| Submitted By | Text | Yes | Staff name |
| Days Pending | Number | Yes | Red if > 7 days; bold red if > 14 days |
| Actions | Button group | No | Approve · Decline · View |

**Action notes:**
- Approve — Role 98 (normal requests); Role 97 and 98 (Urgent requests) — opens `approve-request` modal (420 px): Request summary, Recommended Supplier (text, optional), Notes (textarea, optional), [Confirm Approval] (green) / [Cancel]
- Decline — Role 98 — opens `decline-request` modal (420 px): Decline Reason (textarea, required, min 20 characters), [Confirm Decline] (red danger) / [Cancel]
- View — always; opens full request detail in 480 px modal including all justification text and any uploaded files

**Default sort:** Days Pending descending (longest-pending first).

**Pagination:** Server-side · 25 rows per page.

---

## 6. Drawers & Modals

### Drawer: `equipment-request`
- **Trigger:** [Request Procurement] row action in Section 5.1, or standalone request from branch staff
- **Width:** 480 px
- **Tabs:** Item · Quantity · Branch · Justification

#### Tab: Item
| Field | Type | Required | Validation |
|---|---|---|---|
| Item Name | Text | Yes | Min 3, max 150 characters |
| Sport | Select | Yes | From sport master |
| Category | Select | Yes | Ball Equipment · Protective Gear · Track & Field · Net · Goal · Mat · Other |
| Unit | Select | Yes | Piece · Set · Pair · Kit |

#### Tab: Quantity
| Field | Type | Required | Validation |
|---|---|---|---|
| Quantity Requested | Number | Yes | Integer ≥ 1 |
| Estimated Unit Cost | Currency (INR) | No | Positive decimal; used for procurement budgeting |
| Preferred Brand | Text | No | Max 100 characters |

#### Tab: Branch
| Field | Type | Required | Validation |
|---|---|---|---|
| Branch | Select | Yes | Pre-filled if request originated from a branch item row; otherwise required select |
| Delivery Address | Textarea | No | Max 300 characters |

#### Tab: Justification
| Field | Type | Required | Validation |
|---|---|---|---|
| Reason for Request | Textarea | Yes | Min 30, max 500 characters |
| Priority | Select | Yes | Urgent · Normal |
| Supporting Evidence | File upload | No | PDF or image (JPG/PNG); max 5 MB |

**Loader:** Spinner centred in drawer body while form initialises. File upload shows progress bar below the file upload field during upload.

---

### Drawer: `inventory-item-create`
- **Trigger:** `[+ Add Inventory Item]` header button, or [Edit] row action
- **Width:** 480 px
- **Tabs:** None (single-page form)

| Field | Type | Required | Validation |
|---|---|---|---|
| Item Name | Text | Yes | Min 3, max 150 characters |
| Sport | Select | Yes | From sport master |
| Category | Select | Yes | Ball Equipment · Protective Gear · Track & Field · Net · Goal · Mat · Other |
| Branch | Select | Yes | From group branch list |
| Quantity | Number | Yes | Integer ≥ 1 |
| Condition | Select | Yes | Good · Fair · Poor · Condemned |
| Purchase Date | Date | No | Must not be in the future |
| Supplier | Text | No | Max 150 characters |
| Cost Per Unit | Currency (INR) | No | Positive decimal |
| Location / Storage | Text | No | Max 100 characters (e.g. "Sports Store Room B2") |
| Notes | Textarea | No | Max 300 characters |

**Buttons:** [Save Item] (primary) · [Cancel] (ghost). Inline validation on all required fields before submit. [Save Item] disabled with spinner during submission.

---

### Modal: `maintenance-log`
- **Width:** 420 px
- **Item details pre-filled:** Item Name, Branch, Sport, Current Condition — displayed read-only at top of modal.

| Field | Type | Required | Validation |
|---|---|---|---|
| Issue Description | Textarea | Yes | Min 20, max 500 characters |
| Action Taken | Select | Yes | Repaired · Replaced · Condemned · Cleaned |
| Date | Date | Yes | Must not be in the future |
| Cost | Currency (INR) | No | Positive decimal |
| Next Service Date | Date | No | Must be after Date field |

**Buttons:** [Save Log] (primary) · [Cancel] (ghost). [Save Log] shows spinner and becomes disabled during submit.

On save: If Action Taken = Condemned, the item's Condition in inventory is updated to Condemned automatically. A confirmation note is shown: "This item will be marked as Condemned in the inventory."

---

## 7. Charts

Charts appear in a two-column row below the KPI bar and above the equipment inventory table. A `[▸ Hide Charts]` / `[▾ Show Charts]` toggle collapses this row.

### 7.1 Equipment by Condition per Branch — Stacked Bar Chart

| Property | Value |
|---|---|
| Chart type | Vertical stacked bar (Chart.js 4.x) |
| Title | "Equipment Condition by Branch" |
| Data | For each branch: count of items in each condition (Good / Fair / Poor / Condemned); top 15 branches by total item count shown; `[Show All]` expands |
| X-axis | Branch names (abbreviated) |
| Y-axis | Item count |
| Stacked series | Good (green) · Fair (yellow) · Poor (orange) · Condemned (red) |
| Tooltip | "[Branch]: Good [N] · Fair [N] · Poor [N] · Condemned [N]" |
| Empty state | "No inventory data available for the selected branches." |
| Export | PNG export button in top-right corner of chart card |
| API endpoint | `GET /api/v1/group/{gid}/sports/equipment/charts/condition-by-branch/` |
| HTMX | `<div id="chart-condition-branch" hx-get="/api/v1/group/{gid}/sports/equipment/charts/condition-by-branch/" hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-condition-spinner">` |

### 7.2 Equipment Requests Trend — Bar Chart (Last 6 Months)

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Equipment Requests — Last 6 Months" |
| Data | Count of procurement requests submitted per calendar month for the last 6 months |
| X-axis | Month labels (MMM YYYY); last 6 calendar months |
| Y-axis | Request count |
| Bar colour | Indigo; bars split by status: Pending (amber) · Approved (green) · Declined (red) — stacked |
| Tooltip | "[Month]: Pending [N] · Approved [N] · Declined [N]" |
| Empty state | "No procurement requests in the last 6 months." |
| Export | PNG export button in top-right corner of chart card |
| API endpoint | `GET /api/v1/group/{gid}/sports/equipment/charts/requests-trend/` |
| HTMX | `<div id="chart-requests-trend" hx-get="/api/v1/group/{gid}/sports/equipment/charts/requests-trend/" hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-requests-spinner">` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Inventory item created | "[Item Name] added to inventory for [Branch]." | Success | 4 s |
| Inventory item updated | "[Item Name] updated." | Success | 4 s |
| Item condemned (via maintenance log) | "[Item Name] has been marked as Condemned." | Warning | 6 s |
| Maintenance log saved | "Maintenance log saved for [Item Name] at [Branch]." | Info | 4 s |
| Procurement request created | "Equipment request submitted for [Item Name] — [Branch]." | Success | 4 s |
| Request approved | "Request [REQ-ID] approved. Branch notified." | Success | 4 s |
| Request declined | "Request [REQ-ID] declined. Branch notified with reason." | Info | 4 s |
| Validation error | "Please correct the highlighted fields before saving." | Error | 5 s |
| Export complete | "Inventory exported to [format]." | Success | 4 s |
| Network / server error | "Could not save. Please try again." | Error | 5 s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No inventory items in system | `archive-box` | "No equipment logged" | "Add sports equipment items to begin tracking inventory across branches." | [+ Add Inventory Item] |
| No items match filters | `funnel` | "No items found" | "Try adjusting the branch, sport, category, or condition filters." | [Clear Filters] |
| No pending requests (Section 5.2) | `check-circle` | "No pending requests" | "All branch equipment requests have been actioned." | — |
| Branch has zero items | `building-office` | "No equipment logged for this branch" | "Log the first inventory item for [Branch] or ask the branch to submit a procurement request." | [+ Add Inventory Item] |
| Charts — no data | `chart-bar` | "No data available" | "No inventory data available for the selected filters." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: KPI bar (5 cards) + stats bar + alert banners + charts row (2 shimmer rectangles) + Section 5.1 table (10 rows) + Section 5.2 table (5 rows) |
| Table filter or search change (Section 5.1) | Inline skeleton rows replacing Section 5.1 table body |
| Table filter or search change (Section 5.2) | Inline skeleton rows replacing Section 5.2 table body |
| KPI auto-refresh (every 5 min) | Spinner icon on each KPI card |
| Branch selector change | Spinner over Section 5.1 table while data reloads |
| Inventory item drawer open | Spinner centred in drawer body |
| Maintenance log modal open | Spinner in modal body while item data pre-fills |
| Request approve/decline submit | Spinner inside modal action button; button disabled during submit |
| File upload in equipment-request | Progress bar below file upload field |
| [Save Item] form submission | Button disabled + spinner inside button label |
| [Save Log] form submission | Button disabled + spinner inside button label |
| Chart initial load | Per-chart shimmer rectangle with centred spinner |

---

## 11. Role-Based UI Visibility

| Element | Sports Director G3 (97) | Sports Coordinator G3 (98) |
|---|---|---|
| [+ Add Inventory Item] | Hidden | Visible |
| [Export ↓] | Visible | Visible |
| [Edit] row action (Section 5.1) | Hidden | Visible |
| [Log Maintenance] row action | Hidden | Visible |
| [Request Procurement] row action | Hidden | Visible |
| [Approve] in Section 5.2 (Urgent requests) | Visible | Visible |
| [Approve] in Section 5.2 (Normal requests) | Hidden | Visible |
| [Decline] in Section 5.2 | Hidden | Visible |
| [View] in Section 5.2 | Visible | Visible |
| KPI drill-down links | Visible | Visible |
| Branch selector subtitle bar | Visible (read/filter) | Visible (read/filter) |
| Charts row | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{gid}/sports/equipment/` | JWT (Role 97, 98) | Paginated equipment inventory with filters |
| POST | `/api/v1/group/{gid}/sports/equipment/` | JWT (Role 98) | Create inventory item |
| GET | `/api/v1/group/{gid}/sports/equipment/{eid}/` | JWT (Role 97, 98) | Item detail |
| PUT | `/api/v1/group/{gid}/sports/equipment/{eid}/` | JWT (Role 98) | Update inventory item |
| DELETE | `/api/v1/group/{gid}/sports/equipment/{eid}/` | JWT (Role 98) | Delete item (only if no maintenance history) |
| POST | `/api/v1/group/{gid}/sports/equipment/{eid}/maintenance/` | JWT (Role 98) | Log maintenance entry |
| GET | `/api/v1/group/{gid}/sports/equipment/{eid}/maintenance/` | JWT (Role 97, 98) | Maintenance history for item |
| GET | `/api/v1/group/{gid}/sports/equipment/requests/` | JWT (Role 97, 98) | Paginated procurement requests with filters |
| POST | `/api/v1/group/{gid}/sports/equipment/requests/` | JWT (Role 98) | Submit procurement request |
| GET | `/api/v1/group/{gid}/sports/equipment/requests/{rid}/` | JWT (Role 97, 98) | Request detail |
| POST | `/api/v1/group/{gid}/sports/equipment/requests/{rid}/approve/` | JWT (Role 97, 98) | Approve request |
| POST | `/api/v1/group/{gid}/sports/equipment/requests/{rid}/decline/` | JWT (Role 98) | Decline request with reason |
| GET | `/api/v1/group/{gid}/sports/equipment/kpi/` | JWT (Role 97, 98) | KPI card values |
| GET | `/api/v1/group/{gid}/sports/equipment/charts/condition-by-branch/` | JWT (Role 97, 98) | Chart 7.1 data — condition breakdown per branch |
| GET | `/api/v1/group/{gid}/sports/equipment/charts/requests-trend/` | JWT (Role 97, 98) | Chart 7.2 data — request counts last 6 months |

**Query parameters for inventory list:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Branch IDs; comma-separated |
| `sport` | str[] | Sport slugs |
| `category` | str[] | Category slugs |
| `condition` | str[] | `good` · `fair` · `poor` · `condemned` |
| `stock_level` | str | `normal` · `low` · `critical` |
| `search` | str | Item name, sport, branch name |
| `page` | int | Default 1 |
| `page_size` | int | Default 25, max 100 |
| `ordering` | str | Column field; prefix `-` for descending |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="kpi-bar">` | GET `/api/v1/group/{gid}/sports/equipment/kpi/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"`; shimmer on first load |
| Stats bar load | `<div id="stats-bar">` | GET `/api/v1/group/{gid}/sports/equipment/kpi/` | `#stats-bar` | `innerHTML` | `hx-trigger="load"` alongside KPI bar; updates header stat counts |
| Chart 7.1 load | `<div id="chart-condition-branch">` | GET `/api/v1/group/{gid}/sports/equipment/charts/condition-by-branch/` | `#chart-condition-branch` | `innerHTML` | `hx-trigger="load"`; shimmer until response |
| Chart 7.2 load | `<div id="chart-requests-trend">` | GET `/api/v1/group/{gid}/sports/equipment/charts/requests-trend/` | `#chart-requests-trend` | `innerHTML` | `hx-trigger="load"`; shimmer until response |
| Item name / sport / branch search (§5.1) | `<input id="inventory-search">` | GET `/api/v1/group/{gid}/sports/equipment/?q={val}` | `#inventory-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Filter apply (§5.1) | Filter dropdowns | GET `/api/v1/group/{gid}/sports/equipment/?filters={encoded}` | `#inventory-table-section` | `innerHTML` | `hx-trigger="change"` |
| Branch selector change | `<select id="branch-selector">` | GET `/api/v1/group/{gid}/sports/equipment/?branches={encoded}` | `#inventory-table-section` | `innerHTML` | `hx-trigger="change"`; also refreshes stats bar |
| Pagination (§5.1) | Pagination buttons | GET `/api/v1/group/{gid}/sports/equipment/?page={n}` | `#inventory-table-section` | `innerHTML` | `hx-trigger="click"` |
| Search (§5.2 requests) | `<input id="requests-search">` | GET `/api/v1/group/{gid}/sports/equipment/requests/?q={val}` | `#requests-table-body` | `innerHTML` | `hx-trigger="input delay:300ms"` |
| Filter apply (§5.2) | Filter dropdowns | GET `/api/v1/group/{gid}/sports/equipment/requests/?filters={encoded}` | `#requests-table-section` | `innerHTML` | `hx-trigger="change"` |
| Pagination (§5.2) | Pagination buttons | GET `/api/v1/group/{gid}/sports/equipment/requests/?page={n}` | `#requests-table-section` | `innerHTML` | `hx-trigger="click"` |
| Open inventory item drawer | [Edit] / [+ Add] button | GET `/api/v1/group/{gid}/sports/equipment/{eid}/drawer/` | `#drawer-body` | `innerHTML` | `hx-trigger="click"` |
| Approve request inline | [Approve] button | POST `/api/v1/group/{gid}/sports/equipment/requests/{rid}/approve/` | `#request-row-{rid}` | `outerHTML` | `hx-trigger="click"`; button disabled + spinner during submit |

---

*Page spec version: 1.1 · Last updated: 2026-03-21*
