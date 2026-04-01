# 06 — Strategic Planning Officer Dashboard

> **URL:** `/group/analytics/strategy/`
> **File:** `06-strategic-planning-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Strategic Planning Officer (Role 107, G1) — exclusive post-login landing

---

## 1. Purpose

Primary post-login workspace for the Group Strategic Planning Officer. Serves as the intelligence hub for advising the Group CEO and Chairman on where, when, and how to expand. Aggregates growth signals (enrollment trends, geographic demand, competitor landscape), active feasibility studies, expansion plan milestones, and branch performance signals that flag candidates for intervention or acceleration. The officer does not manage day-to-day operations — they focus entirely on medium-term and long-term strategic analytics that shape the group's investment and expansion decisions.

Scale: Large groups target 1–3 new branches per year; small groups may go 2–3 years between expansions. The Strategic Planning Officer manages 3–10 active feasibility studies at any time and maintains one active 3-year expansion plan.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Strategic Planning Officer | 107 | G1 | Full — all sections, all strategic planning actions, export | Exclusive dashboard |
| Group Analytics Director | 102 | G1 | — | Has own dashboard `/group/analytics/director/` |
| Group MIS Officer | 103 | G1 | — | Has own dashboard `/group/mis/officer/` |
| Group Academic Data Analyst | 104 | G1 | — | Has own dashboard `/group/analytics/academic/` |
| Group Exam Analytics Officer | 105 | G1 | — | Has own dashboard `/group/analytics/exam/` |
| Group Hostel Analytics Officer | 106 | G1 | — | Has own dashboard `/group/analytics/hostel/` |
| All other roles | — | — | — | Redirected to own dashboard |

> **Access enforcement:** `@require_role('strategic_planning_officer')` on all views and API endpoints. G1 level — read-only on operational data from all other divisions; full CRUD on feasibility studies, expansion plans, and strategic notes.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Strategic Planning Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                    [+ New Feasibility Study]  [Export Strategic Report ↓]
[Group Name] — Strategic Planning Officer · Last login: [date time]
AY [current academic year]  ·  [N] Active Studies  ·  [N] Branches in Expansion Plan  ·  3-Year Plan: [Status badge]
```

`[+ New Feasibility Study]` — opens `feasibility-study-create` drawer. Role 107 only.
`[Export Strategic Report ↓]` — dropdown: Export to PDF / Export to XLSX. Role 107 only.

### 3.3 Alert Banners (conditional)

Stacked above KPI bar. Each individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Planned branch opening in < 90 days with milestones < 50% complete | "[N] planned branch(es) have an opening date within 90 days but less than 50% of milestones are completed." | Red |
| Expansion plan not yet created for current AY | "No 3-year expansion plan is active for this group. Create one to track expansion targets." | Red |
| Feasibility studies in Draft for > 45 days | "[N] feasibility study/studies have been in Draft status for more than 45 days. Review or update." | Amber |
| Studies Under Review for > 30 days with no decision | "[N] feasibility study/studies are under review for more than 30 days with no decision made." | Amber |
| Expansion plan due for annual review | "The current expansion plan was last reviewed more than 12 months ago. An annual review is due." | Amber |
| No active feasibility studies | "No feasibility studies are currently active. If expansion is planned, start a study." | Blue |

---

## 4. KPI Summary Bar

Six metric cards displayed horizontally. Auto-refresh every 5 minutes via HTMX polling.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Active Feasibility Studies | Studies with status Draft, Under Review, or Recommended | `FeasibilityStudy.objects.filter(status__in=['draft','under_review','recommended']).count()` | Indigo (neutral) | `#kpi-active-studies` |
| 2 | Expansion Plan Status | Status of the current active 3-year expansion plan | `ExpansionPlan.objects.filter(active=True).first().status` | Green = Approved/Active · Amber = Under Review · Red = No Plan | `#kpi-plan-status` |
| 3 | Branches in Current Plan | Count of planned new branches in the active expansion plan | `ExpansionPlanBranch.objects.filter(plan__active=True).count()` | Indigo (neutral) | `#kpi-plan-branches` |
| 4 | Milestones Overdue | Milestones past their target date and not completed | `Milestone.objects.filter(target_date__lt=today, status__in=['on_track','delayed']).count()` | Red if > 0 · Green = 0 | `#kpi-milestones-overdue` |
| 5 | Branches Flagged (Declining) | Branches with 3+ months of declining performance signals | `BranchSignal.objects.filter(signal_type='declining', months_count__gte=3).values('branch').distinct().count()` | Amber if > 0 · Green = 0 | `#kpi-declining-branches` |
| 6 | High-Growth Markets | Locations identified as high-demand in feasibility studies | `FeasibilityStudy.objects.filter(demand_score__gte=75, status__in=['under_review','recommended','approved']).count()` | Indigo (neutral) | `#kpi-growth-markets` |

**HTMX:** `<div id="strategy-kpi-bar" hx-get="/api/v1/group/{id}/analytics/strategy/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`. Cards shimmer on first load.

---

## 5. Sections

### 5.1 Active Feasibility Studies

> All studies currently in Draft, Under Review, or Recommended status.

**Search bar:** Study name, location, district, state. Debounced 300ms.

**Filter chips:** `[Status ▾]` `[State ▾]` `[Study Type ▾]` `[Demand Score ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Study Name | `study_name` | ▲▼ | Clickable — opens `feasibility-study-detail` drawer |
| Location | `location_name` | ▲▼ | City/area name |
| District / State | `district`, `state` | ▲▼ | — |
| Type | `study_type` | ▲▼ | New Branch / Relocation / Expansion — badge |
| Status | `status` | ▲▼ | Colour badge: Draft = grey · Under Review = blue · Recommended = green · On Hold = amber · Rejected = red |
| Demand Score | `demand_score` | ▲▼ | 0–100; colour: ≥ 75 green · 50–74 amber · < 50 red |
| Financial Viability | `financial_viability` | ▲▼ | Good / Fair / Poor — badge |
| Created | `created_at` | ▲▼ | `DD MMM YYYY` |
| Days in Current Status | `days_in_status` | ▲▼ | Red if Draft > 45d or Under Review > 30d |
| Actions | — | — | `[View]` · `[Edit]` (Draft/Recommended only) · `[Change Status]` |

**Default sort:** Days in Current Status descending.
**Pagination:** 25 rows · Controls: `« Previous  Page N of N  Next »`.

### 5.2 Expansion Plan Progress

> Visual progress tracker for the active 3-year expansion plan.

**Header block (if plan exists):**
```
Current Plan: [Plan Name]  ·  Version [N]  ·  Period: [2026-29]  ·  Status: [badge]
Last Updated: [date]  ·  Next Review: [date]
[N] Planned Branches  ·  [N] On Track  ·  [N] Delayed  ·  Total Budget: ₹[N] Cr
```
`[View Full Plan →]` links to Page 22.
`[Edit Plan]` button — Role 107 only; opens expansion plan detail drawer.

**Milestone table (top 5 upcoming / overdue):**

| Column | Notes |
|---|---|
| Branch | Planned branch name |
| Milestone | Milestone description |
| Target Date | Date — red if past due |
| Status | On Track / Delayed / Blocked / Complete — colour badges |
| Owner | Role/person responsible |

`[View All Milestones →]` links to Page 22 milestones tab.

**Empty state if no plan:** Empty state card with `[+ Create Expansion Plan]` button.

### 5.3 Branch Performance Signals

> Branches showing strong growth or concerning decline — informs strategic resource allocation.

**Filter chips:** `[Signal Type ▾]` `[Zone ▾]` `[Min Months ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | — |
| Signal | `signal_type` | ▲▼ | Growth (green badge) / Declining (red badge) / Stable (grey) |
| Consecutive Months | `months_count` | ▲▼ | How many months signal has persisted |
| Enrollment Trend | `enrollment_trend` | ▲▼ | ↑ increasing / ↓ declining / → stable |
| Avg Score Trend | `score_trend` | ▲▼ | ↑ ↓ → |
| Fee Collection Trend | `fee_trend` | ▲▼ | ↑ ↓ → |
| Composite Score | `composite_score` | ▲▼ | Link to Page 11 (Branch Health Scorecard) |
| Actions | — | — | `[View Branch Profile]` · `[Add Strategic Note]` |

**Default sort:** Signal = Declining first, then Months DESC.
**Pagination:** 25 rows per page.

### 5.4 Quick Navigation

| Tile | Link |
|---|---|
| Branch Feasibility Analyser | Page 21 |
| Three-Year Expansion Plan | Page 22 |
| Branch Health Scorecard | Page 11 |
| Cross-Branch Performance Hub | Page 10 |
| Fee Collection Analytics | Page 15 |
| Analytics Export Centre | Page 24 |

---

## 6. Drawers & Modals

### 6.1 `feasibility-study-create` Drawer — 680px, right-slide

**Trigger:** `[+ New Feasibility Study]` header button. Role 107 only.

**Header:**
```
New Feasibility Study
Studies in Draft status can be edited before submission for review.
```

**Tab 1 — Location**

| Field | Type | Required | Validation |
|---|---|---|---|
| Study Name | Text input | Yes | Min 5, max 200 chars |
| Location Name | Text input | Yes | Max 150 chars (area/locality name) |
| Address / Notes | Textarea | No | Max 500 chars |
| City | Text input | Yes | Max 100 chars |
| District | Text input | Yes | Max 100 chars |
| State | Select | Yes | All Indian states |
| PIN Code | Text input | No | 6 digits |
| Study Type | Select | Yes | New Branch / Relocation of Existing Branch / Expansion of Existing Branch |
| Rationale | Textarea | Yes | Min 100 chars; why is this location being considered? |

**Tab 2 — Demand Analysis**

| Field | Type | Required | Validation |
|---|---|---|---|
| Target Student Segment | Select | Yes | Class 6–10 / Junior College (11–12) / Both |
| Estimated Catchment Students | Number | Yes | Positive integer; students of target age within 15 km |
| Existing Schools/Colleges in Area | Number | Yes | Competitor count |
| Competitor Names | Textarea | No | Max 500 chars |
| Demand Score | Number | Yes | 0–100; analyst's assessment of demand strength |
| Population Growth | Select | Yes | Increasing / Stable / Declining |
| Nearest Group Branch Distance (km) | Number | Yes | Positive decimal — ensures no overlap |
| Notes | Textarea | No | Max 500 chars |

**Tab 3 — Infrastructure**

| Field | Type | Required | Validation |
|---|---|---|---|
| Land Availability | Select | Yes | Owned / Leased / TBD |
| Built-up Area (sq ft) | Number | No | Positive integer |
| Classrooms Planned | Number | No | Positive integer |
| Labs Planned | Number | No | Positive integer |
| Hostel Planned | Toggle | No | Default off; if on: Hostel Capacity (number input) |
| Transport Access | Select | No | Good / Average / Poor |
| Power & Water Availability | Select | No | Good / Average / Poor |
| Infrastructure Notes | Textarea | No | Max 500 chars |

**Tab 4 — Financial Projections**

| Field | Type | Required | Validation |
|---|---|---|---|
| Year 1 Capex (₹) | Currency input | No | Positive decimal, 2dp |
| Year 1 Opex (₹) | Currency input | No | Positive decimal, 2dp |
| Expected Year 1 Enrollment | Number | No | Positive integer |
| Expected Year 3 Enrollment | Number | No | Positive integer |
| Avg Annual Fee per Student (₹) | Currency input | No | Positive decimal |
| Breakeven Year | Number | No | 1–10 |
| 5-Year NPV (₹) | Currency input | No | Can be negative; allow any decimal |
| Financial Viability | Select | No | Good / Fair / Poor |
| Financial Notes | Textarea | No | Max 500 chars |

**Tab 5 — Risk Assessment**

| Field | Type | Required | Validation |
|---|---|---|---|
| Key Risks | Textarea | Yes | Min 50 chars |
| Mitigation Plan | Textarea | Yes | Min 30 chars |
| Risk Level | Select | Yes | Low / Medium / High / Critical |
| Regulatory Hurdles | Textarea | No | CBSE affiliation timeline, state approvals; max 500 chars |
| Competition Risk | Select | No | Low / Medium / High |

**Tab 6 — Decision**

| Field | Type | Required | Validation |
|---|---|---|---|
| Strategic Fit | Select | Yes | Excellent / Good / Fair / Poor |
| Recommendation | Select | Yes | Proceed / Hold / Reject |
| Recommendation Notes | Textarea | Yes | Min 100 chars |
| Submit for Review | Button | — | Changes status Draft → Under Review; only shown if all required fields in Tabs 1–5 are filled |

**Footer:** `[Cancel]`  `[Save as Draft]`

On save: creates record with `status = draft`. `[Submit for Review]` (in Tab 6) changes status to `under_review` and notifies Group CEO (G4).

### 6.2 `feasibility-study-detail` Drawer — 680px, right-slide

**Trigger:** Clicking study name or `[View]` in §5.1.

Same 6 tabs as create drawer but read-only, plus an **Actions tab**:

**Actions tab:**
- `[Edit Study]` — Role 107; shown when status is Draft or Recommended
- `[Change Status]` — opens `study-status-change` modal; Role 107
- `[Add Analyst Note]` — internal note (not visible to CEO); text area + save
- Analyst Notes History — timeline of all internal notes

### 6.3 `study-status-change` Modal — 420px, centred

**Trigger:** `[Change Status]` in study detail. Role 107 only.

| Field | Type | Required | Notes |
|---|---|---|---|
| New Status | Select | Yes | Under Review / Recommended / On Hold / Rejected |
| Reason / Notes | Textarea | Yes | Min 20 chars; explain reason for status change |

**Footer:** `[Cancel]`  `[Confirm Status Change]`

On confirm: status updated; notification dispatched to Group CEO/Analytics Director if status = Recommended.

### 6.4 `strategic-note-add` Modal — 420px, centred

**Trigger:** `[Add Strategic Note]` in §5.3 branch signals table.

| Field | Type | Required | Notes |
|---|---|---|---|
| Branch | Read-only | — | Pre-filled from row |
| Note | Textarea | Yes | Min 30, max 1000 chars |
| Flag for Follow-up | Toggle | No | Default off; if on: adds to follow-up list on dashboard |

**Footer:** `[Cancel]`  `[Save Note]`

---

## 7. Charts

### 7.1 Group Enrollment Growth Trend — Bar Chart

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Group Enrollment Growth — Last 5 Academic Years" |
| Data | Total group enrollment per AY (split: Day Scholars vs Hostelers) |
| X-axis | Academic years (5 years) |
| Y-axis | Student count |
| Bar colours | Day Scholars: indigo-400 · Hostelers: teal-400 |
| Tooltip | "AY [year] · Day Scholars: [N] · Hostelers: [N] · Total: [N] · YoY: [±N]%" |
| Legend | Bottom; Day Scholars and Hostelers |
| Empty state | "Enrollment trend data not available." |
| Export | PNG export button top-right |
| API endpoint | `GET /api/v1/group/{id}/analytics/strategy/enrollment-trend/` |
| HTMX | `<div id="chart-enrollment-trend" hx-get="..." hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-enroll-spinner">` |

### 7.2 Branch Opening Timeline — Gantt-style Bar Chart

| Property | Value |
|---|---|
| Chart type | Horizontal bar / Gantt (Chart.js 4.x with custom plugin or custom rendering) |
| Title | "Expansion Plan — Branch Opening Timeline" |
| Data | Each planned branch as a row; phase bars (Land → Construction → Staff → Affiliation → Trial → Full Ops) |
| Y-axis | Planned branch names |
| X-axis | Date (month-year) |
| Bar colours | Phase colour map: Land=grey, Construction=blue, Staff=green, Affiliation=amber, Trial=orange, Full Ops=teal |
| Tooltip | "[Branch] · Phase: [Name] · [Start Date] – [End Date]" |
| Today marker | Vertical red dotted line at today's date |
| Empty state | "No active expansion plan. Create a plan in the Three-Year Expansion Plan page." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/strategy/expansion-timeline/` |
| HTMX | `<div id="chart-expansion-timeline" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Feasibility study created | "Feasibility study '[Name]' saved as Draft." | Success |
| Study submitted for review | "Study '[Name]' submitted for review. Group CEO will be notified." | Success |
| Study status changed | "Status of '[Name]' changed to [Status]." | Success |
| Strategic note saved | "Strategic note saved for [Branch]." | Success |
| Analyst note saved | "Internal note added to study '[Name]'." | Success |
| Export generated | "Strategic report exported to [format]. Download starting." | Success |
| Study create — required fields | "Please complete all required fields before saving." | Error |
| Study create — rationale too short | "Rationale must be at least 100 characters." | Error |
| Study create — recommendation note too short | "Recommendation notes must be at least 100 characters." | Error |
| Submit for review — missing tabs | "Please complete all required fields in Tabs 1–5 before submitting for review." | Error |
| Status change — server error | "Could not update study status. Please try again." | Error |
| Export failed | "Could not generate export. Please try again." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No active feasibility studies | `magnifying-glass` | "No Active Studies" | "No feasibility studies are currently in progress. Create one to begin strategic evaluation." | `[+ New Feasibility Study]` |
| No expansion plan | `map` | "No Expansion Plan" | "No 3-year expansion plan has been created for this group." | `[Create Expansion Plan]` (links to Page 22) |
| No branch performance signals | `check-circle` | "No Performance Signals" | "No branches are currently showing consistent growth or decline signals." | — |
| Study detail — no analyst notes | `pencil` | "No Internal Notes" | "No analyst notes have been added to this study yet." | `[Add Analyst Note]` |
| Chart 7.1 — no enrollment data | `chart-bar` | "No Enrollment Data" | "Enrollment trend data is not available." | — |
| Chart 7.2 — no expansion plan | `map` | "No Expansion Plan" | "Create a 3-year expansion plan to view the branch opening timeline." | `[Create Plan]` (links to Page 22) |
| Milestone table — no milestones | `check-circle` | "No Upcoming Milestones" | "All milestones are complete, or no expansion plan is active." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Studies table: 5 shimmer rows. Expansion plan block: shimmer header + 3 milestone rows. Signals table: 5 shimmer rows. |
| Studies table — search/filter | Table rows replaced by shimmer rows |
| `feasibility-study-create` drawer open | Drawer slides in; shimmer tab bar + form fields |
| `feasibility-study-detail` drawer open | Drawer slides in; shimmer tabs + content |
| Tab switch in drawer | Tab content shimmer while fetching |
| `[Save as Draft]` submit | Button disabled + "Saving…" + spinner |
| `[Submit for Review]` button | Button disabled + "Submitting…" + spinner |
| `study-status-change` modal — submit | Modal button disabled + spinner; modal closes on success |
| `strategic-note-add` modal — save | Button disabled + spinner |
| Export modal — `[Generate Export]` | Button disabled + "Generating…" + spinner |
| Chart initial load | Shimmer rectangle with centred spinner per chart |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 107 (Strategic Planning Officer) | All Others |
|---|---|---|
| Page | ✅ Full access | ❌ Redirected |
| KPI Summary Bar | ✅ All 6 cards | — |
| Charts (both) | ✅ | — |
| Studies table | ✅ Full | — |
| `[+ New Feasibility Study]` button | ✅ | — |
| `[Export Strategic Report ↓]` button | ✅ | — |
| `[Edit]` in studies table | ✅ (Draft/Recommended only) | — |
| `[Change Status]` in studies table | ✅ | — |
| `[Edit Study]` in study detail drawer | ✅ (Draft/Recommended) | — |
| `[Add Analyst Note]` in study detail | ✅ | — |
| `[Add Strategic Note]` in signals table | ✅ | — |
| Expansion plan block | ✅ Full | — |
| `[Edit Plan]` button | ✅ | — |
| Branch performance signals table | ✅ Full | — |
| Alert banners | ✅ All | — |
| Quick navigation tiles | ✅ | — |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/strategy/kpi/
```
Response: `{ "active_studies": N, "plan_status": "...", "plan_branches": N, "milestones_overdue": N, "declining_branches": N, "high_growth_markets": N }`.

### 12.2 List Feasibility Studies
```
GET /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/
```

| Query Parameter | Type | Description |
|---|---|---|
| `status` | string (multi) | `draft` · `under_review` · `recommended` · `approved` · `on_hold` · `rejected` |
| `state` | string | Filter by Indian state name |
| `study_type` | string | `new_branch` · `relocation` · `expansion` |
| `demand_score_min` | integer | Minimum demand score |
| `search` | string | Study name, location, district, state |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · 100 |
| `ordering` | string | `-days_in_status` (default) · `created_at` · `demand_score` · `study_name` |

Response: `{ count, next, previous, results: [...] }`.

### 12.3 Create Feasibility Study
```
POST /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/
```
Body: JSON with all fields from Tabs 1–6 of create drawer. Role 107 only.
Response: 201 Created — full study object with `status = draft`.

### 12.4 Retrieve Study Detail
```
GET /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/{study_id}/
```
Response: Full study object including analyst notes history.

### 12.5 Update Study
```
PATCH /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/{study_id}/
```
Body: Partial update. Role 107 only; only when status = draft or recommended.
Response: 200 OK.

### 12.6 Change Study Status
```
POST /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/{study_id}/status/
```
Body: `{ "status": "under_review|recommended|on_hold|rejected", "reason": "string" }`. Role 107 only.
Response: 200 OK.

### 12.7 Add Analyst Note to Study
```
POST /api/v1/group/{group_id}/analytics/strategy/feasibility-studies/{study_id}/notes/
```
Body: `{ "note": "string" }`. Role 107 only. Internal — not visible outside Div M.
Response: 201 Created.

### 12.8 Branch Performance Signals
```
GET /api/v1/group/{group_id}/analytics/strategy/branch-signals/
```

| Query Parameter | Type | Description |
|---|---|---|
| `signal_type` | string | `growth` · `declining` · `stable` |
| `zone` | string | Zone ID |
| `months_min` | integer | Minimum consecutive months with signal |
| `page` | integer | Default 1 |
| `ordering` | string | `-months_count` (default) · `branch_name` |

### 12.9 Add Strategic Note to Branch
```
POST /api/v1/group/{group_id}/analytics/strategy/branch-signals/{branch_id}/notes/
```
Body: `{ "note": "string", "flag_for_followup": true }`. Role 107 only.
Response: 201 Created.

### 12.10 Enrollment Trend Chart
```
GET /api/v1/group/{group_id}/analytics/strategy/enrollment-trend/
```
Response: `{ "labels": ["2022-23", ...], "day_scholars": [...], "hostelers": [...] }` (last 5 AYs).

### 12.11 Expansion Timeline Chart
```
GET /api/v1/group/{group_id}/analytics/strategy/expansion-timeline/
```
Response: `{ branches: [{ name, phases: [{ phase, start_date, end_date, status }] }] }`.

### 12.12 Export
```
GET /api/v1/group/{group_id}/analytics/strategy/export/
```
Query: `report_type` (feasibility_summary/expansion_plan/signals_report/full), `format` (pdf/xlsx).
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="strategy-kpi-bar">` | GET `.../strategy/kpi/` | `#strategy-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-enrollment-trend">` | GET `.../strategy/enrollment-trend/` | `#chart-enrollment-trend` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-expansion-timeline">` | GET `.../strategy/expansion-timeline/` | `#chart-expansion-timeline` | `innerHTML` | `hx-trigger="load"` |
| Studies table — search/filter | Search input + filter chips | GET `.../feasibility-studies/?params=` | `#studies-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` or `change` |
| Studies table — pagination | Pagination buttons | GET `.../feasibility-studies/?page={n}` | `#studies-table` | `innerHTML` | `hx-trigger="click"` |
| Open study detail drawer | Study name / [View] button | GET `/htmx/analytics/strategy/feasibility-studies/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Study drawer tab switch | Tab buttons | GET `/htmx/analytics/strategy/studies/{id}/tab/{tab_slug}/` | `#study-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Open study create drawer | `[+ New Feasibility Study]` | GET `/htmx/analytics/strategy/feasibility-studies/create/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Save study as draft | Create/edit form | POST `.../feasibility-studies/` | `#studies-table` | `innerHTML` | `hx-on::after-request="showToast(event); closeDrawer();"` |
| Change study status — open modal | `[Change Status]` button | GET `/htmx/analytics/strategy/studies/{id}/status-modal/` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Change study status — submit | Status form in modal | POST `.../studies/{id}/status/` | `#study-row-{id}` | `outerHTML` | `hx-on::after-request="closeModal(); showToast(event);"` |
| Add strategic note — open modal | `[Add Strategic Note]` | GET `/htmx/analytics/strategy/branches/{id}/note-modal/` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Save strategic note | Note form in modal | POST `.../branch-signals/{id}/notes/` | `#modal-container` | `innerHTML` | `hx-on::after-request="closeModal(); showToast(event);"` |
| Signals table — filter | Filter chips | GET `.../strategy/branch-signals/?filters=` | `#signals-table` | `innerHTML` | `hx-trigger="change"` |
| Signals table — pagination | Pagination buttons | GET `.../strategy/branch-signals/?page={n}` | `#signals-table` | `innerHTML` | `hx-trigger="click"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
