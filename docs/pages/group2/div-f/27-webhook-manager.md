# 27 — Webhook Manager

- **URL:** `/group/it/integrations/webhooks/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Full access

---

## 1. Purpose

The Webhook Manager handles both directions of event-driven communication between EduForge and the external world. Outbound webhooks allow EduForge to push real-time event notifications to external systems — when a fee payment is received, a payment gateway reconciliation system should know immediately; when an exam result is published, an integrated LMS may need to update a student's record; when an admission is confirmed, a CRM might need to trigger a welcome workflow. Rather than requiring external systems to poll EduForge APIs, webhooks push the data at the moment the event occurs.

Inbound endpoints are the mirror image: external systems can push events into EduForge via defined endpoint slugs. Payment gateway webhooks arrive inbound to confirm payment capture. Government API callbacks (DigiLocker verification results) arrive inbound. Third-party exam platform results are pushed inbound after result publication.

The Integration Manager configures both sides. For outbound webhooks, they define: which event triggers the webhook, what the target URL is, what secret key is used to sign the payload (HMAC-SHA256), which branches' events are included in scope, and the retry policy (exponential backoff, max attempts). For inbound endpoints, they define: the endpoint path slug, what source system is expected, what events it should carry, and how the payload is verified (HMAC signature validation, Basic Auth, or no verification).

The delivery log is critical for debugging: every webhook delivery attempt is logged with the full response from the receiving server. When a delivery fails, the retry queue picks it up. The Integration Manager can see exactly which deliveries failed, the HTTP response code returned, and trigger a manual retry.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + write + test + enable/disable | Sole operator of this page |
| Group IT Director | G4 | Read-only | Can view outbound and inbound webhook status; no configuration |
| Group Cybersecurity Officer | G1 | Read-only (endpoint paths and verification method only) | Security audit; no secrets or delivery log content visible |
| Group IT Admin (Role 54, G4) | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → Webhook Manager
```

### 3.2 Page Header
- **Title:** `Webhook Manager`
- **Subtitle:** `[N] Outbound Webhooks · [N] Inbound Endpoints`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** Tab-contextual: `+ Create Outbound Webhook` (on Outbound tab) or `+ Create Inbound Endpoint` (on Inbound tab)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Outbound webhook delivery failure rate >20% in last hour | "Webhook '[Name]' is failing — [N]% of deliveries failing in the last hour. Check target URL availability." | Red |
| Inbound endpoint receiving unexpected payload format | "Inbound endpoint '[Name]' received malformed payload from [Source]. Last occurrence: [timestamp]." | Amber |
| Outbound webhook secret not set (no HMAC) | "Outbound webhook '[Name]' has no secret key configured. Payloads are unsigned — target system cannot verify authenticity." | Amber |
| Retry queue backed up >100 pending retries | "Webhook retry queue has [N] pending deliveries. Check target endpoints for availability issues." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Outbound Webhooks | Total configured outbound webhook endpoints | Blue | Switch to Outbound tab |
| Active Outbound | Outbound with status = Active | Green | Filter Active on Outbound tab |
| Inbound Endpoints | Total configured inbound endpoint definitions | Blue | Switch to Inbound tab |
| Failed Deliveries (24h) | Count of failed delivery attempts across all outbound webhooks in last 24h | Red if > 0, Green if 0 | Opens delivery log filtered by failures |
| Pending Retries | Deliveries currently in retry queue | Amber if > 0 | Opens retry queue view; Drill-down: Filter delivery log to Status = Retry Pending |

---

## 5. Main Tables

### 5.1 Tab: Outbound Webhooks

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Webhook Name | Text | Yes | Yes (text search) |
| Event | Badge (payment.received / result.published / admission.confirmed / attendance.marked / fee.overdue / custom) | Yes | Yes (multi-select) |
| Target URL | Text (truncated, hover shows full URL) | No | No |
| Branch Scope | Text (Group-wide / N Branches) | Yes | No |
| Status | Badge (Active / Inactive) | Yes | Yes |
| Last Triggered | Datetime (relative) | Yes | No |
| Success Rate % | Number — green ≥95%, amber 80–94%, red <80% | Yes | No |
| Actions | Edit / Test / Disable / View Delivery Log | No | No |

### 5.2 Tab: Inbound Endpoints

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Endpoint Name | Text | Yes | Yes (text search) |
| Path | Text (monospace — `/webhooks/{slug}/`) | No | No |
| Source System | Text (e.g., "Razorpay", "DigiLocker") | Yes | No |
| Events Expected | Text (comma-separated event names) | No | No |
| Last Received | Datetime (relative) | Yes | No |
| Verification Method | Badge (HMAC / Basic Auth / None) | Yes | Yes |
| Status | Badge (Active / Inactive) | Yes | Yes |
| Actions | View / Edit / View Payload Log / Disable | No | No |

### 5.3 Filters (Outbound)
- Status: Active / Inactive
- Event: multi-select (all event types)

### 5.4 Filters (Inbound)
- Status: Active / Inactive
- Verification Method: HMAC / Basic Auth / None

### 5.5 Search
- Outbound: Webhook name, target URL domain, event
- Inbound: Endpoint name, source system, path slug
- 300ms debounce

### 5.6 Pagination
- Server-side · 25 rows/page per tab

---

## 6. Drawers

### 6.1 Drawer: `outbound-webhook-create` — Create Outbound Webhook
- **Trigger:** `+ Create Outbound Webhook`
- **Width:** 560px
- **Fields:**
  - Webhook Name (required, text)
  - Event (required, dropdown — all available EduForge events):
    - payment.received, payment.failed, payment.refunded
    - result.published, result.updated
    - admission.confirmed, admission.cancelled
    - attendance.marked, attendance.absent-alert
    - fee.overdue, fee.reminder
    - staff.joined, staff.exited
    - custom (free-text event name)
  - Target URL (required, URL input — validated as HTTPS only)
  - Secret Key (optional but recommended — password input; auto-generate button; stored encrypted; used for HMAC-SHA256 payload signing. Shows warning if left blank)
  - Branch Scope (required, radio: Group-wide / Select Branches → branch multi-select)
  - HTTP Method (radio: POST / PUT — default POST)
  - Custom Headers (optional, key-value pair repeater — for adding Authorization headers etc.)
  - Retry Policy (dropdown: No Retry / 3 Attempts / 5 Attempts / 10 Attempts)
  - Retry Backoff (dropdown: Fixed 30s / Exponential — active when retry enabled)
  - Status (radio: Active / Create as Inactive — default Active)

### 6.2 Drawer: `outbound-webhook-delivery-log` — View Delivery Log
- **Trigger:** Actions → View Delivery Log
- **Width:** 720px
- **Header:** Webhook name, event, target URL, success rate summary
- **Table: Last 50 Delivery Attempts**

  | Column | Description |
  |---|---|
  | # | Attempt number |
  | Triggered At | Datetime |
  | Branch | Branch that originated the event |
  | Status | Success / Failed / Retry Pending |
  | HTTP Response Code | e.g., 200, 404, 500, Timeout |
  | Response Body Snippet | First 200 chars of response (truncated) |
  | Retry Count | Number of retry attempts so far |
  | Actions | Manual Retry (for failed entries) |

- **Retry All Failed** button — triggers retry for all failed deliveries in current log view

### 6.3 Drawer: `inbound-endpoint-create` — Create Inbound Endpoint
- **Trigger:** `+ Create Inbound Endpoint`
- **Width:** 560px
- **Fields:**
  - Endpoint Name (required, text)
  - Path Slug (required, text — alphanumeric + hyphens; auto-generates full path: `/webhooks/{slug}/`, shown read-only below input)
  - Source System (required, text — name of the external system sending payloads)
  - Events Expected (required, text — comma-separated event names expected in payloads)
  - Verification Method (required, radio: HMAC-SHA256 / Basic Auth / None)
    - HMAC: Secret key (auto-generate button); header name where signature is sent (default `X-Signature-256`)
    - Basic Auth: Username, Password
    - None: Shows security warning
  - Branch Scope (required — which branch's data these inbound events relate to)
  - Expected Content-Type (radio: `application/json` / `application/x-www-form-urlencoded` — default JSON)
  - Status (radio: Active / Create as Inactive)

### 6.4 Drawer: `outbound-webhook-edit` — Edit Outbound Webhook
- Same as create, pre-populated; event type is locked post-creation (must delete and recreate to change event)

### 6.5 Modal: Disable Webhook / Endpoint
- Generic confirmation: "Disabling '[Name]' will stop [delivery of events to / acceptance of events from] the configured endpoint. Confirm?"
- Buttons: Confirm Disable · Cancel

---

## 7. Charts

No standalone page-level charts. Delivery success rate trends are visible within the View Delivery Log drawer (sparkline showing success/failure rate over last 7 days per webhook).

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Outbound webhook created | "Outbound webhook '[Name]' created and active." | Success | 4s |
| Inbound endpoint created | "Inbound endpoint '[Name]' created. Path: /webhooks/[slug]/" | Success | 4s |
| Webhook updated | "Webhook '[Name]' updated." | Success | 3s |
| Webhook disabled | "Webhook '[Name]' disabled." | Warning | 4s |
| Manual retry triggered | "Retry triggered for [N] failed deliveries." | Info | 4s |
| Retry all triggered | "Retrying all failed deliveries for '[Name]'." | Info | 4s |
| Test delivery sent | "Test payload sent to '[Target URL]'. Check delivery log for result." | Info | 5s |
| Manual retry succeeded | Success: `Webhook delivery retry succeeded for event [ID].` | Success | 4s |
| Manual retry failed | Error: `Webhook retry failed. Check endpoint availability and try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No outbound webhooks | "No Outbound Webhooks" | "Create outbound webhooks to push EduForge events to external systems in real time." | + Create Outbound Webhook |
| No inbound endpoints | "No Inbound Endpoints" | "Create inbound endpoints to receive event payloads from payment gateways, government APIs, and other external systems." | + Create Inbound Endpoint |
| Delivery log empty | "No Deliveries Yet" | "This webhook has not been triggered yet." | — |
| No filter results | "No Matching Webhooks" | "No webhooks match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 5 KPI shimmer cards + outbound table skeleton (10 rows) |
| Tab switch | Table skeleton shimmer |
| Delivery log drawer open | Drawer spinner; delivery log table loads after header renders |
| Test delivery submit | Button spinner: "Sending test payload…" |
| Manual retry submit | Button spinner: "Retrying…" |
| Retry all submit | Progress indicator: "Queuing retries for [N] failed deliveries…" |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | Cybersecurity Officer (G1) |
|---|---|---|---|
| + Create Outbound Webhook | Visible | Hidden | Hidden |
| + Create Inbound Endpoint | Visible | Hidden | Hidden |
| Edit Actions | Visible | Hidden | Hidden |
| Disable Actions | Visible | Hidden | Hidden |
| View Delivery Log | Visible | Visible | Hidden |
| Response Body in Delivery Log | Visible | Visible | Hidden |
| Secret Keys (HMAC) | Editable (masked) | Hidden | Hidden |
| Verification method badge | Visible | Visible | Visible |
| Target URLs | Visible | Visible | Hidden |
| Manual Retry | Visible | Hidden | Hidden |
| Test Delivery | Visible | Hidden | Hidden |

> Roles 54 (IT Admin), 55 (DPO), and 57 (IT Support Executive) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/webhooks/outbound/` | JWT (G4+) | Paginated outbound webhook list |
| POST | `/api/v1/it/webhooks/outbound/` | JWT (G4 — Integration Manager) | Create outbound webhook |
| GET | `/api/v1/it/webhooks/outbound/{id}/` | JWT (G4+) | Outbound webhook detail |
| PATCH | `/api/v1/it/webhooks/outbound/{id}/` | JWT (G4 — Integration Manager) | Update outbound webhook |
| POST | `/api/v1/it/webhooks/outbound/{id}/disable/` | JWT (G4 — Integration Manager) | Disable outbound webhook |
| POST | `/api/v1/it/webhooks/outbound/{id}/test/` | JWT (G4 — Integration Manager) | Send test payload to target URL |
| GET | `/api/v1/it/webhooks/outbound/{id}/delivery-log/` | JWT (G4+) | Last 50 delivery attempts |
| POST | `/api/v1/it/webhooks/outbound/{id}/retry-all/` | JWT (G4 — Integration Manager) | Retry all failed deliveries |
| POST | `/api/v1/it/webhooks/outbound/{id}/delivery/{attempt_id}/retry/` | JWT (G4 — Integration Manager) | Retry single failed delivery |
| GET | `/api/v1/it/webhooks/inbound/` | JWT (G4+) | Paginated inbound endpoint list |
| POST | `/api/v1/it/webhooks/inbound/` | JWT (G4 — Integration Manager) | Create inbound endpoint |
| GET | `/api/v1/it/webhooks/inbound/{id}/` | JWT (G4+) | Inbound endpoint detail |
| PATCH | `/api/v1/it/webhooks/inbound/{id}/` | JWT (G4 — Integration Manager) | Update inbound endpoint |
| POST | `/api/v1/it/webhooks/inbound/{id}/disable/` | JWT (G4 — Integration Manager) | Disable inbound endpoint |
| GET | `/api/v1/it/webhooks/kpis/` | JWT (G4+) | KPI values for both tabs |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/webhooks/kpis/` | `#kpi-bar` | `innerHTML` |
| Load outbound table | `load` on tab render | GET `/api/v1/it/webhooks/outbound/` | `#outbound-table` | `innerHTML` |
| Load inbound table | `click` on Inbound tab | GET `/api/v1/it/webhooks/inbound/` | `#inbound-table` | `innerHTML` |
| Apply outbound filters | `change` on filter controls | GET `/api/v1/it/webhooks/outbound/?status=...` | `#outbound-table` | `innerHTML` |
| Search outbound | `input` (300ms debounce) | GET `/api/v1/it/webhooks/outbound/?q=...` | `#outbound-table` | `innerHTML` |
| Search inbound | `input` (300ms debounce) | GET `/api/v1/it/webhooks/inbound/?q=...` | `#inbound-table` | `innerHTML` |
| Open delivery log drawer | `click` on View Delivery Log | GET `/api/v1/it/webhooks/outbound/{id}/delivery-log/` | `#webhook-drawer` | `innerHTML` |
| Manual retry single | `click` on Retry | POST `.../delivery/{id}/retry/` | `#delivery-row-{id}` | `outerHTML` |
| Retry all failed | `click` on Retry All | POST `.../retry-all/` | `#delivery-log-table` | `innerHTML` |
| Submit create outbound | `click` on Create | POST `/api/v1/it/webhooks/outbound/` | `#outbound-table` | `innerHTML` |
| Submit create inbound | `click` on Create | POST `/api/v1/it/webhooks/inbound/` | `#inbound-table` | `innerHTML` |
| Send test payload | `click` on Test | POST `/api/v1/it/webhooks/outbound/{id}/test/` | `#test-result` | `innerHTML` |
| Paginate outbound | `click` on page control | GET `/api/v1/it/webhooks/outbound/?page=N` | `#outbound-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Webhook delivery failure rate > 20%: Integration Manager (in-app amber + email) immediately
- Retry queue > 100 items: Integration Manager + IT Admin (in-app amber + email)
- Inbound webhook authentication failure: Integration Manager (in-app amber + email)
- SSL certificate for webhook endpoint < 14 days: Integration Manager (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
