# 03 — Mental Health Coordinator Dashboard

> **URL:** `/group/health/mental-health/`
> **File:** `03-mental-health-coordinator-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Mental Health Coordinator (Role 87, G3) — exclusive post-login landing

---

## 1. Purpose

Primary post-login landing for the Group Mental Health Coordinator. Central hub for monitoring counselling demand across all branches, tracking at-risk students, managing counsellor assignments, running exam stress intervention programs, and monitoring student wellbeing trends across the group.

The Mental Health Coordinator is responsible for the psychological welfare of 20,000–100,000 students distributed across 20–50 branches. Their work is preventive as well as responsive — they must ensure adequate counsellor-to-student ratios at every branch, proactively identify students in distress, and run structured programs during high-stress periods such as board exam preparation. Confidentiality is paramount — clinical notes and risk assessments are restricted to role-appropriate personnel only.

Scale: 50–500 counselling sessions/month during exam periods · 5–50 at-risk students under active management at any time · 2–10 programs running simultaneously.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Mental Health Coordinator | G3 | Full — all sections, all actions | Exclusive dashboard |
| Group Medical Coordinator | G3 | View only — summary metrics, no clinical details | Cannot see individual student risk data |
| Branch Principal | Branch G3 | View — own branch only, no clinical detail | Aggregate numbers only |
| All other roles | — | — | Redirected to own dashboard |

> **Access enforcement:** Django view decorator `@require_role('mental_health_coordinator')`.
> **Data sensitivity:** All student-level clinical data (risk assessment, session notes, intervention plans) is accessible only to Role 87 and authorised counsellors assigned to those students.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Health & Medical  ›  Mental Health Coordinator Dashboard
```

### 3.2 Page Header
```
Welcome back, [Coordinator Name]                 [Export Wellbeing Report ↓]  [Settings ⚙]
[Group Name] — Group Mental Health Coordinator · Last login: [date time]
AY [current academic year]  ·  [N] Branches  ·  [N] Sessions This Month  ·  [N] At-Risk Students Active
```

### 3.3 Alert Banner (conditional — items requiring priority action)

| Condition | Banner Text | Severity |
|---|---|---|
| Student flagged high-risk (immediate escalation) | "HIGH RISK: [Student] at [Branch] has been flagged as high-risk by [Counsellor]. Immediate review required." | Red |
| At-risk student follow-up overdue | "[N] at-risk students have overdue follow-up sessions. Most overdue: [Student] at [Branch] — [N] days." | Red |
| Branch with no counsellor assigned | "[Branch] has no counsellor assigned. [N] students have no access to counselling services." | Red |
| Session volume spike > 50% this week | "Session volume at [Branch] is [N]% above normal this week — possible exam stress surge. Investigate." | Amber |
| Program not started (scheduled start passed) | "Program '[Name]' at [Branch] was due to start on [date] but has not commenced." | Amber |
| Counsellor absence without backup | "Counsellor [Name] at [Branch] is absent today with no backup assigned." | Amber |

Max 5 alerts visible. "View all wellbeing events → Wellbeing Audit Log" always shown below alerts.

---

## 4. KPI Summary Bar (8 cards)

| Card | Metric | Colour Rule | Drill-down |
|---|---|---|---|
| Sessions This Month | Total counselling sessions logged group-wide | Blue always | → Section 5.1 |
| At-Risk Students (Active) | Students currently in active intervention | Green = 0 · Yellow 1–10 · Red > 10 | → Section 5.2 |
| Branches Without Counsellor | Branches with no assigned counsellor | Green = 0 · Yellow 1–2 · Red > 2 | → Section 5.1 |
| Exam Stress Cases This Week | Sessions categorised as exam/academic stress | Blue (informational; spikes to Amber > 20% of total) | → Section 5.3 |
| Sessions Completed vs Planned % | Actual vs scheduled sessions this month | Green ≥ 90% · Yellow 70–90% · Red < 70% | → Section 5.1 |
| Students Requiring Intervention | Flagged by counsellors as needing coordinator-level review | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.2 |
| Follow-ups Overdue | At-risk students with overdue scheduled sessions | Green = 0 · Yellow 1–5 · Red > 5 | → Section 5.2 |
| Programs Running This Month | Active wellbeing/counselling programs group-wide | Blue always | → Section 5.4 |

**HTMX:** `hx-trigger="every 5m"` → At-risk count and follow-ups overdue auto-refresh.

---

## 5. Sections

### 5.1 Branch Counselling Health Overview

> Per-branch summary of counselling service health — Coordinator's primary monitoring table.

**Search:** Branch name. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Counsellor Assigned | Radio | All / Assigned / Unassigned |
| At-Risk Count | Radio | All / Zero / 1–5 / > 5 |
| Follow-ups Overdue | Checkbox | Show branches with overdue follow-ups only |
| Program Running | Checkbox | Show branches with active program only |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Branch | ✅ | Link → `branch-wellbeing-detail` drawer |
| Counsellor Assigned | ✅ | Name(s) or ❌ None (Red) |
| Sessions This Month | ✅ | Count |
| Sessions Planned | ✅ | Planned count for this month |
| Completion % | ✅ | Colour-coded: Green ≥ 90% · Yellow 70–90% · Red < 70% |
| At-Risk Count | ✅ | Students currently in active intervention |
| Follow-ups Overdue | ✅ | Red badge if > 0 |
| Programs Active | ✅ | Count of running programs |
| Actions | ❌ | View · Assign Counsellor · View At-Risk |

**Default sort:** Follow-ups Overdue descending, then At-Risk Count descending.
**Pagination:** Server-side · 25/page.

---

### 5.2 At-Risk Student Monitor

> Students currently under active mental health intervention group-wide.

> **Confidentiality notice:** This table is visible only to Role 87. Student names are shown in full to the Coordinator; all other roles see aggregate counts only.

**Search:** Student name, branch, counsellor. 300ms debounce.

**Filters:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All branches |
| Risk Level | Checkbox | Low / Medium / High / Critical |
| Status | Checkbox | Active / Under Review / Stabilised / Escalated |
| Overdue | Checkbox | Show students with overdue next session only |
| Counsellor | Multi-select | All counsellors |

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Student Name | ✅ | Full name (Role 87 only; others see — ) |
| Branch | ✅ | |
| Class | ✅ | Grade + Section |
| Risk Level | ✅ | Colour badge: Low (Grey) / Medium (Yellow) / High (Orange) / Critical (Red) |
| Last Session | ✅ | Date; Red if > 14 days ago and still active |
| Next Scheduled | ✅ | Upcoming session date; Red if overdue |
| Counsellor | ✅ | Assigned counsellor name |
| Status | ✅ | Active / Under Review / Stabilised / Escalated |
| Actions | ❌ | View Profile · Log Session · Escalate |

**Default sort:** Risk Level descending (Critical first), then Next Scheduled ascending.
**Pagination:** Server-side · 25/page.

---

### 5.3 Session Volume Trend

> Visual bar chart: weekly session counts for the past 12 weeks, split by session type.

**Chart type:** Stacked bar chart — one bar per week.
**Series (colour-coded):**
- Academic Stress (Blue)
- Personal / Family (Orange)
- Social / Peer (Green)
- Hostel / Residential (Purple)
- Grief / Bereavement (Grey)
- Other (Light Grey)

**Interactions:**
- Hover on bar segment → tooltip shows week dates + type count + total
- Click bar → filter Section 5.1 table to that week's data
- Toggle: Group-wide / By Branch (branch selector dropdown appears when By Branch is active)

**Below chart:** Key stats row — Highest week: [date range] · [N] sessions · Primary category: [type]

**HTMX:** Chart data loads on page load via `hx-get` partial; updates with branch toggle.

---

### 5.4 Upcoming Program Events

> Mental health and wellbeing programs and workshops scheduled in the next 30 days across all branches.

**Columns:**
| Column | Sortable | Notes |
|---|---|---|
| Program Name | ✅ | e.g., "Exam Stress Management Workshop" |
| Branch | ✅ | |
| Type | ✅ | Workshop / Awareness Session / Group Therapy / Peer Support / Parent Session |
| Target Group | ✅ | e.g., Grade 10–12 / All Students / Hostellers |
| Date | ✅ | Upcoming date |
| Time | ✅ | |
| Facilitator | ✅ | Counsellor or external expert |
| Status | ✅ | Scheduled / Confirmed / Cancelled |
| Actions | ❌ | View · Edit · Cancel |

**Default sort:** Date ascending (soonest first).
No pagination (max 30-day window, typically < 20 rows).

---

### 5.5 Quick Actions

| Action | Target |
|---|---|
| Schedule Counselling Session | Opens `session-schedule` modal (branch, counsellor, student, date/time, type) |
| Add At-Risk Flag | Opens `at-risk-flag` drawer — search student, set risk level, assign counsellor, initial notes |
| Create Program | Opens `program-create` drawer — name, type, branch, dates, facilitator, target group |
| Export Wellbeing Report | Download CSV/XLSX — sessions, at-risk summary, program completion |
| View All At-Risk Students | → Full at-risk register (Section 5.2 expanded) |

---

## 6. Drawers

### 6.1 Drawer: `student-wellbeing-detail`
- **Trigger:** Actions → View Profile on at-risk student row
- **Width:** 640px
- **Tabs:** Sessions History · Risk Assessment · Intervention Plan · Notes

**Sessions History tab:**
- Table: date, type, counsellor, duration, outcome, follow-up required
- Most recent 20 sessions; paginated
- "Add Session" button (for Coordinator and assigned counsellor)

**Risk Assessment tab:**
- Current risk level (dropdown to update)
- Risk category: Academic / Social / Family / Mental Health Diagnosis / Other
- Initial flagging date and who flagged
- Assessment notes (structured fields: presenting concern, background factors, protective factors)
- Risk level change history (audit log: previous level, changed by, date, reason)

**Intervention Plan tab:**
- Assigned counsellor
- Intervention type: Individual Sessions / Group Support / Referral to Specialist / Parent Counselling
- Frequency: Weekly / Fortnightly / Monthly
- Goals (free text)
- Review date
- External referral (if applicable): specialist name, hospital, referral date, status

**Notes tab:**
- Confidential notes log (chronological)
- Each entry: date, author, note text
- "Add Note" button — text area with submit
- Notes visible to Role 87 and assigned counsellor only

### 6.2 Drawer: `at-risk-flag`
- **Trigger:** Quick Action: Add At-Risk Flag
- **Width:** 560px
- **Fields:** Student lookup (type-ahead) · Branch (auto-filled from student) · Risk Level (radio: Low/Medium/High/Critical) · Presenting Concern (text) · Flagged by (auto: current user) · Assign Counsellor (select) · Initial notes (textarea) · Notify (toggle: notify branch principal — aggregate only, no clinical detail)

### 6.3 Drawer: `program-create`
- **Trigger:** Quick Action: Create Program
- **Width:** 580px
- **Fields:** Program Name · Type (select) · Branch (multi-select) · Target Group (text) · Start Date · End Date · Sessions Planned (number) · Facilitator (select from counsellor registry or free text for external) · Description · Materials upload (optional)

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| At-risk flag added | "At-risk flag created for [Student] at [Branch]. Assigned to [Counsellor]." | Success | 5s |
| Risk level updated | "Risk level updated for [Student] — now [Level]." | Info | 4s |
| Session logged | "Counselling session logged for [Student] at [Branch]." | Success | 4s |
| Program created | "Program '[Name]' created for [Branch]." | Success | 4s |
| Program cancelled | "Program '[Name]' cancelled at [Branch]." | Warning | 5s |
| Escalation triggered | "High-risk alert for [Student] escalated to Group Medical Coordinator." | Warning | 6s |
| Counsellor assigned | "Counsellor [Name] assigned to [Branch]." | Success | 4s |
| Wellbeing report exported | "Wellbeing report export ready. Download now." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No at-risk students | "No Students Currently At-Risk" | "No students have active mental health intervention flags across any branch." | — |
| No sessions this month | "No Sessions Logged Yet" | "No counselling sessions have been logged this month." | — |
| No upcoming programs | "No Programs in Next 30 Days" | "No mental health programs are scheduled in the next 30 days." | [Create Program] |
| Branch search no results | "No Branches Found" | "No branches match your filters." | [Clear Filters] |
| At-risk search no results | "No Students Match Search" | "No at-risk students match your search criteria." | [Clear Search] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page load | Skeleton: 8 KPI cards + branch overview table + at-risk table + chart placeholder + program list + alerts |
| Branch overview filter/search | Inline table skeleton (8 rows × 9 columns) |
| At-risk table filter | Inline table skeleton (6 rows × 9 columns) |
| Session trend chart load | Rectangular chart skeleton with shimmer (400px × 200px) |
| Student wellbeing drawer | 640px drawer skeleton; each tab loads lazily on click |
| At-risk flag drawer | 560px form skeleton |
| KPI auto-refresh | Shimmer on card values only |

---

## 10. Role-Based UI Visibility

| Element | Mental Health Coordinator G3 | Medical Coordinator G3 | Branch Principal (own branch) |
|---|---|---|---|
| View Student Names (at-risk) | ✅ | ❌ (counts only) | ❌ (counts only) |
| View Session Notes | ✅ | ❌ | ❌ |
| View Risk Assessment | ✅ | ❌ | ❌ |
| View Intervention Plans | ✅ | ❌ | ❌ |
| Add At-Risk Flag | ✅ | ❌ | ❌ |
| Update Risk Level | ✅ | ❌ | ❌ |
| Create Program | ✅ | ❌ | ❌ |
| Assign Counsellor | ✅ | ❌ | ❌ |
| View Branch Session Counts | ✅ | ✅ | ✅ (own branch) |
| Export Wellbeing Report | ✅ | ❌ | ❌ |
| Escalate High-Risk Student | ✅ | ❌ | ❌ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/health/mental-health/dashboard/` | JWT (Role 87) | Full dashboard data payload |
| GET | `/api/v1/group/{group_id}/health/mental-health/kpi-cards/` | JWT (Role 87) | KPI auto-refresh values |
| GET | `/api/v1/group/{group_id}/health/mental-health/branch-overview/` | JWT (Role 87) | Branch counselling health table |
| GET | `/api/v1/group/{group_id}/health/mental-health/at-risk/` | JWT (Role 87) | At-risk student list (clinical access) |
| POST | `/api/v1/group/{group_id}/health/mental-health/at-risk/` | JWT (Role 87) | Create at-risk flag |
| PATCH | `/api/v1/group/{group_id}/health/mental-health/at-risk/{id}/` | JWT (Role 87) | Update risk level or status |
| GET | `/api/v1/group/{group_id}/health/mental-health/at-risk/{id}/` | JWT (Role 87) | Full student wellbeing detail |
| POST | `/api/v1/group/{group_id}/health/mental-health/at-risk/{id}/escalate/` | JWT (Role 87) | Escalate to Medical Coordinator |
| GET | `/api/v1/group/{group_id}/health/mental-health/session-trend/` | JWT (Role 87) | 12-week session trend data |
| GET | `/api/v1/group/{group_id}/health/mental-health/programs/` | JWT (Role 87) | Upcoming program events |
| POST | `/api/v1/group/{group_id}/health/mental-health/programs/` | JWT (Role 87) | Create new program |
| PATCH | `/api/v1/group/{group_id}/health/mental-health/programs/{id}/` | JWT (Role 87) | Update/cancel program |
| GET | `/api/v1/group/{group_id}/health/mental-health/export/` | JWT (Role 87) | Async wellbeing report export |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-get/post | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `.../mental-health/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Branch overview search | `input delay:300ms` | GET `.../branch-overview/?q={val}` | `#branch-table-body` | `innerHTML` |
| Branch overview filter | `click` | GET `.../branch-overview/?{filters}` | `#branch-table-section` | `innerHTML` |
| At-risk table filter | `click` | GET `.../at-risk/?{filters}` | `#at-risk-table-section` | `innerHTML` |
| At-risk search | `input delay:300ms` | GET `.../at-risk/?q={val}` | `#at-risk-table-body` | `innerHTML` |
| Load session trend chart | `load` | GET `.../session-trend/` | `#trend-chart-container` | `innerHTML` |
| Branch toggle on chart | `change` | GET `.../session-trend/?branch={id}` | `#trend-chart-container` | `innerHTML` |
| Open wellbeing drawer | `click` on student row | GET `.../at-risk/{id}/` | `#drawer-body` | `innerHTML` |
| Tab switch in drawer | `click` | GET `.../at-risk/{id}/?tab={name}` | `#drawer-tab-content` | `innerHTML` |
| Submit at-risk flag | `click` | POST `.../at-risk/` | `#at-risk-table-section` | `innerHTML` |
| Escalate student | `click` | POST `.../at-risk/{id}/escalate/` | `#at-risk-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
