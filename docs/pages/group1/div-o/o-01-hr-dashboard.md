# O-01 — HR Dashboard

**Route:** `GET /hr/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** HR Manager (#79)
**Also sees (restricted strips):** HR Business Partner (#106) — performance + headcount; Recruiter (#80) — recruitment strip; Payroll & Compliance Executive (#105) — payroll + compliance strip; L&D Coordinator (#107) — L&D strip; Office Administrator (#81) — asset + facilities strip

---

## Purpose

Morning command view for the HR Manager. At 100–150 employees across multiple divisions and cities, HR operations generate constant noise — pending approvals, upcoming compliance deadlines, hiring decisions, payroll windows, and review cycle timelines all compete for attention. This page answers the question "what needs my action today?" without navigating to 7 separate sub-pages. Each role sees only their domain strip, eliminating the need for a separate dashboard per HR sub-function.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `hr_employee` counts + `hr_leave_request` pending counts + `hr_payroll_run` latest status + `hr_position` open counts | 5 min |
| Headcount by division chart | `hr_employee` GROUP BY department WHERE status='ACTIVE' | 30 min |
| Attrition trend chart | `hr_employee` WHERE status='EXITED' GROUP BY month (last 12 months) + headcount snapshot | 60 min |
| Statutory compliance strip | `hr_statutory_filing` WHERE due_date <= today+30d OR status='OVERDUE' ORDER BY due_date ASC | 5 min |
| Pending approvals panel | `hr_leave_request` WHERE status='PENDING' + `hr_offer` WHERE offer_status='DRAFT' (pending HR Manager sign-off) + `hr_pip` WHERE status='PENDING_APPROVAL' | 2 min |
| Upcoming joiners | `hr_offer` WHERE offer_status='ACCEPTED' AND expected_join_date BETWEEN today AND today+30d | 10 min |
| Upcoming exits | `hr_employee` WHERE status='ON_NOTICE' ORDER BY last_working_date ASC | 10 min |
| Recruitment strip | `hr_position` WHERE current_status='OPEN' + `hr_candidate` pipeline counts per position | 10 min |
| Payroll status strip | `hr_payroll_run` WHERE month_year=current_month + `hr_statutory_filing` upcoming filings this month | 5 min |
| L&D strip | `hr_training_enrollment` WHERE completion_status IN ('ENROLLED','IN_PROGRESS') + mandatory incomplete count | 15 min |
| Asset strip | `hr_asset` WHERE status='AVAILABLE' count + `hr_asset` WHERE assigned_to IN (upcoming joiners) flagged | 15 min |

Cache keys scoped to `(role_id, user_id)`. `?nocache=true` available to HR Manager (#79) only.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?nocache` | `true` | — | Bypass Memcached (HR Manager only) |
| `?period` | `this_month`, `last_month`, `this_quarter`, `this_fy` | `this_month` | Affects attrition trend period delta labels |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Auto-Refresh | Target ID |
|---|---|---|---|---|
| KPI strip | `?part=kpi` | Page load | 5 min | `#o1-kpi-strip` |
| Headcount chart | `?part=headcount_chart` | Page load | 30 min | `#o1-headcount-chart` |
| Attrition trend | `?part=attrition_trend` | Page load + period change | 60 min | `#o1-attrition-trend` |
| Compliance strip | `?part=compliance_strip` | Page load | 5 min | `#o1-compliance-strip` |
| Pending approvals | `?part=pending_approvals` | Page load | 2 min | `#o1-pending-approvals` |
| Upcoming joiners | `?part=joiners` | Page load | 10 min | `#o1-joiners` |
| Upcoming exits | `?part=exits` | Page load | 10 min | `#o1-exits` |
| Recruitment strip | `?part=recruitment_strip` | Page load | 10 min | `#o1-recruitment-strip` |
| Payroll strip | `?part=payroll_strip` | Page load | 5 min | `#o1-payroll-strip` |
| L&D strip | `?part=ld_strip` | Page load | 15 min | `#o1-ld-strip` |
| eNPS/Culture Survey strip | `?part=enps_strip` | Page load | 30 min | `#o1-enps-strip` |
| Asset strip | `?part=asset_strip` | Page load | 15 min | `#o1-asset-strip` |

All parts respond with HTML fragments only. Non-primary roles receive only their permitted strip(s); all other parts return HTTP 204 No Content.

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  HR Dashboard   Period: [This Month ▼]               [?nocache]    │
├────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (6 tiles)                                               │
├──────────────────────────┬─────────────────────────────────────────┤
│  HEADCOUNT BY DIVISION   │  ATTRITION TREND (12 months, line)     │
│  (horizontal bar chart)  │                                         │
├──────────────────────────┴─────────────────────────────────────────┤
│  STATUTORY COMPLIANCE STRIP (upcoming deadlines, this month)       │
├──────────────────────────┬─────────────────────────────────────────┤
│  PENDING APPROVALS       │  UPCOMING JOINERS + UPCOMING EXITS      │
├──────────────────────────┴─────────────────────────────────────────┤
│  RECRUITMENT STRIP  │  PAYROLL STRIP  │  L&D STRIP  │  ASSET STRIP │
└─────────────────────┴─────────────────┴─────────────┴──────────────┘
```

> Non-primary roles see only their relevant strip(s). All other sections are suppressed server-side — no hidden DOM elements sent.

---

## KPI Strip (6 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 112          │ │ 8            │ │ 4            │ │ 3            │ │ 7            │ │ 94.2%        │
│ Active       │ │ Open         │ │ Pending      │ │ Joining      │ │ On Notice    │ │ Attendance   │
│ Employees    │ │ Positions    │ │ Leave Reqs   │ │ This Month   │ │              │ │ Rate (today) │
│ ↑3 vs last m.│ │ ↓2 filled    │ │ 1 > 3d wait  │ │ 2 this week  │ │ 3 this month │ │ Target ≥ 90% │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**Tile 1 — Active Employees:** `COUNT(hr_employee) WHERE status='ACTIVE'`. Delta vs prior month. Clicking opens O-02. Green if growing, grey if flat, amber if declining.

**Tile 2 — Open Positions:** `COUNT(hr_position) WHERE current_status='OPEN'`. Sub-label: "N filled this month". Clicking opens O-03?status=open.

**Tile 3 — Pending Leave Requests:** `COUNT(hr_leave_request) WHERE status='PENDING'`. Sub-label: "N > 3d wait" (pending > 3 working days without action). Red sub-label if any > 3 days. Clicking opens O-06?status=pending.

**Tile 4 — Joining This Month:** `COUNT(hr_offer) WHERE offer_status='ACCEPTED' AND EXTRACT(MONTH FROM expected_join_date)=current_month`. Sub-label: "N this week". Clicking opens O-04?tab=onboarding.

**Tile 5 — On Notice:** `COUNT(hr_employee) WHERE status='ON_NOTICE'`. Sub-label: "N exiting this month". Amber if > 5% of headcount on notice simultaneously. Clicking opens O-04?tab=offboarding.

**Tile 6 — Today's Attendance Rate:** `COUNT(hr_attendance_record WHERE date=today AND mode IN ('OFFICE','WFH')) / COUNT(hr_employee WHERE status='ACTIVE' AND is_holiday=false) × 100`. Green if ≥ 90%, amber if 80–89%, red if < 80%. Clicking opens O-06?tab=attendance.

**Loading state:** Shimmer animation during HTMX load. Stale values retained with grey border + "↻ Retry" on auto-refresh failure.

---

## Headcount by Division Chart

Horizontal bar chart (Chart.js) — current active headcount per division.

- **X-axis:** headcount (0 to max, integer)
- **Y-axis:** division labels (A–O)
- **Bars:** colour-coded by division tier: Engineering-tier (C, D, E) in blue-500; Operations-tier (F, G, H, I, J) in green-500; Business-tier (K, L, M, N, O, A, B) in purple-500
- **Each bar:** shows count label inline (e.g., "14")
- **Total label:** "Total: 112 active employees" above chart
- **Hover tooltip:** division name · headcount · % of total · open positions in division

**Visible to:** HR Manager (#79), HR Business Partner (#106).

---

## Attrition Trend Chart

Line chart — 12 months of monthly attrition rate.

- **Primary line (solid red-400):** Attrition rate = (exits in month / avg headcount) × 100
- **Secondary bars (right Y-axis, grey-200):** headcount at month end
- **Reference line:** dashed amber at 2% monthly attrition (24% annualised — industry benchmark for tech startups; EduForge target: < 1.5%/month)
- **X-axis:** month labels (MMM YY)
- **Left Y-axis:** attrition % (0–10%)
- **Right Y-axis:** headcount (0–200)
- **Hover tooltip:** month · exits count · joiners count · net headcount change · attrition rate
- **Null months:** show 0% (not a gap — 0 attrition is valid data)
- **YTD attrition:** shown as annotation label in top-right corner: "YTD: 8.4% (annualised)"
- **Exit reason breakdown toggle:** HRBP (#106) sees additional toggle "By reason" — stacks exits by category (RESIGNATION/TERMINATION/END_OF_CONTRACT/MUTUAL_SEPARATION/RETIREMENT)

**Visible to:** HR Manager (#79), HR Business Partner (#106).

---

## Statutory Compliance Strip

Upcoming and overdue statutory filings for the current month and next 30 days.

```
  ⚠ TDS Deposit (Mar 2026)      Due: 7 Apr 2026   (in 17 days)   UPCOMING   [View →]
  ⚠ PF ECR (Mar 2026)           Due: 15 Apr 2026  (in 25 days)   UPCOMING   [View →]
  ⚠ ESI Challan (Mar 2026)      Due: 15 Apr 2026  (in 25 days)   UPCOMING   [View →]
    PT Challan — Karnataka       Due: 10 Apr 2026  (in 20 days)   UPCOMING   [View →]
    PT Challan — Telangana       Due: 10 Apr 2026  (in 20 days)   UPCOMING   [View →]
    Quarterly TDS Return (Q4)   Due: 31 May 2026  (in 71 days)   UPCOMING   —
```

- Red row: overdue or < 3 days
- Amber row: ≤ 7 days to deadline
- Status badges: UPCOMING (grey) · IN_PROGRESS (blue) · FILED (green) · ACKNOWLEDGED (teal) · OVERDUE (red)
- [View →] links to O-05 with that filing pre-selected
- [View all →] at bottom links to O-05?tab=filings

**Visible to:** HR Manager (#79) full; Payroll & Compliance Executive (#105) full.

---

## Pending Approvals Panel

Consolidated pending actions requiring HR Manager input.

```
  Pending Actions: 6

  LEAVE REQUEST   Rohan Verma (Backend Eng.)    CL 24–25 Mar   Pending 4d   [Approve] [Reject]
  LEAVE REQUEST   Priya S. (SME Math)           SL 22 Mar      Pending 1d   [Approve] [Reject]
  OFFER APPROVAL  Ananya K. → L2 Support Eng.   CTC: ₹8.2L    [Review Offer]
  PIP APPROVAL    HRBP initiated for            [Employee #E-041]    [Review PIP]
  LEAVE REQUEST   3 more requests               [View all →]
```

- Leave requests: inline approve/reject with HTMX (no page reload). On approve: shows green toast; on reject: opens reason modal (mandatory reject reason stored in `hr_leave_request.rejection_reason`).
- Offer approval: opens O-03 offer drawer
- PIP approval: opens O-07 PIP drawer
- [View all →] links to the respective sub-page

**Visible to:** HR Manager (#79) only.

---

## Upcoming Joiners + Upcoming Exits

Two-column panel.

**Left: Upcoming Joiners (next 30 days)**

```
  Joining this month: 4
  ─────────────────────────────
  Meera G.    Backend Engineer    Join: 1 Apr 2026    [Onboarding checklist →]
  Suresh B.   SME — Chemistry     Join: 7 Apr 2026    [Onboarding checklist →]
  Kavya R.    L2 Support Eng.     Join: 15 Apr 2026   —
  [View all →]
```

- [Onboarding checklist →]: links to O-04?employee_id={id}
- Amber highlight if join date is within 3 days and onboarding checklist not fully setup

**Right: Upcoming Exits (on notice)**

```
  On notice: 7   |   Exiting this month: 3
  ─────────────────────────────
  Ravi K.    DevOps Eng.     Last day: 25 Mar 2026   Exit checklist: 8/12 ✓   [View →]
  Neha S.    Data Analyst    Last day: 31 Mar 2026   Exit checklist: 3/12     [View →]
  [View all →]
```

- Red row if last working day is today or tomorrow and F&F not triggered
- [View →]: links to O-04?tab=offboarding&employee_id={id}

**Visible to:** HR Manager (#79) full; Office Administrator (#81) joiners panel only (for asset coordination).

---

## Recruitment Strip

```
  Open Positions: 8   |   Active Candidates: 34   |   Offers Pending: 2

  Backend Engineer (Div C)      5 candidates   Interview stage      [View →]
  SME — Biology (Div D)         3 candidates   Screening stage      [View →]
  L2 Support Engineer (Div I)   2 candidates   Offer stage          [View →]
  [View all positions →]
```

[View →] links to O-03?position_id={id}.

**Visible to:** HR Manager (#79) full; Recruiter (#80) full.

---

## Payroll Strip

```
  March 2026 Payroll
  Status: LOCKED — awaiting HR Manager approval
  ─────────────────────────────
  Processed: 112 employees   Gross: ₹1,24,80,000   Net: ₹1,08,22,000
  [Review & Approve Payroll]

  This month's filings:
  PF ECR        Due: 15 Apr   UPCOMING
  ESI Challan   Due: 15 Apr   UPCOMING
  TDS Deposit   Due: 7 Apr    UPCOMING
```

- [Review & Approve Payroll]: opens O-05 payroll run approval drawer
- Red if payroll status is DRAFT after the 10th of the month (late processing risk)

**Visible to:** HR Manager (#79) full; Payroll & Compliance Executive (#105) full.

---

## L&D Strip

```
  Mandatory Training Completion: 84%
  ─────────────────────────────
  POSH Awareness FY26    Overdue: 6 employees    [Send Reminder]
  Data Privacy FY26      Overdue: 3 employees    [Send Reminder]
  New hire induction     2 in progress           [View →]

  Upcoming sessions this month: 3
  AWS Advanced   15 Apr   8 enrolled   [View →]
```

[Send Reminder] triggers a notification to overdue employees via internal email. [View →] links to O-08.

**Visible to:** HR Manager (#79) full; L&D Coordinator (#107) full.

---

## eNPS / Culture Survey Strip

Shown only to HR Business Partner (#106) and HR Manager (#79).

```
  Last eNPS Pulse — Q1 2026 (Jan 2026)
  ─────────────────────────────────────────────────────────────
  eNPS Score: +42   Responses: 78/112 (69.6% response rate)
  Promoters: 51%  ·  Passives: 40%  ·  Detractors: 9%
  Next dispatch: 1 Apr 2026 (in 11 days)   [Preview Respondents →]

  Active survey: Culture Pulse Q1 2026
  Sent: 15 Mar 2026   Response rate: 42%   Deadline: 28 Mar   [Send Reminder]
```

- eNPS score colour: green if ≥ 40, amber if 20–39, red if < 20 (matches J-07 NPS convention)
- Response rate: amber if < 50%, red if < 30%
- [Send Reminder]: HRBP (#106) only → triggers O-18 survey reminder early (outside automated schedule)
- [Preview Respondents →]: links to O-07?tab=surveys (anonymous aggregate only — no individual names shown to HRBP)
- [View all →] links to O-07?tab=surveys

Data source: `hr_survey` + `hr_survey_response` aggregated. Cache: 30 min.

---

## Asset Strip

```
  Available assets: 12 laptops, 5 monitors, 8 access cards
  ─────────────────────────────
  4 joiners this month — asset pre-assignment needed:
  Meera G.   (join: 1 Apr)   Laptop: ✓ assigned   Access card: ⚠ not assigned   [Assign →]
  Suresh B.  (join: 7 Apr)   Laptop: ⚠ not assigned   [Assign →]
  ─────────────────────────────
  3 exits this month — asset returns pending:
  Ravi K.    Laptop: ⚠ not returned   [Mark Returned]
```

[Assign →] links to O-02 employee asset tab. [Mark Returned] opens inline confirm modal.

**Visible to:** HR Manager (#79); Office Administrator (#81) full.

---

## Empty States

| Section | Condition | Message |
|---|---|---|
| Pending approvals | No pending items | "No pending approvals — all clear." with green checkmark |
| Compliance strip | No filings due in 30 days | "No statutory filings due in the next 30 days." |
| Upcoming joiners | No accepted offers in next 30 days | "No joiners in the next 30 days." |
| Upcoming exits | No employees on notice | "No employees currently on notice." |
| Recruitment strip | No open positions | "No open positions." with [+ Create Position] button |
| L&D strip | All mandatory training complete | "All mandatory training completed for the period." with green shield |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| Leave approved (inline) | "[Employee name]'s leave approved." | Green |
| Leave rejected (inline) | "[Employee name]'s leave rejected." | Amber |
| `?nocache=true` used | "Cache bypassed — showing live HR data." | Blue (info) |
| Payroll approved | "March 2026 payroll approved by [user]. Disbursement queued." | Green |
| Training reminder sent | "Reminder sent to [N] employees for [course name]." | Blue |
| Asset marked returned | "[Asset serial] marked as returned from [employee]." | Green |

---

## Authorization

**Route guard:** `@division_o_required(allowed_roles=[79, 80, 81, 105, 106, 107])` applied to `HRDashboardView`.

| Scenario | Behaviour |
|---|---|
| Unauthenticated | Redirect to `/login/?next=/hr/` |
| Role not in allowed list | 403 redirect to `/403/` |
| HTMX part for non-permitted strip | Return HTTP 204 No Content |
| Pending approvals panel | Only rendered for HR Manager (#79) |
| Payroll strip | HR Manager (#79) full; Payroll Exec (#105) full; others: 204 |
| `?nocache=true` | Allowed only for #79; others: 403 |

---

## Role-Based UI Visibility Summary

| Element | 79 HR Mgr | 80 Recruiter | 81 Office Admin | 105 Payroll Exec | 106 HRBP | 107 L&D Coord |
|---|---|---|---|---|---|---|
| KPI strip (all 6 tiles) | Yes | Tile 2 only | Tile 6 only | Tile 3 (pay) | Tile 1+5 | — |
| Headcount chart | Yes | No | No | No | Yes | No |
| Attrition trend | Yes | No | No | No | Yes | No |
| Compliance strip | Yes | No | No | Yes | No | No |
| Pending approvals | Yes (full) | No | No | No | No | No |
| Upcoming joiners | Yes | Yes (own pipeline) | Yes (asset prep) | No | No | Yes (induction) |
| Upcoming exits | Yes | No | Yes (asset return) | No | Yes (exit interview) | No |
| Recruitment strip | Yes | Yes (full) | No | No | No | No |
| Payroll strip | Yes (full) | No | No | Yes (full) | No | No |
| L&D strip | Yes (full) | No | No | No | Yes (read) | Yes (full) |
| eNPS / Culture Survey strip | No | No | No | No | Yes (full) | No |
| Asset strip | Yes (full) | No | Yes (full) | No | No | No |
| [?nocache=true] | Yes | No | No | No | No | No |

---

## Performance Requirements

| Metric | Target | Notes |
|---|---|---|
| Initial page load (SSR) | < 2s P95 | All HTMX strips issued in parallel |
| KPI strip | < 600ms P95 (cache hit: 5 min) | |
| Pending approvals | < 500ms P95 (cache hit: 2 min) | Must be fresh — action-required panel |
| Compliance strip | < 400ms P95 | Statutory deadlines are hard time constraints |
| `?nocache=true` rebuild | < 6s | All parts re-fetched from DB |

---

## Keyboard Shortcuts

| Key | Action |
|---|---|
| `g` `h` | Go to HR Dashboard (O-01) |
| `g` `e` | Go to Employee Directory (O-02) |
| `g` `r` | Go to Recruitment Pipeline (O-03) |
| `g` `o` | Go to Onboarding & Offboarding (O-04) |
| `g` `p` | Go to Payroll & Compliance (O-05) |
| `g` `v` | Go to Leave & Attendance (O-06) |
| `g` `f` | Go to Performance Management (O-07) |
| `g` `l` | Go to Learning & Development (O-08) |
| `g` `a` | Go to Asset & Facilities (O-09) |
| `Esc` | Close open drawer or modal |
| `?` | Show keyboard shortcut help overlay |
