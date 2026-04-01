# 08 — Branch Portal Config Editor

- **URL:** `/group/it/portals/{id}/config/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Branch Portal Config Editor is the per-branch detailed configuration page. It is accessed from the Branch Portal Manager by clicking "Configure" on any portal row. Unlike the Branch Portal Manager (which gives a group-wide overview), this page is entirely scoped to a single branch portal — every setting on this page applies only to the branch identified in the URL path parameter `{id}`.

This is a settings page, not a table page. It follows a left navigation tabs + right content panel layout pattern, similar to a product settings page. The left nav lists 7 configuration tabs; the right panel renders the active tab's content. This design reduces cognitive load by grouping related settings together and preventing the page from becoming a single overwhelming scroll.

All changes on this page are saved via HTMX PATCH requests and are immediately logged to the IT Audit Log with the IT Admin's user ID, timestamp, changed fields (before/after values), and a plain-English description of the change (e.g., "Feature 'Mock Test Engine' enabled for Narayan-Hyderabad portal"). This audit trail is critical for compliance and for debugging configuration issues raised through IT support tickets.

The "Danger Zone" tab is intentionally separated from functional configuration tabs and uses a visually distinct red border section to prevent accidental destructive actions. All Danger Zone actions require an explicit text confirmation.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + edit all 7 tabs | Primary role |
| Group IT Director | G4 | Full read across all tabs | Cannot save changes — view-only |
| Group EduForge Integration Manager | G4 | Read + edit Integrations tab only | Cannot edit other tabs |
| Group IT Support Executive | G3 | Read-only (General Settings tab only) | Cannot view Danger Zone or edit any tab |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Branch Portal Manager → [Branch Name] → Portal Config
```

### 3.2 Page Header
- **Title:** `Portal Configuration — [Branch Name]`
- **Subtitle:** `Portal: [portal-slug].eduforge.in · Status: [Status Badge] · Last modified: [relative datetime] by [user name]`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `View Audit Log` · `Back to Portal Manager` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Portal status = Suspended | "This portal is currently suspended. Users cannot access it." | Red (non-dismissible while suspended) |
| Unsaved changes exist on current tab | "You have unsaved changes. Save before switching tabs or your changes will be lost." | Amber (dismissible; also shown as modal on tab switch) |
| WhatsApp API key invalid or expired | "WhatsApp API key is invalid or expired. Parent notifications are currently failing for this branch." | Red |
| SSL certificate expiring < 30 days | "SSL certificate for [custom domain] expires in [N] days. Renew via the Domain Manager." | Amber |

---

## 4. KPI Summary Bar

No KPI Summary Bar on this settings page. The header subtitle provides the essential status signals (portal status, last modified). Full KPI monitoring is available on the IT Director and IT Admin dashboards.

---

## 5. Main Table

No main table on this settings page. The page is organised as a tabbed settings editor (see Section 3 for layout description). Each tab is detailed in Section 6.

---

## 6. Configuration Tabs (Settings Sections)

**Audit Trail:** Every field change across all 7 tabs is logged to IT Audit Log including user ID, timestamp, field name, before/after values, and a plain-English change summary (e.g., "Feature Mock Test Engine enabled for [Branch] portal").

### Tab 1 — General Settings
- **Purpose:** Core portal identity and operational settings
- **Fields:**
  - Portal Name: text input (displayed in the branch portal header and browser title)
  - Portal Slug: text input (read-only after activation; shows note "Cannot change slug on an active portal without IT Director approval" + `Request Slug Change` link button). Clicking "Request Slug Change" opens a modal:
    - **Modal: `slug-change-request` (440px):** Title "Request Portal Slug Change". Fields: Proposed New Slug (text input, unique-validated), Reason for Change (required, textarea min 30 chars), Impact Acknowledgement (checkbox: "I understand changing the slug will break existing bookmarks and any hardcoded links to this portal"). On submit: creates an IT Director approval request; toast "Slug change request submitted for IT Director approval. Current slug remains active until approved." The request appears in the IT Director's policy approval queue (page 01) and on the Role Permission Matrix pending approvals.
    - **API:** `POST /api/v1/it/portals/{id}/request-slug-change/` — creates approval request
  - Primary Contact Name: text input (branch principal or IT admin contact name)
  - Primary Contact Email: email input (used for system notifications)
  - Timezone: dropdown (IST default; all 30 Indian timezones listed)
  - Academic Year Start: month select (April default)
  - Language / Locale: dropdown (English IN default; Hindi available)
  - Portal Description: textarea (internal notes — not visible to branch users)
- **Save:** HTMX PATCH to `/api/v1/it/portals/{id}/general/`

### Tab 2 — Feature Toggles
- **Purpose:** Control which EduForge features are enabled for this branch
- **Layout:** Grid of feature cards, 3 per row on desktop. Each card shows: Feature Name, Category badge, brief description, On/Off toggle switch, "Overriding group default" indicator (amber badge if this branch's setting differs from the group-level default)
- **Feature categories:** Academic / Communication / Finance / Admin / AI
- **Group Default indicator:** Each feature shows whether the current value matches the group default. IT Admin can reset individual features to group default.
- **Save:** Batch HTMX PATCH to `/api/v1/it/portals/{id}/features/` — all toggle states sent in one request
- **Note:** Features requiring IT Director approval (e.g., AI Question Generator, Advanced Analytics) are greyed out with a lock icon. IT Admin must submit a policy change request; cannot enable directly.

### Tab 3 — User Roles
- **Purpose:** Assign key operational roles for this specific branch within EduForge
- **Fields (each is a user-search select):**
  - Branch Principal: user assigned as the top-level authority for this branch portal
  - Branch IT Admin: branch-level IT contact (different from Group IT Admin)
  - Branch Accountant: user with access to branch finance modules
  - Branch HR Lead: user with access to branch HR modules
  - Branch Exam Coordinator: user with access to exam and results modules
- **Each role shows:** Currently assigned user (name, email, last login date), Remove Assignment button, Re-assign button
- **Save:** Each role assignment saves individually on change (auto-save with HTMX PATCH); no separate Save button needed

### Tab 4 — Notifications
- **Purpose:** Configure notification delivery channels and triggers for this branch
- **WhatsApp section:**
  - API Provider: select (Meta Business API / Twilio / Gupshup)
  - Business Phone Number ID: text input
  - API Access Token: password input with show/hide toggle (value stored encrypted in PostgreSQL)
  - Test Connection button → HTMX POST to test API credentials, shows success or error inline
  - Notification triggers (per-trigger toggles): New Admission Confirmation / Fee Due Reminder / Exam Result Published / Attendance Alert / Emergency Broadcast
  - Frequency caps: max notifications per student per day (integer input)
- **Email section:**
  - Custom From Email: email input (e.g., `admissions@narayanahyd.com`) — optional override
  - Reply-To Email: email input
- **Save:** HTMX PATCH to `/api/v1/it/portals/{id}/notifications/`

### Tab 5 — Integrations
- **Purpose:** View and manage which integrations are active for this specific branch
- **Layout:** Read-only list of all active integrations for this branch (fetched from Integration Registry), with toggle to enable/disable per integration for this branch
- **Columns:** Integration Name, Type badge, Status, Last Health Check, Enable/Disable toggle for this branch
- **SSO Configuration summary:** Shows current SSO status (Active / Not Configured) with link to Integration Manager for editing SSO config
- **Note:** Creating new integrations is done via the Integration Manager dashboard, not here. This tab is for activating/deactivating existing group integrations at the branch level.
- **Save:** HTMX PATCH to `/api/v1/it/portals/{id}/integrations/`

### Tab 6 — Branding
- **Purpose:** Upload and manage visual branding for this branch portal
- **Fields:**
  - Portal Logo: file upload (PNG or SVG, max 2MB) with live preview. Current logo shown. Upload via POST to Cloudflare R2; URL stored in PostgreSQL.
  - Favicon: file upload (ICO or PNG 32x32) with preview
  - Primary Brand Colour: hex colour picker with real-time preview swatch
  - Secondary Brand Colour: hex colour picker
  - Custom CSS: textarea (max 10,000 characters; G4 only; full-page CSS injected into the branch portal's `<head>`) with a warning: "Custom CSS is applied after default styles. Incorrect CSS may break the portal layout."
  **Clear Custom CSS:** A "Clear CSS" button lets IT Admin remove injected CSS without affecting logo or colours. Clearing and saving logs the change to IT Audit Log.
  - Brand Preview Panel: live preview of the branch portal's header/nav bar rendered with the selected colours and logo — updates as colours change
- **Save:** HTMX PATCH to `/api/v1/it/portals/{id}/branding/` (logo upload is a separate HTMX POST with `hx-encoding="multipart/form-data"`)

### Tab 7 — Danger Zone
- **Purpose:** Irreversible or disruptive portal operations — visually separated with red border
- **Layout:** Red-bordered section. Each action is in its own card with a clear warning label.
- **Actions available:**
  - **Deactivate Portal:** Red outline button. Confirmation modal: type the portal slug to confirm. Sends IT Director notification. Sets status = Inactive.
  - **Reset to Defaults:** Warning button. Resets all feature toggles to the current group defaults. Does not affect user data. Confirmation modal required.
  - **Archive Portal:** Removes portal from active list. Portal data is retained in PostgreSQL but portal is inaccessible. Requires IT Director approval (submits an approval request rather than acting immediately). Cannot be undone without IT Director approval.
- **G4 only:** All Danger Zone actions are hidden for G3 and below. IT Director can view but not initiate (they approve, IT Admin initiates).

**Notifications:**
- Portal deactivation/reset/archive requests: IT Director notified via email immediately; portal deactivation also sends email to branch contact if available.

---

## 7. Charts

No charts on this settings page. Configuration changes are tracked in the IT Audit Log, accessible via the "View Audit Log" link in the page header.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| General settings saved | "General settings updated for [Branch Name]." | Success | 4s |
| Feature toggles saved | "Feature settings saved." | Success | 4s |
| Role assignment saved | "[Role] assigned to [User Name]." | Success | 3s |
| Notification config saved | "Notification settings saved." | Success | 4s |
| WhatsApp test: success | "WhatsApp API connection successful. Credentials are valid." | Success | 5s |
| WhatsApp test: failure | "WhatsApp API connection failed: [Error]. Check your credentials." | Error | 7s |
| Branding saved | "Branding updated. Changes are live on the branch portal." | Success | 4s |
| Logo uploaded | "Logo uploaded and applied." | Success | 3s |
| Logo file too large | "File size exceeds 2MB. Please compress your image and try again." | Error | 5s |
| Logo file wrong format | "Invalid file format. PNG or SVG only." | Error | 5s |
| Portal deactivated | "[Branch Name] portal deactivated." | Warning | 5s |
| Reset to defaults | "All feature toggles reset to group defaults." | Info | 5s |
| Save error | "Failed to save changes. Please check your input." | Error | 6s |
| Notification config save error | Error: `Failed to save notification settings. Verify API credentials and try again.` | Error | 6s |
| Unsaved changes warning on tab switch | Modal: "You have unsaved changes on this tab. Save them before switching?" — Save + Stay / Discard + Switch | — | Modal (no auto-dismiss) |
| Slug change request submitted | "Slug change request submitted for IT Director approval." | Info | 5s |
| Slug change approved (IT Director) | "Portal slug changed to [new-slug]. All portal URLs have been updated." | Success | 6s |

---

## 9. Empty States

| Condition | Heading | Description |
|---|---|---|
| No integrations configured for branch | "No Active Integrations" (in Integrations tab) | "No integrations have been enabled for this branch. Configure integrations via the Integration Manager." |
| No logo uploaded | "Default Logo" (in Branding tab) | Shows EduForge placeholder logo with prompt to upload a custom logo. |
| No roles assigned | "No User Assigned" (per role in User Roles tab) | Shows "Unassigned" badge with Assign button next to each role. |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Left nav loads immediately; right panel shows tab-content shimmer while first tab data fetches |
| Tab switch | Right panel shimmer (300ms) while new tab content loads via HTMX GET |
| Save action (any tab) | Save button spinner + form fields disabled until response |
| WhatsApp test connection | Test button spinner + "Testing connection…" inline label for up to 5s |
| Logo upload | Upload progress bar (uses `hx-on::xhr:progress` HTMX event); preview updates on completion |
| Brand colour preview | Immediate CSS variable update (client-side only, no loader needed) |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | Integration Manager (G4) | IT Support Executive (G3) |
|---|---|---|---|---|
| Left Nav — all 7 tabs | Visible | Visible | Integrations tab only | General Settings tab only |
| General Settings | Editable | Read-only | Hidden | Read-only |
| Feature Toggles | Editable | Read-only | Hidden | Hidden |
| User Roles | Editable | Read-only | Hidden | Hidden |
| Notifications | Editable | Read-only | Hidden | Hidden |
| Integrations | Editable | Read-only | Editable (own integrations only) | Hidden |
| Branding | Editable | Read-only | Hidden | Hidden |
| Danger Zone tab | Visible + actionable | Visible (read-only — can approve, not initiate) | Hidden | Hidden |
| View Audit Log button | Visible | Visible | Visible (integrations only) | Hidden |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403). All UI elements hidden.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/portals/{id}/` | JWT (G4) | Load portal metadata for header (name, status, last modified) |
| GET | `/api/v1/it/portals/{id}/general/` | JWT (G4) | Load General Settings tab data |
| PATCH | `/api/v1/it/portals/{id}/general/` | JWT (G4) | Save General Settings |
| GET | `/api/v1/it/portals/{id}/features/` | JWT (G4) | Load Feature Toggles tab data |
| PATCH | `/api/v1/it/portals/{id}/features/` | JWT (G4) | Batch save feature toggle states |
| GET | `/api/v1/it/portals/{id}/roles/` | JWT (G4) | Load User Roles tab data |
| PATCH | `/api/v1/it/portals/{id}/roles/{role_key}/` | JWT (G4) | Assign a user to a portal role |
| GET | `/api/v1/it/portals/{id}/notifications/` | JWT (G4) | Load Notifications tab data |
| PATCH | `/api/v1/it/portals/{id}/notifications/` | JWT (G4) | Save notification config |
| POST | `/api/v1/it/portals/{id}/notifications/test-whatsapp/` | JWT (G4) | Test WhatsApp API connection |
| GET | `/api/v1/it/portals/{id}/integrations/` | JWT (G4) | Load Integrations tab data |
| PATCH | `/api/v1/it/portals/{id}/integrations/` | JWT (G4) | Enable/disable integrations for branch |
| GET | `/api/v1/it/portals/{id}/branding/` | JWT (G4) | Load Branding tab data |
| PATCH | `/api/v1/it/portals/{id}/branding/` | JWT (G4) | Save branding settings (colours, custom CSS) |
| POST | `/api/v1/it/portals/{id}/branding/logo/` | JWT (G4) | Upload logo file to Cloudflare R2 |
| POST | `/api/v1/it/portals/{id}/deactivate/` | JWT (G4) | Deactivate portal (Danger Zone) |
| POST | `/api/v1/it/portals/{id}/reset-defaults/` | JWT (G4) | Reset feature toggles to group defaults |
| POST | `/api/v1/it/portals/{id}/archive/` | JWT (G4) | Submit archive request (pending IT Director approval) |
| POST | `/api/v1/it/portals/{id}/request-slug-change/` | JWT (G4) | Submit slug change request for IT Director approval |
| GET | `/api/v1/it/users/search/?q={query}&role_min_level={level}` | JWT (G4) | Search available users for role assignment in Tab 3 |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load initial tab (General Settings) | `load` | GET `/api/v1/it/portals/{id}/general/` | `#tab-content` | `innerHTML` |
| Switch to any tab | `click` on left nav tab | GET `/api/v1/it/portals/{id}/{tab-key}/` | `#tab-content` | `innerHTML` |
| Save General Settings | `click` on Save | PATCH `/api/v1/it/portals/{id}/general/` | `#general-save-result` | `innerHTML` |
| Save Feature Toggles | `click` on Save Features | PATCH `/api/v1/it/portals/{id}/features/` | `#features-save-result` | `innerHTML` |
| Assign role (auto-save) | `change` on role select | PATCH `/api/v1/it/portals/{id}/roles/{role_key}/` | `#role-{role_key}-status` | `outerHTML` |
| Test WhatsApp connection | `click` on Test Connection | POST `/api/v1/it/portals/{id}/notifications/test-whatsapp/` | `#whatsapp-test-result` | `innerHTML` |
| Save Notifications | `click` on Save | PATCH `/api/v1/it/portals/{id}/notifications/` | `#notifications-save-result` | `innerHTML` |
| Upload logo | `change` on logo file input | POST `/api/v1/it/portals/{id}/branding/logo/` (multipart) | `#logo-preview` | `innerHTML` |
| Save Branding | `click` on Save Branding | PATCH `/api/v1/it/portals/{id}/branding/` | `#branding-save-result` | `innerHTML` |
| Confirm deactivate | `click` on Confirm Deactivate | POST `/api/v1/it/portals/{id}/deactivate/` | `#danger-zone-result` | `innerHTML` |
| Confirm reset defaults | `click` on Confirm Reset | POST `/api/v1/it/portals/{id}/reset-defaults/` | `#features-grid` | `innerHTML` |
| Unsaved changes tab-switch warning | `click` on left nav (if dirty form) | JS intercept before HTMX fires; shows modal | — | — |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
