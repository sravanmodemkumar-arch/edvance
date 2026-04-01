# 32 — Consent Management

- **URL:** `/group/it/privacy/consent/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group Data Privacy Officer (Role 55, G1) — Read-only; Group IT Admin (Role 54, G4) — Full access

---

## 1. Purpose

The Consent Management page is the group's register of all consent obtained from data subjects — students, parents, and staff — for the processing of their personal data under the DPDP Act 2023. Under the Act, a Data Fiduciary (the group) must obtain free, specific, informed, unconditional, and unambiguous consent before collecting or processing any personal data. This register is the evidence that such consent was obtained, for what specific purpose, using what method, at what time, and whether it remains active or has been withdrawn.

Consent in EduForge is collected at multiple touchpoints: during the online admission form (students and parents consent to their data being used for admission processing, academic record management, and institutional communications), during staff onboarding (staff consent to HR records processing, BGV, and payroll), and at specific moments when a new data processing purpose arises (e.g., obtaining separate explicit consent before using student photos in marketing materials, or before sharing data with a third-party exam platform).

The register does not store actual personal data — it stores a consent record: a pseudonymised reference to the data subject (type + masked ID), the purpose for which consent was given, the collection method, and the current status. This design serves two purposes: it allows the Data Privacy Officer (G1) to audit consent completeness without seeing raw PII, and it limits the sensitivity of this register itself — it is audit data, not subject data.

The IT Admin (G4) may update consent records in limited circumstances: when a paper consent form is scanned and needs to be entered into the system, or when a withdrawal request must be processed. The Data Privacy Officer is read-only: they audit what is there, identify gaps (missing consents, expired consents), and raise issues with the IT Admin for remediation.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Data Privacy Officer | G1 | Read-only — all records visible (masked) | Audit and oversight; cannot modify |
| Group IT Admin | G4 | Full read + process withdrawals + manual entry | Operational management of consent records |
| Group IT Director | G4 | Read-only | Governance visibility |
| All other Division F roles | — | Hidden | No access |
| Group Cybersecurity Officer (Role 56, G1) | Read-only | Security awareness of consent processing practices |
| Group IT Support Executive (Role 57, G3) | No access | Returns 403 |
| Group EduForge Integration Manager (Role 58, G4) | No access | Returns 403 |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → IT & Technology → Data Privacy → Consent Management
```

### 3.2 Page Header
- **Title:** `Consent Management Register`
- **Subtitle:** `DPDP Act 2023 — Data Subject Consent Audit Register · [Total count] consent records`
- **Role Badge:** `Group Data Privacy Officer` or `Group IT Admin`
- **Right-side controls (IT Admin only):** `+ Record Manual Consent` · `Export`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Consents expiring in <30 days | "[N] consent record(s) are expiring within 30 days. Review and obtain renewal where required." | Amber |
| Consent rate for a branch <80% | "Branch [Name] has a consent capture rate of [N]%. Incomplete consent records may indicate process gap." | Amber |
| Withdrawal requests unprocessed >48h | "[N] consent withdrawal request(s) have been pending for more than 48 hours. Process as a priority — DPDP Act requires prompt withdrawal." | Red |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Total Consent Records | Total rows in consent register | Blue | No filter |
| Active Consents | Consent records with status = Active and not expired | Green | Filter by Active |
| Withdrawn Consents | Consent records where withdrawal request has been processed | Amber (informational) | Filter by Withdrawn |
| Consents Expiring <30 Days | Records with expiry_date within 30 days and status = Active | Amber if > 0 | Filter by expiring soon |

---

## 5. Main Table — Consent Register

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Record # | Auto-generated ID (e.g., CNS-00001) | No | No |
| Data Subject | Masked identifier — Type (Student/Parent/Staff) + masked ID (e.g., "Student · STD-••••3421") | No | Yes (type filter) |
| Branch | Branch name | Yes | Yes (multi-select) |
| Consent Purpose | Badge (Admission Data / Academic Records / Photo & Video / Third-Party Sharing / Marketing / HR Processing / Other) | Yes | Yes (multi-select) |
| Collection Date | Date | Yes | Yes (date range) |
| Expiry Date | Date — amber if <30d, red if <7d | Yes | Yes (date range) |
| Status | Badge (Active / Withdrawn / Expired) | Yes | Yes (multi-select) |
| Consent Method | Badge (Digital Form / Paper-OTP Verified / Paper-Unsigned / Verbal-Recorded) | Yes | Yes |
| Actions | View | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All configured branches |
| Purpose | Multi-select checkbox | Admission Data / Academic Records / Photo & Video / Third-Party Sharing / Marketing / HR Processing / Other |
| Status | Multi-select checkbox | Active / Withdrawn / Expired |
| Consent Method | Multi-select checkbox | Digital Form / Paper-OTP Verified / Paper-Unsigned / Verbal-Recorded |
| Collection Date | Date range picker | Any range |
| Expiry Date | Date range picker | Any range |
| Data Subject Type | Dropdown | Student / Parent / Staff / All |

### 5.2 Search
- Record # only (full PII search disabled for DPO role; IT Admin can search by masked ID only)
- 300ms debounce

### 5.3 Pagination
- Server-side · 25 rows/page

---

## 6. Drawers

### 6.1 Drawer: `consent-record-view` — View Consent Record
- **Trigger:** Actions → View
- **Width:** 560px
- **Content (all read-only; no PII shown):**
  - Record number, creation date
  - Data subject category (Student/Parent/Staff), masked subject ID
  - Branch
  - Consent purpose: full purpose text (the written statement of what was consented to, not just the category — e.g., "Collection and use of student name, date of birth, and academic records for the purpose of managing admission to [Branch Name] and maintaining academic performance records.")
  - Collection method and date
  - Consent given by (if minor student: "Parent/Guardian" noted)
  - Expiry date and current status
  - Withdrawal request (if any):
    - Request date and time
    - Reason given by data subject
    - Status (Pending Processing / Processed)
    - Processed by (staff name) and processing date
  - Audit trail: all status changes to this record with timestamp and actor

### 6.2 Drawer: `consent-withdrawal-process` — Process Withdrawal (IT Admin only)
- **Trigger:** View Record → Process Withdrawal (only shown if withdrawal request is pending)
- **Width:** 480px
- **Fields:**
  - Withdrawal request details (read-only from request)
  - Action taken (dropdown: Data Deleted / Data Anonymised / Data Retained with Legal Basis — must select)
  - Legal basis for retention (required if retained — e.g., "Legal obligation under RTE Act to retain academic records for 5 years")
  - Notes (optional, textarea)
  - Confirmation: "I confirm this withdrawal has been processed in accordance with DPDP Act 2023 requirements"
- On confirm: Record status → Withdrawn, withdrawal_processed_at timestamp set, DPO notified

### 6.3 Drawer: `consent-manual-entry` — Record Manual Consent (IT Admin only)
- **Trigger:** `+ Record Manual Consent` button
- **Width:** 560px
- **Fields:**
  - Data Subject Type (dropdown: Student / Parent / Staff)
  - Subject Branch (dropdown)
  - Subject ID (internal EduForge ID — not shown to DPO but IT Admin enters to link consent to subject)
  - Consent Purpose (dropdown — as per purpose categories)
  - Purpose Text (required, textarea — exact purpose statement from consent form)
  - Collection Method (dropdown: Paper-OTP Verified / Paper-Unsigned / Verbal-Recorded)
  - Collection Date (required, date picker)
  - Expiry Date (optional — leave blank for indefinite)
  - Document Reference (optional — scan upload to Cloudflare R2 if paper form)
- On submit: Consent record created; Record # generated

---

## 7. Charts

### 7.1 Consent by Purpose Category (Donut Chart)
- Segments: Admission Data / Academic Records / Photo & Video / Third-Party Sharing / Marketing / HR Processing / Other
- Shows distribution of consent types in the register
- Legend with count and percentage per segment

### 7.2 Withdrawal Trend — 12 Months (Line Chart)
- X-axis: Months (last 12)
- Y-axis: Count of withdrawals processed per month
- Trend line — increasing withdrawals may indicate trust or communications issues
- Positioned beside the donut chart

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Manual consent recorded | "Consent record CNS-[N] created successfully." | Success | 3s |
| Withdrawal processed | "Withdrawal for CNS-[N] processed. Record status updated to Withdrawn." | Success | 4s |
| Export triggered | "Consent register export is being prepared." | Info | 3s |
| Withdrawal processing failed | Error: `Failed to process withdrawal for CNS-[N]. Contact IT Support.` | Error | 5s |

---

**Audit Trail:** All consent record changes (withdrawals, re-consent, flagging) are logged to the IT Audit Log with actor user ID, timestamp, and consent record ID.

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No consent records | "No Consent Records" | "No consent records have been entered. Consent data flows in automatically when students and staff complete digital forms. Use the manual entry option for paper-based consents." | + Record Manual Consent |
| No results for filter | "No Matching Records" | "No consent records match the selected filters." | Clear Filters |
| No withdrawn records | "No Withdrawals" | "No consent withdrawals have been recorded." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | 4 KPI shimmer cards + table skeleton (15 rows) + 2 chart shimmers |
| Filter / search | Table skeleton shimmer |
| View consent drawer | Drawer spinner; audit trail section lazy-loads |
| Process withdrawal submit | Button spinner: "Processing withdrawal…" |
| Manual entry submit | Button spinner |
| Chart load | Chart area shimmer |

---

## 11. Role-Based UI Visibility

| Element | Data Privacy Officer (G1) | IT Admin (G4) | IT Director (G4) |
|---|---|---|---|
| + Record Manual Consent | Hidden | Visible | Hidden |
| Process Withdrawal button | Hidden | Visible | Hidden |
| Export | Hidden | Visible | Visible |
| Subject masked ID in table | Visible (masked) | Visible (full ID in own drawer) | Visible (masked) |
| Audit trail in view drawer | Visible | Visible | Visible |
| Purpose text in view drawer | Visible | Visible | Visible |
| Withdrawal process drawer | Hidden | Visible | Hidden |
| Document upload (R2 link) | Visible (download) | Visible (upload + download) | Visible (download) |
| Charts | Visible | Visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/it/privacy/consent/` | JWT (G1+) | Paginated consent register (masked PII) |
| POST | `/api/v1/it/privacy/consent/` | JWT (G4 — IT Admin) | Manual consent record creation |
| GET | `/api/v1/it/privacy/consent/{id}/` | JWT (G1+) | Full consent record detail |
| POST | `/api/v1/it/privacy/consent/{id}/process-withdrawal/` | JWT (G4 — IT Admin) | Process withdrawal request |
| GET | `/api/v1/it/privacy/consent/kpis/` | JWT (G1+) | KPI card values |
| GET | `/api/v1/it/privacy/consent/charts/purpose-distribution/` | JWT (G1+) | Consent by purpose donut chart data |
| GET | `/api/v1/it/privacy/consent/charts/withdrawal-trend/` | JWT (G1+) | Monthly withdrawal trend line chart data |
| GET | `/api/v1/it/privacy/consent/export/` | JWT (G4 — IT Admin / IT Director) | Export consent register (CSV) |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/it/privacy/consent/kpis/` | `#kpi-bar` | `innerHTML` |
| Load consent table | `load` | GET `/api/v1/it/privacy/consent/` | `#consent-table` | `innerHTML` |
| Apply filters | `change` on filter controls | GET `/api/v1/it/privacy/consent/?branch=...&purpose=...` | `#consent-table` | `innerHTML` |
| Search by record # | `input` (300ms debounce) | GET `/api/v1/it/privacy/consent/?q=...` | `#consent-table` | `innerHTML` |
| Open view drawer | `click` on View | GET `/api/v1/it/privacy/consent/{id}/` | `#consent-drawer` | `innerHTML` |
| Process withdrawal | `click` on Confirm Withdrawal | POST `/api/v1/it/privacy/consent/{id}/process-withdrawal/` | `#consent-drawer` | `innerHTML` |
| Submit manual consent | `click` on Submit | POST `/api/v1/it/privacy/consent/` | `#consent-table` | `innerHTML` |
| Load purpose chart | `load` | GET `/api/v1/it/privacy/consent/charts/purpose-distribution/` | `#purpose-chart` | `innerHTML` |
| Load withdrawal chart | `load` | GET `/api/v1/it/privacy/consent/charts/withdrawal-trend/` | `#withdrawal-chart` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/it/privacy/consent/?page=N` | `#consent-table` | `innerHTML` |
| Export consent register | `click` on Export | GET `/api/v1/it/privacy/consent/export/` | `#export-result` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
