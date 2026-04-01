# Page 49: Software License Manager

**URL:** `/group/it/assets/licenses/`
**Roles:** Group IT Admin (Role 54, G4); Group IT Director (Role 53, G4)
**Priority:** P1
**Division:** F — Group IT & Technology

---

## 1. Purpose

Track and manage all software licenses used across the EduForge group. Software licensing compliance is a legal and operational obligation — using more seats than licensed is a breach of vendor agreements and can result in audits, penalties, and service termination.

**Licenses managed include:**
- Microsoft 365 (per-seat — staff email, Office apps, Teams)
- Antivirus/EDR solutions (per-seat or per-device)
- School management tools (EduForge itself, plus any branch-level tools)
- Design tools (Canva for Education, Adobe Creative Cloud)
- Video conferencing (Zoom, Google Meet)
- Communication platforms (WhatsApp Business API)
- E-signature solutions
- Accounting software (Tally, Zoho Books)
- Custom integrations with annual subscription

For each license, the system tracks total seats purchased, seats currently in use, expiry date, annual cost, renewal owner, and vendor details. License documents are stored in Cloudflare R2.

Key use cases:
- **Compliance:** Ensure no license is overused
- **Renewals:** Get ahead of expiry dates to avoid service interruption
- **Cost management:** Identify underused licenses (< 80% seats used) for renegotiation or cancellation
- **Audit readiness:** Demonstrate license compliance to auditors

---

## 2. Role Access

| Role | Access Level | Notes |
|------|-------------|-------|
| Group IT Admin (Role 54, G4) | Full CRUD | Add, edit, renew, terminate licenses |
| Group IT Director (Role 53, G4) | Full CRUD | Same as IT Admin |
| Group Finance (CFO, etc.) | Read-only | View license costs for budgeting (future phase) |
| All other roles | No access | Returns 403 |
| Group Data Privacy Officer (Role 55, G1) | No access | Returns 403 |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

**Breadcrumb:**
`Group Portal > IT & Technology > IT Assets > Software License Manager`

**Page Header:**
- Title: `Software License Manager`
- Subtitle: `Software license compliance and renewal tracking across the group`
- Right side: `+ Add License` button, `Export (CSV)` button

**Alert Banners:**

1. **License Expiring in <7 Days** (red, non-dismissible):
   - Condition: any license with expiry_date < today + 7 days and status = Active
   - Text: `LICENSE EXPIRING SOON — [Software Name] ([Vendor]) expires in [X] days. Renew immediately or users will lose access.`

2. **License Expired** (red, non-dismissible):
   - Condition: any license with expiry_date < today and status = Active (not yet marked Expired)
   - Text: `LICENSE EXPIRED — [Software Name] expired [X] days ago. Continued use may violate the vendor agreement.`

3. **License Overused** (red, non-dismissible):
   - Condition: any license where used_seats > total_seats
   - Text: `LICENSE OVERUSE — [Software Name]: [used] seats in use but only [total] licensed. Purchase additional seats immediately.`

4. **Underused Licenses** (blue, informational, dismissible):
   - Condition: any license where used_seats < total_seats × 0.80 and license_type = Per Seat
   - Text: `[X] licenses are below 80% utilisation. Review and consider renegotiating or cancelling unused seats.`

---

## 4. KPI Summary Bar

Four KPI cards in a 4-column grid.

| # | Metric | Calculation | Visual |
|---|--------|-------------|--------|
| 1 | Total Licenses | Count of all licenses with status ≠ Cancelled | Plain number |
| 2 | Expiring <30 Days | Count where expiry_date < today + 30 days and status = Active | Number — amber if > 0, red if any < 7 days |
| 3 | Expired (Renewal Overdue) | Count where expiry_date < today and status = Active (not yet actioned) | Number — red if > 0 |
| 4 | Underused (<80% seats used) | Count where used_seats < total_seats × 0.80 and license_type = Per Seat | Number — blue (informational) |

---

## 5. Main Table — License Register

**Table Title:** `Software License Register`

### Columns

| Column | Type | Notes |
|--------|------|-------|
| Software Name | Text | e.g., `Microsoft 365 Business Standard` |
| Vendor | Text | e.g., `Microsoft`, `Symantec`, `Zoom` |
| License Type | Badge | Per Seat / Site License / Concurrent / Subscription |
| Total Seats / Units | Number | Total seats or devices covered |
| Used Seats | Number | Currently in use; red if > total; amber if < 80% of total |
| Expiry Date | Date | Red if expired, amber if < 30 days, green if > 30 days |
| Cost (Annual ₹) | Currency | Annual cost in INR |
| Renewal Owner | Text | Staff member responsible for renewal |
| Status | Badge | Active (green) / Expiring (amber) / Expired (red) / Cancelled (grey) |
| Actions | Buttons | `View` / `Edit` / `Renew` / `Terminate` |

### Filters

- **Status:** All / Active / Expiring / Expired / Cancelled
- **Expiry Range:** All / Expiring < 7 Days / Expiring < 30 Days / Expiring < 90 Days / Already Expired
- **Vendor:** Search/select dropdown
- **License Type:** All / Per Seat / Site License / Concurrent / Subscription
- **Utilisation:** All / Overused / Underused (<80%) / Normal

### Search

Search on Software Name, Vendor, Renewal Owner. `hx-trigger="keyup changed delay:400ms"`, targets `#license-table`.

### Pagination

Server-side, 20 rows per page. `hx-get="/group/it/assets/licenses/table/?page=N"`, targets `#license-table`.

### Sorting

Sortable: Software Name, Expiry Date, Cost, Used Seats %. Default sort: Expiry Date ascending (soonest expiry first for active licenses; expired licenses at top).

---

## 6. Drawers

**Note:** License deletion is not supported. Use the Terminate action to deactivate licenses while retaining records for compliance.

### A. Add License Drawer (640px, right-side)

Triggered by `+ Add License` button.

**Drawer Header:** `Add Software License`

**Fields:**

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| Software Name | Text input | Yes | Full software name including edition |
| Vendor | Text input | Yes | Software vendor/publisher |
| License Type | Dropdown | Yes | Per Seat / Site License / Concurrent / Subscription |
| Total Seats / Units | Number | Conditional | Required for Per Seat/Concurrent; N/A for Site License — Total Seats / Units: required if License Type = Per Seat or Concurrent; not applicable for Site License or Open Source. |
| License Key / Agreement # | Text input | No | For reference; stored securely |
| Purchase Date | Date | Yes | |
| Expiry Date | Date | Yes | |
| Annual Cost (₹) | Number | Yes | |
| Renewal Owner | Search/select | Yes | Staff member responsible |
| Applicable Branches | Multi-select | Yes | Which branches use this license; or "All Branches" |
| Notes | Textarea | No | Renewal terms, vendor contact, etc. |
| Upload License Document | File upload | No | PDF → Cloudflare R2 |
| Upload Purchase Invoice | File upload | No | PDF → Cloudflare R2 |

**Footer:** `Add License` / `Cancel`

On submit: `hx-post="/api/v1/it/assets/licenses/"`. KPIs refresh. Toast: `License "[Software Name]" added.`

---

### B. Edit License Drawer (640px)

Same fields as Add License, pre-populated. Used to update seat counts, cost changes, or renewal owner changes.

**Additional fields:**
- Used Seats (manually updateable if auto-detection not available): Number input

**Footer:** `Save Changes` / `Cancel`

---

### C. Renew License Drawer (440px)

Triggered by `Renew` button. Focused form for processing a renewal without full edit.

**Fields:**
- License: [Software Name] (read-only)
- Current Expiry: [date] (read-only)
- New Expiry Date: Date input (required)
- New Annual Cost (₹): Number input (required — may change at renewal)
- Seats (updated): Number input (optional — seats may increase/decrease at renewal)
- Renewal Notes: Textarea (optional)
- Upload New License Document: File upload → Cloudflare R2

**Footer:** `Confirm Renewal` / `Cancel`

On submit: `hx-post="/api/v1/it/assets/licenses/{id}/renew/"`. Status → Active (if was Expiring/Expired). New expiry recorded. Renewal history entry created. Toast: `License "[Software Name]" renewed until [new expiry date].`

---

### D. Terminate License Drawer (440px)

Triggered by `Terminate` button.

**Fields:**
- License: [Software Name] (read-only)
- Termination Date: Date (defaults to today)
- Reason: Dropdown — Not Needed / Switched Vendor / Budget Cut / Duplicate License / Branch Closure / Other
- Termination Notes: Textarea (required)
- Confirm: `I confirm this license is being terminated and access will be revoked` (checkbox)

**Footer:** `Confirm Termination` (red) / `Cancel`

On submit: Status → Cancelled. Toast: `License "[Software Name]" terminated.`

---

### E. View License Detail Drawer (560px — all roles)

Triggered by `View` button or clicking Software Name.

**Sections:**

**License Overview:**
- Software Name, Vendor, License Type, Status badge
- Total Seats, Used Seats (with utilisation % and colour coding)
- Purchase Date, Expiry Date (with days remaining)
- Annual Cost
- Applicable Branches
- Renewal Owner

**Documents:**
- License Document: `View Document` (R2 signed URL)
- Invoice: `View Invoice` (R2 signed URL)

**Usage History:**
- Trend of seat usage over last 6 months (simple table or mini-line): Month / Seats Used

**Renewal History:**
- Table: Previous Expiry / New Expiry / Cost / Renewed By / Date

**Footer:** `Close` | `Edit` | `Renew` | `Terminate`

---

## 7. Charts

No dedicated full charts section. An inline visual strip below the KPI bar shows:

**Cost Summary by Category:**
- Pie chart showing total annual license spend by software category
- Categories: Productivity (MS365 etc.), Security (antivirus etc.), Communication, Design, Other
- Total annual spend displayed in centre

**This inline chart reduces page length while still providing cost visibility. Data endpoint:** `/api/v1/it/assets/licenses/charts/cost-by-category/`

---

## 8. Toast Messages

| Action | Toast |
|--------|-------|
| License added | Success: `License "[Software Name]" added. Expiry: [date].` |
| License updated | Success: `License "[Software Name]" updated.` |
| License renewed | Success: `License "[Software Name]" renewed until [date].` |
| License terminated | Success: `License "[Software Name]" terminated.` |
| License about to expire (< 7 days — system) | System alert notification (not just toast) |
| Document uploaded | Info: `Document uploaded.` |
| Export initiated | Info: `Exporting license register.` |
| Validation error | Error: `Please complete all required fields.` |
| Overuse detected on save | Warning: `Used seats exceed total licensed seats. Purchase additional seats.` |
| License add failed | Error: `Failed to add license. Please check your details and try again.` | Error | 5s |
| License edit failed | Error: `Failed to update license. Please try again.` | Error | 5s |
| License renewal failed | Error: `Failed to renew license. Verify the expiry date and try again.` | Error | 5s |
| License termination failed | Error: `Failed to terminate license. Please try again.` | Error | 5s |

---

**Audit Trail:** All license mutations (add, edit, renew, terminate) are automatically logged to the IT Audit Log with actor user ID, timestamp, license ID, and full before/after values.

---

## 9. Empty States

| Condition | Message |
|-----------|---------|
| No licenses registered | Icon + `No software licenses registered. Add your first license using "+ Add License".` |
| No licenses match filters | `No licenses match the selected filters.` |
| No renewal history | In view drawer: `No renewals recorded yet.` |
| No documents uploaded | In view drawer: `No documents attached. Edit this license to upload.` |
| No usage history | In view drawer: `No usage history available.` |

---

## 10. Loader States

| Element | Loader Behaviour |
|---------|-----------------|
| KPI bar | 4 skeleton shimmer cards |
| License table | 5 skeleton rows |
| View drawer | Spinner then section render |
| Renewal history (in drawer) | Skeleton table rows |
| Document link generation | Spinner while fetching R2 signed URL |
| Cost summary chart | Spinner in chart area |
| File upload | Progress bar |
| Submit buttons | `Saving...` text + disabled |

---

## 11. Role-Based UI Visibility

| UI Element | Role 54 (G4) | Role 53 (G4) |
|------------|-------------|-------------|
| Add License button | Visible | Visible |
| Edit button | Visible | Visible |
| Renew button | Visible | Visible |
| Terminate button | Visible | Visible |
| View button | Visible | Visible |
| License Key / Agreement # | Visible | Visible |
| Annual Cost | Visible | Visible |
| Export CSV | Visible | Visible |
| All alert banners | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/v1/it/assets/licenses/` | Fetch license list (paginated) |
| POST | `/api/v1/it/assets/licenses/` | Create license |
| GET | `/api/v1/it/assets/licenses/{id}/` | Fetch license detail |
| PUT | `/api/v1/it/assets/licenses/{id}/` | Update license |
| POST | `/api/v1/it/assets/licenses/{id}/renew/` | Renew license |
| PUT | `/api/v1/it/assets/licenses/{id}/terminate/` | Terminate license |
| POST | `/api/v1/it/assets/licenses/{id}/documents/` | Upload document to R2 |
| GET | `/api/v1/it/assets/licenses/{id}/documents/{doc_id}/url/` | R2 signed URL |
| GET | `/api/v1/it/assets/licenses/kpis/` | Fetch KPI values |
| GET | `/api/v1/it/assets/licenses/charts/cost-by-category/` | Cost breakdown chart |
| GET | `/api/v1/it/assets/licenses/export/csv/` | Export register |

---

## 13. HTMX Patterns

```html
<!-- License table -->
<div id="license-table"
     hx-get="/group/it/assets/licenses/table/"
     hx-trigger="load"
     hx-target="#license-table"
     hx-include="#license-filter-form">
</div>

<!-- Search -->
<input type="text" name="search" placeholder="Search licenses..."
       hx-get="/group/it/assets/licenses/table/"
       hx-trigger="keyup changed delay:400ms"
       hx-target="#license-table"
       hx-include="#license-filter-form" />

<!-- Add license drawer -->
<button hx-get="/group/it/assets/licenses/create-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  + Add License
</button>

<!-- Create submit -->
<form hx-post="/api/v1/it/assets/licenses/"
      hx-encoding="multipart/form-data"
      hx-target="#license-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit">Add License</button>
</form>

<!-- Renew license drawer -->
<button hx-get="/group/it/assets/licenses/{{ license.id }}/renew-form/"
        hx-target="#drawer-container"
        hx-swap="innerHTML"
        hx-on::after-request="openDrawer()">
  Renew
</button>

<!-- Renew submit -->
<form hx-post="/api/v1/it/assets/licenses/{{ license.id }}/renew/"
      hx-encoding="multipart/form-data"
      hx-target="#license-table"
      hx-swap="outerHTML"
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit">Confirm Renewal</button>
</form>

<!-- Terminate -->
<form hx-put="/api/v1/it/assets/licenses/{{ license.id }}/terminate/"
      hx-target="#license-table"
      hx-swap="outerHTML"
      hx-confirm="Terminate this license? Access will be revoked."
      hx-on::after-request="closeDrawer(); refreshKPIs()">
  <button type="submit" class="btn-danger">Confirm Termination</button>
</form>

<!-- Inline cost chart -->
<div id="cost-chart"
     hx-get="/group/it/assets/licenses/charts/cost-by-category/"
     hx-trigger="load"
     hx-target="#cost-chart">
</div>
```

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
