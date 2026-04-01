# 02 — Group Admission Coordinator Dashboard

- **URL:** `/group/adm/coordinator/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Admission Coordinator (Role 24, G3)

---

## 1. Purpose

The Group Admission Coordinator Dashboard is the operational hub for managing the centralised application pipeline across all branches of the group. The coordinator is responsible for moving each applicant through the admission funnel — from initial application receipt through document verification, counselling scheduling, branch allocation, offer issuance, and final enrollment — and this page surfaces every actionable item in a single, triage-focused interface. The Kanban-style pipeline summary provides an instant count of applications at each stage, while the "Applications Requiring Action" table ensures no application sits idle for an unacceptable period.

A key responsibility of the coordinator is maintaining accurate branch capacity visibility. As applications arrive and enrollments are confirmed, the branch capacity table updates in near real-time so the coordinator can make informed allocation decisions and flag any branch approaching overflow to the Admissions Director. Document verification is tracked in a dedicated queue that allows quick identification of incomplete submissions and one-click reminder dispatch to applicants or their parents.

The dashboard also supports mid-year governance through the pending branch transfers table, which tracks inter-branch transfer requests and their approval status. The coordinator's workflow is designed around speed and completeness: every actionable item has a direct action button, every delayed item is highlighted, and HTMX-driven polling keeps the view current without requiring full page reloads. Large groups with multiple branches benefit especially from this aggregated, cross-branch view that would otherwise require navigating each branch individually.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admission Coordinator | G3 | Full read + write + allocate + remind | Primary owner of this page |
| Group Admissions Director | G3 | Read-only + override actions available | Can override allocation decisions |
| Group Admission Counsellor | G3 | Read — Section 5.1 (pipeline summary) + Section 5.5 (today's tasks for own sessions) | Cannot access allocation or document queue |
| Group CEO | G3+ | Read-only (all sections) | View only; no actions |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Coordinator Dashboard
```

### 3.2 Page Header
- **Title:** `Admission Coordinator Dashboard`
- **Subtitle:** `Group Admissions · Current Cycle: [Cycle Name] · [Academic Year]`
- **Role Badge:** `Group Admission Coordinator`
- **Right-side controls:** `[+ New Application]` `[Bulk Action ▾]` `[Export Pipeline]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Applications pending > 48 hours | "[N] application(s) have been waiting for action for over 48 hours." | Critical (red) |
| Document verification queue > 20 | "Document queue has [N] pending items. Applicants may face delays." | Warning (amber) |
| Branch at ≥ 95% capacity | "Branch [Name] is at [X]% capacity. Coordinate with Director for seat review." | Warning (amber) |
| No counselling sessions scheduled today | "No counselling sessions are scheduled for today." | Info (blue) |
| Pending transfers > 10 | "[N] inter-branch transfer requests are awaiting approval." | Warning (amber) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Applications in Pipeline Today | Applications received or updated today | `admissions_application` WHERE updated_date = today | Blue (informational) | Opens Section 5.2 filtered to today |
| Applications Requiring Action | Applications with status = 'pending_action' or incomplete for > 24h | `admissions_application` + status flags | Red if > 20; amber 5–20; green 0–4 | Scrolls to Section 5.2 |
| Branch Allocation Pending | Applications accepted but not yet branch-allocated | `application_allocation` WHERE status = 'unallocated' | Red if > 10; amber 1–10; green = 0 | Opens allocation modal |
| Documents Pending Verification | Applicants with at least one unverified document | `application_document` WHERE status = 'pending' | Red if > 15; amber 5–15; green < 5 | Scrolls to Section 5.4 |
| Today's Counselling Sessions | Counselling sessions scheduled for today (all counsellors) | `counselling_session` WHERE date = today | Blue (informational) | Scrolls to Section 5.5 |
| Branches at > 90% Capacity | Count of branches with seat fill ≥ 90% | `seat_matrix` + `enrollment` | Red if > 3; amber 1–3; green = 0 | Opens branch capacity table |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Application Pipeline Status

**Display:** Kanban-style stage summary cards in a horizontal row. Each card shows stage name, count of applications at that stage, and a subtle colour badge. Clicking any card filters Section 5.2 to that stage. Cards auto-poll every 5 minutes.

**Stages (left to right):** New → Document Check → Counselling → Offered → Enrolled → Rejected

**Fields per card:** Stage name | Count | Delta from yesterday (↑/↓) | Colour badge (New=blue, Document Check=amber, Counselling=purple, Offered=teal, Enrolled=green, Rejected=red)

**HTMX Pattern:**
```html
<div id="pipeline-kanban"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/pipeline-summary/"
     hx-trigger="load, every 5m"
     hx-target="#pipeline-kanban"
     hx-swap="innerHTML">
```

**Empty State:** "No applications found in the current cycle. Applications will appear here once submitted."

---

### 5.2 Applications Requiring Action

**Display:** Sortable, selectable table with a search bar. Rows with `days_pending` > 48 highlighted amber; > 72 hours highlighted red. Supports bulk actions (Bulk Assign to Branch, Bulk Send Reminder) via checkbox selection.

**Columns:** ☐ | Student Name | Applied Stream | Applied Branch | Stage | Days Pending | Assigned Counsellor | Action

**Actions per row:** `[Take Action →]` opens application-detail drawer.

**Filters:** Branch, Stream, Stage, Days Pending (Any / 1+ / 2+ / 3+), Assigned Counsellor, Search (student name)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="action-required-table"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/applications/action-required/"
     hx-trigger="load, change from:#action-filters"
     hx-target="#action-required-table"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: inbox with checkmark. "No applications currently require action. Pipeline is up to date."

---

### 5.3 Branch Capacity Overview

**Display:** Sortable table. Each row is a branch × stream combination. Status badge colour-coded by fill percentage. Clicking a branch row opens the allocation modal for that branch.

**Columns:** Branch Name | Stream | Total Seats | Enrolled | Available | % Filled | Status Badge | Action

**Status Badge Rules:** ≥ 95% = red "Critical"; 80–94% = amber "High"; 50–79% = green "Normal"; < 50% = blue "Low"

**Filters:** Branch, Stream, Status (All / Critical / High / Normal / Low), Sort by % Filled (desc default)

**HTMX Pattern:**
```html
<div id="capacity-table"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/branch-capacity/"
     hx-trigger="load, every 5m"
     hx-target="#capacity-table"
     hx-swap="innerHTML">
```

**Empty State:** "Seat matrix data not available. Contact the Admissions Director to configure the seat matrix."

---

### 5.4 Document Verification Queue

**Display:** List-style view. Each item is an applicant with incomplete document submissions. Missing documents shown as comma-separated tag list. Supports one-click reminder dispatch.

**Fields per item:** Applicant Name | Applied Branch | Applied Stream | Missing Documents (tags) | Days Waiting | Phone | Action

**Actions per item:** `[Send Reminder →]` (SMS/WhatsApp trigger) | `[View Application →]` (opens application-detail drawer)

**Filters:** Branch, Stream, Missing Doc Type, Days Waiting (> 1 / > 3 / > 7)

**HTMX Pattern:**
```html
<div id="doc-verification-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/documents/pending/"
     hx-trigger="load"
     hx-target="#doc-verification-queue"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: document with checkmark. "All documents are verified. No pending verification items."

---

### 5.5 Today's Allocation Tasks

**Display:** Chronological task list for today. Each item is a scheduled allocation or counselling task. Completed tasks are struck through. Shows progress: X of Y tasks completed today.

**Fields per item:** Time | Task Type (Allocation / Counselling / Document Review) | Student Name | Branch | Notes | Status (Pending / In Progress / Done) | Action

**Actions per item:** `[Start →]` | `[Mark Done ✓]`

**Filters:** Task Type, Status

**HTMX Pattern:**
```html
<div id="todays-tasks"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/tasks/today/"
     hx-trigger="load"
     hx-target="#todays-tasks"
     hx-swap="innerHTML">
```

**Empty State:** "No allocation tasks scheduled for today. Tasks will appear as applications progress through the pipeline."

---

### 5.6 Pending Branch Transfers

**Display:** Sortable table. Inter-branch transfer requests submitted by branch staff or parents, awaiting coordinator and/or director approval.

**Columns:** Student Name | From Branch | To Branch | Stream | Reason | Requested By | Requested On | Days Pending | Status | Action

**Status Values:** Pending Coordinator | Pending Director | Approved | Rejected

**Actions per row:** `[Review →]` opens allocation-modal pre-filled with transfer context.

**Filters:** From Branch, To Branch, Status, Days Pending

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="transfer-table"
     hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/transfers/pending/"
     hx-trigger="load"
     hx-target="#transfer-table"
     hx-swap="innerHTML">
```

**Empty State:** "No pending inter-branch transfer requests at this time."

---

## 6. Drawers & Modals

### 6.1 Application Detail Drawer
- **Width:** 640px
- **Trigger:** `[Take Action →]` in Section 5.2 or any application link
- **Tabs:**
  - **Profile:** Student + parent details, contact info, class applied for
  - **Documents:** Document checklist — each document with status (Submitted / Verified / Missing / Rejected), `[Verify]` / `[Request Re-upload]` actions
  - **Timeline:** Application stage history with timestamps and action taken by whom
  - **Notes:** Free-text coordinator notes field with `[Save Note]`
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/"`

### 6.2 Allocation Modal
- **Width:** 560px
- **Trigger:** `[Allocate Now]` KPI drill-down or `[Review →]` in Section 5.6
- **Tabs:**
  - **Allocate:** Branch selector (showing available capacity), Stream selector, `[Confirm Allocation]`
  - **Capacity Check:** Real-time seat availability for selected branch+stream combination
  - **Director Override:** Visible only to Director role — force-allocate even if branch is at capacity
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/allocation-modal/{{ application_id }}/"` (GET); `hx-post` on confirm

### 6.3 Document Checklist Drawer
- **Width:** 480px
- **Trigger:** `[View Application →]` in Section 5.4
- **Tabs:**
  - **Checklist:** Required vs submitted documents per admission type (General / RTE / Scholarship)
  - **Upload Log:** History of each document upload with timestamp and uploader
  - **Send Reminder:** Compose and dispatch reminder via SMS / WhatsApp; template selector
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/documents/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Application stage advanced | "Application for [Student Name] moved to [Stage]." | Success | 4s |
| Branch allocation confirmed | "[Student Name] allocated to [Branch] — [Stream]." | Success | 4s |
| Document verified | "Document '[Doc Name]' verified for [Student Name]." | Success | 3s |
| Reminder sent | "Reminder sent to [Student Name] (+91XXXXXXXXXX)." | Success | 3s |
| Transfer request approved | "Transfer approved: [Student Name] → [Branch]." | Success | 4s |
| Transfer request rejected | "Transfer request for [Student Name] has been rejected." | Info | 4s |
| Allocation failed — branch full | "Cannot allocate: [Branch] — [Stream] has no available seats." | Error | 6s |
| Bulk action applied | "[N] applications updated successfully." | Success | 4s |
| Document re-upload requested | "Re-upload request sent to [Student Name]." | Info | 4s |
| Note saved | "Coordinator note saved." | Success | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No applications in cycle | Inbox icon | "No Applications Yet" | "The pipeline is empty. Applications will appear here once received." | `[View Enquiries]` |
| No action-required applications | Checkmark in circle | "All Clear" | "No applications currently require your action." | — |
| Document queue empty | Document checkmark | "Documents Up to Date" | "All submitted documents have been verified." | — |
| No branch transfers pending | Arrows icon | "No Pending Transfers" | "There are no inter-branch transfer requests awaiting review." | — |
| No tasks for today | Calendar checkmark | "No Tasks Today" | "You have no allocation or counselling tasks scheduled for today." | `[View Full Pipeline]` |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Pipeline kanban load | Skeleton stage cards (6 cards in a row) |
| Applications table load | Skeleton table rows (8 rows) |
| Branch capacity table load | Skeleton table rows (5 rows) |
| Document queue load | Skeleton list items (5 items) |
| Today's tasks list load | Skeleton list items (4 items) |
| Transfer table load | Skeleton table rows (5 rows) |
| Drawer content load | Spinner overlay on drawer panel |
| Allocation modal load | Spinner in modal body |
| Reminder dispatch | Inline spinner on `[Send Reminder]` button |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Admission Coordinator | Admissions Director | Admission Counsellor | Group CEO |
|---|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Pipeline + Today's Sessions only | Visible |
| Pipeline Kanban (5.1) | Visible | Visible | Visible | Visible |
| Applications Requiring Action (5.2) | Visible + actions | Read only + override | Hidden | Read only |
| Branch Capacity Table (5.3) | Visible | Visible | Hidden | Visible |
| Document Verification Queue (5.4) | Visible + [Verify] + [Remind] | Read only | Hidden | Hidden |
| Today's Allocation Tasks (5.5) | Visible + [Start] + [Done] | Read only | Own tasks only | Hidden |
| Pending Transfers Table (5.6) | Visible + [Review] | Read only + override | Hidden | Read only |
| `[+ New Application]` button | Visible | Hidden | Hidden | Hidden |
| `[Bulk Action]` button | Visible | Hidden | Hidden | Hidden |
| `[Export Pipeline]` button | Visible | Visible | Hidden | Visible |
| Application Detail Drawer — Documents tab | Visible + Verify actions | Read only | Hidden | Hidden |
| Allocation Modal — Director Override tab | Hidden | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/coordinator/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/coordinator/pipeline-summary/` | JWT G3+ | Application counts per pipeline stage |
| GET | `/api/v1/group/{group_id}/adm/coordinator/applications/action-required/` | JWT G3+ | Applications requiring action (filtered) |
| GET | `/api/v1/group/{group_id}/adm/coordinator/applications/{application_id}/` | JWT G3+ | Full application detail for drawer |
| POST | `/api/v1/group/{group_id}/adm/coordinator/applications/{application_id}/advance/` | JWT G3 | Advance application to next stage |
| GET | `/api/v1/group/{group_id}/adm/coordinator/branch-capacity/` | JWT G3+ | Branch × stream seat capacity |
| GET | `/api/v1/group/{group_id}/adm/coordinator/documents/pending/` | JWT G3 | Applications with pending documents |
| POST | `/api/v1/group/{group_id}/adm/coordinator/applications/{application_id}/documents/{doc_id}/verify/` | JWT G3 | Mark document as verified |
| POST | `/api/v1/group/{group_id}/adm/coordinator/applications/{application_id}/remind/` | JWT G3 | Send document reminder to applicant |
| GET | `/api/v1/group/{group_id}/adm/coordinator/tasks/today/` | JWT G3+ | Today's allocation and counselling tasks |
| POST | `/api/v1/group/{group_id}/adm/coordinator/tasks/{task_id}/complete/` | JWT G3 | Mark task as completed |
| GET | `/api/v1/group/{group_id}/adm/coordinator/transfers/pending/` | JWT G3+ | Pending inter-branch transfer requests |
| POST | `/api/v1/group/{group_id}/adm/coordinator/transfers/{transfer_id}/approve/` | JWT G3 | Approve a branch transfer |
| POST | `/api/v1/group/{group_id}/adm/coordinator/transfers/{transfer_id}/reject/` | JWT G3 | Reject a branch transfer |
| GET | `/api/v1/group/{group_id}/adm/coordinator/allocation-modal/{application_id}/` | JWT G3+ | Pre-fill data for allocation modal |
| POST | `/api/v1/group/{group_id}/adm/coordinator/applications/{application_id}/allocate/` | JWT G3 | Confirm branch allocation |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/kpis/` | `#kpi-bar` | `innerHTML` |
| Pipeline kanban auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/pipeline-summary/` | `#pipeline-kanban` | `innerHTML` |
| Application table filter change | `change from:#action-filters` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/applications/action-required/` | `#action-required-table` | `innerHTML` |
| Pipeline stage card click (filter table) | `click` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/applications/action-required/?stage={{ stage }}` | `#action-required-table` | `innerHTML` |
| Open application detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/` | `#drawer-panel` | `innerHTML` |
| Verify document | `click from:#btn-verify-doc` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/documents/{{ doc_id }}/verify/` | `#doc-verification-queue` | `innerHTML` |
| Send document reminder | `click from:#btn-remind` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/remind/` | `#remind-status-{{ application_id }}` | `innerHTML` |
| Branch capacity table auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/branch-capacity/` | `#capacity-table` | `innerHTML` |
| Open allocation modal | `click` | GET `/api/v1/group/{{ group_id }}/adm/coordinator/allocation-modal/{{ application_id }}/` | `#drawer-panel` | `innerHTML` |
| Confirm allocation | `click from:#btn-confirm-alloc` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/applications/{{ application_id }}/allocate/` | `#action-required-table` | `innerHTML` |
| Mark task complete | `click from:#btn-task-done` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/tasks/{{ task_id }}/complete/` | `#todays-tasks` | `innerHTML` |
| Transfer approve | `click from:#btn-transfer-approve` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/transfers/{{ transfer_id }}/approve/` | `#transfer-table` | `innerHTML` |
| Transfer reject | `click from:#btn-transfer-reject` | POST `/api/v1/group/{{ group_id }}/adm/coordinator/transfers/{{ transfer_id }}/reject/` | `#transfer-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
