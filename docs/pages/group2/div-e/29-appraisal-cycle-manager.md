# 29 — Appraisal Cycle Manager

- **URL:** `/group/hr/appraisal/cycles/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Appraisal Cycle Manager is the governance page through which the HR Director creates, configures, and manages the annual performance appraisal cycle for the entire group. An appraisal cycle is a time-bound exercise that formally evaluates all applicable staff members against a defined KPI framework. Creating and publishing a cycle is a consequential action — once published, it triggers thousands of appraisal tasks to be initiated by branch principals and HODs across the group.

Each appraisal cycle is configured with: a Cycle Name (e.g., "AY 2025-26 Annual Appraisal"), the academic year it applies to, the applicable staff population (All Teaching / Senior Staff Only / All Staff), which branches are included, the KPI framework to be used (selected from the framework library), the rating scale (1–5 Likert or ABCD scale), and the dates for each phase — Self-Assessment Phase, Manager Assessment Phase, Calibration Phase, and Result Publication. Each phase has its own open and close dates.

Once a cycle is created and saved as Draft, the HR Director can preview the cycle setup, make adjustments, and optionally run a dry-run simulation to estimate the number of appraisal tasks that will be generated. When the cycle is Published, the system creates individual appraisal records for every applicable staff member across included branches and notifies branch principals and HR Managers to begin the process. Only one cycle can be active per academic year per staff population type.

The HR Director can monitor aggregate cycle progress on this page: how many branches have completed the self-assessment phase, how many appraisals are awaiting manager review, whether calibration is in progress, and the final count of results published. A cycle can only be closed once all branches have submitted their calibrated ratings. The Results Published state makes ratings visible to staff through the staff portal.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full CRUD + Publish + Close | Sole owner of cycle creation and publication |
| Group HR Manager | G3 | Read + Add notes | Can view progress; cannot create or publish cycles |
| Group Performance Review Officer | G1 | Read Only | Views cycle list and status; no edit |
| Group Training & Development Manager | G2 | No Access | Not applicable |
| Branch Principal | Branch G3 | Read (own branch phase status only) | Cannot see group-level cycle details |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Performance Appraisal > Appraisal Cycle Manager`

### 3.2 Page Header
- **Title:** Appraisal Cycle Manager
- **Subtitle:** Create and manage group-wide appraisal cycles
- **Actions (top-right):**
  - `+ Create Appraisal Cycle` (primary button, HR Director only)
  - `Export Progress Report` (secondary button)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Active cycle has a phase deadline expiring within 3 days | "REMINDER: Self-Assessment phase for '[Cycle Name]' closes in [N] days. [N] branches have not yet completed submissions." | Amber — dismissible |
| Calibration phase has branches with 0% completion at 50% elapsed | "WARNING: [N] branches have not started calibration for '[Cycle Name]'." | Amber — dismissible |
| Cycle results pending publication past publication date | "Results for '[Cycle Name]' are ready to publish. Click Publish Results to release to staff." | Blue — dismissible |
| No active appraisal cycle | "No active appraisal cycle. Create a new cycle to begin the appraisal process." | Grey — informational |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Appraisal Cycles | Count of cycles in Published/In-Progress state | Blue if ≥ 1, Grey if 0 | Filters table to Status = Active |
| Branches with Appraisal Completed | Count of branches at Closed or Results Published phase | Green if = total branches, Amber if < total | Filters to completion view |
| Appraisals Submitted | Count of individual appraisal records in Submitted state | Blue always | Links to teacher performance review page |
| Pending Submission | Count of appraisal records not yet submitted | Amber if > 0, Green if 0 | Filters to pending view |
| Calibration Pending | Count of branches in Calibration phase with < 100% calibrated | Amber if > 0 | Filters to calibration view |
| Results Published | Count of cycles in Results Published state | Green if > 0, Grey if 0 | No drill-down |

---

## 5. Main Table — Appraisal Cycles

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Cycle Name | Text | Yes | No |
| AY | Badge (e.g., 2025-26) | Yes | Yes — dropdown |
| Target Staff | Badge (All Staff / Teaching / Senior) | No | Yes — dropdown |
| Branches | Count badge (e.g., 12/14) | No | No |
| Start Date | Date | Yes | Yes — date range |
| End Date | Date | Yes | Yes — date range |
| Phase | Badge (Draft / Self-Assessment / Manager Review / Calibration / Results Published / Closed) | No | Yes — multi-select |
| Completion % | Progress bar | Yes | No |
| Status | Badge (Active / Completed / Draft / Archived) | No | Yes — multi-select |
| Actions | Icon buttons (View / Edit / Publish / Close) | No | No |

### 5.1 Filters
- **Academic Year:** dropdown
- **Status:** Draft / Active / Completed / Archived
- **Phase:** all phase options multi-select
- **Target Staff Population:** All Staff / Teaching Only / Senior Staff

### 5.2 Search
Free-text search on Cycle Name. Triggers `hx-get` on keyup with 400 ms debounce.

### 5.3 Pagination
Server-side, 15 rows per page (cycles are few; low row count per page improves readability). Shows `Showing X–Y of Z cycles`.

---

## 6. Drawers

### 6.1 Create Appraisal Cycle
**Trigger:** `+ Create Appraisal Cycle` button
**Fields:**
- Cycle Name (text, required)
- Academic Year (dropdown, required)
- Target Staff (radio: All Staff / Teaching Only / Senior Staff)
- Branches Included (multi-select checkbox, default: all)
- KPI Framework (dropdown from framework library)
- Rating Scale (radio: 1–5 Likert / ABCD)
- Self-Assessment Open Date / Close Date
- Manager Assessment Open Date / Close Date
- Calibration Open Date / Close Date
- Results Publication Date
- Notes / Instructions for Branches (textarea)
- Save as Draft button (does not trigger notifications)
- Preview Estimated Tasks button (dry-run count)

### 6.2 View Cycle Progress
**Trigger:** Row click or eye icon
**Displays:** Full cycle configuration summary, phase timeline (visual stepper), per-branch progress breakdown (branch name, phase reached, submissions count, calibration status, completion %).

### 6.3 Edit Cycle
**Trigger:** Edit icon
**Constraint:** Only editable when cycle Status = Draft. Once Published, only Notes field and phase dates can be extended (with confirmation modal). Cannot reduce phase end dates once notified.

### 6.4 Close Cycle / Publish Results
**Trigger:** Dedicated action buttons in view drawer or table row Actions menu
**Publish Results:** Confirmation modal — "This will release appraisal results to all applicable staff. This cannot be undone. Confirm?" Two-step confirm with typed acknowledgement.
**Close Cycle:** Only available after Results Published. Moves cycle to Closed state — archives all appraisal records.

---

## 7. Charts

**Cycle Phase Progress — Stacked Bar by Branch**
- X-axis: Branch names
- Y-axis: Staff count
- Stacks: Self-Assessment Done (teal), Manager Review Done (blue), Calibrated (green), Not Started (grey)
- Rendered per selected cycle from a cycle selector dropdown above the chart

**Rating Distribution Preview (active cycle only)**
- Donut chart showing proportion of 1/2/3/4/5 ratings (or ABCD) submitted so far across all branches
- Visible only once Manager Assessment phase has begun

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Cycle created (Draft) | "Appraisal cycle '[Name]' saved as Draft." | Success | 4s |
| Cycle published | "Appraisal cycle '[Name]' published. Notifications sent to all branch principals." | Success | 5s |
| Cycle phase dates updated | "Phase dates updated for '[Name]'." | Info | 4s |
| Results published | "Results for '[Name]' published to staff portal." | Success | 5s |
| Cycle closed | "Cycle '[Name]' has been closed and archived." | Info | 4s |
| Duplicate cycle error | "An active cycle already exists for this academic year and staff population." | Error | 6s |

---

## 9. Empty States

- **No cycles created:** "No appraisal cycles found. Click '+ Create Appraisal Cycle' to begin the annual appraisal process."
- **No cycles match filters:** "No cycles match the selected filters. Try adjusting the academic year or status filter."
- **Cycle has no branches assigned:** "No branches assigned to this cycle. Edit the cycle to add branches before publishing."

---

## 10. Loader States

- Table skeleton: 5 placeholder rows with shimmer.
- KPI cards: skeleton cards with shimmer during initial load.
- Cycle progress drawer: spinner while per-branch breakdown loads.
- Chart area: grey placeholder with "Loading chart…" until data resolves.

---

## 11. Role-Based UI Visibility

| Element | HR Director (G3) | HR Manager (G3) | Perf. Review Officer (G1) |
|---|---|---|---|
| Create Appraisal Cycle button | Visible + enabled | Hidden | Hidden |
| Edit cycle | Visible + enabled | Hidden | Hidden |
| Publish / Close cycle buttons | Visible + enabled | Hidden | Hidden |
| Export Progress Report | Visible | Visible | Visible |
| View cycle details | Visible | Visible | Visible |
| Add internal notes | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/appraisal/cycles/` | JWT G3 | List all appraisal cycles |
| POST | `/api/v1/hr/appraisal/cycles/` | JWT G3 HR Director | Create a new appraisal cycle |
| GET | `/api/v1/hr/appraisal/cycles/{id}/` | JWT G2+ | Get cycle details and progress |
| PATCH | `/api/v1/hr/appraisal/cycles/{id}/` | JWT G3 HR Director | Update cycle configuration |
| POST | `/api/v1/hr/appraisal/cycles/{id}/publish/` | JWT G3 HR Director | Publish cycle (triggers staff appraisal creation) |
| POST | `/api/v1/hr/appraisal/cycles/{id}/publish-results/` | JWT G3 HR Director | Publish results to staff portal |
| POST | `/api/v1/hr/appraisal/cycles/{id}/close/` | JWT G3 HR Director | Close and archive cycle |
| GET | `/api/v1/hr/appraisal/cycles/{id}/preview/` | JWT G3 | Dry-run task count preview |
| GET | `/api/v1/hr/appraisal/cycles/kpis/` | JWT G2+ | KPI summary bar data |
| GET | `/api/v1/hr/appraisal/cycles/{id}/chart-progress/` | JWT G2+ | Branch-phase progress chart data |
| GET | `/api/v1/hr/appraisal/cycles/export/` | JWT G2+ | Export cycle progress report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search cycle by name | keyup changed delay:400ms | GET `/api/v1/hr/appraisal/cycles/?q={val}` | `#cycles-table-body` | innerHTML |
| Filter by status/AY | change | GET `/api/v1/hr/appraisal/cycles/?{params}` | `#cycles-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/appraisal/cycles/?page={n}` | `#cycles-table-body` | innerHTML |
| Open create drawer | click | GET `/api/v1/hr/appraisal/cycles/new/` | `#drawer-container` | innerHTML |
| Open view/progress drawer | click | GET `/api/v1/hr/appraisal/cycles/{id}/` | `#drawer-container` | innerHTML |
| Submit create cycle form | submit | POST `/api/v1/hr/appraisal/cycles/` | `#cycles-table-body` | innerHTML |
| Refresh KPI bar | load | GET `/api/v1/hr/appraisal/cycles/kpis/` | `#kpi-bar` | innerHTML |
| Switch chart cycle selector | change | GET `/api/v1/hr/appraisal/cycles/{id}/chart-progress/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
