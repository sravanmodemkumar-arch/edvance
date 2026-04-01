# [14] — Annual Returns & Statutory Filings

> **URL:** `/group/legal/annual-returns/`
> **File:** `n-14-annual-returns-statutory-filings.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — consolidated view of all mandatory annual and periodic statutory returns

---

## 1. Purpose

The Annual Returns & Statutory Filings page consolidates every mandatory annual and periodic statutory filing obligation across the Institution Group and all branches. While the Regulatory Filings Tracker (N-04) focuses on education-sector filings (AISHE, UDISE+, state education returns), this page covers the broader statutory compliance obligations — income tax returns for the trust, GST/TDS filings, PF/ESI employer returns, FCRA annual report, Shops & Establishments renewal, Factories Act compliance, and various labour law annual returns.

The Group Compliance Manager oversees this consolidated calendar of statutory obligations. Missing any annual return can trigger government notices, financial penalties, and in severe cases, revocation of trust/society registration or denial of 12A/80G benefits. For an institution group with 20+ branches as separate legal entities or one trust with multiple sub-units, the volume of mandatory filings can exceed 200 per year.

The page provides a master compliance calendar of all these obligations with: filing deadline tracking, submission status, penalty risk if overdue, and linkage to the financial year (not academic year — most statutory filings follow the April–March FY).

Scale: 1 trust entity + 5–50 branch locations · 50–200 statutory filings per FY · Monthly (PF/ESI) + quarterly (TDS) + annual (ITR, FCRA, labour) + one-time filings

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews complex filings externally |
| Group Compliance Manager | 109 | G1 | Full Read + Status Update | Primary user |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Does actual government portal submissions |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Filings linked to disputes | Views returns if a penalty became a dispute |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,128], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Annual Returns & Statutory Filings
```

### 3.2 Page Header
```
Annual Returns & Statutory Filings              [Export ↓]
Group Compliance Manager — [Name]
[Group Name] · FY [year] · [N] Filings Due This Month · [N] Overdue
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| ITR-7 (trust) overdue | "Income Tax Return for Trust (ITR-7) is overdue. Penalty interest accruing — IT Act s.234A." | Critical (red) |
| Monthly PF ECR due within 3 days | "Monthly PF ECR due by [date] — [N] branches not yet filed." | High (amber) |
| TDS return overdue | "TDS Quarterly Return (Form 26Q) overdue — penalty ₹200/day — IT Act s.234E." | Critical (red) |
| FCRA Annual Return overdue | "FCRA Annual Return is overdue. MHA may suspend FCRA registration." | Critical (red) |
| Shops & Establishments renewal due | "[N] branch Shops & Establishments licence(s) expiring within 60 days." | Medium (yellow) |
| Any filing with penalty accruing | "Penalty is currently accruing for [N] overdue filing(s)." | High (amber) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Filings (This FY) | Count | COUNT all filings for current FY | Blue | `#kpi-total` |
| 2 | Filed on Time | Count | COUNT WHERE submitted_date <= due_date | Green | `#kpi-on-time` |
| 3 | Overdue | Count | COUNT WHERE due_date < TODAY AND status != 'submitted' | Red > 0, Green = 0 | `#kpi-overdue` |
| 4 | Due This Month | Count | COUNT WHERE due_date within current month AND status != 'submitted' | Amber > 5, Blue ≤ 5 | `#kpi-due-month` |
| 5 | With Penalty Risk | Count | COUNT WHERE overdue AND has_penalty_clause = True | Red > 0, Green = 0 | `#kpi-penalty-risk` |
| 6 | Branches with All Filings Current | Count | COUNT WHERE all_filings_submitted = True | Green if = total | `#kpi-all-current` |
| 7 | Annual Compliance Rate | % | submitted_on_time / total × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-compliance-rate` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/annual-returns/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Statutory Filings Table

**Search:** Filing name, authority, entity/branch. Debounced 350ms.

**Filters:**
- Filing Category: `All` · `Income Tax` · `GST` · `TDS` · `PF / EPF` · `ESI` · `FCRA` · `Labour` · `Shops & Establishments` · `PT (Professional Tax)` · `Other`
- Frequency: `All` · `Monthly` · `Quarterly` · `Annual` · `One-Time`
- Status: `All` · `Submitted` · `Pending` · `Overdue`
- Entity: `Trust Level` + all branches
- Has Penalty Clause: `Yes` · `No`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Filing Name | Text | Yes | e.g., "ITR-7 — AY 2026–27", "PF ECR — March 2026" |
| Category | Badge | Yes | Colour-coded |
| Authority / Portal | Text | Yes | e.g., "Income Tax e-Filing Portal", "EPFO Unified Portal" |
| Entity | Text | Yes | Trust or specific branch |
| Frequency | Badge | Yes | |
| Period | Text | Yes | e.g., "FY 2025–26", "Q4 FY26" |
| Due Date | Date | Yes | Red if overdue |
| Submitted Date | Date | No | Blank if pending |
| Status | Badge | Yes | Submitted (green) / Pending (amber) / Overdue (red) |
| Penalty Risk | Badge | No | ₹[amount]/day or "None" |
| Ack. Number | Monospace | No | Government acknowledgement |
| Actions | Buttons | No | [View] · [Mark Submitted] (Role 109) |

**Default sort:** Due Date ASC
**Pagination:** Server-side · Default 25/page

---

### 5.2 Monthly Compliance Calendar View

A month-by-month summary showing which months have outstanding/overdue filings.

Each month card shows: Month name · [N] total filings due · [N] submitted · [N] overdue · Status badge (All Clear / Attention / Critical).

Clicking a month card filters the main table to that month's filings.

---

## 6. Drawers & Modals

### 6.1 Drawer: `filing-detail` (680px)
- **Tabs:** Overview · Documents · History · Notes
- **Overview:** Filing name, category, authority, entity, period, due date, actual filed date, filed by, ack number, status, penalty clause details
- **Documents:** Acknowledgement, filed return PDF, computation sheets. [Download].
- **History:** All past periods for this filing type at this entity — dates, status, ack numbers.
- **Notes:** Internal notes; editable by Role 109.

### 6.2 Modal: `mark-submitted-annual` (520px)
Same structure as Regulatory Filings mark-submitted modal:
- Submitted Date, Filed By, Acknowledgement Number, Reference, Acknowledgement Document upload, Notes.
**Footer:** Cancel · Confirm Submission

### 6.3 Modal: `export-returns` (480px)
- Fields: FY selector, Category filter, Entity filter, Status filter, Format.
- Buttons: Cancel · Export.

---

## 7. Charts

### 7.1 Monthly Filing Compliance — Grouped Bar

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Monthly Statutory Filing Compliance — FY [year]" |
| Data | Per month: on-time count, overdue count |
| X-axis | Month |
| Y-axis | Filing count |
| Colour | On-time = `#22C55E`, Overdue = `#EF4444` |
| Tooltip | "[Month]: [N] on time, [N] overdue" |
| API endpoint | `GET /api/v1/group/{id}/legal/annual-returns/monthly-compliance/` |
| HTMX | `hx-get` on load → `hx-target="#chart-monthly-compliance"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Filings by Category — Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Statutory Filings by Category — FY [year]" |
| Data | Count per category |
| Tooltip | "[Category]: [N] filings, [N] submitted" |
| API endpoint | `GET /api/v1/group/{id}/legal/annual-returns/by-category/` |
| HTMX | `hx-get` on load → `hx-target="#chart-by-category"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filing marked submitted | "Filing '[Name]' marked submitted. Ack: [number]." | Success | 4s |
| Overdue filing alert | "[N] statutory filings are now overdue." | Error | 6s |
| Penalty accruing | "Penalty accruing for [Filing] — ₹[rate]/day." | Error | 8s |
| Export triggered | "Generating statutory filings export…" | Info | 3s |
| Export ready | "Export ready. Click to download." | Success | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No filings configured | `file-text` | "No Filings Configured" | "Configure statutory filing obligations for all entities." | Contact IT Admin |
| All filings current | `check-circle` | "All Statutory Filings Current" | "All statutory obligations are submitted and up to date." | View History |
| Filter returns no results | `search` | "No Matching Filings" | | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI + 10-row table + month cards |
| Filter/search | Spinner overlay |
| Charts | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |
| Mark submitted | Button spinner |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|
| Full filings table | Visible | Dispute-related only | Full |
| Monthly calendar cards | Visible | Not visible | Visible |
| [Mark Submitted] | Visible | Not visible | Visible |
| Penalty column | Visible | Visible | Visible |
| Charts | Both | Not visible | Both |
| Export | Visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/annual-returns/` | G1+ | Paginated filings |
| GET | `/api/v1/group/{id}/legal/annual-returns/{fil_id}/` | G1+ | Detail |
| PATCH | `/api/v1/group/{id}/legal/annual-returns/{fil_id}/mark-submitted/` | Role 109, G4+ | Mark submitted |
| GET | `/api/v1/group/{id}/legal/annual-returns/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/legal/annual-returns/monthly-compliance/` | G1+ | Chart data |
| GET | `/api/v1/group/{id}/legal/annual-returns/by-category/` | G1+ | Chart data |
| POST | `/api/v1/group/{id}/legal/annual-returns/export/` | G1+ | Async export |

### Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: name, authority, entity |
| `category` | string | income_tax / gst / tds / pf / esi / fcra / labour / shops / pt / other |
| `frequency` | string | monthly / quarterly / annual / one_time |
| `status` | string | submitted / pending / overdue |
| `entity_id` | integer | Trust or specific branch |
| `has_penalty_clause` | boolean | |
| `fy` | string | Financial year |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100 |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../annual-returns/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | Table body | GET `.../annual-returns/` | `#returns-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET with `?q=` | `#returns-table-body` | `innerHTML` | Debounce 350ms |
| Category filter | Category select | GET with `?category=` | `#returns-table-body` | `innerHTML` | `hx-trigger="change"` |
| Month card click | Month card | GET `.../annual-returns/?month={YYYY-MM}` | `#returns-table-body` | `innerHTML` | `hx-trigger="click"` |
| Open drawer | [View] | GET `.../annual-returns/{fil_id}/` | `#right-drawer` | `innerHTML` | |
| Mark submitted modal | [Mark Submitted] | GET `/htmx/legal/annual-returns/{fil_id}/submit-form/` | `#modal-container` | `innerHTML` | |
| Charts | Chart containers | GET chart endpoints | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#returns-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
