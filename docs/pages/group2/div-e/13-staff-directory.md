# 13 — Group Staff Directory

- **URL:** `/group/hr/staff/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Director (Role 41, G3) — Primary owner; all G3 HR roles have scoped access

---

## 1. Purpose

The Group Staff Directory is the single source of truth for every employee across all branches in the group. It is the master registry — the authoritative record of who works where, in what capacity, under what employment terms, with what compliance status. Every other HR function in Division E — BGV tracking, POCSO compliance, performance review, transfers, disciplinary proceedings, and welfare management — draws its staff data from this directory. When a new staff member is onboarded, their record is created here first; when a staff member is terminated or transferred, this record is updated first; all other systems reflect that change downstream.

The scale of this directory varies considerably by group size: a 5-branch group may have 500–1,000 staff records, while a 50-branch group may have 5,000–10,000+ records. The directory is therefore designed with performance in mind — server-side pagination, indexed searches, and filtered queries ensure the page remains responsive regardless of record volume. The advanced filter panel supports multi-dimensional queries (e.g., "show all permanent teaching staff at Branch X with incomplete BGV and POCSO training pending") that allow any HR role to extract exactly the segment they need without building a custom report.

Access control is role-differentiated: the HR Director and HR Manager have full write access to all staff records, including editing sensitive fields (employment type, BGV status overrides, active/inactive toggle). Other G3 HR roles (BGV Manager, POCSO Coordinator, Transfer Coordinator, etc.) have read access to all records but write access only to the fields within their domain (e.g., BGV Manager can update BGV status fields; POCSO Coordinator can update POCSO training status). G1 roles (Performance Review Officer) have read-only access to names, branches, and roles — they cannot see employment terms, join dates, or compliance status details.

Bulk actions are a key productivity feature for HR operations at scale. The BGV Manager can select all staff with "BGV Pending" status at a specific branch and bulk-initiate verifications, routing them to the BGV queue in a single action. The T&D Manager can select all new joiners from the last 30 days and bulk-assign them to the group induction training program. These bulk operations are audit-logged with the initiating user's identity and timestamp.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director | G3 | Full read + write (all fields) | Can activate/deactivate staff records |
| Group HR Manager | G3 | Full read + write (all fields) | Operational management of all records |
| G3 HR Domain Roles (BGV, POCSO, Transfer, Welfare, Disciplinary) | G3 | Full read + domain-specific write | Each role can edit only their domain fields |
| Group Performance Review Officer | G1 | Read-only (name, branch, role only) | Cannot see compliance status or join date |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Staff Directory
```

### 3.2 Page Header
- **Title:** `Group Staff Directory`
- **Subtitle:** `[Total Count] Staff · [N] Branches · [N] Active · [N] Inactive · AY [current academic year]`
- **Role Badge:** `Group HR Director` (or active role badge for other accessing roles)
- **Right-side controls:** `+ Add Staff` · `Bulk Actions` (dropdown) · `Advanced Filters` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Staff records with no BGV and join date > 7 days | "[N] active staff member(s) have been in the system for more than 7 days without a BGV record. Initiate BGV." | Red |
| Staff records marked Inactive but with future payroll entries | "[N] inactive staff record(s) have uncleared payroll entries. Finance team notified." | Amber |
| Document status Incomplete for > 30 days post-join | "[N] staff member(s) have incomplete document submissions more than 30 days after joining." | Amber |
| POCSO training overdue for new joiners (> 30 days) | "[N] staff member(s) who joined more than 30 days ago have not completed POCSO training." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Active Staff | All staff with Active status across all branches | Blue | No filter applied |
| New Joiners (Last 30 Days) | Staff with join date in last 30 calendar days | Blue | Filtered by recent join |
| BGV Incomplete | Active staff with BGV status Pending or Expired | Red if > 0, Green if 0 | Filtered by BGV status |
| POCSO Not Trained | Active staff without valid POCSO training record | Amber if > 0, Green if 0 | Filtered by POCSO status |
| Document Status Incomplete | Staff with one or more required documents not submitted | Amber if > 0 | Filtered by doc status |
| Inactive Staff | Staff with Inactive/Resigned/Terminated status | Blue (informational) | Filtered by status |

---

## 5. Main Table — Group Staff Directory

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff ID | Text (e.g., STF-0001) | Yes | No |
| Name | Text (link to staff profile) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Department | Text | Yes | Yes (multi-select) |
| Role / Designation | Text | Yes | Yes (text search) |
| Employment Type | Badge (Permanent / Contract / Visiting / Probation) | Yes | Yes |
| Join Date | Date | Yes | Yes (date range) |
| BGV Status | Badge (Completed / In Progress / Pending / Failed / Expired) | Yes | Yes |
| POCSO Status | Badge (Trained / Training Due / Not Trained) | Yes | Yes |
| Document Status | Badge (Complete / Incomplete / Pending Review) | Yes | Yes |
| Record Status | Badge (Active / Inactive / On Leave / Transferred) | Yes | Yes |
| Actions | View / Edit / Deactivate | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches |
| Role Category | Checkbox | Teaching / Non-Teaching / Admin |
| Employment Type | Checkbox | Permanent / Contract / Visiting / Probation |
| BGV Status | Checkbox | Completed / In Progress / Pending / Failed / Expired |
| POCSO Status | Checkbox | Trained / Training Due / Not Trained |
| Document Status | Checkbox | Complete / Incomplete / Pending Review |
| Record Status | Checkbox | Active / Inactive / On Leave / Transferred |
| Join Date | Date range picker | Any range |

### 5.2 Search
- Full-text: Staff ID, name, role, branch, department
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `staff-create` — Add New Staff Member
- **Trigger:** `+ Add Staff` button
- **Width:** 560px
- **Fields:**
  - Full Name (required, text)
  - Branch (required, dropdown)
  - Department (required, dropdown based on branch)
  - Role / Designation (required, text)
  - Role Category (required, radio: Teaching / Non-Teaching / Admin)
  - Employment Type (required, dropdown: Permanent / Contract / Visiting / Probation)
  - Join Date (required, date picker)
  - Date of Birth (required, date picker; staff must be ≥ 18 years)
  - Gender (required, dropdown: Male / Female / Non-Binary / Prefer Not to Say)
  - Contact Number (required, mobile; 10-digit validation)
  - Official Email (optional, text; must be group domain format)
  - Emergency Contact Name (required, text)
  - Emergency Contact Number (required, 10-digit)
  - Probation End Date (required if Employment Type = Probation; date picker)
  - Required Documents Checklist (checkboxes: Aadhaar / PAN / Education Certificates / Experience Letters / Photo / Previous Employer Reference)
- **On submit:** Creates staff record, auto-generates Staff ID, initiates BGV notification to BGV Manager, sends welcome email to official email if provided

### 6.2 Drawer: `staff-view` — View Staff Profile
- **Trigger:** Click on staff name
- **Width:** 720px
- Shows: Full personal and employment details, employment history (if transferred between branches), BGV record summary (with link to full BGV case), POCSO training history, document status breakdown with individual document view, performance review history summary, active or historical disciplinary cases (visible only to HR Director and HR Manager), welfare grievances filed, leave balances (summary from leave management system)

### 6.3 Drawer: `staff-edit` — Edit Staff Record
- **Trigger:** Actions → Edit (visible to HR Director and HR Manager only)
- **Width:** 560px
- Same fields as create, pre-populated; Staff ID is locked; domain-specific fields (BGV Status, POCSO Status) are editable only by the respective domain role

### 6.4 Modal: Deactivate Staff Record
- Confirmation: "You are marking [Staff Name] (Staff ID: [ID]) as Inactive. This will flag their records across all HR modules. If this is an exit, ensure full-and-final settlement has been cleared in the Finance module. Confirm?"
- Dropdown: Reason for Deactivation (Resignation / Termination / Retirement / Transfer Out of Group / Death / Other)
- Buttons: Confirm Deactivate · Cancel

---

## 7. Charts

### 7.1 Staff Strength by Branch (Bar Chart)
- X-axis: Branch names
- Y-axis: Headcount
- Segmented by Employment Type (Permanent / Contract / Visiting)
- Quick visual of branch composition

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Staff record created | "Staff record created. Staff ID: [ID]. BGV Manager notified to initiate background verification." | Success | 5s |
| Staff record updated | "Staff record updated for [Name]." | Success | 3s |
| Staff deactivated | "Record for [Name] marked Inactive. Finance module notified for FnF clearance." | Warning | 5s |
| Bulk BGV initiation triggered | "BGV initiation requested for [N] staff members. BGV Manager notified." | Info | 5s |
| Bulk training assignment done | "Training program assigned to [N] staff members. T&D Manager notified." | Info | 4s |
| Export triggered | "Staff directory export is being prepared." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No staff records | "No Staff Records Found" | "No staff have been added to the group directory yet. Add the first staff member to begin." | + Add Staff |
| No results for applied filter | "No Matching Staff" | "No staff records match the selected filters. Try adjusting your criteria." | Clear Filters |
| All records compliant | "Fully Compliant Directory" | "All active staff have complete BGV, POCSO training, and document records." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (15 rows) |
| Staff profile drawer open | Drawer spinner; each section (BGV, POCSO, performance) loads progressively |
| Staff create form submit | Button spinner; Staff ID generation and notification dispatch running |
| Bulk action submit | Full-screen overlay with progress indicator: "Processing [N] records…" |

---

## 11. Role-Based UI Visibility

| Element | HR Director (G3) | HR Manager (G3) | G3 Domain Roles | Performance Officer (G1) |
|---|---|---|---|---|
| Full Staff Table (all columns) | Visible | Visible | Visible (all rows; limited edit) | Visible (Name, Branch, Role only) |
| + Add Staff Button | Visible | Visible | Hidden | Hidden |
| Edit Action | Visible (all fields) | Visible (all fields) | Visible (domain fields only) | Hidden |
| Deactivate Action | Visible | Visible | Hidden | Hidden |
| Bulk BGV Initiate | Visible | Visible | BGV Manager only | Hidden |
| Bulk Training Assign | Visible | Visible | T&D Manager only | Hidden |
| Export | Visible | Visible | Visible (domain-filtered) | Hidden |
| Disciplinary Cases in Profile | Visible | Visible | Hidden | Hidden |
| Salary / Payroll Data | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/staff/` | JWT (G1+) | Paginated staff directory with role-scoped fields |
| POST | `/api/v1/hr/staff/` | JWT (G3 — HR Director / HR Manager) | Create a new staff record |
| GET | `/api/v1/hr/staff/{id}/` | JWT (G1+) | Full staff profile (fields scoped by role) |
| PATCH | `/api/v1/hr/staff/{id}/` | JWT (G3) | Update staff record (field-level role enforcement) |
| POST | `/api/v1/hr/staff/{id}/deactivate/` | JWT (G3 — HR Director / HR Manager) | Mark staff as inactive |
| POST | `/api/v1/hr/staff/bulk-bgv-initiate/` | JWT (G3 — BGV Manager or above) | Bulk BGV initiation for selected staff IDs |
| POST | `/api/v1/hr/staff/bulk-training-assign/` | JWT (G3 — T&D Manager or above) | Bulk training program assignment |
| GET | `/api/v1/hr/staff/kpis/` | JWT (G1+) | Directory-level KPI values |
| GET | `/api/v1/hr/staff/charts/strength-by-branch/` | JWT (G3) | Staff strength bar chart data |
| GET | `/api/v1/hr/staff/export/` | JWT (G3) | Async export of full or filtered staff directory |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/staff/kpis/` | `#kpi-bar` | `innerHTML` |
| Load staff directory table | `load` | GET `/api/v1/hr/staff/` | `#staff-table` | `innerHTML` |
| Open staff profile drawer | `click` on staff name | GET `/api/v1/hr/staff/{id}/` | `#staff-drawer` | `innerHTML` |
| Apply advanced filters | `change` on any filter control | GET `/api/v1/hr/staff/?branch=...&bgv=...` | `#staff-table` | `innerHTML` |
| Search staff | `input` (300ms debounce) | GET `/api/v1/hr/staff/?q=...` | `#staff-table` | `innerHTML` |
| Submit new staff form | `click` on Submit | POST `/api/v1/hr/staff/` | `#staff-table` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/hr/staff/?page=N` | `#staff-table` | `innerHTML` |
| Execute bulk action | `click` on Confirm in bulk modal | POST `/api/v1/hr/staff/bulk-bgv-initiate/` | `#bulk-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
