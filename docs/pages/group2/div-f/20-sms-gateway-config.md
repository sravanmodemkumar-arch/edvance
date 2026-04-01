# 20 — SMS Gateway Config

- **URL:** `/group/it/notifications/sms/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The SMS Gateway Config page manages the SMS delivery infrastructure that functions as both a fallback channel when WhatsApp delivery fails and as a supplemental direct notification channel for recipients without WhatsApp or with WhatsApp delivery restrictions. While WhatsApp is the primary channel, SMS is the safety net — if the WhatsApp API goes down or a message is undeliverable (wrong number, no WhatsApp), SMS ensures the message still reaches the recipient.

In the Indian regulatory context, SMS delivery for commercial and transactional purposes is subject to strict TRAI regulations under the Distributed Ledger Technology (DLT) framework. Every SMS provider, every sender ID, and every message template must be registered on the DLT platform before a single message can legally be sent. The DLT compliance section of this page — Principal Entity ID, Template IDs — is therefore not optional configuration but a mandatory legal requirement. A DLT-unregistered template will be blocked by every Indian telecom carrier. The page enforces this by showing a non-dismissible red alert banner when any active template lacks a valid DLT ID.

The page follows a similar section structure to the WhatsApp config page (File 19), reflecting the parallel configuration concerns of provider credentials, template management, delivery rules, and log visibility. A credit balance indicator is unique to SMS — unlike WhatsApp which is billed per conversation by the provider, most Indian SMS gateways use prepaid credit bundles, and running out of SMS credits at the wrong moment (e.g., during exam result notification day) is a critical operational failure. The low-credit alert is amber at < 1,000 credits and red at < 200 credits.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (all sections) | Primary operator |
| Group IT Director | G4 | Full read + write | Strategic oversight |
| Group EduForge Integration Manager | G4 | Read-only + template management | Can view; can add/edit DLT templates |
| Group IT Support Executive | G3 | Read-only (Delivery Logs only) | For support ticket diagnosis |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Notifications → SMS Gateway Config
```

### 3.2 Page Header
- **Title:** `SMS Gateway Configuration`
- **Subtitle:** `SMS Provider: [Provider Name] · Sender ID: [SENDER] · DLT Status: [Registered / Not Registered]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Test SMS` · `View Delivery Logs`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| DLT template used by an active trigger but missing DLT ID | "One or more SMS templates in active use have not been registered on DLT. SMS delivery is being blocked by carriers." | Red (non-dismissible) |
| SMS credit balance < 1,000 | "SMS credit balance is critically low ([N] credits remaining). Recharge to ensure uninterrupted delivery." | Amber |
| SMS credit balance < 200 | "SMS credits almost exhausted ([N] remaining). SMS notifications will fail when credits reach zero." | Red |
| Provider API connection failed | "SMS gateway connection failed. SMS notifications are non-functional. Check provider credentials." | Red (non-dismissible) |
| Sender ID not active / suspended by provider | "Sender ID '[SENDER]' is not active with the SMS provider. All SMS will fail until resolved." | Red (non-dismissible) |

---

## 4. KPI Summary Bar

No traditional KPI cards. The page header line provides essential provider status. The credit balance is shown as a dedicated inline widget within Section 4, with colour-coded progress bar (green/amber/red based on credit level).

---

## 5. Main Table — SMS Templates (Section 2)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Template Name | Text | Yes | Yes (text search) |
| DLT Template ID | Text (or "Not Registered" in red) | No | No |
| Content Preview | Text (truncated to 80 chars) | No | No |
| Category | Badge (OTP / Transactional / Promotional) | No | Yes |
| Status | Badge (Active / Inactive / DLT Pending) | No | Yes |
| Actions | View / Edit / Test / Set Active / Set Inactive | No | No |

### 5.1 Filters
- Category: Checkbox (OTP / Transactional / Promotional)
- Status: Checkbox (Active / Inactive / DLT Pending)

### 5.2 Search
- Template Name full-text
- 300ms debounce

### 5.3 Pagination
- Server-side · 15 rows/page

---

## 6. Drawers

### 6.1 Section 1: Provider Configuration (Form Panel)

**Fields:**
- SMS Provider (dropdown: MSG91 / Textlocal / AWS SNS / Kaleyra / Other)
- API Key (masked; show/hide toggle; required)
- Sender ID (text, exactly 6 uppercase alpha characters; e.g., EDUFRG; required for Indian SMS; required, exactly 6 uppercase letters; validation error: "Sender ID must be exactly 6 uppercase letters")
- DLT Principal Entity ID (text; required — the PE ID registered on TRAI DLT portal; required, numeric, typically 9 digits)
- Route (radio: Transactional / Promotional; Transactional for OTP and fee alerts, Promotional for marketing)
- Country Code Default (dropdown: +91 India / Other; for multi-country groups)

**Test SMS button (inline):** Sends a test SMS to a test number entered in a small inline field. Returns success (green inline status) or failure (red with error).

---

### 6.2 Drawer: `sms-template-view` — View / Edit Template
- **Trigger:** Actions → View or Edit
- **Width:** 480px
- **Content (View):**
  - Template Name, Category, Status
  - DLT Template ID (editable if not yet registered)
  - Full SMS body text with variable markers (e.g., `{#var#}` DLT format)
  - Character count (standard SMS = 160 chars; Unicode/regional = 70 chars per segment)
  - DLT registration status and last checked date
- **Content (Edit):**
  - Same fields as view but editable
  - DLT Template ID (text input with helper: "Obtain from your DLT portal registration")
  - Template body (textarea with character counter)
  - Category (dropdown)
  - On Save: PATCH to template endpoint; if DLT ID is blank, status remains "DLT Pending"

### 6.3 Modal: Test SMS Template
- **Trigger:** Actions → Test
- **Type:** Centered modal (440px)
- **Content:** "Send a test SMS using template '[Template Name]'."
- **Fields:**
  - Test Mobile Number (required, 10-digit)
  - Variable values: one input per `{#var#}` placeholder in the template
- **Buttons:** Send Test SMS · Cancel
- **On send:** Delivery result shown inline in modal (Sent / Failed + error)

### 6.4 Section 3: Delivery Settings (Form Panel)

**Fields:**
- Retry Count (number input, 0–3)
- Retry Interval (dropdown: 1 min / 2 min / 5 min / 10 min)
- Default Route (radio: Transactional / Promotional — matches Section 1 setting; per-template override possible)
- OTP SMS Timeout (seconds before OTP SMS is considered expired; 60–600 seconds)

### 6.5 Section 4: Credit Balance (Information Panel)

- **Current Balance:** `[N,NNN] credits` (large display, colour-coded)
- **Progress bar:** Visual credit level indicator (green > 5,000 / amber 1,000–5,000 / red < 1,000)
- **Estimated Remaining Usage:** "At current send rate ([N] SMS/day), this covers approximately [X] days."
- **Low Credit Threshold:** Configurable input — send alert when credits fall below this number (default 1,000)
- **Recharge Link:** External link button "Recharge Credits on [Provider] Portal" (opens in new tab)
- **Last Balance Sync:** Timestamp of last balance API pull + Sync Now button (triggers fresh balance check)

---

### 6.6 Section 5: Delivery Logs (Table Panel)

Most recent 100 SMS messages sent:

| Column | Notes |
|---|---|
| Recipient | Masked phone (last 4 visible) |
| Template Used | Template name |
| Branch | Originating branch |
| Category | OTP / Transactional / Promotional |
| Status | Badge (Sent / Delivered / Failed / DLT Blocked) |
| Timestamp | DateTime |

No Actions column — delivery logs are read-only. Pagination: 20 rows/page.

---

## 7. Charts

No dedicated chart section. Delivery Logs section provides operational visibility. Full SMS analytics on the IT Analytics page.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Provider config saved + connected | "SMS gateway configuration saved. Connection verified." | Success | 4s |
| Provider config saved + failed | "Settings saved but SMS gateway connection failed. Check API credentials." | Error | 7s |
| Test SMS sent | "Test SMS sent to [masked number]." | Info | 4s |
| Test SMS failed | "Test SMS failed: [error message from provider]." | Error | 6s |
| Template saved | "Template '[Name]' saved." | Success | 3s |
| Template activated | "Template '[Name]' is now Active." | Success | 3s |
| Template deactivated | "Template '[Name]' has been deactivated." | Warning | 3s |
| Balance synced | "SMS credit balance updated: [N,NNN] credits." | Info | 3s |
| Low credit alert threshold saved | "Low credit alert threshold set to [N] credits." | Success | 3s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No SMS templates configured | "No SMS Templates" | "No SMS templates have been added. Add templates after registering them on your DLT portal." | Add Template |
| Delivery Logs — no messages sent | "No SMS Delivery Logs" | "No SMS messages have been sent through this gateway yet." | — |
| Templates table — filter shows no results | "No Matching Templates" | "No templates match the selected category or status." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Section 1 form skeleton + Templates table skeleton (8 rows) + Credit Balance panel shimmer + Delivery Logs skeleton |
| Test SMS click | Button spinner; inline result replaces spinner on completion |
| Templates filter/search | Table shimmer |
| Template view/edit drawer open | 480px drawer skeleton |
| Balance sync (Sync Now) | Sync Now button spinner; credit display updates in-place |
| Section save | Section Save button spinner only |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| Section 1 (Provider Config) edit | Visible | Visible | Hidden | Hidden |
| Test SMS (provider level) | Visible | Visible | Hidden | Hidden |
| Templates table | Visible | Visible | Visible | Hidden |
| Template edit / Test | Visible | Visible | Visible | Hidden |
| Section 3 (Delivery Settings) | Visible | Visible | Hidden | Hidden |
| Section 4 (Credit Balance) | Visible | Visible | Visible | Hidden |
| Recharge Credits link | Visible | Visible | Hidden | Hidden |
| Section 5 (Delivery Logs) | Visible | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/notifications/sms/config/` | JWT (G3+) | Retrieve current SMS provider config (API key masked) |
| PATCH | `/api/v1/it/notifications/sms/config/` | JWT (G4) | Update provider configuration |
| POST | `/api/v1/it/notifications/sms/config/test/` | JWT (G4) | Send test SMS |
| GET | `/api/v1/it/notifications/sms/templates/` | JWT (G4) | Paginated SMS template list |
| GET | `/api/v1/it/notifications/sms/templates/{id}/` | JWT (G4) | Single template detail |
| POST | `/api/v1/it/notifications/sms/templates/` | JWT (G4) | Create new SMS template |
| PATCH | `/api/v1/it/notifications/sms/templates/{id}/` | JWT (G4) | Update template (body, DLT ID, status) |
| POST | `/api/v1/it/notifications/sms/templates/{id}/test/` | JWT (G4) | Test send a specific template |
| PATCH | `/api/v1/it/notifications/sms/delivery-settings/` | JWT (G4) | Update delivery and retry settings |
| GET | `/api/v1/it/notifications/sms/credits/` | JWT (G3+) | Current credit balance + usage estimate |
| POST | `/api/v1/it/notifications/sms/credits/sync/` | JWT (G4) | Trigger fresh credit balance sync from provider |
| GET | `/api/v1/it/notifications/sms/delivery-logs/` | JWT (G3+) | Paginated delivery log |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load provider config section | `load` | GET `/api/v1/it/notifications/sms/config/` | `#sms-provider-section` | `innerHTML` |
| Load templates table | `load` | GET `/api/v1/it/notifications/sms/templates/` | `#sms-templates-table` | `innerHTML` |
| Load credit balance section | `load` | GET `/api/v1/it/notifications/sms/credits/` | `#credit-balance-section` | `innerHTML` |
| Load delivery logs | `load` | GET `/api/v1/it/notifications/sms/delivery-logs/` | `#sms-delivery-logs` | `innerHTML` |
| Filter templates | `change` | GET `/api/v1/it/notifications/sms/templates/?category=...` | `#sms-templates-table` | `innerHTML` |
| Search templates | `input` (300ms debounce) | GET `/api/v1/it/notifications/sms/templates/?q=...` | `#sms-templates-table` | `innerHTML` |
| Open template view/edit drawer | `click` on View/Edit | GET `/api/v1/it/notifications/sms/templates/{id}/` | `#sms-template-drawer` | `innerHTML` |
| Save provider config | `click` on Save | PATCH `/api/v1/it/notifications/sms/config/` | `#sms-provider-section` | `outerHTML` |
| Sync credit balance | `click` on Sync Now | POST `/api/v1/it/notifications/sms/credits/sync/` | `#credit-balance-section` | `innerHTML` |
| Paginate delivery logs | `click` on page control | GET `/api/v1/it/notifications/sms/delivery-logs/?page=N` | `#sms-delivery-logs-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- SMS provider connection failed: IT Admin + IT Director (in-app red non-dismissible + email) immediately
- DLT template rejected: IT Admin + Integration Manager (in-app amber + email)
- Low credit balance (< 1000 credits): IT Admin (in-app amber + email daily until topped up)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
