# [11] — Inspection Visit Tracker

> **URL:** `/group/legal/inspections/`
> **File:** `n-11-inspection-visit-tracker.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Compliance Manager (Role 109, G1) — regulatory/board inspection visit tracking, deficiency notice management

---

## 1. Purpose

The Inspection Visit Tracker manages all regulatory and accreditation inspection visits to branches across the Institution Group. Inspections are conducted by: CBSE/State Board (affiliation verification, infrastructure compliance); State Education Department (fee regulation, teacher qualification verification); NAAC (for degree colleges); ISO certification bodies; fire safety authorities; labour inspectors (PF/ESI compliance); and food safety authorities (for hostel kitchens).

The page tracks three phases of each inspection: (1) Pre-inspection preparation — document checklist completion and branch readiness; (2) Inspection visit — recording outcome, inspector details, and observations; (3) Post-inspection — managing deficiency notices, compliance response deadlines, and follow-up inspections. Unresolved deficiency notices can trigger affiliation suspension, which is an existential risk for the affected branch.

The Group Compliance Manager uses this page to ensure no deficiency notice goes unanswered and no inspection catches a branch unprepared. For large groups with 50 branches under multiple affiliating bodies, dozens of inspections occur each year.

Scale: 5–50 branches · 3–15 inspection types per branch per year · 20–200 inspection records per group per year

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Legal Officer | 108 | G0 | No Platform Access | Reviews deficiency responses externally |
| Group Compliance Manager | 109 | G1 | Full Read | Primary user; tracks all inspections |
| Group RTI Officer | 110 | G1 | No Access | Not relevant |
| Group Regulatory Affairs Officer | 111 | G0 | No Platform Access | Coordinates with state dept externally |
| Group POCSO Reporting Officer | 112 | G1 | No Access | Not relevant |
| Group Data Privacy Officer | 113 | G1 | No Access | Not relevant |
| Group Contract Administrator | 127 | G3 | Upload Only | Uploads deficiency response documents |
| Group Legal Dispute Coordinator | 128 | G1 | Read — Inspections with disputes | Views inspections that escalated to legal proceedings |
| Group Insurance Coordinator | 129 | G1 | No Access | Not relevant |

> **Access enforcement:** `@require_role(roles=[109,127,128], min_level=G1)`. G4/G5 full read.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Legal & Compliance  ›  Inspection Visit Tracker
```

### 3.2 Page Header
```
Inspection Visit Tracker                        [Export ↓]
Group Compliance Manager — [Name]
[Group Name] · [N] Inspections This AY · [N] Deficiencies Open
```

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Deficiency response deadline within 7 days | "[N] deficiency response(s) due within 7 days — board/authority deadline approaching." | Critical (red) |
| Deficiency response overdue | "[N] deficiency notice response(s) are overdue." | Critical (red) |
| Inspection scheduled next 7 days | "[N] inspection(s) scheduled in the next 7 days. Ensure branch preparation is complete." | High (amber) |
| Branch failed inspection (outcome: major deficiencies) | "[Branch] failed inspection with major deficiencies. Immediate action required to prevent affiliation action." | Critical (red) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Inspections (This AY) | Count | COUNT all inspection records | Blue | `#kpi-total-inspections` |
| 2 | Upcoming (Next 30d) | Count | COUNT WHERE inspection_date BETWEEN TODAY AND TODAY+30 | Amber > 5, Blue ≤ 5 | `#kpi-upcoming` |
| 3 | Open Deficiency Notices | Count | COUNT deficiency_notices WHERE status != 'closed' | Red > 0, Green = 0 | `#kpi-open-deficiencies` |
| 4 | Deficiency Responses Overdue | Count | COUNT deficiency_notices WHERE response_due < TODAY AND response_submitted = False | Red > 0, Green = 0 | `#kpi-responses-overdue` |
| 5 | Branches Passed (Satisfactory) | Count | COUNT WHERE outcome = 'satisfactory' in last 12 months | Green | `#kpi-passed` |
| 6 | Branches with Open Deficiency | Count | COUNT DISTINCT branches WHERE deficiency_notices.status = 'open' | Red > 0, Green = 0 | `#kpi-deficiency-branches` |

**HTMX:** `hx-get="/api/v1/group/{id}/legal/inspections/kpis/"` with `hx-trigger="load, every 300s"`.

---

## 5. Sections

### 5.1 Inspection Records Table

**Search:** Branch name, inspection type, inspector name, authority. Debounced 350ms.

**Filters:**
- Inspection Type: `All` · `CBSE Affiliation` · `State Board` · `State Edu Dept` · `NAAC` · `ISO` · `Fire Safety` · `Labour/PF` · `Food Safety` · `Other`
- Status: `All` · `Scheduled` · `Completed` · `Deficiencies Issued` · `Cleared` · `Follow-up Pending`
- Outcome: `All` · `Satisfactory` · `Minor Deficiencies` · `Major Deficiencies` · `Failed`
- Branch: dropdown
- AY: Academic Year selector

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Inspection ID | Monospace | Yes | AUTO: INS-YYYYMMDD-NNNN |
| Branch | Text | Yes | |
| Inspection Type | Badge | Yes | Colour by type |
| Authority | Text | Yes | e.g., "CBSE Regional Office – Chennai" |
| Scheduled Date | Date | Yes | |
| Conducted Date | Date | Yes | |
| Inspector Name(s) | Text | No | One or more inspectors |
| Outcome | Badge | Yes | Satisfactory (green) / Minor Def. (amber) / Major Def. (red) / Failed (red) / Pending (grey) |
| Deficiencies | Integer | Yes | Count of open deficiency notices; red if > 0 |
| Follow-up Date | Date | Yes | If follow-up inspection needed |
| Status | Badge | Yes | |
| Actions | Buttons | No | [View] · [Upload Response] (Role 127) |

**Default sort:** Conducted Date DESC (most recent first)
**Pagination:** Server-side · Default 25/page

---

### 5.2 Open Deficiency Notices Sub-Table

Dedicated view for all currently open deficiency notices requiring response.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Deficiency ID | Monospace | Yes | |
| Branch | Text | Yes | |
| From Inspection | Link | Yes | Links to parent inspection record |
| Deficiency Description | Text | Yes | |
| Issued Date | Date | Yes | |
| Response Deadline | Date | Yes | Red if overdue |
| Response Submitted | Badge | Yes | Yes (green) / No (red) |
| Compliance Status | Badge | Yes | Open / Responded / Closed / Follow-up |
| Actions | Buttons | No | [View] · [Submit Response] (Role 127) |

---

## 6. Drawers & Modals

### 6.1 Drawer: `inspection-detail` (720px)
- **Tabs:** Overview · Preparation Checklist · Deficiencies · Documents · Timeline
- **Overview tab:** Inspection ID, Branch, Authority, Type, Dates, Inspector names, Outcome, Follow-up date, Notes
- **Preparation Checklist tab:** Standard checklist items for this inspection type (pre-populated by platform). Each item: Description, Required (Yes/No), Status (Ready / Not Ready). Read-only for G1; editable by branch portal only (cross-linked from branch).
- **Deficiencies tab:** All deficiency notices from this inspection. Each: Deficiency description, issued date, response deadline, status, response submitted, [Upload Response] button.
- **Documents tab:** Inspection report, deficiency notice, compliance response, follow-up report. [Upload] (Role 127) + [Download].
- **Timeline tab:** Audit log.

### 6.2 Modal: `upload-deficiency-response` (560px)
| Field | Type | Required |
|---|---|---|
| Deficiency | Display | — |
| Response Date | Date picker | Yes |
| Response Summary | Textarea | Yes (min 50 chars) |
| Corrective Actions Taken | Textarea | Yes |
| Response Document | File (PDF) | Yes |
| Supporting Evidence | File (multi, PDF/image) | No |

**Footer:** Cancel · Submit Response

---

## 7. Charts

### 7.1 Inspection Outcomes by Branch (Heatmap-style Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Stacked horizontal bar (Chart.js 4.x) |
| Title | "Inspection Outcomes by Branch — Current AY" |
| Data | Per branch: count of Satisfactory / Minor Def. / Major Def. stacked |
| Colour | Satisfactory=green, Minor=amber, Major=red |
| Tooltip | "[Branch]: [N] Satisfactory · [N] Minor · [N] Major" |
| API endpoint | `GET /api/v1/group/{id}/legal/inspections/outcomes-by-branch/` |
| HTMX | `hx-get` on load → `hx-target="#chart-outcomes-branch"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Deficiency response uploaded | "Response submitted for deficiency [ID] at [Branch]." | Success | 4s |
| Deficiency deadline alert | "Deficiency response for [Branch] due in [N] days." | Warning | 6s |
| Inspection scheduled reminder | "Upcoming inspection at [Branch] in [N] days." | Info | 4s |
| Export triggered | "Generating inspection report…" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No inspections this AY | `clipboard-check` | "No Inspections Recorded" | "No inspection visits have been recorded for this academic year." | — |
| No open deficiencies | `check-circle` | "No Open Deficiency Notices" | "All deficiency notices have been resolved." | View History |
| Filter returns no results | `search` | "No Matching Records" | "No inspections match the selected filters." | Clear Filters |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Skeleton: 6 KPI cards + 8-row table |
| Deficiency sub-table | Shimmer rows |
| Chart load | Grey canvas + spinner |
| Drawer open | Right-slide skeleton |
| Checklist tab | Shimmer list items |
| File upload | Button spinner |

---

## 11. Role-Based UI Visibility

| Element | Compliance Mgr (109) | Contract Admin (127) | Legal Dispute (128) | CEO/Chairman |
|---|---|---|---|---|
| All inspections table | Full view | View only | Disputed only | Full view |
| Open deficiencies sub-table | Full view | View only | View only | Full view |
| [Upload Response] | Not visible | Visible | Not visible | Visible |
| Preparation checklist tab | View only | View only | Not visible | Full view |
| Charts | Visible | Not visible | Not visible | Visible |
| Export | Visible | Not visible | Not visible | Visible |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/legal/inspections/` | G1+ | Paginated inspection list |
| GET | `/api/v1/group/{id}/legal/inspections/{ins_id}/` | G1+ | Inspection detail |
| POST | `/api/v1/group/{id}/legal/inspections/{ins_id}/deficiencies/{def_id}/response/` | Role 127, G4+ | Upload deficiency response |
| GET | `/api/v1/group/{id}/legal/inspections/deficiencies/open/` | G1+ | Open deficiency notices |
| GET | `/api/v1/group/{id}/legal/inspections/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/legal/inspections/outcomes-by-branch/` | G1+ | Chart data |
| POST | `/api/v1/group/{id}/legal/inspections/export/` | G1+ | Async export |

### Query Parameters

| Parameter | Type | Description |
|---|---|---|
| `q` | string | Search: branch, type, inspector |
| `inspection_type` | string | cbse / state_board / state_edu / naac / iso / fire / labour / food / other |
| `status` | string | scheduled / completed / deficiencies / cleared / follow_up |
| `outcome` | string | satisfactory / minor / major / failed / pending |
| `branch_id` | integer | |
| `ay` | string | Academic year |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 / 50 |

---

## 13. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load + refresh | KPI container | GET `.../inspections/kpis/` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Table load | Table body | GET `.../inspections/` | `#inspection-table-body` | `innerHTML` | `hx-trigger="load"` |
| Search | Search input | GET with `?q=` | `#inspection-table-body` | `innerHTML` | Debounce 350ms |
| Deficiency sub-table load | Sub-table container | GET `.../inspections/deficiencies/open/` | `#deficiency-sub-table` | `innerHTML` | `hx-trigger="load"` |
| Open drawer | [View] / row | GET `.../inspections/{ins_id}/` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Deficiency response modal | [Upload Response] | GET `/htmx/legal/inspections/{def_id}/response-form/` | `#modal-container` | `innerHTML` | |
| Chart load | Chart container | GET `.../outcomes-by-branch/` | `#chart-outcomes-branch` | `innerHTML` | `hx-trigger="load"` |
| Pagination | Pagination | GET with `?page={n}` | `#inspection-table-body` | `innerHTML` | |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
