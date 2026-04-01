# 25 — SSO Configuration

- **URL:** `/group/it/integrations/sso/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Full access

---

## 1. Purpose

The SSO Configuration page enables the Integration Manager to set up Single Sign-On for branch portals across the group. By default, EduForge users (students, staff, parents) authenticate via mobile OTP. SSO allows branch users to instead authenticate using their institutional identity provider — Google Workspace (for branches that use Google for Education), Microsoft Azure AD (for Microsoft-affiliated institutions), or a custom SAML 2.0 identity provider for institutions with their own identity management infrastructure.

When SSO is configured for a branch, eligible users (typically staff and optionally students) can click "Sign in with Google / Microsoft / Institution" on the branch login page and authenticate through their institutional account rather than receiving an OTP. This reduces friction for daily active users, centralises access revocation (when a staff member's Google Workspace account is deprovisioned, they immediately lose EduForge access), and satisfies institutional IT policy requirements at many schools and colleges that mandate centralised identity management.

The Integration Manager is responsible for the full lifecycle: obtaining client credentials from the institution's IT team, entering them in this page, running a dry-run test authentication, and then enabling SSO for the branch. This page also monitors SSO health — certificate expiry, failed authentication rate, and usage adoption (SSO vs OTP ratio). Branches with SSO enabled but zero SSO logins in 30 days are flagged as potentially misconfigured.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + write + configure + test + enable/disable | Sole operator of this page |
| Group IT Director | G4 | Read-only | Can view SSO status per branch; no configuration access |
| Group IT Admin (Role 54, G4) | Read-only | Can view SSO config; cannot edit |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → SSO Configuration
```

### 3.2 Page Header
- **Title:** `SSO Configuration`
- **Subtitle:** `[N] Branches with SSO Enabled · [N] Pending Configuration · [N] Disabled`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `Configure SSO for New Branch` button

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| SSO certificate expiring <30 days (any branch) | "SSO certificate for [Branch Name] expires in [N] days. Renew before expiry to avoid authentication failures." | Amber |
| SSO certificate expiring <7 days | "URGENT: SSO certificate for [Branch Name] expires in [N] days. Immediate renewal required." | Red |
| SSO failing for active branch (auth errors >10% in last hour) | "SSO authentication failures detected for [Branch Name]. [N]% of SSO login attempts failing in the last hour." | Red (non-dismissible) |
| Branch SSO enabled but zero SSO logins in 30 days | "SSO enabled for [Branch Name] but no SSO logins recorded in 30 days. Verify configuration or disable if not in use." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Branches | Total branch count across the group | Blue | No filter |
| SSO Enabled | Branches with SSO Status = Enabled and at least one successful SSO login | Green | Filter by Enabled |
| Pending Configuration | Branches with SSO Status = Pending Config | Amber | Filter by Pending |
| SSO Disabled | Branches where SSO was previously configured but is currently Disabled | Grey | Filter by Disabled |
| No SSO (OTP Only) | Branches with SSO Type = None | Blue | Filter by None; Drill-down: Filter table by Status = OTP Only |

---

## 5. Main Table — SSO Configuration by Branch

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text (link to configure drawer) | Yes | Yes (text search) |
| SSO Type | Badge (Google / Microsoft / SAML / None) | Yes | Yes (multi-select) |
| SSO Status | Badge (Enabled / Disabled / Pending Config) | Yes | Yes (multi-select) |
| IdP Name | Text (identity provider name, e.g., "BranchX Google Workspace") | Yes | No |
| SP Entity ID | Text (auto-generated EduForge SP entity ID, truncated with copy button) | No | No |
| Last Tested | Datetime (relative) | Yes | Yes (date range) |
| Users Using SSO | Number (count of users who logged in via SSO in last 30 days) | Yes | No |
| Actions | Configure / Test / Enable / Disable | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| SSO Type | Multi-select checkbox | Google / Microsoft / SAML / None |
| SSO Status | Multi-select checkbox | Enabled / Disabled / Pending Config |

### 5.2 Search
- Full-text: Branch name, IdP name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `sso-configure` — Configure SSO for Branch
- **Trigger:** `Configure SSO for New Branch` button, or Actions → Configure
- **Width:** 560px
- **Step 1 — Branch & Type Selection:**
  - Branch (dropdown; pre-filtered to branches without existing SSO configuration if new)
  - SSO Type (radio: Google Workspace / Microsoft Azure AD / Custom SAML 2.0)
- **Step 2 — Dynamic Configuration Form (by SSO Type):**

  **Google Workspace:**
  - Google OAuth Client ID (required, text)
  - Google OAuth Client Secret (required, password input — stored encrypted)
  - Allowed Domain (required, text — e.g., `branchname.edu.in`; restricts login to this domain)
  - Redirect URI (auto-populated, read-only — "https://[branch-slug].eduforge.in/auth/callback/google/")
  - Scope: `openid email profile` (fixed, informational)

  **Microsoft Azure AD:**
  - Azure Tenant ID (required, text)
  - Azure Client ID (required, text)
  - Azure Client Secret (required, password input — stored encrypted)
  - Allowed Tenant Domain (required, text — e.g., `branchname.edu.in`)
  - Redirect URI (auto-populated, read-only)

  **Custom SAML 2.0:**
  - SP Entity ID (auto-generated, read-only — displayed with copy button)
  - ACS URL (auto-generated, read-only — Assertion Consumer Service URL, displayed with copy button)
  - Metadata URL OR Metadata XML Upload (radio toggle — enter IdP metadata URL or upload XML file)
  - Name ID Format (dropdown: `emailAddress` / `persistent` / `transient`)
  - Attribute Mapping: email attribute name, first name attribute, last name attribute (text inputs with defaults)
  - Certificate Upload (optional — upload IdP signing certificate if not in metadata)
  - Certificate Expiry Date (auto-parsed from uploaded cert; shown as read-only after parse)

- **Test SSO Button:** Triggers a dry-run authentication flow. Opens a popup window to complete the IdP auth flow. On return, reports success (green banner: "SSO test successful. Authentication flow completed for test user.") or failure (red banner with error detail).
- **Enable Only After Test:** The "Enable SSO" button is disabled until test has been run and passed at least once. Shows tooltip: "Run a successful SSO test before enabling."
- **On enable:** SSO status set to Enabled; branch login page updated to show SSO option; IT Director notified.

### 6.2 Drawer: `sso-test` — Test SSO Configuration
- **Trigger:** Actions → Test
- **Width:** 480px
- Shows: Branch name, SSO type, last test result and timestamp
- **Run Test button:** Initiates dry-run; shows spinner "Initiating SSO test flow…"
- Inline result after test:
  - Pass: Green banner, response time, IdP name, test user email returned
  - Fail: Red banner, error code, step at which failure occurred (e.g., "Failed at token exchange"), suggested fix

### 6.3 Modal: Enable SSO
- Confirmation: "Enabling SSO for [Branch Name] will add a '[SSO Type] Sign In' option to their portal login page. Users can choose OTP or SSO. OTP remains available as fallback. Confirm?"
- Buttons: Confirm Enable · Cancel

### 6.4 Modal: Disable SSO
- Confirmation: "Disabling SSO for [Branch Name] will remove the SSO login option from their portal. All users will revert to OTP login. Active SSO sessions will be terminated at next token expiry. Confirm?"
- Text input: Reason for disabling (required)
- Buttons: Confirm Disable · Cancel

---

## 7. Charts

### 7.1 SSO Login vs OTP Login Ratio per Branch (Grouped Bar Chart)
- X-axis: Branch names (horizontal scroll if >10 branches)
- Y-axis: Login count (last 30 days)
- Two bars per branch: SSO logins (blue) vs OTP logins (grey)
- Shows SSO adoption rate across the group
- Hover tooltip: exact counts and SSO adoption percentage
- Positioned below the main table
- Only branches with SSO enabled appear; branches with None type shown as 100% OTP

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| SSO configuration saved | "SSO configuration saved for [Branch Name]. Run a test before enabling." | Success | 4s |
| SSO test passed | "SSO test passed for [Branch Name]. You can now enable SSO." | Success | 4s |
| SSO test failed | "SSO test failed for [Branch Name]. Check configuration and IdP settings." | Error | 6s |
| SSO enabled | "SSO enabled for [Branch Name]. Login page updated." | Success | 4s |
| SSO disabled | "SSO disabled for [Branch Name]. Branch will use OTP login." | Warning | 4s |
| Configuration updated | "SSO configuration updated for [Branch Name]. Re-test recommended." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No branches in table | "No Branches Found" | "No branches have been configured in the system." | — |
| All branches showing None | "No SSO Configured" | "No branches have SSO configured. Set up SSO for branches using Google Workspace or Microsoft Azure AD." | Configure SSO for New Branch |
| No results for filter | "No Matching Branches" | "No branches match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 5 KPI shimmer cards + table skeleton (10 rows) |
| Filter / search | Table skeleton shimmer |
| Configure drawer open | Drawer spinner; form loads after branch list fetched |
| Test SSO (dry-run) | Spinner in drawer: "Initiating SSO test flow…" (can take 5–15s) |
| Enable/Disable modal confirm | Button spinner while API call executes |
| Chart load | Chart area shimmer with placeholder axes |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | IT Admin (G4) |
|---|---|---|---|
| Configure SSO Button | Visible | Hidden | Hidden |
| Configure Action | Visible | Hidden | Hidden |
| Test Action | Visible | Hidden | Hidden |
| Enable / Disable Actions | Visible | Hidden | Hidden |
| Client Secret Fields | Editable (masked) | Hidden entirely | Hidden entirely |
| SP Entity ID / ACS URL (copy) | Visible | Visible | Visible |
| SSO Test Results | Visible | Visible (read-only history) | Visible (read-only) |
| Adoption Chart | Visible | Visible | Hidden |
| Export | Visible | Visible | Hidden |

> Roles 55 (DPO), 56 (Cybersecurity Officer), and 57 (IT Support Executive) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/sso/` | JWT (G4) | Paginated SSO configuration list per branch |
| POST | `/api/v1/it/sso/` | JWT (G4 — Integration Manager) | Create SSO configuration for a branch |
| GET | `/api/v1/it/sso/{id}/` | JWT (G4) | Full SSO config detail (credentials masked) |
| PATCH | `/api/v1/it/sso/{id}/` | JWT (G4 — Integration Manager) | Update SSO configuration |
| POST | `/api/v1/it/sso/{id}/test/` | JWT (G4 — Integration Manager) | Trigger dry-run SSO test |
| POST | `/api/v1/it/sso/{id}/enable/` | JWT (G4 — Integration Manager) | Enable SSO for branch |
| POST | `/api/v1/it/sso/{id}/disable/` | JWT (G4 — Integration Manager) | Disable SSO with reason |
| GET | `/api/v1/it/sso/kpis/` | JWT (G4) | KPI card values |
| GET | `/api/v1/it/sso/charts/adoption/` | JWT (G4) | SSO vs OTP login ratio chart data per branch |
| GET | `/api/v1/it/sso/{id}/test-history/` | JWT (G4) | Last 20 SSO test results for a branch |
| GET | `/api/v1/it/sso/form-fields/?type={type}` | JWT (G4) | Dynamic form fields for SSO type selection |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/sso/kpis/` | `#kpi-bar` | `innerHTML` |
| Load SSO table | `load` | GET `/api/v1/it/sso/` | `#sso-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/sso/?type=...&status=...` | `#sso-table` | `innerHTML` |
| Search branches | `input` (300ms debounce) | GET `/api/v1/it/sso/?q=...` | `#sso-table` | `innerHTML` |
| Open configure drawer | `click` on Configure | GET `/api/v1/it/sso/{id}/` | `#sso-drawer` | `innerHTML` |
| SSO type radio change | `change` on SSO type radio | GET `/api/v1/it/sso/form-fields/?type={type}` | `#sso-config-fields` | `innerHTML` |
| Run SSO test | `click` on Test button | POST `/api/v1/it/sso/{id}/test/` | `#test-result-panel` | `innerHTML` |
| Submit configuration | `click` on Save | POST/PATCH `/api/v1/it/sso/` | `#sso-table` | `innerHTML` |
| Confirm Enable | `click` on Confirm Enable | POST `/api/v1/it/sso/{id}/enable/` | `#sso-table` | `innerHTML` |
| Confirm Disable | `click` on Confirm Disable | POST `/api/v1/it/sso/{id}/disable/` | `#sso-table` | `innerHTML` |
| Load adoption chart | `load` | GET `/api/v1/it/sso/charts/adoption/` | `#adoption-chart` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/sso/?page=N` | `#sso-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- SSO configuration broken (test fails after previously passing): Integration Manager + IT Director (in-app red non-dismissible + email + WhatsApp) immediately + affected Branch Principal (email)
- SSO certificate expiry < 30 days: Integration Manager (in-app amber + email) daily
- Zero SSO authentications for > 7 days (for enabled branches): Integration Manager (in-app amber)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
