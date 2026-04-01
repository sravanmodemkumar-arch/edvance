# 40 — Disciplinary Case Register

- **URL:** `/group/hr/disciplinary/cases/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Disciplinary Committee Head (Role 51, G3)

---

## 1. Purpose

The Disciplinary Case Register is the master record of all staff disciplinary cases across all branches of the group. A disciplinary case enters this register when a staff misconduct issue is serious enough to require formal Group HR involvement — branch-level informal corrections do not appear here. Four triggers open a case: a branch principal escalates a staff misconduct matter to Group HR; a POCSO incident results in disciplinary action against a staff member; a financial irregularity investigation implicates a staff member; or a pattern of serious attendance violation (e.g., repeat absenteeism without sanction after branch-level warnings) is escalated by the branch.

The disciplinary process follows a defined legal lifecycle rooted in principles of natural justice. A case is opened with documentation of the alleged conduct. A Show-Cause Notice (SCN) is issued to the staff member, giving them a defined period (minimum 7 days) to submit a written response explaining their conduct. If the response is satisfactory — the staff member provides a credible explanation or the facts are found to be incorrect — the case may be closed with at most a formal warning. If the response is unsatisfactory or no response is received, a disciplinary hearing is scheduled. The Disciplinary Committee Head chairs the hearing, evidence is presented, the staff member has the right to be accompanied by a colleague or union representative, and an outcome decision is recorded. The staff member has the right to appeal the outcome within 14 days. Only after the appeal period — with either no appeal filed or an appeal resolved — is the case definitively closed.

Outcomes of the disciplinary process range from a formal Warning Letter (recorded in the staff file and affecting performance review) through Suspension (with or without pay pending investigation) to Termination (the most severe, requiring full documentation for legal defensibility) to Exoneration (the case is closed in the staff member's favour with no adverse record). All outcomes are recorded with the full reasoning, committee members present, and the signature of the Disciplinary Committee Head.

Cases involving minors — where a POCSO incident has led to the disciplinary case — are tagged Critical and carry additional requirements: mandatory NCPCR coordination, legal team involvement, and a copy of all case documents provided to the POCSO Coordinator for the POCSO Incident Register. These cases cannot be closed without POCSO Coordinator and HR Director sign-off.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Disciplinary Committee Head | G3 | Full CRUD + Case Management | Primary owner |
| Group HR Director | G3 | Full Read + Approval of Termination outcomes | Must approve before Termination is executed |
| Group HR Manager | G3 | Read + Add notes | Operational support |
| Group POCSO Coordinator | G3 | Read (POCSO-tagged cases only) | POCSO overlap coordination |
| Branch Principal | Branch G3 | Read (own branch cases only) | Receives escalation updates |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > Disciplinary > Disciplinary Case Register`

### 3.2 Page Header
- **Title:** Disciplinary Case Register
- **Subtitle:** Group-wide staff disciplinary case management
- **Actions (top-right):**
  - `+ Open New Case` (primary button)
  - `Export Case Register` (secondary button)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Critical (POCSO-related) case open without NCPCR coordination | "CRITICAL: Case [ID] is POCSO-related and NCPCR coordination has not been initiated. Immediate action required." | Red — non-dismissible |
| Termination outcome pending HR Director approval > 48 hours | "PENDING: Termination outcome for Case [ID] awaiting HR Director approval for more than 48 hours." | Amber — dismissible |
| SCN response deadline passed with no response | "NOTICE: Show-Cause Notice for Case [ID] has had no staff response. Default can be applied." | Amber — dismissible |
| Appeal period ending within 24 hours | "REMINDER: Appeal period for Case [ID] ends in [N] hours. No appeal filed — case can be closed." | Blue — dismissible |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Cases | Total open cases (all non-closed) | Amber if > 0 | No drill-down |
| Show-Cause Notices Pending Response | SCN issued, awaiting staff reply | Amber if > 0 | Filters to SCN stage |
| Hearings This Week | Count of hearings scheduled in current week | Blue if > 0 | Filters to hearing stage |
| Outcomes Pending | Cases where hearing done, outcome not yet decided | Amber if > 0 | Filters to pending outcome |
| Appeals Active | Cases in appeal stage | Amber if > 0 | Filters to appeal stage |
| Cases Closed This Month | Cases moved to Closed in current month | Green | Filters to closed this month |

---

## 5. Main Table — Disciplinary Cases

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Case ID | Text (e.g., DISC-2026-001) | No | No |
| Staff Name | Text + avatar | Yes | No |
| Branch | Badge | Yes | Yes — dropdown |
| Category | Badge (Misconduct / Attendance / Financial / POCSO-related) | No | Yes — multi-select |
| Severity | Badge (Critical / High / Medium / Low) | No | Yes — dropdown |
| Date Opened | Date | Yes | Yes — date range |
| Stage | Badge (Case Opened / SCN Issued / Response Received / Hearing Scheduled / Hearing Conducted / Outcome Pending / Appeal / Closed) | No | Yes — multi-select |
| Outcome | Badge (Pending / Warning / Suspension / Termination / Exonerated / N/A) | No | Yes — dropdown |
| Actions | Icon buttons (View / Update Stage / SCN / Schedule Hearing) | No | No |

### 5.1 Filters
- **Category:** multi-select
- **Severity:** dropdown
- **Stage:** multi-select
- **Outcome:** dropdown
- **Branch:** multi-select
- **Date Opened Range:** date picker
- **POCSO-Tagged:** Yes / No

### 5.2 Search
Free-text search on Case ID and Staff Name. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page. Shows `Showing X–Y of Z cases`.

---

## 6. Drawers

### 6.1 Open New Case
**Trigger:** `+ Open New Case` button
**Fields:**
- Staff Member (searchable dropdown)
- Branch (auto-populated, editable)
- Case Category (dropdown: Misconduct / Attendance / Financial / POCSO-related)
- Severity (radio: Critical / High / Medium / Low)
- Incident Date (date picker)
- Case Summary (textarea, required — minimum 150 characters)
- Evidence Documents (file upload — PDF, JPG, PNG)
- POCSO-related toggle (if yes, links to POCSO Incident Register case ID)
- Notify HR Director on opening (toggle, auto-on for Critical)
- Submit → creates case in Case Opened stage, assigns Case ID, notifies HR Manager

### 6.2 View Full Case
**Trigger:** Row click or eye icon
**Displays:** Full case record (all fields), SCN history, staff response (if filed), hearing schedule and notes, committee members, outcome decision text with reasoning, appeal record (if any), audit trail of every stage transition with timestamp and actor name, linked documents.

### 6.3 Update Case Stage
**Trigger:** Update Stage button
**Fields:** New Stage (dropdown, sequential — cannot skip stages), Stage Notes (textarea, required), any additional documents to attach, schedule hearing date/time (if moving to Hearing Scheduled), record outcome (if moving to Outcome Pending or post-hearing).

### 6.4 Delete Confirmation
Not available. Disciplinary cases are permanent legal records. Cases can only be moved to Closed (with outcome) or Archived (with HR Director approval and mandatory reason). Archived cases remain searchable.

---

## 7. Charts

**Case Stage Pipeline (Horizontal Bar / Funnel)**
- Bars: Case Opened → SCN Issued → Hearing → Outcome → Appeal → Closed
- Bar length = count at each stage
- POCSO-related cases highlighted in a separate colour overlay

**Cases by Category (Donut Chart)**
- Segments: Misconduct, Attendance, Financial, POCSO-related
- Date range selector

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Case opened | "Case [ID] opened for [Staff Name]. HR Manager notified." | Success | 4s |
| Stage updated | "Case [ID] moved to [Stage]." | Info | 4s |
| Critical case opened | "Critical case [ID] opened. HR Director and POCSO Coordinator notified." | Warning | 6s |
| Termination submitted for approval | "Termination outcome for Case [ID] submitted to HR Director for approval." | Warning | 5s |
| Case closed | "Case [ID] closed. Outcome: [Outcome]. Staff profile updated." | Success | 5s |
| Export triggered | "Case register export started." | Info | 4s |

---

## 9. Empty States

- **No active cases:** "No active disciplinary cases. The register will display cases as they are opened."
- **No results match filters:** "No cases match the selected filters. Try adjusting category or stage filters."
- **No cases this month:** "No cases closed this month."

---

## 10. Loader States

- Table skeleton: 6 rows with shimmer.
- KPI cards: shimmer on initial load.
- Case view drawer: spinner while full case record and audit trail loads.
- Chart area: placeholder with "Loading chart…" text.

---

## 11. Role-Based UI Visibility

| Element | Disciplinary Committee Head (G3) | HR Director (G3) | POCSO Coordinator (G3) |
|---|---|---|---|
| Open New Case button | Visible + enabled | Hidden | Hidden |
| Update Case Stage | Visible + enabled | Hidden | Hidden |
| Approve Termination | Hidden | Visible + enabled | Hidden |
| View Full Case | Visible (all) | Visible (all) | Visible (POCSO-tagged only) |
| Export Case Register | Visible | Visible | Hidden |
| Staff name column | Visible | Visible | Visible (POCSO cases) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/disciplinary/cases/` | JWT G3 | List disciplinary cases (paginated) |
| POST | `/api/v1/hr/disciplinary/cases/` | JWT G3 Disc. Head | Open new disciplinary case |
| GET | `/api/v1/hr/disciplinary/cases/{id}/` | JWT G3 | View full case record |
| PATCH | `/api/v1/hr/disciplinary/cases/{id}/stage/` | JWT G3 Disc. Head | Update case stage |
| POST | `/api/v1/hr/disciplinary/cases/{id}/approve-termination/` | JWT G3 HR Director | Approve termination outcome |
| POST | `/api/v1/hr/disciplinary/cases/{id}/close/` | JWT G3 Disc. Head | Close case with final outcome |
| GET | `/api/v1/hr/disciplinary/cases/kpis/` | JWT G3 | KPI summary data |
| GET | `/api/v1/hr/disciplinary/cases/charts/pipeline/` | JWT G3 | Pipeline chart data |
| GET | `/api/v1/hr/disciplinary/cases/charts/category/` | JWT G3 | Category donut chart data |
| GET | `/api/v1/hr/disciplinary/cases/export/` | JWT G3 | Export case register |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search case ID or staff | keyup changed delay:400ms | GET `/api/v1/hr/disciplinary/cases/?q={val}` | `#cases-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/disciplinary/cases/?{params}` | `#cases-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/disciplinary/cases/?page={n}` | `#cases-table-body` | innerHTML |
| Open new case drawer | click | GET `/api/v1/hr/disciplinary/cases/new/` | `#drawer-container` | innerHTML |
| Open view drawer | click | GET `/api/v1/hr/disciplinary/cases/{id}/` | `#drawer-container` | innerHTML |
| Submit open case form | submit | POST `/api/v1/hr/disciplinary/cases/` | `#cases-table-body` | innerHTML |
| Submit stage update | submit | PATCH `/api/v1/hr/disciplinary/cases/{id}/stage/` | `#cases-table-body` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/disciplinary/cases/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
