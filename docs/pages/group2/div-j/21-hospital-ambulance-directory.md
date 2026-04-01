# 21 — Hospital & Ambulance Directory

> **URL:** `/group/health/hospital-directory/`
> **File:** `21-hospital-ambulance-directory.md`
> **Template:** `portal_base.html`
> **Priority:** P0
> **Role:** Group Emergency Response Officer (primary) · Group Medical Coordinator (co-manage)

---

## 1. Purpose

Directory of all tied-up hospitals, empanelled clinics, ambulance services, blood banks, on-call doctors, and psychiatrist referrals for every branch across the group. The directory ensures that every branch always has at minimum: one tied-up hospital (preferably cashless for insurance), one 24-hour emergency ambulance contact, one blood bank contact, and one on-call doctor contact. This information must be instantly accessible to first responders and branch staff during an emergency without having to search through emails or paper files.

The directory also tracks MOU (Memorandum of Understanding) status with tied-up hospitals, MOU expiry dates, and verification status of each contact (contacts must be verified — confirmed still active and numbers checked — at least every 6 months). A printable branch emergency directory card is available for physical display in medical rooms and staff notice boards.

Additionally, a read-only emergency quick-access widget displays each branch's primary emergency contacts in the portal sidebar so any staff member can find them instantly without navigating to this page.

Scale: 2–5 contacts per branch × 20–50 branches = 40–250 directory entries.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Emergency Response Officer | G3 | Full CRUD — add, edit, verify, delete contacts; manage MOUs | Primary owner |
| Group Medical Coordinator | G3 | Full CRUD — add, edit, verify contacts | Co-manager |
| Group School Medical Officer | G3 | Edit own branch contacts + mark contacts as verified | Branch-level management |
| Branch Principal | Branch | View own branch contacts (via branch portal) | Read-only; no edit |
| All Staff | — | Read-only emergency numbers via portal sidebar widget | Quick-access widget only; not this full directory page |
| All other roles | — | — | No access to this page |

> **Access enforcement:** `@require_role('emergency_response_officer', 'medical_coordinator', 'school_medical_officer', 'branch_principal')`. School Medical Officer write access scoped to `contact.branch == request.user.branch`. Branch Principal access via branch portal — separate view endpoint. Portal sidebar emergency widget served from `/api/v1/group/{group_id}/health/hospital-directory/emergency-widget/` — returns only primary emergency phone for user's branch; accessible to all authenticated users.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Hospital & Ambulance Directory
```

### 3.2 Page Header
- **Title:** `Hospital & Ambulance Directory`
- **Subtitle:** `[N] Total Contacts · [N] Branches Covered · [N] MOUs Active · [N] Contacts Due Verification`
- **Right controls:** `+ Add Contact` (Emergency Response Officer + Medical Coordinator + School Medical Officer for own branch) · `Advanced Filters` · `Export Directory (PDF)`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no hospital tie-up | "CRITICAL: [N] branch(es) have no tied-up hospital on record. Update the directory immediately." | Red |
| Branch with no ambulance contact | "CRITICAL: [N] branch(es) have no ambulance contact recorded. Add emergency ambulance details now." | Red |
| MOU expired | "⚠ MOU with [N] hospital(s) has/have expired. Renew to maintain cashless admission rights." | Amber |
| Contact number not verified in > 6 months | "⚠ [N] contact(s) have not been verified in over 6 months. Verify to ensure numbers remain active." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule |
|---|---|---|
| Total Contacts | All contacts across all branches and types | Blue always |
| Branches with ≥ 1 Hospital | Branches with at least one tied-up hospital contact | Blue; sub-label shows % of total branches; green if 100% |
| Branches with Ambulance Contact | Branches with at least one ambulance contact | Blue; sub-label shows %; red if < 100% |
| MOUs Active | Contacts where `mou_signed = true` and `mou_expiry >= today` | Blue always |
| Contacts Not Updated in > 12 months | Contacts with `last_verified` > 12 months ago or null | Green = 0 · Amber 1–10 · Red > 10 |

---

## 5. Sections

### 5.1 Main Table — Branch-Wise Directory Overview

Default view. One row per branch.

**Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Missing Hospital | Checkbox | Show only branches with no hospital contact |
| Missing Ambulance | Checkbox | Show only branches with no ambulance contact |
| MOU Status | Radio | All / Active MOU / Expired MOU / No MOU |
| Last Verified | Radio | All / Not verified in > 6 months / Not verified in > 12 months |

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Click → `branch-directory-detail` drawer |
| Hospitals Tied-Up | ✅ | Count; red if 0 |
| Ambulance Services | ✅ | Count; red if 0 |
| Blood Bank | ✅ | Count; amber if 0 |
| On-Call Doctor | ✅ | Count; amber if 0 |
| MOU Status | ✅ | Active / Expired / None — badge |
| Last Verified | ✅ | Most recent verification date across all contacts for this branch; red if > 6 months |
| Actions | ❌ | View · Edit · Verify |

**Default sort:** Branches with missing hospital first (red), then missing ambulance, then alphabetical.
**Pagination:** Server-side · 25 records per page.

---

### 5.2 Contact Detail Sub-table (drill-down from branch row)

Accessed by clicking the **View** action on a branch row, or via the `branch-directory-detail` drawer. Also expandable inline within the main table via HTMX.

One row per contact entry for the selected branch.

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Contact Name | ✅ | Person's name (or organisation name if contact is an entity) |
| Type | ✅ | Hospital / Clinic / Ambulance / Blood Bank / On-Call Doctor / Psychiatrist Referral — badge |
| Organisation | ✅ | Hospital / service name |
| Address | ❌ | Street address; tooltip for full address |
| Primary Phone | ❌ | Clickable tel: link |
| Emergency 24h Phone | ❌ | Clickable tel: link; badge "24h" in green if available |
| Distance from Campus (km) | ✅ | Approximate driving distance |
| Cashless (Insurance) | ✅ | Yes (green badge) / No (grey badge) |
| MOU | ✅ | Yes + expiry date / No |
| Last Verified | ✅ | Date; red if > 6 months ago |
| Actions | ❌ | Edit · Call · Verify |

---

## 6. Drawers / Modals

### 6.1 Drawer — `branch-directory-detail` (700px, right side)

Triggered by branch name link in main table or **View** action.

**Tabs:**

#### Tab 1 — Hospitals
Full details of all hospital and clinic contacts for this branch. Each entry:
- Organisation name, address, Google Maps link (pin opens in new tab), specialities (e.g., trauma, paediatric, gynaecology), bed count (if known), ICU available (yes/no), NICU available (yes/no), primary phone (tel: link), emergency 24h phone (tel: link), cashless (yes/no + insurer names accepted), MOU status and expiry, distance from campus, last verified date and by whom.

#### Tab 2 — Ambulance
All ambulance and emergency transport services. Each entry:
- Service name, operator (private / government / 108 national), primary phone, response time estimate (if known), equipped with: oxygen (yes/no), defibrillator (yes/no), basic trauma kit (yes/no), EMT on board (yes/no), cost (free / paid — approximate ₹), service availability (24h / business hours), last verified.

#### Tab 3 — Blood Bank
Blood bank contacts. Each entry:
- Organisation name, address, map link, phone, blood groups available (checklist: A+, A-, B+, B-, AB+, AB-, O+, O-), platelet availability (yes/no), distance from campus, last verified.

#### Tab 4 — On-Call Doctors
Doctors available for on-call consultation or emergency house visits. Each entry:
- Doctor name, qualification, speciality, clinic/hospital affiliation, primary phone, WhatsApp available (yes/no), consultation hours, emergency call availability (yes/no + hours), fee per visit (₹), last verified.

#### Tab 5 — Psychiatrist Referrals
Mental health professionals available for urgent student referrals. Each entry:
- Name, qualification, clinic affiliation, address, map link, phone, speciality (adolescent / trauma / anxiety / general), languages spoken, session cost (₹), average wait time for new appointment, last verified.

Each tab shows: **+ Add Contact** button (visible to Emergency Response Officer, Medical Coordinator, School Medical Officer for own branch), individual Edit and Verify buttons per contact row.

---

### 6.2 Drawer — `contact-create` (620px, right side)

Triggered by **+ Add Contact**.

| Field | Type | Validation |
|---|---|---|
| Branch | Single-select | Required; auto-filled and locked for School Medical Officer |
| Contact Type | Single-select: Hospital / Clinic / Ambulance / Blood Bank / On-Call Doctor / Psychiatrist Referral | Required |
| Organisation Name | Text input (max 200 chars) | Required |
| Contact Person Name | Text input | Required |
| Primary Phone | Phone number input (10 digits) | Required |
| Emergency 24h Phone | Phone number input | Optional; recommended for hospitals and ambulances |
| Address (Line 1) | Text input | Required |
| Address (City / District) | Text input | Required |
| Google Maps URL | URL input | Optional |
| Distance from Campus (km) | Decimal number input | Required |
| Speciality / Description | Text input (max 200 chars) | Required for Hospital / Clinic / On-Call Doctor |
| Cashless Insurance Available | Radio: Yes / No | Required for Hospital / Clinic |
| Insurers Accepted (if Cashless = Yes) | Multi-select (from policy register) | Required if Cashless = Yes |
| MOU Signed | Radio: Yes / No | Required |
| MOU Number | Text input | Required if MOU = Yes |
| MOU Expiry Date | Date picker | Required if MOU = Yes |
| MOU Document | File upload (PDF, max 15 MB) | Required if MOU = Yes |
| Additional Notes | Textarea (max 500 chars) | Optional |

**Footer:** `Cancel` · `Add Contact`

---

### 6.3 Drawer — `contact-edit` (620px, right side)

Pre-populated with all fields from `contact-create`. All fields editable.

On save: `last_updated` timestamp refreshed; previous values preserved in an edit history log accessible to Emergency Response Officer.

---

### 6.4 Modal — `verify-contact` (440px, centred)

Triggered by **Verify** action on a contact row or branch directory table.

| Field | Type | Validation |
|---|---|---|
| Contact Name | Read-only | |
| Organisation | Read-only | |
| Phone Number Confirmed | Phone input (pre-filled; editable if number has changed) | Required |
| Verification Status | Radio: Contact is still active and number correct / Phone number has changed (update above) / No longer tied-up (deactivate contact) | Required |
| Verified By | Text input (name of person who called to verify) | Required |
| Verification Date | Date picker (default: today) | Required |
| Notes | Textarea (max 300 chars) | Optional |

**Footer:** `Cancel` · `Save Verification`

On save: `last_verified` date updated; `verified_by` recorded. If status = No longer tied-up: contact flagged as Inactive and removed from active directory (retained in archive for audit). If phone changed: contact's phone fields updated and change logged.

---

## 7. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Contact added | "Contact added to [Branch] directory." | Success |
| Contact updated | "[Contact Name] details updated." | Success |
| Contact verified | "[Contact Name] verified as active." | Success |
| Contact marked no longer tied-up | "[Contact Name] marked as inactive and removed from active directory." | Warning |
| MOU document uploaded | "MOU document uploaded for [Organisation Name]." | Success |
| Export initiated | "Branch directory export initiated. Download will be ready shortly." | Info |
| Validation error — duplicate phone | "A contact with this phone number already exists for this branch." | Error |
| Save failed | "Please complete all required fields." | Error |

---

## 8. Empty States

| Context | Heading | Sub-text | Action |
|---|---|---|---|
| No contacts for a branch | "No contacts for this branch." | "Add at least one hospital, ambulance service, and on-call doctor to complete this branch's emergency directory." | `+ Add Contact` |
| Hospital tab empty | "No hospitals on record for this branch." | "Add at least one tied-up hospital to ensure students can receive cashless treatment in an emergency." | `+ Add Contact` |
| Ambulance tab empty | "No ambulance contacts for this branch." | "Add an emergency ambulance contact immediately." | `+ Add Contact` |
| Blood bank tab empty | "No blood bank contacts for this branch." | "Add a blood bank contact for emergency use." | `+ Add Contact` |
| No results for filters | "No branches match your current filters." | "Try adjusting the contact type or verification status filters." | `Clear Filters` |

---

## 9. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Full-page skeleton: 5 KPI cards + branch table (5 grey rows × 8 columns) |
| Filter apply | Table body inline spinner |
| Branch directory detail drawer open | Drawer skeleton: 5 tab headers + contact list skeleton (4 grey rows) |
| Tab switch in drawer | Tab content skeleton (3 grey rows) |
| Contact create / edit save | Submit button spinner; form fields disabled |
| Verify modal submit | Modal footer spinner + "Verifying…" |
| PDF export | Export button spinner + "Preparing directory PDF…"; button replaced with download link when ready |
| Emergency widget load (sidebar) | Single-line placeholder text "Loading emergency contacts…" replaced with phone numbers |

---

## 10. Role-Based UI Visibility

| UI Element | Emergency Response Officer | Medical Coordinator | School Medical Officer | Branch Principal | All Staff |
|---|---|---|---|---|---|
| Full directory (all branches) | ✅ | ✅ | Own branch only | Own branch (branch portal) | ❌ (widget only) |
| + Add Contact button | ✅ | ✅ | ✅ (own branch) | ❌ | ❌ |
| Edit action | ✅ | ✅ | ✅ (own branch) | ❌ | ❌ |
| Verify action | ✅ | ✅ | ✅ (own branch) | ❌ | ❌ |
| Delete / deactivate contact | ✅ | ✅ | ❌ | ❌ | ❌ |
| MOU document upload | ✅ | ✅ | ❌ | ❌ | ❌ |
| MOU document view | ✅ | ✅ | ✅ | ❌ | ❌ |
| Export Directory PDF | ✅ | ✅ | ✅ (own branch) | ✅ (own branch — branch portal) | ❌ |
| KPI bar — all 5 cards | ✅ | ✅ | ❌ | ❌ | ❌ |
| Alert banners | ✅ | ✅ | Own branch alerts | ❌ | ❌ |
| Call button (tel: link) | ✅ | ✅ | ✅ | ✅ | ✅ (widget) |
| Google Maps link | ✅ | ✅ | ✅ | ✅ | ❌ |

---

## 11. API Endpoints

### Base URL: `/api/v1/group/{group_id}/health/hospital-directory/`

| Method | Endpoint | Description | Auth |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/hospital-directory/` | List all branches with contact summary | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/kpi/` | KPI summary bar data | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/alerts/` | Active alert conditions | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/` | Branch contact detail (all types) | JWT + role check + branch scope |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/` | List all contacts for a branch | JWT + role check + branch scope |
| POST | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/` | Add contact to branch | Emergency Response Officer / Medical Coordinator / School Medical Officer (own branch) |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/` | Retrieve contact detail | JWT + role check |
| PATCH | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/` | Update contact | Emergency Response Officer / Medical Coordinator / School Medical Officer (own branch) |
| DELETE | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/` | Deactivate contact (soft delete) | Emergency Response Officer / Medical Coordinator |
| POST | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/verify/` | Verify contact is still active | Emergency Response Officer / Medical Coordinator / School Medical Officer |
| POST | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/documents/` | Upload MOU document | Emergency Response Officer / Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/{branch_id}/contacts/{contact_id}/documents/{doc_id}/` | Download MOU document | JWT + role check |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/export/` | Export full directory as PDF | Emergency Response Officer / Medical Coordinator / School Medical Officer / Branch Principal |
| GET | `/api/v1/group/{group_id}/health/hospital-directory/emergency-widget/` | Emergency quick-access numbers for sidebar widget (returns primary emergency phone per branch for current user's branch) | All authenticated users |

**Query parameters for main list endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `branch` | int[] | Branch filter |
| `missing_hospital` | bool | Show branches with no hospital contact |
| `missing_ambulance` | bool | Show branches with no ambulance contact |
| `mou_status` | str | `active`, `expired`, `none` |
| `last_verified` | str | `6m` (> 6 months), `12m` (> 12 months) |
| `page` | int | Page number |
| `page_size` | int | Default 25; max 100 |

**Query parameters for branch contacts endpoint:**

| Parameter | Type | Description |
|---|---|---|
| `type` | str[] | `hospital`, `clinic`, `ambulance`, `blood_bank`, `on_call_doctor`, `psychiatrist` |

---

## 12. HTMX Patterns

| Interaction | HTMX Attributes | Behaviour |
|---|---|---|
| Filter apply | `hx-get="/api/.../hospital-directory/"` `hx-trigger="change"` `hx-target="#directory-table-body"` `hx-include="#filter-form"` | Branch table rows replaced |
| KPI bar load | `hx-get="/api/.../hospital-directory/kpi/"` `hx-trigger="load"` `hx-target="#kpi-bar"` | On page load |
| Alert banner load | `hx-get="/api/.../hospital-directory/alerts/"` `hx-trigger="load"` `hx-target="#alert-banner"` | On page load |
| Pagination | `hx-get="/api/.../hospital-directory/?page={n}"` `hx-target="#directory-table-body"` `hx-push-url="true"` | Page swap |
| Branch sub-table inline expand | `hx-get="/api/.../hospital-directory/{branch_id}/contacts/"` `hx-target="#subtable-{branch_id}"` `hx-trigger="click"` `hx-swap="innerHTML"` | Contact sub-table inserted below branch row; toggle on second click collapses it |
| Branch directory detail drawer open | `hx-get="/api/.../hospital-directory/{branch_id}/"` `hx-target="#drawer-container"` `hx-trigger="click"` | Drawer slides in; Hospitals tab default |
| Drawer tab switch | `hx-get="/api/.../hospital-directory/{branch_id}/contacts/?type={tab_type}"` `hx-target="#drawer-tab-content"` `hx-trigger="click"` | Tab content loaded by contact type |
| Contact create submit | `hx-post="/api/.../hospital-directory/{branch_id}/contacts/"` `hx-target="#contact-list-{branch_id}"` `hx-swap="beforeend"` `hx-on::after-request="closeDrawer(); fireToast(); refreshKPI();"` | New contact row appended to relevant tab; KPI refreshed |
| Contact edit submit | `hx-patch="/api/.../hospital-directory/{branch_id}/contacts/{contact_id}/"` `hx-target="#contact-row-{contact_id}"` `hx-swap="outerHTML"` | Contact row updated in-place |
| Verify modal submit | `hx-post="/api/.../hospital-directory/{branch_id}/contacts/{contact_id}/verify/"` `hx-target="#contact-row-{contact_id}"` `hx-swap="outerHTML"` `hx-on::after-request="closeModal(); fireToast();"` | Contact row's Last Verified column updated; modal closed |
| Export PDF initiate | `hx-get="/api/.../hospital-directory/export/"` `hx-target="#export-status"` `hx-trigger="click"` | Export button replaced with "Preparing PDF…" spinner; download link appears when ready |
| Emergency widget load (sidebar) | `hx-get="/api/.../hospital-directory/emergency-widget/"` `hx-trigger="load"` `hx-target="#emergency-widget"` | Sidebar widget populated with branch emergency numbers on every page load |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
