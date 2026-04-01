# 17 — Session & Login Audit

- **URL:** `/group/it/users/sessions/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner; Group Cybersecurity Officer (Role 56, G1) — read-only

---

## 1. Purpose

The Session & Login Audit page is the security monitoring and incident investigation surface for all EduForge login activity across the entire group. Every login attempt — successful or failed — every active session, and every suspicious authentication event is recorded in the PostgreSQL audit log and surfaced on this page. The IT Admin uses this page daily to detect anomalies; the Cybersecurity Officer monitors it continuously as part of their threat-monitoring responsibility.

The page is designed around three use cases. First, real-time session monitoring: the IT Admin can see how many users are actively logged in right now, identify any account that has concurrent sessions from different IP addresses (a potential account-sharing or compromise indicator), and force-logout any session directly from this page. Second, incident investigation: when a teacher reports "I cannot log in" or "someone else seems to be using my account," the IT Admin types the name into the search box and immediately sees every login event for that user — IP addresses, device types, success/failure status. Third, brute-force detection: the system automatically flags accounts that have received more than 10 failed OTP attempts within any 1-hour window, and these appear in the alert banner and as "Suspicious" status rows in the table.

The Cybersecurity Officer has G1 (read-only) access to this page. They can view all records, filter, search, and export the audit log for compliance reporting (e.g., DPDP Act 2023 incident logs, cyber insurance audits) but cannot take actions such as force logout or account lock.

All data is pulled directly from PostgreSQL — no caching layer. This ensures the audit log is always current and tamper-evident.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + actions (force logout, lock account) | Primary security operator |
| Group IT Director | G4 | Full read + actions | Strategic oversight |
| Group Cybersecurity Officer | G1 | Read-only (all columns) + export | Cannot take actions; monitoring and audit only |
| Group IT Support Executive | G3 | Read-only (limited — own-branch users only) | For resolving login-related support tickets |
| Group Data Privacy Officer (Role 55, G1) | Read-only (limited columns) | DPDP Act compliance review only |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Session & Login Audit
```

### 3.2 Page Header
- **Title:** `Session & Login Audit`
- **Subtitle:** `Real-time login monitoring and security incident investigation`
- **Role Badge:** `Group IT Admin` (or `Group Cybersecurity Officer`)
- **Right-side controls:** `Export Audit Log` · `Advanced Filters`
- **Auto-refresh indicator:** "Last refreshed: [time ago] · Auto-refresh: ON (every 60s)" with toggle

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Brute-force: > 10 failed OTP attempts on any account within 1 hour | "[N] account(s) are under brute-force attack — more than 10 failed OTP attempts in 1 hour. [View Affected Accounts]" | Red (non-dismissible) |
| Concurrent sessions from different IP addresses (same account) | "[N] account(s) have concurrent active sessions from different IP addresses. [Investigate]" | Amber |
| Accounts locked due to failed attempts | "[N] account(s) have been automatically locked due to excessive failed OTP attempts." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Sessions Now | Count of currently open/active sessions (session expiry not passed) | Blue | Filtered by active sessions |
| Failed OTP Attempts (24h) | Total failed OTP attempts across all accounts in last 24 hours | Red if > 50, Amber if 10–50, Green if < 10 | Filtered by Failed status + 24h |
| Suspicious Logins (24h) | Login events flagged as Suspicious in last 24 hours | Red if > 0, Green if 0 | Filtered by Suspicious + 24h |
| Accounts Locked | Accounts currently in Locked state due to failed attempts | Red if > 0, Green if 0 | Filtered by Locked accounts |
| Unique Logins Today | Count of distinct users who successfully logged in today | Blue | Filtered by Success + today |

---

## 5. Main Table — Login & Session Events

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| User Name | Text (link opens Login Event Detail drawer) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Role | Text | Yes | No |
| Login Time | DateTime (absolute; tooltip shows relative) | Yes | Yes (date range) |
| IP Address | Text (e.g., 192.168.1.xxx — last octet partially masked for display) | No | Yes (text input) |
| Device | Badge (Mobile / Desktop / Tablet / Unknown) | No | Yes |
| Status | Badge (Success / Failed / Suspicious / Force Logged Out) | Yes | Yes (multi-select) |
| Session Duration | Text (e.g., "2h 14m" or "Ended" or "Active") | No | No |
| Actions | View Details / Force Logout / Lock Account | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All group branches |
| Role | Text search | Role/designation name |
| Status | Checkbox | Success / Failed / Suspicious / Force Logged Out |
| Date Range | Date range picker | Any range; default last 7 days |
| IP Address | Text input | Partial IP match supported |
| Device Type | Checkbox | Mobile / Desktop / Tablet / Unknown |

### 5.2 Search
- Full-text search: User Name, Username, IP Address
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page · Default sort: Login Time descending (most recent first)

---

## 6. Drawers

### 6.1 Drawer: `session-detail` — Login Event Detail
- **Trigger:** Click User Name or Actions → View Details
- **Width:** 360px
- **Content sections:**
  - **User Info:** Name, branch, role, access level, account status, link to User Directory profile
  - **This Event:** Login time, status (Success/Failed/Suspicious), IP address (full), device type, user agent string (collapsible), approximate location if detectable (country/state from IP geolocation — informational only)
  - **All Events for This User in Session Window (last 7 days):** Chronological table of all login events — timestamp, status, IP, device. Highlights the current event row.
  - **Active Sessions:** Whether user has any currently active sessions; if yes, shows all active sessions with IP, device, login time, and individual Force Logout button per session

### 6.2 Modal: Force Logout
- **Trigger:** Actions → Force Logout (only available for active sessions)
- **Type:** Centered modal (400px)
- **Content:** "Force logging out [User Name] will immediately terminate all active sessions for this user. They will need to log in again. Proceed?"
- **Field:** Reason for Force Logout (required, dropdown: Security Investigation / Suspicious Activity / Account Policy Enforcement / User Request / Other)
- **Buttons:** Confirm Force Logout (red) · Cancel
- **On confirm:** On confirm: session terminated; user notified via email (optional) that their session was terminated for security reasons; IT Admin receives audit log entry. **Audit:** Force logout logged to IT Audit Log with IT Admin user ID, timestamp, target user, and reason.

### 6.3 Modal: Lock Account
- **Trigger:** Actions → Lock Account
- **Type:** Centered modal (440px)
- **Content:** "Locking [User Name]'s account will prevent any login attempts until manually unlocked by an IT Admin. This is a more severe action than Force Logout."
- **Fields:**
  - Lock Reason (required, textarea)
  - Notify User's Branch Principal (checkbox, default checked)
  - Notify User via SMS (checkbox, default checked)
- **Buttons:** Confirm Lock (red) · Cancel

---

## 7. Charts

No dedicated chart on this page. KPI cards provide the essential security metrics. The auto-refresh KPI bar effectively functions as a live dashboard strip. Detailed trend charts are available on the IT Analytics page.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Force logout confirmed | "[User Name] has been force logged out. All active sessions terminated." | Warning | 4s |
| Account locked | "[User Name]'s account has been locked. Branch principal notified." | Warning | 5s |
| Account unlocked (from User Directory) | "[User Name]'s account has been unlocked. User can now log in." | Success | 4s |
| Export initiated | "Session audit log export is being prepared." | Info | 3s |
| Brute-force auto-lock triggered (system) | "Account [Username] has been auto-locked after 10 consecutive failed OTP attempts." | Error | 7s (persistent) |
| Force logout failed | Error: `Could not force logout [User Name]. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No events in selected date range | "No Login Events Found" | "No login events were recorded in the selected date range. Try expanding the date range." | Expand Date Range |
| No results for filters | "No Matching Events" | "No login events match the selected filters. Try adjusting branch, status, or device type." | Clear Filters |
| No active sessions | "No Active Sessions" | "No users are currently logged in across any branch." | — |
| No suspicious events | "No Suspicious Activity" | "No suspicious login events have been detected in the selected period." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 5 KPI shimmer cards + table skeleton (20 rows) |
| Auto-refresh (every 60s) | KPI bar reloads silently; table shows subtle "Refreshing…" indicator in header |
| Filter / search applied | Table skeleton; KPI bar does not reload on filter change |
| Session detail drawer open | 360px drawer skeleton; all-events section loads lazily |
| Force logout modal confirm | Button spinner; table row status badge updates to "Force Logged Out" |
| Lock account modal confirm | Button spinner; modal closes; toast appears |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Cybersecurity Officer (G1) | IT Support Executive (G3) |
|---|---|---|---|---|
| Full table (all columns) | Visible | Visible | Visible | Visible (own-branch only) |
| IP Address (full) | Visible | Visible | Visible | Hidden |
| Force Logout action | Visible | Visible | Hidden | Hidden |
| Lock Account action | Visible | Visible | Hidden | Hidden |
| Export Audit Log | Visible | Visible | Visible | Hidden |
| Alert banners | Visible | Visible | Visible | Visible |
| Auto-refresh toggle | Visible | Visible | Visible | Hidden |
| View Details action | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/sessions/` | JWT (G1+) | Paginated login event audit log with filters |
| GET | `/api/v1/it/sessions/{id}/` | JWT (G1+) | Single login event detail |
| GET | `/api/v1/it/sessions/user/{user_id}/` | JWT (G1+) | All login events for a specific user |
| POST | `/api/v1/it/sessions/{session_id}/force-logout/` | JWT (G4) | Force logout a specific session |
| POST | `/api/v1/it/users/{user_id}/lock/` | JWT (G4) | Lock user account |
| POST | `/api/v1/it/users/{user_id}/unlock/` | JWT (G4) | Unlock user account |
| GET | `/api/v1/it/sessions/kpis/` | JWT (G1+) | KPI bar values (active sessions, failed attempts, etc.) |
| GET | `/api/v1/it/sessions/export/` | JWT (G1+) | Async export of filtered audit log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/sessions/kpis/` | `#kpi-bar` | `innerHTML` |
| Auto-refresh KPI bar | `every 60s` | GET `/api/v1/it/sessions/kpis/` | `#kpi-bar` | `innerHTML` |
| Load session table | `load` | GET `/api/v1/it/sessions/` | `#session-table` | `innerHTML` |
| Auto-refresh table | `every 60s` (when toggle ON) | GET `/api/v1/it/sessions/?page=1&...` | `#session-table` | `innerHTML` |
| Search | `input` (300ms debounce) | GET `/api/v1/it/sessions/?q=...` | `#session-table` | `innerHTML` |
| Apply filters | `change` | GET `/api/v1/it/sessions/?branch=...&status=...` | `#session-table` | `innerHTML` |
| Paginate | `click` on page control | GET `/api/v1/it/sessions/?page=N` | `#session-table` | `innerHTML` |
| Open event detail drawer | `click` on User Name | GET `/api/v1/it/sessions/{id}/` | `#session-drawer` | `innerHTML` |
| Confirm force logout | `click` on Confirm | POST `/api/v1/it/sessions/{session_id}/force-logout/` | `#session-table` | `innerHTML` |
| Confirm account lock | `click` on Confirm Lock | POST `/api/v1/it/users/{user_id}/lock/` | `#session-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
