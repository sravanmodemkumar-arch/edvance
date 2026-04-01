# 23 — Staff Probation Tracker

- **URL:** `/group/hr/probation/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Probation Tracker manages the formal probation process for all new permanent staff across the group. A standard probation period is 6 months from the date of joining. During this period, the employment relationship is provisional: the institution can terminate employment without invoking the full disciplinary process, and the staff member has a reduced notice period. These legal and operational advantages make the probation window the most important performance review period in a staff member's first year. Failure to track probation end dates and conduct timely reviews results in staff "falling off" probation without a formal confirmation decision — a scenario that creates legal ambiguity about their employment status.

The probation review workflow is structured as follows: 30 days before a probation end date, the system sends an automated notification to the Branch Principal requesting a formal probation review submission. The Branch Principal is expected to provide a structured assessment covering attendance, punctuality, subject knowledge, classroom management (for teachers), professional conduct, and adherence to policies. This review must be submitted through the branch HR portal. Once submitted, the Group HR Manager reviews the assessment and takes one of three decisions: Confirm (the staff member transitions to permanent confirmed employee), Extend Probation (an additional 3-month extension for cases where performance needs more time), or Terminate (the staff member's employment is ended per probation terms). All three decisions are recorded with timestamped rationale.

The tracker also serves as an early warning system for retention. If a probation review shows concerns but the HR Manager decides to confirm anyway with conditions, those conditions are documented and tracked through the Performance Review Officer's workflow. If a probation is extended twice — a rare but possible scenario — the system flags it for HR Director review, as double-extended probations often signal a hiring mistake or an onboarding support failure.

Probation records are permanently linked to the staff profile (page 14). Even after confirmation, the probation record is visible in the Appraisals tab of the staff profile as the first formal assessment of the employee. This historical record is valuable for understanding long-term performance trends and for any future disciplinary proceedings that reference early-tenure behaviour.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access + double-extension review | Approves double probation extensions |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of probation decisions |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | Read-only | Can view confirmed + extended records |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | Read-only | Can view termination-during-probation records |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Probation → Staff Probation Tracker`

### 3.2 Page Header
- Title: "Staff Probation Tracker"
- Subtitle: "Monitor probation periods and confirmation decisions for all new permanent staff."
- Primary CTA: "+ Add Probation Record" (manual, for legacy entries)
- Secondary CTAs: "Export Probation Report" | "Send Overdue Review Reminders"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Probation end date ≤ 7 days, review not submitted | "[N] staff member(s) have probation ending within 7 days with no review submitted." | Red |
| Probation end date ≤ 30 days, review not submitted | "[N] staff member(s) require probation review within 30 days." | Orange |
| Probation end date passed, no decision recorded | "[N] staff member(s) have passed their probation end date without a recorded decision." | Red |
| Double probation extension flagged | "[N] staff member(s) have been on probation extension twice. HR Director review required." | Orange |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Staff on Probation | Count currently on active probation | Neutral blue | Filters to active |
| Confirmations Due in 30 Days | Count with probation end date ≤ 30 days | Orange if > 0 | Filters to upcoming |
| Confirmations Due in 7 Days | Count with probation end date ≤ 7 days | Red if > 0 | Filters to urgent |
| Probation Extended | Count currently on extension period | Amber | Filters to extended |
| Confirmed This Month | Count with decision = Confirmed in current month | Green | — |
| Terminated During Probation | Count with decision = Terminate (all time) | Neutral | Filters to terminated |

---

## 5. Main Table — Probation Records

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to staff profile) | Yes | Yes (search) |
| Branch | Text | Yes | Yes (dropdown) |
| Role | Text | Yes | Yes (search) |
| Join Date | Date | Yes | Yes (date range) |
| Probation End Date | Date | Yes | Yes (upcoming window filter) |
| Days Remaining | Integer / Overdue label | Yes | No |
| Review Status | Chip (Not Started / Principal Submitted / HR Reviewing / Decided) | Yes | Yes |
| Outcome | Chip (Pending / Confirmed / Extended / Terminated) or "—" | Yes | Yes |
| Extensions | Integer (0, 1, or 2) | No | Yes (> 0 filter) |
| Actions | View Review / Record Decision / Extend / Terminate | No | No |

### 5.1 Filters
- Review Status: All | Not Started | Principal Submitted | HR Reviewing | Decided
- Outcome: All | Pending | Confirmed | Extended | Terminated
- Days Remaining: Any | ≤ 7 Days | ≤ 30 Days | Overdue (past end date)
- Branch: All branches (dropdown)
- Extensions: All | With Extensions (> 0)

### 5.2 Search
Search by staff name or employee ID. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. Standard navigation with total record count displayed.

---

## 6. Drawers

### 6.1 Drawer: View Probation Review
Read-only. Displays: Branch Principal's submitted review with all assessment dimensions (Attendance %, Punctuality score, Subject Knowledge rating, Classroom Management, Professional Conduct, Policy Adherence, Overall Recommendation from Principal). Submission date and Principal name. Any supporting notes uploaded by Principal. HR Manager's internal notes field (editable). Decision history (if decision already recorded).

### 6.2 Drawer: Record Decision
Available when review_status = Principal Submitted or HR Reviewing.
Fields: Decision (Confirm / Extend Probation / Terminate — radio), Effective Date (date picker), Decision Rationale (textarea, required for all decisions). Additional fields per decision:
- Confirm: Confirmation Letter (checkbox to auto-generate), Conditions of Confirmation (optional textarea).
- Extend: Extension Duration (3 months / 6 months — dropdown), New Probation End Date (auto-calculated), Improvement Areas (textarea, required).
- Terminate: Last Working Day (date picker), Severance per Contract Terms (checkbox), Notice to staff member (checkbox — auto-sends system notification).
On Submit: PATCH decision to record, staff profile updated, contract status updated, all relevant stakeholders notified.

### 6.3 Drawer: Extend Probation
Shortcut access from "Extend" action. Pre-filled with current probation data. If this is the second extension (extensions = 1), a warning banner displays: "This is the second probation extension for this staff member. HR Director approval is required." Extension beyond 2 is blocked by system rules.

### 6.4 Modal: Terminate During Probation
Triggered by "Terminate" action. Confirmation prompt: "Terminating [Name] during probation. Last working day: [Date]. This action will create an exit record and cannot be undone." Required: Termination Reason (textarea). Confirm / Cancel.
On Confirm: records decision, creates exit record in Exit & Offboarding Manager (page 24), HR Director notified.

---

## 7. Charts

**Probation Outcome Distribution — Donut Chart:** shows split of all decisions in the last 12 months: Confirmed / Extended / Terminated. Rendered via Chart.js. Toggle: "Show Outcome Chart / Hide". Positioned below KPI bar.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Probation review viewed | — (no toast; drawer opens silently) | — | — |
| Decision recorded — Confirmed | "[Staff Name] confirmed as permanent employee." | Success | 5s |
| Decision recorded — Extended | "Probation extended for [Staff Name] by [N] months." | Warning | 5s |
| Decision recorded — Terminated | "[Staff Name] terminated during probation. Exit record created." | Warning | 5s |
| Double extension blocked | "Second extension requires HR Director approval." | Error | 6s |
| Reminder sent | "Probation review reminder sent to [Branch Principal Name]." | Info | 4s |
| Bulk reminders sent | "Review reminders sent to [N] branch principal(s)." | Info | 5s |
| Probation record added manually | "Probation record created for [Staff Name]." | Success | 4s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No staff on probation | "No Active Probation Records" | "New permanent joiners will appear here after onboarding." | — |
| Filter returns no results | "No Matching Records" | "Adjust your filters to find probation records." | Clear Filters |
| No decisions this month | "No Decisions This Month" | "No probation decisions have been recorded this month." | — |
| Terminated tab empty | "No Terminations During Probation" | "No staff members have been terminated during their probation period." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (15) |
| Filter change | Table body row skeletons |
| Review drawer open | Form/content skeletons in drawer |
| Decision submit | Button spinner + disabled state |
| Bulk reminder send | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) | HR Manager (42) | Performance Review Officer (46) | Disciplinary Head (51) |
|---|---|---|---|---|
| Record Decision | Visible | Visible + enabled | Hidden | Hidden |
| Extend Probation | Visible + double-ext approval | Visible (first only) | Hidden | Hidden |
| Terminate action | Visible | Visible | Hidden | Hidden |
| Add Probation Record | Visible | Visible | Hidden | Hidden |
| View Review drawer | Visible | Visible | Visible (read-only) | Visible (read-only) |
| Export Report | Visible | Visible | Hidden | Hidden |
| Internal HR Notes field | Visible + editable | Visible + editable | Visible read-only | Hidden |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/probation/` | JWT | List all probation records |
| POST | `/api/v1/hr/probation/` | JWT | Create probation record manually |
| GET | `/api/v1/hr/probation/{id}/` | JWT | Fetch probation record detail |
| GET | `/api/v1/hr/probation/{id}/review/` | JWT | Fetch principal's submitted review |
| PATCH | `/api/v1/hr/probation/{id}/decision/` | JWT | Record HR decision |
| PATCH | `/api/v1/hr/probation/{id}/extend/` | JWT | Extend probation |
| PATCH | `/api/v1/hr/probation/{id}/terminate/` | JWT | Terminate during probation |
| POST | `/api/v1/hr/probation/{id}/reminder/` | JWT | Send reminder to branch principal |
| POST | `/api/v1/hr/probation/bulk-reminder/` | JWT | Send bulk reminders |
| GET | `/api/v1/hr/probation/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/probation/chart/` | JWT | Outcome distribution chart data |
| GET | `/api/v1/hr/probation/export/` | JWT | Export report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/probation/?q={val}` | `#probation-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/probation/?status={}&outcome={}&branch={}&days={}` | `#probation-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/probation/?page={n}` | `#probation-table-body` | innerHTML |
| View Review drawer | click | GET `/group/hr/probation/{id}/review/drawer/` | `#drawer-container` | innerHTML |
| Record Decision drawer | click | GET `/group/hr/probation/{id}/decision/drawer/` | `#drawer-container` | innerHTML |
| Extend Probation drawer | click | GET `/group/hr/probation/{id}/extend/drawer/` | `#drawer-container` | innerHTML |
| Decision submit | submit | PATCH `/api/v1/hr/probation/{id}/decision/` | `#probation-row-{id}` | outerHTML |
| Terminate modal | click | GET `/group/hr/probation/{id}/terminate/modal/` | `#modal-container` | innerHTML |
| Terminate confirm | click | PATCH `/api/v1/hr/probation/{id}/terminate/` | `#probation-row-{id}` | outerHTML |
| Bulk reminder | click | POST `/api/v1/hr/probation/bulk-reminder/` | `#alert-banner` | outerHTML |
| Chart toggle | click | GET `/group/hr/probation/chart/` | `#chart-container` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
