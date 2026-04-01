# 39 — Child Safety Audit Manager

- **URL:** `/group/hr/pocso/audits/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group POCSO Coordinator (Role 50, G3)

---

## 1. Purpose

The Child Safety Audit Manager is the page for planning, conducting, recording, and tracking annual child safety audits across all branches of the group. The annual child safety audit is a comprehensive inspection of each branch's compliance with child protection standards — it goes beyond training and BGV completion to evaluate the physical, procedural, and cultural safeguards that protect students on campus. The POCSO Coordinator either conducts these audits personally or delegates them to a qualified auditor, records findings through a structured checklist, grades the branch, and assigns corrective action items for any deficiencies found.

The audit checklist covers eight critical areas. POCSO Training Completion checks what percentage of branch staff have completed both the initial and annual refresher training. BGV Completion checks the background verification coverage for all student-contact staff. Incident Response Protocol checks whether the branch has a documented and accessible procedure for reporting POCSO incidents. Student Complaint Box checks whether a physical or digital complaint mechanism exists, is accessible to students, and has been reviewed recently. CCTV Coverage checks whether surveillance cameras are installed and operational in all corridors, classrooms, and entry/exit points — with no blind spots in common areas. No-Staff-Alone-With-Single-Student Policy checks whether the branch enforces the two-adult rule. POCSO Display Board checks whether the mandatory POCSO awareness poster (with CHILDLINE number, internal complaint process, and student rights) is visibly displayed. Internal Complaints Committee (ICC) checks whether the branch has a constituted, active ICC with at least one external member as required by law.

Each audit produces a branch grade: Compliant (all criteria met or minor issues with no time-sensitive risk), Partially Compliant (some criteria not met — corrective actions assigned with deadlines), or Non-Compliant (multiple serious failures — mandatory escalation to HR Director and Group CEO, corrective action plan with 30-day resolution required). A branch's audit grade is visible to the HR Director and feeds into the annual POCSO compliance report submitted to the group board.

Corrective action items are the key operational output of each audit. An action item specifies the deficiency, the required remediation, the responsible party (typically the branch principal), and the deadline. The POCSO Coordinator tracks open corrective actions on this page and sends reminders. Overdue actions — past their deadline with no resolution — automatically escalate to the HR Director.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group POCSO Coordinator | G3 | Full CRUD + Schedule + Record findings + Issue actions | Primary owner |
| Group HR Director | G3 | Full Read + Escalation receipt | Reviews grades and non-compliant branches |
| Group HR Manager | G3 | Read Only | General oversight |
| Branch Principal | Branch G3 | Own branch audit report only | Receives corrective actions; cannot see other branches |
| Group Training & Development Manager | G2 | Read (POCSO training column only) | Cross-reference with induction data |
| Group Performance Review Officer | G1 | No Access | Not applicable |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal > HR & Staff > POCSO Compliance > Child Safety Audit Manager`

### 3.2 Page Header
- **Title:** Child Safety Audit Manager
- **Subtitle:** Annual child safety compliance audits across all branches
- **Actions (top-right):**
  - `+ Schedule Audit` (primary button)
  - `Export Audit Report` (secondary button)
  - Academic Year selector (dropdown — defaults to current AY)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Non-Compliant branch found | "CRITICAL: [Branch Name] has been graded Non-Compliant. HR Director and Group CEO have been notified. Corrective action plan required within 30 days." | Red — non-dismissible |
| Branches with overdue corrective actions | "OVERDUE: [N] corrective action(s) are past their deadline across [N] branch(es)." | Amber — dismissible |
| Branches not yet audited in current AY with < 3 months to AY end | "REMINDER: [N] branches have not been audited this academic year. Schedule audits before AY close." | Amber — dismissible |
| All branches audited and compliant | "All branches have been audited and are Compliant this academic year. No open actions." | Green — auto-dismiss 10s |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Audits Completed This Year | Count of completed audits in current AY | Blue always | Filters table to completed |
| Branches Fully Compliant | Count graded Compliant | Green if = total branches | Filters to Compliant |
| Partially Compliant | Count graded Partially Compliant | Amber if > 0 | Filters to Partially Compliant |
| Non-Compliant | Count graded Non-Compliant | Red if > 0, Green if 0 | Filters to Non-Compliant |
| Open Corrective Actions | Total open action items across all branches | Amber if > 0 | Filters to corrective actions view |
| Overdue Actions | Actions past deadline | Red if > 0, Green if 0 | Filters to overdue actions |

---

## 5. Main Table — Branch Audit Status

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Branch | Text | Yes | Yes — dropdown |
| Last Audit Date | Date | Yes | Yes — date range |
| Auditor | Text | No | No |
| BGV % | Percentage | Yes | Yes — range |
| POCSO Training % | Percentage | Yes | Yes — range |
| CCTV Coverage % | Percentage | Yes | Yes — range |
| ICC Status | Badge (Constituted / Not Constituted / Expired) | No | Yes — dropdown |
| Overall Grade | Badge (Compliant / Partially Compliant / Non-Compliant / Not Yet Audited) | No | Yes — multi-select |
| Open Actions | Integer | Yes | Yes — range |
| Actions | Icon buttons (View Report / Issue Actions / Schedule) | No | No |

### 5.1 Filters
- **Overall Grade:** multi-select
- **Audit Date Range:** date picker
- **Open Actions:** Has open actions / No open actions
- **ICC Status:** Constituted / Not Constituted
- **Academic Year:** dropdown

### 5.2 Search
Free-text search on Branch Name and Auditor. Debounced `hx-get` on keyup (400 ms).

### 5.3 Pagination
Server-side, 20 rows per page. Shows `Showing X–Y of Z branches`.

---

## 6. Drawers

### 6.1 Schedule Audit
**Trigger:** `+ Schedule Audit` button or per-branch Schedule icon
**Fields:**
- Branch (dropdown, required)
- Audit Date (date picker)
- Auditor Name (text — POCSO Coordinator or delegated auditor)
- Audit Type (radio: Full Annual Audit / Follow-up Audit for corrective actions)
- Notes
- Notify Branch Principal (toggle, default on)
- Schedule button → creates audit record in Scheduled status

### 6.2 Record Audit Findings
**Trigger:** Record Findings button (available when audit status = Scheduled or In Progress)
**Fields (structured checklist with score/rating per item):**
- POCSO Training Completion % (auto-pulled from training tracker, editable)
- BGV Completion % (auto-pulled from BGV tracker, editable)
- Incident Response Protocol: Present / Not Present / Needs Update
- Student Complaint Box: Present and Active / Present but Not Reviewed / Not Present
- CCTV Coverage %: (0–100% estimated by auditor)
- No-Staff-Alone Policy: Enforced / Partially Enforced / Not Enforced
- POCSO Display Board: Visible and Compliant / Present but Non-Compliant / Absent
- ICC Status: Constituted with External Member / Constituted No External / Not Constituted
- Overall Auditor Notes (textarea)
- Overall Grade assignment (auto-suggested based on scores, editable with justification)
- Submit Findings → computes grade, opens corrective action assignment screen if needed

### 6.3 View Audit Report
**Trigger:** View Report icon or row click on completed audits
**Displays:** Full checklist responses, scores per area, overall grade, auditor notes, corrective action items list with deadlines and current status. PDF export button.

### 6.4 Issue Corrective Actions
**Trigger:** Issue Actions button or auto-opened after recording findings with Partially Compliant/Non-Compliant grade
**Fields:**
- Deficiency (text — pre-populated from checklist items that scored below threshold)
- Required Action (textarea)
- Responsible Party (dropdown: Branch Principal / Group HR / POCSO Coordinator)
- Deadline (date picker — default: 30 days for Non-Compliant, 60 days for Partially Compliant)
- Priority (radio: Immediate / High / Standard)
- Add Another Action button
- Submit All Actions → creates action records, notifies branch principal

---

## 7. Charts

**Branch Compliance Grade Distribution (Donut Chart)**
- Segments: Compliant (green), Partially Compliant (amber), Non-Compliant (red), Not Yet Audited (grey)
- For current academic year

**Checklist Score Radar / Spider Chart (per branch)**
- Each axis = one checklist area (POCSO Training, BGV, CCTV, ICC, etc.)
- Shows score 0–100% per area for selected branch
- Visible in the View Audit Report drawer
- Comparison option: this year vs. last year for same branch

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Audit scheduled | "Audit scheduled for [Branch] on [Date]. Branch principal notified." | Success | 4s |
| Findings recorded | "Audit findings recorded for [Branch]. Grade: [Grade]." | Success | 4s |
| Non-Compliant grade issued | "Non-Compliant grade issued for [Branch]. HR Director and Group CEO notified." | Warning | 6s |
| Corrective actions issued | "[N] corrective action(s) issued for [Branch]. Branch principal notified." | Success | 5s |
| Action marked complete | "Corrective action [ID] marked as resolved for [Branch]." | Success | 4s |
| Export triggered | "Audit report export started." | Info | 4s |

---

## 9. Empty States

- **No audits this year:** "No child safety audits have been completed for the current academic year. Schedule your first audit."
- **No results match filters:** "No branches match the selected filters."
- **No corrective actions:** "No open corrective actions. All audit findings have been resolved."

---

## 10. Loader States

- Branch table skeleton: 8 rows with shimmer.
- KPI cards: shimmer.
- Audit findings drawer: spinner while checklist and auto-pull data loads.
- Chart area: placeholder with "Loading chart…" text.
- Radar chart in view drawer: spinner while per-branch score data loads.

---

## 11. Role-Based UI Visibility

| Element | POCSO Coordinator (G3) | HR Director (G3) | Branch Principal |
|---|---|---|---|
| Schedule Audit button | Visible + enabled | Hidden | Hidden |
| Record Audit Findings | Visible + enabled | Hidden | Hidden |
| Issue Corrective Actions | Visible + enabled | Hidden | Hidden |
| View Audit Report | Visible (all branches) | Visible (all branches) | Visible (own branch only) |
| Export Audit Report | Visible | Visible | Visible (own branch only) |
| Corrective action status update | Visible + enabled | Hidden | Visible (mark own actions complete) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/pocso/audits/` | JWT G3 | List branch audit records |
| POST | `/api/v1/hr/pocso/audits/` | JWT G3 POCSO Coordinator | Schedule a new audit |
| GET | `/api/v1/hr/pocso/audits/{id}/` | JWT G3 | View full audit report |
| PATCH | `/api/v1/hr/pocso/audits/{id}/findings/` | JWT G3 POCSO Coordinator | Record audit findings and grade |
| POST | `/api/v1/hr/pocso/audits/{id}/actions/` | JWT G3 POCSO Coordinator | Issue corrective actions |
| PATCH | `/api/v1/hr/pocso/audits/actions/{action_id}/` | JWT G3 | Update corrective action status |
| GET | `/api/v1/hr/pocso/audits/kpis/` | JWT G3 | KPI summary data |
| GET | `/api/v1/hr/pocso/audits/charts/grades/` | JWT G3 | Grade distribution donut data |
| GET | `/api/v1/hr/pocso/audits/{id}/charts/radar/` | JWT G3 | Radar chart data for one audit |
| GET | `/api/v1/hr/pocso/audits/export/` | JWT G3 | Export audit report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Search branch name | keyup changed delay:400ms | GET `/api/v1/hr/pocso/audits/?q={val}` | `#audits-table-body` | innerHTML |
| Filter change | change | GET `/api/v1/hr/pocso/audits/?{params}` | `#audits-table-body` | innerHTML |
| Pagination click | click | GET `/api/v1/hr/pocso/audits/?page={n}` | `#audits-table-body` | innerHTML |
| Open schedule drawer | click | GET `/api/v1/hr/pocso/audits/new/` | `#drawer-container` | innerHTML |
| Open view report drawer | click | GET `/api/v1/hr/pocso/audits/{id}/` | `#drawer-container` | innerHTML |
| Submit schedule form | submit | POST `/api/v1/hr/pocso/audits/` | `#audits-table-body` | innerHTML |
| Submit findings form | submit | PATCH `/api/v1/hr/pocso/audits/{id}/findings/` | `#audits-table-body` | innerHTML |
| Refresh KPI bar | htmx:afterRequest | GET `/api/v1/hr/pocso/audits/kpis/` | `#kpi-bar` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
