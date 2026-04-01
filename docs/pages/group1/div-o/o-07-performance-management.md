# O-07 — Performance Management

**Route:** `GET /hr/performance/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** HR Business Partner (#106)
**Also sees:** HR Manager (#79) — full access + calibration authority + PIP approval; Division managers — read-only for their own team's reviews, OKR input, and PIP involvement (via separate limited access, not Division O membership)

---

## Purpose

Structured performance management for all EduForge employees across OKR cycles, formal review cadences, calibration sessions, and Performance Improvement Plans. At 100–150 employees, informal feedback is unreliable — this page ensures every employee has documented OKRs, receives a formal mid-year and annual review, and that calibration decisions (ratings, increments, promotions) are consistent across divisions. The HRBP uses it daily during active review cycles; the HR Manager uses it for final calibration, increment approvals, and PIP oversight.

**Review cycle structure:**
- **Annual:** 1 April – 31 March (FY-aligned)
- **Mid-year checkpoint:** 1 October – 31 October (6-month progress review, no rating change)
- **Probation review:** At 3-month and 6-month marks from join date
- **Confirmation review:** At end of probation (typically 6 months) — outcome: CONFIRMED / EXTENDED / SEPARATED

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Cycle status strip | `hr_performance_cycle` WHERE status NOT IN ('ARCHIVED') | 5 min |
| OKR overview | `hr_okr_objective` JOIN `hr_okr_key_result` for active cycle | 5 min |
| Review completion progress | `hr_performance_review` GROUP BY status for active cycle | 5 min |
| PIP list | `hr_pip` WHERE status NOT IN ('CLOSED') | 2 min |
| Employee reviews | `hr_performance_review` JOIN `hr_employee` for selected cycle | 5 min |
| Calibration grid | `hr_performance_review` WHERE cycle_id=active AND calibration_rating IS NOT NULL | 5 min |
| OKR detail | `hr_okr_objective` + `hr_okr_key_result` for selected employee+cycle | No cache |
| Review detail | `hr_performance_review` single row + `hr_okr_objective` for employee + cycle | No cache |

Cache keys scoped to `(user_id, cycle_id)`.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `overview`, `okrs`, `reviews`, `calibration`, `pips`, `surveys`, `analytics` | `overview` | Active section |
| `?cycle_id` | UUID | latest active | Select review cycle |
| `?division` | A–O | `all` | Filter employees by division |
| `?employee_id` | UUID | — | Jump to specific employee's review/OKR |
| `?review_status` | `not_started`, `self_assessment`, `manager_review`, `calibration`, `completed` | `all` | Filter reviews by status |
| `?pip_status` | `active`, `closed`, `all` | `active` | Filter PIPs by status |
| `?export` | `ratings_csv`, `okr_summary_csv` | — | Export (HR Manager only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger | Target ID |
|---|---|---|---|
| Overview strip | `?part=overview` | Page load | `#o7-overview` |
| OKR table | `?part=okrs&cycle_id={id}` | Tab click + filter | `#o7-okr-table` |
| Reviews table | `?part=reviews&cycle_id={id}` | Tab click + filter | `#o7-reviews-table` |
| Calibration grid | `?part=calibration&cycle_id={id}` | Tab click | `#o7-calibration` |
| PIP list | `?part=pips` | Tab click | `#o7-pip-list` |
| OKR drawer | `?part=okr_drawer&employee_id={id}&cycle_id={id}` | Row click | `#o7-okr-drawer` |
| Review drawer | `?part=review_drawer&review_id={id}` | Row click | `#o7-review-drawer` |
| PIP drawer | `?part=pip_drawer&pip_id={id}` | Row click | `#o7-pip-drawer` |
| Create cycle modal | `?part=create_cycle_modal` | [+ New Cycle] click | `#modal-container` |
| Create PIP modal | `?part=create_pip_modal&employee_id={id}` | [Initiate PIP] click | `#modal-container` |
| OKR check-in modal | `?part=checkin_modal&kr_id={id}` | [Check In] button | `#modal-container` |

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────┐
│  Performance Management   Cycle: [FY 2025-26 Annual ▼]  [+ Cycle]   │
├──────────────────────────────────────────────────────────────────────┤
│  CYCLE STATUS STRIP (cycle phase, deadlines, completion progress)    │
├──────────────────────────────────────────────────────────────────────┤
│  [Overview] [OKRs] [Reviews] [Calibration] [PIPs]                   │
└──────────────────────────────────────────────────────────────────────┘
```

---

## Cycle Status Strip

```
┌──────────────────────────┐ ┌────────────────┐ ┌────────────────┐ ┌────────────────┐
│ FY 2025-26 Annual Review │ │ 64%            │ │ 82%            │ │ 2              │
│ Phase: Self-Assessment   │ │ OKRs with      │ │ Self-Assess    │ │ Active PIPs    │
│ Deadline: 31 Mar 2026    │ │ last check-in  │ │ Submitted      │ │                │
│ (in 10 days)             │ │ < 14 days      │ │ 92/112 emp.    │ │                │
└──────────────────────────┘ └────────────────┘ └────────────────┘ └────────────────┘
```

**Phase badge (cycle phases in order):**
1. OKR_SETTING (green) — start of cycle: employees set objectives
2. OKR_ACTIVE (blue) — cycle in progress: regular check-ins expected
3. SELF_ASSESSMENT (amber) — self-assessment window open
4. MANAGER_REVIEW (purple) — managers complete their assessments
5. CALIBRATION (red) — HRBP + HR Manager calibration sessions
6. RESULTS_COMMUNICATED (teal) — ratings communicated to employees
7. CLOSED (grey) — cycle archived

Deadline countdown: red if ≤ 3 days to current phase deadline.

---

## Overview Tab

```
┌──────────────────────────────────────────────────────────────────────┐
│  FY 2025-26 Annual Review — Progress Summary                         │
├──────────────────────────────────────────────────────────────────────┤
│  REVIEW COMPLETION by Division                                       │
│  A Executive     4/4   ████████████████ 100%                        │
│  C Engineering   18/22 ████████████░░░░  82%   [View incomplete →]  │
│  D Content       10/13 ████████████░░░░  77%   [View incomplete →]  │
│  ...                                                                 │
├──────────────────────────────────────────────────────────────────────┤
│  SELF-ASSESSMENT: 92 submitted / 20 pending                          │
│  MANAGER REVIEW:  61 submitted / 51 pending                          │
│  CALIBRATION:     0 completed  / 112 pending                         │
├──────────────────────────────────────────────────────────────────────┤
│  [Send Reminder to Pending Employees]  [Send Reminder to Managers]   │
└──────────────────────────────────────────────────────────────────────┘
```

[Send Reminder to Pending Employees]: HTMX POST → sends email to all employees who haven't submitted self-assessment. Toast: "Reminder sent to [N] employees." HRBP (#106) can send; HR Manager (#79) can send.

---

## OKRs Tab

### OKR Table

| Column | Description |
|---|---|
| Employee | Name + division |
| Objectives | Count of objectives set for this cycle |
| Avg Confidence | Average KR confidence across all KRs: ON_TRACK / AT_RISK / OFF_TRACK |
| Last Check-in | Days since last check-in. Red if > 14 days |
| Overall Progress | Estimated % completion (avg of all KR current/target ratios) |
| Actions | [View OKRs] [Nudge] |

Sorted by Last Check-in descending (most overdue first) by default.

[Nudge]: sends a nudge notification to the employee to perform a check-in. Throttled: max once per 7 days per employee.

### OKR Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Rohan Verma — OKRs — FY 2025-26 Annual                [×]      │
│  Last check-in: 8 Mar 2026 (13 days ago)   Overall: ~72%        │
├──────────────────────────────────────────────────────────────────┤
│  Objective 1 (weight: 50%): Improve backend API response time    │
│  Status: ON_TRACK                                                │
│  ─────────────────────────────────────────────────────────────  │
│  KR 1.1: Reduce P95 API latency from 450ms to < 200ms           │
│          Current: 280ms | Target: 200ms | Confidence: AT_RISK ⚠  │
│          [Check In]                                              │
│                                                                  │
│  KR 1.2: Achieve 99.9% uptime for exam day APIs                 │
│          Current: 99.95% | Target: 99.9% | Confidence: ON_TRACK ✓│
│          [Check In]                                              │
│  ─────────────────────────────────────────────────────────────  │
│  Objective 2 (weight: 30%): Launch exam result microservice     │
│  Status: ON_TRACK                                                │
│  ...                                                             │
│  ─────────────────────────────────────────────────────────────  │
│  Objective 3 (weight: 20%): Mentor 2 junior engineers           │
│  Status: OFF_TRACK ⚠                                            │
│  ...                                                             │
└──────────────────────────────────────────────────────────────────┘
```

[Check In] modal (HRBP or employee via self-serve at `/hr/my-performance/`):
```
  KR: Reduce P95 API latency < 200ms
  Current value*:  [280   ] ms   (was 310ms at last check-in)
  Confidence*:     [AT_RISK ▼]
  Notes:           [Working on query optimisation — should hit target by end of March]
  [Save Check-in]
```

Check-in stored in `hr_okr_key_result.current_value` + appended to check-in history (JSONB array).

### Create OKR (for employees via self-serve, HRBP during OKR_SETTING phase)

New objectives created only during OKR_SETTING phase or within first 2 weeks of a new joiner's start (even if mid-cycle). After OKR_SETTING phase closes, objectives are locked — only check-ins allowed.

OKR weights must sum to 100% (validation enforced on save). Minimum 2, maximum 5 objectives per employee per cycle.

---

## Reviews Tab

### Reviews Table

| Column | Description |
|---|---|
| Employee | Name + division + grade |
| Self-Assessment | Submitted / Not Started / In Progress |
| Manager Review | Submitted / Not Started / In Progress |
| Manager | Reporting manager name |
| Calibration Rating | EXCEPTIONAL / EXCEEDS / MEETS / BELOW / UNSATISFACTORY / — |
| Promoted | ✓ / — |
| Increment | % / — |
| Status | NOT_STARTED / SELF_ASSESSMENT / MANAGER_REVIEW / CALIBRATION / COMPLETED |
| Actions | [View Review] [Edit Calibration] (HRBP) [View OKRs] |

### Performance Review Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Rohan Verma — Annual Review FY 2025-26              [Close ×]  │
│  Backend Engineer · Division C · Grade L3 · 9 months at grade   │
├──────────────────────────────────────────────────────────────────┤
│  [Self Assessment] [Manager Review] [Calibration] [OKR Summary] │
└──────────────────────────────────────────────────────────────────┘
```

**Self Assessment tab:**

```
  What did you achieve this year? (OKR summary auto-populated):
  "Achieved 99.95% exam day uptime across 12 exam events..."

  Strength demonstrated:
  "Strong ownership of the exam day operations — proactively..."

  Development area:
  "Would benefit from more exposure to system design..."

  Support needed from manager:
  "Access to AWS certification training"

  Self-rating: MEETS_EXPECTATIONS
  Submitted: 20 Mar 2026
```

**Manager Review tab:**

```
  Manager: Arjun Kumar (CTO)
  ─────────────────────────────────────────────────────────
  Performance summary:
  "Rohan delivered consistently this year. The exam day work..."

  Strength demonstrated:
  "Exceptional reliability under pressure. Zero escalations..."

  Development area:
  "Should take more initiative on architecture decisions..."

  Manager rating: EXCEEDS_EXPECTATIONS
  Promotion recommended: Yes (to L4)
  Increment recommended: 15%
  Submitted: 25 Mar 2026
```

**Calibration tab (HRBP + HR Manager only):**

```
  Calibration Rating: [EXCEEDS_EXPECTATIONS ▼]
  Promotion approved: [☑ Yes]   New Designation: [Backend Eng. Sr. ▼]   New Grade: [L4 ▼]
  Increment approved: [15%  ]   Effective: [1 Apr 2026]
  Calibration Note:   "Peer comparison with Division C: consistent top performer."

  [Save Calibration]
```

Calibration changes trigger salary revision task in O-05 (Payroll Exec receives notification to update CTC in next payroll run).

**OKR Summary tab:** read-only pull from OKRs tab — objectives, KR completion, confidence at end of cycle.

---

## Calibration Tab

### 9-Box Calibration Grid

HRBP uses this to run calibration sessions. Plots all employees on a 3×3 grid:

```
  Performance →  BELOW   MEETS   EXCEEDS
  Potential
  HIGH     │  ◉ (2) │  ◉ (8) │  ⭐ (5) │  ← "Stars" — promote + stretch
           │        │        │        │
  MEDIUM   │  ◉ (4) │  ◉(32) │  ◉(18) │  ← Core performers
           │        │        │        │
  LOW      │  ⚠ (2) │  ◉(14) │  ◉ (4) │  ← ⚠ = PIP candidates
```

- Each dot represents an employee. Hover: name, designation, division, grade
- Click dot → opens Review Drawer for that employee
- ⚠ (red): employees in BELOW performance + LOW potential → strong PIP signal, displayed with amber/red marker
- Star (⭐): EXCEEDS + HIGH potential → key talent, retention watch
- Numbers in brackets = count per quadrant
- [Initiate PIP] button appears on hover over ⚠ employees
- [Export 9-Box PNG] → HR Manager only

Potential rating is set by the HRBP based on manager input + HRBP assessment. Stored in `hr_performance_review.potential_rating` (LOW/MEDIUM/HIGH).

### Distribution Summary

Below the grid, a summary bar:

```
  Rating Distribution — FY 2025-26 (112 employees)
  EXCEPTIONAL:      5 (4.5%)   ██
  EXCEEDS:         27 (24.1%)  ████████████
  MEETS:           64 (57.1%)  ████████████████████████████████
  BELOW:            9 (8.0%)   ████
  UNSATISFACTORY:   3 (2.7%)   █
  Not yet calibrated: 4
```

Normal distribution check: amber warning if EXCEPTIONAL > 10% (over-awarding risk) or BELOW + UNSATISFACTORY > 20% (systemic issue signal).

---

## PIPs Tab

### PIP List

| Column | Description |
|---|---|
| Employee | Name + designation |
| Division | Badge |
| Initiated By | HRBP name |
| Start Date | PIP start date |
| End Date | PIP end date (typically 60–90 days) |
| Duration | Days in PIP |
| Status | ACTIVE / CHECKPOINT_DUE / EXTENDED / IMPROVED / SEPARATED / CLOSED |
| Outcome | — or IMPROVED / SEPARATED |
| Actions | [View] [Add Checkpoint] [Close PIP] |

### Initiate PIP Modal (HRBP + HR Manager only — HR Manager must approve before sending)

```
┌──────────────────────────────────────────────────────────────────┐
│  Initiate Performance Improvement Plan                           │
├──────────────────────────────────────────────────────────────────┤
│  Employee*             [Search employee...              ▼]       │
│  Initiated By*         [HR Business Partner (auto)      ]        │
│  Reason for PIP*       [                                ]        │
│  (min 100 chars — must reference specific performance data)      │
│  PIP Start Date*       [2026-04-01                      ]        │
│  PIP Duration*         [90 days (ends: 30 Jun 2026)     ▼]       │
│  Improvement Goals*                                              │
│    Goal 1: [                                            ]        │
│    Goal 2: [                                            ] [+ Add] │
│  Checkpoint Schedule*  [Bi-weekly                       ▼]       │
│  Checkpoint 1 date:    [15 Apr 2026]  (auto-computed)            │
│  Checkpoint 2 date:    [29 Apr 2026]  ...                        │
│                                                                  │
│  ⚠ PIP initiation requires Legal Officer (#75) legal review for  │
│    TERMINATION-risk cases. Flag for legal review: [☐]            │
│                                                                  │
│  [Cancel]              [Save Draft]  [Submit for HR Manager Approval] │
└──────────────────────────────────────────────────────────────────┘
```

**HR Manager approval gate:** HRBP creates PIP draft → HR Manager reviews and approves. Only after approval does the employee's manager get notified to initiate the formal PIP conversation. This two-step prevents premature disclosure.

**Legal flag:** For cases where separation may be the outcome, the Legal Officer (#75) receives a notification to review the PIP documentation for legal compliance (wrongful termination risk).

### PIP Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  PIP — [Employee Name] (EF-XXXX)                      [Close ×]  │
│  Backend Engineer · Division C · Started: 1 Apr 2026            │
│  Duration: 90 days · Ends: 30 Jun 2026 · Status: ACTIVE         │
├──────────────────────────────────────────────────────────────────┤
│  Reason: "Consistent below-target delivery on API performance    │
│  objectives over Q3-Q4 FY2025-26. P95 latency target of 200ms   │
│  not met despite 2 prior coaching conversations."               │
├──────────────────────────────────────────────────────────────────┤
│  Goals:
│  1. Reduce P95 API latency to < 250ms by 30 Apr 2026
│  2. Complete AWS Advanced certification by 15 May 2026
│  3. Zero production incidents caused by own code in PIP period
│
│  Checkpoints:
│  ✓ 15 Apr 2026   CHECKPOINT_1   Met Goal 1 partially (280ms). Goals 2 in progress.
│  ○ 29 Apr 2026   CHECKPOINT_2   [Add Checkpoint]
│  ○ 13 May 2026   CHECKPOINT_3   Pending
│  ○ 30 Jun 2026   FINAL REVIEW   Pending
│
│  [Add Checkpoint]  [Extend PIP] (HR Manager only)  [Close PIP]
└──────────────────────────────────────────────────────────────────┘
```

[Add Checkpoint]: opens checkpoint modal:
```
  Checkpoint date: [29 Apr 2026]
  Goal 1 status:   [MET / PARTIALLY MET / NOT MET ▼]
  Goal 2 status:   [IN_PROGRESS ▼]
  Goal 3 status:   [MET ▼]
  Summary notes:   [                                     ]
  Recommendation:  [Continue PIP ▼]   (Continue PIP / Extend / Improve / Separate)
```

[Close PIP] → requires outcome selection: IMPROVED / SEPARATED / MUTUAL_SEPARATION. On SEPARATED: HR Manager and Legal Officer notified. Employee status updated to `ON_NOTICE` in O-02.

---

## Probation & Confirmation Reviews

Separate from annual cycle. Managed under the same page but with `cycle_type='PROBATION'` or `cycle_type='CONFIRMATION'`.

Triggered automatically by Task O-8 (14 days before 3-month and 6-month marks):

```
  Upcoming Probation Reviews
  ─────────────────────────────────────────────────────────
  Meera G.    Backend Eng.    3-month review due: 1 Jul 2026   [Create Review]
  Suresh B.   SME Chem.       3-month review due: 7 Jul 2026   [Create Review]
```

[Create Review]: opens simplified review form (no OKR scoring — just: Performance rating 1–5, Behaviour rating 1–5, Recommendation: CONFIRM / EXTEND_PROBATION / SEPARATE).

Outcome stored in `hr_performance_review.probation_outcome`. On CONFIRM: `hr_employee.probation_status='CONFIRMED'`. On EXTEND: new probation milestone created. On SEPARATE: exit initiated in O-04.

---

## Empty States

| Condition | Message |
|---|---|
| No active review cycle | "No active performance review cycle. [+ Create Cycle]" |
| No OKRs set for cycle | "No OKRs configured for this cycle. OKR setting window opens [date]." |
| No PIPs | "No active PIPs." with green checkmark |
| Calibration not started | "Calibration has not started for this cycle. Available from [manager review deadline + 1]." |
| No probation reviews due | "No probation reviews due in the next 30 days." |

---

## Toast Messages

| Action | Toast | Type |
|---|---|---|
| OKR check-in saved | "Check-in recorded for [KR title]." | Green |
| Reminder sent | "Reminder sent to [N] employees for self-assessment." | Blue |
| PIP created | "PIP initiated for [Name]. Awaiting HR Manager approval." | Amber |
| PIP approved | "PIP for [Name] approved. Manager notified." | Green |
| Checkpoint added | "Checkpoint recorded for [Name]'s PIP." | Green |
| Calibration saved | "Calibration rating saved for [Name]." | Green |
| Promotion approved | "[Name] approved for promotion to [Grade]. Payroll notified." | Green |

---

## Authorization

**Route guard:** `@division_o_required(allowed_roles=[79, 106])` applied to `PerformanceView`.

| Scenario | Behaviour |
|---|---|
| [Initiate PIP] | HRBP (#106) creates draft; HR Manager (#79) approves — two-step gate |
| Calibration edit | HRBP (#106) enters initial calibration; HR Manager (#79) finalises and locks |
| [Export ratings CSV] | HR Manager (#79) only |
| [Close PIP with SEPARATED outcome] | HR Manager (#79) only |
| 9-Box export | HR Manager (#79) only |
| Division managers | View-only their team's reviews via separate route `/hr/performance/team/` (requires login, not Division O membership) |

---

## eNPS & Culture Surveys

Owned by HR Business Partner (#106). Allows HRBP to create, dispatch, and analyse company-wide employee engagement surveys.

### Survey Types

| Type | Cadence | Description |
|---|---|---|
| eNPS (Employee Net Promoter Score) | Quarterly (Task O-17) | Single question: "On a scale of 0–10, how likely are you to recommend EduForge as a great place to work?" + 1 open-text follow-up |
| Culture Survey | Annual or ad-hoc | Multi-question survey on culture dimensions: values alignment, manager effectiveness, collaboration, growth opportunities, work-life balance |
| Pulse Survey | Ad-hoc (HRBP-triggered) | Short 3–5 question check-in for targeted topics (e.g., return-to-office, restructuring feedback) |

### eNPS Score Calculation

```
  eNPS = % Promoters (9–10) − % Detractors (0–6)
  Passives (7–8) excluded from score calculation

  Example:
    Total respondents: 98
    Promoters (9–10):  54  →  55.1%
    Passives (7–8):    32  →  32.7%
    Detractors (0–6):  12  →  12.2%
    eNPS = 55.1 − 12.2 = +42.9  →  displayed as +42
```

Score benchmark: > +30 = Good, > +50 = Excellent, < 0 = Needs urgent attention.

### Survey Creation

[+ Create Survey] button (HRBP + HR Manager only):

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Survey                                                   │
├──────────────────────────────────────────────────────────────────┤
│  Survey Type*     [eNPS / Culture / Pulse          ▼]            │
│  Title*           [Q1 2026 eNPS Survey               ]           │
│  Target audience* [All Employees / By Division ▼]  [Div C ▼]    │
│  Anonymity*       [☑ Anonymous (responses not linked to name)]   │
│  Launch Date*     [2026-04-01                        ]           │
│  Close Date*      [2026-04-14  (14-day window)       ]           │
│  Questions:                                                      │
│  [Auto-fill eNPS question template]  or  [+ Add Question]        │
│                                                                  │
│  Q1. [On a scale of 0–10, how likely are you to recommend...]    │
│      Type: [Rating 0–10 ▼]                                       │
│  Q2. [What is the primary reason for your score?         ]       │
│      Type: [Free text ▼]                                         │
│                                                                  │
│  [Cancel]                                [Save Draft]  [Launch]  │
└──────────────────────────────────────────────────────────────────┘
```

Stored in `hr_survey` table. On [Launch]: status → ACTIVE, Task O-17 dispatches email invite with unique survey link to each target employee.

### Survey Response Tracking

HTMX part `?part=survey_tracker` updates every 15 minutes:

```
  Q1 2026 eNPS Survey — Active
  ──────────────────────────────────────────────────────────────────
  Launched: 1 Apr 2026   Closes: 14 Apr 2026 (5 days remaining)
  Target: 112 employees
  Responded: 78 (69.6%)  ████████████████████░░░░░░░░░
  Pending:   34 (30.4%)

  [Send Reminder to Non-Respondents]  (throttled: max once per 3 days)
  Task O-18 auto-reminder: fires 7 days before close date
```

### Survey Results View (post-close)

Accessed via [View Results] after survey closes:

```
  eNPS Results — Q1 2026
  ──────────────────────────────────────────────────────────────────
  eNPS Score:  +42
  Promoters:   55.1%   ████████████████████████████
  Passives:    32.7%   ████████████████
  Detractors:  12.2%   ██████

  Trend:  Q4 2025: +38  →  Q3 2025: +35  →  Q2 2025: +41
  (Line chart — last 4 quarters)

  By Division:
  Div C (Engineering):   +51   [████████████████████████████████]
  Div D (Content):       +38   [█████████████████████░░░░░░░░░░░]
  Div I (Support):       +29   [████████████████░░░░░░░░░░░░░░░░]  ⚠ Below +30
  HR (Div O):            +60   [██████████████████████████████████]

  By Tenure:
  < 1 year:  +48
  1–3 years: +44
  > 3 years: +38

  Top open-text themes (anonymised):
  "Growth opportunities" mentioned by 23 respondents
  "Manager support" mentioned by 18 respondents
  "Work-life balance" mentioned by 12 respondents
```

**Anonymity guarantee:** Individual responses never shown to anyone except aggregates. If a segment has < 5 respondents, score is suppressed ("Insufficient responses to show breakdown").

### Culture Survey Questions (multi-dimension)

Culture surveys use a 5-point Likert scale (Strongly Disagree → Strongly Agree) across dimensions:

| Dimension | Sample Questions |
|---|---|
| Values Alignment | "EduForge's values align with my personal values" |
| Manager Effectiveness | "My manager gives me clear, actionable feedback" |
| Collaboration | "Teams across EduForge collaborate effectively" |
| Growth | "I have clear opportunities for career growth here" |
| Work-Life Balance | "I can maintain a healthy work-life balance at EduForge" |
| Inclusion | "I feel I belong at EduForge regardless of my background" |

Results shown as average score per dimension in a radar/spider chart (Chart.js).

### O-01 Dashboard Integration

eNPS strip on O-01 HR Dashboard (HRBP-visible, `?part=enps_strip`):
- Last eNPS score + trend arrow vs previous quarter
- Response rate for current active survey
- Next scheduled eNPS dispatch date (from Task O-17 cron)
- [View Full Results] → deeplinks to this section

---

## Salary Revision → O-05 Payroll Flow

When calibration is finalised in O-07, the salary change must be applied in O-05. The explicit flow:

```
  Step 1 (O-07):  HR Manager finalises calibration
                  → sets increment_pct and/or new_grade for employee
                  → hr_performance_review.calibration_status = 'LOCKED'

  Step 2 (O-07):  System creates hr_salary_revision_history record:
                  {
                    employee_id: <uuid>,
                    revision_type: 'ANNUAL_INCREMENT',
                    old_ctc: <current>,
                    new_ctc: <computed from increment_pct>,
                    effective_date: '2026-04-01',  ← first day of new FY
                    approved_by: <HR Manager user_id>,
                    source_review_id: <hr_performance_review.id>
                  }

  Step 3 (O-16):  Task O-16 (Salary Revision Notification) fires:
                  → Payroll Exec (#105) receives email:
                    "[N] salary revisions pending for April payroll run.
                     Review before running April payroll."

  Step 4 (O-05):  Payroll Exec opens O-05. "14 salary revisions pending"
                  alert shown at top of page. [Apply to Next Payroll Run]
                  → updates hr_employee.ctc and hr_employee.grade
                  → clears pending revision records

  Step 5 (O-05):  April payroll run picks up updated CTC for all revised
                  employees. Payslips reflect new gross = new CTC / 12.
```

**Mid-year off-cycle revision:** HRBP or HR Manager can initiate a standalone salary revision (not tied to annual review) via O-02 Employee Directory → Profile tab → [+ Add Salary Revision]. This creates a `hr_salary_revision_history` record with `revision_type='OFF_CYCLE'` and triggers O-16 immediately (not waiting for scheduled cron).

---

## `/hr/my-performance/` — Employee Self-Serve Spec

All employees access their own performance data. `@login_required` only — no Division O membership.

| Feature | Description |
|---|---|
| My OKRs | View own objectives and key results for active cycle. [Check-In] button per KR: update progress %, confidence (ON_TRACK / AT_RISK / OFF_TRACK), add check-in note |
| My Review Status | Card showing current review cycle status: "Self-assessment due by [date]" → [Start Self-Assessment] → multi-field form (achievements, strengths, development areas, support needed, self-rating). Once submitted, locked for editing |
| My Review History | Paginated list of past review cycles with final calibration rating (once published by HR Manager) |
| My OKR History | Historical OKR cycles — objective completion %, final confidence per KR |
| My PIP (if active) | Stripped-down PIP view: goals, checkpoint dates, status. Read-only — no edit capability for employee |

**OKR check-in flow:**
```
  Employee → [Check-In] on Key Result
  → Modal: Progress % (0–100), Confidence [ON_TRACK/AT_RISK/OFF_TRACK], Note (optional)
  → POST to /hr/my-performance/okr/{kr_id}/checkin/
  → Saves to hr_okr_key_result.check_in_history JSONB array:
    [{date, user_id, progress_pct, confidence, note}, ...]
  → HRBP can see all check-ins in O-07 OKR detail drawer
```

Route guard: `@login_required`. No minimum role — every active employee sees this.

---

## Role-Based UI Visibility Summary

| UI Element | HR Manager (#79) | HRBP (#106) |
|---|---|---|
| Overview tab — all employees | Full | Full |
| OKRs tab — view all employees | ✓ | ✓ |
| OKRs tab — edit employee OKRs | ✓ | ✓ |
| Reviews tab — view all reviews | ✓ | ✓ |
| Reviews tab — edit calibration | ✓ (finalise + lock) | ✓ (draft only) |
| Calibration tab — 9-Box Grid | ✓ (edit + export) | ✓ (edit) |
| PIPs tab — view all PIPs | ✓ | ✓ |
| [Initiate PIP] | ✓ (approve gate) | ✓ (draft + submit) |
| [Approve PIP] | ✓ | — |
| [Close PIP — SEPARATED] | ✓ | — |
| eNPS / Culture Surveys | ✓ | ✓ (primary owner) |
| [Export ratings CSV] | ✓ | — |
| [Export 9-Box PNG] | ✓ | — |
| Probation reviews | ✓ | ✓ |
| Salary revision → O-05 trigger | ✓ (from calibration lock) | — |
| `/hr/my-performance/` | ✓ (own records) | ✓ (own records) |

---

## Performance Requirements

| Operation | Target | Notes |
|---|---|---|
| Overview tab load | < 800ms P95 | Cycle status strip + completion progress; Memcached 5 min |
| OKR list for all employees | < 1s P95 | Paginated 50/page; Memcached 5 min scoped to `(user_id, cycle_id)` |
| 9-Box calibration grid render | < 1.5s P95 | 150 employees plotted; Chart.js scatter on canvas |
| Review drawer open | < 400ms P95 | Single employee review + OKR summary; no cache |
| OKR check-in save | < 300ms P95 | Append to JSONB array; HTMX swap |
| PIP detail drawer | < 400ms P95 | Checkpoint history + goals |
| eNPS results chart | < 1s P95 | Aggregate query; Memcached 30 min |
| Export ratings CSV (150 employees) | < 8s | Celery task for large cycles |
| `/hr/my-performance/` self-serve | < 500ms P95 | Own records only |

---

## Keyboard Shortcuts

| Shortcut | Action |
|---|---|
| `g f` | Go to Performance Management page (`/hr/performance/`) |
| `t o` | Switch to Overview tab |
| `t k` | Switch to OKRs tab |
| `t r` | Switch to Reviews tab |
| `t c` | Switch to Calibration tab |
| `t i` | Switch to PIPs tab |
| `n` | New OKR / New Review (context-aware — opens relevant create modal) |
| `/` | Focus search / filter input |
| `Esc` | Close drawer / modal |
