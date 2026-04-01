# [10] — Vendor & Third-Party Legal Agreements

> **URL:** `/group/legal/vendor-agreements/`
> **File:** `n-10-vendor-legal-agreements.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Contract Administrator (Role 127, G3) — vendor/supplier contracts, AMCs, MOUs, service agreements lifecycle

---

## 1. Purpose

The Vendor & Third-Party Legal Agreements page manages all commercial agreements between the Institution Group and external vendors, suppliers, and service providers. This includes: supply agreements with book and uniform suppliers; maintenance AMCs (Annual Maintenance Contracts) for lab equipment, CCTV, and buses; technology vendor contracts (ERP, video platform, WhatsApp gateway); MOU agreements with coaching institutes or universities; lease agreements for branch premises; and outsourced service contracts (security, housekeeping, catering).

The Group Contract Administrator (Role 127, G3) is the primary user, responsible for the full contract lifecycle: creating records, uploading signed agreements, tracking renewal dates, and triggering renewal workflows before expiry. Expired vendor contracts represent legal risk — the group may continue receiving services without a valid agreement, creating liability for payment disputes and warranty claims.

This page is separate from the Staff Contracts Registry (N-07) which covers employment contracts. The Compliance Manager (Role 109, G1) has read-only oversight for compliance-critical vendor contracts (especially those involving personal data processing, which must have DPDP-compliant DPA clauses).

Scale: 5–50 branches · 10–200 vendor contracts group-wide · Renewal cycles: AMCs annual, supply agreements biannual, technology SaaS annual

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews complex vendor contracts externally |
| Group Compliance Manager | 109 | G1 | Read — Compliance-relevant contracts | Views contracts with DPA requirements or regulatory implications |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | Read — Data processing contracts | Views contracts where vendor processes personal data; checks DPA clause |
| Group Contract Administrator | 127 | G3 | Full CRUD — primary operator | All create, upload, update, renew, terminate |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Disputed contracts | Views contracts involved in vendor disputes |
| Group Insurance Coordinator | 129 | G1 | Read — Insurance-covered vendor liability | Views contracts covered by liability insurance |

> **Access enforcement:** `@require_role(roles=[109,113,127,128,129], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Vendor & Third-Party Agreements
```

### 3.2 Page Header
```
Vendor & Third-Party Legal Agreements           [+ New Agreement]  [Export ↓]
Group Contract Administrator — [Name]
[Group Name] · [N] Active Agreements · [N] Expiring (60d) · Total Value: ₹[amount]/year
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Agreements expired (services potentially continuing without contract) | "[N] vendor agreement(s) have expired. Services may be running without legal cover." | Critical (red) |
| Agreements expiring within 30 days | "[N] vendor agreement(s) expire within 30 days. Initiate renewal." | High (amber) |
| Data processing vendor without signed DPA | "[N] vendor(s) processing personal data have no signed Data Processing Agreement — DPDP Act s.8(6) violation." | High (amber) |
| High-value agreement expiring | "Agreement with [Vendor] (₹[value]/year) expires in [N] days. Renewal approval required from CEO." | Medium (yellow) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Agreements | Count | COUNT WHERE status = 'active' | Blue | `#kpi-active` |
| 2 | Expiring (60 Days) | Count | COUNT WHERE expiry BETWEEN TODAY AND TODAY+60 | Red > 5, Amber 1–5, Green = 0 | `#kpi-expiring-60d` |
| 3 | Expired (Unrenewed) | Count | COUNT WHERE expiry < TODAY AND status != 'renewed' | Red if > 0, Green = 0 | `#kpi-expired` |
| 4 | Data Vendors Without DPA | Count | COUNT WHERE processes_personal_data = True AND dpa_signed = False | Red if > 0, Green = 0 | `#kpi-dpa-missing` |
| 5 | Pending Signature | Count | COUNT WHERE signature_status = 'pending' | Amber > 3, Green ≤ 3 | `#kpi-pending-sig` |
| 6 | Total Annual Contract Value | Sum (₹) | SUM annual_value WHERE status = 'active' | Blue (info metric) | `#kpi-total-value` |
| 7 | Agreements (This FY) | Count | COUNT WHERE created_fy = current | Blue | `#kpi-created-fy` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/vendor-agreements/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Vendor Agreements Table

**Search:** Vendor name, agreement type, branch, service description. Debounced 350ms.

**Filters:**
- Agreement Type: `All` · `Supply Agreement` · `Service Contract` · `AMC` · `MOU` · `Lease` · `Technology/SaaS` · `Outsourcing` · `NDA` · `Other`
- Status: `All` · `Active` · `Expiring Soon` · `Expired` · `Terminated` · `Draft`
- Branch: dropdown (+ Group Level)
- Processes Personal Data: `All` · `Yes` · `No`
- DPA Status: `Signed` · `Missing` · `Not Required`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Agreement ID | Monospace | Yes | AUTO: VEN-YYYYMMDD-NNNN |
| Vendor Name | Text | Yes | |
| Service Description | Text | Yes | Brief, 60 chars |
| Agreement Type | Badge | Yes | |
| Branch / Scope | Text | Yes | Specific branch or "All Branches" |
| Start Date | Date | Yes | |
| End Date | Date | Yes | Red < 30d, amber < 60d |
| Annual Value (₹) | Currency | Yes | |
| DPA | Badge | Yes | Signed ✅ / Missing ❌ / N/A |
| Signature Status | Badge | Yes | Signed / Pending / N/A |
| Status | Badge | Yes | Active / Expiring / Expired / Terminated / Draft |
| Actions | Buttons | No | [View] · [Renew] · [Edit] (Role 127 only) |

**Default sort:** End Date ASC
**Pagination:** Server-side · Default 25/page · Page size: 25/50/100

---

## 6. Drawers & Modals

### 6.1 Drawer: `vendor-agreement-detail` (720px)
- **Tabs:** Overview · Agreement Document · DPA Details · Renewal History · Notes
- **Overview tab:** Agreement ID, Vendor, Service, Type, Branch/Scope, Value, Start/End, Status, Signature details, Processes personal data toggle, Vendor contact details
- **Agreement Document tab:** Uploaded PDFs with version history, [Download], [Upload New Version]
- **DPA Details tab (if processes personal data):** DPA signed toggle, DPA version, DPA expiry, Data categories processed, Processing purpose, Vendor's data residency, Breach notification clause status
- **Renewal History tab:** Past contract cycles — dates, value, status
- **Notes tab:** Internal notes; editable by Role 127

### 6.2 Modal: `create-vendor-agreement` (680px)
| Field | Type | Required |
|---|---|---|
| Vendor Name | Text | Yes |
| Vendor PAN / GST | Text | No |
| Service Description | Text (100 chars) | Yes |
| Agreement Type | Select | Yes |
| Branch / Scope | Select (multi-select) | Yes |
| Start Date | Date picker | Yes |
| End Date | Date picker | Conditional |
| Annual Value (₹) | Number | No |
| Processes Personal Data | Toggle | Yes |
| DPA Included | Toggle | Conditional (if personal data = Yes) |
| Signature Method | Select | Yes |
| Agreement Document | File | Yes (PDF, max 20MB) |
| Notes | Textarea | No |

**Footer:** Cancel · Save Draft · Create Agreement

### 6.3 Modal: `renew-vendor-agreement` (560px)
Same structure as staff contract renewal modal but for vendor agreements.

---

## 7. Charts

### 7.1 Agreements by Type — Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Active Agreements by Type" |
| Data | Count per agreement type |
| Colour | Each type distinct colour |
| Tooltip | "[Type]: [N] agreements, ₹[total_value]/year" |
| API endpoint | `GET /api/v1/group/{id}/legal/vendor-agreements/by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-vendor-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Contract Value by Branch — Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Annual Contract Value by Branch" |
| Data | Sum of annual_value per branch |
| Colour | `#3B82F6` |
| Tooltip | "[Branch]: ₹[total]/year across [N] vendors" |
| API endpoint | `GET /api/v1/group/{id}/legal/vendor-agreements/value-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-vendor-value-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Agreement created | "Agreement [VEN-ID] created with [Vendor]." | Success | 4s |
| Renewal initiated | "Renewal created for [VEN-ID]. Previous agreement marked Renewed." | Success | 4s |
| DPA missing alert | "Warning: [Vendor] processes personal data but has no signed DPA." | Warning | 6s |
| Agreement expired alert | "[Vendor]'s agreement expired [N] days ago — renew immediately." | Error | 6s |
| Export triggered | "Generating vendor agreements export…" | Info | 3s |
| Document uploaded | "Document uploaded to [VEN-ID]." | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No vendor agreements | `briefcase` | "No Vendor Agreements" | "Add vendor and supplier agreements to track contract status." | Create First Agreement |
| Filter returns no results | `search` | "No Matching Agreements" | "No agreements match the selected filters." | Clear Filters |
| All agreements current | `check-circle` | "All Agreements Up to Date" | "All vendor agreements are active and current." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI + 10-row table |
| Table filter/search | Spinner overlay |
| Drawer open | Right-slide skeleton |
| Charts | Grey canvas + spinner |
| File upload | Progress bar in modal |

---

## 11. Role-Based UI Visibility

| Element | Contract Admin (127) | Compliance Mgr (109) | DPO (113) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|---|---|
| Full agreements table | Visible | Compliance-related | Data processing vendors | Disputed contracts | Full |
| [+ New Agreement] | Visible | Not visible | Not visible | Not visible | Visible |
| Annual value column | Visible | Not visible | Not visible | Not visible | Visible |
| DPA details tab | Visible | Not visible | Full access | Not visible | Visible |
| Export | Visible | Not visible | Not visible | Not visible | Visible |
| Charts | Both | Both (read-only) | Not visible | Not visible | Both |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/vendor-agreements/` | G1+ (scoped) | Paginated list |
| POST | `/api/v1/group/{id}/legal/vendor-agreements/` | Role 127, G4+ | Create agreement |
| GET | `/api/v1/group/{id}/legal/vendor-agreements/{vid}/` | G1+ | Detail |
| PATCH | `/api/v1/group/{id}/legal/vendor-agreements/{vid}/` | Role 127, G4+ | Update |
| POST | `/api/v1/group/{id}/legal/vendor-agreements/{vid}/renew/` | Role 127, G4+ | Create renewal |
| GET | `/api/v1/group/{id}/legal/vendor-agreements/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/legal/vendor-agreements/by-type/` | Role 127, G4+ | Chart data |
| GET | `/api/v1/group/{id}/legal/vendor-agreements/value-by-branch/` | Role 127, G4+ | Chart data |
| POST | `/api/v1/group/{id}/legal/vendor-agreements/export/` | G1+ | Async export |

### Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: vendor, type, description |
| `agreement_type` | string | supply / service / amc / mou / lease / technology / outsourcing / nda / other |
| `status` | string | active / expiring / expired / terminated / draft |
| `branch_id` | integer | Filter by branch |
| `processes_personal_data` | boolean | |
| `dpa_status` | string | signed / missing / not_required |
| `expiry_within_days` | integer | |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100 |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../vendor-agreements/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | Table body | GET `.../vendor-agreements/` | `#vendor-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET with `?q=` | `#vendor-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Type filter | Type select | GET with `?agreement_type=` | `#vendor-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open drawer | [View] / row | GET `.../vendor-agreements/{vid}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create modal | [+ New Agreement] | GET `/htmx/legal/vendor-agreements/create-form/` | `#modal-container` | `innerHTML` | |
| Charts | Chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#vendor-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
