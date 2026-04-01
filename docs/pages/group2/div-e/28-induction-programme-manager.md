# 28 — Induction Programme Manager

- **URL:** `/group/hr/training/induction/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Training & Development Manager (Role 45, G2)

---

## 1. Purpose

The Induction Programme Manager is the central page for planning, scheduling, and tracking structured induction programmes for all new staff joiners across every branch in the group. Every staff member — teaching or non-teaching — is required to complete the group induction within their first 30 days of joining. Missing this window triggers an escalation to the HR Manager and HR Director.

The induction programme is split into two distinct tracks: Teaching Staff Track and Non-Teaching Staff Track. Each track has a fixed set of mandatory modules covering EduForge platform orientation, group policies and code of conduct, POCSO awareness (mandatory for all, completed before first day of student contact), child safeguarding principles, fire safety, and emergency evacuation procedures. An additional branch-specific orientation module is conducted by the branch principal at the local level within the first week.

The Training & Development Manager creates induction batches (groups of new joiners onboarded in the same month), assigns them to the correct track, and monitors module-by-module completion progress. Where a module is overdue — i.e., the staff member has not completed a required module and has crossed the 30-day mark — the system flags the case in amber or red depending on severity. POCSO awareness is treated as a P0 module: if any new joiner reaches student-contact status without completing the POCSO module, a non-dismissible red banner appears on this page and on the POCSO Coordinator's dashboard.

The T&D Manager uses this page to schedule induction batch sessions (classroom or virtual), send reminders to staff and branch admins, download completion certificates, and generate compliance reports for HR Director review at the end of each month.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Training & Development Manager | G2 | Full CRUD | Creates batches, assigns staff, tracks progress |
| Group HR Director | G3 | Read + Export | Reviews compliance, receives escalations |
| Group HR Manager | G3 | Read + Export | Monitors overdue cases |
| Group POCSO Coordinator | G3 | Read (POCSO module only) | Views POCSO completion status across branches |
| Group Performance Review Officer | G1 | No Access | Not applicable to this page |
| Branch Principal | Branch G3 | Read (own branch only) | Views induction status of own branch staff |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Training & Development > Induction Programme Manager`

### 3.2 Page Header
- **Title:** Induction Programme Manager
- **Subtitle:** Track new joiner induction completion across all branches
- **Actions (top-right):**
  - `+ Create Induction Batch` (primary button, opens create drawer)
  - `Export Report` (secondary button, downloads CSV/XLSX)
  - `Filter by Batch` (dropdown)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any new joiner in student contact without POCSO module complete | "CRITICAL: [N] staff member(s) are in student contact without POCSO awareness training. Immediate action required." | Red — non-dismissible |
| Induction overdue > 30 days for any staff | "WARNING: [N] staff member(s) have not completed induction within the 30-day window." | Amber — dismissible |
| New batch has unassigned staff | "INFO: Batch [Name] has [N] staff not yet assigned to a track." | Blue — dismissible |
| All active batches 100% complete | "All active induction batches are complete. No action required." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| New Joiners This Month | Count of staff with join date in current month | Blue always | Filters table to current month joiners |
| Induction Completed | Count with Completion % = 100 | Green if ≥ 80% of batch, Amber if 50–79%, Red if < 50% | Filters table to Status = Completed |
| Induction In Progress | Count with 1–99% completion | Blue always | Filters table to Status = In Progress |
| Induction Overdue | Count past 30 days with < 100% completion | Red if > 0, Green if 0 | Filters table to Status = Overdue |
| Completion Rate % | (Completed / Total New Joiners) × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | No drill-down |
| POCSO Module Completed | Count with POCSO module = Done | Red if any active joiner missing, Green if all done | Filters table to POCSO Status = Pending |

---

## 5. Main Table — New Joiner Induction Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Join Date | Date | Yes | Yes — date range |
| Staff Type | Badge (Teaching / Non-Teaching) | Yes | Yes — toggle |
| Induction Track | Text | No | Yes — dropdown |
| Module Progress | Fraction (e.g., 5/8 modules) | No | No |
| Days Since Join | Integer (auto-calculated) | Yes | Yes — range (0–30, 31–60, 61+) |
| Completion % | Progress bar + number | Yes | Yes — range |
| Status | Badge (Completed / In Progress / Overdue / Not Started) | No | Yes — multi-select |
| Actions | Icon buttons | No | No |

### 5.1 Filters
- **Batch:** dropdown of all active/past batches
- **Branch:** multi-select branch dropdown
- **Staff Type:** Teaching / Non-Teaching / All
- **Track:** Teaching Track / Non-Teaching Track / All
- **Status:** Not Started / In Progress / Completed / Overdue
- **Join Date Range:** date-picker from–to
- **POCSO Module Status:** Completed / Pending

### 5.2 Search
Free-text search on Staff Name and Branch. Triggers `hx-get` on keyup with 400 ms debounce. Clears with × icon.

### 5.3 Pagination
Server-side, 25 rows per page. Page number shown as `Showing X–Y of Z staff`. Previous / Next controls. Preserves active filters across pages.

---

## 6. Drawers

### 6.1 Create Induction Batch
**Trigger:** `+ Create Induction Batch` button
**Fields:**
- Batch Name (text, required, e.g., "March 2026 Joiners")
- Academic Year (dropdown, required)
- Branch(es) Included (multi-select)
- Join Date Range (date range picker, required)
- Auto-assign staff from join date range (toggle — if on, system pulls all staff with join date in range)
- Default Track Assignment (Teaching Track / Non-Teaching Track / Auto by role)
- Induction Start Date (date)
- Day-30 Deadline (auto-calculated from join date, editable)

### 6.2 View Induction Record
**Trigger:** Row click or eye icon
**Displays:** Staff profile summary, assigned track, each module name + status (Not Started / In Progress / Done), date completed per module, days since join, POCSO module highlighted, completion certificate download link (if 100% complete).

### 6.3 Edit Induction Record
**Trigger:** Edit icon (T&D Manager only)
**Editable:** Track reassignment, manual override of module status (with mandatory reason text), deadline extension (requires reason, auto-notifies HR Manager).

### 6.4 Delete Confirmation
Not applicable — induction records are permanent audit trail. Soft-archive only via Edit drawer (Status → Archived with reason). Archive prompts: "Are you sure you want to archive this induction record? This action cannot be undone."

---

## 7. Charts

**Induction Completion by Branch (Grouped Bar Chart)**
- X-axis: Branch names
- Y-axis: Staff count
- Series: Completed (green), In Progress (blue), Overdue (red), Not Started (grey)
- Tooltip: Hover shows exact counts and completion %
- Rendered: server-side, refreshed on filter change via HTMX `hx-get`

**Module-wise Completion Rate (Horizontal Bar Chart)**
- Each bar = one module (e.g., EduForge Orientation, POCSO Awareness, Fire Safety, etc.)
- Bar fill = % of assigned staff who completed that module
- POCSO bar highlighted in red/green with threshold marker at 100%

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Batch created | "Induction batch '[Name]' created successfully." | Success | 4s |
| Staff auto-assigned to batch | "[N] staff auto-assigned to batch '[Name]'." | Success | 4s |
| Module status overridden | "Module '[Name]' status updated for [Staff]." | Info | 4s |
| Deadline extended | "Induction deadline extended to [Date] for [Staff]." | Warning | 5s |
| Export triggered | "Induction report export started. Download will begin shortly." | Info | 4s |
| Error on batch creation | "Failed to create batch. Please check required fields." | Error | 6s |

---

## 9. Empty States

- **No new joiners this month:** "No new joiners found for the selected filters. Adjust the date range or batch selection."
- **No batches created yet:** "No induction batches created yet. Click '+ Create Induction Batch' to get started."
- **Batch has no staff assigned:** "This batch has no staff assigned. Use auto-assign or manually add staff."

---

## 10. Loader States

- Table skeleton: 6 placeholder rows with animated shimmer while data loads.
- KPI cards: skeleton rectangles with shimmer during initial page load.
- Drawer content: spinner centred in drawer while staff record or batch data loads.
- Chart area: grey placeholder rectangle with "Loading chart…" label.

---

## 11. Role-Based UI Visibility

| Element | T&D Manager (G2) | HR Director (G3) | POCSO Coordinator (G3) |
|---|---|---|---|
| Create Induction Batch button | Visible + enabled | Hidden | Hidden |
| Edit module status | Visible + enabled | Hidden | Hidden |
| Export Report button | Visible | Visible | Hidden |
| POCSO module filter | Visible | Visible | Visible |
| Delete / Archive record | Visible (Archive only) | Hidden | Hidden |
| View full induction record | Visible | Visible | POCSO module only |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/induction/batches/` | JWT G2+ | List all induction batches |
| POST | `/api/v1/hr/induction/batches/` | JWT G2 | Create a new induction batch |
| GET | `/api/v1/hr/induction/batches/{id}/` | JWT G2+ | Get batch details |
| PATCH | `/api/v1/hr/induction/batches/{id}/` | JWT G2 | Update batch metadata |
| GET | `/api/v1/hr/induction/staff/` | JWT G2+ | List staff induction records (paginated) |
| GET | `/api/v1/hr/induction/staff/{staff_id}/` | JWT G2+ | View individual induction record |
| PATCH | `/api/v1/hr/induction/staff/{staff_id}/modules/` | JWT G2 | Update module completion status |
| GET | `/api/v1/hr/induction/kpis/` | JWT G2+ | Fetch KPI summary bar data |
| GET | `/api/v1/hr/induction/export/` | JWT G2+ | Export induction report (CSV/XLSX) |
| GET | `/api/v1/hr/induction/charts/branch/` | JWT G2+ | Chart data: completion by branch |
| GET | `/api/v1/hr/induction/charts/modules/` | JWT G2+ | Chart data: module-wise completion rate |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search staff by name | keyup changed delay:400ms | GET `/api/v1/hr/induction/staff/?q={val}` | `#induction-table-body` | innerHTML |
| Filter change (branch/status/track) | change | GET `/api/v1/hr/induction/staff/?{params}` | `#induction-table-body` | innerHTML |
| Pagination page click | click | GET `/api/v1/hr/induction/staff/?page={n}` | `#induction-table-body` | innerHTML |
| Open create batch drawer | click | GET `/api/v1/hr/induction/batches/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/induction/staff/{id}/` | `#drawer-container` | innerHTML |
| Submit create batch form | submit | POST `/api/v1/hr/induction/batches/` | `#induction-table-body` | innerHTML |
| Refresh KPI bar | load | GET `/api/v1/hr/induction/kpis/` | `#kpi-bar` | innerHTML |
| Refresh charts on filter change | change | GET `/api/v1/hr/induction/charts/branch/?{params}` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
