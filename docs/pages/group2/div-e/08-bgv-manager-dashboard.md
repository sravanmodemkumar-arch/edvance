# 08 — Group BGV Manager Dashboard

- **URL:** `/group/hr/bgv/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group BGV Manager (Role 48, G3)

---

## 1. Purpose

The Group BGV Manager Dashboard is the command centre for Background Verification (BGV) across all branches in the group. Background verification is not optional — it is a mandatory safety obligation under the POCSO Act for every individual who has physical access to minor students, regardless of their role. This includes not just teachers and administrators but also hostel wardens, security guards, kitchen staff, drivers, and maintenance personnel. The BGV Manager bears institutional accountability for ensuring 100% verification coverage and for taking immediate action when a verification fails or lapses.

BGV records have a defined validity period of three years. This means the BGV Manager must not only track new joiners awaiting their first verification but also monitor existing staff whose verifications are approaching expiry. An expired BGV for a student-facing staff member is treated with the same urgency as a pending BGV — the staff member must be restricted from student-facing duties until the renewal verification is completed. This dashboard surfaces both categories simultaneously, ensuring no expiry passes unnoticed.

Failed BGV cases are the most critical alerts this dashboard handles. A BGV failure — where a police verification, criminal record check, or previous employer check reveals disqualifying information — requires immediate escalation: the staff member must be suspended from duty pending HR Director review, and if the failure involves a conviction related to children, the matter must be reported to the relevant authorities. The red non-dismissible banner ensures the BGV Manager cannot overlook an active BGV failure.

The BGV Manager oversees a team of BGV Executives (Role 49) who do the actual processing. This dashboard gives the Manager a supervisory view: they can see the overall compliance rate, identify which branches or executives have the most backlogs, and intervene before verification delays accumulate. The Manager can also directly initiate verifications for high-priority cases or assign cases to specific executives from this dashboard.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group BGV Manager | G3 | Full read + write + escalation | Primary role; sees all branches |
| Group HR Director | G3 | Full read + action on failures | Receives escalation for failed BGVs |
| Group HR Manager | G3 | Read + initiation | Can initiate BGV for new joiners |
| Group BGV Executive | G3 | Own assigned cases only | Operational processing view (separate page) |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Background Verification
```

### 3.2 Page Header
- **Title:** `Group BGV Manager Dashboard`
- **Subtitle:** `BGV Compliance: [X]% · [N] Staff Total · [N] Verified · AY [current academic year]`
- **Role Badge:** `Group BGV Manager`
- **Right-side controls:** `+ Initiate BGV` · `Assign to Executive` · `Export BGV Report`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any student-facing staff has failed BGV | "🔴 CRITICAL: [N] staff member(s) with FAILED BGV are currently active in student-facing roles. Immediate suspension required." | Red (non-dismissible) |
| Any student-facing staff has expired BGV | "⚠ [N] staff member(s) have EXPIRED BGV and are in student-facing roles. Immediate action required." | Red (non-dismissible) |
| BGV not initiated for new joiners > 7 days post-join | "[N] staff joined more than 7 days ago with BGV not yet initiated. Compliance at risk." | Amber |
| BGV expiring in < 90 days | "[N] staff member(s) have BGV expiring within 90 days. Schedule renewal verifications." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| BGV Completed | Staff with current (non-expired) completed BGV | Blue | Completed list |
| BGV In Progress | Active cases with verification agency | Blue | In-progress list |
| BGV Pending — Not Initiated | Staff with no BGV record or not yet initiated | Red if > 0, Green if 0 | Pending initiation list |
| BGV Failed | Staff with one or more failed checks (any component) | Red (always) | Failed cases list |
| BGV Expiring in 90 Days | Staff whose BGV expiry is within 90 days | Amber if > 0 | Expiry queue |
| BGV Compliance Rate % | Completed ÷ (Total staff − In Progress) | Green ≥ 95%, Amber 85–95%, Red < 85% | Branch breakdown |

---

## 5. Main Table — Staff BGV Status (All Branches)

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to BGV detail) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Role | Text | Yes | Yes (text search) |
| Role Category | Badge (Teaching / Non-Teaching / Admin) | Yes | Yes |
| Join Date | Date | Yes | Yes (date range) |
| BGV Status | Badge (Completed / In Progress / Pending / Failed / Expired) | Yes | Yes |
| Verification Agency | Text | Yes | Yes (text search) |
| Initiated Date | Date | Yes | Yes (date range) |
| Completed Date | Date (blank if not completed) | Yes | No |
| Expiry Date | Date (red if < 90 days, grey if expired) | Yes | Yes (date range) |
| Assigned Executive | Text | Yes | Yes |
| Actions | View / Initiate / Re-initiate / Escalate | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| BGV Status | Checkbox | Completed / In Progress / Pending / Failed / Expired |
| Branch | Multi-select dropdown | All configured branches |
| Role Category | Checkbox | Teaching / Non-Teaching / Admin |
| Expiry Within | Dropdown | 30 days / 60 days / 90 days / Custom range |
| Assigned Executive | Dropdown | All BGV Executives |

### 5.2 Search
- Full-text: Staff name, verification agency name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `bgv-initiate` — Initiate Background Verification
- **Trigger:** `+ Initiate BGV` button or Actions → Initiate
- **Width:** 560px
- **Fields:**
  - Staff Name (required, searchable dropdown from Staff Directory)
  - Branch (required, auto-filled from staff record)
  - Role (required, auto-filled)
  - Verification Type(s) (required, checkboxes: Police Verification / Educational Qualification / Previous Employer / Identity Check / Address Verification)
  - Verification Agency (required, dropdown or text; agency list maintained by BGV Manager)
  - Agency Reference Number (optional, text; filled once agency accepts case)
  - Target Completion Date (required, date picker; max 45 days from today)
  - Assigned Executive (required, dropdown: active BGV Executives)
  - Priority (required, radio: Normal / High / Urgent — for new joiners)
  - Notes (optional textarea)

### 6.2 Drawer: `bgv-detail` — View BGV Case Detail
- **Trigger:** Click on staff name or Actions → View
- **Width:** 720px
- Shows: Staff profile summary, all verification components and their individual statuses, agency communication log, document uploads, assigned executive, timeline of status changes, expiry date, escalation history

### 6.3 Drawer: `bgv-update` — Update BGV Status
- **Trigger:** Actions → Re-initiate (for failed/expired) or by BGV Executive
- **Width:** 560px
- **Fields:** BGV Status update (dropdown), Agency update notes, Updated completion date estimate, Document upload (if new information)

### 6.4 Modal: Escalate Failed BGV
- Confirmation: "You are escalating the FAILED BGV for [Staff Name] at [Branch] to the Group HR Director. This will trigger immediate duty suspension. Confirm?"
- Note: This action is irreversible until the HR Director resolves the case
- Buttons: Confirm Escalation · Cancel

---

## 7. Charts

### 7.1 BGV Compliance by Branch (Horizontal Bar Chart)
- Y-axis: Branch names
- X-axis: Compliance % (0–100%)
- Colour: Green ≥ 95%, Amber 85–95%, Red < 85%
- Sorted by compliance rate ascending (worst at top)

### 7.2 BGV Pipeline Status (Stacked Bar Chart)
- X-axis: Months in current AY
- Segments: Initiated / In Progress / Completed / Failed
- Shows BGV throughput trend over time to identify processing speed

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| BGV initiated | "BGV initiated for [Staff Name]. Assigned to [Executive]. Agency notified." | Success | 4s |
| BGV status updated | "BGV record updated for [Staff Name]." | Success | 3s |
| Escalation triggered | "Failed BGV escalated to HR Director. [Staff Name] flagged for duty suspension." | Warning | 6s |
| Export triggered | "BGV compliance report is being generated." | Info | 4s |
| Agency not found | "Verification agency not found. Please add the agency before initiating." | Error | 5s |
| Validation error | "Please complete all required fields including at least one verification type." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No BGV records | "No BGV Records Found" | "No background verification records exist yet. Begin by initiating BGV for all active staff." | + Initiate BGV |
| All staff verified | "100% BGV Compliance" | "All active staff have current, completed background verifications. Well done." | View Expiry Queue |
| No failed cases | "No Failed BGV Cases" | "There are no failed background verification cases at present." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| BGV detail drawer open | Drawer spinner; verification component list loads progressively |
| Initiate BGV form submit | Button spinner + form disabled; agency notification in progress |
| Escalate BGV submit | Button spinner; system updating suspension flag |

---

## 11. Role-Based UI Visibility

| Element | BGV Manager (G3) | HR Director (G3) | HR Manager (G3) | BGV Executive (G3) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6) | Visible (all 6) | Visible (compliance rate + failed) | Hidden (see own page) |
| Full BGV Table | Visible + all actions | Visible (read + escalate) | Visible (read + initiate) | Not on this page |
| Failed BGV Alert | Visible + escalation button | Visible + action | Visible (read-only) | Not on this page |
| + Initiate BGV Button | Visible | Visible | Visible | Not on this page |
| Assign to Executive | Visible | Hidden | Hidden | Not on this page |
| Export Button | Visible | Visible | Visible | Not on this page |
| Expiry Date Column | Visible | Visible | Visible | Not on this page |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/bgv/kpis/` | JWT (G3) | All 6 KPI values |
| GET | `/api/v1/hr/bgv/records/` | JWT (G3) | Paginated staff BGV status table |
| POST | `/api/v1/hr/bgv/records/` | JWT (G3) | Initiate a new BGV for a staff member |
| GET | `/api/v1/hr/bgv/records/{id}/` | JWT (G3) | Full BGV case detail |
| PATCH | `/api/v1/hr/bgv/records/{id}/` | JWT (G3) | Update BGV status or agency info |
| POST | `/api/v1/hr/bgv/records/{id}/escalate/` | JWT (G3) | Escalate failed BGV to HR Director |
| POST | `/api/v1/hr/bgv/records/{id}/assign/` | JWT (G3) | Assign case to a BGV Executive |
| GET | `/api/v1/hr/bgv/charts/compliance-by-branch/` | JWT (G3) | Branch compliance bar chart data |
| GET | `/api/v1/hr/bgv/charts/pipeline/` | JWT (G3) | Monthly BGV pipeline stacked bar data |
| GET | `/api/v1/hr/bgv/export/` | JWT (G3) | Async compliance report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/bgv/kpis/` | `#kpi-bar` | `innerHTML` |
| Load BGV records table | `load` | GET `/api/v1/hr/bgv/records/` | `#bgv-table` | `innerHTML` |
| Open BGV detail drawer | `click` on staff name | GET `/api/v1/hr/bgv/records/{id}/` | `#bgv-detail-drawer` | `innerHTML` |
| Filter by BGV status | `change` on status filter | GET `/api/v1/hr/bgv/records/?status=...` | `#bgv-table` | `innerHTML` |
| Submit initiate form | `click` on Initiate | POST `/api/v1/hr/bgv/records/` | `#bgv-table` | `innerHTML` |
| Confirm escalation | `click` on Confirm Escalation | POST `/api/v1/hr/bgv/records/{id}/escalate/` | `#escalation-result` | `innerHTML` |
| Paginate table | `click` on page control | GET `/api/v1/hr/bgv/records/?page=N` | `#bgv-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
