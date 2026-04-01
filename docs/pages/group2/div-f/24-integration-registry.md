# 24 — Integration Registry

- **URL:** `/group/it/integrations/registry/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Primary owner; Group IT Director (Role 53, G4) — Read + Test access

---

## 1. Purpose

The Integration Registry is the authoritative master list of every external system and service connected to EduForge across the group. Every API connection, third-party service, government portal, payment gateway, communication channel, and storage layer is catalogued here as a discrete integration record. This single page answers the question: "what does EduForge talk to, and is it healthy right now?"

The scope of integrations across a typical 20–50 branch group is substantial. The registry holds entries for WhatsApp Business API (for parent/student communications), SMS gateways (Textlocal, MSG91, etc.), payment gateways (Razorpay, PayU), Google OAuth (student and staff login), Microsoft Azure AD SSO, SAML-based institutional identity providers, LMS integrations (Moodle, Canvas, internal LMS), external examination platforms (NEET, JEE prep platforms), government APIs (DigiLocker for document verification, UDISE+ portal), AWS S3 and Cloudflare R2 storage, and any custom webhook-based integrations with regional or branch-specific systems.

Each integration record carries: configuration metadata (type, scope, credentials reference — not raw credentials), live health status derived from the most recent health check, latency and error rate data from the last 24 hours, version information, and full audit trail of all configuration changes. The Integration Manager uses this registry as the primary dashboard for managing the group's integration estate. The IT Director uses it for governance and risk oversight — specifically for identifying degraded or failed integrations that may be impacting branch operations.

Health status is not real-time streamed — it is pulled on page load and refreshed via manual "Test Now" per integration, or via the dedicated Health Monitor page (page 28) which auto-refreshes. The registry provides the configuration and management layer; the health monitor provides the live monitoring layer.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + write + test + disable | Primary owner; can create, edit, test, disable integrations |
| Group IT Director | G4 | Full read + test + disable | Cannot create or edit configuration details; governance oversight |
| Group IT Admin | G4 | Read-only | Can view integration list and status; no configuration access |
| Group Cybersecurity Officer (Role 56, G1) | G1 | Read-only (status and type only) | No credentials or config visible |
| Group Data Privacy Officer | G1 | Hidden | No access to this page |
| Group IT Support Executive | G3 | Hidden | No access to this page |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → Integration Registry
```

### 3.2 Page Header
- **Title:** `Integration Registry`
- **Subtitle:** `[Total Count] Integrations · [N] Active · [N] Degraded · [N] Failed · Last synced: [timestamp]`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `+ Add Integration` · `Export` · `Run All Health Checks`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any integration in Failed status | "[N] integration(s) are currently FAILED. Branch operations may be impacted. Review immediately." | Red (non-dismissible) |
| Any integration Degraded | "[N] integration(s) are Degraded. Latency or error rates elevated above threshold." | Amber |
| Any integration untested >7 days | "[N] integration(s) have not been health-checked in more than 7 days." | Amber |
| Payment gateway failing | "Payment gateway is FAILING. Fee collection may be unavailable for affected branches." | Red (non-dismissible) |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Integrations | Count of all integration records in registry | Blue | No filter |
| Active | Integrations with status = Active and last health check passed | Green | Filter by Active status |
| Degraded | Integrations with elevated latency or error rate above warning threshold | Amber | Filter by Degraded |
| Failed | Integrations where last health check returned failure or error | Red if > 0, Green if 0 | Filter by Failed |
| Untested (>7 Days) | Integrations where last health check timestamp > 7 days ago | Amber if > 0 | Filter by untested; Drill-down: Filter table by integrations where last health check > 7 days ago |

---

## 5. Main Table — Integration Registry

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Integration Name | Text (link to view drawer) | Yes | Yes (text search) |
| Type | Badge (WhatsApp / SMS / Payment / OAuth / Storage / Gov / LMS / Custom) | Yes | Yes (multi-select) |
| Scope | Text (Group-wide / Branch-specific / N Branches) | Yes | Yes (dropdown) |
| Status | Badge (Active / Degraded / Failed / Inactive) | Yes | Yes (multi-select) |
| Last Health Check | Datetime (relative: "3h ago") | Yes | Yes (date range) |
| Latency (ms) | Number — green <200ms, amber 200–500ms, red >500ms | Yes | No |
| Error Rate (24h) | Percentage — green <1%, amber 1–5%, red >5% | Yes | No |
| Version | Text (e.g., v2.1) | Yes | No |
| Actions | View / Edit / Test Now / Disable | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Type | Multi-select checkbox | WhatsApp / SMS / Payment / OAuth / Storage / Gov / LMS / Custom |
| Status | Multi-select checkbox | Active / Degraded / Failed / Inactive |
| Scope | Dropdown | Group-wide / Branch-specific / All |
| Last Health Check | Date range picker | Any range |

### 5.2 Search
- Full-text: Integration Name, type, scope
- 300ms debounce; HTMX-driven

### 5.3 Pagination
- Server-side · 25 rows/page · total count shown

---

## 6. Drawers

### 6.1 Drawer: `integration-create` — Add Integration
- **Trigger:** `+ Add Integration` button
- **Width:** 560px
- **Fields:**
  - Integration Name (required, text — e.g., "Razorpay Payment Gateway")
  - Type (required, dropdown: WhatsApp / SMS / Payment / OAuth / Storage / Gov / LMS / Custom)
  - Scope (required, radio: Group-wide / Branch-specific → multi-select branches if branch-specific)
  - Description (optional, textarea)
  - Credentials Configuration (dynamic section by type):
    - **WhatsApp:** Phone number ID, Access Token, Webhook verify token, Business Account ID
    - **SMS:** Gateway name, API key, Sender ID, DLT template IDs (textarea)
    - **Payment:** Gateway name (Razorpay/PayU/Other), Key ID, Key Secret, Webhook secret
    - **OAuth/SSO:** Provider, Client ID, Client Secret, Redirect URI, Scopes
    - **Storage:** Provider (AWS S3/Cloudflare R2), Access Key ID, Secret Key, Bucket name, Region/Account ID
    - **Gov:** API name, API endpoint, Auth token/API key, Certificate upload (if required)
    - **LMS:** LMS name, API base URL, Auth type (Bearer/Basic), Token/credentials
    - **Custom:** Endpoint URL, Auth type, Headers (key-value pairs), Request schema notes
  - Version (optional, text)
  - **Test Connection button** (inline in drawer — runs validation call before save; shows success/error inline)
- **On submit:** Saves integration record; credentials stored encrypted in PostgreSQL; integration ID generated; health check scheduled immediately

### 6.2 Drawer: `integration-view` — View Integration Detail
- **Trigger:** Integration name link or View action
- **Width:** 720px
- **Tabs:**
  - **Config:** Integration name, type, scope, version, creation date, created by, last modified by — no raw credentials shown (only masked reference IDs)
  - **Health History:** Table of last 50 health check results — timestamp, status, latency (ms), HTTP response code, error message (if any)
  - **Error Log:** Last 100 error events — timestamp, error type, error message, affected operation, resolved (yes/no)
  - **Usage Metrics:** API calls today / this week / this month (from PostgreSQL usage_log table), top 5 operations by volume, peak usage time

### 6.3 Drawer: `integration-edit` — Edit Integration
- **Trigger:** Actions → Edit
- **Width:** 560px
- Same fields as create form, pre-populated; Integration ID locked; credential fields show masked placeholders ("••••••••") with option to replace
- Test Connection button re-runs validation
- Saving re-runs health check automatically

### 6.4 Drawer: `integration-test` — Test Integration
- **Trigger:** Actions → Test Now
- **Width:** 480px
- Shows: Integration name, type, last test result
- **Test button:** Triggers a live connectivity and authentication validation call to the external service
- Result shown inline in drawer:
  - Success: green banner, response time in ms, "Integration is reachable and authenticated."
  - Failure: red banner, error code, error message, suggested resolution steps (per integration type)
- Test result saved to health_check_log table; Last Health Check timestamp updated

### 6.5 Modal: Disable Integration
- **Trigger:** Actions → Disable
- Confirmation: "Disabling [Integration Name] will stop all EduForge operations that depend on this integration. Affected branches: [list]. Are you sure?"
- Text input: Reason for disabling (required)
- Buttons: Confirm Disable · Cancel
- On confirm: status set to Inactive; audit log entry created; IT Director notified via in-app notification

---

## 7. Charts

### 7.1 Integration Health Overview (Donut Chart)
- Segments: Active / Degraded / Failed / Inactive
- Positioned in the page header area as a compact inline chart
- Click segment filters main table by that status

### 7.2 Error Rate by Integration (Bar Chart)
- X-axis: Integration names (abbreviated)
- Y-axis: Error rate % (24h)
- Colour: green <1%, amber 1–5%, red >5%
- Shows at a glance which integrations have highest error burden

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Integration created | "Integration '[Name]' added. Health check scheduled." | Success | 4s |
| Integration updated | "Integration '[Name]' configuration updated." | Success | 3s |
| Test passed | "Health check passed for '[Name]'. Latency: [N]ms." | Success | 4s |
| Test failed | "Health check FAILED for '[Name]'. Error: [message]. Check error log." | Error | 6s |
| Integration test passed (elevated latency) | Warning: `Health check passed but latency is elevated ([N]ms). Monitor closely.` | Warning | 4s |
| Integration disabled | "Integration '[Name]' has been disabled. IT Director notified." | Warning | 5s |
| Run all checks triggered | "Running health checks for all [N] integrations. Results will update in a few minutes." | Info | 5s |
| Export triggered | "Integration registry export is being prepared." | Info | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No integrations | "No Integrations Registered" | "Add your first integration to begin tracking external services connected to EduForge." | + Add Integration |
| No results for filter | "No Matching Integrations" | "No integrations match the selected filters. Adjust or clear your filters." | Clear Filters |
| All integrations healthy | "All Integrations Healthy" | "Every registered integration is active with normal latency and error rates." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 5 KPI shimmer cards + table skeleton (15 rows) |
| Filter / search applied | Table rows shimmer (3-row skeleton) while query runs |
| View integration drawer | Drawer spinner; tabs load progressively; Health History tab lazy-loads |
| Test Now drawer | Spinner with label "Running health check…" while test executes (up to 10s timeout) |
| Run All Health Checks | Top of page progress indicator: "Checking [N] of [Total]…" |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | IT Admin (G4) | Cybersecurity Officer (G1) |
|---|---|---|---|---|
| + Add Integration | Visible | Hidden | Hidden | Hidden |
| Edit Action | Visible | Hidden | Hidden | Hidden |
| Disable Action | Visible | Visible | Hidden | Hidden |
| Test Now Action | Visible | Visible | Hidden | Hidden |
| Credentials in Config Tab | Masked references visible | Hidden | Hidden | Hidden |
| Error Log Tab | Visible | Visible | Visible | Hidden |
| Usage Metrics Tab | Visible | Visible | Hidden | Hidden |
| Export | Visible | Visible | Hidden | Hidden |
| Run All Health Checks | Visible | Visible | Hidden | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/integrations/` | JWT (G4+) | Paginated integration registry with role-scoped fields |
| POST | `/api/v1/it/integrations/` | JWT (G4 — Integration Manager) | Create new integration record |
| GET | `/api/v1/it/integrations/{id}/` | JWT (G4+) | Full integration detail (config, health, errors, usage) |
| PATCH | `/api/v1/it/integrations/{id}/` | JWT (G4 — Integration Manager) | Update integration configuration |
| POST | `/api/v1/it/integrations/{id}/test/` | JWT (G4) | Run live health check for integration |
| POST | `/api/v1/it/integrations/{id}/disable/` | JWT (G4) | Disable integration with reason |
| POST | `/api/v1/it/integrations/test-all/` | JWT (G4) | Trigger health check run for all integrations |
| GET | `/api/v1/it/integrations/kpis/` | JWT (G4+) | KPI card values |
| GET | `/api/v1/it/integrations/{id}/health-history/` | JWT (G4+) | Last 50 health check results |
| GET | `/api/v1/it/integrations/{id}/error-log/` | JWT (G4+) | Last 100 error events |
| GET | `/api/v1/it/integrations/{id}/usage-metrics/` | JWT (G4) | Usage counts by day/week/month |
| GET | `/api/v1/it/integrations/export/` | JWT (G4) | Export integration registry |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/integrations/kpis/` | `#kpi-bar` | `innerHTML` |
| Load integrations table | `load` | GET `/api/v1/it/integrations/` | `#integrations-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/integrations/?type=...&status=...` | `#integrations-table` | `innerHTML` |
| Search integrations | `input` (300ms debounce) | GET `/api/v1/it/integrations/?q=...` | `#integrations-table` | `innerHTML` |
| Open view drawer | `click` on integration name | GET `/api/v1/it/integrations/{id}/` | `#integration-drawer` | `innerHTML` |
| Load Health History tab | `click` on tab | GET `/api/v1/it/integrations/{id}/health-history/` | `#tab-content` | `innerHTML` |
| Load Error Log tab | `click` on tab | GET `/api/v1/it/integrations/{id}/error-log/` | `#tab-content` | `innerHTML` |
| Load usage metrics tab | `click` on Usage Metrics tab | GET `/api/v1/it/integrations/{id}/usage/` | `#usage-tab-content` | `innerHTML` |
| Run Test Now | `click` on Test button in drawer | POST `/api/v1/it/integrations/{id}/test/` | `#test-result` | `innerHTML` |
| Submit Create form | `click` on Submit | POST `/api/v1/it/integrations/` | `#integrations-table` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/integrations/?page=N` | `#integrations-table` | `innerHTML` |
| Confirm Disable | `click` on Confirm Disable | POST `/api/v1/it/integrations/{id}/disable/` | `#integrations-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Integration status changes to Failed: IT Admin + Integration Manager (in-app red + email) immediately
- Integration untested > 7 days: Integration Manager (in-app amber + email)
- Health check timeout: Integration Manager (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
