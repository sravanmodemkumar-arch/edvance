# 18 — Auth Policy Manager

- **URL:** `/group/it/users/auth-policy/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The Auth Policy Manager is the group-wide authentication and security configuration page for EduForge. Every setting on this page applies to all user accounts across all branches in the group — there are no per-branch authentication policies unless overridden at the IP Allowlist level (Section 4). This centralised model ensures consistent security posture and prevents individual branches from inadvertently weakening authentication (e.g., by setting OTP expiry to 30 minutes or disabling session timeouts).

The page covers five security domains. OTP Settings govern the nature of the one-time password: its length (4 or 6 digits), how long it remains valid before expiry, how many consecutive wrong attempts lock the account, and how long to wait before a resend is allowed. Session Policy governs what happens after successful login: how long a session can idle before the user is automatically logged out, how many concurrent sessions a single user account may maintain, and whether a role change should terminate all existing sessions. Account Lockout defines the automated lockout threshold and its duration, plus whether the IT Admin receives a notification when any account gets locked. IP Allowlist is an optional, per-branch feature: a branch can whitelist a set of IP addresses (e.g., the school's fixed internet IP), so that logins from outside that whitelist are rejected, preventing access from home networks or mobile data for sensitive admin roles. Device Trust governs whether a successfully authenticated device can be "trusted" for a period, skipping OTP on subsequent logins from the same device.

All settings are persisted in a `group_auth_policy` table in PostgreSQL (single row per group, versioned). Changes are written only after the form section is saved explicitly — there is no auto-save. Sensitive settings (session timeout, IP allowlist changes) require IT Director confirmation via an in-page approval prompt. Every change is logged to the IT Audit Log with full before/after diff.

Audit log entry includes: timestamp, section changed (OTP/Session/Lockout/IP Allowlist/Device Trust), operator name, before value, after value, IT Director approval status if applicable.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + edit (all sections) | Sensitive section changes require IT Director confirmation |
| Group IT Director | G4 | Full read + confirm sensitive changes | Also has full edit rights |
| Group Cybersecurity Officer | G1 | Read-only (all sections) | Security posture review |
| Group Data Privacy Officer | G1 | Read-only (OTP and IP Allowlist sections only) | DPDP compliance review |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → User Management → Auth Policy
```

### 3.2 Page Header
- **Title:** `Authentication & Security Policy`
- **Subtitle:** `Group-wide authentication settings · Last updated: [date] by [admin name]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `View Change History`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| OTP expiry is set to > 10 minutes | "OTP expiry is currently set to [N] minutes. Best practice is ≤ 5 minutes. Consider reducing it." | Amber |
| IP Allowlist enabled for a branch but no IPs configured | "IP Allowlist is enabled for [Branch Name] but no IP addresses have been added. Users at this branch will be unable to log in." | Red |
| Session timeout > 4 hours of inactivity | "Session timeout is set to [N] minutes. This may allow abandoned sessions to persist. Review security implications." | Amber |
| Changes pending IT Director confirmation | "[N] auth policy change(s) are awaiting IT Director confirmation before taking effect." | Amber |

---

## 4. KPI Summary Bar

This is a settings page — no KPI cards. The header subtitle provides the last-modified context. Policy sections are displayed as distinct form panels, each with its own inline status and Save button.

---

## 5. Main Table

There is no data table on this page. The layout is a single-column stack of form sections, each section clearly labelled with a section title, description, form fields, and a Save / Save & Confirm button.

---

## 6. Drawers

### 6.1 Section 1: OTP Settings

**Fields:**
- OTP Length (radio: 4 digits / 6 digits; current value highlighted)
- OTP Expiry (number input, 1–30 minutes; inline warning if > 10 min)
- Max Failed OTP Attempts Before Lockout (number input, 3–10; current: [value])
- Resend OTP Cooldown (number input, 30–300 seconds)

**Save button behaviour:** On click, shows confirmation summary "You are changing OTP settings for all [N] users group-wide. Confirm?" → inline confirm (no modal). On confirm, PATCH to policy endpoint; success toast; audit log written.

---

### 6.2 Section 2: Session Policy

**Fields:**
- Session Timeout — Inactivity (dropdown: 15 min / 30 min / 1 hour / 2 hours / 4 hours / 8 hours / Never)
- Maximum Concurrent Sessions Per User (radio: 1 / 2 / Unlimited)
- Force Logout on Role Change (toggle: Yes / No; when Yes, all user sessions are invalidated the moment their role/access level is changed by an admin)

**Sensitive field:** Session Timeout > 1 hour requires IT Director confirmation. On Save, if timeout > 1 hour: inline approval prompt rendered — "This change requires IT Director confirmation. [Notify IT Director for Approval]" button. The setting is staged but not committed until IT Director approves.

---

### 6.3 Section 3: Account Lockout Policy

**Fields:**
- Lock Account After N Failed Attempts (should match or be less than OTP Section setting; number input, 3–10)
- Lockout Duration (radio: 5 minutes / 15 minutes / 30 minutes / 1 hour / Until Manual Unlock)
- Notify IT Admin on Each Lockout (toggle: Yes / No)
- Notify Branch Principal on Account Lockout (toggle: Yes / No)

**Note displayed:** "Lockout policy works in conjunction with OTP failed attempts configured in Section 1. Both values should be consistent."

---

### 6.4 Section 4: IP Allowlist (Per-Branch Optional)

**Layout:** A table of branches with allowlist configuration per row.

| Column | Type |
|---|---|
| Branch Name | Text |
| Allowlist Enabled | Toggle (Yes / No) |
| Configured IPs | Count (e.g., "3 IPs") or "None" |
| Actions | Edit IPs |

**Edit IPs mini-drawer (360px):**
- List of current whitelisted IPs with delete (×) per row
- Add IP input (text + Add button)
- Supports CIDR notation (e.g., 203.0.113.0/24)
- Validation: must be valid IPv4/CIDR
- Save button within mini-drawer

Each IP Allowlist entry records: IP/CIDR, Branch, Status (Enabled/Disabled), Last Modified timestamp, Modified By.

**Warning shown when Allowlist enabled:** "Only users logging in from the listed IP addresses will be able to access [Branch] portal. Ensure you include all valid school IP addresses before enabling."

**This section requires IT Director confirmation before any IP Allowlist is enabled or disabled (not just modified).**

---

### 6.5 Section 5: Device Trust Settings

**Fields:**
- Enable Device Trust (toggle: Yes / No; when off, all sections below are greyed out)
- Device Trust Duration (dropdown: 7 days / 15 days / 30 days / 60 days)
- Apply To Roles (multi-select checkboxes: All Roles / G3 and above only / G4 only; lower access levels like G0/G1 student/parent accounts often should not get device trust)
- Revoke All Trusted Devices (danger button, red, with confirm modal) — clears all device trust tokens group-wide; users must re-authenticate on all devices

---

### 6.6 Drawer: `policy-history` — View Change History
- **Trigger:** `View Change History` button (top right)
- **Width:** 480px
- **Content:** Paginated table of all auth policy changes — timestamp, section changed, changed by (admin name), before value, after value, IT Director approval (if required)
- Each row expandable to show full before/after diff

---

## 7. Charts

No charts on this page. The settings form is the entirety of the interface.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| OTP settings saved | "OTP settings updated. Changes apply to all new OTP requests immediately." | Success | 4s |
| Session policy saved | "Session policy updated. Existing sessions will be affected at next activity check." | Success | 4s |
| Lockout policy saved | "Account lockout policy updated." | Success | 3s |
| IP saved (pending IT Director approval) | "IP Allowlist change staged. Awaiting IT Director confirmation before taking effect." | Info | 5s |
| IP Allowlist approved | "IP Allowlist for [Branch] is now active." | Success | 4s |
| Device trust settings saved | "Device trust settings updated." | Success | 3s |
| All trusted devices revoked | "All device trust tokens have been revoked group-wide. Users must re-authenticate on all devices." | Warning | 5s |
| Save failed (validation) | "Could not save: [specific validation error message]." | Error | 5s |
| Device token revoke failed | Error: `Could not revoke device tokens. Please try again.` | Error | 5s |
| Policy save failed (validation) | Error: `Failed to save policy. Please review required fields and try again.` | Error | 5s |

---

## 9. Empty States

Not applicable — this is a settings page that always has values (system defaults on first deployment). The IP Allowlist table will show an empty-state row if no branches have been configured yet: "No branches with IP Allowlist configured. Enable for specific branches using the Edit IPs action."

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Section skeletons: each form section shows shimmer fields while policy data loads |
| Save button click | Button spinner on the specific section's Save button only; other sections remain interactive |
| IP Allowlist mini-drawer open | 360px drawer skeleton; IP list loads |
| Policy history drawer open | Drawer skeleton; history rows load progressively |
| Revoke all devices confirm | Full-section spinner overlay: "Revoking all trusted devices…" |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Cybersecurity Officer (G1) | Data Privacy Officer (G1) |
|---|---|---|---|---|
| All five sections (read) | Visible | Visible | Visible | OTP + IP sections only |
| Edit fields in all sections | Visible | Visible | Hidden | Hidden |
| Save buttons | Visible | Visible | Hidden | Hidden |
| IT Director approval prompt | Sees "Notify IT Director" | Sees "Approve" button | Hidden | Hidden |
| IP Allowlist Edit IPs action | Visible | Visible | Hidden | Hidden |
| Revoke All Trusted Devices | Visible | Visible | Hidden | Hidden |
| Revoke All Trusted Devices button | Visible | Visible | Hidden | Hidden |
| View Change History | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/auth-policy/` | JWT (G1+) | Retrieve current group auth policy (all sections) |
| PATCH | `/api/v1/it/auth-policy/otp/` | JWT (G4) | Update OTP settings |
| PATCH | `/api/v1/it/auth-policy/session/` | JWT (G4) | Update session policy (sensitive — may need approval) |
| PATCH | `/api/v1/it/auth-policy/lockout/` | JWT (G4) | Update lockout policy |
| GET | `/api/v1/it/auth-policy/ip-allowlist/` | JWT (G1+) | Get per-branch IP allowlist config |
| PATCH | `/api/v1/it/auth-policy/ip-allowlist/{branch_id}/` | JWT (G4) | Update IP allowlist for a branch (staged) |
| POST | `/api/v1/it/auth-policy/ip-allowlist/{branch_id}/approve/` | JWT (G4 — IT Director) | Approve staged IP allowlist change |
| PATCH | `/api/v1/it/auth-policy/device-trust/` | JWT (G4) | Update device trust settings |
| POST | `/api/v1/it/auth-policy/device-trust/revoke-all/` | JWT (G4) | Revoke all trusted device tokens |
| GET | `/api/v1/it/auth-policy/history/` | JWT (G1+) | Paginated change history for all policy sections |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load all policy sections | `load` | GET `/api/v1/it/auth-policy/` | `#policy-container` | `innerHTML` |
| Load IP Allowlist table | `load` | GET `/api/v1/it/auth-policy/ip-allowlist/` | `#ip-allowlist-section` | `innerHTML` |
| Save OTP settings | `click` on Save (OTP section) | PATCH `/api/v1/it/auth-policy/otp/` | `#otp-section` | `outerHTML` |
| Save session policy | `click` on Save (session section) | PATCH `/api/v1/it/auth-policy/session/` | `#session-section` | `outerHTML` |
| Save lockout policy | `click` on Save (lockout section) | PATCH `/api/v1/it/auth-policy/lockout/` | `#lockout-section` | `outerHTML` |
| Open IP edit mini-drawer | `click` on Edit IPs | GET `/api/v1/it/auth-policy/ip-allowlist/{branch_id}/` | `#ip-mini-drawer` | `innerHTML` |
| Save device trust settings | `click` on Save (device section) | PATCH `/api/v1/it/auth-policy/device-trust/` | `#device-section` | `outerHTML` |
| Open change history drawer | `click` on View Change History | GET `/api/v1/it/auth-policy/history/` | `#policy-history-drawer` | `innerHTML` |
| Revoke all devices confirm | `click` on Confirm Revoke | POST `/api/v1/it/auth-policy/device-trust/revoke-all/` | `#device-section` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
