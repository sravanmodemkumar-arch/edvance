# Page 39: Device Policy Manager

**URL:** `/group/it/security/devices/`
**Roles:** Group Cybersecurity Officer (Role 56, G1) — read-only; Group IT Admin (Role 54, G4) — configure policy + manage devices
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Device policy definition and compliance tracking for all registered devices accessing the EduForge platform across all branches. This page serves two functions:

1. **Policy Configuration** (IT Admin only): Define which device types are permitted to access EduForge, minimum OS versions required, mandatory security apps, screen lock requirements, BYOD conditions, and VPN requirements for remote access.

2. **Compliance Tracking** (all roles): Monitor the device register — every device that has accessed or is registered to access EduForge is listed with its compliance status, last check date, and any issues found.

The Cybersecurity Officer (Role 56, G1) uses this page to monitor device compliance across branches and flag non-compliant or unregistered devices to the IT Admin. Enforcement actions (deregister, flag) require Role 54 (IT Admin).

This page enforces the principle that staff accessing student data must do so from secure, registered devices.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full access | Read + configure policy + flag + deregister devices |
| Group IT Director (Role 53, G4) | Read + export | Can view but cannot edit policy |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | Can view policy and table; cannot modify |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > Cybersecurity > Device Policy Manager`

**Page Header:**
- Title: `Device Policy Manager`
- Subtitle: `Device compliance policy and registered device register across all branches`
- Right side: `Export Device Register (CSV)` button (Role 54/53 only)
- `Last Updated: [timestamp]`

**Alert Banners:**

1. **Unregistered Devices Detected** (amber, dismissible per session):
   - Condition: any device in the register with status = Unregistered
   - Text: `[X] unregistered devices have accessed the portal. Review and register or block these devices.`

2. **Policy Change Pending Review** (blue, informational):
   - Condition: policy was changed in last 7 days
   - Text: `Device policy was last updated [X] days ago by [Actor Name]. Notify branches of updated requirements.`

**Page Structure:**
1. Policy Configuration Panel (top section, collapsible)
2. KPI Summary Bar (4 cards)
3. Device Register Table (main content)
4. Charts (bottom section)

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Total Devices | Count of all records in device register | Plain number |
| 2 | Compliant | Count where compliance_status = Compliant | Number, green badge |
| 3 | Non-Compliant | Count where compliance_status = Non-Compliant | Number, red if > 0 |
| 4 | Unregistered | Count where compliance_status = Unregistered (accessed portal without registration) | Number, amber if > 0 |

---

## 5. Main Table — Device Register

**Table Title:** `Registered Device Register`
**Description:** Every device that has accessed or attempted to access EduForge across all branches.

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Device Name/ID | Text | Unique device identifier or friendly name |
| User | Text | Masked (format: `J*** D***`) for Role 56; full name for Role 54/53 |
| Branch | Text | Branch the device/user belongs to |
| Device Type | Badge | Mobile / Desktop / Tablet |
| OS | Text | e.g., Android 13, iOS 17.2, Windows 11, macOS 14 |
| Compliance Status | Badge | Compliant (green) / Non-Compliant (red) / Unregistered (amber) |
| Last Check Date | Date | When compliance was last verified |
| Issues Found | Text | Brief description of non-compliance reason, or `—` if compliant |
| Actions | Buttons | `View` / `Flag` (Role 54 only) / `Deregister` (Role 54 only) |

### Filters

- **Branch:** Multi-select dropdown
- **Device Type:** All / Mobile / Desktop / Tablet
- **OS:** All / Android / iOS / Windows / macOS
- **Compliance Status:** All / Compliant / Non-Compliant / Unregistered
- **Issues Found:** Toggle — `Show devices with issues only`

### Search

Search on device name/ID or user name (masked for Role 56). `hx-trigger="keyup changed delay:400ms"`, targets `#device-table`.

### Pagination

Server-side, 25 rows per page. `hx-get="/group/it/security/devices/table/?page=N"`, targets `#device-table`.

### Sorting

Sortable: Last Check Date, Compliance Status, Branch, Device Type. Default sort: Compliance Status (Non-Compliant first, then Unregistered, then Compliant).

---

## 6. Drawers

### A. Policy Configuration Panel (Top of Page — IT Admin Only)

This is not a drawer but an inline collapsible panel (accordion). Collapsed by default; expanded with `Edit Policy` button.

**Panel Header:** `Device Access Policy` — `Last Updated: [date] by [actor]` — `Edit Policy` button (Role 54 only)

**Policy Fields (when in Edit mode — Role 54 only):**

| Field | Type | Options |
|-------|------|---------|
| Allowed OS: Android | Toggle + Min Version | Toggle enabled/disabled; if enabled: minimum version text input |
| Allowed OS: iOS | Toggle + Min Version | Toggle + min version |
| Allowed OS: Windows | Toggle + Min Version | Toggle + min version |
| Allowed OS: macOS | Toggle + Min Version | Toggle + min version |
| Screen Lock Required | Toggle | Yes / No |
| Antivirus Required | Toggle | Yes / No |
| VPN Required for Remote Access | Toggle | Yes / No |
| BYOD Permitted | Toggle + Conditions | Yes/No; if Yes: conditions text area (e.g., "Must register device, must have antivirus") |

**Save Policy** button — saves with `hx-post`, shows confirmation toast. Change is logged to IT Audit Log automatically.

**View mode (Role 56/53):** Same fields rendered as read-only key-value pairs.

---

### B. View Device Drawer (440px, right-side)

Triggered by `View` button in table. Read-only for all roles.

**Fields:**
- Device ID / Name
- Assigned User (unmasked for Role 54; masked for Role 56)
- Branch
- Device Type
- Operating System (version)
- Compliance Status (badge)
- Registration Date
- Last Check Date
- Issues Found (full list)
- Check History: last 5 compliance checks (date, status, issues)

**Footer:** `Close` button. `Flag Device` button (Role 54 only).

---

### C. Flag Device Drawer (440px, right-side)

Triggered by `Flag` button (Role 54 only).

**Fields:**
- Device: [Device ID — read-only]
- Flag Reason (dropdown): Non-compliant OS / Missing antivirus / No screen lock / Suspicious activity / BYOD policy violation / Other
- Details (textarea, required)
- Action to Take (radio): Notify user only / Block device access / Deregister device
- Notify User via: WhatsApp / Email / Both

**Footer:** `Submit Flag` / `Cancel`

On submit: `hx-post="/group/it/security/devices/flag/"`. Device compliance status updates. Toast: `Device [ID] flagged. User notified.`

---

### D. Deregister Device Drawer (440px, right-side)

Triggered by `Deregister` button (Role 54 only).

**Confirmation dialog with:**
- Device: [Device ID — read-only]
- Warning: `Deregistering this device will block its access to EduForge. The user will need to re-register.`
- Reason for Deregistration (textarea, required)
- Confirm checkbox: `I confirm I want to deregister this device`

**Footer:** `Confirm Deregister` (red button) / `Cancel`

On submit: `hx-delete="/group/it/security/devices/{device_id}/"`. Toast: `Device deregistered. Access blocked.`

---

### E. How Devices Enter the Register — Auto-Detection and Manual Registration

**Auto-detection (primary method):** Every time a staff or admin user logs in to EduForge, the platform captures the device fingerprint (browser user-agent, OS version, device type, and a persistent browser cookie). If this device fingerprint has not been seen before for this user, the platform automatically creates a new entry in the device register with status "Unregistered". The IT Admin sees this as an Unregistered device and must review it. Auto-detection requires no action from the end user.

**Manual registration (supplementary):**

The `+ Register Device` button (IT Admin only, top-right of Device Register table) opens a manual registration drawer:

**Drawer: `device-register` — Register Device (440px)**
- **Fields:**
  - User (required, searchable dropdown — from User Directory)
  - Device Name / Label (required, text — e.g., "John's iPhone", "Lab Desktop 3")
  - Device Type (required, radio: Mobile / Desktop / Tablet)
  - OS (required, dropdown: Android / iOS / Windows / macOS / Other)
  - OS Version (required, text input)
  - Device Serial / IMEI (optional, text — for corporate devices)
  - Registration Source (radio: Corporate-issued / BYOD — personal)
  - Branch (required, dropdown — defaults to user's branch)
  - Compliance Status Initial Assessment (radio: Compliant — meets all policy requirements / Non-Compliant — flag immediately)
  - Notes (optional, textarea)
- **Footer:** Register Device / Cancel
- **On submit:** Device record created with status based on Compliance Status field; audit log entry written; toast: "Device registered for [User Name]."

### F. Edit Device Drawer (440px, right-side — Role 54 only)

Triggered by `Edit` button on a registered device row (Role 54 only).

**Fields:**
- Device Name / Label (text, editable)
- OS Version (text, editable)
- Branch (dropdown, editable)
- Compliance Status (radio: Compliant / Non-Compliant)
- Notes (textarea, optional)

**Footer:** `Update Device` / `Cancel`

**On submit:** `hx-put="/api/v1/it/security/devices/{device_id}/"` — device record updated. Toast: `Device [ID] updated.`

**Audit:** Device record edits are logged to the IT Audit Log.

---

## 7. Charts

Two charts rendered below the main table in a 2-column grid.

### Chart 1: Device OS Distribution
- **Type:** Donut chart
- **Segments:** Android, iOS, Windows, macOS, Other
- **Centre label:** Total device count
- **Purpose:** Identify which OS platforms dominate the device fleet — informs policy priority
- **Data endpoint:** `/api/v1/it/security/devices/charts/os-distribution/`

### Chart 2: Compliance Trend (6 Months)
- **Type:** Line chart (3 series)
- **Series:** Compliant (green), Non-Compliant (red), Unregistered (amber)
- **X-axis:** Last 6 months
- **Y-axis:** Device count
- **Purpose:** Track whether compliance is improving after policy enforcement actions
- **Filter:** Branch multi-select (optional)
- **Data endpoint:** `/api/v1/it/security/devices/charts/compliance-trend/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Policy saved successfully | Success: `Device access policy updated and saved. Change logged to IT Audit Log.` |
| Policy save failed (validation) | Error: `Please complete all required policy fields.` |
| Device registered (manual) | Success: `Device registered for [User Name]. Compliance status: [Compliant/Non-Compliant].` |
| Device flagged | Success: `Device [ID] flagged. User notified via [channel].` |
| Device deregistered | Success: `Device [ID] deregistered. Portal access blocked.` |
| CSV export initiated | Info: `Exporting device register — please wait.` |
| Flag failed | Error: `Failed to flag device. Please try again.` |
| Device updated | Success: `Device [ID] updated successfully.` | Success | 3s |
| Device update failed | Error: `Failed to update device record. Please try again.` | Error | 5s |

---

**Audit Trail:** All device policy changes, device registrations, flagging actions, and deregistrations are logged to the IT Audit Log with IT Admin user ID and timestamp.

**Notifications for Critical Events:**
- Device flagged (Suspicious Activity): Cybersecurity Officer (in-app amber + email) + IT Director (email)
- Large number of unregistered devices (> 20): IT Admin (in-app amber + email)
- Device deregistered: Branch contact notified via email (if "Action to Take = Block device access")

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No devices registered | Icon + `No devices registered. Devices appear here when staff first access EduForge.` |
| No devices match filters | `No devices match the selected filters. Try adjusting your search.` |
| Policy not yet configured | Policy panel shows: `Device access policy has not been configured. [Edit Policy] to get started.` (Role 54) or `Policy not configured. Contact IT Admin.` (Role 56) |
| Chart insufficient data | `Insufficient data to display trend. Check back after devices are registered.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI cards | 4 skeleton shimmer cards |
| Device table | 5 skeleton rows with shimmer |
| Policy panel (on open) | Spinner while loading current policy values |
| Charts | Spinner centred in chart container |
| Flag/Deregister drawers | Spinner in button during submit |

---

## 11. Role-Based UI Visibility

| UI Element | Role 56 (G1) | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|-------------|
| Policy panel | Visible, read-only | Visible + Edit Policy button | Visible, read-only |
| Edit Policy button | Hidden | Visible | Hidden |
| Device table | Visible (user masked) | Visible (user unmasked) | Visible (user unmasked) |
| View button | Visible | Visible | Visible |
| Flag button | Hidden | Visible | Hidden |
| Deregister button | Hidden | Visible | Hidden |
| Export CSV button | Hidden | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/security/devices/policy/` | Fetch current device policy config |
| PUT | `/api/v1/it/security/devices/policy/` | Update device policy (Role 54 only) |
| GET | `/api/v1/it/security/devices/` | Fetch device register (paginated) |
| GET | `/api/v1/it/security/devices/{device_id}/` | Fetch single device detail |
| POST | `/api/v1/it/security/devices/flag/` | Flag a device (Role 54 only) |
| DELETE | `/api/v1/it/security/devices/{device_id}/` | Deregister device (Role 54 only) |
| GET | `/api/v1/it/security/devices/export/csv/` | Export device register as CSV |
| GET | `/api/v1/it/security/devices/charts/os-distribution/` | OS distribution data |
| GET | `/api/v1/it/security/devices/charts/compliance-trend/` | Compliance trend (6 months) |
| PUT | `/api/v1/it/security/devices/{device_id}/` | JWT (G4) | Update device record (name, OS, branch, compliance status) |

**Query Parameters (device table):**
- `page`, `page_size` (default 25)
- `branch_id`, `device_type`, `os`, `compliance_status`
- `has_issues` (bool)
- `search` (device name or user)
- `sort_by`, `sort_dir`

---

## 13. HTMX Patterns

```html
<!-- Policy panel edit toggle -->
<button hx-get="/group/it/security/devices/policy/edit-form/"
        hx-target="#policy-panel-content"
        hx-swap="innerHTML">
  Edit Policy
</button>

<!-- Save policy -->
<form hx-put="/group/it/security/devices/policy/"
      hx-target="#policy-panel-content"
      hx-swap="innerHTML">
  <!-- policy fields -->
  <button type="submit">Save Policy</button>
</form>

<!-- Device table load -->
<div id="device-table"
     hx-get="/group/it/security/devices/table/"
     hx-trigger="load"
     hx-target="#device-table"
     hx-include="#device-filter-form">
</div>

<!-- Search with debounce -->
<input type="text" name="search"
       hx-get="/group/it/security/devices/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#device-table"
       hx-include="#device-filter-form" />

<!-- Flag device drawer -->
<button hx-get="/group/it/security/devices/{{ device.id }}/flag-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Flag
</button>

<!-- Flag submit -->
<form hx-post="/group/it/security/devices/flag/"
      hx-target="#device-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); showToast('Device flagged.')">
  <!-- flag fields -->
</form>

<!-- Deregister -->
<form hx-delete="/group/it/security/devices/{{ device.id }}/"
      hx-target="#device-table"
      hx-swap="outerHTML"
      hx-confirm="Deregister this device? This will block portal access."
      hx-on::after-request="closeDrawer()">
  <button type="submit" class="btn-danger">Confirm Deregister</button>
</form>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
