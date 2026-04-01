# Page 10 — Admission Criteria Manager

- **URL:** `/group/adm/criteria/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Admission Criteria Manager defines the eligibility rules and academic cut-off marks that govern whether an applicant qualifies for a particular stream and branch. Without clearly configured criteria, the platform cannot auto-screen incoming applications, counsellors must make subjective judgements on eligibility, and inconsistencies arise across branches in the same group. This page ensures that every admission decision rests on documented, approved, and version-controlled criteria.

Criteria vary significantly across a large group. A competitive MPC programme at a flagship branch may mandate 90%+ marks in Class 10 Science and Mathematics along with a mandatory entrance test; a General stream at a smaller branch may run with a minimum 40% aggregate and no entrance requirement. The Admission Criteria Manager accommodates this diversity by allowing per-branch, per-stream, per-class configuration. The Director sets the group-level guidelines and approves each branch's criteria before the cycle opens, while the Coordinator is responsible for applying them during the application screening process.

Special circumstances inevitably arise — a student narrowly misses a cut-off but has other exceptional qualities. The platform handles this via a formal exception process: the Counsellor raises a criteria exception request, the Director reviews it, and if approved, the exception is logged with full attribution. The Criteria Exceptions Log (Section 5.4) provides transparency and an audit trail, preventing ad-hoc admissions that could undermine institutional integrity. Cut-off history (Section 5.3) enables year-on-year planning by showing how application volumes and enrolment rates tracked against each year's cut-off.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Create / Edit / Approve / Delete criteria | Only role that can approve criteria; can grant exceptions |
| Group Admission Coordinator (Role 24) | G3 | View + raise exception requests | Cannot create or modify criteria directly |
| Group Admission Counsellor (Role 25) | G3 | View only + submit exception requests | Read-only criteria; can initiate exception requests for their assigned students |
| Group Scholarship Manager (Role 27) | G3 | View only | Relevant for scholarship-track eligibility criteria |
| CEO / Executive | G3+ | View only | All criteria across all branches |

> **Enforcement:** `[Edit →]`, `[Approve →]`, and `[+ Add Criteria]` buttons are rendered only for `request.user.role == 'admissions_director'`. Django views enforce HTTP 403 on any criteria write from other roles. Exception requests are routed through a dedicated `CriteriaExceptionRequest` model with a Director-only approval endpoint.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Admission Criteria Manager
```

### 3.2 Page Header
- **Title:** Admission Criteria Manager
- **Subtitle:** `{current_cycle_name}` · Configure and manage eligibility rules per branch and stream
- **Right-side actions:** `[+ Add Criteria]` (Director only) · `[Clone from Branch →]` (Director only) · `[Bulk Approve Selected]` (Director only) · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Criteria pending Director approval | "{N} criteria record(s) awaiting your approval before the cycle can be marked open." |
| Criteria gaps detected (cycle open) | "{N} branch-stream combination(s) have no criteria configured — admissions are open." |
| Criteria expiring this cycle | "{N} criteria record(s) expire at the end of this cycle and need renewal." |
| Exceptions granted this cycle > threshold | "{N} criteria exceptions have been granted this cycle. Review exception log for patterns." |
| Criteria approval required before allocation | "Allocation cannot proceed for {Branch} — {Stream}: criteria pending approval." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/criteria/kpis/" hx-trigger="every 5m" hx-target="#criteria-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Branches Configured (%) | % of branches with at least one active criteria record for current cycle | Computed | Green ≥ 90%; amber 70–89%; red < 70% | Filters table to configured branches |
| Streams with Cut-offs Set | Count of distinct stream criteria with a cut-off score configured | `AdmissionCriteria.objects.filter(cutoff_score__isnull=False)` | Neutral (blue) | Filters table to records with cut-offs |
| Pending Approval | Criteria records in Draft or Pending Approval status | `status__in=['draft','pending_approval']` | Amber if > 0; green if 0 | Filters table to pending |
| Criteria Expiring (this cycle end) | Criteria records expiring at cycle close | `valid_until=cycle_end_date` | Amber if > 0; green if 0 | Filters table to expiring records |
| Exceptions Granted (this cycle) | Count of approved exception requests this cycle | `CriteriaExceptionRequest.status='approved'` | Amber if > 5; green otherwise | Opens exceptions log (5.4) |

---

## 5. Sections

### 5.1 Criteria Configuration Table

**Display:** Sortable, filterable table. One row per Branch + Stream + Class combination. 20 rows per page, server-side pagination.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Stream | MPC / BiPC / MEC / CEC / General |
| Class | Class 6 / 9 / 10 / 11 / 12 etc. |
| Min % (10th / Prev Year) | Minimum aggregate percentage required |
| Required Subjects | Comma-separated subject requirements |
| Entrance Test Required? | Yes / No badge |
| Cut-off Score | Entrance test cut-off (shown as "—" if no test) |
| Age Limit | Upper/lower age limit or "—" |
| Special Conditions | Truncated text; hover/click for full text |
| Status | Badge: Active (green) / Draft (grey) / Pending Approval (amber) |
| Actions | `[Edit →]` (Director) · `[Approve →]` (Director, visible only on Pending rows) |

**Filters:**
- Branch (multi-select)
- Stream (multi-select)
- Status (multi-select: Active / Draft / Pending Approval)

**Bulk Actions (Director only):** `[Bulk Approve Selected]` — approves all selected Pending rows in one action.

**HTMX Pattern:** Filter changes: `hx-get="/api/v1/group/{group_id}/adm/criteria/?{filters}"` `hx-target="#criteria-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`. Pagination: `hx-get` on page links, `hx-target="#criteria-table-wrapper"`. Bulk approve: `hx-post="/api/v1/group/{group_id}/adm/criteria/bulk-approve/"` `hx-target="#criteria-table-body"` `hx-swap="innerHTML"` `hx-confirm="Approve all selected criteria records?"`

**Empty State:** Illustration of empty clipboard. Heading: "No Criteria Configured." Description: "No admission criteria have been set up for this cycle and the selected filters. Use the Add Criteria button to begin." CTA: `[+ Add Criteria]` (Director only)

---

### 5.2 Criteria Gap Alert

**Display:** Collapsible alert panel. Lists branch-stream combinations for the current cycle that have no Active criteria record configured. Displays as a red alert panel when the cycle is open; amber when cycle has not yet opened.

| Column | Notes |
|---|---|
| Branch | Branch name |
| Stream | Stream name |
| Class | Class with no criteria |
| Cycle Status | Open / Upcoming |
| Risk Level | High (cycle open, no criteria) / Medium (cycle upcoming) |
| Action | `[Configure Now →]` (Director) · `[Request Configuration →]` (Coordinator) |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/criteria/gaps/"` `hx-trigger="load, every 5m"` `hx-target="#criteria-gap-panel"` `hx-swap="innerHTML"`

**Empty State:** Green banner: "All branch-stream combinations for the current cycle have active criteria configured."

---

### 5.3 Cut-off History

**Display:** Table showing the last 3 admission cycles per branch-stream combination. Sortable by branch, stream, or cycle year.

| Column | Notes |
|---|---|
| Branch | Branch short name |
| Stream | Stream name |
| Cycle | e.g., 2023–24, 2024–25, 2025–26 |
| Cut-off Score | Entrance test cut-off for that cycle |
| Min % Required | Aggregate % required |
| Applicants | Total applicants for that branch-stream-cycle |
| Enrolled | Total enrolled |
| Conversion Rate | `(Enrolled / Applicants) * 100` |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/criteria/history/?cycles=3"` `hx-trigger="load"` `hx-target="#cutoff-history-table"` `hx-swap="innerHTML"`; branch/stream filter: `hx-trigger="change"` on filter dropdowns.

**Empty State:** "No historical cut-off data available. Data will populate after the first completed admission cycle."

---

### 5.4 Criteria Exceptions Log

**Display:** Table of all students admitted under a formal exception (i.e., their scores were below the configured cut-off or they did not meet the required subjects criteria). Sortable, filterable.

**Columns:**

| Column | Notes |
|---|---|
| Student Name | Clickable — opens application detail |
| Branch | Branch name |
| Stream | Stream name |
| Actual Score / % | Student's actual score or aggregate percentage |
| Cut-off / Threshold | Configured cut-off at time of admission |
| Shortfall | Actual − Threshold (shown in red) |
| Exception Reason | Director-entered justification |
| Approved By | Director name |
| Approval Date | `DD MMM YYYY` |

**Filters:** Branch, Stream, Cycle, Date range

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/criteria/exceptions/"` `hx-trigger="load"` `hx-target="#exceptions-log-table"` `hx-swap="innerHTML"`; filter changes: `hx-trigger="change"`.

**Empty State:** Green checkmark graphic. "No exceptions granted this cycle. All admitted students have met the configured criteria."

---

## 6. Drawers & Modals

### 6.1 Criteria Edit Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** `[+ Add Criteria]` or `[Edit →]` in table (Director only)
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/criteria/{id}/edit/` (edit); `GET /api/v1/group/{group_id}/adm/criteria/new/` (create)

**Tabs:**

| Tab | Content |
|---|---|
| Eligibility | Branch selector, Stream selector, Class selector, Min aggregate %, Required subjects (multi-select), Age limit (min/max), Special conditions (free text) |
| Cut-offs | Entrance test required toggle; if enabled: test name, cut-off score, pass/fail rule, score validity period |
| Documents Required | Checklist of mandatory documents for this stream: Previous marksheet, TC, DOB certificate, Aadhar, Medical certificate, etc. — each with a Mandatory/Optional toggle |
| Exceptions Policy | Maximum exceptions allowed per cycle (numeric), Exception approval workflow: Director only / Director + CEO, Reason categories dropdown (configurable) |
| Preview | Read-only render of the criteria record as it will appear to Counsellors and applicants |

**Actions:** `[Save as Draft]` · `[Submit for Approval]` · `[Cancel]`

---

### 6.2 Criteria Exception Approval Modal
- **Width:** 400px (centred modal)
- **Trigger:** Counsellor or Coordinator clicks `[Request Exception]` on an application below cut-off; Director sees `[Review Exception →]` in the exceptions queue
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/criteria/exceptions/new/` (request form); `GET /api/v1/group/{group_id}/adm/criteria/exceptions/{id}/review/` (review form)

**Fields (request form):**
- Student name and application ID (read-only)
- Criteria shortfall details (read-only)
- Reason for exception (dropdown: Financial Hardship / Outstanding Extracurricular / Management Discretion / Medical / Other)
- Supporting justification (textarea)

**Fields (review form — Director):**
- All request details (read-only)
- Decision: Approve / Reject
- Director notes (required on rejection)
- `[Approve Exception]` · `[Reject]`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Criteria saved as draft | "Criteria saved as draft for {Branch} — {Stream}." | Info | 4s |
| Criteria submitted for approval | "Criteria submitted for Director approval." | Info | 4s |
| Criteria approved | "Criteria for {Branch} — {Stream} approved and now active." | Success | 4s |
| Bulk criteria approved | "{N} criteria records approved successfully." | Success | 5s |
| Criteria cloned from branch | "Criteria cloned from {Source Branch}. Review and approve before use." | Info | 5s |
| Exception request submitted | "Exception request submitted for {Student name}. Awaiting Director review." | Info | 5s |
| Exception approved | "Exception approved. {Student name} admitted under exception for {Stream}." | Success | 4s |
| Exception rejected | "Exception rejected. {Student name} does not meet criteria." | Warning | 5s |
| Criteria deletion blocked | "Cannot delete active criteria — applications are in progress." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No criteria configured | Empty clipboard graphic | "No Criteria Configured" | "Admission criteria have not been set up for this cycle." | `[+ Add Criteria]` (Director) |
| Filter returns no rows | Search-miss graphic | "No Matching Criteria" | "No criteria records match the selected branch, stream, or status filters." | `[Clear Filters]` |
| No gaps detected | Green shield graphic | "No Gaps Detected" | "All branch-stream combinations have active criteria for the current cycle." | — |
| No cut-off history | Chart (empty) | "No History Available" | "Cut-off history will populate after the first completed cycle." | — |
| No exceptions this cycle | Checkmark graphic | "No Exceptions Granted" | "All admitted students have met configured criteria this cycle." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (table rows + KPI bar shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Filter change | Table body skeleton (5-row shimmer) |
| Criteria gap panel load/refresh | Panel skeleton |
| Cut-off history table load | Table body skeleton |
| Exceptions log load | Table body skeleton |
| Criteria edit drawer open | Drawer content skeleton (3-block shimmer) |
| Drawer tab switch | Tab content area spinner |
| Exception approval modal load | Modal content skeleton |
| Bulk approve action | Button spinner + table overlay "Approving…" |
| Clone from branch operation | Page-level progress bar |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | Scholarship Mgr (27) | CEO |
|---|---|---|---|---|---|
| [+ Add Criteria] button | Visible | Hidden | Hidden | Hidden | Hidden |
| [Clone from Branch →] button | Visible | Hidden | Hidden | Hidden | Hidden |
| [Bulk Approve Selected] button | Visible | Hidden | Hidden | Hidden | Hidden |
| [Edit →] column action | Visible | Hidden | Hidden | Hidden | Hidden |
| [Approve →] column action | Visible | Hidden | Hidden | Hidden | Hidden |
| Criteria Gap Alert panel | Visible | Visible | Hidden | Hidden | Hidden |
| [Configure Now →] in gap panel | Visible | Hidden | Hidden | Hidden | Hidden |
| [Request Configuration →] in gap panel | Hidden | Visible | Hidden | Hidden | Hidden |
| Exceptions Policy tab in drawer | Visible | Hidden | Hidden | Hidden | Hidden |
| [Request Exception] button | Hidden | Visible | Visible | Hidden | Hidden |
| [Review Exception →] button | Visible | Hidden | Hidden | Hidden | Hidden |
| Criteria Exceptions Log | Visible | Visible | Hidden | Hidden | Visible |
| Cut-off History | Visible | Visible | Visible | Hidden | Visible |
| Criteria Configuration Table | Visible | Visible | Visible | Visible (read) | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/criteria/` | JWT G3+ | List all criteria records with filters |
| POST | `/api/v1/group/{group_id}/adm/criteria/` | JWT G3 (Director) | Create new criteria record |
| GET | `/api/v1/group/{group_id}/adm/criteria/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/criteria/gaps/` | JWT G3+ | List branch-stream combinations with no criteria |
| GET | `/api/v1/group/{group_id}/adm/criteria/history/` | JWT G3+ | Cut-off history for last N cycles |
| GET | `/api/v1/group/{group_id}/adm/criteria/exceptions/` | JWT G3+ | List all exception requests and approvals |
| POST | `/api/v1/group/{group_id}/adm/criteria/exceptions/` | JWT G3 | Submit a new criteria exception request |
| GET | `/api/v1/group/{group_id}/adm/criteria/exceptions/{id}/review/` | JWT G3 (Director) | Review form for exception request |
| PATCH | `/api/v1/group/{group_id}/adm/criteria/exceptions/{id}/` | JWT G3 (Director) | Approve or reject exception request |
| GET | `/api/v1/group/{group_id}/adm/criteria/{id}/edit/` | JWT G3 (Director) | Criteria edit form |
| PATCH | `/api/v1/group/{group_id}/adm/criteria/{id}/` | JWT G3 (Director) | Update criteria record |
| DELETE | `/api/v1/group/{group_id}/adm/criteria/{id}/` | JWT G3 (Director) | Delete criteria record (blocked if applications active) |
| POST | `/api/v1/group/{group_id}/adm/criteria/bulk-approve/` | JWT G3 (Director) | Bulk approve selected pending criteria |
| POST | `/api/v1/group/{group_id}/adm/criteria/clone/` | JWT G3 (Director) | Clone criteria from source branch to target branches |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/criteria/kpis/` | `#criteria-kpi-bar` | `innerHTML` |
| Filter change (branch/stream/status) | `change` | GET `/api/v1/group/{group_id}/adm/criteria/?{filters}` | `#criteria-table-body` | `innerHTML` |
| Pagination click | `click` | GET `/api/v1/group/{group_id}/adm/criteria/?page={n}&{filters}` | `#criteria-table-wrapper` | `innerHTML` |
| Sort column click | `click` | GET `/api/v1/group/{group_id}/adm/criteria/?sort={col}&order={dir}` | `#criteria-table-body` | `innerHTML` |
| Criteria gap panel load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/criteria/gaps/` | `#criteria-gap-panel` | `innerHTML` |
| Cut-off history table load | `load` | GET `/api/v1/group/{group_id}/adm/criteria/history/?cycles=3` | `#cutoff-history-table` | `innerHTML` |
| Exceptions log load | `load` | GET `/api/v1/group/{group_id}/adm/criteria/exceptions/` | `#exceptions-log-table` | `innerHTML` |
| Exceptions log filter change | `change` | GET `/api/v1/group/{group_id}/adm/criteria/exceptions/?{filters}` | `#exceptions-log-table` | `innerHTML` |
| [+ Add Criteria] / [Edit →] click | `click` | GET `/api/v1/group/{group_id}/adm/criteria/{id}/edit/` | `#criteria-edit-drawer` | `innerHTML` |
| Drawer tab switch | `click` | GET `/api/v1/group/{group_id}/adm/criteria/{id}/edit/?tab={tab}` | `#drawer-tab-content` | `innerHTML` |
| Criteria form save | `submit` | POST/PATCH `/api/v1/group/{group_id}/adm/criteria/{id}/` | `#criteria-table-body` | `innerHTML` |
| [Approve →] single row | `click` | PATCH `/api/v1/group/{group_id}/adm/criteria/{id}/` | `#criteria-table-body` | `innerHTML` |
| [Bulk Approve Selected] | `click` | POST `/api/v1/group/{group_id}/adm/criteria/bulk-approve/` | `#criteria-table-body` | `innerHTML` |
| Exception request modal open | `click` | GET `/api/v1/group/{group_id}/adm/criteria/exceptions/new/` | `#exception-modal` | `innerHTML` |
| Exception form submit | `submit` | POST `/api/v1/group/{group_id}/adm/criteria/exceptions/` | `#exception-modal` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
