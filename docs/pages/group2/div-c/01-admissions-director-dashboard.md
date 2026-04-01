# 01 — Group Admissions Director Dashboard

- **URL:** `/group/adm/director/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Admissions Director (Role 23, G3)

---

## 1. Purpose

The Group Admissions Director Dashboard serves as the strategic command centre for overseeing the entire admission lifecycle across all branches of the group. The director gains a real-time, bird's-eye view of application volumes, seat fill rates, branch-wise allocation queues, and cut-off configuration statuses for the current admission cycle. Every critical decision point — from approving seat matrices to setting admission criteria per stream — is surfaced here, ensuring that no branch falls behind and that group-level targets are met on schedule.

This page consolidates intake funnel analytics alongside scholarship exam scheduling so the director can correlate recruitment pipeline health with scholarship throughput. The admission funnel visualises each conversion stage (Enquiry → Application → Counselling → Offered → Enrolled) broken down per branch, enabling early identification of drop-off points. Seat fill rate charts provide immediate clarity on which branches need urgent outreach or reallocation of available seats.

Beyond operational oversight, the page functions as an audit trail and governance layer. The director's recent approval actions are logged and displayed, providing accountability and supporting compliance reviews. Admission criteria configuration gaps are highlighted as actionable alerts so that no branch inadvertently operates without defined eligibility rules for a given cycle. Together, these capabilities make this dashboard the definitive single screen for group-level admission governance.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director | G3 | Full read + write + approve + configure | Primary owner of this page |
| Group Admission Coordinator | G3 | Read-only (all sections) | Cannot modify cut-offs or seat matrix |
| Group Scholarship Exam Manager | G3 | Read — Section 5.5 (Scholarship Exam Calendar) only | No access to seat/allocation sections |
| Group Scholarship Manager | G3 | Read — Section 5.5 only | No access to seat/allocation sections |
| Group CEO | G3+ | Read-only (all sections) | View only; no actions |
| Chief Academic Officer (CAO) | G3+ | Read-only (all sections) | View only; no actions |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Director Dashboard
```

### 3.2 Page Header
- **Title:** `Admissions Director Dashboard`
- **Subtitle:** `Group Admissions · Current Cycle: [Cycle Name] · [Academic Year]`
- **Role Badge:** `Group Admissions Director`
- **Right-side controls:** `[Switch Cycle ▾]` `[Export Report]` `[Configure Criteria]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch has 0 admission criteria configured | "Admission criteria missing for [N] branch(es). Students cannot be evaluated without cut-offs." | Critical (red) |
| Pending branch allocations exceed 48 hours | "[N] allocation(s) have been pending for more than 48 hours. Immediate action required." | Warning (amber) |
| Scholarship exam in next 7 days with incomplete readiness | "Scholarship exam '[Name]' on [Date] — [N] branch(es) not yet confirmed ready." | Warning (amber) |
| Seat fill rate > 95% for any branch | "Branch [Name] has exceeded 95% seat fill. Consider capacity review before closing admissions." | Info (blue) |
| No active admission criteria set for current cycle | "No admission criteria have been set for the current cycle. Please configure immediately." | Critical (red) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Applications | Count of applications in current cycle | `admissions_application` table | Green if ≥ target; amber if 75–99% of target; red if < 75% | Opens Section 5.3 filtered view |
| Seats Filled % | (Enrolled / Total seats) × 100 across all branches | `seat_matrix` + `enrollment` | Green ≥ 80%; amber 50–79%; red < 50% | Opens Section 5.2 seat fill chart |
| Conversion Rate | (Enrolled / Enquiries) × 100 for current cycle | `enquiry` + `enrollment` tables | Green ≥ 30%; amber 15–29%; red < 15% | Opens admission funnel modal |
| Pending Allocations | Count of applications awaiting branch allocation | `application_allocation` WHERE status = 'pending' | Green = 0; amber 1–10; red > 10 | Opens Section 5.3 allocation queue |
| Scholarship Exam Registrations | Total registrations for all upcoming scholarship exams | `scholarship_exam_registration` | Informational (blue always) | Opens Section 5.5 calendar |
| Demo Conversions (Month) | Prospects who attended demo and enrolled this month | `demo_attendance` + `enrollment` | Green ≥ 20%; amber 10–19%; red < 10% | Opens demo conversion modal |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Admission Funnel Overview

**Display:** Chart.js 4.x funnel-style stacked horizontal bar chart rendered inside `<canvas id="admission-funnel">`. Each bar represents a stage (Enquiry, Application, Counselling, Offered, Enrolled) with colour-coded segments per branch. Branch-level toggle checkboxes sit above the chart.

**Filters:**
- Branch (multi-select)
- Stream (MPC / BiPC / MEC / CEC / Commerce)
- Cycle (current cycle pre-selected)
- Date range

**HTMX Pattern:**
```html
<div id="funnel-chart-container"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/funnel/"
     hx-trigger="load, change from:#funnel-filters"
     hx-target="#funnel-chart-container"
     hx-swap="innerHTML">
```

**Empty State:** "No funnel data available for the selected filters. Ensure admission cycle is active and enquiries have been logged."

---

### 5.2 Seat Fill Rate by Branch

**Display:** Chart.js horizontal bar chart. Each bar represents a branch with sub-bars per stream. A red dashed line marks the 90% threshold. Branch labels link to the branch allocation detail drawer.

**Columns/Fields shown below chart:** Branch Name, Stream, Total Seats, Enrolled, Available, Fill %

**Filters:**
- Stream
- Sort by: Fill % (desc default) / Branch Name / Available Seats

**HTMX Pattern:**
```html
<div id="seat-fill-chart"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/seat-fill/"
     hx-trigger="load, change from:#seat-fill-filters"
     hx-target="#seat-fill-chart"
     hx-swap="innerHTML">
```

**Empty State:** "Seat matrix has not been configured for this cycle. Use [Configure Seat Matrix] to set up seats per branch and stream."

---

### 5.3 Branch-wise Allocation Queue

**Display:** Sortable, selectable table. Rows with pending > 24 hours are highlighted amber; > 48 hours highlighted red.

**Columns:** Branch Name | Stream | Pending Applications | Urgent (>48h) | Last Allocation Date | Allocated By | Action

**Actions per row:** `[Allocate Now →]` opens branch-allocation-detail drawer.

**Filters:** Branch, Stream, Urgency (All / Urgent / Normal), Status

**HTMX Pattern:**
```html
<div id="allocation-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/allocation-queue/"
     hx-trigger="load, every 5m"
     hx-target="#allocation-queue"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: checkmark icon. "All allocations are up to date. No pending branch allocations at this time."

---

### 5.4 Cut-off Configuration Status

**Display:** Table listing all branches + streams with cut-off configuration state for the current cycle.

**Columns:** Branch | Stream | Subjects Covered | Cut-offs Set | Set By | Last Modified | Status Badge (Configured / Pending / Overdue) | Action

**Status Badge Rules:** Configured = green; Pending (within deadline) = amber; Overdue (past deadline, not set) = red.

**Actions:** `[Configure →]` opens cut-off-config-detail drawer for director.

**Filters:** Branch, Stream, Status (All / Configured / Pending / Overdue)

**HTMX Pattern:**
```html
<div id="cutoff-status"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/cutoff-status/"
     hx-trigger="load"
     hx-target="#cutoff-status"
     hx-swap="innerHTML">
```

**Empty State:** "No cut-off data found. Ensure admission cycle is created and branches are enrolled in the current cycle."

---

### 5.5 Scholarship Exam Calendar

**Display:** Horizontal timeline of upcoming scholarship exams in the next 30 days. Each event shows: Exam Name, Date, Type (Merit / Need-based / RTE), Registration count, Status badge.

**Fields per event card:** Exam Name | Date & Time | Exam Type | Registered | Venue / Online | Status (Scheduled / In Progress / Results Pending / Completed)

**Filters:** Exam Type, Branch, Date range

**HTMX Pattern:**
```html
<div id="scholarship-calendar"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exams/upcoming/"
     hx-trigger="load"
     hx-target="#scholarship-calendar"
     hx-swap="innerHTML">
```

**Empty State:** "No scholarship exams scheduled in the next 30 days. Use [Schedule Exam] to add one."

---

### 5.6 Admission Criteria Gaps

**Display:** Alert-style list. Each item is a branch+stream combination where admission criteria (eligibility marks, subjects, age limit) have not been configured for the current cycle.

**Fields per item:** Branch | Stream | Missing Criteria Type | Days Until Admissions Open | Action

**Actions:** `[Configure Now →]` opens cut-off-config-detail drawer directly for that branch/stream.

**HTMX Pattern:**
```html
<div id="criteria-gaps"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/criteria-gaps/"
     hx-trigger="load"
     hx-target="#criteria-gaps"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: checkmark shield. "All branches and streams have admission criteria configured for this cycle."

---

### 5.7 Top Sources of Admissions

**Display:** Chart.js 4.x doughnut/pie chart. Segments: Walk-in, Referral (parent), Alumni Referral, Demo Class, Scholarship Exam, Online (website), Other.

**Fields:** Source label, Count, Percentage

**Filters:** Branch (All / specific), Stream, Cycle, Date range

**HTMX Pattern:**
```html
<div id="admission-sources"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/sources/"
     hx-trigger="load, change from:#source-filters"
     hx-target="#admission-sources"
     hx-swap="innerHTML">
```

**Empty State:** "No enrollment source data available for the selected filters."

---

### 5.8 Recent Approval Actions

**Display:** Audit trail table showing the last 10 actions taken by the director. Read-only. Paginated (20 rows default, server-side).

**Columns:** Timestamp | Action Type | Subject (student name / branch / cut-off label) | Details | IP Address | Status (Completed / Reversed)

**Filters:** Action Type (All / Allocation / Cut-off / Criteria / Seat Matrix / Override)

**HTMX Pattern:**
```html
<div id="audit-log"
     hx-get="/api/v1/group/{{ group_id }}/adm/director/audit-log/"
     hx-trigger="load"
     hx-target="#audit-log"
     hx-swap="innerHTML">
```

**Empty State:** "No approval actions recorded yet for this session or cycle."

---

## 6. Drawers & Modals

### 6.1 Branch Allocation Detail Drawer
- **Width:** 640px
- **Trigger:** `[Allocate Now →]` in Section 5.3
- **Tabs:**
  - **Overview:** Branch summary — total seats, enrolled, available per stream
  - **Pending Applications:** Table of pending applicants with `[Assign to Stream]` action
  - **History:** Past allocations made for this branch this cycle
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/allocation/"`

### 6.2 Seat Matrix Detail Drawer
- **Width:** 640px
- **Trigger:** Click on any branch in Section 5.2 chart
- **Tabs:**
  - **Current Matrix:** Table — Stream, Total Seats, Reserved (RTE/Govt), Available for General, Enrolled
  - **Edit Matrix:** Inline edit fields (director only) — each seat count editable, `[Save Changes]`
  - **History:** Seat matrix revision log
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/seat-matrix/"`

### 6.3 Cut-off Configuration Detail Drawer
- **Width:** 560px
- **Trigger:** `[Configure →]` in Section 5.4 or `[Configure Now →]` in Section 5.6
- **Tabs:**
  - **Set Cut-offs:** Per-subject minimum marks + aggregate cut-off entry form for selected branch + stream
  - **Preview:** Estimated eligible applicants based on current applications vs proposed cut-off
  - **History:** Previous cut-off values for this stream/branch across past cycles
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/cutoff/"` (GET); `hx-post` on save

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Allocation submitted | "Branch allocation saved successfully." | Success | 4s |
| Cut-off configuration saved | "Cut-off marks updated for [Stream] at [Branch]." | Success | 4s |
| Seat matrix updated | "Seat matrix for [Branch] updated. Changes take effect immediately." | Success | 5s |
| Allocation failed (validation) | "Allocation failed: no seats available in the selected stream." | Error | 6s |
| Cut-off save failed | "Failed to save cut-off. Please check all fields and try again." | Error | 6s |
| Criteria gap resolved | "Admission criteria configured for [Branch] — [Stream]." | Success | 4s |
| Exam readiness confirmed | "Branch [Name] marked as ready for [Exam Name]." | Success | 4s |
| Export initiated | "Report export started. You will be notified when ready." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No admission cycle active | Calendar icon | "No Active Admission Cycle" | "Create or activate an admission cycle to begin managing applications." | `[Create Cycle]` |
| No applications in current cycle | Inbox icon | "No Applications Yet" | "Applications will appear here once enquiries are converted and submitted." | `[View Enquiries]` |
| No branches configured | Building icon | "No Branches Found" | "Branch setup is required before admission management can begin." | `[Configure Branches]` |
| No cut-offs for all branches | Shield icon | "Cut-offs Not Configured" | "Set cut-off marks for each branch and stream to enable automated screening." | `[Configure Cut-offs]` |
| Allocation queue empty | Checkmark icon | "All Allocations Complete" | "No pending branch allocations. All applications have been processed." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Admission funnel chart load | Canvas placeholder with spinner overlay |
| Seat fill chart load | Skeleton bar chart (5 bars) |
| Allocation queue table load | Skeleton table rows (5 rows) |
| Cut-off status table load | Skeleton table rows (5 rows) |
| Scholarship exam calendar load | Skeleton timeline items (3 items) |
| Criteria gaps list load | Skeleton list items (3 rows) |
| Sources pie chart load | Circular skeleton spinner in chart area |
| Audit log table load | Skeleton table rows (5 rows) |
| Drawer open (any) | Spinner overlay on drawer panel until content loads |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Admissions Director | Admission Coordinator | Scholarship Exam Mgr | Scholarship Manager | Group CEO | CAO |
|---|---|---|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Scholarship section only | Scholarship section only | Visible | Visible |
| Admission Funnel chart (5.1) | Visible | Visible | Hidden | Hidden | Visible | Visible |
| Seat Fill Rate chart (5.2) | Visible | Visible | Hidden | Hidden | Visible | Visible |
| Allocation Queue table (5.3) | Visible + actions | Read only | Hidden | Hidden | Read only | Read only |
| Cut-off Configuration (5.4) | Visible + [Configure] | Read only | Hidden | Hidden | Read only | Read only |
| Scholarship Exam Calendar (5.5) | Visible | Visible | Visible | Visible | Visible | Visible |
| Criteria Gaps list (5.6) | Visible + [Configure Now] | Read only | Hidden | Hidden | Read only | Read only |
| Top Sources chart (5.7) | Visible | Visible | Hidden | Hidden | Visible | Visible |
| Audit Log (5.8) | Visible (own actions) | Hidden | Hidden | Hidden | Read only | Read only |
| Branch Allocation Drawer | Full (read + write) | Read only | Hidden | Hidden | Hidden | Hidden |
| Seat Matrix Drawer | Full (edit tab visible) | Read only | Hidden | Hidden | Hidden | Hidden |
| Cut-off Config Drawer | Full (edit form visible) | Read only | Hidden | Hidden | Hidden | Hidden |
| `[Export Report]` button | Visible | Hidden | Hidden | Hidden | Visible | Visible |
| `[Configure Criteria]` button | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| `[Switch Cycle]` button | Visible | Visible | Hidden | Hidden | Visible | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/director/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/director/funnel/` | JWT G3+ | Admission funnel data per branch/stream |
| GET | `/api/v1/group/{group_id}/adm/director/seat-fill/` | JWT G3+ | Seat fill rates per branch and stream |
| GET | `/api/v1/group/{group_id}/adm/director/allocation-queue/` | JWT G3+ | Pending branch allocation items |
| POST | `/api/v1/group/{group_id}/adm/director/branches/{branch_id}/allocate/` | JWT G3 | Submit branch allocation |
| GET | `/api/v1/group/{group_id}/adm/director/cutoff-status/` | JWT G3+ | Cut-off config status per branch/stream |
| GET | `/api/v1/group/{group_id}/adm/director/branches/{branch_id}/cutoff/` | JWT G3+ | Fetch cut-off values for a branch |
| POST | `/api/v1/group/{group_id}/adm/director/branches/{branch_id}/cutoff/` | JWT G3 | Save / update cut-off configuration |
| GET | `/api/v1/group/{group_id}/adm/director/criteria-gaps/` | JWT G3+ | Branches/streams missing admission criteria |
| GET | `/api/v1/group/{group_id}/adm/director/sources/` | JWT G3+ | Admission source distribution |
| GET | `/api/v1/group/{group_id}/adm/director/audit-log/` | JWT G3+ | Director's recent approval actions |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exams/upcoming/` | JWT G3+ | Upcoming scholarship exams (30 days) |
| GET | `/api/v1/group/{group_id}/adm/director/branches/{branch_id}/seat-matrix/` | JWT G3+ | Seat matrix for a branch |
| POST | `/api/v1/group/{group_id}/adm/director/branches/{branch_id}/seat-matrix/` | JWT G3 | Update seat matrix |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/director/kpis/` | `#kpi-bar` | `innerHTML` |
| Funnel chart filter change | `change from:#funnel-filters` | GET `/api/v1/group/{{ group_id }}/adm/director/funnel/` | `#funnel-chart-container` | `innerHTML` |
| Seat fill chart filter change | `change from:#seat-fill-filters` | GET `/api/v1/group/{{ group_id }}/adm/director/seat-fill/` | `#seat-fill-chart` | `innerHTML` |
| Allocation queue auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/director/allocation-queue/` | `#allocation-queue` | `innerHTML` |
| Open branch allocation drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/allocation/` | `#drawer-panel` | `innerHTML` |
| Submit branch allocation | `click from:#btn-allocate` | POST `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/allocate/` | `#allocation-queue` | `innerHTML` |
| Open seat matrix drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/seat-matrix/` | `#drawer-panel` | `innerHTML` |
| Save seat matrix | `click from:#btn-save-matrix` | POST `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/seat-matrix/` | `#seat-fill-chart` | `innerHTML` |
| Open cut-off config drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/cutoff/` | `#drawer-panel` | `innerHTML` |
| Save cut-off config | `click from:#btn-save-cutoff` | POST `/api/v1/group/{{ group_id }}/adm/director/branches/{{ branch_id }}/cutoff/` | `#cutoff-status` | `innerHTML` |
| Scholarship calendar load | `load` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exams/upcoming/` | `#scholarship-calendar` | `innerHTML` |
| Sources chart filter change | `change from:#source-filters` | GET `/api/v1/group/{{ group_id }}/adm/director/sources/` | `#admission-sources` | `innerHTML` |
| Criteria gaps load | `load` | GET `/api/v1/group/{{ group_id }}/adm/director/criteria-gaps/` | `#criteria-gaps` | `innerHTML` |
| Audit log load | `load` | GET `/api/v1/group/{{ group_id }}/adm/director/audit-log/` | `#audit-log` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
