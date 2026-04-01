# 34 — BGV Registry — Group Background Verification Register

- **URL:** `/group/hr/bgv/registry/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group BGV Manager (Role 48, G3)

---

## 1. Purpose

The BGV Registry is the master audit-trail register of all staff background verification records across every branch of the group. Background verification is a non-negotiable compliance requirement for every staff member who has access to students — whether teaching or non-teaching. Any adult on the school campus with student contact must have an active, non-flagged BGV on file. This registry is the definitive record that satisfies regulatory audits, POCSO compliance checks, and institutional governance requirements.

The BGV programme covers five distinct verification components. Police Verification is obtained from the local police station or through an authorised online portal and is valid for three years from the date of issue. Educational Qualification Verification confirms that the staff member's academic credentials — degree certificates, diplomas, professional certifications — are genuine and issued by the claimed institution, cross-checked with the issuing university's registrar. Previous Employment Verification confirms the staff member's last two employers, checks for any adverse exit, and validates the claimed role and tenure. Address Verification confirms the current residential address through physical or postal verification. Criminal Record Check is a national criminal history check conducted through an authorised agency or police clearance.

A BGV record is created for every new joiner at onboarding. The record progresses through states: Not Initiated → In Progress → Pending Agency Response → Clear or Flagged or Expired. A Flagged BGV — where any component returns an adverse finding — triggers immediate escalation to the HR Director and POCSO Coordinator. No flagged-BGV staff member may continue in student-contact roles until the HR Director resolves the case. An Expired BGV (past 3-year validity) must be renewed — the registry proactively flags staff whose BGV expires within 90 days so renewal can be initiated before lapse.

The BGV Registry is the top-level view: it shows one record per staff member with their aggregate BGV status. Drill-down to individual component-level detail (which specific verification components are done vs. pending) is accessible via the view drawer. Bulk actions — bulk initiation for a cohort of new joiners, and export for external agency submission — save significant administrative time.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group BGV Manager | G3 | Full CRUD + Bulk Actions + Export | Primary owner |
| Group BGV Executive | G3 | Read + Update status on assigned cases | Cannot create new records |
| Group HR Director | G3 | Read + Escalation view | Views flagged cases; receives notifications |
| Group POCSO Coordinator | G3 | Read (flagged staff only) | Sees BGV flags relevant to POCSO oversight |
| Group HR Manager | G3 | Read Only | General oversight |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Background Verification > BGV Registry`

### 3.2 Page Header
- **Title:** BGV Registry — Group Background Verification Register
- **Subtitle:** Master register of all staff background verification records
- **Actions (top-right):**
  - `+ Initiate BGV` (primary button — single record)
  - `Bulk Initiate for New Joiners` (secondary button)
  - `Export BGV Report` (secondary button)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any Flagged BGV with staff still in student contact | "CRITICAL: [N] staff with Flagged BGV are currently in student-contact roles. HR Director has been notified. Immediate action required." | Red — non-dismissible |
| BGV expiring within 30 days | "URGENT: [N] staff member(s) BGV expire within 30 days. Initiate renewal immediately." | Red — dismissible |
| BGV expiring within 90 days | "WARNING: [N] staff member(s) BGV expire within 90 days. Schedule renewal." | Amber — dismissible |
| New joiners with BGV not yet initiated | "INFO: [N] new joiner(s) do not have a BGV record initiated. Use 'Bulk Initiate for New Joiners'." | Blue — dismissible |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Staff Registered | Count of all staff with a BGV record | Blue always | No drill-down |
| Clear BGV | Count with Status = Clear and not expired | Green if ≥ 95% of total, Amber if 85–94%, Red if < 85% | Filters table to Clear |
| Flagged (Immediate Action) | Count with Status = Flagged | Red if > 0, Green if 0 | Filters to Flagged |
| Pending | Count with Status = In Progress or Pending Response | Amber if > 0 | Filters to Pending |
| Expiring in 90 Days | Count with expiry date within 90 days | Amber if > 0 | Filters to expiring soon |
| Never Initiated | Staff in system with no BGV record | Red if > 0, Green if 0 | Filters to unregistered |

---

## 5. Main Table — BGV Records

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Role / Designation | Text | Yes | Yes — dropdown |
| BGV Type | Badge (New Joiner / Renewal / Supplementary) | No | Yes — dropdown |
| Initiated Date | Date | Yes | Yes — date range |
| Agency | Text | No | Yes — dropdown |
| Status | Badge (Clear / Flagged / In Progress / Pending Response / Expired / Not Initiated) | No | Yes — multi-select |
| Expiry Date | Date with colour coding | Yes | Yes — date range |
| Actions | Icon buttons (View / Edit / Renew) | No | No |

### 5.1 Filters
- **Branch:** multi-select
- **Status:** multi-select
- **BGV Type:** New Joiner / Renewal / Supplementary
- **Agency:** dropdown
- **Expiry:** Expired / Expiring 30 days / Expiring 90 days / Valid
- **Initiated Date Range:** date picker

### 5.2 Search
Free-text search on Staff Name and Branch. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 25 rows per page. Shows `Showing X–Y of Z records`. Bulk select checkboxes appear on left of each row when BGV Manager is logged in.

---

## 6. Drawers

### 6.1 Initiate BGV (Create)
**Trigger:** `+ Initiate BGV` button
**Fields:**
- Staff Member (searchable dropdown — staff directory)
- BGV Type (radio: New Joiner / Renewal / Supplementary)
- Components to Verify (multi-select checklist: Police Verification / Education Verification / Previous Employment / Address Verification / Criminal Record Check)
- Verification Agency (dropdown from agency register)
- Target Completion Date (date picker)
- Internal Reference Notes (textarea)
- Submit button → creates BGV record in In Progress state and assigns to BGV Executive queue

### 6.2 View BGV Record
**Trigger:** Row click or eye icon
**Displays:** Staff profile summary, all BGV components with individual status, agency name, submitted date, completed date, outcome per component (Clear / Flagged / Pending), uploaded agency report links, internal notes per component, audit trail of all status changes with timestamps and changed-by names.

### 6.3 Edit BGV Record
**Trigger:** Edit icon (BGV Manager only)
**Editable:** Agency assignment, target completion date, add/remove components (pre-completion only), internal notes. Cannot change outcome once set — outcome changes go through a formal review process with reason logged.

### 6.4 Bulk Initiate for New Joiners
**Trigger:** `Bulk Initiate for New Joiners` button
**Modal:** Select join date range → system lists all staff joined in that range without a BGV record → BGV Manager selects default components and agency → bulk creates BGV records and assigns to BGV Executive queue → confirmation: "[N] BGV records created and assigned."

---

## 7. Charts

**BGV Status Distribution (Stacked Bar by Branch)**
- X-axis: Branch names
- Y-axis: Staff count
- Stacks: Clear (green), In Progress (blue), Flagged (red), Expired (grey), Not Initiated (light grey)
- Benchmark line at top of each bar showing total staff count for that branch

**BGV Expiry Timeline (Line Chart)**
- X-axis: Month (next 12 months)
- Y-axis: Count of BGV records expiring
- Useful for forward planning of renewal workload
- Highlight zone: next 90 days in amber

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| BGV record initiated | "BGV initiated for [Staff Name]. Assigned to BGV Executive queue." | Success | 4s |
| Bulk BGV initiated | "[N] BGV records created for new joiners." | Success | 5s |
| BGV status updated | "BGV status updated to [Status] for [Staff Name]." | Info | 4s |
| Flagged BGV escalated | "Flagged BGV for [Staff Name] escalated to HR Director and POCSO Coordinator." | Warning | 6s |
| Export started | "BGV report export started. Download will begin shortly." | Info | 4s |
| Error on initiation | "Failed to initiate BGV for [Staff Name]. Staff record not found." | Error | 6s |

---

## 9. Empty States

- **No BGV records:** "No BGV records found. Use '+ Initiate BGV' or 'Bulk Initiate for New Joiners' to begin."
- **No results match filters:** "No BGV records match the selected filters. Try removing one or more filter conditions."
- **All records clear:** "All staff BGV records are Clear and valid. No action required."

---

## 10. Loader States

- Table skeleton: 8 rows with shimmer on initial load.
- KPI cards: shimmer rectangles.
- View drawer: spinner while full BGV record and component data loads.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | BGV Manager (G3) | BGV Executive (G3) | HR Director (G3) |
|---|---|---|---|
| Initiate BGV button | Visible + enabled | Hidden | Hidden |
| Bulk Initiate button | Visible + enabled | Hidden | Hidden |
| Edit BGV record | Visible + enabled | Hidden | Hidden |
| View BGV record | Visible | Visible (assigned cases) | Visible (flagged only) |
| Export BGV Report | Visible | Hidden | Visible |
| Bulk select checkboxes | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/bgv/registry/` | JWT G3 | List all BGV records (paginated) |
| POST | `/api/v1/hr/bgv/registry/` | JWT G3 BGV Manager | Initiate new BGV record |
| GET | `/api/v1/hr/bgv/registry/{id}/` | JWT G3 | View full BGV record with components |
| PATCH | `/api/v1/hr/bgv/registry/{id}/` | JWT G3 BGV Manager | Update BGV record |
| POST | `/api/v1/hr/bgv/registry/bulk-initiate/` | JWT G3 BGV Manager | Bulk initiate for new joiners |
| GET | `/api/v1/hr/bgv/registry/kpis/` | JWT G3 | KPI summary data |
| GET | `/api/v1/hr/bgv/registry/charts/status/` | JWT G3 | Status distribution chart data |
| GET | `/api/v1/hr/bgv/registry/charts/expiry/` | JWT G3 | Expiry timeline chart data |
| GET | `/api/v1/hr/bgv/registry/export/` | JWT G3 | Export BGV report (CSV/XLSX) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search staff name | keyup changed delay:400ms | GET `/api/v1/hr/bgv/registry/?q={val}` | `#bgv-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/bgv/registry/?{params}` | `#bgv-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/bgv/registry/?page={n}` | `#bgv-table-body` | innerHTML |
| Open initiate drawer | click | GET `/api/v1/hr/bgv/registry/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/bgv/registry/{id}/` | `#drawer-container` | innerHTML |
| Submit initiate form | submit | POST `/api/v1/hr/bgv/registry/` | `#bgv-table-body` | innerHTML |
| Refresh KPI bar after action | htmx:afterRequest | GET `/api/v1/hr/bgv/registry/kpis/` | `#kpi-bar` | innerHTML |
| Load expiry chart | load | GET `/api/v1/hr/bgv/registry/charts/expiry/` | `#chart-expiry` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
