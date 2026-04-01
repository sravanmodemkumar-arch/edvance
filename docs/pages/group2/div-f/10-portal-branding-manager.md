# 10 — Portal Branding Manager

- **URL:** `/group/it/portals/branding/`
- **Template:** `portal_base.html`
- **Priority:** P2
- **Role:** Group IT Admin (Role 54, G4)

---

## 1. Purpose

The Portal Branding Manager provides centralised control over the visual branding of every branch portal in the group. Each branch portal can have its own distinct visual identity — custom logo, primary and secondary brand colours, and favicon — while still running on the same EduForge platform. This supports multi-brand education groups where individual branches may operate under different school names or carry their own local brand identity.

Brand assets are stored in Cloudflare R2 at the path `/static/tenants/{branch_slug}/`, ensuring fast CDN delivery to students and parents loading the portal. File metadata (file names, R2 paths, upload timestamps, uploader user IDs) are stored in PostgreSQL. The actual file bytes are never stored in the application database.

The page provides a management table showing each branch's current branding status, with quick one-click access to the Edit Branding drawer for any branch. For branches still using default EduForge branding, the table makes this clearly visible so the IT Admin can prioritise branding setup during branch onboarding. A live preview panel within the Edit Branding drawer allows the IT Admin to see exactly how the portal header will look with the selected logo and colours before saving.

This page also exposes a `brand.json` concept — a structured JSON representation of the branch's brand tokens (primary colour, secondary colour, font family, logo URL, favicon URL) that can be consumed by the portal's Tailwind CSS configuration at build time or at runtime via CSS custom properties. The IT Admin does not need to write JSON manually; it is generated automatically from the form inputs.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group IT Admin | G4 | Full read + upload logos + set brand colours | Primary role |
| Group IT Director | G4 | Read-only | Can view branding status; cannot upload or edit |
| Group IT Support Executive | G3 | Read-only | Branch name, logo status, last updated columns only |
| Group EduForge Integration Manager | G4 | Read-only | No branding-related authority |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group Cybersecurity Officer (Role 56, G1) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Branch Portal Manager → Branding Manager
```

### 3.2 Page Header
- **Title:** `Portal Branding Manager`
- **Subtitle:** `[Branches with Custom Logo] of [Total Portals] branches have custom branding configured`
- **Role Badge:** `Group IT Admin`
- **Right-side controls:** `Export Branding Status (CSV)` · `Notification Bell`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Logo file for a branch returning 404 from R2 | "Logo for [Branch Name] is not loading. The R2 file may have been deleted. Re-upload required." | Red |
| Branch portal active with no branding configured | "[N] active portal(s) are using default EduForge branding. Consider adding branch-specific branding." | Info (dismissible) |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Branches with Custom Logo | Count of branches with a non-default logo uploaded to R2 | Blue (informational) | Filters table to "Logo Uploaded" |
| Branches with Brand Config | Count of branches with at least primary colour set (non-default) | Blue (informational) | Filters table to "Brand Colour Set = Yes" |
| Branches Using Default Branding | Count of branches with no custom logo and no custom colours | Blue (informational) | Filters table to fully default branches |

---

## 5. Main Table — Branch Branding Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch Name | Text | Yes | Yes (multi-select) |
| Portal Slug | Text (monospace, small) | No | No |
| Logo Status | Badge: Uploaded (green) / Default (grey) | No | Yes (Uploaded / Default) |
| Brand Colour Set | Badge: Yes (green) / No (grey) | No | Yes (Yes / No) |
| Last Updated | Relative datetime (or "Never" if default) | Yes | Yes (date range) |
| Preview | Inline mini-preview of the branch logo (thumbnail 40×40px) or EduForge default logo placeholder | No | No |
| Actions | `Edit Branding` · `Reset to Default` icon buttons | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Logo Status | Checkbox | Uploaded / Default |
| Brand Colour Set | Checkbox | Yes / No |
| Last Updated | Date range picker | From / To |
| Branding Complete (logo + colour set) | Toggle switch | Show only complete / Show only incomplete |

### 5.2 Search
- Full-text: Branch name, portal slug
- 300ms debounce, triggers HTMX GET with `?search=` query param

### 5.3 Pagination
- Server-side · 20 rows/page · Shows total count

---

## 6. Drawers

### 6.1 Drawer: `branding-edit` — Edit Branding
- **Trigger:** Actions → Edit Branding on any row
- **Width:** 480px
- **Layout:** Form fields on left 60% + live preview panel on right 40% (vertical stack on narrow screens)
- **Fields:**
  - **Current Logo:** Thumbnail of current logo (or default placeholder). File path shown below.
  - **Upload New Logo:** File input (`accept=".png,.svg"`). Validation: max 2MB, PNG or SVG only. On file select, preview updates immediately via JS FileReader (client-side preview before upload). Upload triggered on form save, not on file select, to avoid unnecessary R2 writes.
  **Remove Logo:** Logo field includes a "Remove Logo" button to clear the logo without affecting colours. Favicon field has a separate "Remove Favicon" button.
  - **Upload Favicon:** File input (`accept=".ico,.png"`). Max 100KB. PNG 32×32 or ICO format.
  - **Primary Brand Colour:** Hex colour picker with manual hex input field. Defaults to current value or EduForge blue `#1E40AF`.
  - **Secondary Brand Colour:** Hex colour picker with manual hex input field. Defaults to current value or EduForge grey `#6B7280`.
  - **Live Preview Panel:** Renders a static HTML snippet of the portal's top navigation bar using the currently-selected logo and colours (CSS custom properties updated client-side in real time as colours change). Shows: Logo left, nav links in primary colour, page title area in secondary colour, so the IT Admin can judge contrast and readability.
  - **brand.json Preview (collapsible):** Read-only JSON block showing the auto-generated brand.json that will be applied to the portal on save.
- **Save Changes button:** PATCH for colour/text fields → R2 POST for files → then PATCH to update PostgreSQL with new R2 URLs
- **Note:** If only colours are being changed (no new files), only the PATCH endpoint is called. Files are only uploaded to R2 on explicit file selection + save.

### 6.2 Modal: `branding-reset` — Reset to Default
- **Trigger:** Actions → Reset to Default
- **Width:** 400px
- **Content:** "You are about to reset [Branch Name]'s branding to the EduForge default. The custom logo and brand colours will be removed. The R2 files will be retained for 30 days before deletion. This action is reversible within 30 days." · Confirm Reset · Cancel
- **On confirm:** PATCH sets logo_url and colours to null (portal reverts to EduForge default). R2 files are soft-deleted (flagged for deletion after 30 days).

**Audit Trail:** All branding changes are logged to IT Audit Log: user ID, timestamp, field changed (logo/primary colour/secondary colour/favicon), old and new values, branch identifier.

---

## 7. Charts

No charts on this page. The 3-card KPI bar provides the aggregate branding adoption view. Branding is a configuration attribute, not a time-series metric.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Branding saved (no file upload) | "Brand colours updated for [Branch Name]." | Success | 4s |
| Logo uploaded and saved | "Logo uploaded and applied to [Branch Name] portal." | Success | 4s |
| Favicon uploaded and saved | "Favicon updated for [Branch Name]." | Success | 4s |
| Reset to default | "[Branch Name] branding reset to EduForge default." | Info | 4s |
| File too large | "File exceeds the [2MB / 100KB] size limit. Please compress the file and try again." | Error | 5s |
| Invalid file type | "Invalid file type. [PNG or SVG / ICO or PNG] files only." | Error | 5s |
| R2 upload failure | "Logo upload failed. Storage service may be temporarily unavailable. Try again in a moment." | Error | 7s |
| Save error | "Failed to save branding changes. Please try again." | Error | 6s |
| Reset to default failed | Error: `Failed to reset branding. Please try again.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No portals exist | "No Branch Portals" | "No branch portals have been created. Create portals via the Branch Portal Manager before configuring branding." | Go to Portal Manager |
| All branches have custom branding | "All Branches Branded" | "Every active branch portal has custom branding configured." | — |
| Search returns no results | "No Branches Match" | "No branches match your search or filter criteria." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer (3 cards) + table skeleton (8 rows) including logo thumbnail placeholder shimmer |
| Edit Branding drawer open | Drawer-scoped spinner while current branding data loads |
| Client-side logo preview (file select) | Instant via FileReader API — no server round-trip; spinner not needed |
| Live preview colour update | Instant via CSS custom property update — no loader |
| Logo upload (on save) | Save button spinner + progress indicator "Uploading logo… [%]" using `hx-on::xhr:progress` |
| Save (colours only) | Save button spinner + fields disabled |
| Reset to default | Confirm button spinner + disabled |

---

## 11. Role-Based UI Visibility

| Element | IT Admin (G4) | IT Director (G4) | IT Support Executive (G3) | Integration Manager (G4) |
|---|---|---|---|---|
| KPI Summary Bar | All 3 cards | All 3 cards | Hidden | Hidden |
| Branding Table | Visible + Edit Branding + Reset to Default | Visible (no action buttons) | Branch Name + Logo Status + Last Updated only | Hidden |
| Edit Branding Drawer | Visible + fully editable | Hidden | Hidden | Hidden |
| Logo Upload Field | Visible | Hidden | Hidden | Hidden |
| Colour Pickers | Visible | Hidden | Hidden | Hidden |
| Reset to Default Action | Visible | Hidden | Hidden | Hidden |
| Live Preview Panel | Visible | Visible (read-only in view mode) | Hidden | Hidden |
| brand.json Collapsible | Visible | Visible | Hidden | Hidden |
| Export CSV | Visible | Visible | Hidden | Hidden |
| Alert Banners | All | All | Hidden | Hidden |

**Note:** Role 55 (DPO) and Role 56 (Cybersecurity Officer) have no access to this page (returns 403).

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/portals/branding/` | JWT (G4) | Paginated branch branding status table |
| GET | `/api/v1/it/portals/branding/kpis/` | JWT (G4) | Returns 3 KPI card values |
| GET | `/api/v1/it/portals/{id}/branding/` | JWT (G4) | Current branding data for a specific portal (for drawer) |
| PUT | `/api/v1/it/portals/{id}/branding/` | JWT (G4) | Save brand colour and settings changes |
| POST | `/api/v1/it/portals/{id}/branding/logo/` | JWT (G4) | Upload logo file → stored in Cloudflare R2 at `/static/tenants/{slug}/logo.{ext}` |
| POST | `/api/v1/it/portals/{id}/branding/favicon/` | JWT (G4) | Upload favicon file → stored in R2 at `/static/tenants/{slug}/favicon.{ext}` |
| POST | `/api/v1/it/portals/{id}/branding/reset/` | JWT (G4) | Reset portal branding to EduForge defaults |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar on page ready | `load` | GET `/api/v1/it/portals/branding/kpis/` | `#kpi-bar` | `innerHTML` |
| Load branding table | `load` | GET `/api/v1/it/portals/branding/` | `#branding-table` | `innerHTML` |
| Open Edit Branding drawer | `click` on Edit Branding | GET `/api/v1/it/portals/{id}/branding/` | `#branding-drawer` | `innerHTML` |
| Save brand colours (no file) | `click` on Save Changes (no new file) | PUT `/api/v1/it/portals/{id}/branding/` | `#branding-save-result` | `innerHTML` |
| Upload logo on save | `click` on Save Changes (with file selected) | POST `/api/v1/it/portals/{id}/branding/logo/` (multipart) then PUT colours | `#logo-preview` | `innerHTML` |
| Upload favicon on save | `click` on Save Changes (favicon selected) | POST `/api/v1/it/portals/{id}/branding/favicon/` (multipart) | `#favicon-preview` | `innerHTML` |
| Reset to default (confirm) | `click` on Confirm Reset | POST `/api/v1/it/portals/{id}/branding/reset/` | `#branding-row-{id}` | `outerHTML` |
| Filter table | `change` on filter controls | GET `/api/v1/it/portals/branding/?logo_status=default` | `#branding-table` | `innerHTML` |
| Search branches | `keyup[debounce:300ms]` on search | GET `/api/v1/it/portals/branding/?search=` | `#branding-table` | `innerHTML` |
| Paginate | `click` on page button | GET `/api/v1/it/portals/branding/?page=N` | `#branding-table` | `innerHTML` |
| Refresh KPI after save/reset | `htmx:afterRequest` on PUT/POST | GET `/api/v1/it/portals/branding/kpis/` | `#kpi-bar` | `innerHTML` |
| Client-side colour preview update | `input` on colour picker (JS only — no HTMX) | CSS custom property update on `#preview-panel` | — | — |

---

**Audit Trail:** All write operations on this page are logged to the IT Audit Log with actor user ID and timestamp.

**Notifications:** Critical alerts on this page trigger in-app notifications to the relevant role owners as specified in the alert banner conditions above.

*Page spec version: 1.0 · Last updated: 2026-03-21*
