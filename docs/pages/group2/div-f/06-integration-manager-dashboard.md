# 06 — Group EduForge Integration Manager Dashboard

- **URL:** `/group/it/integrations/manager/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group EduForge Integration Manager (Role 58, G4)

---

## 1. Purpose

The Group EduForge Integration Manager Dashboard is the command centre for all technical integrations that connect EduForge to external systems — SSO identity providers, third-party APIs, inbound/outbound webhooks, and custom domain configurations. It is also the page where the Integration Manager monitors overall integration health and responds to failures before they impact branch operations.

EduForge integrations fall into four main categories: SSO (Single Sign-On using SAML 2.0 or OAuth 2.0 for staff and student login), API integrations (third-party tools that call EduForge APIs or EduForge calling external APIs — e.g., payment gateways, SMS providers), Webhooks (event-driven notifications from EduForge to external systems — e.g., exam result webhooks to parent apps), and Domain integrations (custom domain DNS verification and SSL certificate management). All four types are surfaced in the Integration Registry table.

The Integration Manager is the only role authorised to create or modify SSO configurations, rotate API keys, and verify custom domains. This authority is intentional — misconfigured SSO or incorrect API credentials can lock users out of branch portals entirely or expose sensitive data. Changes made on this page are logged to the IT Audit Log with the Integration Manager's user ID and timestamp.

The webhook delivery rate KPI is a leading indicator of integration health. A drop in delivery rate below 95% typically precedes branch staff reporting that parent notifications are not being sent, or that exam results are not appearing in third-party apps. Monitoring this proactively allows the Integration Manager to diagnose and fix delivery failures before branch complaints are raised.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + create/edit/test/delete integrations | Primary role |
| Group IT Admin | G4 | Full read + edit non-SSO integrations | Cannot create or delete SSO configs |
| Group IT Director | G4 | Full read (review only) | Cannot modify integrations directly |
| Group IT Support Executive | G3 | Read-only (health status only) | Cannot access config or keys |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integration Manager Dashboard
```

### 3.2 Page Header
- **Title:** `EduForge Integration Manager Dashboard`
- **Subtitle:** `Integration Health — [Active Integrations] active integrations · [SSO-Enabled Branches] SSO-enabled branches`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `+ Add Integration` · `Rotate Expiring Keys ([count])` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any integration with Status = Failed | "Integration failure: [Integration Name] ([Type]) is currently failing. Branch operations may be impacted." | Red (non-dismissible) |
| API key expiring within 7 days | "API key for [Integration Name] expires in [N] days. Rotate key before expiry to avoid service interruption." | Amber |
| Webhook delivery rate drops below 90% | "Webhook delivery rate has dropped to [N]%. Check delivery error log." | Amber |
| SSL certificate on custom domain expiring < 14 days | "SSL certificate for [Domain] expires in [N] days. Renew before expiry." | Amber |
| SSO configuration broken at any branch | "SSO is broken for [Branch Name]. Users cannot log in via SSO. Immediate fix required." | Red (non-dismissible) |

**Critical Notification Rules:**
- Integration status = Failed: Integration Manager (in-app red non-dismissible + email + WhatsApp) + IT Director (email)
- API key expiring < 7 days: Integration Manager (in-app amber + email) at 7 days, 1 day, and expiry
- Webhook delivery rate < 90%: Integration Manager (in-app amber) + IT Admin (email)
- SSO broken: Integration Manager (in-app red non-dismissible + email + WhatsApp) + IT Director (in-app + email) + affected Branch Principal (email)

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Integrations | Total count of integrations with Status = Active | Blue (informational) | No drill-down |
| SSO-Enabled Branches | Count of branches with an active SSO configuration | Blue (informational) | Filters table to SSO type |
| API Keys Active | Count of active (non-expired) API keys across all integrations | Green = all active, Amber if any expiring < 30 days, Red if any expired | Filters table to API type |
| Webhook Delivery Rate % | Average delivery success rate across all webhooks in last 24 hours | Green ≥ 98%, Amber 90–97%, Red < 90% | Filters table to Webhook type |
| Integration Failures (24h) | Count of integrations that recorded at least one failure in the last 24 hours | Green = 0, Amber 1–2, Red ≥ 3 | Filters table to failed/degraded |
| Custom Domains Verified | Count of custom domains with DNS Verification Status = Verified | Green if all verified, Amber if any pending, Red if any failed | Links to Domain Manager (`/group/it/portals/domains/`) |

---

## 5. Main Table — Integration Registry

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Integration Name | Text (link to integration detail drawer) | Yes | No |
| Type | Badge: SSO (purple) / API (blue) / Webhook (teal) / Domain (grey) | No | Yes (checkbox group) |
| Branch (or Group-wide) | Text: branch name or "Group-wide" badge | Yes | Yes (multi-select) |
| Status | Badge: Active (green) / Degraded (amber) / Failed (red) / Inactive (grey) | Yes | Yes (checkbox group) |
| Last Health Check | Relative datetime (e.g., "5 min ago") | Yes | No |
| Error Count (24h) | Integer (0 shown as green dash, > 0 shown as red count) | Yes | Yes (> 0) |
| Actions | `View` · `Edit` · `Test` · `Rotate Key` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Integration Type | Checkbox group | SSO / API / Webhook / Domain |
| Status | Checkbox group | Active / Degraded / Failed / Inactive |
| Branch | Multi-select dropdown | All branches + Group-wide option |
| Error Count Above | Numeric input | Integer threshold |
| Last Health Check | Date range picker | From / To |

### 5.2 Search
- Full-text: Integration name, branch name
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 25 rows/page · Shows total count

---

## 6. Drawers

### 6.1 Drawer: `integration-detail` — Integration Detail
- **Trigger:** Actions → View or click Integration Name
- **Width:** 560px
- **Tabs within drawer:**
  - **Config:** Integration type-specific fields (for SSO: entity ID, ACS URL, IdP metadata URL, attribute mappings; for API: base URL, auth method, rate limits, last successful call; for Webhook: endpoint URL, event triggers, secret key (masked), retry policy; for Domain: domain name, CNAME record, DNS status, SSL cert details)
  - **Health Log:** Table of the last 50 health check results — timestamp, status (Pass/Fail), response time (ms), HTTP status code
  - **Error Log:** Table of the last 50 errors — timestamp, error type, error message (truncated with "Show full" toggle), HTTP status code if applicable

### 6.2 Drawer: `integration-edit` — Edit Integration
- **Trigger:** Actions → Edit
- **Width:** 560px
- **Content:** Same fields as Config tab in detail drawer, but all fields are editable. Save Changes button (HTMX PATCH). Validation errors shown inline. Warning banner at top: "Changes to active integrations will take effect immediately and may impact logged-in users."

**Audit:** Integration configuration edits logged to IT Audit Log with Integration Manager user ID and timestamp.

### 6.3 Drawer: `integration-create` — Add Integration
- **Trigger:** `+ Add Integration` button in header
- **Width:** 560px
- **Step 1:** Select Integration Type (SSO / API / Webhook / Domain) — radio buttons
- **Step 2 (conditional on type selection):** Type-specific configuration form rendered via HTMX GET of form template
- **Step 3:** Select Branch (multi-select for group-wide or specific branches)
- **Submit:** POST creates integration in draft state; triggers automated health check; Status updates to Active if health check passes

**Audit:** New integration creation logged to IT Audit Log.

### 6.4 Modal: `rotate-key` — Rotate API Key
- **Trigger:** Actions → Rotate Key
- **Width:** 400px
- **Content:** Integration name, current key age, warning "Rotating the key will invalidate the current key immediately. You must update the external system with the new key before rotating.", Confirm Rotate button
- **On confirm:** New key generated and displayed once (copy button). User must acknowledge they have copied the key before the modal closes.

**Audit:** API key rotations logged to IT Audit Log (key values not stored in log).

### 6.5 Modal: `integration-delete-confirm` — Delete Integration

Triggered by `Delete` button in Actions column (Integration Manager + IT Director only). Width: 400px.

**Content:**
- Integration name and type (read-only)
- Warning: `Deleting this integration will immediately stop all active connections. Branches using this integration may lose functionality. This action cannot be undone.`
- Affected branches count (if applicable)
- Confirm Delete checkbox: `I confirm I want to delete this integration`

**Footer:** `Confirm Delete` (red button) / `Cancel`

**On submit:** `hx-delete="/api/v1/it/integrations/{id}/"` — integration removed; affected branches notified. Logged to IT Audit Log.

---

## 7. Charts

### 7.1 Integration Health Over 7 Days — Heatmap
- **Rows:** Each active integration (integration name on y-axis)
- **Columns:** Last 7 days (daily, with hours as sub-columns for finer granularity)
- **Cell colour:** Green = all health checks passed / Amber = some failures / Red = majority failures / Grey = no checks run
- **Purpose:** Quickly identifies integrations with recurring failure patterns vs. one-off incidents
- **Data source:** GET `/api/v1/it/integrations/charts/health-heatmap/`

### 7.2 Webhook Delivery Success Rate Trend (Line Chart)
- **X-axis:** Last 30 days (daily)
- **Y-axis:** Delivery success rate %
- **Series:** Group-wide average (blue) + individual webhook lines for webhooks with < 98% rate (red dashed) — others hidden by default, toggleable
- **Threshold line:** 98% SLA target as dashed green line
- **Data source:** GET `/api/v1/it/integrations/charts/webhook-delivery/`

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Integration created (health check passed) | "Integration created and activated. Health check passed." | Success | 4s |
| Integration created (health check failed) | "Integration created but health check failed. Review config and re-test." | Warning | 6s |
| Integration updated | "Integration [Name] configuration updated." | Success | 4s |
| API key rotated | "API key rotated successfully. Remember to update the external system." | Success | 5s |
| Health check triggered (manual test) | "Health check running for [Integration Name]…" | Info | 3s (then auto-refresh) |
| Health check result: pass | "Health check passed. Integration is operational." | Success | 4s |
| Health check result: fail | "Health check failed. Error: [Error Type]. View error log for details." | Error | 7s |
| Integration deleted | "Integration [Name] has been removed." | Info | 4s |
| Integration delete error | Error: `Failed to delete integration. Please try again.` | Error | 6s |
| API key rotation error | Error: `Failed to rotate API key. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No integrations configured | "No Integrations Yet" | "No EduForge integrations are configured for the group. Add your first integration to enable SSO, API connections, or webhooks." | + Add Integration |
| All integrations active | "All Integrations Healthy" | "Every configured integration is active and passing health checks. No action required." | View Health Logs |
| Search/filter returns no results | "No Integrations Match" | "No integrations match your search or filter criteria. Try adjusting your filters." | Clear Filters |
| No failed integrations | "No Failures in 24h" | "No integration failures have been recorded in the last 24 hours." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (6 cards) + table skeleton (8 rows) + chart shimmer |
| Integration detail drawer open | Drawer spinner; tabs load individually on click |
| Health log tab load | Tab-scoped inline spinner |
| Error log tab load | Tab-scoped inline spinner |
| Health check test running | Row status cell shows animated "Testing…" badge; action buttons disabled |
| API key rotation | Confirm button spinner + disabled state |
| Integration create — step 2 form load | Drawer content shimmer while type-specific form renders |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| KPI Summary Bar | All 6 cards | All 6 cards | All 6 cards | Active Integrations + Failures only |
| Integration Registry Table | Visible + all Actions | Visible + Edit (non-SSO), View, Test | Visible (View only) | Visible (Status column only, no Actions) |
| + Add Integration Button | Visible | Hidden | Hidden | Hidden |
| Edit SSO Integration | Visible | Hidden | Hidden | Hidden |
| Rotate API Key | Visible | Visible (non-SSO keys) | Hidden | Hidden |
| Delete Integration | Visible | Hidden | Hidden | Hidden |
| Alert Banners | All banners | All banners | All banners | Failure banners only |
| Charts | Both charts | Both charts | Both charts | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/integrations/kpis/` | JWT (G4) | Returns all 6 KPI card values |
| GET | `/api/v1/it/integrations/` | JWT (G4) | Paginated integration registry table |
| POST | `/api/v1/it/integrations/` | JWT (G4) | Create a new integration |
| GET | `/api/v1/it/integrations/{id}/` | JWT (G4) | Full integration detail for drawer |
| PATCH | `/api/v1/it/integrations/{id}/` | JWT (G4) | Edit integration configuration |
| DELETE | `/api/v1/it/integrations/{id}/` | JWT (G4) | Remove an integration |
| POST | `/api/v1/it/integrations/{id}/test/` | JWT (G4) | Trigger a manual health check |
| POST | `/api/v1/it/integrations/{id}/rotate-key/` | JWT (G4) | Rotate API key for an integration |
| GET | `/api/v1/it/integrations/{id}/health-log/` | JWT (G4) | Health check history for detail drawer |
| GET | `/api/v1/it/integrations/{id}/error-log/` | JWT (G4) | Error log history for detail drawer |
| GET | `/api/v1/it/integrations/charts/health-heatmap/` | JWT (G4) | 7-day integration health heatmap data |
| GET | `/api/v1/it/integrations/charts/webhook-delivery/` | JWT (G4) | 30-day webhook delivery success rate data |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/integrations/kpis/` | `#kpi-bar` | `innerHTML` |
| Load integration table | `load` | GET `/api/v1/it/integrations/` | `#integration-table` | `innerHTML` |
| Open integration detail drawer | `click` on Integration Name or View | GET `/api/v1/it/integrations/{id}/` | `#detail-drawer` | `innerHTML` |
| Load Health Log tab | `click` on Health Log tab | GET `/api/v1/it/integrations/{id}/health-log/` | `#drawer-tab-content` | `innerHTML` |
| Load Error Log tab | `click` on Error Log tab | GET `/api/v1/it/integrations/{id}/error-log/` | `#drawer-tab-content` | `innerHTML` |
| Open edit drawer | `click` on Edit | GET `/api/v1/it/integrations/{id}/edit-form/` | `#edit-drawer` | `innerHTML` |
| Save integration edit | `click` on Save Changes | PATCH `/api/v1/it/integrations/{id}/` | `#edit-result` | `innerHTML` |
| Select integration type (create flow) | `change` on type radio | GET `/api/v1/it/integrations/form/?type=SSO` | `#create-form-step2` | `innerHTML` |
| Trigger health check test | `click` on Test | POST `/api/v1/it/integrations/{id}/test/` | `#integration-row-{id}` | `outerHTML` |
| Filter table | `change` on filter controls | GET `/api/v1/it/integrations/?type=SSO&status=failed` | `#integration-table` | `innerHTML` |
| Search integrations | `keyup[debounce:300ms]` on search | GET `/api/v1/it/integrations/?search=` | `#integration-table` | `innerHTML` |
| Paginate | `click` on page button | GET `/api/v1/it/integrations/?page=N` | `#integration-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
