# 36 — Data Residency Tracker

- **URL:** `/group/it/privacy/residency/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read-only (primary); Group IT Admin (Role 54, G4) — Update

---

## 1. Purpose

The Data Residency Tracker maintains the group's register of where personal data assets are physically stored and processed. Under DPDP Act 2023, data localisation is a critical compliance requirement: personal data of Indian residents must, as a baseline, be stored and processed within India. Cross-border data transfers are permitted only with explicit exemptions — where data subjects have consented to foreign transfer, where a legal necessity exists, or where the central government has specifically permitted transfers to certain jurisdictions.

In practical terms for EduForge, the group must document every database, storage bucket, and processing system that holds personal data and confirm it resides in India. The primary approved locations are AWS Mumbai Region (ap-south-1), Cloudflare R2 with an India Point of Presence configured, and the EduForge platform's own PostgreSQL databases hosted in India. Third-party integrations that process or store personal data (such as Google Analytics, certain AI services, or foreign-headquartered EdTech platforms) must be individually assessed — if they process Indian personal data on foreign servers, they need a documented justification and often a separate consent from data subjects.

The Data Privacy Officer uses this tracker to identify data assets that are non-compliant with data localisation requirements, prioritise remediation (typically migrating data or switching to an India-based alternative), and document justifications for any approved cross-border transfers. The IT Admin maintains the technical accuracy of the register — updating storage locations as infrastructure evolves, noting when data has been migrated, and adding new data assets as new systems are deployed.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only — full view | Primary user; monitors compliance; cannot modify records |
| Group IT Admin | G4 | Full read + update residency status | Maintains technical accuracy of records |
| Group IT Director | G4 | Read-only | Governance oversight |
| All other Division F roles | — | Hidden | No access |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | Security posture assessment of data residency |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Data Residency Tracker
```

### 3.2 Page Header
- **Title:** `Data Residency Tracker`
- **Subtitle:** `DPDP Act 2023 — Data Localisation Compliance · [N] Data Assets Tracked`
- **Role Badge:** `Group Data Privacy Officer`
- **Right-side controls (IT Admin only):** `+ Add Data Asset` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Non-compliant assets found | "[N] data asset(s) are non-compliant with DPDP Act data localisation requirements. Review and remediate." | Red |
| Assets under review >30 days | "[N] data asset(s) have been in Review Required status for more than 30 days. Action needed." | Amber |
| New integration added without data asset entry | "A new integration has been added to the Integration Registry without a corresponding data asset record in this tracker. Review required." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Data Assets Tracked | Total data asset records in register | Blue | No filter |
| Compliant (India-resident) | Assets where residency_status = Compliant | Green | Filter by Compliant |
| Non-Compliant (Foreign) | Assets where residency_status = Non-Compliant | Red if > 0, Green if 0 | Filter by Non-Compliant |
| Under Review | Assets where residency_status = Review Required | Amber if > 0 | Filter by Review Required |

---

## 5. Main Table — Data Asset Residency Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Data Asset Name | Text (e.g., "Student Profile Database", "Exam Results Store", "Payroll Records") | Yes | Yes (text search) |
| Data Category | Badge (Student PII / Staff PII / Financial / Health / Academic / Operational) | Yes | Yes (multi-select) |
| Storage Location | Text (e.g., "AWS Mumbai (ap-south-1)", "Cloudflare R2 (India PoP)", "Third-party: [Name]") | Yes | Yes (multi-select dropdown of known locations) |
| Processing Location | Text (where data is computed/processed — may differ from storage) | Yes | Yes (multi-select) |
| Residency Status | Badge (Compliant / Non-Compliant / Review Required) | Yes | Yes (multi-select) |
| Justification (if foreign) | Text (truncated) — shown only if Non-Compliant | No | No |
| Last Reviewed | Date (relative) — amber if >90 days | Yes | Yes (date range) |
| Responsible Owner | Staff name | Yes | No |
| Actions | View / Update | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Data Category | Multi-select checkbox | Student PII / Staff PII / Financial / Health / Academic / Operational |
| Storage Location | Multi-select dropdown | AWS Mumbai / Cloudflare R2 / PostgreSQL India / Third-Party (specific names from register) |
| Residency Status | Multi-select checkbox | Compliant / Non-Compliant / Review Required |
| Last Reviewed | Date range picker | Any range |

### 5.2 Search
- Data Asset Name, storage location
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page

---

## 6. Drawers

### 6.1 Drawer: `asset-view` — View Asset Detail
- **Trigger:** Actions → View
- **Width:** 720px
- **Content:**
  - Asset name and description (full, not truncated)
  - Data category and specific data types stored (e.g., "Student PII — includes name, DOB, contact, Aadhaar reference")
  - Storage location: system name, provider, region, India-resident (yes/no)
  - Processing location: system name, provider, region (may differ — e.g., stored in India but processed via a foreign AI service)
  - Data lineage section: Where does this data flow after storage? (list of downstream systems, each with their own residency status)
  - Retention policy: how long this data is retained, deletion schedule, legal basis for retention
  - Responsible owner: role and name
  - Residency status and detailed justification (if Non-Compliant or Review Required)
  - Cross-border transfer basis (if applicable): one of — Data subject consent / Central government whitelist / Legal necessity / Contractual necessity / DPB approved transfer
  - Audit trail: all status changes with timestamp and actor

### 6.2 Drawer: `asset-update` — Update Residency Status (IT Admin only)
- **Trigger:** Actions → Update
- **Width:** 560px
- **Fields:**
  - Data Asset Name (locked — cannot change name; must create new record for new asset)
  - Storage Location (editable — update if infrastructure has changed)
  - Processing Location (editable)
  - Residency Status (required, dropdown: Compliant / Non-Compliant / Review Required)
  - Justification (required if Non-Compliant — text area; must document legal basis for cross-border transfer)
  - Cross-Border Transfer Basis (required if Non-Compliant, dropdown: Data Subject Consent / Government Whitelist / Legal Necessity / Contractual Necessity / DPB Approved)
  - Data Lineage updates (add/edit downstream systems — each with storage location)
  - Retention Policy updates (textarea)
  - Responsible Owner (dropdown — staff with IT role)
  - Review Notes (textarea — what was assessed and by whom)
- On save: last_reviewed timestamp updated; DPO notified if status changed to Non-Compliant

**Audit Trail:** All residency status updates are automatically logged to the IT Audit Log, including previous status, new status, justification changes, and timestamp.

### 6.3 Drawer: `asset-create` — Add Data Asset (IT Admin only)
- **Trigger:** `+ Add Data Asset`
- **Width:** 560px
- **Fields:**
  - Asset Name (required, text)
  - Description (required, textarea)
  - Data Category (required, dropdown)
  - Specific Data Types (required, multi-select checkboxes + free text)
  - Storage Location (required — select from known locations or add new)
  - Storage Provider (text — e.g., AWS, Cloudflare, PostgreSQL self-hosted)
  - Storage Region/PoP (required)
  - India-resident storage? (required, radio: Yes / No)
  - Processing Location (required if different from storage)
  - Residency Status (required, dropdown)
  - Responsible Owner (required, dropdown)
  - Retention Policy (required, textarea)
  - Link to related Integration Registry entry (optional — dropdown)

---

## 7. Charts

### 7.1 Compliance Status Distribution (Donut Chart)
- Segments: Compliant (green) / Non-Compliant (red) / Review Required (amber)
- Shows at-a-glance how the data asset estate is split by compliance status
- Count and percentage per segment
- Positioned in the right column of the KPI bar or below KPIs as a compact chart

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Data asset created | "Data asset '[Name]' added to residency register." | Success | 3s |
| Status updated to Compliant | "Data asset '[Name]' marked Compliant. DPO notified." | Success | 4s |
| Status updated to Non-Compliant | "Data asset '[Name]' marked Non-Compliant. DPO notified. Justification logged." | Warning | 5s |
| Status updated to Review Required | "Data asset '[Name]' flagged for review." | Info | 3s |
| Export triggered | "Data residency register export prepared." | Info | 3s |
| Data asset creation failed | Error: `Failed to add data asset. Verify storage location and residency status.` | Error | 5s |
| Data asset update failed | Error: `Failed to update data asset. Ensure all required fields are valid.` | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No data assets | "No Data Assets Registered" | "Add data assets to track where personal data is stored and processed across EduForge systems." | + Add Data Asset |
| All assets compliant | "All Data Assets Compliant" | "Every tracked data asset is stored and processed within India in compliance with DPDP Act requirements." | — |
| No non-compliant assets | "No Non-Compliant Assets" | "No data assets are currently flagged as non-compliant with data localisation requirements." | — |
| No filter results | "No Matching Assets" | "No data assets match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + donut chart shimmer + table skeleton (10 rows) |
| Filter / search | Table skeleton shimmer |
| View asset drawer | Drawer spinner; data lineage section lazy-loads after base info |
| Update submit | Button spinner |
| Create submit | Button spinner |
| Export | Button spinner: "Preparing export…" |

---

## 11. Role-Based UI Visibility

| Element | Data Privacy Officer (G1) | IT Admin (G4) | IT Director (G4) |
|---|---|---|---|
| + Add Data Asset | Hidden | Visible | Hidden |
| Update Action | Hidden | Visible | Hidden |
| View Action | Visible | Visible | Visible |
| Full asset detail in drawer | Visible | Visible | Visible |
| Justification text (Non-Compliant) | Visible | Visible + editable | Visible |
| Data lineage details | Visible | Visible + editable | Visible |
| Retention policy | Visible | Visible + editable | Visible |
| Audit trail | Visible | Visible | Visible |
| Export | Hidden | Visible | Visible |
| Compliance donut chart | Visible | Visible | Visible |
| Alert banners | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/residency/` | JWT (G1+) | Paginated data asset residency register |
| POST | `/api/v1/it/privacy/residency/` | JWT (G4 — IT Admin) | Add new data asset |
| GET | `/api/v1/it/privacy/residency/{id}/` | JWT (G1+) | Full data asset detail + lineage + audit trail |
| PATCH | `/api/v1/it/privacy/residency/{id}/` | JWT (G4 — IT Admin) | Update data asset residency status |
| GET | `/api/v1/it/privacy/residency/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/residency/charts/compliance-distribution/` | JWT (G1+) | Donut chart data (compliant vs non-compliant vs review) |
| GET | `/api/v1/it/privacy/residency/export/` | JWT (G4 — IT Admin / IT Director) | Export residency register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/residency/kpis/` | `#kpi-bar` | `innerHTML` |
| Load residency table | `load` | GET `/api/v1/it/privacy/residency/` | `#residency-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/residency/?category=...&status=...` | `#residency-table` | `innerHTML` |
| Search assets | `input` (300ms debounce) | GET `/api/v1/it/privacy/residency/?q=...` | `#residency-table` | `innerHTML` |
| Open view drawer | `click` on View | GET `/api/v1/it/privacy/residency/{id}/` | `#residency-drawer` | `innerHTML` |
| Load data lineage | `load` (lazy in drawer) | GET `/api/v1/it/privacy/residency/{id}/` (lineage section) | `#lineage-section` | `innerHTML` |
| Open update drawer | `click` on Update | GET `/api/v1/it/privacy/residency/{id}/` | `#residency-drawer` | `innerHTML` |
| Submit update | `click` on Save | PATCH `/api/v1/it/privacy/residency/{id}/` | `#residency-table` | `innerHTML` |
| Submit create | `click` on Add Asset | POST `/api/v1/it/privacy/residency/` | `#residency-table` | `innerHTML` |
| Load compliance chart | `load` | GET `/api/v1/it/privacy/residency/charts/compliance-distribution/` | `#compliance-chart` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/residency/?page=N` | `#residency-table` | `innerHTML` |
| Export residency register | `click` on Export | GET `/api/v1/it/privacy/residency/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
