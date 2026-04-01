# 19 — WhatsApp Notification Config

- **URL:** `/group/it/notifications/whatsapp/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Admin (Role 54, G4) — Primary owner

---

## 1. Purpose

The WhatsApp Notification Config page is the critical configuration surface for the WhatsApp Business API integration that powers the majority of EduForge's outbound communication. This page is Priority P0 — if the configuration here is broken, OTP login stops working for all users across all branches, attendance alerts stop reaching parents, fee reminders stop sending, and exam notifications go dark. Every message that EduForge sends via WhatsApp originates from the settings configured on this page.

EduForge uses WhatsApp as the primary communication channel because of near-universal smartphone adoption among Indian school parents and staff. The platform integrates with a WhatsApp Business API (WABA) provider — such as 360dialog or Gupshup — which acts as the conduit between EduForge's FastAPI backend and Meta's WhatsApp Business platform. The IT Admin must configure the API credentials, map them to approved message templates, and control delivery behaviour from this single page. Branch staff have no access to WhatsApp configuration — this is exclusively a group-level IT function.

The page is structured into five logical sections rather than a primary table + drawer layout, reflecting its nature as a configuration hub rather than a data management surface. However, the Message Templates section does contain a proper table with associated actions. The Delivery Logs section provides operational visibility into the last 100 messages sent, allowing the IT Admin to diagnose delivery failures without needing to query the database directly.

The non-dismissible red alert banner for provider connection failure is a critical design requirement: if the IT Admin inadvertently saves incorrect API credentials, they must be made immediately and inescapably aware that the OTP channel is broken.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + write (all sections) | Sole operator of this page |
| Group IT Director | G4 | Full read + write | Strategic oversight; can also configure |
| Group EduForge Integration Manager | G4 | Read-only + template management | Can view all; can create/edit/test templates |
| Group IT Support Executive | G3 | Read-only (Delivery Logs section only) | For diagnosing delivery failures in support tickets |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Notifications → WhatsApp Config
```

### 3.2 Page Header
- **Title:** `WhatsApp Notification Configuration`
- **Subtitle:** `WhatsApp Business API · Provider: [Provider Name] · Status: [Connected ✓ / Disconnected ✗]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Test Connection` · `View Delivery Logs`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Provider API connection failed (last health check) | "WhatsApp provider connection FAILED. OTP delivery and all WhatsApp notifications are currently non-functional. Check API credentials immediately." | Red (non-dismissible) |
| One or more active templates not approved by Meta | "[N] WhatsApp template(s) are not approved by Meta and cannot be sent. Review template status." | Amber |
| OTP template is inactive or not approved | "The OTP authentication template is inactive or not approved. Users cannot log in via OTP." | Red (non-dismissible) |
| WABA phone number approaching 24h window limit | "WhatsApp conversation window expiring for [N] active conversations. Utility messages may not reach users." | Amber |

---

## 4. KPI Summary Bar

No traditional KPI cards. The page header status line (Connected / Disconnected) serves as the primary health indicator. Section 5 (Delivery Logs) provides the last-24h delivery stats inline.

---

## 5. Main Table — Message Templates (Section 2)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Template Name | Text | Yes | Yes (text search) |
| Category | Badge (Authentication / Utility / Marketing) | No | Yes (multi-select) |
| Language | Text (e.g., English / Telugu / Hindi) | No | Yes |
| Status | Badge (Approved / Pending / Rejected / Inactive) | No | Yes |
| Last Used | Date (relative) | Yes | No |
| Message Count (30d) | Number | Yes | No |
| Actions | View / Test / Set Active / Set Inactive | No | No |

### 5.1 Filters (Templates table)
- Category: Multi-select (Authentication / Utility / Marketing)
- Language: Multi-select (all configured languages)
- Status: Checkbox (Approved / Pending / Rejected / Inactive)

### 5.2 Search (Templates table)
- Full-text: Template Name
- 300ms debounce

### 5.3 Pagination (Templates table)
- Server-side · 15 rows/page

---

## 6. Drawers

### 6.1 Section 1: Provider Configuration (Form Panel)

**Fields:**
- WhatsApp Business API Provider (dropdown: 360dialog / Gupshup / Meta Direct / Other)
- API Key (masked input; show/hide toggle; required, min 32 characters, alphanumeric + special characters)
- Phone Number ID (text; required — the WABA phone number ID from Meta Business Manager)
- WhatsApp Business Account ID / WABA ID (text; required)
- Webhook URL (read-only, auto-generated: `https://api.eduforge.in/webhooks/whatsapp/`)
- Webhook Verify Token (text; set once; used for Meta webhook verification)

**Test Connection button (inline):** Sends a test API ping to the provider; returns success (green inline message) or failure (red inline message with error code). Does not send a WhatsApp message.

**Save button:** PATCH to provider config endpoint; on save, triggers an immediate connection health check; alert banner updates accordingly.

---

### 6.2 Drawer: `template-view` — View Template
- **Trigger:** Actions → View
- **Width:** 480px
- **Content:**
  - Template Name, Category, Language, Meta approval status, Meta template ID
  - Full message body with variable placeholders highlighted (e.g., `{{1}}` shown as `{{student_name}}` with variable mapping table)
  - Header (if any), Body, Footer (if any), Buttons (if any — quick reply or call-to-action)
  - Last used date, 30-day send count
  - Whether this template is currently set as the Active OTP template (if Category = Authentication)

### 6.3 Modal: Test Template
- **Trigger:** Actions → Test
- **Type:** Centered modal (440px)
- **Content:** "Send a test message using template '[Template Name]' to a test number."
- **Fields:**
  - Test Mobile Number (required, 10-digit with country code)
  - Variable values: one input per variable placeholder in the template (e.g., "Student Name: [text input]", "Fee Amount: [text input]")
- **Buttons:** Send Test Message · Cancel
- **On send:** POST to test-send endpoint; inline result shows delivery status (Sent / Failed with error)

---

### 6.4 Section 3: Delivery Settings (Form Panel)

**Fields:**
- Retry on Delivery Failure (toggle: Yes / No)
- Max Retry Attempts (number input, 1–5; disabled if retry off)
- Retry Interval (dropdown: 2 min / 5 min / 10 min / 30 min)
- Fallback to SMS if WhatsApp Delivery Fails (toggle: Yes / No; links to SMS gateway config)
- Fallback Trigger (dropdown: After 1 retry / After all retries / Never; visible only if fallback on)

---

### 6.5 Section 4: Branch Overrides (Table Panel)

A small table showing per-branch WhatsApp config status:

| Branch | Uses Group Config | Override Details | Actions |
|---|---|---|---|
| Branch A | Yes (default) | — | — |
| Branch B | No (override) | Custom WABA ID set | View Override |

"View Override" opens a read-only mini-drawer showing the branch's custom WhatsApp configuration. Branch-level overrides are configured by the IT Admin at branch level and are visible here for audit purposes only — they cannot be edited from this group-level page.

---

### 6.5 Drawer: `template-import` — Import / Register Template from Meta
- **Trigger:** `Import Template` button (top-right of templates table, IT Admin / Integration Manager only)
- **Width:** 520px
- **Context note at top:** "WhatsApp templates are created and submitted for approval in Meta Business Manager. Once Meta approves a template, register it here so EduForge can use it for notifications. Do NOT create templates in EduForge — they must exist and be approved in Meta Business Manager first."
- **Fields:**
  - Meta Template Name (required, text — exact name as registered in Meta Business Manager; case-sensitive)
  - Category (required, dropdown: Authentication / Utility / Marketing)
  - Language (required, dropdown: English / Telugu / Hindi / Tamil / Kannada / Malayalam)
  - Meta Template ID (optional, text — the numeric ID from Meta Business Manager for reference)
  - Variable Mapping (dynamic section — shown after name is entered): for each `{{N}}` variable in the template body, provide a human-readable label (e.g., `{{1}}` → "Student Name", `{{2}}` → "Fee Amount") so IT Admin can understand the template in the EduForge interface
  - Set as Active OTP Template (checkbox — only shown if Category = Authentication; marks this as the template used for login OTPs)
- **Fetch from Meta button:** "Validate & Fetch Template" — calls Meta API with the given name to confirm the template exists and is Approved; populates the body preview inline; shows error if template not found or not approved
- **Footer:** Import Template / Cancel
- **On submit:** Template registered in EduForge's template registry; status reflects Meta's current approval status (Approved/Pending/Rejected)

---

### 6.6 Section 5: Delivery Logs (Table Panel)

Most recent 100 WhatsApp messages sent group-wide:

| Column | Type |
|---|---|
| Recipient | Masked phone (last 4 digits visible: +91 XXXXX X5678) |
| Template Used | Template name |
| Branch | Originating branch |
| Category | Authentication / Utility / Marketing |
| Status | Badge (Sent / Delivered / Read / Failed) |
| Timestamp | DateTime |
| Actions | View Details |

**View Details** opens an inline expanded row (not a drawer) showing: full WhatsApp message ID, provider message ID, error code if failed, retry attempts made.

Pagination: 20 rows/page within this section. Not linked to main table pagination.

---

## 7. Charts

No dedicated chart section. Delivery Logs table provides operational visibility. Full analytics (delivery rates, failure trends) are on the IT Analytics page.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Provider settings saved + connection OK | "WhatsApp provider configuration saved. Connection verified successfully." | Success | 4s |
| Provider settings saved + connection failed | "Settings saved but provider connection failed. Check API credentials." | Error | 7s |
| Test message sent | "Test message sent to [masked number]. Check WhatsApp for delivery." | Info | 4s |
| Test message failed | "Test message failed: [error message from provider]." | Error | 6s |
| Template set Active | "Template '[Name]' is now set as Active." | Success | 3s |
| Template set Inactive | "Template '[Name]' has been deactivated." | Warning | 3s |
| Template imported | "Template '[Name]' imported successfully. Status: [Approved/Pending]." | Success | 4s |
| Template validation failed | "Template '[Name]' not found in Meta Business Manager or not yet approved." | Error | 6s |
| Delivery settings saved | "Delivery settings updated." | Success | 3s |
| Test connection failed | Error: `WhatsApp provider test failed: [error code]. Check API credentials.` | Error | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No templates configured | "No WhatsApp Templates" | "No message templates have been registered. Create templates in Meta Business Manager, get them approved, then import them here." | Import Template |
| Delivery Logs — no messages sent yet | "No Delivery Logs" | "No WhatsApp messages have been sent through this configuration yet." | — |
| Templates table — no results for filter | "No Templates Match" | "No templates match the selected category or status filter." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Section 1 (Provider Config) form skeleton + Templates table skeleton (8 rows) + Delivery Logs table skeleton |
| Test Connection button click | Button spinner; inline result appears within the section (not toast) |
| Templates table filter/search | Table rows shimmer; section header count updates |
| Template view drawer open | 480px drawer skeleton |
| Test template send | Modal send button spinner; inline result appears within modal |
| Section save (any) | Section-level Save button spinner only |
| Import template drawer open | Drawer skeleton while form loads |
| Template validation (Validate & Fetch button) | Button spinner: "Fetching template…" |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| Section 1 (Provider Config) edit | Visible | Visible | Hidden | Hidden |
| Test Connection | Visible | Visible | Hidden | Hidden |
| Templates table | Visible | Visible | Visible | Hidden |
| Template View / Test | Visible | Visible | Visible | Hidden |
| Set Active / Set Inactive | Visible | Visible | Visible | Hidden |
| Section 3 (Delivery Settings) edit | Visible | Visible | Hidden | Hidden |
| Section 4 (Branch Overrides) | Visible (read) | Visible (read) | Visible (read) | Hidden |
| Section 5 (Delivery Logs) | Visible | Visible | Visible | Visible |
| Export Delivery Logs | Visible | Visible | Visible | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/notifications/whatsapp/config/` | JWT (G1+) | Retrieve current provider config (API key masked) |
| PATCH | `/api/v1/it/notifications/whatsapp/config/` | JWT (G4) | Update provider configuration |
| POST | `/api/v1/it/notifications/whatsapp/config/test-connection/` | JWT (G4) | Test provider API connectivity |
| GET | `/api/v1/it/notifications/whatsapp/templates/` | JWT (G4) | Paginated template list |
| GET | `/api/v1/it/notifications/whatsapp/templates/{id}/` | JWT (G4) | Single template detail |
| POST | `/api/v1/it/notifications/whatsapp/templates/{id}/test/` | JWT (G4) | Send test message for a template |
| POST | `/api/v1/it/notifications/whatsapp/templates/import/` | JWT (G4) | Import a Meta-approved template into EduForge |
| POST | `/api/v1/it/notifications/whatsapp/templates/validate/` | JWT (G4) | Validate template name against Meta API and fetch body preview |
| PATCH | `/api/v1/it/notifications/whatsapp/templates/{id}/` | JWT (G4) | Set template active/inactive status |
| PATCH | `/api/v1/it/notifications/whatsapp/delivery-settings/` | JWT (G4) | Update retry and fallback settings |
| GET | `/api/v1/it/notifications/whatsapp/delivery-logs/` | JWT (G3+) | Paginated delivery log (last 100) |
| GET | `/api/v1/it/notifications/whatsapp/branch-overrides/` | JWT (G4) | Per-branch override status |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load provider config section | `load` | GET `/api/v1/it/notifications/whatsapp/config/` | `#provider-config-section` | `innerHTML` |
| Load templates table | `load` | GET `/api/v1/it/notifications/whatsapp/templates/` | `#templates-table` | `innerHTML` |
| Load delivery logs section | `load` | GET `/api/v1/it/notifications/whatsapp/delivery-logs/` | `#delivery-logs-section` | `innerHTML` |
| Test connection button | `click` | POST `/api/v1/it/notifications/whatsapp/config/test-connection/` | `#connection-status` | `innerHTML` |
| Filter templates | `change` | GET `/api/v1/it/notifications/whatsapp/templates/?category=...` | `#templates-table` | `innerHTML` |
| Search templates | `input` (300ms debounce) | GET `/api/v1/it/notifications/whatsapp/templates/?q=...` | `#templates-table` | `innerHTML` |
| Open template view drawer | `click` on View | GET `/api/v1/it/notifications/whatsapp/templates/{id}/` | `#template-drawer` | `innerHTML` |
| Save provider config | `click` on Save | PATCH `/api/v1/it/notifications/whatsapp/config/` | `#provider-config-section` | `outerHTML` |
| Save delivery settings | `click` on Save | PATCH `/api/v1/it/notifications/whatsapp/delivery-settings/` | `#delivery-settings-section` | `outerHTML` |
| Paginate delivery logs | `click` on page control | GET `/api/v1/it/notifications/whatsapp/delivery-logs/?page=N` | `#delivery-logs-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- Provider API connection failed: IT Admin + IT Director (in-app red non-dismissible + email) immediately
- OTP template inactive/not approved: IT Admin + IT Director (in-app red non-dismissible + email) immediately
- Template rejected by Meta: IT Admin + Integration Manager (in-app amber + email)

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
