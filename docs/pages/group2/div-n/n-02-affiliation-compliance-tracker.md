# [02] — Affiliation Compliance Tracker

> **URL:** `/group/legal/affiliation-compliance/`
> **File:** `n-02-affiliation-compliance-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Compliance Manager (Role 109, G1) — tracks CBSE/ICSE/State Board affiliation status for every branch

---

## 1. Purpose

The Affiliation Compliance Tracker provides a consolidated, real-time view of the affiliation status for every branch in the Institution Group. Each branch school or college operates under a board affiliation (CBSE, ICSE, State Board, CISCE, or University affiliation for degree colleges), and maintaining that affiliation in good standing is a primary legal obligation. A lapsed or revoked affiliation renders the institution unable to award certificates or conduct board examinations — an existential risk.

This page tracks the complete lifecycle of affiliation compliance: from initial application through document submission, inspection scheduling, approval/rejection, and annual or triennial renewal. The Group Compliance Manager uses this page to ensure no branch falls out of compliance due to a missed renewal, an outstanding document requirement, or an unresolved deficiency notice from the affiliating body. For a large group with 50 branches across multiple boards, this tracker is indispensable.

Regulatory basis: CBSE Affiliation Bye-laws 2018 (as amended), ICSE Regulations 2021, respective State Board affiliation rules. Affiliation numbers are issued per school per board and are unique identifiers referenced in all board communications, examinations, and result declarations.

Scale: 5–50 branches · 1 affiliation per branch · Renewal cycle annual or triennial · Alert threshold 90 days before expiry

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews documents outside platform |
| Group Compliance Manager | 109 | G1 | Read — Full Page | Primary user; sees all data, no edit |
| Group RTI Officer | 110 | G1 | Read — Limited | Can view affiliation numbers for RTI disclosure purposes |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Handles board correspondence externally |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant to this module |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant to this module |
| Group Contract Administrator | 127 | G3 | No Access | Affiliation is not a contract-type document |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Limited | Views only if affiliation dispute is active |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant to this module |

> **Access enforcement:** `@require_role(roles=[109,110,128], min_level=G1, division='N')` plus G4/G5 global access on all views and API endpoints.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Affiliation Compliance Tracker
```

### 3.2 Page Header
```
Affiliation Compliance Tracker                  [Export Excel]  [Export PDF]
Group Compliance Manager — Priya Krishnamurthy
Sunrise Education Group · 28 branches · FY 2025–26
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch affiliation expired | "CRITICAL: [N] branch(es) have expired affiliation. Board examination eligibility at risk." | Critical (red) |
| Any branch affiliation expiring within 30 days | "[N] branch affiliation(s) expire within 30 days — immediate renewal documentation required." | High (amber) |
| Any branch affiliation expiring within 90 days | "[N] branch affiliation(s) expire within 90 days. Begin renewal process now." | Medium (yellow) |
| Any branch affiliation under deficiency notice | "[N] branch(es) have open deficiency notices from board. Compliance response required." | High (amber) |
| Any affiliation application rejected | "Affiliation application rejected for [Branch Name]. Legal review required." | Critical (red) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Affiliations | N | COUNT all active affiliation records | Static display | `#kpi-total-affiliations` |
| 2 | Fully Compliant | N / Total | COUNT affiliations where status = 'approved' and expiry > TODAY+90 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-compliant` |
| 3 | Expiring (90 days) | Count | COUNT affiliations where expiry_date BETWEEN TODAY AND TODAY+90 | Red if > 0, Green = 0 | `#kpi-expiring-90` |
| 4 | Renewal In Progress | Count | COUNT affiliations where status IN ('renewal_submitted','docs_pending','inspection_scheduled') | Amber if > 3, Green ≤ 3 | `#kpi-renewal-in-progress` |
| 5 | Deficiency Notices | Count | COUNT affiliations where deficiency_status = 'open' | Red if > 0, Green = 0 | `#kpi-deficiencies` |
| 6 | Expired | Count | COUNT affiliations where expiry_date < TODAY | Red if > 0, Green = 0 | `#kpi-expired` |

**HTMX:** Cards use `hx-get="/api/v1/group/{id}/legal/affiliation/kpis/"` with `hx-trigger="load"` → `hx-swap="innerHTML"`.

---

## 5. Sections

### 5.1 Affiliation Records Table

Master list of all branch affiliations. Each row represents one branch's affiliation with its board.

Search: Search by branch name, affiliation number, board name, or city. Debounced 350ms. HTMX: `hx-get` with `?q=` → `hx-target="#affiliation-table-body"`.

Filter chips: `All` · `Compliant` · `Expiring Soon` · `Renewal In Progress` · `Deficiency Notice` · `Expired` · `Rejected`

Board filter dropdown: `All Boards` · `CBSE` · `ICSE/CISCE` · `State Board` · `NIOS` · `University`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Branch Name | Text + link | Yes | Opens branch detail drawer on click |
| City / District | Text | Yes | Location identifier |
| Board | Badge | Yes | CBSE (blue), ICSE (purple), State Board (green), etc. |
| Affiliation No. | Text (monospace) | Yes | Unique board-issued number |
| Class Range | Text | No | e.g., "I–XII" or "VI–XII" |
| Affiliation Type | Badge | No | Regular / Provisional / Self-Finance |
| Valid From | Date | Yes | Affiliation start date |
| Valid Until | Date | Yes | Expiry date; red if < 30d, amber if < 90d |
| Days to Expiry | Integer badge | Yes | Calculated; red if < 0 (expired) |
| Status | Badge | Yes | Compliant / Renewing / Deficiency / Expired / Rejected |
| Documents | Icon | No | Paperclip icon → count of attached docs |
| Last Inspected | Date | No | Date of last board inspection |
| Action | Button | No | "Details →" opens right drawer |

**Default sort:** Days to Expiry ASC (most urgent first)
**Pagination:** Server-side · Default 25/page

### 5.2 Board-wise Summary Tab

Aggregated view grouped by affiliating board. Shows how many branches per board are compliant/non-compliant.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Board | Text | Yes | Board name |
| Total Branches | Integer | Yes | Count of branches affiliated to this board |
| Compliant | Integer | Yes | Count status = 'approved' + not expiring |
| Expiring (90d) | Integer | Yes | Count expiring within 90 days |
| Deficiency | Integer | Yes | Count with open deficiency notices |
| Expired | Integer | Yes | Count with expired affiliation |
| Actions | Button | No | "Expand" to see branch-level detail |

---

## 6. Drawers & Modals

### 6.1 Drawer: `affiliation-detail` (720px, right-slide)
Opens when clicking any row in the affiliation table or clicking "Details →".
- **Tabs:** Overview · Documents · Renewal History · Deficiencies · Timeline
- **Overview tab fields:**
  - Branch Name, Board, Affiliation Number, Class Range, Type (Regular/Provisional)
  - Valid From / Valid Until, Days to Expiry (countdown timer if < 90 days)
  - Current Status badge, Principal Name, Contact Email
  - CBSE School ID / UDISE Code (linked reference)
  - Board's Regional Office / Liaison Officer
  - Notes (free text, read-only for G1)
- **Documents tab:** Grid of uploaded documents — Affiliation Certificate, NOC, Essentiality Certificate, Inspection Report, Deficiency Response. Each doc: filename, upload date, uploaded by, version, Download button.
- **Renewal History tab:** Table of all past affiliation cycles with dates, status, inspector names, outcomes.
- **Deficiencies tab:** List of all deficiency notices received from the board. Each entry: Notice date, deficiency description, deadline for response, response submitted, status (Open/Closed).
- **Timeline tab:** Full chronological audit log of all status changes, document uploads, correspondence, and user actions.
- **Footer buttons:** "Go to Inspection Tracker →" (N-11) · "Go to Renewal Calendar →" (N-18) · Close

### 6.2 Modal: `affiliation-renewal-alert`
- **Width:** 560px
- **Title:** "Renewal Deadline Alert — [Branch Name]"
- **Purpose:** Triggered from notification or from renewal calendar; shows all documents required for renewal submission with checklist
- **Fields:** Branch name, board, affiliation number, expiry date, days remaining, Document checklist (each item: required/uploaded), Next step recommendation
- **Buttons:** Close · "View Full Details →"

### 6.3 Modal: `pre-renewal-checklist` (620px)
Board-specific document checklist to prepare a renewal submission. Triggered from the affiliation-detail drawer footer or the Renewal Calendar (N-18).

| Field | Type | Notes |
|---|---|---|
| Branch Name | Display | Pre-filled |
| Board | Display | Pre-filled |
| Affiliation Number | Display | Pre-filled |
| Expiry Date / Days Remaining | Display | Countdown |
| Document Checklist | Checkbox list | Board-specific (see below) |
| Completion Summary | Progress bar | X / N documents ready |

**Board-specific document requirements:**

| Board | Required Documents |
|---|---|
| CBSE | Affiliation application form (Online SIS), NOC from State Govt, Land certificate/ownership proof, Building safety certificate, Fire safety NOC, Essentiality certificate, Fee structure, Staff statement, Inspection request |
| ICSE | Application letter, State Govt recognition certificate, Building plan approved by Municipality, Infrastructure compliance, Qualified staff list, Fee affidavit |
| State Board | State-specific form (varies); typically: Principal appointment order, Recognition letter, Infrastructure report, Fee certificate |
| University | University affiliation form, NAAC/inspection compliance, Governing body composition, Financial audit, Infrastructure report |

Each checklist item shows: Document name · Status (Uploaded ✅ / Not Uploaded ❌) · Upload button · Last uploaded date.

**Footer:** Close · Go to Documents Tab →

### 6.4 Modal: `export-affiliation-report`
- **Width:** 480px
- **Fields:** Board filter, Status filter, Date range, Format (PDF/Excel)
- **Buttons:** Cancel · Export
- **Behaviour:** POST to export endpoint; async delivery via toast

---

## 7. Charts

### 7.1 Affiliation Status Distribution (Donut Chart)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Affiliation Status Distribution" |
| Data | Count per status: Compliant, Expiring (90d), Renewal In Progress, Deficiency, Expired |
| X-axis | N/A |
| Y-axis | N/A |
| Colour | Compliant=`#22C55E`, Expiring=`#F59E0B`, Renewal=`#3B82F6`, Deficiency=`#EF4444`, Expired=`#6B7280` |
| Tooltip | "[Status]: [N] branches ([X]%)" |
| API endpoint | `GET /api/v1/group/{id}/legal/affiliation/status-distribution/` |
| HTMX | `hx-get` on load → `hx-target="#chart-affiliation-status"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Affiliation Expiry Timeline (Bar Chart)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Upcoming Affiliation Expiries by Quarter" |
| Data | Count of affiliations expiring per quarter for next 4 quarters |
| X-axis | Quarter (Q1 FY26, Q2 FY26, Q3 FY26, Q4 FY26) |
| Y-axis | Number of affiliations |
| Colour | `#F59E0B` (upcoming), `#EF4444` (overdue) |
| Tooltip | "[Quarter]: [N] affiliations expiring" |
| API endpoint | `GET /api/v1/group/{id}/legal/affiliation/expiry-timeline/` |
| HTMX | `hx-get` on load → `hx-target="#chart-expiry-timeline"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Page data loaded | "Affiliation data loaded — [N] branches" | Success | 2s |
| Export triggered | "Generating affiliation compliance report…" | Info | 3s |
| Export complete | "Export ready. Click to download." | Success | 6s |
| Filter applied | "Showing [N] affiliations matching: [filter]" | Info | 2s |
| Drawer opened | (no toast — silent) | — | — |
| Alert: expiring affiliation | "Reminder: [Branch] affiliation expires in [N] days" | Warning | 5s |
| Export error | "Export failed. Please try again." | Error | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No affiliations recorded | 🏫 school | "No Affiliations Configured" | "Add branch affiliation records to begin compliance tracking." | Contact Administrator |
| Filter returns no results | 🔍 search | "No Matches Found" | "No affiliations match the selected filters. Try adjusting your search." | Clear Filters |
| All affiliations compliant | ✅ check | "All Branches Fully Compliant" | "Every branch affiliation is current and in good standing." | View Renewal Calendar |
| Board tab — no branches for that board | 📋 clipboard | "No Branches Under This Board" | "No branch in this group is affiliated with [Board Name]." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial table load | Table skeleton: 10 shimmer rows × 14 columns |
| KPI card load | 6 grey shimmer card blocks with pulsing animation |
| Chart data fetch | Canvas placeholder with circular spinner centre |
| Drawer open | Right-slide skeleton: shimmer title, 5 tab buttons, content area |
| Search/filter | Overlay spinner on table body + opacity 0.5 on existing rows |
| Export generation | Progress bar in modal: 0%→100% |
| Pagination | Table body shimmer while new page loads |

---

## 11. Role-Based UI Visibility

| Element | Compliance Manager (109) | RTI Officer (110) | Legal Dispute (128) | CEO/Chairman (G4/G5) | All Others |
|---|---|---|---|---|---|
| Full Affiliation Table | Visible | Visible (read-only) | Visible (read-only) | Visible | No access |
| Board-wise Summary Tab | Visible | Visible | Hidden | Visible | No access |
| Export Buttons | Visible | Not visible | Not visible | Visible | No access |
| Alert Banners | Visible | Visible | Visible | Visible | No access |
| KPI Cards (all 6) | Visible | Partial (affiliation no. only) | Visible | Visible | No access |
| Drawer — all tabs | Visible | Overview tab only | Overview + Timeline | All tabs | No access |
| Deficiency Detail | Visible | Not visible | Visible | Visible | No access |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/affiliation/` | G1+ | Paginated affiliation list |
| GET | `/api/v1/group/{id}/legal/affiliation/{aff_id}/` | G1+ | Single affiliation detail |
| GET | `/api/v1/group/{id}/legal/affiliation/kpis/` | G1+ | KPI summary bar values |
| GET | `/api/v1/group/{id}/legal/affiliation/status-distribution/` | G1+ | Donut chart data |
| GET | `/api/v1/group/{id}/legal/affiliation/expiry-timeline/` | G1+ | Bar chart data — quarterly expiries |
| GET | `/api/v1/group/{id}/legal/affiliation/board-summary/` | G1+ | Board-wise aggregated summary |
| GET | `/api/v1/group/{id}/legal/affiliation/{aff_id}/documents/` | G1+ | Documents for one affiliation |
| GET | `/api/v1/group/{id}/legal/affiliation/{aff_id}/history/` | G1+ | Renewal history for one affiliation |
| GET | `/api/v1/group/{id}/legal/affiliation/{aff_id}/deficiencies/` | G1+ | Deficiency notices for one affiliation |
| POST | `/api/v1/group/{id}/legal/affiliation/export/` | G1+ | Trigger async export |

### Query Parameters for Affiliation List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Full-text search (branch, affiliation no., board) |
| `status` | string | compliant / expiring / renewal_in_progress / deficiency / expired |
| `board` | string | cbse / icse / state_board / nios / university |
| `expiry_within_days` | integer | Filter: expiring within N days |
| `branch_id` | integer | Filter to specific branch |
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Default 25, max 100 |
| `sort` | string | Field name to sort by |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Load affiliation table | `<tbody id="affiliation-table-body">` | `hx-get="/api/v1/group/{id}/legal/affiliation/"` | `#affiliation-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search affiliations | Search input | `hx-get` with `?q={value}` | `#affiliation-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Filter by status | Status chip buttons | `hx-get` with `?status={val}` | `#affiliation-table-body` | `innerHTML` | `hx-trigger="click"` |
| Filter by board | Board dropdown | `hx-get` with `?board={val}` | `#affiliation-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open detail drawer | Row click | `hx-get="/api/v1/group/{id}/legal/affiliation/{aff_id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Load KPI cards | KPI container | `hx-get="/api/v1/group/{id}/legal/affiliation/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Load donut chart | Chart container | `hx-get="/api/v1/group/{id}/legal/affiliation/status-distribution/"` | `#chart-affiliation-status` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Page nav buttons | `hx-get` with `?page={n}` | `#affiliation-table-body` | `innerHTML` | Replaces body only |
| Export report | Export button | `hx-post="/api/v1/group/{id}/legal/affiliation/export/"` | `#export-toast` | `innerHTML` | Shows toast on success |
| Pre-renewal checklist | Drawer footer / Calendar link | GET `/htmx/legal/affiliation/{aff_id}/pre-renewal-checklist/` | `#modal-container` | `innerHTML` | Opens board-specific checklist modal |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
