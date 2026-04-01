# O-06 — Leave & Attendance

**Route:** `GET /hr/leave/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** HR Manager (#79)
**Also sees (own records):** All Division O roles and all EduForge employees via self-serve route `GET /hr/my-leave/` (out of scope of this spec — covered below as a companion self-serve page)

---

## Purpose

Centralised leave management and attendance oversight for all EduForge employees. HR Manager uses this page to: approve/reject leave requests, view team-wide attendance, manage the holiday master calendar, monitor leave balance health, and pull monthly attendance reports for payroll LOP computation. The attendance view is especially important for payroll — LOP (Loss of Pay) days computed here are the direct input to O-05 payroll processing.

Employee self-service (leave application, balance check, attendance calendar) is handled at `/hr/my-leave/` — accessible by all employees, not just Division O.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Leave request list | `hr_leave_request` JOIN `hr_employee` JOIN `hr_leave_type` | 2 min |
| Leave balance table | `hr_leave_balance` JOIN `hr_employee` for current FY | 5 min |
| Attendance grid | `hr_attendance_record` for selected month + all active employees | 5 min |
| Monthly attendance summary | `hr_attendance_record` GROUP BY employee + mode for selected month | 5 min |
| Holiday master | `hr_holiday` for current FY | 60 min (rarely changes) |
| Leave analytics | `hr_leave_request` aggregated by type, division, month for last 12 months | 30 min |
| Team calendar | `hr_leave_request WHERE status='APPROVED'` + `hr_holiday` for next 30 days | 5 min |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `requests`, `balances`, `attendance`, `calendar`, `analytics` | `requests` | Active section |
| `?status` | `pending`, `approved`, `rejected`, `cancelled`, `all` | `pending` | Filter leave requests |
| `?leave_type` | `cl`, `sl`, `el`, `ml`, `pl`, `comp_off`, `lop`, `all` | `all` | Filter by leave type |
| `?division` | A–O | `all` | Filter by employee division |
| `?month` | `YYYY-MM` | current month | Attendance and balance reporting period |
| `?employee_id` | UUID | — | Jump to specific employee's records |
| `?export` | `attendance_report_csv`, `leave_register_csv`, `lop_report_csv` | — | Export (HR Manager only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Leave requests list | `?part=requests` | Page load + filter | `#o6-requests-list` |
| Leave balances table | `?part=balances` | Tab click + month | `#o6-balances-table` |
| Attendance grid | `?part=attendance&month={YYYY-MM}` | Tab click + month change | `#o6-attendance-grid` |
| Monthly summary | `?part=monthly_summary&month={YYYY-MM}` | Attendance tab + month | `#o6-monthly-summary` |
| Team calendar | `?part=calendar` | Calendar tab click | `#o6-team-calendar` |
| Analytics charts | `?part=analytics` | Analytics tab click | `#o6-analytics` |
| Approve/reject inline | `POST /hr/leave/requests/{id}/action/` | [Approve]/[Reject] click | Inline row swap |
| Holiday form | `?part=holiday_modal` | [+ Add Holiday] click | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Leave & Attendance   Month: [March 2026 ▼]                          │
├──────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (4 tiles)                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  [Requests (4 pending)] [Balances] [Attendance] [Calendar] [Analytics]│
└──────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (4 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 4            │ │ 94.2%        │ │ 3            │ │ 2            │
│ Pending      │ │ Attendance   │ │ On Leave     │ │ LOP Days     │
│ Requests     │ │ Rate (today) │ │ Today        │ │ This Month   │
│ 1 > 3d wait  │ │ 112/119 emp  │ │ CL:2 · SL:1  │ │ (payroll in) │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

---

## Leave Requests Tab

```
  Filter: Status [Pending ▼]  Type [All ▼]  Division [All ▼]

  ☐ │ Employee │ Division │ Type │ Dates │ Days │ Reason │ Applied │ Status │ Actions
```

| Column | Description |
|---|---|
| Employee | Name + avatar |
| Division | Division badge |
| Type | CL / SL / EL / ML / PL / COMP_OFF / LOP |
| Dates | From – To dates |
| Days | Number of days (0.5 for half-day) |
| Reason | Truncated (first 60 chars) + hover tooltip for full text |
| Applied | "N days ago" or absolute date |
| Status | PENDING (amber) / APPROVED (green) / REJECTED (red) / CANCELLED (grey) |
| Actions | [Approve] [Reject] [View Details] |

**[Approve]:** inline HTMX — row transitions to APPROVED green. `hr_leave_request.status='APPROVED'`, `approved_by`, `approved_at` set. `hr_leave_balance` decremented. Employee notified via email.

**[Reject]:** opens rejection reason modal:
```
  Reason for rejection* (required):
  [                                              ]
  [Cancel]                              [Reject Leave]
```
Reason stored in `hr_leave_request.rejection_reason`. Employee notified with reason.

**[View Details]:** opens leave detail drawer (full application text, employee's leave balance preview, conflict check with other team members on same dates).

### Leave Conflict Detection

On HR Manager opening a leave request for approval, the system checks:
- Are other employees from the same division on leave on the same dates?
- If conflict: amber banner in detail drawer: "⚠ 2 other employees from Division C are on leave on 25 Mar (Rohan V.: CL, Priya S.: EL). Approve with caution."
- This is advisory — HR Manager can still approve.

### Half-Day Leave

`hr_leave_request.days = 0.5`. System stores `half_day_session`: MORNING / AFTERNOON. Attendance record for that day shows mode = `HALF_DAY_LEAVE`. Payroll treats 0.5 LOP days accordingly.

### Leave Type Logic

| Code | Name | Max/Year | Carry Forward | Auto-Approve | Notes |
|---|---|---|---|---|---|
| CL | Casual Leave | 12 | No (lapse) | After 3d pending | Cannot club with EL or ML |
| SL | Sick Leave | 12 | No (lapse) | After 3d pending | Medical certificate required if > 3 consecutive days |
| EL | Earned Leave | 30 (accrual: 2.5/month) | Yes, max 30 days | No | Encashable at exit (F&F) |
| ML | Maternity Leave | 182 days (Maternity Benefit Act 2017) | N/A | No — HR Manager approval + HR Manager notifies payroll | 26 weeks for first 2 children; 12 for subsequent |
| PL | Paternity Leave | 7 days (EduForge policy) | No | No | Within 3 months of birth/adoption |
| COMP_OFF | Compensatory Off | As earned | Lapse in 30 days | No | Earned when employee works on a declared holiday |
| LOP | Loss of Pay | Unlimited | N/A | No — HR Manager manually marks | Applied when leave balance exhausted; deducted from salary |
| BL | Bereavement Leave | 3 days | No | No | Immediate family death |

**Task O-7 auto-approval eligibility:** Only CL, SL, EL, and COMP_OFF are eligible for auto-approval after 3 working days. ML, PL, BL, and LOP are **never** auto-approved — they require HR Manager manual review (ML requires payroll team notification; BL requires documentation; LOP is HR Manager-initiated only).

---

## Comp Off Admin Flow

When an employee works on a declared holiday (`hr_holiday.is_compensatory=true` for that holiday), they earn a compensatory off day.

### Employee Request (via `/hr/my-leave/`)

```
  Comp Off Request
  ────────────────────────────────────────────────────
  Worked on holiday*:  [25 Mar 2026 — Holi ▼]
  (only declared compensatory holidays listed)
  Work reason*:        [Production incident — exam day support]
  [Submit Comp Off Request]
```

Creates `hr_comp_off_request` with `status='PENDING'`.

### HR Manager Side (Leave Requests tab)

Comp-off requests appear in the leave requests list with type badge `COMP_OFF` and are subject to the same approve/reject flow.

| Rule | Detail |
|---|---|
| HR Manager approval required | Comp-off is not automatic — manager must confirm the holiday work |
| 30-day expiry | On approval, `hr_comp_off_request.expiry_date = approved_at + 30 days`. If not consumed within 30 days, Task O-7 extension lapses the record. |
| Balance creation | On approval: `hr_leave_balance.comp_off_balance += 1`. Employee can then apply COMP_OFF leave normally. |
| Lapse enforcement | Daily check (extension of Task O-5): expired comp-offs removed from balance; employee notified "Your comp-off earned for [holiday] has lapsed." |
| Maximum accumulated | HR Manager can set a cap (default: 2 comp-offs in balance at once) via `hr_policy_config`. |

Consumed comp-off: when employee applies COMP_OFF leave and it's approved, `hr_comp_off_request.status='CONSUMED'`, `consumed_on` set, balance decremented.

---

## Balances Tab

### Leave Balance Table

| Column | Description |
|---|---|
| Employee | Name + EF-ID |
| Division | |
| CL Balance | Remaining CL for current FY |
| SL Balance | Remaining SL |
| EL Balance | Accrued EL (with carry-forward) |
| Comp Off | Available comp-offs |
| LOP Used | Total LOP days consumed in current FY |
| EL Carry-Forward | Amount carried forward from last FY |

Sortable. Searchable by name. Export as CSV.

**EL Accrual:** 2.5 days per completed month (Celery Task O-5). Employees joining mid-year accrue from the month of joining. Probationers accrue EL only after confirmation.

**EL Encashment on Exit:** Computed in O-05 F&F settlement: `encashable_days = min(EL_balance, 30) × (basic_salary / 26)` (26 = average paid days/month per Payment of Wages Act convention).

---

## Attendance Tab

### Attendance Grid

Monthly calendar-style grid — rows = employees, columns = dates.

```
  March 2026 — 21 working days (excl. 2 Saturdays off + 4 Sundays + Holi 25 Mar)

  Employee         01  02  03  04  05  06  07 ... 31  Total  LOP
  Rohan V.    (C)  O   O   O   O   O   O   O  ...  O   21/21   0
  Priya S.    (D)  O   O   O   O   L   L   O  ...  W   19/21   0   (2 SL)
  Kavya R.    (I)  O   W   O   O   O   O   O  ...  O   20/21   0   (WFH on 2nd)
  Rahul M.    (H)  O   O   O   A   O   O   O  ...  H   20/21   1   (1 LOP on 4th — absent, no leave applied)
  ...
```

Colour legend:
- O (green) — Office
- W (blue) — WFH
- L (amber) — Approved Leave
- A (red) — Absent without leave → triggers LOP review
- H (grey) — Holiday
- S (grey-light) — Sunday/Weekend
- P (purple) — Partial (half-day)

**LOP Detection:** Cells marked `A` (absent without approved leave) are flagged for LOP. HR Manager reviews and either:
1. Accepts LOP → `hr_attendance_record.mode` stays `ABSENT`, LOP count auto-fed to payroll for that month
2. Converts to leave retrospectively → creates a retroactive approved leave record (must have remaining balance)

[Mark LOP] bulk action: select multiple flagged cells → [Mark as LOP] → confirmation modal with LOP deduction preview.

### Monthly Attendance Summary

Compact table below the grid:

| Employee | Working Days | Office | WFH | Leave | Holiday | Absent | LOP | Attendance % |
|---|---|---|---|---|---|---|---|---|
| Rohan V. | 21 | 14 | 7 | 0 | 0 | 0 | 0 | 100% |
| Rahul M. | 21 | 18 | 2 | 0 | 0 | 1 | 1 | 95.2% |

[Export LOP Report (CSV)] → used as input to O-05 payroll run.

---

## Calendar Tab

Team leave calendar — visual view of next 30 days showing who is on leave and holidays.

```
  March 22–April 21, 2026
  ─────────────────────────────────────────────────────────────────────
  25 Mar  HOLIDAY  — Holi
  27 Mar  Ravi K. (DevOps) — EL (last day before notice period exit)
  31 Mar  Neha S. (Data Analyst) — SL
   1 Apr  Rohan V. — CL
   1 Apr  [3 others on leave] — [+3 more ▼]
  15 Apr  HOLIDAY — Ram Navami
```

- Holidays shown with orange background
- Multiple leaves on same day: grouped with "[+N more ▼]" expand
- Filter by division to see team-specific leave calendar
- **Division managers can view their team's calendar** via their own portal navigation (not Division O exclusive — configurable access)

---

## Analytics Tab

### Leave Consumption Trend

Stacked bar chart — 12 months of leave consumption by type (CL, SL, EL, ML, LOP).

- X-axis: month labels
- Y-axis: total days consumed
- Colour per leave type
- Hover tooltip: month · type · days · % of total

### Division-wise Leave Distribution

Horizontal bar chart — total leave days consumed per division (last 6 months). Helps identify divisions with high absence rates.

### Absenteeism Rate Trend

Line chart — monthly absenteeism rate = `LOP days / total working days across all employees × 100`. Reference line at 2% (EduForge threshold).

### Top Leave Consumers

Table — employees with highest total leave consumption in current FY. HR Manager only (sensitive — not shown to HRBP).

---

## Holiday Master Management

Accessible via [Manage Holidays] button (HR Manager only).

```
  EduForge Holiday Calendar — FY 2025-26
  ─────────────────────────────────────────────────────────────────────
  Date        Holiday Name                 Type            Applicable To
  26 Jan 2026  Republic Day               NATIONAL         All locations
  14 Mar 2026  Holi                       OPTIONAL/BANK    All locations
  25 Mar 2026  Holi (declared holiday)    DECLARED         All locations
  14 Apr 2026  Dr. Ambedkar Jayanti       NATIONAL         All locations
  09 Aug 2026  Muharram                   RESTRICTED       Hyderabad, Delhi
  15 Aug 2026  Independence Day           NATIONAL         All locations
```

Types:
- NATIONAL: mandatory for all locations (bank holiday)
- DECLARED: EduForge-declared full holiday
- RESTRICTED: location-specific (e.g., state-specific festivals)
- OPTIONAL: employee can take or not (counted as CL if taken)

[+ Add Holiday]: date, name, type, applicable locations. Duplicate date guard (warns if date already has a holiday).
[Edit] / [Delete]: Holiday deletion blocked if any employee has approved leave on that date — must revoke those leaves first.

Holiday list visible to all employees at `/hr/holidays/` (public within company intranet).

---

## Employee Self-Service: `/hr/my-leave/`

Brief companion spec (not Division O gated — all employees access):

| Feature | Description |
|---|---|
| Apply Leave | Form: leave type, dates, reason. Validates against available balance before submission |
| My Leave Balances | Card view of all leave type balances for current FY |
| My Leave History | Paginated history of all leave requests with status |
| My Attendance Calendar | Monthly calendar of own attendance records |
| Cancel Leave | Can cancel PENDING requests; APPROVED requests can be cancelled up to 1 day before start date |
| Comp Off Request | Log overtime/holiday work → request Comp Off with approval from HR Manager |
| My Payslips | Own payslips for last 36 months — PDF download |

Route guard: `@login_required` — no Division O membership required.

---

## Empty States

| Condition | Message |
|---|---|
| No pending requests | "No pending leave requests. All approvals up to date." with green checkmark |
| No employees on leave today | "No employees on approved leave today." |
| No LOP days this month | "No LOP days recorded for [month]." |
| No upcoming leaves (calendar) | "No approved leaves in the next 30 days." |
| No holidays configured for FY | "Holiday calendar not yet set for FY [year]. [Add Holidays →]" with amber warning |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Leave approved | "[Name]'s [type] leave approved ([dates])." | Green |
| Leave rejected | "[Name]'s leave rejected. Reason sent." | Amber |
| LOP marked | "[N] LOP days marked for [Name] for [month]." | Amber |
| Holiday added | "[Holiday name] added to holiday calendar." | Green |
| Leave cancelled by employee | "[Name] cancelled [type] leave for [dates]." | Blue (info) |
| Auto-approval triggered | "[Name]'s [type] leave auto-approved (3+ days pending)." | Blue (info) |

---

## Authorization

**Route guard:** `@division_o_required(allowed_roles=[79, 80, 81, 105, 106, 107])` for `/hr/leave/`. All roles see only:
- HR Manager (#79): full access — all employees, all actions
- HR Business Partner (#106): all employees' leave requests and balances (read-only; no approve/reject — HR Manager only approves)
- Payroll Exec (#105): attendance tab + LOP report only (for payroll input)
- Recruiter (#80), L&D Coordinator (#107), Office Admin (#81): own records only (redirect to `/hr/my-leave/`)

| Scenario | Behaviour |
|---|---|
| [Approve] / [Reject] | HR Manager (#79) only |
| [Manage Holidays] | HR Manager (#79) only |
| [Export LOP Report] | HR Manager + Payroll Exec (#105) |
| Analytics — Top Leave Consumers | HR Manager (#79) only |
| All employees attendance grid | HR Manager + HRBP (#106) |

---

## WFH Self-Mark Workflow

EduForge operates a hybrid work policy. Employees self-mark WFH days via `/hr/my-leave/` — no manager approval required.

### Self-Mark Flow

```
  Employee action (via /hr/my-leave/):
  ────────────────────────────────────────────────────────────
  [Mark Today as WFH]  →  creates hr_attendance_record row:
                          date = today, employee = self,
                          mode = 'WFH', source = 'SELF_MARK'
                          (allowed until 11:59 PM same day)

  Retroactive self-mark allowed for D-1 only (yesterday):
  [Mark Yesterday as WFH]  →  available until 10:00 AM next day
```

### Rules

| Rule | Detail |
|---|---|
| No approval required | WFH self-mark is automatic — no HR Manager action |
| Retroactive window | D-1 only, closes at 10:00 AM of the following day |
| Cannot WFH on leave days | If approved leave exists for the date → WFH mark blocked with: "You have approved leave on this date." |
| Cannot WFH on public holidays | `hr_holiday` check — WFH mark on a declared holiday blocked |
| HR Manager override | HR Manager can override `mode` on any attendance record (via attendance grid [Edit] cell). Override recorded with `source='HR_OVERRIDE'` and reason required |
| WFH limit (optional policy) | HR Manager can configure max WFH days/month per grade in `hr_policy_config`. If employee exceeds limit → self-mark rejected with: "WFH limit of [N] days/month reached." |

### Attendance Grid Display

- WFH day cell shows **W** (blue badge) vs **O** (office, green) vs **L** (leave, amber) vs **A** (absent/LOP, red)
- Monthly WFH count shown in attendance summary column
- HR Manager can filter attendance grid: `Mode = WFH` to review WFH patterns

---

## Half-Day LOP Clarification

Half-day leave deductions feed directly into payroll (O-05). Rules:

| Scenario | Deduction Formula |
|---|---|
| Full-day LOP | `gross_monthly / 26` per day |
| Half-day LOP (morning or afternoon) | `(gross_monthly / 26) × 0.5` |
| Same-day morning + afternoon half-day leave | Treated as 1 full-day LOP — `gross_monthly / 26` |
| Multiple half-day LOPs in month | Accumulated: `N × (gross_monthly / 26 × 0.5)` — rounded to 2 decimal places at payroll run |

**Half-day leave types:** CL, SL, and EL support half-day applications. ML, PL, COMP_OFF — full-day only.

**LOP Report to payroll:** The monthly LOP report (exported from Attendance tab) includes a `lop_days` column with fractional values (e.g., 1.5 for 3 half-days) — O-05 payroll run reads this as `lop_days` directly for deduction computation.

**26-day divisor rationale:** EduForge uses 26 (not calendar days) for monthly salary calculation — standard industry practice for monthly-rated employees. Sundays not counted as working days; second Saturdays are non-working (no "second Saturday working" variant).

---

## Role-Based UI Visibility Summary

| UI Element | HR Manager (#79) | HRBP (#106) | Payroll Exec (#105) | Recruiter (#80) | L&D Coord (#107) | Office Admin (#81) |
|---|---|---|---|---|---|---|
| Leave Requests tab (all employees) | Full (approve/reject) | Read-only | — (own only) | — (own only) | — (own only) | — (own only) |
| Balances tab (all employees) | Full | Read-only | — | — | — | — |
| Attendance tab (all employees) | Full | Read-only | Read-only (LOP only) | — | — | — |
| [Export LOP Report] | ✓ | — | ✓ | — | — | — |
| Calendar tab (all employees) | Full | Read-only | — | — | — | — |
| Analytics tab — all charts | ✓ | ✓ | — | — | — | — |
| Analytics — Top Leave Consumers | ✓ | — | — | — | — | — |
| [Manage Holidays] | ✓ | — | — | — | — | — |
| [Approve] / [Reject] leave | ✓ | — | — | — | — | — |
| Attendance grid [Edit] cell | ✓ | — | — | — | — | — |
| WFH override | ✓ | — | — | — | — | — |
| `/hr/my-leave/` (self-serve) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) | ✓ (own) |

---

## Performance Requirements

| Operation | Target | Notes |
|---|---|---|
| Leave requests list load | < 800ms P95 | With pagination (50/page) + Memcached 2 min TTL |
| Attendance grid render (monthly) | < 1.2s P95 | 150 employees × 31 days = 4,650 cells; Memcached 5 min TTL |
| Leave approve/reject HTMX | < 300ms P95 | Single row update via `?part=requests` |
| LOP report CSV export | < 5s | 150 employees × 1 month aggregate |
| Holiday master load | < 200ms P95 | Memcached 60 min TTL |
| Analytics charts | < 1.5s P95 | 12-month aggregates; Memcached 30 min TTL |
| `/hr/my-leave/` self-serve | < 500ms P95 | Employee's own records only; no role-scoping overhead |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `g v` | Go to Leave & Attendance page (`/hr/leave/`) |
| `t r` | Switch to Requests tab |
| `t b` | Switch to Balances tab |
| `t a` | Switch to Attendance tab |
| `t c` | Switch to Calendar tab |
| `a` | Approve selected leave request (HR Manager only) |
| `r` | Reject selected leave request (HR Manager only) |
| `/` | Focus search / filter input |
