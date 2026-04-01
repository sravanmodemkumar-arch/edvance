# 16 — Staff Contract Manager

- **URL:** `/group/hr/contracts/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Contract Manager ensures that every staff member across all branches has a valid, signed employment contract on file before their first working day. This is a foundational HR compliance requirement: a staff member who begins work without a signed contract creates legal liability for the group, exposes it to labour law violations, and complicates dispute resolution. This page provides the Group HR Manager with a complete, real-time view of contract status across the entire staff roster.

Three contract types are managed here. Permanent contracts are issued to confirmed, full-time employees and do not carry an expiry date. Fixed-Term contracts run for one to two years and are common for probationary hires, contractual teachers, or project-based roles. Visiting Faculty contracts span a single semester (approximately five months) and must be renewed each semester. The system tracks all three types under a unified contract lifecycle: Draft → Sent to Staff → Signed → Active → Expiring Soon → Expired. Renewals can be initiated from this page before a contract lapses.

Key risk signals are surfaced prominently. Any staff member flagged as "Active" in the system but whose contract has expired appears as a red alert. Contracts expiring within 30 days receive orange warnings; contracts expiring in 90 days receive yellow reminders. The HR Manager can act from the table directly — initiate a renewal, send the contract for signing, or terminate a contract cleanly. This prevents the common scenario of a visiting faculty member continuing to teach in semester 3 under a semester 1 contract that was never renewed.

Contract documents are stored as PDFs and linked to the staff member's profile (page 14). A PDF preview link is available inside the view drawer without requiring a separate file download. The system also generates automated reminder notifications to branch HR contacts 60 days, 30 days, and 7 days before a fixed-term or visiting contract expires, reducing the reliance on manual calendar tracking.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access — override approvals | Can approve out-of-band salary in contracts |
| Group HR Manager (42) | G3 | Full CRUD — all contracts | Primary owner of this page |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | Read-only | Can view contracts for transfer decisions |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | Read-only | Can view for disciplinary context |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Contracts → Staff Contract Manager`

### 3.2 Page Header
- Title: "Staff Contract Manager"
- Subtitle: "Track and manage employment contracts across all branches."
- Primary CTA: "+ Create Contract"
- Secondary CTAs: "Export Report" | "Bulk Reminder" (sends renewal reminder to all expiring contracts)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any Active staff with expired contract | "[N] active staff member(s) have expired contracts. Immediate renewal or termination required." | Red |
| Contracts expiring within 7 days | "[N] contract(s) expire within 7 days." | Red |
| Contracts expiring within 30 days | "[N] contract(s) expire within 30 days." | Orange |
| Unsigned draft contracts > 14 days old | "[N] contract(s) have been in Draft status for over 14 days." | Yellow |
| Recent bulk reminder sent | "Renewal reminders sent to [N] staff members." | Blue / Info |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Contracts | Count of Signed + Active contracts | Neutral blue | Filters table to Active |
| Expiring in 30 Days | Count expiring within 30 days | Orange if > 0, Green if 0 | Filters table to expiring |
| Expiring in 90 Days | Count expiring within 90 days | Yellow if > 5 | Filters table to 90-day range |
| Expired — Action Needed | Count of expired contracts still tied to active staff | Red if > 0, Green if 0 | Filters table to expired |
| Draft / Unsigned | Count in Draft or Sent-Unsigned status | Amber if > 3 | Filters table to draft |
| Signed This Month | Count of contracts signed in current calendar month | Green | — |

---

## 5. Main Table — Staff Contracts

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to staff profile) | Yes | Yes (search) |
| Branch | Text | Yes | Yes (dropdown) |
| Contract Type | Chip (Permanent / Fixed-Term / Visiting) | Yes | Yes |
| Start Date | Date | Yes | Yes (date range) |
| End Date | Date / "—" for Permanent | Yes | Yes (date range) |
| Status | Chip (Draft / Sent / Signed / Expired / Terminated) | Yes | Yes |
| Days to Expiry | Integer / "N/A" for Permanent | Yes | No |
| Created By | Text | No | No |
| Actions | View / Edit / Renew / Terminate | No | No |

### 5.1 Filters
- Contract Type: All | Permanent | Fixed-Term | Visiting Faculty
- Status: All | Draft | Sent | Signed | Expiring Soon | Expired | Terminated
- Branch: All branches (dropdown)
- Expiry Window: Next 7 Days | Next 30 Days | Next 90 Days | Custom range

### 5.2 Search
Search by staff name or employee ID. Minimum 2 characters, HTMX live search with 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. Navigation controls: First / Previous / Page N of M / Next / Last. Total contract count displayed.

---

## 6. Drawers

### 6.1 Drawer: Create Contract
Fields: Staff Member (typeahead search, required), Branch (auto-populated from staff profile, editable), Contract Type (Permanent / Fixed-Term / Visiting), Start Date (date picker), End Date (date picker — disabled for Permanent, required for Fixed-Term and Visiting), Role Title (auto-populated from staff profile), Salary (₹, must be within grade band — validated), Contract Document (PDF upload, max 10 MB), Special Conditions / Notes (textarea), Send for Signature on Save (checkbox — if checked, status transitions to "Sent" immediately).
Validation: End Date must be after Start Date; Salary within grade band (warning shown if exceeds max — HR Director approval flag set); document upload required before "Send for Signature".
On Save: POST to API, row added to table, toast shown.

### 6.2 Drawer: View Contract
Read-only. Displays all contract fields, PDF preview link (opens in new tab or inline), signature status with timestamp, created/modified audit trail. "Download PDF" button. "Renew" and "Terminate" action buttons at the bottom for authorised users.

### 6.3 Drawer: Edit Contract
Editable only for Draft or Sent (unsigned) contracts. Fields same as Create. Cannot edit a Signed contract — must use Renew to create a new version. Reason for Edit (textarea, required).
On Save: PATCH to API, row updated in place.

### 6.4 Drawer: Renew Contract
Available for Signed contracts with an End Date (Fixed-Term, Visiting). Pre-fills: Staff, Branch, Contract Type, Role. User must set new Start Date (defaults to day after current end date), new End Date, updated Salary, upload new document. On Submit: creates a new contract record linked to the current one. Old contract status moves to "Superseded".

### 6.5 Modal: Terminate Contract
Triggered by "Terminate" action. Fields: Termination Effective Date (date picker), Reason (dropdown: Resignation / End of Term / Misconduct / Redundancy / Other), Notes. Confirmation: "Terminating [Name]'s contract on [Date]. This cannot be undone." On Confirm: PATCH status = Terminated, creates exit record automatically.

---

## 7. Charts

**Contract Expiry Timeline** — horizontal Gantt-style bar chart showing contracts expiring in the next 90 days grouped by month. X-axis: months. Y-axis: staff names (or count per branch). Colour: Red = next 7 days, Orange = 8–30 days, Yellow = 31–90 days. Toggle button: "Show Expiry Chart / Hide". Positioned below the KPI bar.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Contract created | "Contract created for [Staff Name]." | Success | 4s |
| Contract sent for signature | "Contract sent to [Staff Name] for signing." | Success | 4s |
| Contract updated | "Contract updated successfully." | Success | 4s |
| Contract renewed | "Contract renewed. New contract effective [Date]." | Success | 4s |
| Contract terminated | "Contract for [Staff Name] terminated." | Warning | 5s |
| Bulk reminder sent | "Renewal reminders sent to [N] staff members." | Info | 5s |
| Salary out-of-band warning | "Salary exceeds grade band maximum. HR Director approval required." | Warning | 6s |
| PDF upload failed | "Upload failed — PDF only, max 10 MB." | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No contracts in system | "No Contracts on File" | "Create employment contracts for your staff to ensure compliance." | Create Contract |
| Filter returns no results | "No Matching Contracts" | "Adjust your filters to find contracts." | Clear Filters |
| Search returns no results | "No Staff Found" | "Check the staff name or employee ID and try again." | Clear Search |
| Terminated tab empty | "No Terminated Contracts" | "No contracts have been terminated." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI skeletons (6) + table row skeletons (15) |
| Filter/search apply | Table body skeleton replaces content |
| Drawer open | Form field skeletons |
| PDF preview load | Spinner inside preview container |
| Bulk reminder action | Full button spinner + disabled |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | HR Manager (42) | Read-Only (47, 51) |
|---|---|---|---|
| Create Contract button | Visible | Visible + enabled | Hidden |
| Edit action | Visible | Visible | Hidden |
| Renew action | Visible | Visible | Hidden |
| Terminate action | Visible | Visible | Hidden |
| View action | Visible | Visible | Visible |
| Bulk Reminder button | Visible | Visible | Hidden |
| Export Report | Visible | Visible | Visible |
| Out-of-band approval flag | Visible + actionable | Visible as warning only | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/contracts/` | JWT | List all contracts (paginated, filtered) |
| POST | `/api/v1/hr/contracts/` | JWT | Create new contract |
| GET | `/api/v1/hr/contracts/{id}/` | JWT | Fetch contract detail |
| PATCH | `/api/v1/hr/contracts/{id}/` | JWT | Update contract |
| POST | `/api/v1/hr/contracts/{id}/renew/` | JWT | Renew contract (creates new version) |
| PATCH | `/api/v1/hr/contracts/{id}/terminate/` | JWT | Terminate contract |
| POST | `/api/v1/hr/contracts/{id}/send/` | JWT | Send contract for signature |
| GET | `/api/v1/hr/contracts/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/contracts/chart/` | JWT | Expiry timeline chart data |
| POST | `/api/v1/hr/contracts/bulk-reminder/` | JWT | Send renewal reminders |
| GET | `/api/v1/hr/contracts/export/` | JWT | Export contracts report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/contracts/?q={val}` | `#contracts-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/contracts/?type={}&status={}&branch={}` | `#contracts-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/contracts/?page={n}` | `#contracts-table-body` | innerHTML |
| Create drawer open | click | GET `/group/hr/contracts/create/drawer/` | `#drawer-container` | innerHTML |
| View drawer open | click | GET `/group/hr/contracts/{id}/view/drawer/` | `#drawer-container` | innerHTML |
| Edit drawer open | click | GET `/group/hr/contracts/{id}/edit/drawer/` | `#drawer-container` | innerHTML |
| Renew drawer open | click | GET `/group/hr/contracts/{id}/renew/drawer/` | `#drawer-container` | innerHTML |
| Terminate modal | click | GET `/group/hr/contracts/{id}/terminate/modal/` | `#modal-container` | innerHTML |
| Create submit | submit | POST `/api/v1/hr/contracts/` | `#contracts-table-body` | afterbegin |
| Terminate confirm | click | PATCH `/api/v1/hr/contracts/{id}/terminate/` | `#contract-row-{id}` | outerHTML |
| Chart toggle | click | GET `/group/hr/contracts/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
