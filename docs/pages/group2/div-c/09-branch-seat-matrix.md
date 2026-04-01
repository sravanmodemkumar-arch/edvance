# Page 09 — Branch Seat Matrix

- **URL:** `/group/adm/seat-matrix/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Branch Seat Matrix is the authoritative source of truth for seat availability across every branch, stream, and student type combination in the group. It is the foundation upon which all allocation decisions are made — without an accurate, up-to-date matrix, coordinators cannot tell applicants whether a seat exists, counsellors cannot set realistic expectations, and the Director cannot track group-level capacity utilisation. Every admission offer, allocation, and waitlist decision ultimately references this matrix.

The matrix distinguishes between multiple student categories: Day Scholar, Hosteler (AC), Hosteler (Non-AC), RTE quota, Scholarship reserved, and NRI quota. Each of these categories has its own seat count, its own fill rate, and its own compliance obligations. RTE quota in particular carries a legal mandate — the 25% rule — and the matrix tracks compliance with this mandate at the branch level so the Director can take corrective action before the admission cycle closes.

The Admissions Director owns configuration of the matrix and must approve any changes to seat counts. The Coordinator uses the read-only view of the matrix daily while making allocation decisions, looking up available seats per branch and stream. The matrix also feeds the Branch Seat Fill Rate Heatmap (Section 5.2), which gives the Director an immediate visual overview of which branches are approaching capacity and which have significant headroom. Historical fill trends (Section 5.5) allow year-on-year planning by revealing which streams consistently overfill and which chronically underperform.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full edit + approve seat changes | Only role that can modify seat counts and approve edit requests |
| Group Admission Coordinator (Role 24) | G3 | View + request seat changes | Can submit change requests; cannot directly edit counts |
| Group Admission Counsellor (Role 25) | G3 | View only | Read-only across all branches |
| Group Scholarship Manager (Role 27) | G3 | View only | Can see scholarship reserved seat counts |
| CEO / Executive | G3+ | View only | All branches and streams |
| CFO / Finance | G3+ | View only | For budgetary and capacity planning reference |

> **Enforcement:** All seat count edit controls are conditionally rendered server-side based on `request.user.role == 'admissions_director'`. Coordinator edit requests are submitted as `SeatChangeRequest` objects pending Director approval. Django views reject any direct seat count POST from non-Director roles with HTTP 403.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Branch Seat Matrix
```

### 3.2 Page Header
- **Title:** Branch Seat Matrix
- **Subtitle:** `{current_cycle_name}` — e.g., *Admission Cycle 2026–27*
- **Right-side actions:** `[Enable Edit Mode]` (Director only — activates inline editing in Section 5.3) · `[Export Matrix →]` · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Branch fill rate > 90% | "{N} branch(es) are over 90% full. Review capacity immediately." |
| RTE quota deficit detected | "{N} branch(es) are below mandated RTE quota. Compliance action required." |
| Pending seat change requests | "{N} seat change request(s) awaiting Director approval." |
| Branch fill rate < 50% with cycle closing in < 30 days | "{N} branch(es) are below 50% fill with {X} days left in the cycle. Marketing escalation recommended." |
| Edit mode active | "Seat edit mode is active. Changes will take effect after you save and confirm." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/kpis/" hx-trigger="every 5m" hx-target="#seat-matrix-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Seats (Group) | Sum of all seat counts across all branches, streams, types | `SeatMatrix.objects.aggregate(total=Sum('total_seats'))` | Neutral (blue) | Opens full matrix table |
| Total Enrolled | Sum of enrolled counts across all records | `Sum('enrolled')` | Neutral (blue) | Filters table to enrolled > 0 |
| Overall Fill % | `(total_enrolled / total_seats) * 100` | Computed | Green < 80%; amber 80–90%; red > 90% | Opens fill rate heatmap |
| Branches > 90% Full | Count of branches where any stream fill% > 90 | Computed per branch | Red if > 0; green if 0 | Filters heatmap to > 90% cells |
| Branches < 50% Full | Count of branches where any stream fill% < 50 | Computed per branch | Amber if > 0; green if 0 | Filters heatmap to < 50% cells |
| RTE Compliance | Count of branches meeting RTE 25% mandate | `rte_filled >= rte_mandated` per branch | Green = all compliant; red = any deficit | Opens RTE compliance summary (5.4) |

---

## 5. Sections

### 5.1 Seat Matrix Table

**Display:** Sortable, filterable table. One row per Branch + Stream + Student Type combination. Responsive horizontal scroll. Export-ready.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Stream | MPC / BiPC / MEC / CEC / General |
| Student Type | Day Scholar / Hosteler AC / Hosteler Non-AC / RTE / Scholarship / NRI |
| Total Seats | Configured seat count |
| Enrolled | Students currently enrolled in this slot |
| Reserved (RTE + Scholarship) | Sum of RTE and scholarship reserved seats |
| Available | `Total Seats − Enrolled` |
| Fill % | Progress bar + percentage; green < 70%, amber 70–89%, red ≥ 90% |
| [Edit Seats →] | Director only — opens seat-edit-drawer for this row |

**Filters:**
- Branch (multi-select)
- Stream (multi-select)
- Student Type (multi-select)
- Fill % range (slider: 0–100%)

**Bulk Action:** `[Export Matrix →]` — CSV of filtered rows

**HTMX Pattern:** Filter changes trigger `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/?{filters}"` `hx-target="#seat-matrix-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`

**Empty State:** Illustration of empty grid. Heading: "No Seat Configuration Found." Description: "Seat matrix has not been configured for this admission cycle. Contact the Admissions Director to set up the matrix." CTA: `[Configure Now →]` (Director only)

---

### 5.2 Fill Rate Heatmap

**Display:** Matrix visualisation — branches as rows, streams as columns, fill % value in each cell with a colour gradient background (white = 0%, light green = 50%, amber = 80%, red = 100%). Cells with no data show "—". Clicking a cell filters the main table to that branch+stream.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/heatmap/"` `hx-trigger="load"` `hx-target="#fill-rate-heatmap"` `hx-swap="innerHTML"`; cell click: `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/?branch={id}&stream={id}"` `hx-target="#seat-matrix-table-body"` `hx-swap="innerHTML"`

**Empty State:** "Heatmap unavailable — seat matrix not configured."

---

### 5.3 Seat Configuration Manager

**Display:** Shown only to Director. An `[Enable Edit Mode]` toggle switches the table rows from read-only to inline editable cells. In edit mode, Total Seats cells become `<input type="number">` fields. A `[Save All Changes]` button and a `[Cancel]` button appear in a sticky footer. Changes are submitted as a batch PATCH. A confirmation dialog summarises changes before final save.

**HTMX Pattern:** `[Enable Edit Mode]` click: `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/edit-mode/"` `hx-target="#seat-matrix-table-wrapper"` `hx-swap="innerHTML"`; Save: `hx-patch="/api/v1/group/{group_id}/adm/seat-matrix/bulk-update/"` `hx-target="#seat-matrix-table-wrapper"` `hx-swap="innerHTML"` `hx-confirm="Are you sure you want to update seat counts? This will affect active allocations."`

**Empty State (edit mode):** "No editable rows found for the selected filters."

---

### 5.4 RTE Quota Compliance Summary

**Display:** Dedicated table below the heatmap. One row per branch.

| Column | Notes |
|---|---|
| Branch | Branch name |
| RTE Mandated Seats | 25% of total general seats (auto-computed) |
| RTE Filled | Students enrolled under RTE category |
| Deficit | `Mandated − Filled` (0 if compliant) |
| Compliance Status | Badge: Compliant (green) / Deficit (red) / Surplus (blue) |
| [View Detail →] | Opens rte-compliance-detail drawer |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/"` `hx-trigger="load"` `hx-target="#rte-compliance-table"` `hx-swap="innerHTML"`

**Empty State:** "RTE compliance data unavailable. Ensure seat matrix is configured."

---

### 5.5 Historical Fill Trend

**Display:** Line chart (Chart.js 4.x). X-axis: admission cycles (last 3 years). Y-axis: fill % (0–100%). One line per branch (colour-coded legend). Hover tooltip shows exact fill % per cycle. Branch filter dropdown to narrow which branches are plotted.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/seat-matrix/fill-trend/?years=3"` `hx-trigger="load"` `hx-target="#fill-trend-chart-data"` `hx-swap="innerHTML"`; branch filter change: same endpoint with `&branch_ids={ids}`.

**Empty State:** "No historical data available. Fill trends will appear after the first completed admission cycle."

---

## 6. Drawers & Modals

### 6.1 Seat Edit Drawer
- **Width:** 560px (right-side slide-in)
- **Trigger:** `[Edit Seats →]` in matrix table row (Director only)
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/seat-matrix/{branch_id}/{stream}/edit/`

**Tabs:**

| Tab | Content |
|---|---|
| Edit Seats | Branch, Stream, Student Type (read-only); editable fields: Total Seats, RTE Reserved, Scholarship Reserved, NRI Quota; Justification textarea (required); effective date picker |
| Change History | Log of all previous seat count changes for this branch+stream: Date, Changed by, Old count, New count, Reason |

**Actions:** `[Save Changes]` (saves and sets status to Approved if Director; saves as pending request if Coordinator) · `[Cancel]`

---

### 6.2 RTE Compliance Detail Drawer
- **Width:** 480px
- **Trigger:** `[View Detail →]` in RTE compliance table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/{branch_id}/`

**Content:** Branch name, academic year, total general seats, 25% mandate calculation, list of RTE-enrolled students (name, class, stream, enrolment date), compliance gap narrative, `[Download RTE Report →]` button.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Seat counts saved (Director) | "Seat matrix updated for {Branch} — {Stream}." | Success | 4s |
| Change request submitted (Coordinator) | "Seat change request submitted for Director approval." | Info | 5s |
| Change request approved | "Seat change request approved. Matrix updated." | Success | 4s |
| Change request rejected | "Seat change request rejected. {Reason}" | Warning | 6s |
| Export started | "Matrix export is being prepared. Download will start shortly." | Info | 5s |
| Edit mode enabled | "Seat edit mode active. Remember to save before leaving." | Info | 4s |
| Invalid seat count entered | "Seat count cannot be less than current enrolled count ({N})." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No matrix configured | Empty grid graphic | "Seat Matrix Not Configured" | "No seat allocations have been set up for this admission cycle." | `[Configure Matrix →]` (Director only) |
| Filter returns no rows | Search-miss graphic | "No Matching Rows" | "No seat records match the selected branch, stream, or student type filters." | `[Clear Filters]` |
| No RTE compliance data | Scale/balance graphic | "No RTE Data" | "RTE compliance cannot be computed — seat matrix not configured." | `[Go to Configuration]` |
| No historical trend data | Chart graphic (empty) | "No Historical Data" | "Fill trend data will appear after the first completed cycle." | — |
| Heatmap — no data | Grid graphic | "Heatmap Unavailable" | "Configure the seat matrix to view fill rate heatmap." | `[Configure Matrix →]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (table rows + KPI bar shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Filter change (table) | Table body skeleton (5-row shimmer) |
| Heatmap load | Heatmap area spinner with "Loading heatmap…" label |
| RTE compliance table load | Table body skeleton |
| Historical fill trend chart load | Chart area spinner |
| Seat edit drawer open | Drawer content skeleton |
| Save seat changes | Button spinner + table overlay "Saving…" |
| Export generation | Button spinner; button disabled until complete |
| Edit mode activation | Table area overlay spinner "Enabling edit mode…" |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | Scholarship Mgr (27) | CFO | CEO |
|---|---|---|---|---|---|---|
| [Enable Edit Mode] button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| [Edit Seats →] column action | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Seat Configuration Manager section | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Change request status column | Visible | Visible | Hidden | Hidden | Hidden | Hidden |
| RTE Compliance Summary | Visible | Visible | Hidden | Hidden | Visible | Visible |
| Historical Fill Trend | Visible | Visible | Visible | Hidden | Visible | Visible |
| Fill Rate Heatmap | Visible | Visible | Visible | Hidden | Visible | Visible |
| [Export Matrix →] | Visible | Visible | Hidden | Hidden | Visible | Visible |
| Seat Matrix Table | Visible | Visible | Visible | Visible (scholarship rows) | Visible | Visible |
| Pending change requests badge | Visible | Visible (own requests) | Hidden | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/` | JWT G3+ | List seat matrix rows with filters |
| PATCH | `/api/v1/group/{group_id}/adm/seat-matrix/bulk-update/` | JWT G3 (Director) | Bulk update seat counts |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/heatmap/` | JWT G3+ | Heatmap data (branch × stream fill %) |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/` | JWT G3+ | RTE compliance table data |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/{branch_id}/` | JWT G3+ | RTE compliance detail for a branch |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/fill-trend/` | JWT G3+ | Historical fill % by branch (last N years) |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/{branch_id}/{stream}/edit/` | JWT G3 (Director) | Seat edit form for a branch+stream row |
| PATCH | `/api/v1/group/{group_id}/adm/seat-matrix/{branch_id}/{stream}/` | JWT G3 (Director) | Update seat counts for a specific row |
| POST | `/api/v1/group/{group_id}/adm/seat-matrix/change-request/` | JWT G3 | Coordinator submits seat change request |
| PATCH | `/api/v1/group/{group_id}/adm/seat-matrix/change-request/{id}/approve/` | JWT G3 (Director) | Approve seat change request |
| GET | `/api/v1/group/{group_id}/adm/seat-matrix/export/` | JWT G3+ | Export matrix as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/seat-matrix/kpis/` | `#seat-matrix-kpi-bar` | `innerHTML` |
| Filter change (branch/stream/type/fill%) | `change` | GET `/api/v1/group/{group_id}/adm/seat-matrix/?{filters}` | `#seat-matrix-table-body` | `innerHTML` |
| Sort column click | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/?sort={col}&order={dir}` | `#seat-matrix-table-body` | `innerHTML` |
| Heatmap initial load | `load` | GET `/api/v1/group/{group_id}/adm/seat-matrix/heatmap/` | `#fill-rate-heatmap` | `innerHTML` |
| Heatmap cell click (filter table) | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/?branch={id}&stream={id}` | `#seat-matrix-table-body` | `innerHTML` |
| RTE compliance table load | `load` | GET `/api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/` | `#rte-compliance-table` | `innerHTML` |
| RTE detail drawer open | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/rte-compliance/{branch_id}/` | `#rte-compliance-detail-drawer` | `innerHTML` |
| Historical trend chart load | `load` | GET `/api/v1/group/{group_id}/adm/seat-matrix/fill-trend/?years=3` | `#fill-trend-chart-data` | `innerHTML` |
| Fill trend branch filter change | `change` | GET `/api/v1/group/{group_id}/adm/seat-matrix/fill-trend/?branch_ids={ids}` | `#fill-trend-chart-data` | `innerHTML` |
| [Edit Seats →] button click | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/{branch_id}/{stream}/edit/` | `#seat-edit-drawer` | `innerHTML` |
| Enable Edit Mode toggle | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/edit-mode/` | `#seat-matrix-table-wrapper` | `innerHTML` |
| Save seat changes (inline edit) | `click` | PATCH `/api/v1/group/{group_id}/adm/seat-matrix/bulk-update/` | `#seat-matrix-table-wrapper` | `innerHTML` |
| Coordinator change request submit | `submit` | POST `/api/v1/group/{group_id}/adm/seat-matrix/change-request/` | `#change-request-confirm` | `innerHTML` |
| Export matrix button click | `click` | GET `/api/v1/group/{group_id}/adm/seat-matrix/export/` | `#export-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
