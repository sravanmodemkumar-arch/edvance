# 22 — Staff Onboarding Tracker

- **URL:** `/group/hr/onboarding/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Staff Onboarding Tracker is one of the highest-priority pages in Division E because it governs compliance at the most critical transition point in a staff member's journey: the gap between "Offer Accepted" and "Fully Active." New joiners who reach student-facing roles without completing mandatory requirements represent direct institutional risk. This page exists to close that gap with a structured, auditable checklist for every new hire.

The onboarding checklist is comprehensive and non-negotiable. Every new staff member must complete: document submission (Aadhaar card, PAN card, degree/diploma certificate, experience letter, address proof), contract signing, ID card issuance, system account creation (portal access, email, attendance biometric), BGV initiation, POCSO training completion (mandatory before any student contact), bank account details submission for salary processing, ESI and PF registration, induction training attendance, and branch orientation completion. Mandatory steps cannot be skipped or waived by branch HR — only the Group HR Director can authorise a temporary exception with a documented reason and deadline.

The compliance risk around POCSO training is treated with maximum severity on this page. If a staff member has been assigned to any student-contact role (teacher, warden, lab assistant, counsellor, librarian, etc.) and their POCSO training is not yet marked as Complete, the system displays a persistent red banner on the onboarding tracker and on the individual's staff profile (page 14). This mirrors the legal requirement under the POCSO Act 2012 that all staff working in proximity to minors must be trained and aware of the provisions. Failure to enforce this could expose the institution to regulatory action.

When an offer is accepted via the Offer Letter Manager (page 21), the system automatically creates an onboarding record for the new joiner with all checklist items in a "Pending" state. The HR Manager is notified. Each checklist item has a system-suggested due date (typically 7 days from join date for documents; 1 day for system account; 30 days for BGV; before join date for POCSO). Tasks overdue beyond 7 days are flagged in the "Overdue Tasks Count" column, and the HR Manager receives a daily digest notification for any new joiners with overdue items.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access + exception approval | Can waive/extend checklist deadlines |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of onboarding |
| Group Recruiter — Teaching (43) | G0 | No access | — |
| Group Recruiter — Non-Teaching (44) | G0 | No access | — |
| Group Training & Dev Manager (45) | G2 | Read — POCSO and training items only | Can update POCSO training status |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | Read — BGV checklist item only | Can mark BGV Initiated from onboarding |
| Group BGV Executive (49) | G3 | Read — BGV checklist item only | Same scope as BGV Manager |
| Group POCSO Coordinator (50) | G3 | Read/Write — POCSO item only | Can mark POCSO training complete |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | Read — ESI/PF, insurance items | Can update welfare-related items |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Onboarding → Staff Onboarding Tracker`

### 3.2 Page Header
- Title: "Staff Onboarding Tracker"
- Subtitle: "Track onboarding completion for all new joiners."
- Primary CTA: "+ Add Joiner Manually" (HR Director / Manager)
- Secondary CTAs: "Export Onboarding Report" | "Send Reminder to Overdue Joiners"

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Any student-contact staff without POCSO training complete | "[N] new joiner(s) in student-contact roles have not completed POCSO training. Immediate action required." | Red / Critical |
| Any new joiner with BGV not yet initiated > 30 days post-join | "[N] joiner(s) have no BGV initiated. Compliance deadline breached." | Red |
| Overdue tasks (any task > 7 days past due date) > 0 | "[N] onboarding task(s) are overdue across [M] staff members." | Orange |
| Joiners with 0% completion after 7 days | "[N] joiner(s) have not started onboarding tasks." | Yellow |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Joiners This Month | Count of new onboarding records created this month | Neutral blue | — |
| Onboarding 100% Complete | Count with all checklist items = Completed | Green | Filters to complete |
| Onboarding In Progress | Count with ≥ 1 item pending, none overdue | Amber | Filters to in-progress |
| Overdue Tasks | Count of staff with ≥ 1 overdue task | Red if > 0 | Filters to overdue |
| BGV Not Yet Initiated | Count with BGV checklist item still Pending | Red if > 0 | Filters to BGV pending |
| POCSO Not Completed | Count in student-contact role without POCSO done | Red if > 0 | Filters to POCSO pending |

---

## 5. Main Table — New Joiners Onboarding

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Staff Name | Text (link to onboarding detail drawer) | Yes | Yes (search) |
| Branch | Text | Yes | Yes (dropdown) |
| Join Date | Date | Yes | Yes (date range) |
| Role | Text | Yes | Yes (search) |
| Completion % | Progress bar + percentage | Yes | Yes (< 100% filter) |
| BGV Status | Chip (Not Initiated / In Progress / Cleared) | No | Yes |
| POCSO Status | Chip (Completed / Pending) | No | Yes |
| Overdue Tasks | Integer (count of tasks past due) | Yes | Yes (> 0 filter) |
| Days Since Joining | Integer (computed) | Yes | No |
| Actions | View Checklist / Send Reminder / Mark Complete All | No | No |

### 5.1 Filters
- Completion: All | 100% Complete | In Progress | Not Started
- POCSO Status: All | Completed | Pending
- BGV Status: All | Not Initiated | In Progress | Cleared
- Overdue Tasks: All | Has Overdue Tasks
- Branch: All branches (dropdown)
- Join Date Range: This Month | Last 30 Days | Custom

### 5.2 Search
Search by staff name or employee ID. Minimum 2 characters, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. Standard navigation controls with total joiner count shown.

---

## 6. Drawers

### 6.1 Drawer: Onboarding Checklist (View / Update)
Full checklist displayed as a structured list with categories: Documents | Contract & ID | System Setup | BGV | Training | Payroll & Benefits.
Each checklist item shows: Item Name, Status (Pending / In Progress / Completed / Waived), Due Date, Completed Date, Completed By (username), Notes.
HR Manager can mark any item Completed, In Progress, or Waived (waiver requires reason + HR Director confirmation).
POCSO item: conditionally highlighted in red if role is student-contact and status ≠ Completed.
BGV item: "Initiate BGV" link that opens BGV module for the staff member.
Progress ring at top of drawer (e.g., "7 / 10 tasks complete").

### 6.2 Drawer: Add Joiner Manually
Used for joiners not processed through the offer pipeline. Fields: Staff Name (typeahead — must exist as a staff record), Join Date, Branch, Role, Employee Category (Permanent / Contract / Visiting), Notes. On Save: creates onboarding record with all checklist items in Pending state.

### 6.3 Drawer: Waiver Request (HR Director only)
Triggered when HR Manager tries to waive a mandatory checklist item. Fields: Item Being Waived, Reason (textarea), Temporary Deadline Extension (date picker), Acknowledging Risk (checkbox, required). On Save: item marked Waived with audit log; HR Director notified.

### 6.4 Modal: Send Reminder
Triggered by "Send Reminder" action. Preview of reminder message. Confirm / Cancel. On Confirm: system notification sent to staff member's registered email + in-portal notification. Logged with timestamp.

---

## 7. Charts

No charts on this page. The checklist progress bars per staff member and the KPI completion cards provide sufficient visual status indication without charts. Excessive charting on a compliance-focused operational page adds noise without actionable insight.

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Checklist item marked complete | "[Item Name] marked complete for [Staff Name]." | Success | 4s |
| Joiner added manually | "Onboarding record created for [Staff Name]." | Success | 4s |
| Reminder sent | "Reminder sent to [Staff Name]." | Info | 4s |
| POCSO item completed | "POCSO training marked complete. Student-contact restriction lifted." | Success | 5s |
| Waiver approved | "[Item] waived for [Staff Name]. Audit log updated." | Warning | 5s |
| BGV initiated from checklist | "BGV initiated for [Staff Name]. BGV Manager notified." | Success | 4s |
| Bulk reminder sent | "Reminders sent to [N] staff members with overdue tasks." | Info | 5s |
| Onboarding 100% complete | "Onboarding for [Staff Name] is now 100% complete." | Success | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No new joiners this month | "No New Joiners" | "New joiners from accepted offers will appear here automatically." | Add Joiner Manually |
| Filter — no results | "No Matching Records" | "Adjust your filters to find the joiner you're looking for." | Clear Filters |
| All onboarding complete | "All Onboarding Up to Date" | "All new joiners have completed their onboarding checklists." | — |
| POCSO filter — none pending | "No POCSO Issues" | "All staff in student-contact roles have completed POCSO training." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI card skeletons (6) + table row skeletons (15) |
| Filter / search change | Table body row skeletons |
| Checklist drawer open | Drawer skeleton (checklist item skeletons, 10 rows) |
| Checklist item update | Spinner on the item row, disabled until response |
| Bulk reminder send | Button spinner + disabled state |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) / Manager (42) | POCSO Coord (50) | BGV Roles (48, 49) | Welfare Officer (52) |
|---|---|---|---|---|
| Add Joiner Manually | Visible + enabled | Hidden | Hidden | Hidden |
| Full checklist edit | Visible + enabled | POCSO item only | BGV item only | ESI/PF items only |
| Waiver Request | Visible (Director only approves) | Hidden | Hidden | Hidden |
| Send Reminder | Visible + enabled | Hidden | Hidden | Hidden |
| Export Onboarding Report | Visible | Hidden | Hidden | Hidden |
| All table columns | Visible | POCSO column visible | BGV column visible | ESI/PF notes only |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/onboarding/` | JWT | List all onboarding records (paginated) |
| POST | `/api/v1/hr/onboarding/` | JWT | Create onboarding record manually |
| GET | `/api/v1/hr/onboarding/{id}/` | JWT | Fetch onboarding detail + checklist |
| PATCH | `/api/v1/hr/onboarding/{id}/checklist/{item_id}/` | JWT | Update checklist item status |
| POST | `/api/v1/hr/onboarding/{id}/reminder/` | JWT | Send reminder to staff member |
| POST | `/api/v1/hr/onboarding/{id}/waiver/` | JWT | Submit waiver request for an item |
| GET | `/api/v1/hr/onboarding/kpis/` | JWT | KPI summary |
| POST | `/api/v1/hr/onboarding/bulk-reminder/` | JWT | Send bulk reminders to overdue joiners |
| GET | `/api/v1/hr/onboarding/export/` | JWT | Export onboarding report |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/onboarding/?q={val}` | `#onboarding-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/onboarding/?completion={}&pocso={}&bgv={}&branch={}` | `#onboarding-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/onboarding/?page={n}` | `#onboarding-table-body` | innerHTML |
| Checklist drawer open | click | GET `/group/hr/onboarding/{id}/checklist/drawer/` | `#drawer-container` | innerHTML |
| Checklist item status update | change | PATCH `/api/v1/hr/onboarding/{id}/checklist/{item_id}/` | `#checklist-item-{item_id}` | outerHTML |
| Add Joiner drawer open | click | GET `/group/hr/onboarding/add/drawer/` | `#drawer-container` | innerHTML |
| Add Joiner submit | submit | POST `/api/v1/hr/onboarding/` | `#onboarding-table-body` | afterbegin |
| Send reminder modal | click | GET `/group/hr/onboarding/{id}/reminder/modal/` | `#modal-container` | innerHTML |
| Bulk reminder | click | POST `/api/v1/hr/onboarding/bulk-reminder/` | `#alert-banner` | outerHTML |
| KPI refresh after item update | after:PATCH | GET `/api/v1/hr/onboarding/kpis/` | `#kpi-bar` | outerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
