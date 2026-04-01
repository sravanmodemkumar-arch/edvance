# 15 — Grade Bands & Compensation Manager

- **URL:** `/group/hr/compensation/grade-bands/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Director (Role 41, G3)

---

## 1. Purpose

The Grade Bands & Compensation Manager is the authoritative configuration page for all salary structures across the group. It defines the minimum and maximum salary range for each staff category — teaching and non-teaching — and enforces those boundaries across all branch-level HR operations. Without well-defined grade bands, salary inconsistencies emerge between branches: the same role in two campuses could have a 40% pay disparity, creating staff morale issues and legal exposure. This page prevents that by making grade bands the single binding reference for all compensation decisions.

Teaching staff bands cover the full hierarchy: Trained Graduate Teacher (TGT), Post Graduate Teacher (PGT), Head of Department (HOD), Vice Principal, and Principal. Non-teaching bands cover Warden (Boys/Girls), Office Assistant, Security Guard, Driver, Cook/Mess Staff, Electrician, Lab Assistant, and Librarian. Each band specifies a Grade Code, Role Category, Minimum Salary, Maximum Salary, Standard Annual Increment Percentage, and allowance components (HRA, Dearness Allowance, Transport Allowance). All branch-level salary offers must fall within the defined band range; any exception requires Group HR Director approval before the offer is sent.

The page also surfaces critical compliance signals: staff who have drifted below the band minimum due to policy changes, or staff whose salary has exceeded the band maximum due to multiple increments, both appear as alert-level KPI cards. The HR Director can act directly from the table — either by triggering a salary adjustment or by revising the band — ensuring no staff member remains out-of-band indefinitely. Band review history is retained for audit purposes so that external auditors can trace why a band was changed and when.

Compensation data is sensitive. Only the Group HR Director (Role 41, G3) can create, edit, or archive grade bands. The HR Manager has read-only visibility to understand constraints when extending offers. All other roles have no access to this page. Changes to any band's minimum or maximum generate a system notification to the HR Manager, as those changes affect all active offers and contracts referencing that band.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full CRUD — all bands | Create, edit, archive grade bands |
| Group HR Manager (42) | G3 | Read-only | Can view bands; cannot edit |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Compensation → Grade Bands & Compensation Manager`

### 3.2 Page Header
- Title: "Grade Bands & Compensation Manager"
- Subtitle: "Define salary ranges and allowance structures for all staff categories."
- Last Reviewed Date chip (e.g., "Last Reviewed: Jan 2026")
- Primary CTA: "+ Add Grade Band" (HR Director only)
- Secondary CTA: "Download Compensation Report" (PDF/XLSX)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Staff count below band minimum > 0 | "[N] staff members are paid below their band minimum. Immediate action required." | Red |
| Staff count above band maximum > 0 | "[N] staff members exceed their band maximum. Review required." | Orange |
| Any band not reviewed in > 12 months | "[N] grade bands have not been reviewed in over 12 months." | Yellow |
| Band edit in last 7 days | "Grade band updated recently — active offers may be affected. Review pending offers." | Blue |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Grade Bands | Count of active bands | Neutral blue | Scrolls to table |
| Bands Awaiting Review | Count with last_reviewed > 12 months | Red if > 0 | Filters table to overdue |
| Staff Below Minimum | Count of staff below band min | Red if > 0, Green if 0 | Modal list of affected staff |
| Staff Above Maximum | Count of staff above band max | Orange if > 0, Green if 0 | Modal list of affected staff |
| Avg Salary per Band | Mean midpoint across all active bands (₹) | Neutral | Opens detailed breakdown chart |
| Last Band Review Date | Most recent review date across all bands | Amber if > 6 months ago | — |

---

## 5. Main Table — Grade Bands

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Grade Code | Text (e.g., TGT-A, PGT-B) | Yes | No |
| Role Category | Chip (Teaching / Non-Teaching) | Yes | Yes |
| Role Title | Text | Yes | Yes (search) |
| Min Salary (₹) | Currency | Yes | No |
| Max Salary (₹) | Currency | Yes | No |
| Std Increment % | Percentage | Yes | No |
| HRA % | Percentage | No | No |
| DA (₹) | Currency | No | No |
| Transport (₹) | Currency | No | No |
| Staff in Band | Integer (count) | Yes | No |
| Last Reviewed | Date | Yes | Yes (date range) |
| Status | Chip (Active / Archived) | No | Yes |
| Actions | Edit / View Staff / Archive | No | No |

### 5.1 Filters
- Role Category: All | Teaching | Non-Teaching
- Status: All | Active | Archived
- Last Reviewed: Before [date picker] (to surface overdue reviews)

### 5.2 Search
Search box: matches Grade Code or Role Title (minimum 2 characters, HTMX-triggered live search).

### 5.3 Pagination
Server-side pagination, 15 bands per page. Navigation: Previous / Page numbers / Next. Total record count displayed above table.

---

## 6. Drawers

### 6.1 Drawer: Create Grade Band
Fields: Grade Code (text, unique, uppercase enforced), Role Category (Teaching / Non-Teaching), Role Title (text), Min Salary (₹, numeric), Max Salary (₹, must be > Min), Standard Increment % (0.01–30.00), HRA % of Basic (numeric), DA Fixed Amount (₹), Transport Allowance (₹), Notes / Justification (textarea), Effective From (date picker).
Validation: Grade Code unique; Max > Min; all monetary fields ≥ 0; Effective From ≥ today.
On Save: POST to API, table row prepended, toast shown, drawer closes.

### 6.2 Drawer: Edit Grade Band
Pre-populated with existing values. All fields editable. Change Reason field (textarea, required). Shows "Current Staff Count in Band: [N]" warning when editing salary range.
On Save: PATCH to API, table row updated in place, toast shown, system notification triggered to HR Manager.

### 6.3 Drawer: View Staff in Band
Read-only list of all staff assigned to this grade band. Columns: Staff Name, Branch, Current Salary, Position in Band (Below Min / In Range / Above Max), Last Increment Date.
Pagination within drawer: 10 per page. Export to XLSX button.

### 6.4 Modal: Archive Confirmation
Triggered by "Archive" action. Displays: "Are you sure you want to archive [Grade Code]? [N] staff are currently assigned to this band. They will need to be reassigned." Confirm / Cancel. On Confirm: PATCH status = Archived, table row moves to archived view.

---

## 7. Charts

**Salary Distribution by Grade Band** — horizontal bar chart (or grouped bar) showing Min, Midpoint, and Max salary for each active band side by side. Colour coding: Teaching bands in indigo, non-teaching bands in teal. Rendered via Chart.js. Positioned below the main table. Toggle button: "Show Chart / Hide Chart" (collapsed by default to save vertical space). Clicking a bar segment highlights the corresponding row in the table above.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Grade band created | "Grade band [Code] created successfully." | Success | 4s |
| Grade band updated | "Grade band [Code] updated. HR Manager notified." | Success | 5s |
| Band archived | "Grade band [Code] archived." | Info | 4s |
| Duplicate Grade Code | "Grade Code already exists. Use a unique identifier." | Error | 6s |
| Max < Min validation | "Maximum salary must be greater than minimum salary." | Error | 6s |
| Report downloaded | "Compensation report downloaded." | Success | 3s |
| Unauthorised access attempt | "You do not have permission to modify grade bands." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No grade bands configured | "No Grade Bands Defined" | "Define salary grade bands to standardise compensation across all branches." | Add Grade Band |
| No bands match current filter | "No Matching Bands" | "Adjust your filters or search term to find grade bands." | Clear Filters |
| Archived tab empty | "No Archived Bands" | "No grade bands have been archived yet." | — |
| Staff-in-band drawer empty | "No Staff Assigned" | "No staff are currently mapped to this grade band." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (10) |
| Filter/search apply | Table body replaced with row skeletons |
| Drawer open | Drawer form field skeletons (6 fields) |
| Chart render | Spinner centred in chart container |
| Save / archive action | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | HR Manager (42) | All Other Roles |
|---|---|---|---|
| Add Grade Band button | Visible + enabled | Hidden | Hidden |
| Edit action in table | Visible + enabled | Hidden | Hidden |
| Archive action in table | Visible + enabled | Hidden | Hidden |
| View Staff in Band | Visible | Visible | Hidden |
| Download Compensation Report | Visible | Visible | Hidden |
| Chart toggle | Visible | Visible | Hidden |
| KPI alert cards (Below/Above Min) | Visible with action links | Visible read-only | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/compensation/grade-bands/` | JWT | List all grade bands (paginated) |
| POST | `/api/v1/hr/compensation/grade-bands/` | JWT | Create new grade band |
| GET | `/api/v1/hr/compensation/grade-bands/{id}/` | JWT | Fetch single band detail |
| PATCH | `/api/v1/hr/compensation/grade-bands/{id}/` | JWT | Update grade band |
| PATCH | `/api/v1/hr/compensation/grade-bands/{id}/archive/` | JWT | Archive grade band |
| GET | `/api/v1/hr/compensation/grade-bands/{id}/staff/` | JWT | List staff assigned to band |
| GET | `/api/v1/hr/compensation/grade-bands/kpis/` | JWT | KPI summary (counts) |
| GET | `/api/v1/hr/compensation/grade-bands/chart/` | JWT | Chart data — salary ranges per band |
| GET | `/api/v1/hr/compensation/grade-bands/export/` | JWT | Download compensation report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/compensation/grade-bands/?q={val}` | `#bands-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/compensation/grade-bands/?category={val}&status={val}` | `#bands-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/compensation/grade-bands/?page={n}` | `#bands-table-body` | innerHTML |
| Create drawer open | click | GET `/group/hr/compensation/grade-bands/create/drawer/` | `#drawer-container` | innerHTML |
| Edit drawer open | click | GET `/group/hr/compensation/grade-bands/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| View Staff drawer open | click | GET `/group/hr/compensation/grade-bands/{id}/staff/drawer/` | `#drawer-container` | innerHTML |
| Create submit | submit | POST `/api/v1/hr/compensation/grade-bands/` | `#bands-table-body` | afterbegin |
| Edit submit | submit | PATCH `/api/v1/hr/compensation/grade-bands/{id}/` | `#band-row-{id}` | outerHTML |
| Archive confirm | click | PATCH `/api/v1/hr/compensation/grade-bands/{id}/archive/` | `#band-row-{id}` | outerHTML |
| Chart toggle | click | GET `/group/hr/compensation/grade-bands/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
