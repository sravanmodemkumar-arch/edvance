# 26 — API Key Manager

- **URL:** `/group/it/integrations/api-keys/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group EduForge Integration Manager (Role 58, G4) — Full access

---

## 1. Purpose

The API Key Manager is the central control panel for all API keys used by external systems to access EduForge's APIs. When a third-party system needs programmatic access to EduForge — a payment gateway sending webhooks, an analytics platform pulling attendance data, an LMS integration syncing results — it authenticates using an API key issued from this page.

API keys are scoped on two dimensions: branch scope (which branches' data the key can access — a single branch, multiple branches, or group-wide) and endpoint scope (which API endpoints the key is authorised to call). This fine-grained scoping follows the principle of least privilege: the Razorpay payment webhook only gets access to payment-related endpoints for the branches it serves, not student records or exam data.

Security is paramount here. Raw API key values are shown exactly once — immediately after creation — in a full-screen masked reveal with a copy button and a prominent "Store this key securely — it will never be shown again" warning. After dismissal, only the first 8 and last 4 characters are shown as a truncated hint (e.g., `efk_live_abcd••••••••••••wxyz`). The full value is stored as a SHA-256 hash in PostgreSQL — never as plaintext. Key rotation is supported with a 24-hour grace period where both old and new keys are valid, allowing zero-downtime rotation for production integrations.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group EduForge Integration Manager | G4 | Full read + write + rotate + revoke | Sole operator of this page |
| Group IT Director | G4 | Read-only (no key values visible) | Governance oversight; can see key names and statuses |
| Group Cybersecurity Officer | G1 | Read-only (status and expiry only) | Security audit visibility; no key hints visible |
| Group IT Admin (Role 54, G4) | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Integrations → API Key Manager
```

### 3.2 Page Header
- **Title:** `API Key Manager`
- **Subtitle:** `[N] Active Keys · [N] Expiring Soon · [N] Revoked (Last 30 Days)`
- **Role Badge:** `Group EduForge Integration Manager`
- **Right-side controls:** `+ Create API Key` button

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| API key expiring <7 days | "API key '[Key Name]' expires in [N] days. Rotate before expiry to prevent integration failure." | Red |
| API key expiring <30 days | "API key '[Key Name]' expires in [N] days. Consider rotating soon." | Amber |
| Revoked key still making requests (detected via auth failure log) | "SECURITY: Revoked key '[Key Name]' is still being used to make API requests. Verify the consuming system has been updated." | Red (non-dismissible) |
| Key with group-wide scope has not been rotated in >180 days | "API key '[Key Name]' has group-wide scope and has not been rotated in over 180 days. Rotation recommended." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total API Keys | Count of all non-deleted key records | Blue | No filter |
| Active | Keys with status = Active and not expired | Green | Filter by Active |
| Expiring <30 Days | Keys where expiry_date is within next 30 days | Amber if > 0 | Filter by expiring soon |
| Revoked (Last 30 Days) | Keys revoked in the last 30 calendar days | Red if > 0, Grey otherwise | Filter by Status = Revoked AND Created Date >= 30 days ago |

---

## 5. Main Table — API Keys

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Key Name | Text (descriptive name given at creation) | Yes | Yes (text search) |
| Created For | Text (system or integration name — e.g., "Razorpay Webhook Handler") | Yes | Yes (text search) |
| Scope | Text compound (e.g., "3 Branches · /payments/*, /webhooks/*") | No | No |
| Status | Badge (Active / Expired / Revoked) | Yes | Yes (multi-select) |
| Expiry Date | Date — amber if <30d, red if <7d, grey if expired | Yes | Yes (date range) |
| Last Used | Datetime (relative — "2h ago" or "Never") | Yes | No |
| Created By | Text (staff name) | Yes | No |
| Created Date | Date | Yes | Yes (date range) |
| Actions | View / Edit / Rotate / Revoke | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Multi-select checkbox | Active / Expired / Revoked |
| Expiry Date | Date range picker | Any range |
| Created Date | Date range picker | Any range |
| Branch Scope | Multi-select dropdown | All configured branches + Group-wide option |

### 5.2 Search
- Full-text: Key Name, Created For (integration/system name)
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page

---

## 6. Drawers

### 6.1 Drawer: `api-key-create` — Create API Key
- **Trigger:** `+ Create API Key` button
- **Width:** 480px
- **Fields:**
  - Key Name (required, text — e.g., "Razorpay Production Webhook Key")
  - Purpose / Description (required, textarea — describe what system will use this key and why)
  - Branch Scope (required, multi-select or radio: Group-wide / Select Branches → branch multi-select)
  - Endpoint Scope (required, multi-select checkbox with API endpoint categories):
    - Payments & Webhooks (`/api/v1/payments/*`, `/api/v1/webhooks/*`)
    - Student Data Read (`/api/v1/students/` GET only)
    - Attendance Data Read (`/api/v1/attendance/` GET only)
    - Exam Results Read (`/api/v1/results/` GET only)
    - Admission Data Read (`/api/v1/admissions/` GET only)
    - Custom Endpoints (text input — comma-separated endpoint patterns)
  - Expiry Date (required, date picker — minimum 1 day, maximum 2 years; default 1 year from today)
  - IP Allowlist (optional, comma-separated IPv4 addresses or CIDR ranges; each entry validated; error shown for invalid format)
- **On Submit:**
  - Full page overlay with key reveal UI:
    - Header: "API Key Created — Store This Securely"
    - Warning box (red): "This is the ONLY time you will see this key. Copy it now and store it in a secure secrets manager. It cannot be retrieved again."
    - Key value displayed in monospace box with copy button
    - Checkbox: "I have copied and stored this key securely" (must check to dismiss)
    - Dismiss button (disabled until checkbox checked)

### 6.2 Drawer: `api-key-view` — View API Key Detail
- **Trigger:** Actions → View
- **Width:** 560px
- **Sections:**
  - Key metadata: Name, Created For, Created By, Created Date, Expiry Date, Status
  - Scope summary: Branch scope list, endpoint scope list
  - IP Allowlist (if configured)
  - Key hint: Truncated key (`efk_live_abcd••••••••••••wxyz`) with tooltip "Full key value cannot be retrieved"
  - Usage: Last Used timestamp, Total requests (last 7d, last 30d), Top calling IPs (last 7d)
  - Rotation history: Table of past rotations — date, rotated by, grace period end date

### 6.3 Drawer: `api-key-edit` — Edit API Key
- **Trigger:** Actions → Edit
- **Width:** 480px
- Editable fields: Key Name, Purpose/Description, Expiry Date, IP Allowlist
- Non-editable: Branch Scope, Endpoint Scope (require rotate to change scope — this is by design to prevent scope creep; tooltip explains)
- On save: Audit log entry created

### 6.4 Drawer: `api-key-rotate` — Rotate API Key
- **Trigger:** Actions → Rotate
- **Width:** 480px
- Explanation text: "Rotating generates a new API key value. The old key remains valid for 24 hours (grace period) to allow zero-downtime rotation in production systems. After 24 hours the old key is automatically invalidated."
- Grace period override: Radio (24h grace period / Immediate invalidation — use for security incidents)
- Confirm checkbox: "I understand this will generate a new key value"
- **On Rotate:** New key reveal overlay (same as creation) + shows grace period end datetime

### 6.5 Modal: Revoke API Key
- **Trigger:** Actions → Revoke
- Warning: "Revoking '[Key Name]' will IMMEDIATELY and PERMANENTLY disable this key. Any system currently using this key will receive 401 Unauthorized responses. This cannot be undone."
- Text input: Reason for revocation (required — e.g., "Key compromised", "Integration decommissioned")
- Buttons: Confirm Revoke (red) · Cancel

---

## 7. Charts

No standalone charts on this page. Usage metrics are shown within the View drawer.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| API key created | "API key '[Name]' created. Copy the key value from the reveal overlay now — it will not be shown again." | Success | 6s |
| API key updated | "API key '[Name]' updated." | Success | 3s |
| Key rotated | "API key '[Name]' rotated. New key active. Old key valid until [datetime]." | Success | 5s |
| Key rotated (immediate) | "API key '[Name]' rotated. Old key immediately invalidated." | Warning | 5s |
| Key revoked | "API key '[Name]' revoked. Reason logged." | Warning | 4s |
| Revoked key still in use alert | "Security alert: Revoked key '[Name]' attempted authentication. Verify consuming system has been updated." | Error | 8s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No API keys | "No API Keys" | "No API keys have been created yet. Create a key to allow external systems to access EduForge APIs." | + Create API Key |
| No results for filter | "No Matching Keys" | "No API keys match the selected filters." | Clear Filters |
| All keys revoked or expired | "No Active Keys" | "All API keys are expired or revoked. Create a new key to restore integration access." | + Create API Key |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (15 rows) |
| Filter / search | Table skeleton shimmer |
| View drawer open | Drawer spinner; usage metrics section lazy-loads after base info |
| Create / rotate key submit | Full-screen overlay (key reveal UI) replaces spinner — appears immediately on success |
| Edit save | Button spinner |
| Revoke confirm | Button spinner "Revoking…" |

---

## 11. Role-Based UI Visibility

| Element | Integration Manager (G4) | IT Director (G4) | Cybersecurity Officer (G1) |
|---|---|---|---|
| + Create API Key | Visible | Hidden | Hidden |
| Edit Action | Visible | Hidden | Hidden |
| Rotate Action | Visible | Hidden | Hidden |
| Revoke Action | Visible | Hidden | Hidden |
| Key Hint (truncated) | Visible | Hidden | Hidden |
| Scope Details | Visible | Visible | Visible (status/expiry only) |
| Usage Metrics in View Drawer | Visible | Visible | Hidden |
| Rotation History | Visible | Visible | Hidden |
| IP Allowlist | Visible | Visible | Hidden |
| Export | Visible | Hidden | Hidden |

> Roles 54 (IT Admin), 55 (DPO), and 57 (IT Support Executive) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/api-keys/` | JWT (G4+) | Paginated API key list (no raw values) |
| POST | `/api/v1/it/api-keys/` | JWT (G4 — Integration Manager) | Create new API key; returns raw value once |
| GET | `/api/v1/it/api-keys/{id}/` | JWT (G4+) | Key detail (metadata + usage; no raw value) |
| PATCH | `/api/v1/it/api-keys/{id}/` | JWT (G4 — Integration Manager) | Update key metadata |
| POST | `/api/v1/it/api-keys/{id}/rotate/` | JWT (G4 — Integration Manager) | Rotate key; returns new raw value once |
| POST | `/api/v1/it/api-keys/{id}/revoke/` | JWT (G4 — Integration Manager) | Immediately revoke key |
| GET | `/api/v1/it/api-keys/kpis/` | JWT (G4+) | KPI card values |
| GET | `/api/v1/it/api-keys/{id}/usage/` | JWT (G4) | Usage stats (requests last 7d/30d, top IPs) |
| GET | `/api/v1/it/api-keys/{id}/rotation-history/` | JWT (G4) | Past rotation records |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/api-keys/kpis/` | `#kpi-bar` | `innerHTML` |
| Load API keys table | `load` | GET `/api/v1/it/api-keys/` | `#api-keys-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/api-keys/?status=...` | `#api-keys-table` | `innerHTML` |
| Search keys | `input` (300ms debounce) | GET `/api/v1/it/api-keys/?q=...` | `#api-keys-table` | `innerHTML` |
| Open view drawer | `click` on View | GET `/api/v1/it/api-keys/{id}/` | `#key-drawer` | `innerHTML` |
| Load usage metrics in drawer | `load` (lazy on drawer open) | GET `/api/v1/it/api-keys/{id}/usage/` | `#key-usage-section` | `innerHTML` |
| Submit create form | `click` on Create Key | POST `/api/v1/it/api-keys/` | `#key-reveal-overlay` | `innerHTML` |
| Submit rotate | `click` on Confirm Rotate | POST `/api/v1/it/api-keys/{id}/rotate/` | `#key-reveal-overlay` | `innerHTML` |
| Confirm revoke | `click` on Confirm Revoke | POST `/api/v1/it/api-keys/{id}/revoke/` | `#api-keys-table` | `innerHTML` |
| Dismiss reveal overlay | `click` on Dismiss (after checkbox) | — | `#key-reveal-overlay` | Remove element |
| Paginate table | `click` on page control | GET `/api/v1/it/api-keys/?page=N` | `#api-keys-table` | `innerHTML` |

---

**Audit Trail:** All write operations on this page (configuration saves, creates, updates, deletes, activations) are logged to the IT Audit Log with actor user ID, timestamp, and changed values.

**Notifications for Critical Events:**
- API key expiring < 7 days: Integration Manager (in-app amber + email) at 7 days, 1 day, and expiry
- Revoked key still generating requests: Integration Manager + IT Admin (in-app amber + email) immediately
- API key used from unallowlisted IP: Integration Manager + IT Director (in-app amber + email) immediately

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
