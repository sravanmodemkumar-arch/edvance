# 16 — Bulk User Operations

- **URL:** `/group/it/users/bulk/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The Bulk User Operations page is the high-throughput batch management interface for EduForge user accounts. It exists because individual account management — one record at a time — becomes impractical at scale. At the start of each academic year, a large group may need to import 300–500 new teaching and non-teaching staff accounts across all branches. At the end of the year, 200–400 accounts may need to be deactivated as staff exit. Mid-year role reorganisations may require 50–100 accounts to shift roles simultaneously. These operations must be fast, safe, and auditable.

The page is structured as a wizard-style multi-step interface rather than a traditional data table. There is no persistent list to browse — instead, the admin selects an operation (tab), follows a guided step-by-step flow, reviews a preview before committing, and receives a results summary. This deliberate design prevents accidental mass operations and ensures the admin has explicitly confirmed the impact before execution.

Four operations are available:
- **Bulk Import:** Upload CSV → validate → preview → import new accounts
- **Bulk Deactivate:** Filter users → preview list → confirm deactivation with reason
- **Bulk Role Change:** Select users → pick new role → preview → confirm (with IT Director approval gate for >50 accounts)
- **Bulk Export:** Apply filters → export user list as CSV or XLSX for external audit

All bulk operations are atomic within PostgreSQL transactions — either all rows succeed or the entire batch is rolled back with a per-row error report. No partial commits without explicit admin acknowledgement of the error rows.

All bulk operations are logged to the IT Audit Log, including operator name, timestamp, operation type (Import/Deactivate/Role Change), number of rows affected, and any error counts.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full access (all four operations) | Primary operator |
| Group IT Director | G4 | Full access + bulk role change approval gate | Must approve bulk role changes > 50 accounts |
| Group IT Support Executive | G3 | Bulk Export only | Read-only export for support audit |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Bulk Operations
```

### 3.2 Page Header
- **Title:** `Bulk User Operations`
- **Subtitle:** `Import, deactivate, and manage user accounts at scale`
- **Role Badge:** `Group IT Admin`
- **No right-side action buttons** — all actions are within the wizard tabs below

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| A previous bulk import is still processing | "A bulk import is currently being processed ([N] of [M] rows completed). Do not start a new import." | Amber |
| Bulk role change pending IT Director approval | "A bulk role change affecting [N] accounts is awaiting IT Director approval." | Amber |
| Last import had validation errors | "The last bulk import completed with [N] validation errors. Download the error report." | Red (dismissible) |

---

## 4. KPI Summary Bar

No KPI cards on this page — the wizard-step UI uses the full width. Operation context (e.g., "N users selected for deactivation") is shown inline within each wizard step.

---

## 5. Main Table

There is no persistent main data table on this page. Each operation's Step 3 (Preview) displays a temporary preview table of the records to be processed — this is not paginated in the traditional sense but shows up to 200 rows in a scrollable container with a "Download full preview as CSV" link for larger sets.

### Preview Table (Steps 3 of each operation) — common columns:
| Column | Notes |
|---|---|
| # | Row number |
| Full Name | From CSV or selected filter |
| Branch | Branch name |
| Role / Designation | Current role (or new role for Role Change) |
| Access Level | Current G-level (or new G-level) |
| Status | Current account status |
| Validation | Green tick (row OK) / Red cross (row has error with error message) |

---

## 6. Drawers

This page uses no slide-out drawers. All interaction is within the main wizard area. Confirmations use inline modals.

### Operation 1: Bulk Import — Wizard Steps

**Step 1 — Download Template & Upload CSV**
- Download CSV template button (pre-formatted with required column headers)
- Required columns: Full Name, Mobile Number, Email (optional), Branch Code, Role/Designation, Access Level (G0–G5)
- File upload dropzone (accepts .csv only, max 5 MB)
- HTMX: file selection triggers immediate upload to validation endpoint

**CSV Column Format Validation:**
- Full Name: 1–100 characters, no special characters
- Mobile Number: 10 digits, numeric only
- Email: valid email format (optional)
- Branch Code: must match configured branch codes (e.g., BR001)
- Role/Designation: max 50 characters; must match predefined role list
- Access Level: G0, G1, G2, G3, G4, or G5 only

**Step 2 — Validation Results**
- Preview table with per-row validation status
- Errors flagged: duplicate mobile, invalid branch code, invalid access level, missing required fields, duplicate username
- Summary: "[N] rows valid, [M] rows have errors"
- Options: Fix and Re-upload · Proceed with Valid Rows Only (skip errored rows)
- Download error report (CSV of errored rows with error descriptions)

**Step 3 — Preview**
- Scrollable table of all valid rows to be imported
- Total count: "You are about to create [N] new user accounts."

**Step 4 — Confirm**
- Confirmation: "Confirm creation of [N] user accounts across [P] branches. Activation OTPs will be sent to all users."
- OTP send option: Send Activation OTP immediately (default yes) / Stage accounts for manual OTP later
- Final Confirm Import button (green)

**Step 5 — Result**
- Success summary: "[N] accounts created successfully."
- Error summary (if partial): "[M] rows failed. Download error report."
- Links: Go to Account Manager · Start Another Import

---

### Operation 2: Bulk Deactivate — Wizard Steps

**Step 1 — Select Users**
- Filter controls: Branch (multi-select), Role/Designation (text), Access Level, Status
- "Load Preview" button triggers Step 2

**Step 2 — Preview**
- Table of users matching selected filters
- Count: "[N] accounts will be deactivated."
- Individual row deselect: checkboxes allow removing specific users from the batch

**Step 3 — Confirm Deactivation**
- Deactivation Reason (required, dropdown: End of Academic Year / Staff Exit / Role Ended / Other)
- Additional Notes (optional textarea)
- Effective Date (date picker; default today)
- Transfer Outstanding Tasks To (user lookup — single designee for entire batch, or "No transfer required")
- Final Confirm Deactivation button (red)

**Step 4 — Result**
- "[N] accounts deactivated."

---

### Operation 3: Bulk Role Change — Wizard Steps

**Step 1 — Select Users**
- User search/filter + checkbox selection from filtered table
- Selected count shown dynamically

**Step 2 — Select New Role**
- New Role / Designation (text)
- New Access Level (dropdown G0–G5)
- If Access Level escalates to G4/G5: warning displayed; requires IT Director approval before commit

**Step 3 — Preview**
- Table: Name | Branch | Current Role → New Role | Current Level → New Level

**Step 4 — Confirm**
- If ≤ 50 accounts: IT Admin can self-approve; confirm button available
- If > 50 accounts: "This change affects [N] accounts and requires IT Director approval. Submit for Approval button replaces Confirm."

**Step 5 — Result / Pending Approval**
- ≤ 50: "[N] role changes applied."
- > 50: "Role change request submitted for IT Director approval. Changes pending."

---

### Operation 4: Bulk Export — Wizard Steps

**Step 1 — Select Filters**
- Same filter controls as the User Directory (Branch, Access Level, Status, Date Range, Last Login)

**Step 2 — Select Format**
- Format: CSV / XLSX
- Columns to include (checklist — default all)

**Step 3 — Confirm & Export**
- Export button; file generated server-side, download link returned

---

## 7. Charts

No charts on this page. The wizard interface is the primary interaction surface.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Bulk import completed (all success) | "[N] user accounts imported successfully. OTPs sent to all users." | Success | 5s |
| Bulk import completed (with errors) | "[N] accounts imported. [M] rows had errors. Download error report." | Warning | 7s (persistent until dismissed) |
| Bulk deactivation completed | "[N] accounts deactivated successfully. Effective date: [date]." | Warning | 5s |
| Bulk role change applied | "[N] role changes applied successfully." | Success | 5s |
| Bulk role change submitted for approval | "Role change request for [N] accounts submitted for IT Director approval." | Info | 5s |
| Bulk export ready | "Export ready. [Download CSV]." | Success | 10s (with download link) |
| CSV upload rejected (wrong format) | "Upload failed: only .csv files are accepted. Please use the provided template." | Error | 5s |
| CSV file too large | Error: `File exceeds 5MB limit. Please reduce file size and re-upload.` | Error | 5s |
| CSV file corrupt | Error: `Uploaded file appears corrupt. Re-download the template and try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| Bulk deactivate — no users match filter | "No Users Match These Filters" | "No active user accounts match the selected branch and role filters. Adjust and try again." | Adjust Filters |
| Bulk role change — no users selected | "No Users Selected" | "Select at least one user account to proceed with the role change." | Go back to Step 1 |
| Bulk export — no records match filter | "No Records to Export" | "No user accounts match the selected export filters." | Adjust Filters |
| Step 2 validation — all rows errored | "All Rows Have Errors" | "Every row in the uploaded CSV has validation errors. Fix the file and re-upload." | Re-upload CSV |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| CSV file upload + validation | Full-width progress bar: "Validating [N] rows…" with row count ticker |
| Load preview (deactivate/role change) | Preview table skeleton (up to 20 rows shimmer) |
| Confirm import | Step 5 progress: "Creating accounts: [N] of [M] complete" (progress bar, updates via HTMX poll) |
| Confirm bulk deactivation | Overlay spinner: "Deactivating [N] accounts…" |
| Bulk export generation | Spinner + "Preparing export…" message; download link replaces spinner on completion |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) |
|---|---|---|---|
| Bulk Import tab | Visible | Visible | Hidden |
| Bulk Deactivate tab | Visible | Visible | Hidden |
| Bulk Role Change tab | Visible | Visible (approver only) | Hidden |
| Bulk Export tab | Visible | Visible | Visible |
| Approval gate (> 50 role changes) | Submit only | Approve/Reject | Hidden |
| Download error report | Visible | Visible | Hidden |
| OTP send option (import) | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/it/users/bulk/import/validate/` | JWT (G4) | Upload and validate CSV; returns per-row status |
| POST | `/api/v1/it/users/bulk/import/commit/` | JWT (G4) | Commit validated rows; creates accounts |
| POST | `/api/v1/it/users/bulk/deactivate/preview/` | JWT (G4) | Returns list of users matching deactivation filters |
| POST | `/api/v1/it/users/bulk/deactivate/commit/` | JWT (G4) | Commit bulk deactivation |
| POST | `/api/v1/it/users/bulk/role-change/preview/` | JWT (G4) | Preview role change impact for selected users |
| POST | `/api/v1/it/users/bulk/role-change/submit/` | JWT (G4) | Submit role change (for ≤ 50) or request approval (> 50) |
| POST | `/api/v1/it/users/bulk/role-change/approve/` | JWT (G4 — IT Director) | Approve pending bulk role change |
| GET | `/api/v1/it/users/bulk/import/status/{job_id}/` | JWT (G4) | Poll import job progress |
| GET | `/api/v1/it/users/bulk/export/` | JWT (G3+) | Generate and return filtered user export |
| GET | `/api/v1/it/users/bulk/import/{job_id}/errors/` | JWT (G4) | Download error report for a completed import job |
| GET | `/api/v1/it/users/bulk/import/is-processing/` | JWT (G4) | Check if a bulk import job is currently running |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| CSV file selected (auto-upload) | `change` on file input | POST `/api/v1/it/users/bulk/import/validate/` | `#validation-results` | `innerHTML` |
| Load deactivation preview | `click` on Load Preview | POST `/api/v1/it/users/bulk/deactivate/preview/` | `#preview-table` | `innerHTML` |
| Load role change preview | `click` on Preview Changes | POST `/api/v1/it/users/bulk/role-change/preview/` | `#preview-table` | `innerHTML` |
| Confirm import | `click` on Confirm Import | POST `/api/v1/it/users/bulk/import/commit/` | `#wizard-step` | `innerHTML` |
| Poll import progress | `every 2s` (while processing) | GET `/api/v1/it/users/bulk/import/status/{job_id}/` | `#import-progress` | `innerHTML` |
| Confirm bulk deactivation | `click` on Confirm Deactivation | POST `/api/v1/it/users/bulk/deactivate/commit/` | `#wizard-step` | `innerHTML` |
| Submit bulk role change | `click` on Confirm/Submit | POST `/api/v1/it/users/bulk/role-change/submit/` | `#wizard-step` | `innerHTML` |
| Trigger export | `click` on Export | GET `/api/v1/it/users/bulk/export/?...` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
