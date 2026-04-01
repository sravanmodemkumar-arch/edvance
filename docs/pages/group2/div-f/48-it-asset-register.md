# Page 48: IT Asset Register

**URL:** `/group/it/assets/`
**Roles:** Group IT Admin (Role 54, G4); Group IT Director (Role 53, G4)
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Centralised register of all IT assets across the EduForge group — every branch's computers, servers, networking equipment, AV/projector systems, digital display boards, tablets, and mobile devices. Tracking assets enables:

- **Budget planning:** Know what exists, what's ageing, and what will need replacing
- **Warranty management:** Track expiry dates to avoid post-warranty failures going unnoticed
- **Assignment tracking:** Know which staff member has which device; prevent ghost assets (assets that are listed but physically missing)
- **Maintenance scheduling:** Track devices under repair or requiring preventive maintenance
- **Audit readiness:** Provide complete asset inventory to auditors or insurance assessors
- **Lifecycle management:** Plan disposal, upgrades, and replacements proactively

Asset categories:
- **Computer** — desktops, laptops
- **Server** — physical or virtual servers (if any on-premise)
- **Networking** — routers, switches, WAPs, firewalls
- **AV** — projectors, interactive whiteboards, digital displays, speakers
- **Mobile** — smartphones, tablets issued to staff
- **Other** — UPS, printers, scanners, CCTV equipment

All purchase invoices and warranty documents are stored in Cloudflare R2.

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full CRUD | Add, edit, transfer, dispose assets |
| Group IT Director (Role 53, G4) | Full CRUD | Same as IT Admin |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | Can view device register subset (filtered to security-relevant devices) — via their own page (Page 39) |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Assets > Asset Register`

**Page Header:**
- Title: `IT Asset Register`
- Subtitle: `Group-wide IT asset inventory — all branches`
- Right side: `+ Add Asset` button, `Export (CSV)` button

**Alert Banners:**

1. **Warranty Expiring Soon** (amber, dismissible per session):
   - Condition: any asset with warranty_expiry_date < today + 90 days and status ≠ Disposed
   - Text: `[X] assets have warranties expiring within 90 days. Review and arrange renewals or replacements.`

2. **Assets Under Maintenance >30 Days** (amber, dismissible per session):
   - Condition: any asset with status = Under Repair and last_status_change_date < today - 30 days
   - Text: `[X] assets have been under repair for over 30 days. Verify repair status with the branch.`

3. **Unaudited Assets** (blue, informational):
   - Condition: any asset with last_audit_date < today - 180 days
   - Text: `[X] assets have not been audited in over 6 months. Schedule an asset verification.`

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Total Assets | Count of all assets with status ≠ Disposed | Plain number |
| 2 | In Use | Count where status = In Use | Number, green |
| 3 | Under Maintenance | Count where status = Under Repair | Number, amber if > 0 |
| 4 | Warranty Expiring <90 Days | Count where warranty_expiry_date < today + 90 days and status ≠ Disposed | Number, amber if > 0, red if expiry < 30 days |

---

## 5. Main Table — Asset Register

**Table Title:** `Asset Register`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Asset Tag | Text | Unique identifier (e.g., `ASSET-BLR01-0042`); searchable |
| Asset Name | Text | Friendly name (e.g., `Dell Latitude 5520 — Staff Laptop`) |
| Category | Badge | Computer / Server / Networking / AV / Mobile / Other |
| Brand/Model | Text | e.g., `Dell Latitude 5520` |
| Branch | Text | Branch this asset belongs to |
| Assigned To | Text | Staff member name or `Unassigned` |
| Purchase Date | Date | |
| Warranty Expiry | Date | Colour: red if expired, amber if < 90 days |
| Status | Badge | In Use (green) / In Store (blue) / Under Repair (amber) / Disposed (grey) |
| Last Audit Date | Date | When asset was physically verified; amber if > 6 months |
| Actions | Buttons | `View` / `Edit` / `Transfer` / `Dispose` |

### Filters

- **Branch:** Multi-select dropdown
- **Category:** All / Computer / Server / Networking / AV / Mobile / Other
- **Status:** All / In Use / In Store / Under Repair / Disposed
- **Warranty Expiry:** All / Expiring < 30 Days / Expiring < 90 Days / Already Expired
- **Assigned To:** All / Unassigned / Assigned

### Search

Search on Asset Tag, Asset Name, Brand/Model, or Assigned To name. `hx-trigger="keyup changed delay:400ms"`, targets `#asset-table`.

### Pagination

Server-side, 25 rows per page. `hx-get="/group/it/assets/table/?page=N"`, targets `#asset-table`.

### Sorting

Sortable: Asset Tag, Category, Branch, Warranty Expiry, Status, Last Audit Date. Default sort: Warranty Expiry ascending (soonest expiry first among non-disposed assets).

---

## 6. Drawers

**Note:** Asset deletion is not supported. Use the Dispose action to retire assets while retaining historical records for audit compliance.

### A. Add Asset Drawer (640px, right-side)

Triggered by `+ Add Asset` button.

**Drawer Header:** `Add IT Asset`

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Asset Tag | Text input | Yes | Auto-suggest format: `ASSET-[BranchCode]-[NNN]`; editable |
| Asset Name | Text input | Yes | Descriptive name |
| Category | Dropdown | Yes | Computer / Server / Networking / AV / Mobile / Other |
| Brand | Text input | Yes | Manufacturer name |
| Model | Text input | Yes | Model number/name |
| Serial Number | Text input | Yes | Hardware serial number |
| Branch | Dropdown | Yes | Which branch this asset belongs to |
| Assigned To | Search/select | No | Staff member; leave blank if unassigned/in store |
| Status | Dropdown | Yes | In Use / In Store / Under Repair |
| Purchase Date | Date | Yes | |
| Purchase Cost (₹) | Number | Yes | Amount paid |
| Warranty Expiry Date | Date | Yes | |
| Notes | Textarea | No | Any relevant notes |
| Upload Invoice | File upload | No | PDF/image → Cloudflare R2 |
| Upload Warranty Doc | File upload | No | PDF/image → Cloudflare R2 |

**Footer:** `Add Asset` / `Cancel`

On submit: `hx-post="/api/v1/it/assets/"`. Toast: `Asset [Tag] added to register.`

---

### B. Edit Asset Drawer (640px)

Same fields as Add Asset, pre-populated. Also includes:
- `Last Audit Date` field (editable — update when physical verification performed)

**Footer:** `Save Changes` / `Cancel`

---

### C. View Asset Drawer (560px)

Triggered by `View` button or clicking Asset Name in table.

**Sections:**

**Asset Summary:**
- Asset Tag, Name, Category, Brand/Model, Serial Number
- Status badge, Branch, Assigned To
- Purchase Date, Purchase Cost
- Warranty Expiry (with days remaining or `Expired [X] days ago`)
- Last Audit Date

**Documents:**
- Invoice: `View Invoice` link (R2 signed URL)
- Warranty Document: `View Warranty Doc` link (R2 signed URL)

**Transfer History:**
- Chronological list of branch transfers with date, from/to, actioned by

**Maintenance History:**
- List of Under Repair entries with dates and notes

**Footer:** `Close` | `Edit` | `Transfer` | `Dispose`

---

### D. Transfer Asset Drawer (440px)

Triggered by `Transfer` button.

**Purpose:** Move asset from one branch to another. Creates a transfer record.

**Fields:**
- Asset: [Tag — Name] (read-only)
- Current Branch: [Branch] (read-only)
- Transfer To Branch: Dropdown (required)
- Transfer Reason: Dropdown — Reallocation / Branch Closure / Surplus Equipment / Other
- Transfer Notes: Textarea (optional)
- New Assigned To: Search/select (optional — re-assign at new branch)
- Transfer Date: Date (defaults to today)

**Footer:** `Confirm Transfer` / `Cancel`

On submit: `hx-post="/api/v1/it/assets/{id}/transfer/"`. Asset branch updated, transfer record created. Toast: `Asset [Tag] transferred to [Branch].`

---

### E. Dispose Asset Drawer (440px)

Triggered by `Dispose` button. Marks asset as disposed — removes from active register but retains record.

**Fields:**
- Asset: [Tag — Name] (read-only)
- Disposal Date: Date (defaults to today)
- Disposal Method: Dropdown — Sold / Donated / Scrapped / Returned to Vendor / Written Off / Stolen/Lost
- Disposal Reason: Textarea (required)
- Disposal Reference: Text (optional — e-waste certificate #, sale receipt #)
- Confirm: `I confirm this asset is being permanently removed from service` (checkbox)

**Footer:** `Confirm Disposal` (red) / `Cancel`

On submit: `hx-put` sets status = Disposed, disposal metadata recorded. Toast: `Asset [Tag] marked as disposed.`

---

## 7. Charts

Three charts below the main table in a responsive 2-column layout (first full width, others side by side).

### Chart 1: Asset Distribution by Branch (Full Width)
- **Type:** Horizontal bar chart (stacked by category)
- **Y-axis:** Branch names
- **X-axis:** Asset count
- **Segments:** Category colours (Computer blue, Networking teal, AV purple, Mobile green, etc.)
- **Purpose:** Understand how assets are distributed across branches; identify under-resourced branches
- **Data endpoint:** `/api/v1/it/assets/charts/by-branch/`

### Chart 2: Warranty Expiry Timeline
- **Type:** Vertical bar chart
- **X-axis:** Quarters (Q2 2026, Q3 2026, Q4 2026, Q1 2027, Q2 2027, Q3 2027)
- **Y-axis:** Asset count
- **Colour:** Red for Q2 2026 (most urgent), orange for Q3, amber for Q4+
- **Purpose:** Budget planning — understand how many assets will need replacement each quarter
- **Data endpoint:** `/api/v1/it/assets/charts/warranty-timeline/`

### Chart 3: Asset Category Breakdown
- **Type:** Donut chart
- **Segments:** Each category with count and %
- **Purpose:** Understand the composition of the asset fleet
- **Data endpoint:** `/api/v1/it/assets/charts/by-category/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| Asset added | Success: `Asset [Tag] added to register.` |
| Asset updated | Success: `Asset [Tag] updated.` |
| Asset transferred | Success: `Asset [Tag] transferred to [Branch].` |
| Asset disposed | Success: `Asset [Tag] marked as disposed.` |
| Document uploaded | Info: `Document uploaded and saved.` |
| Export initiated | Info: `Exporting asset register.` |
| Validation error | Error: `Please complete all required fields.` |
| Duplicate asset tag | Error: `Asset tag [Tag] already exists. Use a unique tag.` |
| Asset add failed | Error: `Failed to add asset. Please check your connection and try again.` | Error | 5s |
| Asset edit failed | Error: `Failed to save changes. Please try again.` | Error | 5s |
| Transfer failed | Error: `Failed to transfer asset. Verify the branch exists and try again.` | Error | 5s |
| Disposal failed | Error: `Failed to mark asset as disposed. Please try again.` | Error | 5s |

---

**Audit Trail:** All asset mutations (add, edit, transfer, dispose) are automatically logged to the IT Audit Log with actor user ID, timestamp, asset ID, and full before/after values.

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No assets registered | Icon + `No assets registered. Add your first asset using "+ Add Asset".` |
| No assets match filters | `No assets match the selected filters.` |
| No transfer history | In view drawer: `No transfers recorded for this asset.` |
| No documents uploaded | In view drawer: `No documents uploaded. Edit asset to attach invoice or warranty.` |
| Chart insufficient data | `Add assets across multiple branches to display distribution data.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 4 skeleton shimmer cards |
| Asset table | 6 skeleton rows |
| View Asset drawer | Spinner then progressive render |
| Transfer history section | Skeleton list items |
| Document links | Spinner while generating R2 signed URLs |
| Charts | Spinner in each chart container |
| File upload progress | Progress bar in drawer upload field |
| Submit buttons | `Saving...` text + disabled |

---

## 11. Role-Based UI Visibility

| UI Element | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|
| Add Asset button | Visible | Visible |
| Edit button | Visible | Visible |
| Transfer button | Visible | Visible |
| Dispose button | Visible | Visible |
| View button | Visible | Visible |
| Export CSV | Visible | Visible |
| Purchase Cost field | Visible | Visible |
| All filters | Visible | Visible |

**Note:** Role 56 (Cybersecurity Officer, G1) has read-only access — can view all assets but cannot add, edit, transfer, or dispose. Export CSV hidden. All edit/action buttons hidden.

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/assets/` | Fetch asset list (paginated) |
| POST | `/api/v1/it/assets/` | Create asset |
| GET | `/api/v1/it/assets/{id}/` | Fetch asset detail |
| PUT | `/api/v1/it/assets/{id}/` | Update asset |
| POST | `/api/v1/it/assets/{id}/transfer/` | Transfer to new branch |
| PUT | `/api/v1/it/assets/{id}/dispose/` | Dispose asset |
| POST | `/api/v1/it/assets/{id}/documents/` | Upload invoice/warranty to R2 |
| GET | `/api/v1/it/assets/{id}/documents/{doc_id}/url/` | Get R2 signed URL |
| GET | `/api/v1/it/assets/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/assets/charts/by-branch/` | Distribution by branch |
| GET | `/api/v1/it/assets/charts/warranty-timeline/` | Warranty expiry timeline |
| GET | `/api/v1/it/assets/charts/by-category/` | Category breakdown |
| GET | `/api/v1/it/assets/export/csv/` | Export register |

---

## 13. HTMX Patterns

```html
<!-- Asset table -->
<div id="asset-table"
     hx-get="/group/it/assets/table/"
     hx-trigger="load"
     hx-target="#asset-table"
     hx-include="#asset-filter-form">
</div>

<!-- Search -->
<input type="text" name="search" placeholder="Search assets..."
       hx-get="/group/it/assets/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#asset-table"
       hx-include="#asset-filter-form" />

<!-- Add asset drawer -->
<button hx-get="/group/it/assets/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Add Asset
</button>

<!-- Create submit with file upload -->
<form hx-post="/api/v1/it/assets/"
      hx-encoding="multipart/form-data"
      hx-target="#asset-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <!-- asset fields + file inputs -->
  <button type="submit">Add Asset</button>
</form>

<!-- Transfer drawer -->
<button hx-get="/group/it/assets/{{ asset.id }}/transfer-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Transfer
</button>

<!-- Dispose drawer -->
<button hx-get="/group/it/assets/{{ asset.id }}/dispose-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Dispose
</button>

<!-- Dispose confirm -->
<form hx-put="/api/v1/it/assets/{{ asset.id }}/dispose/"
      hx-target="#asset-table"
      hx-swap="outerHTML"
      hx-confirm="Permanently mark this asset as disposed?"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit" class="btn-danger">Confirm Disposal</button>
</form>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
