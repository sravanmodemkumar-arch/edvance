# O-22 — Cross-Branch Enrollment Drive

> **URL:** `/group/marketing/enrollment/drive/`
> **File:** `o-22-cross-branch-enrollment-drive.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary driver

---

## 1. Purpose

The Cross-Branch Enrollment Drive is the seat-fill war room — a real-time dashboard tracking branch-wise enrollment targets vs actuals across all branches in the group. In Indian education, the entire academic year's revenue is determined by how many seats are filled by July. A group with 20,000 seats charging ₹80,000/year loses ₹8 crore for every 1,000 unfilled seats. The enrollment drive page is where the Campaign Manager monitors daily seat-fill progress, identifies branches falling behind, reallocates marketing effort, and triggers emergency campaigns for underperforming branches.

The problems this page solves:

1. **Target visibility:** Each branch has a seat target per class, per stream. A 30-branch group has 200+ individual targets (10 classes × 2–3 streams). Without a centralised view, the Campaign Manager doesn't know that Kukatpally MPC is at 95% but Dilsukhnagar BiPC is at 40%.

2. **Daily progress tracking:** During peak season (Feb–Apr), seats fill at 50–200 per day across the group. Daily tracking with Red/Amber/Green colour-coding shows which branches are on track and which need intervention.

3. **Resource reallocation:** When a branch is underperforming, the Campaign Manager needs to act fast — increase newspaper ads for that branch, add telecallers to its leads, run a flash WhatsApp campaign, or offer a fee discount. This page links enrollment gaps to actionable campaigns.

4. **Seat transfer logic:** When Branch A is full but Branch B (same city) has vacancies, parents can be offered seats at Branch B with transport support. The enrollment drive tracks inter-branch seat transfer opportunities.

5. **Integration with Division C:** Seat availability data comes from Division C (Admissions) seat matrix. When a seat is filled via fee payment, it auto-updates here. The enrollment drive page is the marketing view of Division C's operational seat data.

**Scale:** 5–50 branches · 500–50,000 total seats · 10–200 seats/day fill rate during peak · 100–500 individual targets (class × stream × branch)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — set targets, track progress, trigger campaigns, manage transfers | Primary drive manager |
| Group Admission Data Analyst | 132 | G1 | Read + Export — analytics, trend data | Reporting |
| Group Admission Telecaller Executive | 130 | G3 | Read (own branch) — see branch seat status for context during calls | Lead context |
| Group Topper Relations Manager | 120 | G3 | Read — enrollment data for topper-pipeline cross-reference | Topper impact tracking |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve seat targets, approve emergency campaigns | Strategic authority |
| Branch Principal | — | G3 | Read (own branch) — view own branch targets and progress | Branch accountability |
| Group CFO | 30 | G1 | Read — revenue projection based on seat fill | Financial planning |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Target setting: role 119 or G4+. Branch staff see only own branch.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  Cross-Branch Enrollment Drive
```

### 3.2 Page Header
```
Cross-Branch Enrollment Drive                        [Set Targets]  [Launch Emergency Campaign]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 18,420 / 22,000 seats filled (83.7%) · 3,580 remaining · 42 days to target date
```

**Master progress bar:** Full-width, colour-segmented: Green (filled) + Amber (pipeline/offered) + Grey (remaining).

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Seats | Integer | SUM(seat_capacity) all branches | Static blue | `#kpi-total-seats` |
| 2 | Filled | Integer + % | COUNT enrolled + % of total | Green ≥ 90%, Amber 75–90%, Red < 75% | `#kpi-filled` |
| 3 | Pipeline (Offered) | Integer | COUNT leads at "Offered" stage | Static amber | `#kpi-pipeline` |
| 4 | Remaining to Fill | Integer | Total − Filled − Pipeline | Red if > 20% of total | `#kpi-remaining` |
| 5 | Fill Rate (This Week) | Integer/day | AVG daily fills this week | Green ≥ target rate, Red < target rate | `#kpi-fill-rate` |
| 6 | Days to Target Date | Integer | Target date − today | Red ≤ 14, Amber 15–30, Green > 30 | `#kpi-days-left` |
| 7 | Branches On Track | N/M | Branches ≥ 85% of pro-rated target | Green = all, Red = any below | `#kpi-on-track` |
| 8 | Revenue at Risk | ₹ Amount | Remaining seats × avg annual fee | Red > ₹1 Cr, Amber ₹50L–₹1Cr, Green < ₹50L | `#kpi-revenue-risk` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Branch Dashboard** — Heat-map table of all branches with targets vs actuals
2. **Class/Stream View** — Drill-down by class and stream across branches
3. **Daily Progress** — Day-over-day fill chart
4. **Action Centre** — Emergency campaigns and interventions

### 5.2 Tab 1: Branch Dashboard

**Master branch enrollment table:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Branch | Text | Yes | Branch name + city |
| Total Seats | Integer | Yes | Total capacity |
| Target | Integer | Yes | Season enrollment target (may be < capacity) |
| Filled | Integer | Yes | Confirmed enrollments (fee paid) |
| Offered | Integer | Yes | Seats offered, awaiting fee payment |
| Remaining | Integer | Yes | Target − Filled |
| Fill % | Progress bar | Yes | Filled / Target × 100 |
| Pro-rated Target | Integer | No | Expected fills by today (linear projection from season start to target date) |
| Actual vs Pro-rated | Delta + badge | Yes | Green (ahead), Amber (within 5%), Red (behind > 5%) |
| Fill Rate (7d) | Decimal | Yes | Avg daily fills last 7 days |
| Required Rate | Decimal | Yes | Remaining / Days left (to hit target) |
| Gap Analysis | Badge | Yes | On Track ✅ / At Risk ⚠️ / Critical 🔴 |
| Top Channel | Badge | No | Source driving most enrollments |
| Actions | Buttons | No | [View Detail] [Launch Campaign] [Transfer Seats] |

**Colour-coded rows:**
- Green: fill % ≥ 90% of target
- Amber: 75–90%
- Red: < 75%
- Dark red: < 50% (critical intervention needed)

**Totals row:** Group-level totals at bottom.

### 5.3 Tab 2: Class/Stream View

Matrix view: rows = class + stream, columns = branches.

| | Kukatpally | Dilsukhnagar | Miyapur | ... | Group Total |
|---|---|---|---|---|---|
| Jr Inter MPC | 180/200 (90%) | 120/180 (67%) | 95/150 (63%) | ... | 1,420/1,800 |
| Jr Inter BiPC | 85/100 (85%) | 60/100 (60%) | 45/80 (56%) | ... | 680/900 |
| Foundation | 120/120 (100%) ✅ | 90/100 (90%) | 80/100 (80%) | ... | 890/980 |
| ... | ... | ... | ... | ... | ... |

**Cell colour:** Green ≥ 85%, Amber 60–85%, Red < 60%
**Cell content:** Filled/Target (%)
**Click on cell:** Opens drill-down showing individual leads at that branch + class + stream

### 5.4 Tab 3: Daily Progress

Charts section (see §7) showing:
- Daily enrollment count (bar chart)
- Cumulative fill (area chart with target line)
- Fill rate trend (line)

### 5.5 Tab 4: Action Centre

Recommended and active interventions for underperforming branches.

**Auto-generated recommendations:**

| Branch | Gap | Recommendation | Priority | Action |
|---|---|---|---|---|
| Dilsukhnagar | −60 seats from target | Launch WhatsApp blast to 2,400 leads in pipeline | High | [Execute] |
| Miyapur | Fill rate 3/day, need 8/day | Add 2 telecallers from Kukatpally (which is full) | High | [Reassign] |
| Secunderabad | BiPC at 45% | Run newspaper ad in Secunderabad edition + open day | Medium | [Create Campaign] |

**Active emergency campaigns:** Table of campaigns launched from this page with their progress.

---

## 6. Drawers & Modals

### 6.1 Modal: `set-targets` (720px)

- **Title:** "Set Enrollment Targets — Season [Year]"
- **Table editor:** Rows = branches × classes × streams; Columns = Seat Capacity, Target, Target Date
- **Bulk options:**
  - Copy from last year (shift +X%)
  - Set all targets = capacity
  - Set all targets = X% of capacity
- **Validation:** Target ≤ Capacity per cell
- **Buttons:** Cancel · Save Draft · Submit for G4 Approval
- **Access:** Role 119 or G4+

### 6.2 Modal: `launch-emergency-campaign` (560px)

- **Title:** "Launch Emergency Campaign — [Branch]"
- **Pre-filled:** Branch, gap (seats remaining), recommended channels
- **Fields:**
  - Campaign name (auto-generated: "Emergency Fill — [Branch] — [Date]")
  - Channels (multi-select): WhatsApp Blast / Telecalling Push / Newspaper Ad / Flex Banner / Walk-in Saturday / Fee Discount
  - Target audience: Leads at [Stage] for [Branch] (auto-queried from O-15)
  - Budget (₹, from O-09 remaining)
  - Duration: Start → End
  - Special offer? (toggle → link to O-23 offer campaign)
- **Buttons:** Cancel · Launch Now
- **Access:** Role 119 or G4+

### 6.3 Modal: `transfer-seats` (560px)

- **Title:** "Inter-Branch Seat Transfer"
- **Purpose:** When Branch A is full, redirect leads to Branch B
- **Fields:**
  - Source branch (full or nearly full)
  - Target branch (has vacancies)
  - Class/stream (dropdown)
  - Number of leads to transfer (or "All pipeline leads for this class")
  - Incentive for parent: Transport subsidy / Fee discount / Both / None
  - Notes (textarea)
- **Preview:** "[N] leads from [Source] will be offered seats at [Target]"
- **Buttons:** Cancel · Execute Transfer
- **Behaviour:** Updates lead records in O-15, sends WhatsApp to affected parents with new branch offer
- **Access:** Role 119 or G4+

### 6.4 Drawer: `branch-enrollment-detail` (720px, right-slide)

- **Tabs:** Overview · Class Breakdown · Daily Log · Pipeline · Campaigns
- **Overview tab:** Branch KPIs — total target, filled, offered, remaining, fill rate, gap analysis, revenue at risk
- **Class Breakdown tab:** Per-class per-stream table with targets and actuals
- **Daily Log tab:** Day-by-day enrollment count for this branch (table + mini chart)
- **Pipeline tab:** Leads in pipeline (Interested → Offered) for this branch, segmented by stage
- **Campaigns tab:** Active marketing campaigns targeting this branch
- **Footer:** [Launch Campaign] [Transfer Seats] [Adjust Target] [Export]

---

## 7. Charts

### 7.1 Cumulative Enrollment (Area + Target Line)

| Property | Value |
|---|---|
| Chart type | Area with dashed target line (Chart.js 4.x) |
| Title | "Cumulative Enrollment — Season [Year]" |
| Data | Daily cumulative fills (area) + linear target projection (dashed line) |
| Area colour | `#10B981` green with gradient |
| Target line | `#94A3B8` grey dashed |
| X-axis | Date (season start → target date) |
| Y-axis | Seat count |
| Annotations | Phase boundaries, major campaign launches |
| API | `GET /api/v1/group/{id}/marketing/enrollment/drive/analytics/cumulative/` |

### 7.2 Daily Fill Rate (Bar)

| Property | Value |
|---|---|
| Chart type | Bar (Chart.js 4.x) |
| Title | "Daily Enrollments — Last 30 Days" |
| Data | Per day: enrollment count |
| Colour | Green (above required rate) / Red (below required rate) |
| Benchmark line | Required daily rate (dashed) |
| API | `GET /api/v1/group/{id}/marketing/enrollment/drive/analytics/daily-fills/` |

### 7.3 Branch Fill Comparison (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar |
| Title | "Branch Enrollment Progress" |
| Data | Per branch: filled (green bar) + offered (amber bar) + remaining (grey bar) = stacked to target |
| API | `GET /api/v1/group/{id}/marketing/enrollment/drive/analytics/branch-fill/` |

### 7.4 Stream-wise Fill (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Enrollment by Stream — All Branches" |
| Data | Per stream (MPC/BiPC/MEC/Foundation/etc.): filled vs target |
| Colour | Filled: green / Target: light grey outline |
| API | `GET /api/v1/group/{id}/marketing/enrollment/drive/analytics/stream-fill/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Targets set | "Enrollment targets set for Season [Year] — [N] branches, [M] total seats" | Success | 4s |
| Targets approved | "Targets approved by [Approver]" | Success | 3s |
| Emergency campaign launched | "Emergency campaign launched for [Branch] — [Channel]" | Success | 4s |
| Seat transfer executed | "[N] leads transferred from [Source] to [Target Branch]" | Info | 4s |
| Branch hit target | "🎉 [Branch] has reached 100% enrollment target!" | Success | 6s |
| Branch critical | "⚠️ [Branch] is at [X]% with [N] days remaining — intervention needed" | Error | 8s |
| Daily milestone | "Group crossed [N] enrollments today — [X]% of total target" | Success | 5s |
| Fill rate declining | "Fill rate has dropped below required rate — [X]/day vs needed [Y]/day" | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No targets set | 🎯 | "No Enrollment Targets" | "Set branch-wise enrollment targets to start tracking the drive." | Set Targets |
| No enrollments yet | 📋 | "No Enrollments Recorded" | "Enrollment data will appear as students complete fee payment." | — |
| Season not started | 📅 | "Season Not Yet Active" | "The enrollment drive for Season [Year] hasn't started yet." | — |
| All targets met | 🎉 | "All Targets Met!" | "Congratulations! All branches have met their enrollment targets." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer + master progress bar placeholder + branch table skeleton (15 rows) |
| Tab switch | Content skeleton |
| Class/stream matrix | Grid shimmer |
| Branch detail drawer | 720px skeleton: KPIs + 5 tabs |
| Chart load | Grey canvas placeholder |
| Target setting modal | Editable grid shimmer |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/` | G1+ | Branch dashboard data |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/{branch_id}/` | G1+ | Branch detail |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/class-stream/` | G1+ | Class × stream × branch matrix |
| POST | `/api/v1/group/{id}/marketing/enrollment/drive/targets/` | G3+ | Set/update targets |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/drive/targets/approve/` | G4+ | Approve targets |
| POST | `/api/v1/group/{id}/marketing/enrollment/drive/emergency-campaign/` | G3+ | Launch emergency campaign |
| POST | `/api/v1/group/{id}/marketing/enrollment/drive/transfer/` | G3+ | Inter-branch seat transfer |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/daily-log/` | G1+ | Daily enrollment log |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/recommendations/` | G3+ | Auto-generated recommendations |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/analytics/cumulative/` | G1+ | Cumulative chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/analytics/daily-fills/` | G1+ | Daily bar chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/analytics/branch-fill/` | G1+ | Branch comparison |
| GET | `/api/v1/group/{id}/marketing/enrollment/drive/analytics/stream-fill/` | G1+ | Stream chart |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../drive/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` (5 min) |
| Tab switch | Tab click | `hx-get` with tab param | `#drive-content` | `innerHTML` | `hx-trigger="click"` |
| Branch table | Dashboard tab | `hx-get=".../drive/"` | `#branch-table` | `innerHTML` | `hx-trigger="load"` |
| Branch detail drawer | Row click | `hx-get=".../drive/{branch_id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Class matrix | Matrix tab | `hx-get=".../drive/class-stream/"` | `#class-matrix` | `innerHTML` | `hx-trigger="click"` |
| Matrix cell drill-down | Cell click | `hx-get=".../drive/?branch={id}&class={c}&stream={s}"` | `#cell-detail` | `innerHTML` | Inline popup |
| Set targets | Target form | `hx-post=".../drive/targets/"` | `#target-result` | `innerHTML` | Toast |
| Emergency campaign | Campaign form | `hx-post=".../drive/emergency-campaign/"` | `#emergency-result` | `innerHTML` | Toast |
| Seat transfer | Transfer form | `hx-post=".../drive/transfer/"` | `#transfer-result` | `innerHTML` | Toast + table refresh |
| Chart load | Daily tab | `hx-get=".../drive/analytics/..."` | `#chart-container` | `innerHTML` | Per chart |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
