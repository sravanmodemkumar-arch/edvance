# [07] — Staff Contracts Registry

> **URL:** `/group/legal/staff-contracts/`
> **File:** `n-07-staff-contracts-registry.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Contract Administrator (Role 127, G3) — employment contracts lifecycle management for all staff across all branches

---

## 1. Purpose

The Staff Contracts Registry manages the complete lifecycle of employment and service agreements for all staff across every branch in the Institution Group. This includes appointment letters, service agreements, confidentiality agreements (NDAs), non-compete clauses, renewal letters, and termination documents. For a large group with 3,000+ staff across 50 branches, the absence of a centralised contract registry leads to expired contracts, inconsistent terms, unsigned agreements, and significant legal exposure.

The Group Contract Administrator (Role 127, G3) is the sole role with full CRUD access on this page. The Compliance Manager (Role 109, G1) and CEO (G4) have read-only oversight. The Contract Administrator is responsible for: generating and uploading contracts; tracking signature status (physical or digital); sending renewal reminders before expiry; and ensuring all staff with student access have valid NDAs on file.

Contracts are linked to the HR module staff records. When a new staff member is onboarded via Division E (HR), a contract record is automatically created here in "Pending Draft" status. The Contract Administrator drafts, uploads, and manages the signature workflow.

Scale: 5–50 branches · 50–3,000 staff members · 200–15,000 contract records (including historical) · Contract renewal cycle typically annual for teachers

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews contract templates externally |
| Group Compliance Manager | 109 | G1 | Read — Full Page | Oversight; views all contracts, no edit |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | Read — NDA status only | Verifies NDAs are on file for staff with data access |
| Group Contract Administrator | 127 | G3 | Full CRUD — primary operator | Create, upload, update, renew, terminate contracts |
| Group Legal Dispute Coordinator | 128 | G1 | Read — contracts in dispute | Views contracts involved in legal disputes |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,113,127,128], min_level=G1)` with CRUD restricted to Role 127, G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Staff Contracts Registry
```

### 3.2 Page Header
```
Staff Contracts Registry                        [+ New Contract]  [Export ↓]
Group Contract Administrator — [Officer Name]
[Group Name] · [N] Active Contracts · [N] Expiring (60d) · FY [year]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Contracts expiring within 30 days | "[N] staff contract(s) expire within 30 days. Renewal action required." | High (amber) |
| Contracts already expired (not renewed) | "[N] staff contract(s) have expired and not been renewed. Legal risk — immediate action." | Critical (red) |
| Unsigned contracts > 14 days old | "[N] draft contract(s) have been unsigned for more than 14 days." | Medium (yellow) |
| Staff with data access missing NDA | "[N] staff member(s) with data access do not have a signed NDA on file." | High (amber) |
| New staff onboarded without contract | "[N] staff onboarded via HR module have no contract record. Create contracts." | Medium (yellow) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Active Contracts | Count | COUNT WHERE status = 'active' | Blue | `#kpi-active-contracts` |
| 2 | Expiring (60 Days) | Count | COUNT WHERE expiry_date BETWEEN TODAY AND TODAY+60 | Red > 10, Amber 5–10, Green ≤ 5 | `#kpi-expiring-60d` |
| 3 | Expired (Not Renewed) | Count | COUNT WHERE expiry_date < TODAY AND status != 'renewed' | Red if > 0, Green = 0 | `#kpi-expired` |
| 4 | Pending Signature | Count | COUNT WHERE signature_status = 'pending' | Amber > 5, Green ≤ 5 | `#kpi-pending-sig` |
| 5 | NDAs on File | Percentage | staff with NDA / total staff × 100 | Green ≥ 95%, Amber 80–94%, Red < 80% | `#kpi-nda-coverage` |
| 6 | Contracts This Month | Count | COUNT created in current calendar month | Blue | `#kpi-created-month` |
| 7 | Terminated (This FY) | Count | COUNT WHERE status = 'terminated' AND fy = current | Blue | `#kpi-terminated` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/staff-contracts/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Contract List (Main Table)

All staff employment contracts across all branches.

**Search:** Staff name, employee ID, branch, contract type. Debounced 350ms.

**Filters:**
- Status: `All` · `Active` · `Expiring Soon` · `Expired` · `Terminated` · `Draft` · `Pending Signature`
- Contract Type: `All` · `Appointment Letter` · `Service Agreement` · `NDA` · `Non-Compete` · `Renewal` · `Termination Letter` · `Addendum`
- Branch: dropdown
- Staff Category: `Teaching` · `Non-Teaching` · `Hostel` · `Transport` · `Management`
- Signature Status: `All` · `Signed` · `Pending` · `Not Required`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Contract ID | Monospace | Yes | AUTO: CON-YYYYMMDD-NNNN |
| Staff Name | Text | Yes | Linked to HR staff record |
| Employee ID | Monospace | Yes | From HR module |
| Branch | Text | Yes | |
| Role / Designation | Text | Yes | e.g., "Senior Physics Teacher" |
| Contract Type | Badge | Yes | Colour by type |
| Start Date | Date | Yes | |
| End Date / Expiry | Date | Yes | Red if < 30d, amber if < 60d |
| Days to Expiry | Badge | Yes | Integer; red if negative (expired) |
| Signature Status | Badge | Yes | Signed (green) / Pending (amber) / Not Required (grey) |
| NDA on File | Badge | No | Yes (green) / No (red) / N/A (grey) |
| Status | Badge | Yes | Active / Expiring / Expired / Terminated / Draft |
| Actions | Buttons | No | [View] · [Edit] · [Renew] (Role 127 only) |

**Default sort:** End Date ASC (expiring soonest first)
**Pagination:** Server-side · Default 25/page · Page size: 25/50/100

---

### 5.2 Expiry Forecast Tab

Dedicated view showing only contracts expiring in the next 90 days, grouped by month.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Month | Header row | Group header: "Expiring in [Month Year] — [N] contracts" |
| Staff Name | Text | |
| Branch | Text | |
| Contract Type | Badge | |
| Expiry Date | Date | |
| Days Left | Badge | Red < 30, Amber 30–60, Yellow 61–90 |
| Renewal Status | Badge | Renewal Initiated / Not Started |
| Actions | Buttons | [Initiate Renewal] (Role 127) |

---

## 6. Drawers & Modals

### 6.1 Drawer: `contract-detail` (720px, right-slide)
- **Tabs:** Overview · Contract Document · Signature · Renewal History · Notes
- **Overview tab:**
  - Contract ID, Staff Name (link → HR profile), Employee ID, Branch, Designation
  - Contract Type badge, Start Date, End Date, Duration
  - Status badge, Termination Date (if terminated)
  - Created By (Contract Admin), Created Date, Last Modified
  - Key Terms Summary (free text, max 500 chars)
  - Linked HR Onboarding Record (link)
- **Contract Document tab:**
  - Uploaded contract PDFs — filename, version, upload date, uploaded by, [Download] button
  - [Upload New Version] button (Role 127 only)
  - Version history table
- **Signature tab:**
  - Signature Method: Physical / DigiSign / DocuSign
  - Staff Signature: Signed Date / Pending / Not Required
  - Authorised Signatory (Group): Signed Date / Pending
  - If DigiSign: webhook status, reference, [Resend Request] button (Role 127)
- **Renewal History tab:** All past contract versions — start date, end date, type, status, uploaded by
- **Notes tab:** Internal notes; Role 127 can add/edit; G1 roles read-only

### 6.2 Modal: `create-contract` (680px)
Used by Contract Administrator to create a new contract record.

| Field | Type | Required | Validation |
|---|---|---|---|
| Staff Member | Search + Select (linked to HR) | Yes | Must exist in HR module |
| Branch | Auto-filled from staff record | — | Read-only |
| Contract Type | Select | Yes | |
| Start Date | Date picker | Yes | |
| End Date | Date picker | Conditional | Required unless perpetual (for permanent appointments) |
| Perpetual Contract | Toggle | No | Disables End Date if checked |
| Signature Method | Select | Yes | Physical / DigiSign |
| Contract Document | File upload | Yes | PDF only, max 20MB |
| Key Terms Summary | Textarea | No | Max 500 chars |
| NDA Included | Toggle | Yes | Yes / No |
| Notes | Textarea | No | |

**Footer:** Cancel · Save as Draft · Create Contract

### 6.3 Modal: `renew-contract` (560px)
| Field | Type | Required | Validation |
|---|---|---|---|
| Original Contract | Display | — | Shows contract ID, staff name, expiry |
| New Start Date | Date picker | Yes | Must be on or before original end date |
| New End Date | Date picker | Yes | Must be after new start date |
| Renewal Terms Changed | Toggle | No | If Yes: show Changes Description textarea |
| Updated Contract Document | File upload | Conditional | Required if terms changed |

**Footer:** Cancel · Initiate Renewal
**On success:** New contract record created with status Active; previous record marked Renewed.

### 6.4 Modal: `export-contracts` (480px)
- **Fields:** Branch filter, Contract type, Status, Expiry date range, Format (Excel/PDF)
- **Buttons:** Cancel · Export

---

## 7. Charts

### 7.1 Contract Expiry by Month (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Contract Expiries by Month — Next 12 Months" |
| Data | Count of contracts expiring per month |
| X-axis | Month (next 12 months) |
| Y-axis | Contract count |
| Colour | `#F59E0B` for upcoming, `#EF4444` for already expired |
| Tooltip | "[Month]: [N] contracts expiring" |
| API endpoint | `GET /api/v1/group/{id}/legal/staff-contracts/expiry-forecast/` |
| HTMX | `hx-get` on load → `hx-target="#chart-expiry-forecast"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Contracts by Type — Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Active Contracts by Type" |
| Data | Count per contract type |
| Colour | Each type a distinct colour |
| Tooltip | "[Type]: [N] contracts ([X]%)" |
| API endpoint | `GET /api/v1/group/{id}/legal/staff-contracts/by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-contracts-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Contract created | "Contract [CON-ID] created for [Staff Name]." | Success | 4s |
| Renewal initiated | "Renewal contract created for [Staff Name]. Previous contract marked Renewed." | Success | 4s |
| Contract expired alert | "[Staff Name]'s contract at [Branch] expired [N] days ago. Renew immediately." | Error | 6s |
| Signature reminder sent | "Signature reminder sent to [Staff Name] via [method]." | Info | 3s |
| Export triggered | "Generating contracts export…" | Info | 3s |
| Export ready | "Contracts export ready. Click to download." | Success | 6s |
| Draft saved | "Contract draft saved for [Staff Name]." | Info | 3s |
| Validation error | "Please complete all required fields." | Error | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No contracts in registry | `file-text` | "No Contracts in Registry" | "Upload employment contracts for staff across all branches." | Create First Contract |
| Filter returns no results | `search` | "No Matching Contracts" | "No contracts match the selected filters." | Clear Filters |
| All contracts current | `check-circle` | "All Contracts Up to Date" | "All staff employment contracts are active and current." | View Expiry Forecast |
| Expiry forecast tab empty | `calendar-check` | "No Expiries in Next 90 Days" | "No contracts are due for renewal in the next 90 days." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI shimmer cards + 10-row table skeleton |
| Table search/filter | Spinner overlay on table body |
| Drawer open | Right-slide skeleton with tab placeholders |
| Charts | Grey canvas + centred spinner |
| Export generation | Toast with progress indicator |
| Contract upload | Button spinner + progress bar (for large PDFs) |
| Signature status webhook update | Inline spinner in signature status badge |

---

## 11. Role-Based UI Visibility

| Element | Contract Admin (127, G3) | Compliance Mgr (109, G1) | DPO (113, G1) | Legal Dispute (128, G1) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| Full contract table | Visible | Visible | NDA column only | Visible | Visible |
| [+ New Contract] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Edit] / [Renew] buttons | Visible | Not visible | Not visible | Not visible | Visible |
| Export buttons | Visible | Visible | Not visible | Not visible | Visible |
| Contract document download | Visible | Not visible | Not visible | Visible (dispute-related) | Visible |
| Signature tab — resend | Visible | Not visible | Not visible | Not visible | Visible |
| Charts | Both visible | Both visible | Not visible | Not visible | Both visible |
| Alert banners | All | All | NDA missing only | Expired/dispute only | All |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/staff-contracts/` | G1+ | Paginated contract list |
| POST | `/api/v1/group/{id}/legal/staff-contracts/` | Role 127, G4+ | Create new contract |
| GET | `/api/v1/group/{id}/legal/staff-contracts/{con_id}/` | G1+ | Contract detail |
| PATCH | `/api/v1/group/{id}/legal/staff-contracts/{con_id}/` | Role 127, G4+ | Update contract |
| POST | `/api/v1/group/{id}/legal/staff-contracts/{con_id}/renew/` | Role 127, G4+ | Create renewal contract |
| GET | `/api/v1/group/{id}/legal/staff-contracts/kpis/` | G1+ | KPI summary |
| GET | `/api/v1/group/{id}/legal/staff-contracts/expiry-forecast/` | G1+ | Monthly expiry chart |
| GET | `/api/v1/group/{id}/legal/staff-contracts/by-type/` | G1+ | Contracts by type donut |
| POST | `/api/v1/group/{id}/legal/staff-contracts/export/` | G1+ | Async export |
| POST | `/api/v1/group/{id}/legal/staff-contracts/{con_id}/signature-reminder/` | Role 127, G4+ | Resend signature request |

### Query Parameters for Contract List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: staff name, employee ID, branch |
| `status` | string | active / expiring / expired / terminated / draft / pending_signature |
| `contract_type` | string | appointment / service / nda / non_compete / renewal / termination / addendum |
| `branch_id` | integer | Filter by branch |
| `staff_category` | string | teaching / non_teaching / hostel / transport / management |
| `signature_status` | string | signed / pending / not_required |
| `expiry_within_days` | integer | Contracts expiring within N days |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100; default 25 |
| `sort` | string | end_date / staff_name / branch / contract_type |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | `<div id="kpi-bar">` | GET `.../staff-contracts/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Contract table load | `<tbody id="contracts-table-body">` | GET `.../staff-contracts/` | `#contracts-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET `.../staff-contracts/?q={v}` | `#contracts-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Status filter | Status chips | GET `.../staff-contracts/?status={v}` | `#contracts-table-body` | `innerHTML` | `hx-trigger="click"` |
| Type filter | Type dropdown | GET `.../staff-contracts/?contract_type={v}` | `#contracts-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open detail drawer | Row click / [View] | GET `.../staff-contracts/{con_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create contract modal | [+ New Contract] | GET `/htmx/legal/contracts/create-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Renew contract modal | [Renew] button | GET `/htmx/legal/contracts/{con_id}/renew-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit create form | Form | POST `.../staff-contracts/` | `#contracts-table-body` | `afterbegin` | Prepends new row |
| Expiry forecast tab | Tab click | GET `.../staff-contracts/?expiry_within_days=90&sort=end_date` | `#expiry-tab-content` | `innerHTML` | Lazy load |
| Chart loads | Chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET `.../staff-contracts/?page={n}` | `#contracts-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
