# 05 — Group Training & Development Manager Dashboard

- **URL:** `/group/hr/training/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Training & Development Manager (Role 45, G2)

---

## 1. Purpose

The Group Training & Development Manager Dashboard is the central hub for planning, scheduling, and tracking all staff learning and development programs across the group's branch network. The T&D Manager is responsible for four distinct training categories that each carry different urgency levels: Induction Training for new joiners (must be completed within the first 30 days of joining), Continuing Professional Development (CPD) for existing teaching and non-teaching staff, Compliance Training that is legally mandated (POCSO awareness, fire safety, first aid, CBSE-mandated programs), and Skill Upgrade Programs tied to appraisal and promotion cycles.

A school group operating 5–50 branches with hundreds to thousands of teaching staff requires a structured, data-driven approach to CPD. Without this dashboard, the T&D Manager would have no reliable way to track which branches are running training sessions, which staff have met their minimum CPD hours for the year, or which compliance certificates are approaching expiry. The dashboard addresses this gap by aggregating completion data from all branches into a unified view with branch-level breakdowns.

The training calendar embedded in this dashboard allows the T&D Manager to plan sessions months in advance, assign trainers (internal faculty or external vendors), and send automated enrollment reminders. Session conflicts (a teacher enrolled in two overlapping sessions) are detected at enrollment time. The T&D Manager can also assign mandatory training programs to entire branches or to specific role categories, with the system tracking individual completion against the group-wide mandate.

Certificate management is a compliance-critical function surfaced on this dashboard. Several training programs (POCSO, first aid, fire safety) issue certificates with fixed validity periods (typically 1–3 years). When a certificate is 60 days from expiry, it enters the renewal queue. This dashboard ensures the T&D Manager can act proactively on certificate renewals rather than allowing lapsed certifications to create regulatory exposure during inspections.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Training & Development Manager | G2 | Full read + write on training programs | Primary role; G2 allows content creation |
| Group HR Director | G3 | Full read + override | Can view all T&D data and escalate |
| Group HR Manager | G3 | Full read | Can view completion stats for HR reporting |
| Group Performance Review Officer | G1 | Read-only | Views CPD hours as part of appraisal context |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → HR & Staff → Training & Development
```

### 3.2 Page Header
- **Title:** `Group Training & Development Dashboard`
- **Subtitle:** `[N] Active Programs · [N] Staff Trained This Month · AY [current academic year]`
- **Role Badge:** `Group T&D Manager`
- **Right-side controls:** `+ New Training Program` · `Training Calendar` · `Export Completion Report`

### 3.3 Alert Banner (conditional)

| Condition | Banner | Severity |
|---|---|---|
| Compliance certificates expiring in < 30 days | "[N] staff member(s) have compliance training certificates expiring within 30 days. Schedule renewals." | Red |
| Induction training overdue for new joiners | "[N] new joiner(s) have not completed induction training within the 30-day window." | Red |
| CPD compliance below 60% in any branch | "CPD completion at [Branch Name] is critically low at [X]%. Intervention required." | Amber |
| Training session scheduled tomorrow with < 50% enrollment | "Session [Program Name] tomorrow has only [N] enrolled out of [N] required. Send reminders." | Amber |

---

## 4. KPI Summary Bar

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Active Training Programs | Count of programs with at least one scheduled session in current AY | Blue | Links to programs table |
| Staff Trained This Month | Unique staff who completed at least one session in current month | Blue | Completion detail |
| Completion Rate % | Group-wide % of enrolled staff who completed their assigned sessions | Green ≥ 80%, Amber 60–80%, Red < 60% | Branch breakdown chart |
| Certificates Expiring (30 Days) | Count of certificates expiring within 30 days | Red if > 0, Green if 0 | Expiry queue list |
| Induction Pending | New joiners (last 30 days) who have not completed induction | Red if > 0, Green if 0 | Pending induction list |
| CPD Hours per Teacher (Avg) | Average CPD hours logged per teaching staff in current AY | Green ≥ 20h, Amber 10–20h, Red < 10h | CPD hours detail |

---

## 5. Main Table — Training Programs

| Column | Type | Sortable | Filterable |
|---|---|---|---|
| Program Name | Text (link to program detail) | Yes | Yes (text search) |
| Type | Badge (CPD / Induction / Compliance / Skill Upgrade) | Yes | Yes (checkbox) |
| Target Role Category | Text (Teaching / Non-Teaching / All Staff) | Yes | Yes (dropdown) |
| Branches | Count badge (e.g., "5 branches") | Yes | Yes (multi-select) |
| Scheduled Date | Date (earliest upcoming session) | Yes | Yes (date range) |
| Enrolled | Integer | Yes | No |
| Completed | Integer | Yes | No |
| Completion % | Percentage bar | Yes | Yes (< threshold) |
| Status | Badge (Upcoming / Ongoing / Completed / Cancelled) | Yes | Yes |
| Actions | View / Edit / Duplicate / Cancel | No | No |

### 5.1 Filters

| Filter | Type | Options |
|---|---|---|
| Program Type | Checkbox | CPD / Induction / Compliance / Skill Upgrade |
| Branch | Multi-select dropdown | All configured branches |
| Status | Checkbox | Upcoming / Ongoing / Completed / Cancelled |
| Completion Rate | Threshold input | Below X% |
| Scheduled Date | Date range picker | Any range |

### 5.2 Search
- Full-text: Program name, target role category, branch name
- 300ms debounce

### 5.3 Pagination
- Server-side · 20 rows/page

---

## 6. Drawers

### 6.1 Drawer: `training-create` — Create New Training Program
- **Trigger:** `+ New Training Program` button
- **Width:** 560px
- **Fields:**
  - Program Name (required, text, max 120 chars)
  - Program Type (required, dropdown: CPD / Induction / Compliance / Skill Upgrade)
  - Description (required, rich textarea, max 2000 chars)
  - Target Role Category (required, multi-select: Teaching / Non-Teaching / Admin / All Staff)
  - Target Branches (required, multi-select, all branches)
  - Trainer Name / Organisation (required, text)
  - Training Mode (required, radio: In-Person / Online / Hybrid)
  - Session Date(s) (required, date-time picker; multi-session supported)
  - Duration per Session (required, numeric in hours)
  - Venue / Link (required, text)
  - Certificate Issued (checkbox; if checked: Certificate Name, Validity in months)
  - Max Enrollment per Session (optional, integer)
- **Validation:** At least one session date required; if Certificate Issued, validity months required

### 6.2 Drawer: `training-view` — View Program Detail
- **Trigger:** Click on program name
- **Width:** 720px
- Shows: Full program description, all sessions with dates and enrollment counts, enrolled staff list, completion list with dates, certificate records, branch-wise completion breakdown

### 6.3 Drawer: `training-edit` — Edit Program
- **Trigger:** Actions → Edit
- **Width:** 560px
- Same fields as create, pre-populated; Type and Target Role locked after first enrollment

### 6.4 Modal: Cancel Program
- Confirmation: "You are cancelling [Program Name]. [N] enrolled staff will be notified. Completed records will be retained. Confirm cancellation?"
- Buttons: Confirm Cancel · Back

---

## 7. Charts

### 7.1 Training Completion by Branch (Grouped Bar Chart)
- **X-axis:** Branch names
- **Series 1:** Enrolled count (grey bar)
- **Series 2:** Completed count (green bar)
- **Filter toggle:** By Program Type (CPD / Compliance / Induction)

### 7.2 CPD Hours Trend (Line Chart)
- **X-axis:** Months in current academic year
- **Y-axis:** Average CPD hours per teaching staff
- **Series:** Group average + individual branch lines
- **Benchmark line:** 20 hours/year target shown as dashed line

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Program created | "Training program [Name] created and enrollment opened." | Success | 4s |
| Program updated | "Training program updated successfully." | Success | 3s |
| Program cancelled | "Program cancelled. [N] enrolled staff have been notified." | Warning | 5s |
| Export triggered | "Completion report is being generated. You will be notified when ready." | Info | 5s |
| Reminder sent | "Enrollment reminders sent to [N] unregistered eligible staff." | Info | 4s |
| Validation error | "Please fill all required fields. Certificate validity required if certificate is issued." | Error | 5s |

---

## 9. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No programs in current AY | "No Training Programs Yet" | "No training programs have been scheduled for this academic year. Start planning." | + New Training Program |
| No completions this month | "No Completions This Month" | "No staff have completed any training sessions in the current month." | View Programs |
| All inductions complete | "Induction Queue Clear" | "All new joiners in the last 30 days have completed their induction training." | — |

---

## 10. Loader States

| Trigger | Loader |
|---|---|
| Initial page load | Full skeleton: 6 KPI shimmer cards + table skeleton (10 rows) |
| Program detail drawer open | Drawer spinner; enrollment list loads progressively |
| Program creation form submit | Button spinner + form disabled |
| Charts load | Shimmer overlay on each chart panel |

---

## 11. Role-Based UI Visibility

| Element | T&D Manager (G2) | HR Director (G3) | HR Manager (G3) | Performance Officer (G1) |
|---|---|---|---|---|
| KPI Summary Bar | Visible (all 6 cards) | Visible (all 6 cards) | Visible (all 6 cards) | Visible (CPD Hours card only) |
| Programs Table | Visible + Create/Edit/Cancel | Visible (read + override) | Visible (read-only) | Visible (read-only) |
| + New Training Program | Visible | Visible | Hidden | Hidden |
| Enrollment Lists in Drawer | Visible | Visible | Visible | Visible (no PII beyond names) |
| Certificate Management | Visible | Visible | Visible | Hidden |
| Export Button | Visible | Visible | Visible | Hidden |
| Charts | Visible | Visible | Visible | Visible (CPD Hours only) |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/hr/training/kpis/` | JWT (G2+) | All 6 KPI card values |
| GET | `/api/v1/hr/training/programs/` | JWT (G2+) | Paginated list of training programs |
| POST | `/api/v1/hr/training/programs/` | JWT (G2) | Create a new training program |
| GET | `/api/v1/hr/training/programs/{id}/` | JWT (G2+) | Program detail with enrollment and completion |
| PATCH | `/api/v1/hr/training/programs/{id}/` | JWT (G2) | Update program fields |
| POST | `/api/v1/hr/training/programs/{id}/cancel/` | JWT (G2) | Cancel a program and notify enrollees |
| GET | `/api/v1/hr/training/charts/completion-by-branch/` | JWT (G2+) | Branch completion bar chart data |
| GET | `/api/v1/hr/training/charts/cpd-trend/` | JWT (G2+) | CPD hours trend line chart data |
| POST | `/api/v1/hr/training/programs/{id}/send-reminders/` | JWT (G2) | Trigger enrollment reminder notifications |
| GET | `/api/v1/hr/training/export/completion/` | JWT (G2+) | Async completion report export |

---

## 13. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Load KPI bar | `load` | GET `/api/v1/hr/training/kpis/` | `#kpi-bar` | `innerHTML` |
| Load programs table | `load` | GET `/api/v1/hr/training/programs/` | `#programs-table` | `innerHTML` |
| Open program detail drawer | `click` on program name | GET `/api/v1/hr/training/programs/{id}/` | `#program-drawer` | `innerHTML` |
| Filter by program type | `change` on type filter | GET `/api/v1/hr/training/programs/?type=...` | `#programs-table` | `innerHTML` |
| Submit new program form | `click` on Submit | POST `/api/v1/hr/training/programs/` | `#programs-table` | `innerHTML` |
| Send enrollment reminders | `click` on Send Reminders button | POST `/api/v1/hr/training/programs/{id}/send-reminders/` | `#reminder-result` | `innerHTML` |
| Paginate programs table | `click` on page controls | GET `/api/v1/hr/training/programs/?page=N` | `#programs-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
