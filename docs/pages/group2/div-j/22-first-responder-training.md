# 22 — First Responder Training Register

> **URL:** `/group/health/first-responder-training/`
> **File:** `22-first-responder-training.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Emergency Response Officer (primary) · Group Medical Coordinator

---

## 1. Purpose

Track and manage first aid and emergency response training certifications for all staff across every branch of the group. Every branch must maintain a minimum of 5 certified first responders, including at least one trained person on each floor of each building and one trained bus driver per operational fleet. Core certification is CPR + AED (defibrillator operation), with a standard 2-year validity. Additional certification types include Basic First Aid, Advanced First Aid, Basic Cardiac Life Support (BCLS), and Trauma First Responder.

The register tracks: which staff members are certified, what they are certified in, the certifying body, certification number, training date, expiry date, and days remaining until expiry. Renewal scheduling is managed through training events, which can be organised for individual staff or in batches across one or more branches. Expiring certifications are flagged so renewal can be arranged before a lapse creates a compliance gap.

Branch compliance is tracked via a toggle view showing each branch's certified count versus the required minimum of 5, broken down by active, expiring, and expired certifications.

Scale: 5–30 certified staff per branch × 20–50 branches = 100–1,500 training records across the group.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full CRUD — add records, create training events, bulk import, export | Primary owner |
| Group Medical Coordinator | G3 | View all records + add individual records | Co-manager |
| HR Manager | Group | View all records (for background verification and staff compliance files) | Read-only |
| Branch Principal | Branch | View own branch records (via branch portal) | Read-only; no edit |
| All other roles | — | — | No access |

> **Access enforcement:** `@require_role('emergency_response_officer', 'medical_coordinator', 'hr_manager', 'branch_principal')`. HR Manager and Branch Principal read-only enforced server-side. Branch Principal scoped to `record.branch == request.user.branch`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  First Responder Training Register
```

### 3.2 Page Header
- **Title:** `First Responder Training Register`
- **Subtitle:** `[N] Certified First Responders · [N] Active Certifications · [N] Expiring in 60 Days · [N] Expired`
- **Right controls:** `+ Add Record` · `+ Organise Training Event` · `Toggle: Individual / Branch View` · `Advanced Filters` · `Export` · `Bulk Import` (Emergency Response Officer only)

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch below minimum 5 certified first responders | "⚠ [N] branch(es) have fewer than 5 certified first responders. Schedule training immediately." | Red |
| Batch of certifications expiring this month | "⚠ [N] first responder certification(s) expire this month. Schedule renewal training." | Amber |
| No renewal training scheduled for an expiring batch | "[N] staff member(s) have certifications expiring in 60 days with no renewal training scheduled." | Amber |
| Branch with zero trained transport staff (bus drivers) | "CRITICAL: [N] branch(es) have no certified first responder among their bus driver/transport staff." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Certified First Responders | Unique staff with at least one active certification | Blue always |
| Certifications Active | Individual certification records with status = Active | Blue always |
| Certifications Expiring in 60 Days | Expiry date ≤ today + 60 days and status = Active | Green = 0 · Yellow 1–10 · Red > 10 |
| Certifications Expired | Status = Expired (not renewed) | Green = 0 · Amber 1–5 · Red > 5 |
| Branches Below Minimum (< 5 certified) | Branches with < 5 active certified first responders | Green = 0 · Red ≥ 1 |
| Training Events Planned This Year | Training events scheduled for current calendar year | Blue always |

---

## 5. Sections

### 5.1 Individual Records View (default)

**Search:** Staff name, certification number, branch name. 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Training Type | Checkbox | Basic First Aid / CPR + AED / Advanced First Aid / BCLS / Trauma First Responder |
| Status | Checkbox | Active / Expiring (< 60 days) / Expired / Pending Renewal |
| Days to Expiry | Radio | All / Within 30 days / Within 60 days / Within 90 days / Already expired |
| Staff Role Type | Radio | All / Teaching Staff / Non-Teaching Staff / Bus Driver / Hostel Warden |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Staff Name | ✅ | Click → `training-record-detail` drawer |
| Role | ✅ | Staff role/designation |
| Branch | ✅ | |
| Training Type | ✅ | Badge per type |
| Certifying Body | ✅ | Red Cross / St. John Ambulance / BCLS Institute / Internal / Other |
| Certification No | ✅ | Alphanumeric; tooltip shows full certificate reference |
| Trained Date | ✅ | Date training was completed |
| Expiry Date | ✅ | Red if past; amber if within 60 days; green if > 60 days away |
| Days to Expiry | ✅ | Countdown; negative if expired; colour rules same as Expiry Date |
| Status | ✅ | Active (green) / Expiring (amber) / Expired (red) / Pending Renewal (blue) badge |
| Actions | ❌ | View · Edit · Renew · Verify |

**Default sort:** Status (Expired first, then Expiring, then Pending Renewal, then Active), then Days to Expiry ascending.
**Pagination:** Server-side · 25 records per page.

---

### 5.2 Branch Compliance Summary View (toggle)

Accessed via **Toggle: Individual / Branch View** in header.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Branch name |
| Required Minimum | ❌ | Fixed: 5 |
| Certified Count | ✅ | Staff with ≥ 1 active certification |
| Expired Count | ✅ | Staff whose only/all certifications have expired |
| Active Count | ✅ | Staff with valid, non-expiring certifications |
| Compliance | ❌ | Green check if ≥ 5 active / Yellow warning if 3–4 / Red X if < 3 |
| Last Training Event | ✅ | Date of most recent training event at this branch |
| Actions | ❌ | Schedule Training · View Records |

**Default sort:** Compliance (Red first, then Yellow, then Green), then Certified Count ascending.

---

## 6. Drawers / Modals

### 6.1 Drawer — `training-record-detail` (660px, right side)

Triggered by staff name link or **View** action.

**Tabs:**

#### Tab 1 — Certification

| Field | Notes |
|---|---|
| Staff Name | |
| Staff ID | From HR registry |
| Role / Designation | |
| Branch | |
| Training Type | |
| Certifying Body | Name + logo if available (Red Cross, St. John Ambulance, etc.) |
| Certificate Number | |
| Issue Date | |
| Expiry Date | Colour-coded: red if expired, amber if within 60 days |
| Certificate PDF | View inline or Download button |
| Current Status | Active / Expiring / Expired / Pending Renewal — badge |

#### Tab 2 — Training Details

| Field | Notes |
|---|---|
| Trainer Name | Name of individual trainer or training organisation |
| Training Date | |
| Training Venue | Address or branch name |
| Batch Number | If part of a group training event |
| Duration (hours) | |
| Skills Covered | Checklist display (ticked = covered): CPR Adult, CPR Child, CPR Infant, AED Operation, Wound Care, Fracture Management, Choking Response, Anaphylaxis Management, Burns First Aid, Diabetic Emergency, Seizure Management |
| Training Event Reference | Link to `training-event` record (if created via training event — Page 22 event management) |

#### Tab 3 — Renewal History

Table of all previous certification records for this staff member:

| Column | Notes |
|---|---|
| Certification Type | |
| Certifying Body | |
| Certificate Number | |
| Issue Date | |
| Expiry Date | |
| Status at Time | Active / Expired / Superseded |
| Certificate | Download link |

---

### 6.2 Drawer — `training-record-create` (640px, right side)

Triggered by **+ Add Record**.

| Field | Type | Validation |
|---|---|---|
| Staff Search | Autocomplete from staff registry (name + branch + role) | Required; minimum 3 characters |
| Branch | Auto-filled from staff record; editable | Required |
| Training Type | Single-select: Basic First Aid / CPR + AED / Advanced First Aid / BCLS / Trauma First Responder | Required |
| Certifying Body | Single-select: Indian Red Cross Society / St. John Ambulance / ACLS/BCLS Institute / Apollo First Aid / Internal (School-organised) / Other | Required |
| Certifying Body (Other) | Text input | Required if Other selected |
| Certificate Number | Text input | Required; unique per certifying body |
| Training Date | Date picker | Required; cannot be future date |
| Expiry Date | Date picker | Required; must be > Training Date |
| Skills Covered | Multi-checkbox (CPR Adult, CPR Child, CPR Infant, AED Operation, Wound Care, Fracture Management, Choking, Anaphylaxis, Burns, Diabetic Emergency, Seizure) | Required; at least one |
| Trainer Name | Text input | Required |
| Training Venue | Text input | Required |
| Batch / Event Reference | Text input | Optional |
| Duration (hours) | Number input | Required |
| Certificate Upload | File upload (PDF/JPG/PNG; max 10 MB) | Required |

**Footer:** `Cancel` · `Save Record`

---

### 6.3 Drawer — `training-event-create` (640px, right side)

Triggered by **+ Organise Training Event**. Used to schedule a batch training session and link resulting certifications to an event.

| Field | Type | Validation |
|---|---|---|
| Event Name | Text input (max 200 chars) | Required; auto-suggested: "[Type] Training — [Month Year]" |
| Training Type | Single-select (same options as individual record) | Required |
| Branch(es) | Multi-select (can organise for multiple branches in one event) | Required |
| Trainer / Training Organisation | Text input | Required |
| Training Date | Date picker | Required |
| Venue | Text input | Required |
| Expected Participants | Add-rows: Staff search + role + branch (one row per participant) | Required; minimum 1 |
| Duration (hours) | Number input | Required |
| Certifying Body | Single-select | Required |
| Notes / Agenda | Textarea (max 500 chars) | Optional |
| Notify Participants | Checkbox (default checked) — sends portal notification + WhatsApp to each listed participant | |

**Post-event:** After the training date passes, the Emergency Response Officer can open this event record and bulk-add individual certification records for all participants who completed training, linking each to this event.

**Footer:** `Cancel` · `Create Training Event`

---

### 6.4 Modal — `bulk-record-import` (500px, centred)

Triggered by **Bulk Import** (Emergency Response Officer only). Used for initial data entry of existing certifications when setting up the system.

| Field | Type | Notes |
|---|---|---|
| Download Template | Button: "Download CSV Template" | Template includes: staff_name, staff_id, branch, training_type, certifying_body, certificate_number, training_date, expiry_date, skills_covered (pipe-separated) |
| Upload CSV | File upload (.csv, max 5 MB) | Required |
| Preview | Shows first 5 rows of uploaded CSV for validation | Auto-generated after file select |
| Validation errors | Inline: list of rows with errors (missing fields, invalid dates, unknown branch/staff) | Shown before final import |

**Footer:** `Cancel` · `Validate` → `Import [N] Records`

Validation must pass before import is allowed. Partial imports not permitted; fix all errors and re-upload.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Record added | "Certification record added for [Staff Name]." | Success |
| Record updated | "Certification record updated for [Staff Name]." | Success |
| Training event created | "Training event '[Event Name]' created. [N] participant(s) notified." | Success |
| Bulk import completed | "[N] certification records imported successfully." | Success |
| Bulk import partial failure | "Import stopped: [N] row(s) have errors. Download error report, fix, and re-upload." | Error |
| Renew action | "Renewal record created for [Staff Name]. Previous certification archived." | Success |
| Export initiated | "Export initiated. Download will be ready shortly." | Info |
| Validation error — duplicate certificate | "A record with this certificate number already exists for this staff member." | Error |
| Save failed | "Please complete all required fields before saving." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No records in system | "No first responder training records on file." | "Add individual records or bulk-import existing certifications to get started." | `+ Add Record` · `Bulk Import` |
| No records match filters | "No training records match your filters." | "Try adjusting the branch, training type, or expiry filters." | `Clear Filters` |
| Branch compliance — no records for branch | "No training records for this branch." | "Schedule a training event to begin certifying first responders at this branch." | `Schedule Training` |
| Renewal history — first certification | "No previous certifications on record." | "Renewal history will appear here after the first renewal." | — |
| Training event — no participants added | "No participants listed yet." | "Search for staff to add as expected participants." | — |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 6 KPI cards + training table (5 grey rows × 11 columns) |
| View toggle (Individual / Branch) | Table body replaced with skeleton of new view format (individual: 11 columns; branch: 7 columns) |
| Filter apply | Table body inline spinner |
| Training record detail drawer open | Drawer skeleton: 3 tab headers + content blocks (6 grey field rows) |
| Renewal history tab load | Table skeleton (3 grey rows) |
| Training event participant search | Autocomplete dropdown spinner |
| Record create / edit save | Submit button spinner; form fields disabled |
| Bulk import CSV validation | Progress indicator "Validating…" after upload; replaced by preview table or error list |
| Export | Export button spinner + "Preparing…" label |

---

## 10. Role-Based UI Visibility

| UI Element | Emergency Response Officer | Medical Coordinator | HR Manager | Branch Principal |
|---|---|---|---|---|
| Full training list (all branches) | ✅ | ✅ | ✅ (view only) | Own branch only |
| Branch compliance summary | ✅ | ✅ | ✅ (view only) | Own branch only |
| + Add Record button | ✅ | ✅ | ❌ | ❌ |
| + Organise Training Event button | ✅ | ❌ | ❌ | ❌ |
| Bulk Import button | ✅ | ❌ | ❌ | ❌ |
| Edit action | ✅ | ✅ | ❌ | ❌ |
| Renew action | ✅ | ✅ | ❌ | ❌ |
| Verify action | ✅ | ✅ | ❌ | ❌ |
| Delete record | ✅ | ❌ | ❌ | ❌ |
| Certificate PDF download | ✅ | ✅ | ✅ | ✅ |
| Renewal history tab | ✅ | ✅ | ✅ | ✅ |
| Training Details tab | ✅ | ✅ | ✅ | ✅ |
| Export button | ✅ | ❌ | ✅ | ❌ |
| KPI bar — all 6 cards | ✅ | ✅ | ✅ | ❌ |
| Alert banners | ✅ | ✅ | ❌ | Own branch alerts |
| Schedule Training button (branch view) | ✅ | ❌ | ❌ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/first-responder-training/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/first-responder-training/` | List all training records (paginated, filtered, role-scoped) | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/first-responder-training/` | Add new training record | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/` | Retrieve training record detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/` | Update training record | Emergency Response Officer / Medical Coordinator |
| DELETE | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/` | Delete training record (soft delete) | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/branch-compliance/` | Branch compliance summary view data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/renewal-history/` | Renewal history for a staff member | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/renew/` | Create renewal record (archives previous) | Emergency Response Officer / Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/certificate/` | Upload certificate document | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/{record_id}/certificate/` | Download certificate document | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/events/` | List training events | JWT + role check |
| POST | `/api/v1/group/{group_id}/health/first-responder-training/events/` | Create training event | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/events/{event_id}/` | Retrieve training event detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/first-responder-training/events/{event_id}/` | Update training event | Emergency Response Officer |
| POST | `/api/v1/group/{group_id}/health/first-responder-training/bulk-import/` | CSV bulk import of certification records | Emergency Response Officer |
| GET | `/api/v1/group/{group_id}/health/first-responder-training/export/` | Export training records | Emergency Response Officer / HR Manager |

**Query parameters for list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `search` | str | Staff name, certificate number, or branch name |
| `branch` | int[] | Branch filter |
| `training_type` | str[] | `basic_first_aid`, `cpr_aed`, `advanced_first_aid`, `bcls`, `trauma` |
| `status` | str[] | `active`, `expiring`, `expired`, `pending_renewal` |
| `days_to_expiry` | int | Filter: `30`, `60`, or `90` (within N days) |
| `role_type` | str | `teaching`, `non_teaching`, `driver`, `warden` |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |
| `ordering` | str | e.g. `days_to_expiry`, `-trained_date` |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Individual / branch view toggle | `hx-get="/api/.../first-responder-training/?view={individual|branch}"` `hx-target="#training-view-container"` `hx-trigger="click"` | Full view container swapped; URL updated |
| Search debounce | `hx-get="/api/.../first-responder-training/"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#training-table-body"` `hx-include="#filter-form"` | Table rows replaced |
| Filter apply | `hx-get="/api/.../first-responder-training/"` `hx-trigger="change"` `hx-target="#training-table-body"` `hx-include="#filter-form"` | Table rows replaced; KPI bar refreshed |
| KPI bar load | `hx-get="/api/.../first-responder-training/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| Alert banner load | `hx-get="/api/.../first-responder-training/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load |
| Pagination | `hx-get="/api/.../first-responder-training/?page={n}"` `hx-target="#training-table-body"` `hx-push-url="true"` | Page swap |
| Training record detail drawer open | `hx-get="/api/.../first-responder-training/{record_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Certification tab default |
| Drawer tab switch | `hx-get="/api/.../first-responder-training/{record_id}/?tab={tab_slug}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Lazy load on first click |
| Renewal history tab load | `hx-get="/api/.../first-responder-training/{record_id}/renewal-history/"` `hx-target="#renewal-history-content"` `hx-trigger="click[tab='renewal_history'] once"` | Loaded once |
| Staff search autocomplete | `hx-get="/api/v1/staff/search/?q={val}"` `hx-trigger="keyup changed delay:300ms"` `hx-target="#staff-search-results"` | Dropdown results updated |
| Record create submit | `hx-post="/api/.../first-responder-training/"` `hx-target="#training-table-body"` `hx-on::after-request="closeDrawer(); fireToast(); refreshKPI();"` | New row prepended; KPI refreshed |
| Record edit submit | `hx-patch="/api/.../first-responder-training/{record_id}/"` `hx-target="#training-row-{record_id}"` `hx-swap="outerHTML"` | Row updated in-place |
| Renew action | `hx-post="/api/.../first-responder-training/{record_id}/renew/"` `hx-target="#training-row-{record_id}"` `hx-swap="outerHTML"` `hx-on::after-request="fireToast();"` | Row status updated; previous record archived |
| Certificate upload | `hx-post="/api/.../first-responder-training/{record_id}/certificate/"` `hx-encoding="multipart/form-data"` `hx-target="#certificate-section"` | Certificate section in drawer refreshed |
| Training event create submit | `hx-post="/api/.../first-responder-training/events/"` `hx-target="#events-count"` `hx-on::after-request="closeDrawer(); fireToast();"` | KPI Training Events card incremented; drawer closed |
| Bulk import validate | `hx-post="/api/.../first-responder-training/bulk-import/"` `hx-encoding="multipart/form-data"` `hx-target="#import-preview"` `hx-indicator="#import-spinner"` | Preview table or error list shown before final confirm |
| Bulk import confirm | Separate confirm button after validation: `hx-post="/api/.../first-responder-training/bulk-import/?confirmed=true"` `hx-target="#training-table-body"` `hx-on::after-request="closeModal(); fireToast(); refreshKPI();"` | Table repopulated; modal closed |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
