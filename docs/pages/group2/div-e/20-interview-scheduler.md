# 20 — Interview Scheduler

- **URL:** `/group/hr/recruitment/interviews/`
- **Template:** `portal_base.html`
- **Priority:** P1
- **Role:** Group HR Manager (Role 42, G3)

---

## 1. Purpose

The Interview Scheduler centralises the scheduling and tracking of all interviews across both teaching and non-teaching recruitment pipelines. Without a dedicated scheduling tool, interview coordination becomes a fragmented exercise in email chains, missed confirmations, and last-minute cancellations — each of which damages candidate experience and increases time-to-hire. This page eliminates that fragmentation by giving the Group HR Manager a unified view of all upcoming, in-progress, and completed interviews across every branch and role.

For teaching candidates, the Interview Scheduler must coordinate Demo Class slots with the target branch principal. A demo class requires a real classroom, a specific grade and subject, and availability of the observing panel (typically the Subject HOD and the Principal). These constraints mean that simply picking a date is insufficient — the branch must confirm the slot before the candidate is notified. This page manages that confirmation workflow: the HR Manager proposes a slot, the branch principal confirms or proposes an alternative, and once confirmed, the candidate is notified automatically. The system tracks the confirmation status of each demo class separately from the interview itself.

For non-teaching candidates, the page schedules panel interviews, telephonic screenings, and practical skills tests (driving test, cooking test). These interviews are simpler logistically but still benefit from centralised tracking, particularly for multi-branch groups where the same day could have 15 interviews happening across 8 branches, all needing to be documented and outcome-recorded.

Key operational metrics include the no-show rate (candidates who do not attend scheduled interviews) and the reschedule request rate (either side requesting a change). High no-show rates may indicate poor candidate communication or scheduling at inconvenient times. The page also tracks interviews pending slot confirmation, which is a direct measure of coordination friction between Group HR and branch principals.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group HR Director (41) | G3 | Full access | Can schedule, edit, cancel any interview |
| Group HR Manager (42) | G3 | Full CRUD | Primary owner of scheduling |
| Group Recruiter — Teaching (43) | G0 | Read — their candidates' interviews only | Cannot schedule or cancel |
| Group Recruiter — Non-Teaching (44) | G0 | Read — their candidates' interviews only | Cannot schedule or cancel |
| Group Training & Dev Manager (45) | G2 | No access | — |
| Group Performance Review Officer (46) | G1 | No access | — |
| Group Staff Transfer Coordinator (47) | G3 | No access | — |
| Group BGV Manager (48) | G3 | No access | — |
| Group BGV Executive (49) | G3 | No access | — |
| Group POCSO Coordinator (50) | G3 | No access | — |
| Group Disciplinary Committee Head (51) | G3 | No access | — |
| Group Employee Welfare Officer (52) | G3 | No access | — |

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group HR → Recruitment → Interview Scheduler`

### 3.2 Page Header
- Title: "Interview Scheduler"
- Subtitle: "Schedule and track interviews for teaching and non-teaching candidates."
- View toggle: "Table View" | "Calendar View" (weekly calendar grouped by branch)
- Primary CTA: "+ Schedule Interview"
- Secondary CTAs: "Export Interview List" | "Today's Interviews" (quick filter)

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Interviews today with unconfirmed slot | "[N] interview(s) scheduled today are still awaiting confirmation." | Red |
| Demo classes awaiting principal confirmation > 48 hours | "[N] demo class slot requests have not been confirmed in over 48 hours." | Orange |
| Reschedule requests pending HR action > 24 hours | "[N] reschedule request(s) need your attention." | Orange |
| No-shows this week > 3 | "High no-show rate this week ([N] no-shows). Review candidate communication process." | Yellow |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Interviews Scheduled This Week | Count with interview date in current week | Neutral blue | Filters to current week |
| Completed Today | Count with status = Completed and date = today | Green | — |
| No-Shows This Month | Count with status = No-Show in current month | Red if > 5 | Filters to no-shows |
| Reschedule Requests | Count with status = Reschedule Requested | Amber if > 0 | Filters to reschedule queue |
| Demo Classes Confirmed | Count of demo interviews with slot confirmed | Green | Filters to demo type |
| Pending Slot Confirmation | Count awaiting branch/candidate confirmation | Orange if > 0 | Filters to pending |

---

## 5. Main Table — Interviews

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Candidate Name | Text (link to candidate drawer) | Yes | Yes (search) |
| Applied Role | Text | Yes | Yes (dropdown) |
| Branch | Text | Yes | Yes (dropdown) |
| Interview Type | Chip (Demo / Panel / Telephonic / Skills Test) | Yes | Yes |
| Scheduled Date | Date + Time | Yes | Yes (date range) |
| Interviewer / Panel | Text (names list) | No | Yes (interviewer search) |
| Status | Chip (Scheduled / Confirmed / Completed / No-Show / Cancelled / Rescheduled) | Yes | Yes |
| Slot Confirmed By | Text (branch principal name or "Pending") | No | No |
| Actions | View / Edit / Mark Complete / No-Show / Reschedule / Cancel | No | No |

### 5.1 Filters
- Interview Type: All | Demo Class | Panel Interview | Telephonic | Skills Test
- Status: All | Scheduled | Confirmed | Completed | No-Show | Reschedule Requested | Cancelled
- Branch: All branches (dropdown)
- Date Range: Today | This Week | Next 7 Days | Custom range
- Pending Confirmation: Toggle (shows only interviews with status = pending confirmation)

### 5.2 Search
Search by candidate name. 2-character minimum, 400ms debounce.

### 5.3 Pagination
Server-side pagination, 20 records per page. First / Prev / Page N / Next / Last navigation. Record count above table.

---

## 6. Drawers

### 6.1 Drawer: Schedule Interview
Fields: Candidate (typeahead search — filters to candidates in pipeline at Interview Scheduled stage), Interview Type (Demo / Panel / Telephonic / Skills Test), Branch (auto-populated from candidate), Date (date picker), Time (time picker), Duration (dropdown: 30 min / 45 min / 60 min / 90 min / Custom), Interviewer / Panel Members (multi-select from staff list at branch), Location / Online Link (text), Demo-Specific Fields (visible only if Demo type): Class Grade (dropdown), Subject, Observing HOD, Send Branch Principal Confirmation Request (checkbox — triggers notification to branch principal). Candidate Notification (checkbox — sends interview invite to candidate email). Internal Notes.
Validation: Date must be future; at least one interviewer required; demo class must have grade + subject.
On Save: interview record created, status = Scheduled (or Pending Confirmation if demo + checkbox checked).

### 6.2 Drawer: View / Edit Interview
Pre-populated form. Edit allowed for Scheduled or Reschedule Requested status. If editing date/time, candidate and panel notified of change. Status change actions at drawer footer: Mark Confirmed / Mark Completed (prompts outcome entry) / Mark No-Show / Request Reschedule / Cancel.

### 6.3 Drawer: Record Outcome
Triggered by "Mark Complete". Fields: Overall Recommendation (Proceed to Offer / Hold — Further Review / Reject), Score / Rating (1–5 per criterion: Subject Knowledge, Communication, Attitude, Classroom Management — for demo), Panel Notes (textarea), Decision Rationale (textarea). On Submit: interview status = Completed, candidate pipeline stage updated accordingly.

### 6.4 Modal: Cancel Interview
Reason (dropdown: Candidate Withdrew / Scheduling Conflict / Role Filled / Other) + Notes. Confirm / Cancel. On Confirm: status = Cancelled, notifications sent to candidate and panel.

---

## 7. Charts

**Weekly Calendar Widget** — available in Calendar View. 7-day column layout showing all interviews for the current week, grouped by branch (colour-coded). Each interview appears as a time-block tile with candidate name, type chip, and status badge. Clicking a tile opens the View/Edit drawer. Navigation: Previous Week / Current Week / Next Week. Rendered using a lightweight HTMX-fetched HTML calendar grid (no client-side calendar library required).

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Interview scheduled | "Interview scheduled for [Candidate] on [Date]." | Success | 4s |
| Slot confirmation sent | "Branch principal notified for demo class confirmation." | Info | 4s |
| Interview confirmed by branch | "Demo class slot confirmed by [Principal Name]." | Success | 4s |
| Interview completed — outcome saved | "Interview outcome recorded for [Candidate]." | Success | 4s |
| No-show marked | "[Candidate] marked as no-show. Recruiter notified." | Warning | 5s |
| Reschedule requested | "Reschedule request logged. HR Manager notified." | Info | 4s |
| Interview cancelled | "Interview cancelled. Notifications sent." | Info | 4s |
| Duplicate time slot warning | "Another interview is already scheduled at this time for this branch. Confirm to proceed." | Warning | 6s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No interviews scheduled | "No Interviews Scheduled" | "Schedule interviews for candidates in the recruitment pipeline." | Schedule Interview |
| Filter returns no results | "No Matching Interviews" | "Adjust filters or date range to find interviews." | Clear Filters |
| Calendar view — no interviews this week | "No Interviews This Week" | "There are no interviews scheduled for this week." | Schedule Interview |
| Today's filter — no interviews today | "No Interviews Today" | "No interviews are scheduled for today." | View This Week |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | KPI skeletons (6) + table row skeletons (12) |
| Filter change | Table body skeletons |
| Calendar view load | Full calendar skeleton (7-column grid with placeholder tiles) |
| Drawer open | Form field skeletons |
| Mark Complete outcome submit | Button spinner + row shimmer |

---

## 11. Role-Based UI Visibility

| Element | HR Director (41) / Manager (42) | Recruiter (43, 44) |
|---|---|---|
| Schedule Interview button | Visible + enabled | Hidden |
| Edit action | Visible + enabled | Hidden |
| Cancel action | Visible + enabled | Hidden |
| Mark Complete action | Visible + enabled | Hidden |
| No-Show mark action | Visible + enabled | Hidden |
| View action | Visible | Visible (own candidates only) |
| Calendar view | Full — all branches | Read-only — own candidates only |
| Export Interview List | Visible | Hidden |
| Interviewer assignment field | Visible | N/A |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/recruitment/interviews/` | JWT | List all interviews (paginated) |
| POST | `/api/v1/hr/recruitment/interviews/` | JWT | Schedule new interview |
| GET | `/api/v1/hr/recruitment/interviews/{id}/` | JWT | Fetch interview detail |
| PATCH | `/api/v1/hr/recruitment/interviews/{id}/` | JWT | Update interview |
| PATCH | `/api/v1/hr/recruitment/interviews/{id}/confirm/` | JWT | Confirm slot (branch principal action) |
| PATCH | `/api/v1/hr/recruitment/interviews/{id}/complete/` | JWT | Record interview outcome |
| PATCH | `/api/v1/hr/recruitment/interviews/{id}/noshow/` | JWT | Mark as no-show |
| PATCH | `/api/v1/hr/recruitment/interviews/{id}/cancel/` | JWT | Cancel interview |
| GET | `/api/v1/hr/recruitment/interviews/kpis/` | JWT | KPI summary |
| GET | `/api/v1/hr/recruitment/interviews/calendar/` | JWT | Calendar view data (week range) |
| GET | `/api/v1/hr/recruitment/interviews/export/` | JWT | Export interview list |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Live search | keyup changed delay:400ms | GET `/api/v1/hr/recruitment/interviews/?q={val}` | `#interviews-table-body` | innerHTML |
| Filter apply | change | GET `/api/v1/hr/recruitment/interviews/?type={}&status={}&branch={}` | `#interviews-table-body` | innerHTML |
| Date filter | change | GET `/api/v1/hr/recruitment/interviews/?date_range={val}` | `#interviews-table-body` | innerHTML |
| Pagination | click | GET `/api/v1/hr/recruitment/interviews/?page={n}` | `#interviews-table-body` | innerHTML |
| Schedule drawer open | click | GET `/group/hr/recruitment/interviews/schedule/drawer/` | `#drawer-container` | innerHTML |
| View/Edit drawer open | click | GET `/group/hr/recruitment/interviews/{id}/drawer/` | `#drawer-container` | innerHTML |
| Record Outcome drawer | click | GET `/group/hr/recruitment/interviews/{id}/outcome/drawer/` | `#drawer-container` | innerHTML |
| Cancel modal | click | GET `/group/hr/recruitment/interviews/{id}/cancel/modal/` | `#modal-container` | innerHTML |
| Schedule submit | submit | POST `/api/v1/hr/recruitment/interviews/` | `#interviews-table-body` | afterbegin |
| Mark No-Show | click | PATCH `/api/v1/hr/recruitment/interviews/{id}/noshow/` | `#interview-row-{id}` | outerHTML |
| Calendar week navigation | click | GET `/api/v1/hr/recruitment/interviews/calendar/?week={date}` | `#calendar-container` | innerHTML |
| Switch to Calendar view | click | GET `/group/hr/recruitment/interviews/calendar/` | `#main-content` | innerHTML |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
