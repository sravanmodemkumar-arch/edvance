# 07 — Doctor Visit Schedule

> **URL:** `/group/health/doctor-schedule/`
> **File:** `07-doctor-visit-schedule.md`
> **Template:** `portal_base.html`
> **Priority:** P1
> **Role:** Group Medical Coordinator (primary) · School Medical Officer (manage own branch)

---

## 1. Purpose

Schedule and track all doctor visits across every branch in the group. This page is the operational planning tool for ensuring continuous medical coverage — every branch must have a minimum of two general physician visits per week, plus specialist visits as required by the student health profile of that branch.

The page serves two modes: forward planning (scheduling upcoming visits) and compliance monitoring (tracking whether planned visits actually occurred). Gaps in doctor visits — branches going days without a visit — represent a health infrastructure failure and may create medico-legal exposure. The compliance view surfaces these gaps immediately so the Medical Coordinator can take corrective action. Scale: 2–5 visits/week per branch × 20–50 branches = 40–250 visits/week group-wide.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Medical Coordinator | G3 | Full CRUD — all branches, all schedules | Primary planner and compliance monitor |
| Group School Medical Officer | G3 | Create / edit / mark complete — own branch only | Cannot see other branches' clinical details |
| Group Mental Health Coordinator | G3 | Read only — for specialist counselling visit coordination | No edit access |
| Group Emergency Response Officer | G3 | Read only — for emergency doctor availability awareness | No edit access |
| All other roles | — | — | No access |

> **Access enforcement:** Django view decorator `@require_role('medical_coordinator', 'school_medical_officer', 'mental_health_coordinator', 'emergency_response_officer')`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Doctor Visit Schedule
```

### 3.2 Page Header
- **Title:** `Doctor Visit Schedule`
- **Subtitle:** `[N] Visits Scheduled This Week · [N] Completed · [N]% Compliance`
- **Right controls:** `+ Schedule Visit` · `List / Calendar Toggle` · `Advanced Filters` · `Export`
- **Date navigation (Calendar mode):** `← Prev Week` · `[Current Week Label]` · `Next Week →` · `Today`

### 3.3 Alert Banner

| Condition | Banner Text | Severity |
|---|---|---|
| Branch with no visit > 7 days | "[Branch] has had no doctor visit in [N] days. Minimum coverage breach." | Red |
| Doctor absent with no replacement | "Dr [Name] is absent at [Branch] today with no replacement assigned." | Red |
| Visit cancelled with no rescheduling | "Visit at [Branch] on [date] was cancelled with no rescheduled date." | Amber |
| Specialist visit overdue | "Specialist ([Specialization]) visit at [Branch] is [N] days overdue." | Amber |
| Low weekly coverage (< 2 visits) | "[Branch] has only [N] general physician visit(s) scheduled this week — below minimum." | Amber |

---

## 4. KPI Summary Bar (6 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Visits Scheduled This Week | Total planned visits across all branches, current week | Blue always | → List view, filtered to this week |
| Visits Completed This Week | Visits marked as Completed | Blue always | → List view, filtered Completed |
| Compliance % (Planned vs Actual) | (Completed / Scheduled) × 100 for current week | Green ≥ 90% · Yellow 70–90% · Red < 70% | → List view, full |
| Branches with Zero Visit This Week | Branches with no visit scheduled or completed this week | Green = 0 · Yellow 1–2 · Red > 2 | → List filtered to affected branches |
| Specialist Visits This Month | Count of specialist (non-GP) visits scheduled/completed this month | Blue always | → List filtered to Specialist type |
| Overdue Visits | Visits in Scheduled status with date in the past | Green = 0 · Yellow 1–5 · Red > 5 | → List filtered to Overdue |

---

## 5. Main Table / Calendar

### 5.1 List View (Default)

**Search:** Branch name, doctor name. 300ms debounce.

**Advanced Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Date Range | Date picker | From — To (default: current week) |
| Type | Checkbox | General / Specialist / Emergency |
| Status | Checkbox | Scheduled / Completed / Cancelled / No-Show |
| Doctor | Multi-select | All doctors in registry |
| Compliance Gap | Checkbox | Show branches with < 2 GP visits this week only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Date | ✅ | |
| Day | ✅ | Mon–Sun |
| Branch | ✅ | |
| Doctor | ✅ | Doctor name; link → staff-detail drawer |
| Specialization | ✅ | General Physician / Paediatrician / Ortho / Gynaecology etc. |
| Type | ✅ | General / Specialist / Emergency |
| Scheduled Time | ✅ | HH:MM |
| Actual Arrival | ✅ | HH:MM or — (if not yet marked) |
| Patients Seen | ✅ | Count; — if not yet completed |
| Status | ✅ | Colour badge: Scheduled (Blue) / Completed (Green) / Cancelled (Red) / No-Show (Orange) |
| Actions | ❌ | View · Edit · Cancel · Mark Complete |

**Bulk actions:** Export selected; Mark selected as Completed; Bulk cancel with reason.
**Default sort:** Date ascending (soonest first), then Branch.
**Pagination:** Server-side · 25/page.

---

### 5.2 Calendar View (Toggle)

> Weekly grid — branches as rows, days (Mon–Sun) as columns. Designed for at-a-glance coverage verification.

**Structure:**
- Each cell = intersection of branch (row) + day (column)
- If a visit is scheduled: cell shows `Doctor Name · HH:MM` — colour-coded by status
  - Blue background = Scheduled
  - Green background = Completed
  - Red background = Cancelled or No-Show
  - Grey background = No visit scheduled (empty cell)
- If multiple visits on same day at same branch: stacked cell entries
- Click on cell → opens `visit-detail` drawer for that visit
- Empty cell click → opens `visit-create` drawer pre-filled with branch + date

**Week navigation:** `← Prev Week` · `Next Week →` · `Today` — HTMX partial update, no full page reload.

**Branch row summary (rightmost column):** Count of completed visits this week for that branch, colour-coded vs minimum (≥ 2 = Green, 1 = Yellow, 0 = Red).

---

## 6. Drawers

### 6.1 Drawer: `visit-detail` — View Visit Details
- **Trigger:** Actions → View · or click on calendar cell
- **Width:** 620px

**Sections:**
| Field | Notes |
|---|---|
| Visit ID | System-generated |
| Branch | |
| Doctor | Name + specialization + contact |
| Visit Type | General / Specialist / Emergency |
| Scheduled Date & Time | |
| Actual Arrival Time | Editable if still today |
| Scheduled Duration | e.g., 3 hours |
| Patients Seen | Count |
| Consultation Summary | Brief notes from doctor's session |
| Issues Reported | Any branch health concerns raised by doctor |
| Prescription Summary | Total prescriptions issued (count) |
| Follow-up Recommended | Toggle + notes |
| Status | Current status |
| Cancellation Reason | If Cancelled/No-Show |

**Actions in drawer (role-dependent):** Mark Complete · Edit · Cancel · Log Patients Seen

---

### 6.2 Drawer: `visit-create` — Schedule New Visit
- **Trigger:** `+ Schedule Visit` button · empty calendar cell click
- **Width:** 600px

**Fields:**
| Field | Type | Validation |
|---|---|---|
| Branch | Select | Required; pre-filled if from calendar cell |
| Doctor | Select + search | Required; from medical staff registry, filtered by type |
| Date | Date | Required; cannot be in the past (unless backdating existing visit) |
| Time | Time | Required |
| Duration | Select | 1hr / 2hr / 3hr / Half Day / Full Day |
| Visit Type | Radio | General / Specialist / Emergency |
| Recurrence | Select | One-off / Weekly / Fortnightly / Monthly |
| Recurrence End Date | Date | Required if Recurrence ≠ One-off |
| Notes | Textarea | Optional — pre-visit instructions or requirements |

**Availability check:** On doctor + date selection, system checks doctor's availability (other branch visits on same date/time). Conflict shown inline: "Dr [Name] already has a visit at [Branch] at [Time] on [Date]. Confirm or change."

**Minimum coverage enforcement:** If scheduling would result in < 2 GP visits this week at the selected branch, a warning banner appears in the drawer: "This branch currently has [N] GP visit(s) this week. Minimum is 2."

**Recurrence preview:** When recurrence is selected, a collapsible preview shows all dates that will be created (up to 8 occurrences shown).

---

### 6.3 Drawer: `visit-edit` — Edit Existing Visit
- **Trigger:** Actions → Edit
- **Width:** 600px (same fields as create, pre-populated)
- **Additional field:** Reason for Change (required if doctor, date, or time is changed)
- **Read-only:** Visit ID, original Branch

---

### 6.4 Modal: `cancel-visit` — Cancel a Visit
- **Trigger:** Actions → Cancel
- **Width:** 440px

**Fields:**
| Field | Type | Notes |
|---|---|---|
| Cancellation Reason | Select | Doctor Absent / Branch Closed / Emergency / Weather / Holiday / Other |
| Reason Details | Textarea | Required if "Other"; optional otherwise |
| Reschedule? | Toggle | If Yes: Reschedule Date + Time fields appear |
| Reschedule Date | Date | Conditional; must be within 7 days |
| Notify Medical Coordinator | Checkbox | Default: checked if user is School Medical Officer |

**Warning text:** "Cancelling this visit may create a coverage gap at [Branch]. A replacement visit should be scheduled within [N] days to maintain compliance."

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Visit scheduled | "Doctor visit scheduled: Dr [Name] at [Branch] on [date] at [time]." | Success | 4s |
| Recurring visits created | "[N] visits created for Dr [Name] at [Branch] ([recurrence pattern])." | Success | 5s |
| Visit marked complete | "Visit at [Branch] by Dr [Name] marked as Completed." | Success | 4s |
| Visit cancelled | "Visit at [Branch] on [date] cancelled. [Reschedule date shown if applicable]." | Warning | 5s |
| No-show recorded | "No-show recorded for Dr [Name] at [Branch] on [date]." | Warning | 5s |
| Doctor conflict alert | "Scheduling conflict detected for Dr [Name] on [date]. Review required." | Warning | 6s |
| Visit updated | "Visit details updated for [Branch] on [date]." | Success | 4s |
| Export prepared | "Visit schedule export ready. Download now." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No visits scheduled this week | "No Visits Scheduled This Week" | "No doctor visits have been scheduled for any branch this week." | [+ Schedule Visit] |
| All visits complete | "All Visits Completed" | "All scheduled doctor visits for this week are marked complete." | — |
| No overdue visits | "No Overdue Visits" | "All past visits have been accounted for — completed, cancelled, or no-show." | — |
| Filter returns no results | "No Visits Match Filters" | "Adjust the branch, date range, or status filters to see results." | [Clear Filters] |
| Branch has no visits ever | "No Visit History" | "No doctor visits have been scheduled for this branch yet." | [Schedule First Visit] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load (list view) | Skeleton: 6 KPI cards + table skeleton (15 rows × 11 columns) + alerts |
| Page load (calendar view) | Skeleton: 6 KPI cards + weekly grid skeleton (N branches × 7 days, shimmer cells) |
| Week navigation (calendar) | Calendar grid shimmer; KPI bar updates alongside |
| Filter/search (list view) | Table body skeleton |
| Visit detail drawer | 620px form skeleton (field rows) |
| Create visit drawer | 600px form skeleton; doctor dropdown populates via lazy fetch |
| Doctor availability check | Inline spinner on doctor+date field combination |
| Recurrence preview | Collapsible section shimmer while dates are computed |

---

## 10. Role-Based UI Visibility

| Element | Medical Coordinator G3 | School Medical Officer G3 | Mental Health Coordinator G3 | Emergency Response Officer G3 |
|---|---|---|---|---|
| Schedule Visit (all branches) | ✅ | ❌ | ❌ | ❌ |
| Schedule Visit (own branch) | ✅ | ✅ | ❌ | ❌ |
| Edit Visit | ✅ | ✅ (own branch) | ❌ | ❌ |
| Cancel Visit | ✅ | ✅ (own branch) | ❌ | ❌ |
| Mark Complete | ✅ | ✅ (own branch) | ❌ | ❌ |
| View All Branches | ✅ | ✅ (read) | ✅ (read) | ✅ (read) |
| View Calendar | ✅ | ✅ | ✅ | ✅ |
| Export Schedule | ✅ | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/` | JWT (G3+) | Paginated, filtered visit list |
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/calendar/` | JWT (G3+) | Weekly calendar view data |
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/{id}/` | JWT (G3+) | Single visit detail |
| POST | `/api/v1/group/{group_id}/health/doctor-schedule/` | JWT (Role 85, 86) | Create visit (single or recurring) |
| PATCH | `/api/v1/group/{group_id}/health/doctor-schedule/{id}/` | JWT (Role 85, 86) | Update visit |
| POST | `/api/v1/group/{group_id}/health/doctor-schedule/{id}/complete/` | JWT (Role 85, 86) | Mark visit as completed |
| POST | `/api/v1/group/{group_id}/health/doctor-schedule/{id}/cancel/` | JWT (Role 85, 86) | Cancel visit |
| POST | `/api/v1/group/{group_id}/health/doctor-schedule/{id}/no-show/` | JWT (Role 85, 86) | Record doctor no-show |
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/kpis/` | JWT (G3+) | KPI card values |
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/availability/` | JWT (G3+) | Doctor availability check (date + doctor params) |
| GET | `/api/v1/group/{group_id}/health/doctor-schedule/export/` | JWT (Role 85, 86) | Async schedule export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| List view search | `input delay:300ms` | GET `.../doctor-schedule/?q={val}` | `#visit-table-body` | `innerHTML` |
| List view filter | `click` | GET `.../doctor-schedule/?{filters}` | `#visit-table-section` | `innerHTML` |
| Pagination | `click` | GET `.../doctor-schedule/?page={n}` | `#visit-table-section` | `innerHTML` |
| Calendar week navigation | `click` Prev/Next/Today | GET `.../doctor-schedule/calendar/?week={date}` | `#calendar-grid` | `innerHTML` |
| Toggle list/calendar view | `click` toggle button | GET `.../doctor-schedule/?view={list\|calendar}` | `#schedule-view-container` | `innerHTML` |
| Open visit drawer | `click` on row or cell | GET `.../doctor-schedule/{id}/` | `#drawer-body` | `innerHTML` |
| Open create drawer (calendar cell) | `click` on empty cell | GET `.../doctor-schedule/create/?branch={id}&date={date}` | `#drawer-body` | `innerHTML` |
| Doctor availability check | `change` on doctor/date fields | GET `.../doctor-schedule/availability/?doctor={id}&date={date}` | `#availability-status` | `innerHTML` |
| Mark complete | `click` | POST `.../doctor-schedule/{id}/complete/` | `#visit-row-{id}` | `outerHTML` |
| Cancel confirm | `click` | POST `.../doctor-schedule/{id}/cancel/` | `#visit-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
