# O-07 — Campaign Calendar & Planner

> **URL:** `/group/marketing/campaigns/calendar/`
> **File:** `o-07-campaign-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary planner

---

## 1. Purpose

The Campaign Calendar & Planner is the strategic planning backbone for the group's entire admission marketing operation. It provides a visual timeline of every campaign — newspaper blitz, digital push, WhatsApp broadcast wave, school fair circuit, open day schedule, topper felicitation events, referral programme launches — plotted across the 10-month admission cycle (September to July). Every campaign has a date range, budget allocation, target branches, assigned channels, and expected lead targets, all visible on a single interactive calendar.

In a large Indian education group running 50 branches, the admission season involves 30–60 distinct campaigns across 7 phases. Without a central calendar:
- Two campaigns cannibalise each other's budget in the same geography during the same week
- A WhatsApp blast goes out the day after a newspaper ad — instead of the same morning for reinforcement
- Open days at neighbouring branches are scheduled on the same Sunday, splitting parent attendance
- The topper felicitation press release goes out before the felicitation event actually happens
- Budget gets front-loaded in Phase 2 (December) and runs out by Phase 4 (March) when walk-ins peak

This calendar prevents all of these failures by providing timeline conflict detection, budget distribution visualization, channel overlap warnings, and phase-wise milestone tracking. The Campaign Manager builds the annual plan here in September–October, gets G4/G5 approval, and then executes against it for the next 10 months — updating actual vs planned as campaigns run.

**Scale:** 5–50 branches · 15–60 campaigns per season · 7 phases · ₹10L–₹10Cr annual budget · 10-month planning horizon

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create, edit, move, delete campaigns on calendar | Primary planner |
| Group Topper Relations Manager | 120 | G3 | Read + Add topper events | Can add felicitation/press events |
| Group Campaign Content Coordinator | 131 | G2 | Read only | Views timeline for material prep deadlines |
| Group Admission Telecaller Executive | 130 | G3 | Read only | Views upcoming campaigns to prepare call scripts |
| Group Admission Data Analyst | 132 | G1 | Read only | Views for analytics planning |
| Group CEO | — | G4 | Read + Approve annual plan | Approves the season campaign plan |
| Group Chairman | — | G5 | Read + Approve + Override | Final budget approval |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Create/edit restricted to role 119 or G4+. Topper events: role 120. Approval: G4/G5 only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Calendar & Planner
```

### 3.2 Page Header
```
Campaign Calendar & Planner                    [Add Campaign]  [Plan Season]  [Submit for Approval]  [Export]
Campaign Manager — Ramesh Venkataraman
Sunrise Education Group · Season 2026-27 · 38 campaigns planned · Budget: ₹5.6 Cr · Status: Approved ✅
```

**Season selector:** Dropdown to switch between seasons. Current season default.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Season plan not yet approved by G4/G5 | "Season campaign plan is in DRAFT. Submit for CEO/Chairman approval before execution." | High (amber) |
| Campaign overlap detected (same branches, same week, same channel) | "Conflict: [Campaign A] and [Campaign B] overlap on [Channel] for [Branches] during [Dates]" | Medium (yellow) |
| Budget allocation exceeds season budget | "Total campaign budgets (₹[X]) exceed approved season budget (₹[Y]) by ₹[Z]" | Critical (red) |
| Phase milestone approaching (< 7 days) | "Phase [N] — [Phase Name] starts in [X] days. [N] campaigns scheduled." | Info (blue) |
| No campaigns in upcoming 30 days | "No campaigns scheduled in the next 30 days. Review calendar for gaps." | Medium (yellow) |

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Campaigns | Integer | COUNT(campaigns) WHERE season = current | Static blue | `#kpi-total-campaigns` |
| 2 | Active Now | Integer | COUNT(campaigns) WHERE status = 'active' AND today BETWEEN start AND end | Static green | `#kpi-active-now` |
| 3 | Budget Allocated | ₹ + % | SUM(campaign_budget) / season_budget × 100 | Green ≤ 95%, Amber 95–100%, Red > 100% | `#kpi-budget-allocated` |
| 4 | Budget Spent | ₹ + % | SUM(campaign_actual_spend) / SUM(campaign_budget) × 100 | Green < 80%, Amber 80–95%, Red > 95% | `#kpi-budget-spent` |
| 5 | Upcoming (30d) | Integer | COUNT(campaigns) WHERE start_date within 30 days AND status = 'scheduled' | Static blue | `#kpi-upcoming` |
| 6 | Plan Status | Badge | Season plan approval status | Green = Approved, Amber = Pending, Red = Rejected | `#kpi-plan-status` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/campaigns/calendar/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Calendar View

Interactive calendar with three view modes: **Month** (default), **Quarter**, and **Timeline (Gantt)**.

#### 5.1.1 Month View

Standard calendar grid (7 columns × 5–6 rows). Each date cell shows campaign blocks.

**Campaign block on cell:**
- Coloured bar spanning start-to-end dates (multi-day campaigns span across cells)
- Colour = channel type: 📰 Newspaper (dark blue) / 📱 Digital (purple) / 💬 WhatsApp (green) / 🏗️ Outdoor (amber) / 🎪 Event (pink) / 📧 Email (teal) / 📋 Multi-channel (gradient)
- Text: Campaign name (truncated)
- Click opens campaign detail drawer

**Cell interactions:**
- Hover on date: tooltip shows all campaigns on that date
- Click empty date: opens "Add Campaign" modal with date pre-filled
- Drag campaign bar to move dates (G3+ only)
- Resize campaign bar edges to change duration (G3+ only)

**Phase overlay:** Semi-transparent background colour bands showing the 7 admission phases across the calendar months.

| Phase | Colour Band | Months |
|---|---|---|
| Phase 1 — Pre-Campaign | Light grey | Sep–Oct |
| Phase 2 — Early Bird | Light blue | Nov–Dec |
| Phase 3 — Newspaper Blitz | Light amber | Jan–Feb |
| Phase 4 — Peak Admissions | Light green | Feb–Apr |
| Phase 5 — Results Season | Light gold | May–Jun |
| Phase 6 — Late Fill | Light orange | Jun–Jul |
| Phase 7 — Post-Season | Light grey | Aug–Sep |

#### 5.1.2 Quarter View

Shows 3 months side-by-side in a compact horizontal layout. Campaigns shown as horizontal bars spanning across the 3-month timeline. Better for seeing campaign distribution and gaps.

#### 5.1.3 Timeline / Gantt View

Horizontal Gantt chart with:
- Y-axis: Campaign names (grouped by channel or by phase)
- X-axis: Date timeline (weeks)
- Bars: Campaign duration, colour-coded by channel
- Milestones: Diamond markers for key dates (approval deadline, material ready, launch, end)
- Dependencies: Arrows connecting dependent campaigns (e.g., "Material Prep" → "Newspaper Launch")
- Today line: Vertical red dashed line showing current date

**Gantt grouping options:** By Channel / By Phase / By Branch Cluster / Flat (no grouping)

### 5.2 Filter Bar

| Filter | Type | Options |
|---|---|---|
| Channel | Multi-select chips | Newspaper / Digital / WhatsApp / SMS / Outdoor / Event / Email / Multi-channel |
| Phase | Dropdown | All / Phase 1–7 |
| Branch | Dropdown | All / Specific branch / Branch cluster |
| Status | Multi-select chips | Scheduled / Active / Paused / Completed / Cancelled |
| Budget Range | Slider | ₹0 – ₹1Cr |
| Assigned To | Dropdown | Campaign Manager / Content Coordinator |

### 5.3 Campaign List (below calendar)

Tabular list of all campaigns for quick scanning and bulk actions.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Campaign Name | Text | Yes | Click opens detail drawer |
| Channel | Badge(s) | Yes | Colour-coded channel icons |
| Phase | Badge | Yes | Phase 1–7 |
| Start Date | Date | Yes | Campaign start |
| End Date | Date | Yes | Campaign end |
| Duration | Text | Yes | "[N] days" |
| Branches | Text | Yes | "All" or count + names |
| Budget | ₹ Amount | Yes | Allocated budget |
| Spent | ₹ Amount | Yes | Actual spend to date |
| Leads (Target) | Integer | Yes | Expected leads |
| Leads (Actual) | Integer | Yes | Actual leads so far |
| Status | Badge | Yes | Scheduled / Active / Paused / Completed / Cancelled |
| Actions | Buttons | No | [View] [Edit] [Pause/Resume] [⋮] |

**Default sort:** Start Date ASC
**Pagination:** Server-side · 25/page

### 5.4 Budget Distribution View

Visual breakdown of how the season budget is allocated across phases and channels.

**Phase Budget Table:**

| Phase | Allocated | Spent | Remaining | % of Total | Bar |
|---|---|---|---|---|---|
| Phase 1 — Pre-Campaign | ₹20,00,000 | ₹18,50,000 | ₹1,50,000 | 3.6% | ████░ |
| Phase 2 — Early Bird | ₹60,00,000 | ₹58,00,000 | ₹2,00,000 | 10.7% | ███████████░ |
| Phase 3 — Newspaper Blitz | ₹1,40,00,000 | ₹92,00,000 | ₹48,00,000 | 25.0% | ████████████████████████░░░░ |
| Phase 4 — Peak Admissions | ₹1,80,00,000 | ₹1,10,00,000 | ₹70,00,000 | 32.1% | ████████████████████████████████░░░░░░ |
| Phase 5 — Results Season | ₹80,00,000 | ₹0 | ₹80,00,000 | 14.3% | (scheduled) |
| Phase 6 — Late Fill | ₹50,00,000 | ₹0 | ₹50,00,000 | 8.9% | (scheduled) |
| Phase 7 — Post-Season | ₹30,00,000 | ₹0 | ₹30,00,000 | 5.4% | (scheduled) |
| **Total** | **₹5,60,00,000** | **₹2,78,50,000** | **₹2,81,50,000** | **100%** | |

**Channel Budget Split (Donut):** Visual split of budget by channel type.

### 5.5 Conflict Detector

Automated conflict detection panel showing overlapping campaigns.

**Conflict Types:**

| Conflict | Description | Severity |
|---|---|---|
| Same Channel + Same Branch + Same Week | Two newspaper campaigns target the same branch in the same week | High (red) |
| Budget Overlap | Total campaign budgets in a week exceed weekly budget cap | Medium (amber) |
| Event Clash | Two open day/fair events at neighbouring branches on same date | High (red) |
| WhatsApp Fatigue | More than 2 WhatsApp campaigns targeting same parent list in 7 days | Medium (amber) |
| Material Not Ready | Campaign starts within 7 days but linked material status ≠ 'published' | High (red) |
| No Telecaller Assigned | Campaign expects telecalling follow-up but no telecallers assigned | Medium (amber) |

**Conflict Row:**
- Campaign A name ↔ Campaign B name
- Conflict type + description
- Branches affected
- Date overlap range
- Suggested resolution (auto-generated)
- Actions: [Reschedule A] [Reschedule B] [Dismiss]

---

## 6. Drawers & Modals

### 6.1 Modal: `add-campaign` (640px)
- **Title:** "Add Campaign to Calendar"
- **Fields:**
  - Campaign name (text, required)
  - Channel (multi-select, required): Newspaper / Digital / WhatsApp / SMS / Outdoor / Event / Email
  - Phase (auto-detected from dates, editable)
  - Start date (date picker, required)
  - End date (date picker, required)
  - Target branches (radio): All Branches / Select Branches (multi-select) / Branch Cluster (dropdown)
  - Target streams (multi-select): MPC / BiPC / MEC / CEC / HEC / Foundation / All
  - Budget (₹, required)
  - Lead target (integer — expected enquiries from this campaign)
  - Description / objective (textarea)
  - Material required (toggle — links to O-03 material library)
  - Material ready by date (date, if material required)
  - Telecalling follow-up needed (toggle — auto-creates telecaller assignment)
  - Dependencies (multi-select — other campaigns that must complete first)
  - Milestones (repeatable group):
    - Milestone name (text)
    - Milestone date (date)
    - e.g., "Creative approval", "Print order", "Launch", "Mid-review", "End review"
  - Assigned to (dropdown — team member responsible)
  - Notes (textarea)
- **Buttons:** Cancel · Save as Draft · Add to Calendar
- **Access:** Role 119 or G4+

### 6.2 Modal: `plan-season` (720px — full wizard)
- **Title:** "Plan Admission Season"
- **Step 1 — Season Setup:**
  - Season name (text)
  - Academic year (dropdown)
  - Season start date → end date
  - Total budget (₹)
  - Target total leads (integer)
  - Target total enrollments (integer)
- **Step 2 — Phase Configuration:**
  - 7 phases pre-filled with default dates (editable)
  - Budget allocation per phase (₹ + %)
  - Lead target per phase
- **Step 3 — Channel Budget Split:**
  - Budget % per channel (sliders): Newspaper / Digital / WhatsApp / Outdoor / Events / Referral / Other
  - Pie chart updates live as sliders move
- **Step 4 — Branch Targets:**
  - Table: Branch name / Seat target / Lead target / Budget share
  - Auto-calculate based on branch size or manual override
- **Step 5 — Review & Submit:**
  - Summary of all settings
  - [Save as Draft] [Submit for Approval]
- **Access:** Role 119 or G4+

### 6.3 Drawer: `campaign-detail` (720px, right-slide)
- **Tabs:** Overview · Budget · Leads · Timeline · Materials · Branches
- **Overview tab:** Campaign name, channel(s), phase, dates, status, description, assigned to, milestones list with completion status
- **Budget tab:** Allocated vs spent, daily spend line chart, projected burn date, expense log
- **Leads tab:** Leads generated from this campaign (count by stage, source attribution, branch-wise split)
- **Timeline tab:** Gantt bar for this campaign with milestones, actual vs planned dates
- **Materials tab:** Linked materials from O-03 with readiness status
- **Branches tab:** Branch-wise performance — leads per branch from this campaign
- **Footer:** [Edit] [Pause] [Resume] [Clone] [Cancel Campaign] [View in Builder → O-08]

### 6.4 Modal: `submit-for-approval` (480px)
- **Title:** "Submit Season Plan for Approval"
- **Summary:** Total campaigns, total budget, phase breakdown, branch coverage
- **Approver:** CEO (Role, auto-populated)
- **Notes to approver (textarea)**
- **Buttons:** Cancel · Submit
- **Behaviour:** PATCH status → 'pending_approval' → notification to G4/G5

### 6.5 Modal: `approval-review` (640px) — G4/G5 only
- **Title:** "Review Season Campaign Plan"
- **Shows:** Full season summary — phases, budgets, channels, branch targets, campaign count
- **Comparison:** vs previous season (side-by-side)
- **Actions:** [Approve ✅] [Request Changes ✏️] [Reject ❌]
- **Notes field (textarea)**
- **Behaviour:** PATCH status → approved/changes_requested/rejected → notification to role 119

---

## 7. Charts

### 7.1 Budget Allocation by Channel (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Season Budget by Channel" |
| Data | Budget allocated per channel type |
| Colour | Newspaper: dark blue / Digital: purple / WhatsApp: green / Outdoor: amber / Events: pink / Email: teal / Other: grey |
| Tooltip | "[Channel]: ₹[X] ([Y]% of total)" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/calendar/analytics/budget-by-channel/` |

### 7.2 Campaign Density Heatmap

| Property | Value |
|---|---|
| Chart type | Heatmap (calendar-style, 52 weeks × 7 days or 12 months × 4 weeks) |
| Title | "Campaign Activity Density — Season Timeline" |
| Data | Number of active campaigns per week |
| Colour scale | Light blue (0–1) → Medium blue (2–3) → Dark blue (4–5) → Red (6+, over-saturated) |
| Tooltip | "Week of [Date]: [N] active campaigns, ₹[X] budget committed" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/calendar/analytics/density/` |

### 7.3 Budget: Planned vs Actual (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Budget: Planned vs Actual by Phase" |
| Data | Per phase: planned budget (bar 1), actual spend (bar 2) |
| Colour | Planned: `#93C5FD` light blue / Actual: `#3B82F6` blue |
| Tooltip | "[Phase]: Planned ₹[X], Actual ₹[Y] ([Z]% utilisation)" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/calendar/analytics/budget-planned-vs-actual/` |

### 7.4 Leads: Target vs Actual (Line + Bar Combo)

| Property | Value |
|---|---|
| Chart type | Combo — Bars (actual monthly leads) + Line (cumulative target) |
| Title | "Lead Generation: Target vs Actual — Season Progress" |
| Data | Monthly actual leads (bars) + cumulative target line |
| Colour | Bars: `#10B981` green / Line: `#EF4444` red (target) |
| Tooltip | "[Month]: [N] leads (target: [M]) — cumulative: [X] / [Y]" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/calendar/analytics/leads-target-vs-actual/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign added | "Campaign '[Name]' added to calendar — [Start] to [End]" | Success | 3s |
| Campaign updated | "Campaign '[Name]' updated" | Success | 2s |
| Campaign moved (drag) | "Campaign '[Name]' moved to [New Start] – [New End]" | Success | 3s |
| Campaign paused | "Campaign '[Name]' paused" | Info | 3s |
| Campaign resumed | "Campaign '[Name]' resumed" | Success | 3s |
| Campaign cancelled | "Campaign '[Name]' cancelled" | Info | 3s |
| Season plan submitted | "Season plan submitted for CEO approval" | Success | 4s |
| Season plan approved | "Season plan approved by [Approver]. Campaigns ready for execution." | Success | 6s |
| Season plan rejected | "Season plan returned with changes requested. Review comments." | Warning | 6s |
| Conflict detected | "Campaign conflict detected: [Campaign A] ↔ [Campaign B]. Review calendar." | Warning | 6s |
| Budget exceeded | "Total allocated budgets exceed season budget by ₹[X]. Adjust before approval." | Error | 8s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No season configured | 📅 | "No Admission Season" | "Create an admission season to start planning campaigns." | Plan Season |
| No campaigns added | 📢 | "Calendar is Empty" | "Add your first campaign to start building the admission season plan." | Add Campaign |
| No campaigns in current view | 🔍 | "No Campaigns This Month" | "No campaigns scheduled for the displayed period. Try a different month or filter." | Clear Filters |
| Season plan not approved | ⏳ | "Plan Pending Approval" | "The season campaign plan has been submitted and is awaiting CEO/Chairman approval." | — |
| No conflicts | ✅ | "No Conflicts Detected" | "All campaigns are well-spaced with no overlaps or resource conflicts." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + calendar grid skeleton (7×5 cells) |
| Month navigation | Calendar grid shimmer replacing current month |
| Gantt view load | Horizontal bars skeleton (10 rows) with timeline header |
| Campaign list load | Table skeleton: 10 rows |
| Campaign detail drawer | 720px right-slide skeleton with 6 tabs |
| Budget view load | Table skeleton + donut placeholder |
| Conflict detection | Spinner: "Checking for campaign conflicts…" |
| Season wizard steps | Step skeleton with form field placeholders |
| Chart load | Grey canvas + "Loading chart…" |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/` | G1+ | Calendar data (campaigns with dates) |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/campaigns/` | G1+ | Campaign list (paginated) |
| GET | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/` | G1+ | Single campaign detail |
| POST | `/api/v1/group/{id}/marketing/campaigns/` | G3+ | Create campaign |
| PUT | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/` | G3+ | Update campaign |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/status/` | G3+ | Pause/resume/cancel |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/dates/` | G3+ | Move campaign (drag) |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/{campaign_id}/` | G4+ | Delete campaign |
| POST | `/api/v1/group/{id}/marketing/campaigns/calendar/season/` | G3+ | Create season plan |
| PUT | `/api/v1/group/{id}/marketing/campaigns/calendar/season/{season_id}/` | G3+ | Update season plan |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/calendar/season/{season_id}/approval/` | G4+ | Approve/reject plan |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/conflicts/` | G1+ | Conflict detection results |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/analytics/budget-by-channel/` | G1+ | Budget chart |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/analytics/density/` | G1+ | Density heatmap |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/analytics/budget-planned-vs-actual/` | G1+ | Budget comparison |
| GET | `/api/v1/group/{id}/marketing/campaigns/calendar/analytics/leads-target-vs-actual/` | G1+ | Leads comparison |
| POST | `/api/v1/group/{id}/marketing/campaigns/calendar/export/` | G1+ | Export calendar (PDF/XLSX/ICS) |

### Query Parameters — Calendar

| Parameter | Type | Description |
|---|---|---|
| `view` | string | month / quarter / gantt |
| `month` | integer | Month number (1–12) |
| `year` | integer | Year |
| `season_id` | integer | Season filter |
| `channel` | string | Filter by channel type |
| `phase` | integer | Filter by phase (1–7) |
| `branch_id` | integer | Filter by branch |
| `status` | string | scheduled / active / paused / completed / cancelled |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../calendar/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Calendar month load | `<div id="calendar-grid">` | `hx-get=".../calendar/?view=month&month={m}&year={y}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="load"` |
| Month nav (prev/next) | Nav arrow buttons | `hx-get` with month±1 | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| View toggle | View buttons (month/quarter/gantt) | `hx-get=".../calendar/?view={mode}"` | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Filter controls | `hx-get` with filter params | `#calendar-content` | `innerHTML` | `hx-trigger="change"` |
| Campaign detail drawer | Campaign bar click | `hx-get=".../campaigns/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Add campaign | Form submit | `hx-post=".../campaigns/"` | `#add-result` | `innerHTML` | Toast + calendar refresh |
| Move campaign (drag) | Drag-end event | `hx-patch=".../campaigns/{id}/dates/" (new start/end)` | `#campaign-bar-{id}` | `outerHTML` | JS drag + HTMX patch |
| Pause/resume | Status button | `hx-patch=".../campaigns/{id}/status/"` | `#campaign-status-{id}` | `innerHTML` | Inline badge update |
| Conflict check | Auto on campaign add/move | `hx-get=".../calendar/conflicts/"` | `#conflict-panel` | `innerHTML` | `hx-trigger="load"` on calendar change |
| Campaign list load | `<div id="campaign-list">` | `hx-get=".../campaigns/"` | `#campaign-list-body` | `innerHTML` | `hx-trigger="load"` |
| Season wizard steps | Next/Back buttons | `hx-get=".../calendar/season/wizard/step/{n}/"` | `#wizard-content` | `innerHTML` | Multi-step form |
| Submit approval | Submit button | `hx-patch=".../calendar/season/{id}/approval/"` | `#approval-status` | `innerHTML` | Toast + status update |
| Export | Export button | `hx-post=".../calendar/export/"` | `#export-result` | `innerHTML` | Download link in toast |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
