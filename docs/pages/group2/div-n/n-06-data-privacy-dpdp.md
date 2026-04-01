# [06] — Data Privacy & DPDP Compliance

> **URL:** `/group/legal/data-privacy/`
> **File:** `n-06-data-privacy-dpdp.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Data Privacy Officer (Role 113, G1) — DPDP Act 2023 compliance, consent management, breach notification

---

## 1. Purpose

The Data Privacy & DPDP Compliance page manages the Institution Group's obligations under the Digital Personal Data Protection Act 2023 (DPDP Act). As a "Data Fiduciary" under the Act, the group collects and processes personal data of students, parents, and staff across all branches — including name, contact details, UID/Aadhaar numbers, academic records, health information, and biometric data. Failure to comply can result in penalties up to ₹250 crore for a data breach and ₹10,000 per individual for failure to comply with data principal requests.

The Group Data Privacy Officer (DPO) uses this page to: track active consent records and coverage; manage Data Subject Requests (DSRs) — access, correction, erasure, and grievance; monitor data breach incidents; maintain the sub-processor register (third parties processing data on the group's behalf); and ensure the 72-hour breach notification to CERT-In and the Data Protection Board is met.

The page also tracks DPDP-specific requirements: purpose limitation (data used only for stated purpose), storage limitation (data retained only as long as necessary), data localisation (personal data stored in India), and children's data obligations (additional consent for minor data subjects under 18).

Scale: 5–50 branches · 2,000–1,00,000 data subjects · Consent records per student/parent · 72-hour breach notification window

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Advises on legal basis externally |
| Group Compliance Manager | 109 | G1 | Read — Overview Only | Sees aggregate stats; no individual DSR details |
| Group RTI Officer | 110 | G1 | No Access | RTI and DPDP are separate regimes |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | No role in DPDP |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | Full Read + Update DSR Status + Upload Breach Report | Primary user |
| Group Contract Administrator | 127 | G3 | Read — Sub-processor contracts only | Views DPA clauses in vendor contracts |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Breach incidents only | Tracks if breach leads to Data Protection Board proceedings |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[113,109,127,128], min_level=G1)` with field-level scoping. G4/G5 have full read access.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Data Privacy & DPDP Compliance
```

### 3.2 Page Header
```
Data Privacy & DPDP Compliance                  [Export DPO Report]
Group Data Privacy Officer — [Officer Name]
[Group Name] · [N] Branches · [N] Active Consent Records · Last sync: [datetime]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any data breach not notified to CERT-In within 72 hours | "CRITICAL: Data breach at [Branch] — [X]h elapsed. CERT-In notification required within 72h — DPDP Act s.8(6)." | Critical (red, sticky) |
| Any DSR not responded to within 30 days | "[N] Data Subject Request(s) are overdue — 30-day response limit exceeded." | High (amber) |
| Any DSR due within 7 days | "[N] DSR(s) require response within 7 days." | Medium (yellow) |
| Consent coverage below 80% for any branch | "[N] branch(es) have consent coverage below 80% — DPDP Act s.6 requires explicit consent." | Medium (yellow) |
| Sub-processor contract expiring within 60 days | "Data Processing Agreement with [Vendor] expires in [N] days. Renew to maintain DPDP s.8(6) compliance." | Medium (yellow) |

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Data Subjects | Count | COUNT unique students + parents + staff in group | Blue | `#kpi-data-subjects` |
| 2 | Consent Coverage | Percentage | subjects with valid consent / total × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-consent-coverage` |
| 3 | Pending DSRs | Count | COUNT dsr WHERE status IN ('received','in_progress') | Red if any overdue within set, Amber > 3, Green ≤ 3 | `#kpi-dsr-pending` |
| 4 | Overdue DSRs | Count | COUNT dsr WHERE due_date < TODAY AND status != 'resolved' | Red if > 0, Green = 0 | `#kpi-dsr-overdue` |
| 5 | Active Data Breaches | Count | COUNT breaches WHERE status != 'closed' | Red if > 0, Green = 0 | `#kpi-breaches-active` |
| 6 | CERT-In Notified | Count (this FY) | COUNT breaches WHERE cert_in_notified = True | Green if = total breaches; Red if any pending | `#kpi-cert-in-notified` |
| 7 | Sub-processors Registered | Count | COUNT active sub-processor records | Blue | `#kpi-sub-processors` |
| 8 | Branches with DPA Signed | Count | COUNT branches where data_processing_agreement_signed = True | Green if = total; Red if any unsigned | `#kpi-dpa-signed` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/data-privacy/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Data Subject Requests (DSR) Table

Tracks all formal requests from students, parents, or staff exercising DPDP Act rights.

**Search:** Free-text on DSR ID, requester type, subject/description. Debounced 350ms.

**Filters:**
- Request Type: `All` · `Data Access` · `Data Correction` · `Data Erasure` · `Portability` · `Consent Withdrawal` · `Grievance`
- Status: `All` · `Received` · `In Progress` · `Resolved` · `Rejected` · `Overdue`
- Branch: dropdown
- Period: FY selector

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| DSR ID | Text (monospace) | Yes | Auto: DSR-YYYY-NNNN |
| Received Date | Date | Yes | |
| Requester Type | Badge | Yes | Student / Parent / Staff |
| Request Type | Badge | Yes | Colour-coded by type |
| Branch Concerned | Text | Yes | |
| Due Date | Date | Yes | Received + 30 days |
| Days Left | Badge | Yes | Red if negative |
| Status | Badge | Yes | Received / In Progress / Resolved / Rejected / Overdue |
| Response Mode | Text | No | Email / Portal / Post (shown if resolved) |
| Actions | Buttons | No | [View] · [Update Status] (Role 113 only) |

**Default sort:** Due Date ASC
**Pagination:** Server-side · Default 25/page

---

### 5.2 Data Breach Register

Tracks all actual or suspected personal data breaches.

**Search:** Breach ID, branch, description keywords. Debounced 350ms.

**Filters:** Status: `All` · `Open` · `CERT-In Notified` · `DPB Notified` · `Closed`; Branch dropdown

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Breach ID | Monospace | Yes | AUTO: BRH-YYYY-NNNN |
| Detected Date | Date + Time | Yes | When breach was discovered |
| Branch | Text | Yes | |
| Type | Badge | Yes | Unauthorised Access / Data Loss / Ransomware / Accidental Disclosure / Other |
| Records Affected | Integer | Yes | Approximate count of affected data subjects |
| Data Categories | Tags | No | Names / Contact / Financial / Health / Biometric / Academic |
| Hours Since Detection | Integer | Yes | Red if > 72 and CERT-In not notified |
| CERT-In Notified | Badge | Yes | Submitted ✅ / Pending ⚠️ — **72h window** from detection (IT Act 2000 + CERT-In Directions 2022) |
| DPB Notified | Badge | No | Submitted / Pending / Not Required — **72h window** from detection for reportable breaches (DPDP Act s.8(6)); applicability determined by DPB rules |
| Status | Badge | Yes | Open / Under Investigation / Closed |
| Actions | Buttons | No | [View] · [Record Notification] (Role 113) |

**Default sort:** Detected Date DESC

---

### 5.3 Sub-Processor Register

Third parties (vendors, SaaS tools) that process personal data on behalf of the group.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Vendor Name | Text | Yes | |
| Service Type | Text | Yes | e.g., "WhatsApp OTP Gateway", "Cloud Storage", "Video Learning Platform" |
| Data Categories Processed | Tags | No | |
| Data Location | Badge | Yes | India / Abroad — red if Abroad (DPDP requires India residency for most categories) |
| DPA Signed | Badge | Yes | Yes (green) / No (red) |
| DPA Expiry | Date | Yes | Date Data Processing Agreement expires |
| Security Assessment | Badge | No | Done / Pending |
| Actions | Buttons | No | [View] |

---

## 6. Drawers & Modals

### 6.1 Drawer: `dsr-detail` (680px, right-slide)
- **Tabs:** Overview · Communication · Documents · Resolution · Timeline
- **Overview tab:** DSR ID, Received Date, Requester Type, Request Type, Branch, Description of request, Due Date, Legal basis (DPDP Act sections cited), Status
- **Communication tab:** All correspondence with requester (emails/letters) listed chronologically with download links
- **Documents tab:** Supporting docs from requester; identity verification document; response document
- **Resolution tab (Role 113):**
  - Resolution Type: Fulfilled / Rejected / Partially Fulfilled
  - If Rejected: Reason (with DPDP s.12 exemption if applicable)
  - Response Document upload (PDF, max 10MB)
  - Responded Date, Mode
  - [Mark as Resolved] button
- **Timeline tab:** Immutable audit log of all status changes and document accesses

### 6.2 Drawer: `breach-detail` (720px, right-slide)
- **Tabs:** Overview · Impact Assessment · Notifications · Remediation · Timeline
- **Overview tab:** Breach ID, Detected Date, Branch, Type, Records Affected, Data Categories affected, Description, Detected By, Root Cause (if known)
- **Impact Assessment tab:** Risk level (Low/Medium/High/Critical), Sensitive data categories involved, Vulnerable groups (children/staff/parents), Likely harm (financial/physical/reputational/other)
- **Notifications tab (Role 113 primary):**
  - **CERT-In Notification** (72h window — IT Act 2000 + CERT-In Directions 2022): Reference number, Submitted Date/Time, Document upload, [Record Notification] button; system shows elapsed hours since detection with red countdown if > 60h
  - **Data Protection Board (DPB) Notification** (72h window — DPDP Act s.8(6)): Required for breaches affecting sensitive personal data or a large volume of data subjects; Reference, Date, [Record DPB Notification] button; pending rules may update thresholds — use "Not Applicable" for low-risk breaches until DPB clarifies
  - Affected data subjects notified: Yes/No, Date, Mode
- **Remediation tab:** Containment steps taken, Technical measures applied, Policy changes, Staff training triggered
- **Timeline tab:** Immutable audit log

### 6.3 Modal: `record-dsr` (580px)
| Field | Type | Required | Validation |
|---|---|---|---|
| Received Date | Date picker | Yes | Cannot be future |
| Requester Type | Select | Yes | Student / Parent / Staff |
| Request Type | Select | Yes | Access / Correction / Erasure / Portability / Withdrawal / Grievance |
| Branch | Select | Yes | |
| Description | Textarea | Yes | Min 20 chars |
| Requester Contact | Text | Yes | Email or phone |
| Identity Verification | File | No | ID proof |

**Footer:** Cancel · Submit Request

### 6.4 Modal: `record-breach` (620px)
| Field | Type | Required | Validation |
|---|---|---|---|
| Detected Date and Time | Datetime picker | Yes | Cannot be future |
| Branch | Select | Yes | |
| Breach Type | Select | Yes | |
| Records Affected (estimate) | Number | Yes | Min 1 |
| Data Categories Affected | Multi-select | Yes | |
| Description | Textarea | Yes | Min 30 chars |
| Detected By | Text | Yes | |
| Immediate Action | Textarea | Yes | |

**Footer:** Cancel · Record Breach — starts 72-hour CERT-In clock

---

## 7. Charts

### 7.1 Consent Coverage by Branch (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Consent Coverage by Branch — Current AY" |
| Data | Per branch: % of data subjects with valid consent |
| X-axis | Coverage % (0–100) |
| Y-axis | Branch name |
| Colour | Green ≥ 90%, Amber 70–89%, Red < 70% (dynamic per bar) |
| Tooltip | "[Branch]: [X]% coverage ([N] / [Total] subjects)" |
| API endpoint | `GET /api/v1/group/{id}/legal/data-privacy/consent-coverage/` |
| HTMX | `hx-get` on load → `hx-target="#chart-consent-coverage"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 DSR Volume by Request Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "DSR Requests by Type — Current FY" |
| Data | Count per request type |
| Colour | Each type: distinct colour from palette |
| Tooltip | "[Type]: [N] requests ([X]%)" |
| API endpoint | `GET /api/v1/group/{id}/legal/data-privacy/dsr-by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-dsr-types"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| DSR recorded | "DSR [DSR-YYYY-NNNN] recorded. Response due by [date]." | Success | 5s |
| DSR resolved | "DSR [DSR-YYYY-NNNN] marked as resolved." | Success | 4s |
| Breach recorded | "Data breach [BRH-YYYY-NNNN] recorded. 72-hour CERT-In clock started." | Warning | 10s (sticky) |
| CERT-In notification logged | "CERT-In notification submitted for [BRH-YYYY-NNNN]." | Success | 5s |
| Breach CERT-In overdue | "CRITICAL: [BRH-YYYY-NNNN] — CERT-In 72-hour deadline exceeded." | Error | Sticky |
| Export triggered | "Generating DPO compliance report…" | Info | 3s |
| Export ready | "DPO report ready. Click to download." | Success | 6s |
| Sub-processor DPA expiring | "DPA with [Vendor] expires in [N] days. Renew to maintain DPDP compliance." | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No DSRs this FY | `inbox` | "No Data Subject Requests" | "No DSRs have been received this financial year." | Record First DSR |
| No breaches on record | `shield-check` | "No Data Breaches Recorded" | "No personal data breaches have occurred." | — |
| No sub-processors configured | `database` | "Sub-Processor Register Empty" | "Register all third-party processors to comply with DPDP Act s.8(6)." | Contact IT Admin |
| Filter returns no results | `search` | "No Matches Found" | "No items match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 8 KPI shimmer cards + 3-section skeleton |
| DSR table load | 8-row shimmer skeleton |
| Breach table load | 5-row shimmer skeleton |
| Sub-processor table load | 5-row shimmer skeleton |
| Chart load | Grey canvas + centred spinner |
| Drawer open | Right-slide skeleton |
| Form submission | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | DPO (113, G1) | Compliance Mgr (109, G1) | Contract Admin (127, G3) | Legal Dispute (128, G1) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| DSR Table (full) | Visible | Not visible (counts only) | Not visible | Not visible | Visible |
| Breach Register | Full access | Summary counts only | Not visible | Full access | Full access |
| Sub-processor Register | Full access | Read-only | DPA column only | Not visible | Full access |
| [Record DSR] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Record Breach] button | Visible | Not visible | Not visible | Not visible | Visible |
| [Record Notification] in breach | Visible | Not visible | Not visible | Not visible | Visible |
| Consent Coverage chart | Visible | Visible | Not visible | Not visible | Visible |
| DSR Types chart | Visible | Not visible | Not visible | Not visible | Visible |
| Export DPO Report | Visible | Not visible | Not visible | Not visible | Visible |
| Alert banners (all) | All visible | CERT-In only | DPA expiry only | Breach only | All visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/data-privacy/kpis/` | Role 113, 109 (limited), G4+ | KPI summary bar |
| GET | `/api/v1/group/{id}/legal/data-privacy/dsrs/` | Role 113, G4+ | Paginated DSR list |
| POST | `/api/v1/group/{id}/legal/data-privacy/dsrs/` | Role 113, G4+ | Record new DSR |
| GET | `/api/v1/group/{id}/legal/data-privacy/dsrs/{dsr_id}/` | Role 113, G4+ | DSR detail |
| PATCH | `/api/v1/group/{id}/legal/data-privacy/dsrs/{dsr_id}/resolve/` | Role 113, G4+ | Mark DSR resolved |
| GET | `/api/v1/group/{id}/legal/data-privacy/breaches/` | Role 113, 128, G4+ | Paginated breach register |
| POST | `/api/v1/group/{id}/legal/data-privacy/breaches/` | Role 113, G4+ | Record new breach |
| POST | `/api/v1/group/{id}/legal/data-privacy/breaches/{bid}/notifications/` | Role 113, G4+ | Record CERT-In notification |
| GET | `/api/v1/group/{id}/legal/data-privacy/sub-processors/` | Role 113, 127 (limited), G4+ | Sub-processor register |
| GET | `/api/v1/group/{id}/legal/data-privacy/consent-coverage/` | Role 113, G4+ | Consent coverage chart data |
| GET | `/api/v1/group/{id}/legal/data-privacy/dsr-by-type/` | Role 113, G4+ | DSR type donut chart |
| POST | `/api/v1/group/{id}/legal/data-privacy/export/` | Role 113, G4+ | Export DPO report |

### Query Parameters for DSR List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: DSR ID, requester type, subject |
| `request_type` | string | access / correction / erasure / portability / withdrawal / grievance |
| `status` | string | received / in_progress / resolved / rejected / overdue |
| `branch_id` | integer | Filter by branch |
| `fy` | string | Financial year |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50; default 25 |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | `<div id="kpi-bar">` | GET `.../data-privacy/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| DSR table load | `<tbody id="dsr-table-body">` | GET `.../data-privacy/dsrs/` | `#dsr-table-body` | `innerHTML` | `hx-trigger="load"` |
| DSR search | Search input | GET `.../data-privacy/dsrs/?q={v}` | `#dsr-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| DSR filter | Status/type chips | GET `.../data-privacy/dsrs/?status={v}` | `#dsr-table-body` | `innerHTML` | `hx-trigger="click"` |
| Open DSR drawer | [View] button | GET `.../data-privacy/dsrs/{dsr_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Breach table load | `<tbody id="breach-table-body">` | GET `.../data-privacy/breaches/` | `#breach-table-body` | `innerHTML` | `hx-trigger="load"` |
| Open breach drawer | [View] button | GET `.../data-privacy/breaches/{bid}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Record DSR modal | [+ Record DSR] | GET `/htmx/legal/data-privacy/dsr-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Record breach modal | [+ Record Breach] | GET `/htmx/legal/data-privacy/breach-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit forms | Form elements | POST to respective endpoints | `#table-body or #modal-container` | `outerHTML / innerHTML` | Validates client-side first |
| Chart loads | Both chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
