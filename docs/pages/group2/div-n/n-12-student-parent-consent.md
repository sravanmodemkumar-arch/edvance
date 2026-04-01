# [12] — Student/Parent Consent Management

> **URL:** `/group/legal/consent/`
> **File:** `n-12-student-parent-consent.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Data Privacy Officer (Role 113, G1) — DPDP Act 2023 consent records, consent campaigns, withdrawal management

---

## 1. Purpose

The Student/Parent Consent Management page tracks explicit consent records for all data subjects across the Institution Group — students (consent given by guardian for minors under 18) and parents — as required under the Digital Personal Data Protection Act 2023. The DPDP Act mandates that Data Fiduciaries obtain explicit, informed, and specific consent before processing personal data, and that consent withdrawal requests be honoured within 30 days.

Consent types tracked include: general data processing consent; marketing communications (WhatsApp, email, SMS); photo and video recording for school events (published on website/social media); biometric data collection; UID/Aadhaar linkage; third-party data sharing (e.g., with exam boards, scholarship bodies); and opt-in for competitive exam coaching programs. Each consent type has an independent record — a student may consent to data processing but withdraw consent for marketing.

The DPO uses this page to: monitor consent coverage rates per branch; run mass consent campaigns (e.g., at the start of each academic year); manage individual consent withdrawal requests within the 30-day DPDP deadline; and generate compliance reports for auditors.

Scale: 5–50 branches · 2,000–1,00,000 students/parents · Multiple consent types per data subject · Annual re-consent campaigns

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews consent forms externally |
| Group Compliance Manager | 109 | G1 | Read — Aggregate stats | Views coverage metrics; no individual records |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | Full Read + Campaign Management + Withdrawal Updates | Primary user |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Withdrawal disputes only | Views contested withdrawals |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,113,128], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Student/Parent Consent Management
```

### 3.2 Page Header
```
Student/Parent Consent Management              [+ Launch Campaign]  [Export Consent Report]
Group Data Privacy Officer — [Name]
[Group Name] · [N] Data Subjects · Overall Coverage: [X]% · AY [year]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Consent coverage below 80% for any branch | "[N] branch(es) have consent coverage below 80% — DPDP Act s.6 requires explicit consent." | High (amber) |
| Withdrawal request overdue (> 30 days) | "[N] consent withdrawal request(s) are overdue — 30-day DPDP deadline exceeded." | Critical (red) |
| Withdrawal request due within 7 days | "[N] withdrawal request(s) require action within 7 days." | High (amber) |
| Academic year started with no consent campaign | "New academic year [AY] has started. Launch consent campaign for new students." | Medium (yellow) |
| Consent records older than 2 years (recommended re-consent) | "[N] consent records are older than 2 years. Consider re-consent campaign." | Info (blue) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Data Subjects | Count | COUNT unique students + parents | Blue | `#kpi-data-subjects` |
| 2 | Overall Consent Coverage | % | subjects with ≥ 1 active consent / total | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-coverage` |
| 3 | Pending Withdrawals | Count | COUNT withdrawal_requests WHERE status != 'processed' | Red if any overdue, Amber > 3, Green = 0 | `#kpi-withdrawals` |
| 4 | Overdue Withdrawals | Count | COUNT WHERE due_date < TODAY AND status != 'processed' | Red > 0, Green = 0 | `#kpi-withdrawals-overdue` |
| 5 | Active Campaigns | Count | COUNT campaigns WHERE status = 'active' | Blue | `#kpi-active-campaigns` |
| 6 | Consents This AY | Count | COUNT consent_records WHERE ay = current | Blue | `#kpi-consents-ay` |
| 7 | Withdrawn (This AY) | Count | COUNT withdrawal_requests WHERE status = 'processed' AND ay = current | Blue | `#kpi-withdrawn-ay` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/consent/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Consent Coverage by Branch

Branch-level coverage summary — primary view.

**Search:** Branch name. Debounced 350ms.

**Filters:**
- Consent Type: `All` · `Data Processing` · `Marketing (WhatsApp)` · `Photo/Video` · `Biometric` · `Aadhaar Linkage` · `Third-Party Sharing`
- Coverage Status: `All` · `High (≥ 90%)` · `Medium (70–89%)` · `Low (< 70%)`
- Branch: dropdown

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | |
| Total Students | Integer | Yes | |
| Consented (Data Processing) | % + bar | Yes | |
| Consented (Marketing) | % + bar | Yes | |
| Consented (Photo/Video) | % + bar | Yes | |
| Overall Coverage | % + colour | Yes | Green/Amber/Red |
| Last Campaign | Date | Yes | Date of most recent consent campaign |
| Actions | Button | No | [View Details] · [Launch Campaign] (Role 113) |

**Default sort:** Overall Coverage ASC (lowest first)
**Pagination:** Server-side · Default 25/page

---

### 5.2 Withdrawal Requests Table

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Request ID | Monospace | Yes | |
| Received Date | Date | Yes | |
| Data Subject Type | Badge | Yes | Student / Parent |
| Branch | Text | Yes | |
| Consent Type Withdrawn | Badge | Yes | |
| Request Channel | Badge | No | Platform / Email / Written Letter |
| Due Date | Date | Yes | +30 days from received; red if overdue |
| Status | Badge | Yes | Pending / Processing / Processed / Disputed |
| Actions | Buttons | No | [View] · [Mark Processed] (Role 113) |

**Default sort:** Due Date ASC

---

### 5.3 Consent Campaigns

History of all consent campaigns run by the group.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Campaign Name | Text | Yes | |
| Launched Date | Date | Yes | |
| Branches Included | Integer | Yes | |
| Target Count | Integer | Yes | Students/parents targeted |
| Response Count | Integer | Yes | Number who responded |
| Response Rate | % | Yes | |
| Status | Badge | Yes | Active / Completed / Draft |
| Actions | Buttons | No | [View] |

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-consent-detail` (680px)
- **Tabs:** Overview · Consent by Type · Withdrawal Requests · Timeline
- **Overview tab:** Branch name, total students, overall coverage %, last campaign date, DPO notes
- **Consent by Type tab:** Table per consent type — total subjects, consented count, coverage %, last updated
- **Withdrawal Requests tab:** All withdrawal requests from this branch with status
- **Timeline tab:** Campaign history, coverage changes over time

### 6.2 Modal: `launch-campaign` (620px)
| Field | Type | Required |
|---|---|---|
| Campaign Name | Text | Yes |
| Academic Year | Select | Yes |
| Branches | Multi-select | Yes |
| Consent Types | Multi-checkbox | Yes |
| Channel | Multi-checkbox | Yes — WhatsApp / Email / Physical Form |
| Start Date | Date | Yes |
| Deadline | Date | Yes |
| Message Template | Textarea | No |
| Trigger: Re-consent (2-year rule) | Toggle | No — when ON, pre-filters recipients to data subjects whose consent was last given ≥ 2 years ago; system auto-runs `flag_reconsent_due` Celery task to populate this list |

**Celery task:** `flag_reconsent_due` — runs daily at 09:00 IST; sets `reconsent_required = True` on all consent records where `consent_date < TODAY − 730 days`; used to populate the re-consent trigger filter and the info-level alert banner.

**Footer:** Cancel · Save Draft · Launch Campaign

### 6.3 Modal: `process-withdrawal` (480px)
| Field | Type | Required |
|---|---|---|
| Request | Display | — |
| Processing Date | Date | Yes |
| Action Taken | Select | Yes — Consent withdrawn / Partial withdrawal / Rejected with reason |
| Reason (if rejected) | Textarea | Conditional |
| Reference | Text | No |

**Footer:** Cancel · Confirm Processing

---

## 7. Charts

### 7.1 Consent Coverage by Branch — Horizontal Bar

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Overall Consent Coverage by Branch" |
| Data | Overall coverage % per branch |
| Colour | Green ≥ 90%, Amber 70–89%, Red < 70% per bar |
| Tooltip | "[Branch]: [X]% coverage ([N] / [Total] subjects)" |
| API endpoint | `GET /api/v1/group/{id}/legal/consent/coverage-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-consent-coverage"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Consent Type Distribution — Stacked Bar

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Consent Coverage by Type — Group Average" |
| Data | Per consent type: consented %, not consented % |
| Colour | Consented = green, Not consented = red |
| Tooltip | "[Type]: [X]% consented group-wide" |
| API endpoint | `GET /api/v1/group/{id}/legal/consent/coverage-by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-consent-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign launched | "Consent campaign '[Name]' launched for [N] branches." | Success | 4s |
| Withdrawal processed | "Withdrawal request [ID] processed for [Branch]." | Success | 4s |
| Withdrawal overdue | "Withdrawal request [ID] is now overdue — 30-day DPDP deadline passed." | Error | 6s |
| Coverage alert | "[Branch] consent coverage dropped below 80%." | Warning | 5s |
| Export triggered | "Generating consent compliance report…" | Info | 3s |
| Export ready | "Consent report ready. Click to download." | Success | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No consent records | `file-text` | "No Consent Records" | "Launch a consent campaign for the current academic year." | Launch Campaign |
| No withdrawal requests | `check-circle` | "No Pending Withdrawals" | "No consent withdrawal requests are pending." | — |
| No campaigns | `megaphone` | "No Campaigns Launched" | "No consent campaigns have been run yet." | Launch First Campaign |
| Filter returns no results | `search` | "No Matching Records" | "No data matches the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI cards + 3-table skeleton |
| Table filter | Spinner overlay |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |
| Campaign launch | Button spinner |

---

## 11. Role-Based UI Visibility

| Element | DPO (113) | Compliance Mgr (109) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|---|
| Branch coverage table | Full | Aggregate stats only | Not visible | Full |
| Withdrawal table | Full | Not visible | Full (dispute cases) | Full |
| Campaigns table | Full | Not visible | Not visible | Full |
| [Launch Campaign] | Visible | Not visible | Not visible | Visible |
| [Mark Processed] | Visible | Not visible | Not visible | Visible |
| Charts | Both | Coverage chart only | Not visible | Both |
| Export | Visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/consent/coverage/` | G1+ (scoped) | Coverage by branch |
| GET | `/api/v1/group/{id}/legal/consent/withdrawals/` | Role 113, 128, G4+ | Withdrawal requests |
| PATCH | `/api/v1/group/{id}/legal/consent/withdrawals/{wid}/process/` | Role 113, G4+ | Process withdrawal |
| GET | `/api/v1/group/{id}/legal/consent/campaigns/` | Role 113, G4+ | Campaigns list |
| POST | `/api/v1/group/{id}/legal/consent/campaigns/` | Role 113, G4+ | Launch campaign |
| GET | `/api/v1/group/{id}/legal/consent/re-consent-due/` | Role 113, G4+ | Returns list of data subjects with consent records older than 2 years (recommended re-consent trigger) |
| GET | `/api/v1/group/{id}/legal/consent/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/legal/consent/coverage-by-branch/` | Role 113, G4+ | Chart data |
| GET | `/api/v1/group/{id}/legal/consent/coverage-by-type/` | Role 113, G4+ | Chart data |
| POST | `/api/v1/group/{id}/legal/consent/export/` | Role 113, G4+ | Export report |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../consent/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Coverage table load | Table body | GET `.../consent/coverage/` | `#coverage-table-body` | `innerHTML` | `hx-trigger="load"` |
| Withdrawal table load | Table body | GET `.../consent/withdrawals/` | `#withdrawal-table-body` | `innerHTML` | `hx-trigger="load"` |
| Open drawer | [View Details] | GET `.../consent/coverage/{branch_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Campaign modal | [+ Launch Campaign] | GET `/htmx/legal/consent/campaign-form/` | `#modal-container` | `innerHTML` | |
| Process withdrawal modal | [Mark Processed] | GET `/htmx/legal/consent/withdrawals/{wid}/process-form/` | `#modal-container` | `innerHTML` | |
| Charts | Chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
