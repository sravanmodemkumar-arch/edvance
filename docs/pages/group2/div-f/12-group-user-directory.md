# 12 — Group User Directory

- **URL:** `/group/it/users/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The Group User Directory is the master searchable registry of every EduForge user account across all branches in the group. Every individual who holds an EduForge login — from the Group Chairman and Branch Principal down to the Transport Warden and Parent Observer — appears as a single row in this directory. The directory is the authoritative source of truth for user identity, access level, branch linkage, and account lifecycle state across the entire platform.

This page serves three primary operational purposes. First, it is the user lifecycle management hub: the IT Admin can view, edit, suspend, or trigger a password/OTP reset for any account without navigating to a branch-specific portal. Second, it is the role verification surface: when a branch raises a ticket ("our principal cannot log in" or "a teacher has wrong access level"), the IT Admin resolves it here in seconds. Third, it is the access audit tool: the security and compliance team uses this page to verify that no ghost accounts, over-privileged roles, or deactivated-but-not-suspended accounts exist.

The scale of this directory is significant — a 20-branch group may carry 10,000–25,000 user records including all student accounts, parent accounts, and staff accounts. All queries are server-side with indexed PostgreSQL lookups; no in-memory filtering is performed in the browser. Multi-select filters, full-text search with 300ms debounce, and server-side pagination at 25 rows per page ensure performance at any scale.

Bulk operations (suspend batch, reset OTP batch, export filtered list) are available from this page and logged to the IT Audit Log with the initiating admin's identity and timestamp. The directory integrates read-only with the Session & Login Audit page (File 17) — clicking any user's "Last Login" cell navigates to their filtered session log.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (all users, all branches) | Can suspend, edit roles, reset OTP |
| Group IT Director | G4 | Full read + write | Strategic oversight; can view all records |
| Group Cybersecurity Officer | G1 | Read-only (all columns) | Cannot edit or suspend; view audit purpose |
| Group Data Privacy Officer | G1 | Read-only (Name, Branch, Status only) | DPDP Act compliance audits only |
| Group IT Support Executive | G3 | Read-only + OTP Reset only | Cannot change roles or suspend accounts |
| Group IT Support Executive (Role 57, G3) | Read-only + OTP Reset only | Cannot change roles or suspend accounts |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → User Directory
```

### 3.2 Page Header
- **Title:** `Group User Directory`
- **Subtitle:** `[Total Count] Users · [N] Branches · [N] Active · [N] Suspended · AY [current academic year]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Bulk Actions` (dropdown) · `Advanced Filters` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Users with no login for > 90 days but status Active | "[N] active accounts have not logged in for more than 90 days. Review for deactivation." | Amber |
| Accounts in Pending Activation state > 7 days | "[N] accounts are awaiting activation for more than 7 days. Resend OTP or follow up with branch." | Amber |
| Accounts with overdue mandatory password/OTP reset | "[N] accounts have exceeded the mandatory OTP reset deadline set in Auth Policy." | Red |
| Suspended accounts with active sessions (data anomaly) | "[N] suspended account(s) have an active session. Force logout and investigate." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Users | All user accounts across all branches | Blue | No filter applied |
| Active Users | Accounts with status = Active | Green always | Filtered by Active |
| Inactive / Suspended | Accounts with status = Inactive or Suspended | Red if > 5% of total, else Blue | Filtered by those statuses |
| New Users (Last 30 Days) | Accounts created in last 30 calendar days | Blue | Filtered by created date |
| Overdue OTP Reset | Accounts past mandatory OTP reset date | Red if > 0, Green if 0 | Filtered by overdue reset |

---

## 5. Main Table — Group User Directory

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Name | Text (link opens View drawer) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Role / Designation | Text | Yes | Yes (text search) |
| Access Level | Badge (G0 / G1 / G2 / G3 / G4 / G5) | Yes | Yes (multi-select) |
| Email / Phone | Text (OTP delivery contact, partially masked) | No | No |
| Status | Badge (Active / Inactive / Suspended / Pending Activation) | Yes | Yes (multi-select) |
| Last Login Date | Date (relative: "3 days ago") | Yes | Yes (Never / >30d / >90d) |
| Account Created | Date | Yes | Yes (date range) |
| Actions | View / Edit / Suspend / Reset OTP | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches in group |
| Access Level | Checkbox | G0 / G1 / G2 / G3 / G4 / G5 |
| Status | Checkbox | Active / Inactive / Suspended / Pending Activation |
| Created Date Range | Date range picker | Any range |
| Last Login | Radio | Any / Never logged in / > 30 days ago / > 90 days ago |

### 5.2 Search
- Full-text search across: Name, Email, Phone, Username, Branch, Role/Designation
- 300ms debounce; min 2 characters

### 5.3 Pagination
- Server-side · 25 rows/page · Total record count always displayed

---

## 6. Drawers

### 6.1 Drawer: `user-view` — View User Profile
- **Trigger:** Click user name or Actions → View
- **Width:** 480px
- **Content sections:**
  - **Identity:** Full name, username, email, phone (masked last 4 digits), profile photo if set
  - **Account Details:** Access level badge, role/designation, branch(es) linked, account status, account created date, account created by (admin name)
  - **Login History:** Last 10 login events (timestamp, IP, device type, status) — loaded lazily with HTMX on drawer open
  - **Role Assignments:** All roles currently assigned to this user with effective dates
  - **Linked Branches:** Multi-branch users list all linked branches with access level per branch
  - **Audit Trail:** Last 5 account changes (role change, status change, OTP reset, branch change) with actor and timestamp
- **Actions at bottom:** Edit · Suspend · Reset OTP (visible per role permissions)

### 6.2 Drawer: `user-edit` — Edit User Account
- **Trigger:** Actions → Edit
- **Width:** 480px
- **Fields (pre-populated, editable):**
  - Full Name (text)
  - Email (text; triggers OTP resend if changed)
  - Mobile Number (text; triggers OTP resend if changed)
  - Branch (dropdown; changing branch logs a branch-transfer event)
  - Role / Designation (text)
  - Access Level (dropdown: G0–G5; requires IT Director confirmation if escalating to G4/G5)
  - Status (dropdown: Active / Inactive / Pending Activation)
- **Read-only fields:** Username, Account Created Date, User ID
- **On submit:** PATCH to user endpoint; audit log entry created; if access level changed, active sessions invalidated

### 6.3 Modal: Suspend User
- **Trigger:** Actions → Suspend
- **Type:** Centered modal (480px wide)
- **Content:** "You are suspending [User Name] ([Username]) at [Branch]. All active sessions will be terminated immediately. The user will not be able to log in until the suspension is lifted."
- **Fields:**
  - Suspension Reason (required, textarea)
  - Suspension Duration (radio: 24 hours / 7 days / 30 days / Indefinite)
  - Notify Branch Principal (checkbox, default checked)
- **Buttons:** Confirm Suspend (red) · Cancel

### 6.4 Modal: Unsuspend / Lift Suspension
- **Trigger:** Actions → Unsuspend (visible only when row Status = Suspended)
- **Type:** Centered modal (480px wide)
- **Content:** "You are lifting the suspension for [User Name] ([Username]) at [Branch]. Their account will be restored to Active and they will be able to log in immediately."
- **Fields:**
  - Reason for Lifting Suspension (required, textarea — min 20 characters)
  - Notify User via WhatsApp (checkbox, default checked)
  - Notify Branch Principal (checkbox, default checked)
- **Buttons:** Confirm Unsuspend (green) · Cancel
- **On confirm:** POST to unsuspend endpoint; account status → Active; toast shown; audit log entry written.

### 6.5 Modal: Reset OTP
- **Trigger:** Actions → Reset OTP
- **Type:** Centered modal (400px wide)
- **Content:** "A new OTP will be sent to [masked phone number] for user [User Name]. Their current OTP credentials will be invalidated immediately."
- **Confirmation:** Single Confirm button + Cancel
- **On confirm:** POST to reset-otp endpoint; toast shows "OTP reset initiated for [Name]. OTP sent to registered mobile."

---

## 7. Charts

No dedicated chart section on this page. KPI cards serve as the primary data visualisation. The session audit page (File 17) carries login trend charts. For user-growth analytics, refer to `/group/it/analytics/` (separate page).

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| User account updated | "Account updated for [Name]." | Success | 3s |
| Suspension confirmed | "[Name]'s account has been suspended. Active sessions terminated." | Warning | 5s |
| Suspension lifted | "[Name]'s account has been restored to Active." | Success | 4s |
| OTP reset sent | "OTP reset initiated for [Name]. OTP sent to registered mobile." | Success | 4s |
| Bulk suspend completed | "[N] accounts suspended. Branch principals notified." | Warning | 5s |
| Bulk OTP reset triggered | "OTP reset initiated for [N] accounts." | Info | 4s |
| Export triggered | "User directory export is being prepared. You will be notified when ready." | Info | 4s |
| Role escalation pending approval | "Access level change for [Name] submitted for IT Director approval." | Info | 5s |
| Suspend failed | Error: `Could not suspend [Name]. Please try again or contact support.` | Error | 5s |

---

## 8.5 Notifications for Critical Actions

| Action | Recipients | Channel | Timing |
|--------|-----------|---------|--------|
| Group-level admin (Role 53–56) suspended | IT Director + Group CEO | In-app alert + email | Immediate |
| OTP reset performed | IT Admin (logged; no active notification) | Audit log only | On action |
| Bulk suspension (>10 users) | IT Director | In-app alert + email | Immediate |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No user records at all | "No User Accounts Found" | "No EduForge user accounts exist in this group yet. Accounts are created via the User Account Manager." | Go to Account Manager |
| No results for applied filters | "No Matching Users" | "No user accounts match the selected filters. Try adjusting the branch, status, or access level filters." | Clear Filters |
| No results for search term | "No Users Found" | "No accounts match '[search term]'. Check the name, email, or username and try again." | Clear Search |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 5 KPI shimmer cards + table skeleton (15 rows × 9 columns) |
| Filter or search applied | Table skeleton replaces rows; KPI bar does NOT reload |
| View drawer open | 480px drawer skeleton; login history section has its own spinner (lazy load) |
| Edit form submit | Button spinner on "Save Changes"; table row refreshes on success |
| Suspend / Reset OTP modal confirm | Button spinner; modal closes on success |
| Bulk action confirm | Full-screen overlay: "Processing [N] accounts…" with spinner |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Cybersecurity Officer (G1) | Data Privacy Officer (G1) | IT Support Executive (G3) |
|---|---|---|---|---|---|
| Full table (all columns) | Visible | Visible | Visible | Name/Branch/Status only | Visible |
| Email / Phone column | Visible (partial mask) | Visible (partial mask) | Visible (partial mask) | Hidden | Hidden |
| Edit Action | Visible | Visible | Hidden | Hidden | Hidden |
| Suspend Action (status ≠ Suspended) | Visible | Visible | Hidden | Hidden | Hidden |
| Unsuspend Action (status = Suspended) | Visible | Visible | Hidden | Hidden | Hidden |
| Reset OTP Action | Visible | Visible | Hidden | Hidden | Visible |
| Bulk Actions dropdown | Visible | Visible | Hidden | Hidden | Hidden |
| Export button | Visible | Visible | Visible (read-only export) | Hidden | Hidden |
| Access Level escalation | Visible (pending IT Director approval) | Visible (self-approve) | Hidden | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/users/` | JWT (G1+) | Paginated user directory; fields scoped by role |
| GET | `/api/v1/it/users/{id}/` | JWT (G1+) | Full user profile; login history loaded separately |
| GET | `/api/v1/it/users/{id}/login-history/` | JWT (G1+) | Last 10 login events for a specific user |
| PATCH | `/api/v1/it/users/{id}/` | JWT (G4 — IT Admin / IT Director) | Update user account fields |
| POST | `/api/v1/it/users/{id}/suspend/` | JWT (G4) | Suspend account; terminates active sessions |
| POST | `/api/v1/it/users/{id}/unsuspend/` | JWT (G4) | Lift suspension; restores account to Active |
| POST | `/api/v1/it/users/{id}/reset-otp/` | JWT (G3+) | Trigger OTP reset for a user |
| POST | `/api/v1/it/users/bulk-suspend/` | JWT (G4) | Bulk suspend selected user IDs |
| POST | `/api/v1/it/users/bulk-reset-otp/` | JWT (G4) | Bulk OTP reset for selected user IDs |
| GET | `/api/v1/it/users/kpis/` | JWT (G1+) | KPI card values for the directory |
| GET | `/api/v1/it/users/export/` | JWT (G3+) | Async export of filtered user list as CSV/XLSX |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/users/kpis/` | `#kpi-bar` | `innerHTML` |
| Load user table | `load` | GET `/api/v1/it/users/` | `#user-table` | `innerHTML` |
| Search users | `input` (300ms debounce) | GET `/api/v1/it/users/?q=...` | `#user-table` | `innerHTML` |
| Apply filters | `change` on any filter control | GET `/api/v1/it/users/?branch=...&status=...` | `#user-table` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/users/?page=N` | `#user-table` | `innerHTML` |
| Open view drawer | `click` on user name | GET `/api/v1/it/users/{id}/` | `#user-drawer` | `innerHTML` |
| Load login history in drawer | `load` (drawer inner) | GET `/api/v1/it/users/{id}/login-history/` | `#login-history-section` | `innerHTML` |
| Submit edit form | `click` on Save Changes | PATCH `/api/v1/it/users/{id}/` | `#user-table` | `innerHTML` (after close) |
| Confirm suspend | `click` on Confirm Suspend | POST `/api/v1/it/users/{id}/suspend/` | `#user-table` | `innerHTML` |
| Confirm unsuspend | `click` on Confirm Unsuspend | POST `/api/v1/it/users/{id}/unsuspend/` | `#user-table` | `innerHTML` |
| Confirm OTP reset | `click` on Confirm | POST `/api/v1/it/users/{id}/reset-otp/` | `#toast-container` | `afterbegin` |
| Bulk action confirm | `click` on Confirm in bulk modal | POST `/api/v1/it/users/bulk-suspend/` | `#bulk-result-banner` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
