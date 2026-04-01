# [04] — Regulatory Filings Tracker

> **URL:** `/group/legal/regulatory-filings/`
> **File:** `n-04-regulatory-filings-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — tracks all mandatory statutory and regulatory filings across all branches

---

## 1. Purpose

The Regulatory Filings Tracker consolidates every statutory and regulatory submission obligation for the Institution Group and its branches into a single management view. Large institution groups are required to submit data to multiple central and state government portals — AISHE (Annual Status in Higher Education), UDISE+ (Unified District Information System for Education), NITI Aayog / NGO-Darpan (for trusts and societies), State Education Department annual returns, CBSE annual school returns, and various labour compliance filings (PF/ESI ECR).

The Group Compliance Manager uses this tracker to know which filings are pending, which branches have submitted, which are at risk of missing deadlines, and which are already overdue. The Group Regulatory Affairs Officer (Role 111, G0) does the actual filing in external government portals — this page records the status, submission details, acknowledgements, and evidence for each filing.

Missing or delayed regulatory filings can result in: withdrawal of AISHE grade which affects NIRF rankings; delay in UDISE+ data publication affecting scholarship disbursements; lapse of trust registration affecting 12A/80G tax exemptions; and non-compliance with labour laws triggering PF/ESI inspections.

Scale: 5–50 branches · 10–30 filing types per branch per year · 100–1,500 filing records group-wide per year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews complex regulatory obligations externally |
| Group Compliance Manager | 109 | G1 | Read — Full Page + Update Status | Primary user; marks filings as submitted/pending |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Does actual government portal submissions externally |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant |
| Group Contract Administrator | 127 | G3 | No Access | Not relevant |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Limited | Views only if a regulatory default becomes a legal dispute |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,128], min_level=G1)` on all views. G4/G5 global read access.
>
> **Status update:** Role 109 can update filing status (Pending → Submitted) and attach acknowledgement documents. This is the only write operation on this page.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Regulatory Filings Tracker
```

### 3.2 Page Header
```
Regulatory Filings Tracker                      [Export Excel]  [Export PDF]
Group Compliance Manager — [Officer Name]
[Group Name] · [N] Active Filings · [N] Overdue · FY [year]
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any filing overdue (past deadline, not submitted) | "[N] filing(s) are overdue — deadline passed without submission. Immediate action required." | Critical (red) |
| Any filing due within 7 days | "[N] filing(s) are due within 7 days." | High (amber) |
| AISHE deadline within 30 days | "AISHE Annual Survey deadline approaching — [N] branches not yet submitted." | High (amber) |
| UDISE+ window closing within 14 days | "UDISE+ data entry window closes in [N] days — [N] branches pending." | High (amber) |
| PF/ESI ECR due this month | "Monthly PF/ESI ECR due by 15th of this month — [N] branches pending acknowledgement." | Medium (yellow) |
| Any trust registration nearing annual renewal | "Trust/Society registration renewal due within 60 days at [State] registrar." | Medium (yellow) |

---

## 4. KPI Summary Bar (7 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Filings This FY | Count | COUNT all filing records for current FY | Blue (static) | `#kpi-total-filings` |
| 2 | Submitted | Count | COUNT WHERE status = 'submitted' | Green | `#kpi-submitted` |
| 3 | Pending | Count | COUNT WHERE status = 'pending' AND due_date >= TODAY | Amber if > 10, Blue ≤ 10 | `#kpi-pending` |
| 4 | Overdue | Count | COUNT WHERE status != 'submitted' AND due_date < TODAY | Red if > 0, Green = 0 | `#kpi-overdue` |
| 5 | Submission Rate (This FY) | Percentage | submitted / total × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-submission-rate` |
| 6 | Branches With All Filings Current | Count | COUNT branches where all filings = submitted | Green if = total branches | `#kpi-branches-current` |
| 7 | Filings Due (Next 30 Days) | Count | COUNT WHERE due_date BETWEEN TODAY AND TODAY+30 AND status != 'submitted' | Amber > 10, Green ≤ 10 | `#kpi-due-30d` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/regulatory-filings/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Regulatory Filings Table (Main View)

All filing obligations for the group and all branches, with current status.

**Search:** Free-text on filing type name, branch name, authority/portal name. Debounced 350ms.

**Filters:**
- Status: `All` · `Submitted` · `Pending` · `Overdue` · `Not Applicable`
- Filing Type: dropdown — AISHE / UDISE+ / NITI Aayog / State Dept Return / CBSE Annual Return / PF ECR / ESI / Income Tax / GST Returns / Other
- Branch: dropdown of all branches + "Group Level"
- Due Period: `This Month` · `Next 30 Days` · `This Quarter` · `This FY`
- Frequency: `Monthly` · `Quarterly` · `Annual` · `One-Time`

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Filing Name | Text | Yes | e.g., "AISHE 2025–26 Annual Data Submission" |
| Authority / Portal | Text | Yes | e.g., "MoE AISHE Portal", "EPFO Unified Portal" |
| Branch | Text | Yes | Branch name or "Group Level" for trust-wide filings |
| Frequency | Badge | Yes | Monthly / Quarterly / Annual / One-Time |
| Period | Text | Yes | e.g., "FY 2025–26", "Sep 2025" |
| Due Date | Date | Yes | Red if overdue, amber if < 7d |
| Days Left | Badge | Yes | Integer; red if negative |
| Status | Badge | Yes | Submitted (green) / Pending (amber) / Overdue (red) / Not Applicable (grey) |
| Submitted Date | Date | No | Actual submission date (blank if pending) |
| Acknowledgement | Icon | No | Paperclip if acknowledgement document attached |
| Actions | Buttons | No | [View] · [Mark Submitted] (Role 109) |

**Default sort:** Due Date ASC (earliest first)
**Pagination:** Server-side · Default 25/page · Page size selector: 25/50/100

---

### 5.2 Branch-wise Filing Status Matrix

Compact pivot-style view: rows = branches, columns = major filing types. Each cell shows the status of that branch's filing of that type.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Branch | Text + link | Opens branch detail |
| AISHE | Status badge | ✅ / ⚠️ / ❌ |
| UDISE+ | Status badge | ✅ / ⚠️ / ❌ |
| CBSE Annual Return | Status badge | ✅ / ⚠️ / N/A |
| State Dept Return | Status badge | ✅ / ⚠️ / ❌ |
| PF ECR (this month) | Status badge | ✅ / ⚠️ / ❌ |
| ESI (this month) | Status badge | ✅ / ⚠️ / ❌ |
| GST Returns (quarterly) | Status badge | ✅ / ⚠️ / ❌ / N/A |
| Overall Status | Score badge | All ✅ = green; any ❌ = red |

Legend: ✅ Submitted · ⚠️ Pending · ❌ Overdue · N/A Not Applicable

---

## 6. Drawers & Modals

### 6.1 Drawer: `filing-detail` (680px, right-slide)
Opens on [View] button or row click.

- **Tabs:** Overview · Documents · History · Notes
- **Overview tab:**
  - Filing Name, Authority, Portal URL (read-only link), Frequency, Period
  - Branch, Group Level or specific branch
  - Due Date, Extended Due Date (if applicable), Days Remaining
  - Status badge, Submitted Date (if submitted)
  - Acknowledgement Number (if any), Reference Number
  - Responsible Role (who does this filing externally)
  - Notes / Special Instructions
- **Documents tab:** Acknowledgement receipts, submission PDFs, supporting data files. Each: filename, upload date, uploader, Download.
- **History tab:** All past submissions for this filing type at this branch — date, status, acknowledgement number, submitted by.
- **Notes tab:** Internal notes; Role 109 can add/edit notes.

### 6.2 Modal: `mark-submitted` (520px)
Used by Compliance Manager to record that a filing has been submitted by the Regulatory Affairs Officer.

| Field | Type | Required | Validation |
|---|---|---|---|
| Filing | Display only | — | Shows filing name and branch |
| Submitted Date | Date picker | Yes | Cannot be future; cannot be before current period start |
| Submitted By | Text | Yes | Name of person who filed |
| Acknowledgement Number | Text | No | Government portal ack number |
| Portal Reference | Text | No | Portal transaction ID |
| Acknowledgement Document | File upload | No | PDF/image, max 10MB |
| Notes | Textarea | No | Internal notes |

**Footer:** Cancel · Confirm Submission
**On success:** Row status changes to Submitted (green) + timestamp logged.

### 6.3 Modal: `export-filings-report` (480px)
- **Fields:** FY selector, Branch filter, Filing type filter, Status filter, Format (Excel/PDF)
- **Buttons:** Cancel · Export

---

## 7. Charts

### 7.1 Monthly Filing Submission Rate (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Monthly Filing Submission Rate — Current FY" |
| Data | Monthly: submitted% vs pending% |
| X-axis | Month (Apr → Mar) |
| Y-axis | Percentage (0–100%) |
| Colour | Submitted = `#22C55E`, Pending+Overdue = `#EF4444` |
| Tooltip | "[Month]: [N] submitted ([X]%), [N] overdue" |
| API endpoint | `GET /api/v1/group/{id}/legal/regulatory-filings/monthly-rate/` |
| HTMX | `hx-get` on load → `hx-target="#chart-monthly-rate"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Filings by Type — Status Donut

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Filing Status by Type — Current FY" |
| Data | Per filing type: count of submitted vs pending vs overdue |
| Segments | Each filing type as a segment (grouped by status) |
| Tooltip | "[Type]: [N] submitted, [N] pending, [N] overdue" |
| API endpoint | `GET /api/v1/group/{id}/legal/regulatory-filings/status-by-type/` |
| HTMX | `hx-get` on load → `hx-target="#chart-by-type"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Filing marked as submitted | "Filing '[Name]' marked as submitted for [Branch]." | Success | 4s |
| Overdue reminder | "[N] filings are now overdue. Please update status or escalate." | Warning | 5s |
| Export triggered | "Generating regulatory filings report…" | Info | 3s |
| Export ready | "Export ready. Click to download." | Success | 6s |
| Validation error on modal | "Please complete all required fields." | Error | 4s |
| Filter applied | "Showing [N] filings: [filter description]" | Info | 2s |
| Status auto-refresh | "Data refreshed — [N] filings updated." | Info | 2s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No filings configured | `file-text` | "No Filings Configured" | "Configure filing obligations for each branch to begin tracking." | Contact IT Admin |
| Filter returns no results | `search` | "No Matching Filings" | "No regulatory filings match your selected filters." | Clear Filters |
| All filings submitted | `check-circle` | "All Filings Up to Date" | "Every regulatory filing for all branches is submitted and current." | View History |
| Branch has no applicable filings | `info` | "No Obligations for This Branch" | "This branch has no mandatory regulatory filings configured." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 7 KPI shimmer cards + 10-row table skeleton |
| Table search/filter | Spinner overlay on table body + rows dimmed to 50% |
| KPI auto-refresh | Shimmer pulse on card values |
| Drawer open | Right-slide skeleton: tab bar + content area shimmer |
| Branch matrix load | Grid shimmer: N rows × 7 columns |
| Chart load | Grey canvas placeholder with centred spinner |
| Mark submitted action | Submit button spinner + disabled |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109, G1) | Legal Dispute (128, G1) | CEO/Chairman (G4/G5) | All Others |
|---|---|---|---|---|
| Filings table | Full view | Read-only; limited to dispute-related filings | Full view | No access |
| Branch matrix | Visible | Not visible | Visible | No access |
| [Mark Submitted] button | Visible | Not visible | Visible | No access |
| Export buttons | Visible | Not visible | Visible | No access |
| Charts | Both visible | Not visible | Both visible | No access |
| Alert banners | All visible | Critical only | All visible | No access |
| Notes tab in drawer | Read + Edit | Read-only | Read + Edit | No access |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/regulatory-filings/` | G1+ | Paginated filings list |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/{fil_id}/` | G1+ | Single filing detail |
| PATCH | `/api/v1/group/{id}/legal/regulatory-filings/{fil_id}/mark-submitted/` | Role 109, G4+ | Mark filing as submitted |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/kpis/` | G1+ | KPI summary bar values |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/branch-matrix/` | G1+ | Branch × type status matrix |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/monthly-rate/` | G1+ | Monthly submission rate chart |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/status-by-type/` | G1+ | Status by type donut chart data |
| POST | `/api/v1/group/{id}/legal/regulatory-filings/export/` | G1+ | Trigger async export |
| GET | `/api/v1/group/{id}/legal/regulatory-filings/{fil_id}/history/` | G1+ | Past submission history for one filing |

### Query Parameters for Filings List

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: filing name, authority, branch |
| `status` | string | submitted / pending / overdue / not_applicable |
| `filing_type` | string | aishe / udise / cbse_return / state_return / pf_ecr / esi / income_tax / gst / niti_aayog / other |
| `branch_id` | integer | Filter to specific branch |
| `frequency` | string | monthly / quarterly / annual / one_time |
| `due_period` | string | this_month / next_30d / this_quarter / this_fy |
| `fy` | string | Financial year e.g. `2025-26` |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 / 100; default 25 |
| `sort` | string | due_date / status / branch / filing_type |
| `order` | string | asc / desc |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + auto-refresh | `<div id="kpi-bar">` | GET `.../regulatory-filings/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | `<tbody id="filings-table-body">` | GET `.../regulatory-filings/` | `#filings-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET `.../regulatory-filings/?q={v}` | `#filings-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Filter by status | Status chips | GET `.../regulatory-filings/?status={v}` | `#filings-table-body` | `innerHTML` | `hx-trigger="click"` |
| Filter by type | Filing type dropdown | GET `.../regulatory-filings/?filing_type={v}` | `#filings-table-body` | `innerHTML` | `hx-trigger="change"` |
| Filter by branch | Branch dropdown | GET `.../regulatory-filings/?branch_id={id}` | `#filings-table-body` | `innerHTML` | `hx-trigger="change"` |
| Open detail drawer | Row click / [View] | GET `.../regulatory-filings/{fil_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Mark submitted modal | [Mark Submitted] button | GET `/htmx/legal/regulatory-filings/{fil_id}/submit-form/` | `#modal-container` | `innerHTML` | Opens modal |
| Submit form | Mark-submitted form | PATCH `.../regulatory-filings/{fil_id}/mark-submitted/` | `#filing-row-{fil_id}` | `outerHTML` | Row updates status on success |
| Branch matrix load | `<div id="branch-matrix">` | GET `.../regulatory-filings/branch-matrix/` | `#branch-matrix` | `innerHTML` | `hx-trigger="load"` |
| Chart loads | Both chart containers | GET `.../charts/...` | `#{chart-id}` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination controls | GET `.../regulatory-filings/?page={n}` | `#filings-table-body` | `innerHTML` | Replaces body only |

---

*Page spec version: 1.1 · Last updated: 2026-03-22*
