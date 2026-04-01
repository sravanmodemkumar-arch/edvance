# 04 — Group Scholarship Exam Manager Dashboard

- **URL:** `/group/adm/scholarship-exam/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Scholarship Exam Manager (Role 26, G3)

---

## 1. Purpose

The Group Scholarship Exam Manager Dashboard is the central control panel for planning, executing, and closing out all scholarship and entrance examinations conducted by the group's admissions division. This role owns the full exam lifecycle: scheduling scholarship exams across branches, managing candidate registrations, generating hall tickets, maintaining the question bank, and publishing results. Each of these lifecycle stages has a dedicated section on the dashboard, arranged in the natural chronological order of exam operations so the manager can track readiness and progress without switching contexts.

A key operational challenge this page addresses is multi-branch coordination. Scholarship exams are often offered simultaneously or in staggered schedules across multiple branches, and each branch must independently confirm readiness — exam halls, invigilation staff, and question paper receipt. The branch readiness checklist section provides a branch-by-branch compliance grid that surfaces gaps before exam day. Automated registration reminder dispatch to under-subscribed branches helps the manager close registration gaps without manual follow-up email chains.

The question bank summary provides subject-wise health metrics — total questions, monthly additions, approval rates, and difficulty distribution — enabling the manager to proactively identify subjects at risk of an insufficient question pool before paper-building begins. Together with the result publication queue, which shows evaluated-but-unpublished exam results pending manager sign-off, this dashboard ensures that no exam outcome is delayed and that every registered candidate moves through the scholarship pipeline without administrative bottlenecks.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Scholarship Exam Manager | G3 | Full read + write + publish | Primary owner of this page |
| Group Admissions Director | G3 | Read-only (all sections) | View only; no actions |
| Group Scholarship Manager | G3 | Read — Section 5.5 (Result Publication Queue) only | Needs visibility into results for scholarship award decisions |
| Chief Academic Officer (CAO) | G3+ | Read-only (all sections) | View only; no actions |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Scholarship Exam Manager
```

### 3.2 Page Header
- **Title:** `Scholarship Exam Manager Dashboard`
- **Subtitle:** `Group Admissions · Current Cycle: [Cycle Name] · [Academic Year]`
- **Role Badge:** `Group Scholarship Exam Manager`
- **Right-side controls:** `[+ Schedule Exam]` `[Question Bank]` `[Export Registrations]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Exam in < 3 days with incomplete branch readiness | "Exam '[Name]' on [Date]: [N] branch(es) have not confirmed readiness." | Critical (red) |
| Hall tickets not generated for exam in < 5 days | "Hall tickets not yet generated for '[Exam Name]' scheduled on [Date]." | Critical (red) |
| Results pending publication > 7 days post-exam | "Results for '[Exam Name]' have been pending publication for [N] days." | Warning (amber) |
| Question bank for a subject < 50 approved questions | "Question bank for [Subject] has fewer than 50 approved questions. Add more before scheduling." | Warning (amber) |
| Exam registration deadline passed with < 50% target | "Registration for '[Exam Name]' closed at [X]% of target. Review before proceeding." | Info (blue) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Upcoming Exams (30 Days) | Count of scholarship exams scheduled in next 30 days | `scholarship_exam` WHERE date ≤ today+30 AND status ≠ 'completed' | Blue (informational) | Scrolls to Section 5.1 |
| Registered Candidates | Total registrations across all upcoming exams in current cycle | `scholarship_exam_registration` WHERE exam.cycle = current | Green if ≥ registration target; amber 60–99%; red < 60% | Opens registration detail |
| Hall Tickets Issued % | (Hall tickets generated / Total registered) × 100 | `hall_ticket` WHERE issued = true | Green ≥ 90%; amber 50–89%; red < 50% | Scrolls to Section 5.3 |
| Questions Added (Month) | Questions added to question bank this month across all subjects | `question_bank` WHERE created_month = current | Green if ≥ 50; amber 20–49; red < 20 | Scrolls to Section 5.4 |
| Results Pending Publication | Exams with evaluation complete but results not yet published | `scholarship_exam` WHERE eval_complete = true AND published = false | Red if > 2; amber = 1–2; green = 0 | Scrolls to Section 5.5 |
| Branches Not Ready | Branches that have not confirmed readiness for any upcoming exam | `exam_branch_readiness` WHERE confirmed = false | Red if > 3; amber 1–3; green = 0 | Scrolls to Section 5.6 |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Exam Schedule Overview

**Display:** Horizontal timeline of all upcoming and recent scholarship exams. Each exam is a card with key details inline. Filter chips above the timeline for type and status. Completed exams shown with muted styling.

**Fields per exam card:** Date & Time | Exam Name | Type (Merit-based / Need Screening / RTE / Entrance) | Registered Candidates | Venue / Online | Status Badge (Scheduled / Registration Open / Registration Closed / In Progress / Evaluation / Results Pending / Completed) | Action

**Actions per card:** `[Manage →]` opens exam-detail-drawer.

**Filters:** Exam Type, Status, Branch, Date range

**HTMX Pattern:**
```html
<div id="exam-schedule"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exams/list/"
     hx-trigger="load, change from:#exam-filters"
     hx-target="#exam-schedule"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: calendar icon. "No scholarship exams scheduled. Use [+ Schedule Exam] to create one."

---

### 5.2 Registration Status by Branch

**Display:** Sortable table. Rows where % filled < 50% are highlighted amber; < 25% highlighted red. Deadline passed rows shown with a strikethrough on deadline date.

**Columns:** Branch | Exam Name | Registrations | Target | % Filled | Registration Deadline | Status | Action

**Actions per row:** `[Send Reminder →]` dispatches reminder to branch admission coordinator | `[View Details]` opens registration-detail drawer.

**Filters:** Exam Name, Branch, % Filled (All / Below 50% / Below 25%), Deadline (Upcoming / Passed)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="registration-status"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/registrations/by-branch/"
     hx-trigger="load, change from:#reg-filters"
     hx-target="#registration-status"
     hx-swap="innerHTML">
```

**Empty State:** "No registration data available. Exams must be scheduled and registration opened first."

---

### 5.3 Hall Ticket Generation Status

**Display:** Sortable table. Rows where hall ticket generation is incomplete for exams within 5 days are highlighted red. Completed rows show a green checkmark.

**Columns:** Exam Name | Exam Date | Registered | Hall Tickets Generated | % Done | Status | Action

**Actions per row:** `[Generate All →]` triggers batch hall ticket generation for that exam | `[Download ZIP →]` for generated tickets.

**Filters:** Exam Name, Status (All / Pending / Partial / Complete)

**HTMX Pattern:**
```html
<div id="hall-ticket-status"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/hall-tickets/"
     hx-trigger="load"
     hx-target="#hall-ticket-status"
     hx-swap="innerHTML">
```

**Empty State:** "No hall ticket data found. Hall tickets can be generated once registration closes."

---

### 5.4 Question Bank Summary

**Display:** Grid of stat cards, one per subject (Mathematics, Physics, Chemistry, Biology, Social Studies, English, etc.). Each card shows subject name, total questions, questions added this month, approved count, pending review count, and a small difficulty distribution Chart.js doughnut (Easy / Medium / Hard). Clicking a card opens question-bank-subject-detail drawer.

**Fields per card:** Subject Name | Total Questions | Added This Month | Approved | Pending Review | Difficulty Donut chart

**Filters:** Subject, Difficulty level filter across all subjects, Added By (filter to see own additions)

**HTMX Pattern:**
```html
<div id="question-bank-summary"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/question-bank/summary/"
     hx-trigger="load"
     hx-target="#question-bank-summary"
     hx-swap="innerHTML">
```

**Empty State:** "Question bank is empty. Start adding questions to build your exam paper library."

---

### 5.5 Result Publication Queue

**Display:** List of exams where evaluation is complete or near-complete but results have not been published. Each item shows evaluation progress and has a publish action.

**Fields per item:** Exam Name | Exam Date | Total Registered | Evaluated (count + %) | Pending Evaluation | Moderated? | Action

**Actions per item:** `[View Results Preview →]` opens results in review mode | `[Publish Results →]` (with confirmation modal) — available only when Evaluated = 100% and Moderated = Yes.

**Filters:** Exam Name, Moderated (Yes / No), Evaluated % range

**HTMX Pattern:**
```html
<div id="result-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/results/pending/"
     hx-trigger="load"
     hx-target="#result-queue"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: checkmark circle. "No results pending publication. All evaluated exams have been published."

---

### 5.6 Branch Readiness Checklist

**Display:** Table grid. Each row is a branch. Each column is a readiness criterion. Cell shows status icon (✓ confirmed / ✗ not confirmed / — not applicable). Rows with any red ✗ are highlighted if exam date is within 7 days.

**Columns:** Branch | Exam Halls Confirmed | Invigilation Assigned | Question Paper Received | IT Setup (if online) | Branch Coordinator Notified | Overall Status | Action

**Overall Status Badge:** All Done = green; 1–2 pending = amber; 3+ pending = red.

**Actions per row:** `[View Details →]` opens exam-detail-drawer filtered to that branch | `[Send Nudge]` dispatches reminder to branch coordinator.

**Filters:** Exam Name (dropdown — select which exam to check readiness for), Branch, Status (All / Complete / Partial / Not Started)

**HTMX Pattern:**
```html
<div id="branch-readiness"
     hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/branch-readiness/"
     hx-trigger="load, change from:#readiness-exam-selector"
     hx-target="#branch-readiness"
     hx-swap="innerHTML">
```

**Empty State:** "No readiness data yet. Select an upcoming exam from the filter to view branch readiness."

---

## 6. Drawers & Modals

### 6.1 Exam Detail Drawer
- **Width:** 640px
- **Trigger:** `[Manage →]` in Section 5.1 or `[View Details →]` in Section 5.6
- **Tabs:**
  - **Overview:** Exam name, date/time, type, venue, description, status
  - **Registrations:** Full list of registered candidates with name, branch, contact, registration date, hall ticket status; `[Export]` button
  - **Paper Builder:** Link to exam paper builder (opens in new tab) + summary of current paper — total questions, subject distribution, total marks
  - **Results:** If evaluation complete — rank list preview, topper names, marks distribution mini-chart
  - **Branch Readiness:** Same grid as Section 5.6 but scoped to this exam
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exams/{{ exam_id }}/"`

### 6.2 Registration Detail Drawer
- **Width:** 560px
- **Trigger:** `[View Details]` in Section 5.2
- **Tabs:**
  - **Registrant List:** Table — Name, Class, Branch, Contact, Registration Date, Hall Ticket Issued
  - **Send Reminder:** Compose and dispatch registration reminder to branch; choose channel (SMS / Email / Both); `[Send]`
  - **Statistics:** Registration trend chart (daily registrations over registration period)
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/{{ exam_id }}/registrations/{{ branch_id }}/"`

### 6.3 Question Bank Subject Detail Drawer
- **Width:** 640px
- **Trigger:** Click on subject stat card in Section 5.4
- **Tabs:**
  - **Questions List:** Paginated table — Question text (truncated), Difficulty, Topic, Status (Approved / Pending / Rejected), Added By, Added On; `[Review →]` action per row
  - **Add Questions:** Bulk upload form (CSV template download + upload) or manual add form
  - **Analytics:** Difficulty distribution bar chart, topic coverage heatmap, monthly additions trend line
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/scholarship-exam/question-bank/{{ subject_id }}/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Exam scheduled | "Scholarship exam '[Name]' scheduled for [Date]." | Success | 4s |
| Registration reminder sent | "Reminder sent to [Branch] branch coordinator for '[Exam Name]'." | Success | 3s |
| Hall tickets generated | "Hall tickets generated for [N] candidates for '[Exam Name]'." | Success | 4s |
| Hall ticket generation failed | "Hall ticket generation failed. Ensure all candidate profiles are complete." | Error | 6s |
| Results published | "Results for '[Exam Name]' have been published." | Success | 5s |
| Results publish failed — not moderated | "Cannot publish: results have not been moderated. Complete moderation first." | Error | 6s |
| Questions added | "[N] question(s) added to [Subject] question bank." | Success | 4s |
| Questions bulk upload failed | "Bulk upload failed: [N] rows had errors. Download error report for details." | Error | 6s |
| Branch readiness nudge sent | "Readiness reminder sent to [Branch] coordinator." | Success | 3s |
| Exam deleted | "Exam '[Name]' has been removed from the schedule." | Info | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No exams scheduled | Calendar icon | "No Exams Scheduled" | "No scholarship exams are currently planned. Schedule one to begin." | `[+ Schedule Exam]` |
| No registrations | Clipboard icon | "No Registrations Yet" | "Registrations will appear here once exam registration is opened." | `[Open Registration]` |
| No hall ticket data | Ticket icon | "Hall Tickets Not Generated" | "Hall tickets will appear here after registration closes." | — |
| Question bank empty | Book icon | "Empty Question Bank" | "Start building your question bank by adding questions subject-wise." | `[Add Questions]` |
| No results pending | Checkmark icon | "No Pending Results" | "All evaluated exams have been published." | — |
| All branches ready | Shield checkmark | "All Branches Ready" | "Every branch has confirmed readiness for the selected exam." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Exam schedule timeline load | Skeleton exam cards (3 items) |
| Registration status table load | Skeleton table rows (5 rows) |
| Hall ticket table load | Skeleton table rows (5 rows) |
| Question bank summary grid load | Skeleton stat cards (6 cards) |
| Result queue list load | Skeleton list items (3 items) |
| Branch readiness table load | Skeleton table rows (5 rows) |
| Drawer content load | Spinner overlay on drawer panel |
| Hall ticket batch generation | Full-width progress bar with percentage |
| Results publish confirmation | Spinner on `[Publish Results →]` button |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Scholarship Exam Manager | Admissions Director | Scholarship Manager | CAO |
|---|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Result Pending card only | Visible |
| Exam Schedule (5.1) | Visible + [Manage] | Read only | Hidden | Read only |
| `[+ Schedule Exam]` button | Visible | Hidden | Hidden | Hidden |
| Registration Status (5.2) | Visible + [Send Reminder] | Read only | Hidden | Read only |
| Hall Ticket Status (5.3) | Visible + [Generate All] | Read only | Hidden | Read only |
| Question Bank Summary (5.4) | Visible + [Add Questions] | Read only | Hidden | Read only |
| Result Publication Queue (5.5) | Visible + [Publish Results] | Read only | Read only | Read only |
| `[Publish Results →]` button | Visible | Hidden | Hidden | Hidden |
| Branch Readiness (5.6) | Visible + [Send Nudge] | Read only | Hidden | Read only |
| Exam Detail Drawer — Paper Builder tab | Visible | Hidden | Hidden | Hidden |
| Exam Detail Drawer — Results tab | Visible | Visible | Visible | Visible |
| Question Bank Drawer — Add Questions tab | Visible | Hidden | Hidden | Hidden |
| `[Export Registrations]` button | Visible | Visible | Hidden | Visible |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exams/list/` | JWT G3+ | All scholarship exams (filtered) |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exams/` | JWT G3 | Create / schedule a new scholarship exam |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exams/{exam_id}/` | JWT G3+ | Full exam detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/registrations/by-branch/` | JWT G3+ | Registration counts by branch and exam |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/{exam_id}/remind/{branch_id}/` | JWT G3 | Send registration reminder to branch |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/{exam_id}/registrations/{branch_id}/` | JWT G3+ | Registrant list for a branch + exam |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/hall-tickets/` | JWT G3+ | Hall ticket generation status per exam |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/{exam_id}/hall-tickets/generate/` | JWT G3 | Generate hall tickets for all registered candidates |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/summary/` | JWT G3+ | Question bank stats per subject |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/{subject_id}/` | JWT G3+ | Question list for a subject |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/question-bank/{subject_id}/` | JWT G3 | Add question(s) to subject bank |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/results/pending/` | JWT G3+ | Exams with results pending publication |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/{exam_id}/results/publish/` | JWT G3 | Publish results for an exam |
| GET | `/api/v1/group/{group_id}/adm/scholarship-exam/branch-readiness/` | JWT G3+ | Branch readiness checklist data |
| POST | `/api/v1/group/{group_id}/adm/scholarship-exam/branch-readiness/{branch_id}/nudge/` | JWT G3 | Send readiness reminder to branch |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/kpis/` | `#kpi-bar` | `innerHTML` |
| Exam schedule filter change | `change from:#exam-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exams/list/` | `#exam-schedule` | `innerHTML` |
| Open exam detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exams/{{ exam_id }}/` | `#drawer-panel` | `innerHTML` |
| Registration table filter change | `change from:#reg-filters` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/registrations/by-branch/` | `#registration-status` | `innerHTML` |
| Send registration reminder | `click from:#btn-remind-branch` | POST `/api/v1/group/{{ group_id }}/adm/scholarship-exam/{{ exam_id }}/remind/{{ branch_id }}/` | `#remind-status-{{ branch_id }}` | `innerHTML` |
| Open registration detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/{{ exam_id }}/registrations/{{ branch_id }}/` | `#drawer-panel` | `innerHTML` |
| Generate hall tickets | `click from:#btn-generate-tickets` | POST `/api/v1/group/{{ group_id }}/adm/scholarship-exam/{{ exam_id }}/hall-tickets/generate/` | `#hall-ticket-status` | `innerHTML` |
| Open question bank subject drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/question-bank/{{ subject_id }}/` | `#drawer-panel` | `innerHTML` |
| Add question (manual) | `click from:#btn-add-question` | POST `/api/v1/group/{{ group_id }}/adm/scholarship-exam/question-bank/{{ subject_id }}/` | `#question-bank-summary` | `innerHTML` |
| Publish results | `click from:#btn-publish-results` | POST `/api/v1/group/{{ group_id }}/adm/scholarship-exam/{{ exam_id }}/results/publish/` | `#result-queue` | `innerHTML` |
| Branch readiness exam selector change | `change from:#readiness-exam-selector` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/branch-readiness/` | `#branch-readiness` | `innerHTML` |
| Send readiness nudge | `click from:#btn-readiness-nudge` | POST `/api/v1/group/{{ group_id }}/adm/scholarship-exam/branch-readiness/{{ branch_id }}/nudge/` | `#readiness-row-{{ branch_id }}` | `innerHTML` |
| Result queue load | `load` | GET `/api/v1/group/{{ group_id }}/adm/scholarship-exam/results/pending/` | `#result-queue` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
