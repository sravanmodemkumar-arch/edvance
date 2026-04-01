# 11 — Group Disciplinary Committee Head Dashboard

- **URL:** `/group/hr/disciplinary/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Disciplinary Committee Head (Role 51, G3)

---

## 1. Purpose

The Group Disciplinary Committee Head Dashboard oversees all staff misconduct cases across every branch in the group. Staff disciplinary proceedings are legally sensitive matters that require strict procedural adherence — the failure to follow proper process (issuing show-cause notices, conducting hearings, documenting outcomes) can expose the institution to wrongful termination litigation and regulatory scrutiny. This dashboard exists to ensure that every disciplinary case is processed consistently, transparently, and within defined timelines regardless of which branch it originates from.

Disciplinary cases in a school group vary widely in severity: from minor misconduct (unauthorised absence, classroom management failures) handled with written warnings, to serious misconduct (fraud, insubordination, policy violations) requiring suspension and formal inquiry, to grave misconduct (physical violence, substance abuse, financial misappropriation) that may result in termination and potential police reporting. This dashboard categorises cases by severity and routes them to the appropriate process pathway automatically.

The intersection with POCSO is a critical design concern. Any disciplinary case that involves conduct with or towards a student is automatically flagged with a POCSO overlap indicator, which sends an alert to both the POCSO Coordinator and the HR Director. These cases are never resolved at the branch level alone — the Group Disciplinary Committee must chair the proceedings, and the outcome must be reviewed by the HR Director before implementation. This cross-functional escalation pathway is enforced by the system: the "Close Case" action is disabled for POCSO-flagged cases until the HR Director's sign-off is recorded.

The committee head also manages the appeals pipeline. Staff who contest a disciplinary outcome have the right to file an appeal within 15 days. The appeals process has its own timeline (hearing within 30 days of appeal), and this dashboard tracks whether appeals are being addressed within the mandated window. Overdue appeals create legal risk and are flagged prominently.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Disciplinary Committee Head | G3 | Full read + write on all disciplinary cases | Primary role |
| Group HR Director | G3 | Full read + sign-off on POCSO-flagged outcomes | Must approve POCSO-overlapping closures |
| Group HR Manager | G3 | Full read | Monitoring; no action authority |
| Group POCSO Coordinator | G3 | Read-only on POCSO-flagged cases | Receives automatic alerts on these cases |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Disciplinary
```

### 3.2 Page Header
- **Title:** `Group Disciplinary Committee Head Dashboard`
- **Subtitle:** `[N] Active Cases · [N] Hearings This Week · [N] Awaiting Outcome · AY [current academic year]`
- **Role Badge:** `Group Disciplinary Committee Head`
- **Right-side controls:** `+ New Case` · `Hearing Schedule` · `Appeals Queue` · `Export Case Log`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any case involving conduct with a minor (POCSO overlap) | "🔴 POCSO-Flagged Case Active: [Staff Name] at [Branch]. POCSO Coordinator and HR Director have been notified. HR Director sign-off required before closure." | Red (non-dismissible) |
| Show-cause notice not issued within 7 days of case opening | "[N] case(s) have no show-cause notice issued within the 7-day requirement." | Red |
| Appeal hearing overdue (> 30 days since appeal filing) | "[N] appeal(s) have exceeded the 30-day hearing deadline." | Amber |
| Case pending outcome > 30 days from hearing | "[N] case(s) have been awaiting a formal outcome for more than 30 days post-hearing." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Cases | Total open disciplinary cases group-wide | Red if > 0, Blue if 0 | Full case table |
| Show-Cause Notices Issued | Notices issued in current AY | Blue | Filtered list |
| Hearings Scheduled This Week | Formal hearings in current week | Blue | Hearing schedule |
| Cases Awaiting Outcome | Post-hearing cases without a recorded outcome | Amber if > 0 | Filtered table |
| Appeals Pending | Active appeals awaiting hearing | Amber if > 0 | Appeals queue |
| Cases Resolved This Month | Formally closed cases in current calendar month | Green | Resolved log |

---

## 5. Main Table — Disciplinary Cases

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Case ID | Text (e.g., DISC-2026-0089) | Yes | No |
| Staff Name | Text (link to case detail) | Yes | Yes (text search) |
| Branch | Text | Yes | Yes (multi-select) |
| Charge Category | Badge (Minor Misconduct / Serious Misconduct / Grave Misconduct / POCSO-Flagged) | Yes | Yes |
| Date Opened | Date | Yes | Yes (date range) |
| Show-Cause Date | Date (red if overdue) | Yes | Yes |
| Hearing Date | Date (future = blue, past = neutral) | Yes | Yes (date range) |
| Status | Badge (Opened / SCN Issued / Hearing Scheduled / Hearing Done / Outcome Pending / Closed / Appeal Filed / Appealed Resolved) | Yes | Yes |
| Outcome | Badge (Warning / Suspension / Termination / Exonerated / Pending / — ) | Yes | Yes |
| POCSO Flag | Boolean icon (visible only if flagged) | Yes | Yes (flagged only) |
| Actions | View / Issue SCN / Schedule Hearing / Record Outcome / Close / View Appeal | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Status | Checkbox | Opened / SCN Issued / Hearing Scheduled / Hearing Done / Outcome Pending / Closed / Appeal Filed |
| Charge Category | Checkbox | Minor / Serious / Grave / POCSO-Flagged |
| Branch | Multi-select dropdown | All configured branches |
| Date Opened | Date range picker | Any range |
| POCSO-Flagged Only | Toggle | Yes |

### 5.2 Search
- Full-text: Staff name, Case ID
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `disc-case-create` — Open New Disciplinary Case
- **Trigger:** `+ New Case` button
- **Width:** 560px
- **Fields:**
  - Staff Name (required, searchable dropdown)
  - Branch (required, auto-filled from staff; editable)
  - Charge Category (required, dropdown: Minor / Serious / Grave)
  - Charge Description (required, textarea, min 100 chars)
  - Involves Conduct Towards Student/Minor (required, radio: Yes / No; if Yes, POCSO flag auto-set)
  - Incident Date (required, date picker)
  - Reporting Authority (required, text; who brought the complaint)
  - Supporting Documents (file upload, optional; PDF/images, max 5 files)
  - Show-Cause Notice Target Date (required, date picker; must be within 7 days)

### 6.2 Drawer: `disc-case-detail` — Case Detail View
- **Trigger:** Click on Staff Name or Case ID
- **Width:** 720px
- Shows: Full case timeline, all documents, show-cause notice copy, staff's written response (if received), hearing minutes, committee member names, outcome details, legal hold status, appeal record if any

### 6.3 Drawer: `disc-record-outcome` — Record Case Outcome
- **Trigger:** Actions → Record Outcome (enabled only for Hearing Done status)
- **Width:** 560px
- **Fields:**
  - Outcome Decision (required, dropdown: Exonerated / Written Warning / Final Warning / Suspension (with pay / without pay) / Termination / Referred to Police)
  - Effective Date (required, date picker)
  - Outcome Summary (required, textarea, min 100 chars)
  - Relief Order or Termination Letter Reference (optional, text)
  - HR Director Sign-off Required (read-only checkbox; auto-checked for POCSO-flagged cases)
- **POCSO-Flagged Constraint:** Outcome submission is blocked until HR Director sign-off is recorded in the system

### 6.4 Modal: Close Disciplinary Case
- Confirmation: "You are formally closing Case [DISC-ID] for [Staff Name] with outcome: [Outcome]. This action is final and will be recorded in the staff member's permanent HR record. All documents will be archived."
- Buttons: Confirm Close · Cancel

---

## 7. Charts

### 7.1 Case Status Distribution (Donut Chart)
- Segments: Opened / SCN Issued / Hearing Scheduled / Hearing Done / Outcome Pending / Closed
- Shows current active case pipeline distribution
- Helps identify bottlenecks (e.g., too many cases stuck at Hearing Done → Outcome Pending)

### 7.2 Cases by Branch and Category (Grouped Bar Chart)
- X-axis: Branch names
- Series: Minor / Serious / Grave / POCSO-Flagged
- Identifies branches with disproportionately high misconduct volumes

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Case opened | "Disciplinary case [DISC-ID] opened. Show-cause notice due by [Date]." | Warning | 5s |
| POCSO flag auto-set | "POCSO flag applied. POCSO Coordinator and HR Director notified automatically." | Warning | 6s |
| Outcome recorded | "Outcome recorded for Case [DISC-ID]. Staff member notified." | Success | 4s |
| POCSO case closure blocked | "Cannot close POCSO-flagged case without HR Director sign-off. Request sign-off first." | Error | 7s |
| Case closed | "Case [DISC-ID] closed and archived in [Staff Name]'s HR record." | Success | 5s |
| Export triggered | "Case log export is being prepared." | Info | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No active cases | "No Active Disciplinary Cases" | "There are no open disciplinary cases across the group. This is a positive indicator of staff conduct." | View Closed Cases |
| No hearings this week | "No Hearings Scheduled This Week" | "No formal disciplinary hearings are scheduled in the current week." | Hearing Schedule |
| No appeals pending | "No Pending Appeals" | "All disciplinary outcomes have been accepted or appeal periods have lapsed." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer + table skeleton (10 rows) |
| Case detail drawer open | Drawer spinner; case timeline loads progressively |
| Outcome record form submit | Button spinner + "Awaiting HR Director sign-off check…" indicator for POCSO cases |
| Charts load | Shimmer overlay on both chart panels |

---

## 11. Role-Based UI Visibility

| Element | Committee Head (G3) | HR Director (G3) | HR Manager (G3) | POCSO Coordinator (G3) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6) | Visible (all 6) | Visible (all 6) | Visible (POCSO-flagged count only) |
| Full Cases Table | Visible + all actions | Visible + sign-off action | Visible (read-only) | Visible (POCSO-flagged rows only) |
| + New Case Button | Visible | Hidden | Hidden | Hidden |
| POCSO Flag Indicator | Visible | Visible | Visible | Visible (highlighted) |
| Record Outcome Button | Visible (blocked for POCSO until sign-off) | Visible (provides sign-off) | Hidden | Hidden |
| Close Case Button | Visible (POCSO blocked) | Visible (after sign-off) | Hidden | Hidden |
| Charts | Visible | Visible | Visible | Visible (POCSO-flagged series only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/disciplinary/kpis/` | JWT (G3) | All 6 KPI values |
| GET | `/api/v1/hr/disciplinary/cases/` | JWT (G3) | Paginated case list |
| POST | `/api/v1/hr/disciplinary/cases/` | JWT (G3) | Open a new disciplinary case |
| GET | `/api/v1/hr/disciplinary/cases/{id}/` | JWT (G3) | Full case detail |
| POST | `/api/v1/hr/disciplinary/cases/{id}/record-outcome/` | JWT (G3) | Record case outcome |
| POST | `/api/v1/hr/disciplinary/cases/{id}/close/` | JWT (G3) | Close and archive case |
| POST | `/api/v1/hr/disciplinary/cases/{id}/signoff/` | JWT (G3) | HR Director sign-off for POCSO-flagged outcomes |
| GET | `/api/v1/hr/disciplinary/appeals/` | JWT (G3) | Appeals queue |
| GET | `/api/v1/hr/disciplinary/charts/status/` | JWT (G3) | Case status donut chart data |
| GET | `/api/v1/hr/disciplinary/charts/by-branch/` | JWT (G3) | Cases by branch and category chart data |
| GET | `/api/v1/hr/disciplinary/export/` | JWT (G3) | Async case log export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/disciplinary/kpis/` | `#kpi-bar` | `innerHTML` |
| Load cases table | `load` | GET `/api/v1/hr/disciplinary/cases/` | `#cases-table` | `innerHTML` |
| Open case detail drawer | `click` on Case ID or Staff Name | GET `/api/v1/hr/disciplinary/cases/{id}/` | `#case-drawer` | `innerHTML` |
| Filter by charge category | `change` on category filter | GET `/api/v1/hr/disciplinary/cases/?category=...` | `#cases-table` | `innerHTML` |
| Submit new case form | `click` on Submit | POST `/api/v1/hr/disciplinary/cases/` | `#cases-table` | `innerHTML` |
| Submit record outcome form | `click` on Record Outcome | POST `/api/v1/hr/disciplinary/cases/{id}/record-outcome/` | `#outcome-result` | `innerHTML` |
| Paginate cases table | `click` on page control | GET `/api/v1/hr/disciplinary/cases/?page=N` | `#cases-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
