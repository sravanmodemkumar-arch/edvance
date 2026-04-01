# 13 — User Account Manager

- **URL:** `/group/it/users/accounts/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The User Account Manager is the primary provisioning interface for EduForge user accounts. While the Group User Directory (File 12) is used to search, audit, and manage existing accounts, this page is purpose-built for the operational workflow of creating and lifecycle-managing individual user accounts. It is where the IT Admin spends most of their time during onboarding waves — new academic year staff intake, mid-year joiners, group-level role appointments, and branch-level system administrator setup.

Account creation in EduForge follows a structured flow: every account requires a real human identity (name + mobile), a branch affiliation, a designated role, and an access level. The IT Admin can create accounts directly (for group-level staff who do not go through branch provisioning requests) or provision accounts arising from approved provisioning requests (File 15). Both flows terminate on this page.

A key governance feature is the Account History audit trail: every action taken on a user account — role change, branch reassignment, status toggle, OTP reset — is timestamped and attributed to the actor admin. This history is visible in the View Account History drawer and is non-deletable. This ensures complete accountability for the identity lifecycle of every EduForge user.

Deactivation is handled with deliberate friction: the admin must specify a reason, an effective date, and a "transfer outstanding tasks to" designee, ensuring no operational orphan tasks are left behind when an account is deactivated.

**Account Deletion Policy:** Account deletion is not supported. Accounts are deactivated (marked inactive) to preserve audit trail history. Once deactivated, an account cannot be reactivated — a new account must be created if the user returns.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (create, edit, deactivate all accounts) | Primary operator of this page |
| Group IT Director | G4 | Full read + write | Can approve escalated role assignments |
| Group IT Support Executive | G3 | Read-only | For support reference; cannot create or modify |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Account Manager
```

### 3.2 Page Header
- **Title:** `User Account Manager`
- **Subtitle:** `Provision and manage individual EduForge user accounts`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `+ Create Account` · `Advanced Filters` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Accounts created but activation OTP not confirmed > 48h | "[N] accounts were created more than 48 hours ago and have not been activated. Resend OTP or follow up with user." | Amber |
| Deactivated accounts with pending tasks not transferred | "[N] deactivated accounts have outstanding tasks that have not been transferred. Assign a designee." | Red |
| Role escalation pending IT Director approval | "[N] access level changes are awaiting IT Director approval." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Accounts | All user accounts regardless of status | Blue | No filter |
| Active Accounts | Accounts with status = Active | Green always | Filtered by Active |
| Created This Month | Accounts created in the current calendar month | Blue | Filtered by current month |
| Deactivated This Month | Accounts deactivated in the current calendar month | Blue (informational) | Filtered by deactivated + month |

---

## 5. Main Table — User Account Manager

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Username | Text (auto-generated, read-only) | Yes | Yes (text search) |
| Full Name | Text (link opens View History drawer) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Role / Designation | Text | Yes | Yes (text search) |
| Access Level | Badge (G0–G5) | Yes | Yes (multi-select) |
| Status | Badge (Active / Inactive / Suspended / Pending Activation) | Yes | Yes |
| Created Date | Date | Yes | Yes (date range) |
| Created By | Text (admin name) | No | No |
| Actions | View History / Edit / Deactivate | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All group branches |
| Access Level | Checkbox | G0 / G1 / G2 / G3 / G4 / G5 |
| Status | Checkbox | Active / Inactive / Suspended / Pending Activation |
| Created Date Range | Date range picker | Any range |
| Created By | Text search | Admin username |

### 5.2 Search
- Full-text search: Username, Full Name, Email, Branch, Role
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page

---

## 6. Drawers

### 6.1 Drawer: `account-create` — Create New User Account
- **Trigger:** `+ Create Account` button
- **Width:** 480px
- **Fields:**
  - Full Name (required, text)
  - Mobile Number (required, 10-digit; this is the OTP delivery number)
  - Email Address (optional, text; used for email notifications)
  - Branch (required, dropdown; all group branches)
  - Role / Designation (required, text; e.g., "Branch Principal", "Fee Accountant")
  - Access Level (required, dropdown: G0 / G1 / G2 / G3 / G4 / G5; G4/G5 require IT Director confirmation)
  - Username (auto-generated from name + branch code; editable before save, unique validated)
  - Send Activation OTP (checkbox, default checked; uncheck only if account is pre-staged for later)
  - Provisioned From Request (optional, lookup field to link to a Provisioning Request #)
- **Validation:** Mobile uniqueness check (no two accounts share the same mobile); username uniqueness enforced
- **On submit:** Account created in PostgreSQL; if OTP checkbox checked, OTP sent via WhatsApp/SMS; audit log entry written

### 6.2 Drawer: `account-edit` — Edit User Account
- **Trigger:** Actions → Edit
- **Width:** 480px
- **Editable fields:** Full Name, Email, Mobile Number, Branch, Role/Designation, Access Level, Status
- **Read-only:** Username, User ID, Created Date, Created By
- **Access Level escalation to G4/G5:** Requires IT Director confirmation — a confirmation dialog pops asking IT Director to verify (if IT Admin is self-approving, blocked; must be a different G4 user)
- **Branch change:** Logs a branch-transfer event in account history; existing sessions invalidated

### 6.3 Modal: Deactivate Account
- **Trigger:** Actions → Deactivate
- **Type:** Centered modal (500px wide)
- **Content:** "You are deactivating the account for [Full Name] ([Username]) at [Branch]. Their access to EduForge will be removed immediately."
- **Fields:**
  - Deactivation Reason (required, dropdown: Resignation / Termination / Role Ended / Duplicate Account / Other)
  - Additional Notes (optional, textarea)
  - Effective Date (required, date picker; default today; can be a future date for scheduled deactivation)
  - Transfer Outstanding Tasks To (required, user lookup — type name to search active users at same branch)
  - Notify Branch Principal (checkbox, default checked)
- **Buttons:** Confirm Deactivate (red) · Cancel

### 6.4 Drawer: `account-history` — View Account History
- **Trigger:** Actions → View History (or click Full Name in table)
- **Width:** 480px
- **Content:** Chronological audit trail of all events on this account, newest first:
  - Account Created (timestamp, created by, initial role and access level)
  - Role / Designation Change (old value → new value, changed by, timestamp)
  - Branch Change (old branch → new branch, changed by, timestamp)
  - Access Level Change (old G-level → new G-level, approved by, timestamp)
  - Status Change (Active → Suspended, etc., reason, changed by, timestamp)
  - OTP Reset (triggered by, timestamp)
  - Login Events summary: count of successful/failed logins in last 30 days; link navigates to Page 17 (Session & Login Audit) filtered by this user
- Each event row is non-editable and non-deletable

---

## 7. Charts

### 7.1 Account Creation vs Deactivation Trend (Bar Chart)
- **Type:** Grouped bar chart
- **X-axis:** Last 12 months (month labels)
- **Y-axis:** Account count
- **Series:** Accounts Created (blue bars) · Accounts Deactivated (red bars)
- **Purpose:** Visual trend of net user growth; useful at academic year start (spike in creation) and year end (spike in deactivation)
- **Data source:** GET `/api/v1/it/users/accounts/charts/trend/`
- **Placement:** Below KPI bar, above main table, collapsible

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Account created with OTP | "Account created for [Name]. Activation OTP sent to [masked phone]." | Success | 5s |
| Account created without OTP | "Account created for [Name]. OTP not sent — account is in Pending Activation state." | Info | 5s |
| Account updated | "Account updated for [Name]." | Success | 3s |
| Account deactivated | "[Name]'s account has been deactivated. Outstanding tasks transferred to [Designee Name]." | Warning | 5s |
| Access level change submitted for approval | "Access level change for [Name] submitted for IT Director approval." | Info | 5s |
| Duplicate mobile number | "An account with this mobile number already exists. Each mobile number must be unique." | Error | 6s |
| Username conflict | "Username '[username]' is already taken. A suggested alternative: '[suggestion]'." | Error | 5s |
| Deactivation failed | Error: `Could not deactivate [Name]. Please try again.` | Error | 5s |
| Designee not found | Error: `The selected designee could not be found. Select a different user.` | Error | 5s |
| Escalation rejected | Error: `Access level escalation for [Name] was rejected. Review rejection notes.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No accounts exist | "No Accounts Yet" | "No EduForge user accounts have been created. Create the first account to get started." | + Create Account |
| No results for filters/search | "No Matching Accounts" | "No accounts match the selected filters. Try adjusting branch, status, or access level." | Clear Filters |
| Account history drawer — no history | "No History Available" | "No changes have been recorded for this account beyond its initial creation." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + trend chart skeleton + table skeleton (15 rows) |
| Chart data loading | Chart area shows pulsing skeleton of 12 bar pairs |
| Create account drawer open | Drawer skeleton; branch dropdown async-loads branches |
| Account history drawer open | Drawer skeleton; events load progressively via HTMX |
| Form submit (create / edit) | Button spinner; table refreshes on success |
| Deactivate confirm | Button spinner in modal; modal closes, table row updates status badge |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) |
|---|---|---|---|
| Full table | Visible | Visible | Visible |
| + Create Account | Visible | Visible | Hidden |
| Edit Action | Visible | Visible | Hidden |
| Deactivate Action | Visible | Visible | Hidden |
| View History Action | Visible | Visible | Visible |
| Access Level escalation (G4/G5) | Submit only (needs other G4 approval) | Can self-approve for others | Hidden |
| Export button | Visible | Visible | Hidden |
| Trend chart | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/users/accounts/` | JWT (G3+) | Paginated account list with filters |
| POST | `/api/v1/it/users/accounts/` | JWT (G4) | Create a new user account |
| GET | `/api/v1/it/users/accounts/{id}/` | JWT (G3+) | Single account details |
| PATCH | `/api/v1/it/users/accounts/{id}/` | JWT (G4) | Update account fields |
| POST | `/api/v1/it/users/accounts/{id}/deactivate/` | JWT (G4) | Deactivate account; transfer tasks |
| GET | `/api/v1/it/users/accounts/{id}/history/` | JWT (G3+) | Full audit trail for an account |
| GET | `/api/v1/it/users/accounts/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/it/users/accounts/charts/trend/` | JWT (G3+) | 12-month creation vs deactivation data |
| GET | `/api/v1/it/users/accounts/export/` | JWT (G4) | Async CSV/XLSX export |
| POST | `/api/v1/it/users/accounts/{id}/approve-level-change/` | JWT (G4 — IT Director only) | Approve G4/G5 access level escalation |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/users/accounts/kpis/` | `#kpi-bar` | `innerHTML` |
| Load trend chart | `load` | GET `/api/v1/it/users/accounts/charts/trend/` | `#trend-chart` | `innerHTML` |
| Load accounts table | `load` | GET `/api/v1/it/users/accounts/` | `#accounts-table` | `innerHTML` |
| Search accounts | `input` (300ms debounce) | GET `/api/v1/it/users/accounts/?q=...` | `#accounts-table` | `innerHTML` |
| Apply filters | `change` | GET `/api/v1/it/users/accounts/?branch=...` | `#accounts-table` | `innerHTML` |
| Paginate | `click` on page control | GET `/api/v1/it/users/accounts/?page=N` | `#accounts-table` | `innerHTML` |
| Open account history drawer | `click` on Full Name | GET `/api/v1/it/users/accounts/{id}/history/` | `#account-drawer` | `innerHTML` |
| Submit create form | `click` on Create Account | POST `/api/v1/it/users/accounts/` | `#accounts-table` | `innerHTML` |
| Submit edit form | `click` on Save Changes | PATCH `/api/v1/it/users/accounts/{id}/` | `#accounts-table` | `innerHTML` |
| Confirm deactivation | `click` on Confirm Deactivate | POST `/api/v1/it/users/accounts/{id}/deactivate/` | `#accounts-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
