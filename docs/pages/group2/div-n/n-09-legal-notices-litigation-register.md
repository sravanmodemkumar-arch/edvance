# [09] — Legal Notices & Litigation Register

> **URL:** `/group/legal/litigation/`
> **File:** `n-09-legal-notices-litigation-register.md`
> **Template:** `portal_base.html` (light theme — restricted)
> **Priority:** P1
> **Role:** Group Legal Dispute Coordinator (Role 128, G1) — court cases, legal notices, arbitration proceedings tracking

---

## 1. Purpose

The Legal Notices & Litigation Register tracks all legal proceedings involving the Institution Group and its branches — incoming legal notices, outgoing notices, civil court cases, consumer forum complaints, High Court writs, criminal cases, arbitration proceedings, and any regulatory proceedings before quasi-judicial bodies. This is a sensitive, high-stakes page: active litigation and legal notices are confidential matters that could affect the group's reputation, finances, and regulatory standing.

The Group Legal Dispute Coordinator (Role 128, G1) maintains this register by recording all legal proceedings as they arise, updating case status and next hearing dates, tracking assigned advocates, and monitoring estimated financial liabilities. The Group Legal Officer (Role 108, G0) handles actual advocacy externally — this page is the information management system for those proceedings.

Key use cases: (a) before any board meeting, the Chairman/CEO can review all active litigation and estimated liabilities; (b) before renewing any staff contract, the Contract Administrator can check if the staff member is a party to any proceedings; (c) before annual audit, the Finance team can verify contingent liabilities.

Scale: 5–50 branches · 5–50 active legal matters at any time · Each case tracked from inception to resolution

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Manages cases externally; provides updates to Coordinator |
| Group Compliance Manager | 109 | G1 | Read — Regulatory cases only | Views cases arising from compliance failures |
| Group RTI Officer | 110 | G1 | Read — RTI-related cases only | Views appeal cases at Information Commission |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Not relevant |
| Group POCSO Reporting Officer | 112 | G1 | Read — POCSO criminal cases only | Views criminal proceedings from POCSO incidents |
| Group Data Privacy Officer | 113 | G1 | Read — DPDP/data-related cases only | Views Data Protection Board proceedings |
| Group Contract Administrator | 127 | G3 | Read — Contract dispute cases only | Views cases involving staff/vendor contract disputes |
| Group Legal Dispute Coordinator | 128 | G1 | Full Read + Update | Primary user; records and updates all litigation |
| Group Insurance Coordinator | 129 | G1 | Read — Insured liability cases | Views cases that are covered by insurance |

> **Access enforcement:** `@require_role(roles=[109,110,112,113,127,128,129], min_level=G1)` with row-level filtering based on case category for most roles.
>
> **Confidentiality:** This page is marked confidential. All accesses logged. Cases with sensitive data (criminal, POCSO-linked) are restricted to Role 128, 112, G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Legal Notices & Litigation Register   [Confidential]
```

### 3.2 Page Header
```
Legal Notices & Litigation Register             [+ Record Matter]  [Export ↓]
Group Legal Dispute Coordinator — [Name]
[Group Name] · [N] Active Matters · Est. Liability: ₹[amount] · Last updated: [datetime]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Court hearing tomorrow or today | "Hearing scheduled TODAY/TOMORROW for [Case ID] at [Court/Forum]. Advocate confirmed?" | Critical (red) |
| Response deadline within 3 days | "[N] matter(s) require filing of response/reply within 3 days." | Critical (red) |
| Response deadline within 7 days | "[N] legal notice(s) require response within 7 days." | High (amber) |
| Case with no advocate assigned | "[N] active matter(s) have no assigned advocate." | High (amber) |
| High-value case (est. liability > ₹10 lakh) | "Matter [Case ID] has estimated liability of ₹[amount]. Ensure Chairman is briefed." | Medium (yellow) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Matters | Count | COUNT WHERE status NOT IN ('disposed','archived','settled') | Blue | `#kpi-active-matters` |
| 2 | Hearings This Month | Count | COUNT WHERE next_hearing_date within current month | Amber > 5, Blue ≤ 5 | `#kpi-hearings-month` |
| 3 | Response Deadlines (7d) | Count | COUNT WHERE response_due_date BETWEEN TODAY AND TODAY+7 | Red > 0, Green = 0 | `#kpi-deadlines-7d` |
| 4 | Notices Awaiting Response | Count | COUNT legal_notices WHERE response_sent = False | Red > 3, Amber 1–3, Green = 0 | `#kpi-notices-pending` |
| 5 | Total Est. Liability | Sum (₹) | SUM estimated_liability WHERE status = 'active' | Red > ₹50L, Amber ₹10–50L, Green < ₹10L | `#kpi-est-liability` |
| 6 | Settled This FY | Count | COUNT WHERE status = 'settled' AND settled_fy = current | Blue | `#kpi-settled` |
| 7 | Matters Won/Disposed | Count | COUNT WHERE outcome IN ('won','disposed_favour') AND fy = current | Green | `#kpi-won` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/litigation/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Active Matters Table (Main View)

**Search:** Matter ID, case number, branch, court/forum, party name. Debounced 350ms.

**Filters:**
- Matter Type: `All` · `Legal Notice Received` · `Legal Notice Sent` · `Civil Suit` · `Consumer Forum` · `High Court Writ` · `Supreme Court` · `Criminal Case` · `Arbitration` · `Revenue / Land` · `Labour Tribunal` · `Regulatory Proceeding`
- Status: `All` · `Active` · `Stay Granted` · `Pending Disposal` · `Settled` · `Disposed` · `Archived`
- Branch: dropdown
- Liability Range: `All` · `< ₹1 Lakh` · `₹1–10 Lakh` · `₹10–50 Lakh` · `> ₹50 Lakh`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Matter ID | Monospace | Yes | AUTO: LIT-YYYY-NNNN |
| Matter Type | Badge | Yes | Colour by type |
| Branch / Entity | Text | Yes | Branch name or "Group Level" |
| Petitioner | Text | Yes | Petitioner/complainant name |
| Respondent | Text | Yes | Group/branch as respondent, or vice versa |
| Court / Forum | Text | Yes | e.g., "District Consumer Forum – Hyderabad" |
| Case Number | Monospace | Yes | Court-issued case number |
| Filed Date | Date | Yes | Date case/notice was filed/received |
| Next Hearing / Deadline | Date | Yes | Red if today/tomorrow, amber if within 7 days |
| Assigned Advocate | Text | No | Advocate name; red if empty |
| Est. Liability | Currency | Yes | ₹ amount or "N/A"; red if > ₹10L |
| Status | Badge | Yes | Active / Stay / Settled / Disposed |
| Actions | Buttons | No | [View] · [Update] (Role 128 only) |

**Default sort:** Next Hearing / Deadline ASC
**Pagination:** Server-side · Default 25/page

---

### 5.2 Legal Notices Sub-Table

Specifically for legal notices (received and sent) — separate from court cases.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Notice ID | Monospace | Yes | |
| Direction | Badge | Yes | Received / Sent |
| Received / Sent Date | Date | Yes | |
| From / To | Text | Yes | Sender or recipient name |
| Subject | Text | Yes | Brief subject (80 chars) |
| Response Due | Date | Yes | Red if < 7 days |
| Response Sent | Badge | Yes | Yes (green) / No (red) |
| Actions | Buttons | No | [View] · [Mark Responded] (Role 128) |

---

## 6. Drawers & Modals

### 6.1 Drawer: `matter-detail` (760px, right-slide)
- **Tabs:** Overview · Parties · Hearings · Documents · Financials · Timeline
- **Overview tab:**
  - Matter ID, Type, Status, Filed Date, Court/Forum, Case Number
  - Branch/Entity, Brief Description, Background (free text)
  - Assigned Advocate, Advocate Firm, Contact, Engagement Letter date
  - Next Hearing Date, Response/Filing Deadline
  - Outcome (if disposed/settled): Summary
- **Parties tab:** Petitioner details, Respondent details, Co-petitioners, Co-respondents, Interveners
- **Hearings tab:** Table of all past and scheduled hearings — Date, Court, Judge, Proceedings Summary, Next Date Set. [+ Add Hearing] button (Role 128).
- **Documents tab:** All case documents — notices, plaints, written statements, court orders, judgements. Each: name, upload date, uploader, [Download].
- **Financials tab:** Estimated Liability, Litigation Cost to Date, Insurance Coverage (if any), Provision in Books (Yes/No), Settlement Amount (if settled).
- **Timeline tab:** Immutable audit log of all updates.

### 6.2 Modal: `record-matter` (680px)
| Field | Type | Required | Validation |
|---|---|---|---|
| Matter Type | Select | Yes | |
| Branch / Entity | Select | Yes | |
| Filed / Received Date | Date picker | Yes | Cannot be future |
| Court / Forum | Text | Yes | |
| Case Number | Text | No | May not be assigned yet |
| Petitioner | Text | Yes | |
| Respondent | Text | Yes | |
| Brief Description | Textarea | Yes | Min 30 chars |
| Assigned Advocate | Text | No | |
| Next Hearing / Deadline | Date | No | |
| Estimated Liability | Number | No | ₹ amount; 0 if unknown |
| Insurance Covered | Toggle | No | Yes / No |
| Initial Document | File | No | PDF, max 20MB |

**Footer:** Cancel · Save Matter

### 6.3 Modal: `add-hearing` (480px)
| Field | Type | Required |
|---|---|---|
| Hearing Date | Date + Time | Yes |
| Court / Bench | Text | Yes |
| Proceedings Summary | Textarea | No |
| Next Date Set | Date | No |
| Order / Interim Relief | Textarea | No |

**Footer:** Cancel · Save Hearing

---

## 7. Charts

### 7.1 Active Matters by Type (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Active Legal Matters by Type" |
| Data | Count per matter type |
| X-axis | Count |
| Y-axis | Matter type |
| Colour | `#3B82F6` |
| Tooltip | "[Type]: [N] active matters" |
| API endpoint | `GET /api/v1/group/{id}/legal/litigation/by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-matters-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Liability Exposure by Branch (Bar)

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Estimated Liability by Branch — Active Cases" |
| Data | Sum of estimated_liability per branch |
| X-axis | Branch name |
| Y-axis | ₹ amount |
| Colour | Red if > ₹10L per branch, Amber 1–10L, Blue < 1L |
| Tooltip | "[Branch]: ₹[total_liability] across [N] cases" |
| API endpoint | `GET /api/v1/group/{id}/legal/litigation/liability-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-liability-by-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Matter recorded | "Legal matter [LIT-YYYY-NNNN] recorded." | Success | 4s |
| Hearing added | "Hearing on [date] added to [LIT-YYYY-NNNN]." | Success | 3s |
| Hearing tomorrow alert | "Hearing scheduled for tomorrow — [LIT-YYYY-NNNN] at [Court]." | Warning | 8s |
| Response deadline alert | "Response deadline in [N] days for [LIT-YYYY-NNNN]." | Warning | 6s |
| Status updated | "Matter [LIT-YYYY-NNNN] status updated to [status]." | Success | 3s |
| Export triggered | "Generating litigation register export…" | Info | 3s |
| Document uploaded | "Document uploaded to [LIT-YYYY-NNNN]." | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No active matters | `scale` | "No Active Legal Matters" | "There are no active court cases, notices, or disputes." | Record First Matter |
| Filter returns no results | `search` | "No Matching Matters" | "No legal matters match the selected filters." | Clear Filters |
| Hearings sub-tab empty | `calendar` | "No Hearings Scheduled" | "No past or upcoming hearings on record for this matter." | Add Hearing |
| No legal notices | `mail` | "No Legal Notices on Record" | "No incoming or outgoing legal notices have been recorded." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI cards + 8-row table skeleton |
| Table filter/search | Spinner overlay |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton with tab placeholders |
| Hearing sub-tab | Shimmer rows |
| Document upload | Button spinner |

---

## 11. Role-Based UI Visibility

| Element | Legal Dispute (128, G1) | Compliance Mgr (109, G1) | POCSO Officer (112, G1) | Contract Admin (127, G3) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|
| All matters table | Full view | Regulatory cases only | POCSO cases only | Contract disputes only | Full view |
| [+ Record Matter] | Visible | Not visible | Not visible | Not visible | Visible |
| [Update] button | Visible | Not visible | Not visible | Not visible | Visible |
| Financials tab | Full access | Not visible | Not visible | Not visible | Full access |
| Estimated liability KPI | Visible | Not visible | Not visible | Not visible | Visible |
| Charts | Both visible | Not visible | Not visible | Not visible | Both visible |
| Export | Visible | Not visible | Not visible | Not visible | Visible |
| Alert banners | All | Compliance cases | POCSO cases | Contract cases | All |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/litigation/` | G1+ (scoped) | Paginated matters list |
| POST | `/api/v1/group/{id}/legal/litigation/` | Role 128, G4+ | Record new matter |
| GET | `/api/v1/group/{id}/legal/litigation/{lit_id}/` | G1+ (scoped) | Matter detail |
| PATCH | `/api/v1/group/{id}/legal/litigation/{lit_id}/` | Role 128, G4+ | Update matter |
| POST | `/api/v1/group/{id}/legal/litigation/{lit_id}/hearings/` | Role 128, G4+ | Add hearing record |
| GET | `/api/v1/group/{id}/legal/litigation/kpis/` | G1+ | KPI summary |
| GET | `/api/v1/group/{id}/legal/litigation/by-type/` | Role 128, G4+ | Chart data by type |
| GET | `/api/v1/group/{id}/legal/litigation/liability-by-branch/` | Role 128, G4+ | Liability chart data |
| POST | `/api/v1/group/{id}/legal/litigation/export/` | Role 128, G4+ | Async export |
| GET | `/api/v1/group/{id}/legal/litigation/{lit_id}/timeline/` | Role 128, G4+ | Audit log |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | `<div id="kpi-bar">` | GET `.../litigation/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | `<tbody id="litigation-table-body">` | GET `.../litigation/` | `#litigation-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET `.../litigation/?q={v}` | `#litigation-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Type filter | Type select | GET `.../litigation/?matter_type={v}` | `#litigation-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open drawer | [View] / row | GET `.../litigation/{lit_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Hearings tab lazy | Tab click | GET `.../litigation/{lit_id}/hearings/` | `#drawer-tab-content` | `innerHTML` | Lazy |
| Add hearing modal | [+ Add Hearing] in drawer | GET `/htmx/legal/litigation/{lit_id}/hearing-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Charts | Chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET `.../litigation/?page={n}` | `#litigation-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
