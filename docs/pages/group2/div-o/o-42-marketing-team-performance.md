# O-42 — Marketing Team Performance

> **URL:** `/group/marketing/admin/team-performance/`
> **File:** `o-42-marketing-team-performance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator; Telecaller Executive (130) — own metrics view

---

## 1. Purpose

The Marketing Team Performance page is the Campaign Manager's command centre for monitoring, measuring, and motivating every person on the marketing and admissions team. In a large Indian education group during peak admission season (February–April), 5–10 telecallers make 50,000–1,50,000 calls, the Campaign Manager runs 15–30 concurrent campaigns across branches, and the Content Coordinator uploads 200–500 creative assets. The difference between a group that fills 95% seats by April and one that struggles at 70% is not marketing budget — it is execution quality by individual team members.

The problems this page solves:

1. **Telecaller performance opacity:** The single biggest operational challenge in Indian admissions telecalling is variance. In a team of 8 telecallers, the top performer converts 12–15% of leads to walk-ins while the bottom performer converts 2–3%. Without per-person tracking, the Campaign Manager cannot: (a) identify who needs training vs who needs more leads, (b) redistribute workload from underperformers to high-converters during the critical March rush, (c) calculate per-conversion incentive payouts accurately. Many groups pay telecallers ₹50–200 per confirmed admission as incentive — with 500–2,000 admissions per season, this is a ₹2.5L–₹4L incentive pool that must be attributed accurately.

2. **No daily targets or accountability:** Without daily targets (e.g., 50 calls/day, 25 contacts, 5 walk-in bookings), telecallers self-pace. The system tracks hourly and daily call volumes, flags anyone below 50% of target by 2 PM, and auto-generates warnings. The Campaign Manager can intervene the same day — not discover underperformance in a weekly review when the leads have already gone cold.

3. **Campaign Manager self-measurement:** The Campaign Manager (119) also needs visibility into their own execution metrics: campaigns launched on time, lead response SLA (first contact within 4 hours of enquiry), enrollment drive progress vs targets, budget utilisation pacing. Without this, CEO reviews become subjective.

4. **Content Coordinator throughput:** During peak season, the Content Coordinator (131) must upload 10–20 new creatives per week (newspaper ads, WhatsApp banners, flex designs, social media posts). Branches request material and expect same-day turnaround. The page tracks upload velocity, approval rate (what percentage of uploaded assets get approved by Campaign Manager on first submission), and usage rate (what percentage of uploaded assets are actually used in campaigns).

5. **Gamification and motivation:** Indian telecalling teams respond strongly to visible leaderboards. When a telecaller sees "Priya: Rank #1, 48 calls, 8 walk-ins" on a shared screen, competition drives productivity. The page provides a real-time leaderboard with daily/weekly/monthly rankings, streak tracking (consecutive days above target), and achievement badges.

**Scale:** 5–15 team members tracked · 50–100 calls/person/day · 6-month admission season · ₹2L–₹5L incentive pool · 500–2,000 attributed conversions/season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — view all team members, set targets, view all metrics, calculate incentives, run performance reviews | Primary operator + own metrics |
| Group Admission Telecaller Executive | 130 | G3 | Read (own metrics only) — own calls, own conversion rate, own ranking, own incentive calculation | Cannot see other telecallers' individual data |
| Group Campaign Content Coordinator | 131 | G2 | Read (own metrics only) — own upload count, approval rate, usage rate | Cannot see telecaller data |
| Group Admission Data Analyst | 132 | G1 | Read + Export — all team metrics, aggregated analytics, MIS reports | No target setting |
| Group Topper Relations Manager | 120 | G3 | Read (own metrics only) — own events managed, topper records added | Limited to own role metrics |
| Group CEO | — | G4 | Read — full team dashboard, leaderboard, incentive reports | Strategic oversight |
| Group Chairman | — | G5 | Read + Override — can override targets, approve incentive payouts | Final authority |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Telecallers (130) see only `user_id = self`. Campaign Manager (119) sees all team members. Incentive payout approval: G4+ only. Target setting: role 119 or G4+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Administration  >  Marketing Team Performance
```

### 3.2 Page Header (Campaign Manager View — Role 119)
```
Marketing Team Performance                           [Set Targets]  [Calculate Incentives]  [Export Report]
Campaign Manager — Ramesh Venkataraman
Season 2026-27 · Team: 12 members · Today's Calls: 428/600 (71%) · Season Conversions: 1,847 · Incentive Pool: ₹3,42,000
```

### 3.3 Page Header (Telecaller View — Role 130)
```
My Performance                                       [My Targets]  [My Incentives]
Telecaller — Priya Reddy
Today: 52 calls · 28 contacts · 7 walk-ins · Season Rank: #2 of 8 · Streak: 14 days above target
```

### 3.4 Alert Banner (conditional — Campaign Manager only)

| Condition | Banner Text | Severity |
|---|---|---|
| Team below 50% of daily target by 2 PM | "Team at [X]% of daily call target — [N] telecallers below 50%" | Critical (red) |
| Any telecaller idle > 2 hours | "[Name] has made 0 calls in the last 2 hours — check status" | High (amber) |
| Incentive calculation pending for > 7 days | "Incentive calculation for [Period] is overdue — telecallers expecting payout" | Medium (yellow) |
| Underperformers (< 50% target for 3+ consecutive days) | "[N] telecallers below 50% target for 3+ days — intervention required" | High (amber) |
| Season target at risk | "Team conversion rate [X]% — below [Y]% target. [Z] working days remaining" | Critical (red) |

---

## 4. KPI Summary Bar (6 cards)

### 4.1 Campaign Manager View (Role 119)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Team Size | Integer | COUNT(active team members across all roles in Division O) | Static blue | `#kpi-team-size` |
| 2 | Avg Calls/Day (Team) | Decimal | SUM(telecaller calls today) / COUNT(active telecallers) | Green ≥ 50, Amber 30–49, Red < 30 | `#kpi-avg-calls` |
| 3 | Avg Conversion Rate | Percentage | Total walk-ins booked / Total contacts (season) × 100 | Green ≥ 12%, Amber 8–12%, Red < 8% | `#kpi-avg-conversion` |
| 4 | Top Performer | Name + metric | Telecaller with highest conversions this month | Static gold | `#kpi-top-performer` |
| 5 | Underperformers | Integer | COUNT(telecallers) WHERE daily_avg < 50% of target for last 3 days | Red > 0, Green = 0 | `#kpi-underperformers` |
| 6 | Team Target Achievement % | Percentage | Actual conversions / Season target × 100 | Green ≥ 90%, Amber 70–89%, Red < 70% | `#kpi-target-achievement` |

### 4.2 Telecaller Self-View (Role 130)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | My Calls Today | Integer | COUNT(my calls today) | Green ≥ target, Amber 70–99% target, Red < 70% | `#kpi-my-calls` |
| 2 | My Contact Rate | Percentage | Contacts / Calls today × 100 | Green ≥ 50%, Amber 35–49%, Red < 35% | `#kpi-my-contact-rate` |
| 3 | My Walk-ins Today | Integer | COUNT WHERE disposition = 'walk_in_booked' today | Static green | `#kpi-my-walkins` |
| 4 | My Rank | "#N of M" | Rank by conversions this month among telecallers | Gold = #1, Silver = #2, Bronze = #3, Static blue otherwise | `#kpi-my-rank` |
| 5 | My Streak | "N days" | Consecutive days where daily calls ≥ target | Green ≥ 7 days, Amber 3–6, Red = 0 | `#kpi-my-streak` |
| 6 | My Incentive (Est.) | ₹ Amount | Confirmed conversions × per-conversion rate (₹50–₹200) | Static green | `#kpi-my-incentive` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/admin/team-performance/kpis/"` → `hx-trigger="load, every 120s"`

---

## 5. Sections

### 5.1 Tab: Telecaller Performance (Campaign Manager view)

Real-time performance grid for all telecallers. This is the primary monitoring workspace.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Integer (badge) | No | Daily rank based on conversions — gold/silver/bronze icons for top 3 |
| Telecaller Name | Text (link) | Yes | Click opens individual performance drawer |
| Branch | Text | Yes | Primary assigned branch |
| Status | Badge | No | Online / On Call / Idle / Break / Offline |
| Daily Target | Integer | No | Configured daily call target |
| Calls Today | Integer / Target | Yes | E.g., "52/60" with progress bar |
| Contacts Today | Integer | Yes | Successfully connected calls |
| Contact Rate | Percentage | Yes | Contacts / Calls × 100 |
| Walk-ins Booked | Integer | Yes | Walk-in bookings today |
| Conversions (Month) | Integer | Yes | Confirmed admissions attributed this month |
| Conversion Rate | Percentage | Yes | Walk-ins / Contacts (monthly) × 100 |
| Avg Call Duration | Duration | Yes | Average call length today |
| Follow-ups Due | Integer | Yes | Pending follow-ups for today — Red if overdue > 0 |
| Overdue Follow-ups | Integer | Yes | Red if > 0 |
| Idle Time | Duration | No | Time since last call if currently idle |
| Actions | Buttons | No | [View Detail] [Assign Leads] [Set Target] |

**Default sort:** Rank ASC (top performer first)
**Auto-refresh:** Every 120 seconds
**Colour coding:**
- Green row: above target (calls ≥ daily target, conversion rate ≥ 12%)
- Amber row: on track (calls 70–99% of target)
- Red row: underperforming (calls < 70% of target or idle > 2 hours or conversion rate < 5%)

**Time period toggle:** Today / This Week / This Month / This Season
- When period changes, columns adjust: "Calls Today" becomes "Calls This Week" etc.
- Rank recalculates based on selected period

### 5.2 Tab: Campaign Manager Metrics (Self-view or CEO view)

Tracks the Campaign Manager's (119) own execution quality.

**Metrics table:**

| Metric | Target | Actual | Achievement % | Notes |
|---|---|---|---|---|
| Campaigns launched on time | 100% | [X]% | — | Campaigns that started on their planned date |
| Lead response SLA (< 4 hours) | 95% | [X]% | — | First telecaller contact within 4 hours of enquiry |
| Lead assignment backlog | 0 | [N] leads | — | Unassigned leads older than 24 hours |
| Budget utilisation pacing | On track | [Status] | — | Budget spend vs linear projection for this point in season |
| Enrollment drive targets | [Target] | [Actual] seats | [X]% | Cross-branch seat fill vs plan |
| Vendor deliverable on-time % | 90% | [X]% | — | Vendor deliverables received on or before due date |
| Weekly MIS report submitted | Yes/No | — | — | Did Campaign Manager submit weekly MIS to CEO on time? |

### 5.3 Tab: Content Coordinator Metrics

Tracks Content Coordinator (131) asset management throughput.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Coordinator Name | Text | Yes | Content Coordinator name |
| Assets Uploaded (Period) | Integer | Yes | Total creative assets uploaded |
| Assets Approved (First Pass) | Integer | Yes | Approved without revision |
| First-Pass Approval Rate | Percentage | Yes | Green ≥ 80%, Amber 60–79%, Red < 60% |
| Assets In Revision | Integer | Yes | Sent back for changes |
| Assets Used in Campaigns | Integer | Yes | Assets actually deployed in live campaigns |
| Usage Rate | Percentage | Yes | Used / Uploaded × 100 — measures relevance |
| Avg Turnaround Time | Duration | Yes | Upload to approval average time |
| Pending Branch Requests | Integer | Yes | Open material requests from branches — Red > 5 |
| Actions | Buttons | No | [View Detail] |

**Time period toggle:** This Week / This Month / This Season

### 5.4 Tab: Gamification Leaderboard

Real-time competitive leaderboard for telecallers. Designed to be displayed on a shared screen in the telecalling room.

**Leaderboard display (not a traditional table — card-based):**

```
┌──────────────────────────────────────────────────────────────────────┐
│  🏆 TELECALLER LEADERBOARD — March 2026                            │
│                                                                      │
│  #1  Priya Reddy        148 conversions  │ 🔥 Streak: 22 days       │
│  #2  Arun Kumar         131 conversions  │ 🔥 Streak: 18 days       │
│  #3  Sneha Patil        119 conversions  │ 🔥 Streak: 14 days       │
│  #4  Mohammed Rafi       98 conversions  │    Streak: 8 days        │
│  #5  Kavitha Nair        87 conversions  │    Streak: 5 days        │
│  #6  Rajesh Sharma       72 conversions  │    Streak: 2 days        │
│  #7  Deepa Kumari        61 conversions  │    Streak: 0 days ⚠️     │
│  #8  Suresh Babu         43 conversions  │    Streak: 0 days ⚠️     │
│                                                                      │
│  Today's Star: Priya Reddy — 12 walk-ins booked                    │
│  Team Total: 759 conversions | Target: 900 | Gap: 141 (84.3%)       │
└──────────────────────────────────────────────────────────────────────┘
```

**Leaderboard columns (data backing):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Rank | Badge | No | Gold #1 / Silver #2 / Bronze #3 / numeric rest |
| Telecaller Name | Text | No | — |
| Conversions (Period) | Integer | No | Walk-in bookings that converted to enrollment |
| Calls Made | Integer | No | Total calls in period |
| Contact Rate | Percentage | No | Contacts / Calls |
| Walk-in Booking Rate | Percentage | No | Walk-ins / Contacts |
| Streak | Integer + icon | No | Consecutive days above daily target |
| Achievement Badges | Icons | No | Sprint King (most calls/day), Closer (best conversion), Consistent (30-day streak), Century (100 conversions/month) |

**Time period toggle:** Today / This Week / This Month / This Season
**Auto-refresh:** Every 60 seconds (designed for always-on display)

**Achievement badges (full list):**

| Badge | Criteria | Icon |
|---|---|---|
| Sprint King | Most calls in a single day (≥ 80 calls) | Lightning bolt |
| The Closer | Highest conversion rate in a month (≥ 15%) | Target |
| Consistency Champion | 30 consecutive days above daily target | Shield |
| Century Club | 100+ conversions in a calendar month | Star |
| Follow-up Master | Zero overdue follow-ups for 14 consecutive days | Checkmark |
| Rising Star | Biggest week-over-week improvement (≥ 50%) | Arrow up |
| Early Bird | First to hit daily target for 10 consecutive days | Sun |
| Team Player | Highest contact rate for walk-in handoff to branches | Handshake |

### 5.5 Tab: Target Management (Campaign Manager only)

Configuration page for individual and team targets.

**Target configuration table:**

| Column | Type | Notes |
|---|---|---|
| Team Member | Text | Name + role |
| Role | Badge | Telecaller / Campaign Manager / Content Coordinator |
| Daily Call Target | Integer (editable) | Default: 50 for telecaller, N/A for others |
| Daily Contact Target | Integer (editable) | Default: 25 |
| Daily Walk-in Target | Integer (editable) | Default: 5 |
| Monthly Conversion Target | Integer (editable) | Default: 100 |
| Season Conversion Target | Integer (editable) | Calculated from monthly × remaining months |
| Incentive Rate | ₹ (editable) | Per-conversion incentive amount (₹50–₹200) |
| Effective From | Date | When target takes effect |
| Actions | Buttons | [Save] [Reset to Default] [View History] |

**Target adjustment rules:**
- Targets can only be increased mid-month (not decreased — prevents gaming)
- Decrease requires G4+ approval
- All target changes logged with reason and approver
- Seasonal targets auto-calculated from monthly targets × remaining months

### 5.6 Tab: Incentive Calculator (Campaign Manager only)

Calculates per-telecaller incentive payouts based on confirmed conversions.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Telecaller | Text | Yes | Name |
| Period | Badge | No | Month being calculated |
| Confirmed Conversions | Integer | Yes | Admissions where fee paid AND attributed to this telecaller |
| Disputed Conversions | Integer | Yes | Conversions where attribution is contested (e.g., walk-in vs telecall) |
| Incentive Rate | ₹ | No | Per-conversion rate for this telecaller |
| Gross Incentive | ₹ Amount | Yes | Confirmed × Rate |
| Bonus (Target Exceeded) | ₹ Amount | Yes | Additional bonus for exceeding monthly target by > 20% |
| Total Payout | ₹ Amount | Yes | Gross + Bonus |
| Approval Status | Badge | Yes | Draft / Submitted / Approved / Paid |
| Actions | Buttons | No | [Review Conversions] [Submit for Approval] |

**Incentive rules:**
- Base incentive: ₹[X] per confirmed conversion (configurable per telecaller)
- Target exceeded bonus: if monthly conversions > 120% of target, additional ₹[Y] per conversion above target
- Attribution rule: conversion attributed to the telecaller who booked the walk-in (not the last caller)
- Disputed conversions: Campaign Manager resolves attribution before submission
- Approval workflow: Campaign Manager calculates → CEO (G4) approves → Finance processes payout
- Payment frequency: monthly (calculated by 5th of following month)

---

## 6. Drawers & Modals

### 6.1 Modal: `set-targets` (560px)

- **Title:** "Set Performance Targets"
- **Scope:** Individual telecaller or bulk (all telecallers)
- **Fields:**
  - Target for (dropdown: individual telecaller / all telecallers)
  - If individual: telecaller name (dropdown)
  - Daily call target (integer, required, min 20, max 150)
  - Daily contact target (integer, required)
  - Daily walk-in target (integer, required)
  - Monthly conversion target (integer, required)
  - Incentive rate per conversion (₹, required, min ₹10, max ₹500)
  - Effective from (date, required, must be ≥ today)
  - Reason for change (textarea, required if modifying existing target)
- **Validation:**
  - Contact target ≤ call target (you cannot contact more than you call)
  - Walk-in target ≤ contact target
  - If reducing any target: requires G4+ approval — show warning "Target reduction requires CEO approval"
- **Buttons:** Cancel · Save Targets
- **Access:** Role 119 or G4+

### 6.2 Drawer: `individual-performance` (720px, right-slide)

- **Title:** "[Name] — Performance Deep Dive"
- **Tabs:** Today · This Week · This Month · This Season · Incentives
- **Today tab:**
  - Call log table: time, lead name, duration, disposition, outcome
  - Hourly call volume sparkline (8 AM – 8 PM)
  - Current queue size, pending follow-ups, overdue follow-ups
  - Real-time stats: calls, contacts, walk-ins, contact rate, avg duration
- **This Week tab:**
  - Daily breakdown table: Mon–Sat with calls, contacts, walk-ins, conversion rate
  - Week total + daily average
  - Comparison with team average (inline bar)
  - Trend vs previous week (arrow up/down with %)
- **This Month tab:**
  - Weekly breakdown table (Week 1–4)
  - Monthly total vs target (progress bar)
  - Disposition breakdown donut (same chart as O-18 §7.2 but individual)
  - Top 5 converting leads (which leads they converted, with source)
  - Conversion funnel: Calls → Contacts → Walk-ins → Admissions
- **This Season tab:**
  - Monthly trend line (calls, contacts, conversions over season months)
  - Season total vs target
  - Rank history (line chart — how rank has changed month over month)
  - Cumulative conversions vs linear target projection
  - Badges earned (with dates)
- **Incentives tab:**
  - Monthly incentive history table: month, conversions, rate, gross, bonus, total, status (paid/pending)
  - Season total earned + pending
  - Disputed conversions with details
- **Footer:** [Assign More Leads] [Adjust Target] [Download Report] [Start Performance Review]
- **Access:** Role 119 (all telecallers), 130 (own only), G4+ (all)

### 6.3 Modal: `incentive-calculator` (640px)

- **Title:** "Calculate Incentives — [Month Year]"
- **Fields:**
  - Calculation period (month-year dropdown)
  - Auto-populated table:
    - Telecaller | Confirmed | Disputed | Rate | Gross | Bonus | Total
  - For each telecaller: [Review Conversions] link (opens list of attributed admissions)
  - Dispute resolution: for each disputed conversion, select attribution (Telecaller A / Telecaller B / Walk-in — no attribution)
  - Total incentive pool: ₹[X] (auto-calculated)
  - Budget check: "Available incentive budget: ₹[Y] — [Sufficient / Exceeded by ₹Z]"
- **Buttons:** Cancel · Save as Draft · Submit for CEO Approval
- **Access:** Role 119 (calculate + submit), G4+ (approve)

### 6.4 Modal: `performance-review-template` (560px)

- **Title:** "Performance Review — [Name]"
- **Fields:**
  - Review period (dropdown: monthly / quarterly / season-end)
  - Auto-populated metrics summary (from individual performance data)
  - Strengths (textarea — 3 mandatory bullet points)
  - Areas for improvement (textarea — 2 mandatory bullet points)
  - Training needs identified (multi-select: Pitch delivery / Objection handling / Product knowledge / Call etiquette / Follow-up discipline / Time management / CRM usage / Other)
  - Recommended action (dropdown: Continue as-is / Additional training / Role change / Performance improvement plan / Recognition/promotion)
  - Manager rating (1–5 stars)
  - Notes / discussion summary (textarea)
- **Buttons:** Cancel · Save Draft · Submit Review
- **Access:** Role 119 (create reviews for team), G4+ (view all reviews)

---

## 7. Charts

### 7.1 Telecaller Ranking — Monthly Conversions (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Telecaller Conversions — [Current Month]" |
| Data | Confirmed conversions per telecaller, sorted DESC |
| X-axis | Conversion count |
| Y-axis | Telecaller name |
| Colour | Top 3: `#F59E0B` gold, `#9CA3AF` silver, `#CD7F32` bronze / Rest: `#3B82F6` blue / Below 50% target: `#EF4444` red |
| Target line | Monthly target per telecaller (dashed grey vertical) |
| Tooltip | "[Name]: [N] conversions ([X]% of target) — ₹[Y] incentive earned" |
| API | `GET /api/v1/group/{id}/marketing/admin/team-performance/analytics/telecaller-ranking/` |

### 7.2 Conversion Rate Trend — Per Person (Multi-line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Weekly Conversion Rate Trend — Last 8 Weeks" |
| Data | Weekly conversion rate (walk-ins / contacts × 100) per telecaller |
| X-axis | Week (W1–W8) |
| Y-axis | Conversion rate (%) |
| Colour | One colour per telecaller (max 10 lines) + `#9CA3AF` dashed for team average |
| Legend | Telecaller names — click to show/hide individual lines |
| Tooltip | "[Name] — [Week]: [X]% conversion ([N] walk-ins from [M] contacts)" |
| API | `GET /api/v1/group/{id}/marketing/admin/team-performance/analytics/conversion-trend/` |

### 7.3 Daily Call Volume — Team (Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Daily Call Volume by Telecaller — This Week" |
| Data | Daily calls per telecaller (stacked segments) |
| X-axis | Day (Mon–Sat) |
| Y-axis | Call count |
| Colour | One colour per telecaller |
| Target line | Team daily target (dashed red horizontal) |
| Tooltip | "[Day] — [Name]: [N] calls | Team total: [T]" |
| API | `GET /api/v1/group/{id}/marketing/admin/team-performance/analytics/daily-volume/` |

### 7.4 Team Target vs Actual — Season (Gauge)

| Property | Value |
|---|---|
| Chart type | Gauge / Doughnut (Chart.js 4.x with doughnut cutout 75%) |
| Title | "Season Conversion Target Progress" |
| Data | Actual conversions vs season target |
| Colour | Green ≥ 90%, Amber 70–89%, Red < 70% — filled arc |
| Centre text | "[X]% — [Actual]/[Target] conversions" |
| Sub-text | "[N] working days remaining" |
| API | `GET /api/v1/group/{id}/marketing/admin/team-performance/analytics/season-gauge/` |

### 7.5 Individual Performance Radar (per telecaller — in drawer)

| Property | Value |
|---|---|
| Chart type | Radar (Chart.js 4.x) |
| Title | "[Name] — Performance Profile" |
| Axes (6) | Call Volume / Contact Rate / Conversion Rate / Follow-up Compliance / Call Quality / Streak Consistency |
| Data | Individual score (0–100 normalised) on each axis + team average overlay |
| Colour | Individual: `#3B82F6` blue fill (opacity 0.3) / Team avg: `#9CA3AF` grey dashed |
| Tooltip | "[Axis]: [X] (Team avg: [Y])" |
| Purpose | Visual strengths/weaknesses identification for training decisions |
| API | `GET /api/v1/group/{id}/marketing/admin/team-performance/analytics/radar/{user_id}/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Targets saved | "Targets updated for [Name] — effective from [Date]" | Success | 3s |
| Targets saved (bulk) | "Targets updated for [N] telecallers — effective from [Date]" | Success | 3s |
| Target reduction submitted | "Target reduction request submitted for CEO approval" | Info | 3s |
| Incentive calculated | "Incentives calculated for [Month]: ₹[X] total for [N] telecallers" | Success | 4s |
| Incentive submitted for approval | "Incentive payout of ₹[X] submitted for CEO approval" | Info | 3s |
| Incentive approved | "Incentive payout approved — ₹[X] for [N] telecallers" | Success | 4s |
| Performance review saved | "Performance review saved for [Name]" | Success | 2s |
| Underperformer alert | "[Name] is at [X]% of daily target — 0 calls in last [N] hours" | Warning | 5s |
| Streak milestone | "[Name] has achieved a [N]-day streak! Badge: [Badge Name]" | Success | 4s |
| Badge earned | "[Name] earned the [Badge Name] badge!" | Success | 4s |
| Team target reached | "Team has reached [X]% of monthly target — [N] conversions!" | Success | 5s |
| Export complete | "Team performance report exported — [filename].csv" | Success | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No team members configured | 👥 | "No Team Members" | "Add marketing team members and set their roles to start tracking performance." | Configure Team (Admin) |
| No targets set | 🎯 | "No Targets Configured" | "Set daily and monthly targets for telecallers to enable performance tracking." | Set Targets |
| No calls logged today | 📞 | "No Calls Today" | "Telecallers haven't logged any calls yet today. Ensure they are using the Telecalling Manager (O-18)." | — |
| No conversions this month | 📊 | "No Conversions Yet" | "No confirmed admissions attributed to telecallers this month." | — |
| No incentive history | 💰 | "No Incentives Calculated" | "Calculate your first monthly incentive payout using the Incentive Calculator." | Calculate Incentives |
| Telecaller self-view — no data | 📋 | "No Activity Yet" | "Start making calls from your Telecalling Manager (O-18) to see your performance here." | Go to Telecalling Manager |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + table skeleton (8 rows) |
| Telecaller performance grid | 8-row table skeleton with progress bars |
| Campaign Manager metrics | 7-row metric card skeleton |
| Content Coordinator metrics | 4-row table skeleton |
| Leaderboard | Card skeleton (8 entries) with rank badges |
| Target management tab | 10-row editable table skeleton |
| Incentive calculator | 8-row table skeleton with amount columns |
| Individual performance drawer | 720px skeleton: header + 5 tab placeholders + chart grey |
| Chart load | Grey canvas placeholder per chart |
| Radar chart (in drawer) | Hexagonal grey placeholder |
| Auto-refresh (120s cycle) | Silent refresh — no visible loader; data swaps in place |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/` | G1+ | Team overview (all members, current period) |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/kpis/` | G1+ | KPI values (role-contextual) |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/telecallers/` | G3+ (119) | Telecaller performance grid |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/telecallers/{user_id}/` | G3+ (119/self) | Individual telecaller deep dive |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/telecallers/{user_id}/calls/` | G3+ (119/self) | Individual call log for period |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/telecallers/{user_id}/incentives/` | G3+ (119/self) | Individual incentive history |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/campaign-manager/` | G3+ (119/G4+) | Campaign Manager metrics |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/content-coordinator/` | G2+ (131/119/G4+) | Content Coordinator metrics |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/leaderboard/` | G1+ | Leaderboard data (period parameterised) |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/targets/` | G3+ (119) | Current targets for all team members |
| POST | `/api/v1/group/{id}/marketing/admin/team-performance/targets/` | G3+ (119) | Set / update targets |
| PATCH | `/api/v1/group/{id}/marketing/admin/team-performance/targets/{target_id}/` | G3+ (119) | Modify individual target |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/targets/history/` | G3+ (119) | Target change history |
| POST | `/api/v1/group/{id}/marketing/admin/team-performance/incentives/calculate/` | G3+ (119) | Calculate incentives for period |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/incentives/` | G3+ (119) | Incentive calculations list |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/incentives/{calc_id}/` | G3+ (119) | Incentive calculation detail |
| PATCH | `/api/v1/group/{id}/marketing/admin/team-performance/incentives/{calc_id}/submit/` | G3+ (119) | Submit for CEO approval |
| PATCH | `/api/v1/group/{id}/marketing/admin/team-performance/incentives/{calc_id}/approve/` | G4+ | Approve incentive payout |
| POST | `/api/v1/group/{id}/marketing/admin/team-performance/reviews/` | G3+ (119) | Create performance review |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/reviews/` | G3+ (119/G4+) | List all performance reviews |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/analytics/telecaller-ranking/` | G1+ | Ranking bar chart |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/analytics/conversion-trend/` | G1+ | Conversion rate multi-line |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/analytics/daily-volume/` | G1+ | Daily call volume stacked bar |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/analytics/season-gauge/` | G1+ | Season progress gauge |
| GET | `/api/v1/group/{id}/marketing/admin/team-performance/analytics/radar/{user_id}/` | G3+ (119/self) | Individual radar chart |
| POST | `/api/v1/group/{id}/marketing/admin/team-performance/export/` | G1+ | Export team performance report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../team-performance/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 120s"` |
| Telecaller grid | Tab click | `hx-get=".../team-performance/telecallers/"` | `#tab-content` | `innerHTML` | `hx-trigger="load"` |
| Telecaller grid refresh | Auto-refresh | `hx-get=".../team-performance/telecallers/"` | `#telecaller-grid` | `innerHTML` | `hx-trigger="every 120s"` |
| Campaign Manager tab | Tab click | `hx-get=".../team-performance/campaign-manager/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Content Coordinator tab | Tab click | `hx-get=".../team-performance/content-coordinator/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Leaderboard | Tab click | `hx-get=".../team-performance/leaderboard/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Leaderboard auto-refresh | Always-on display | `hx-get=".../team-performance/leaderboard/"` | `#leaderboard` | `innerHTML` | `hx-trigger="every 60s"` |
| Target management tab | Tab click | `hx-get=".../team-performance/targets/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Incentive tab | Tab click | `hx-get=".../team-performance/incentives/"` | `#tab-content` | `innerHTML` | `hx-trigger="click"` |
| Set targets | Form submit | `hx-post=".../team-performance/targets/"` | `#target-result` | `innerHTML` | Toast + target table refresh |
| Individual drawer | Row click | `hx-get=".../team-performance/telecallers/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab click in drawer | `hx-get` with period param | `#drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Calculate incentives | Form submit | `hx-post=".../team-performance/incentives/calculate/"` | `#incentive-result` | `innerHTML` | Toast + table update |
| Submit incentive | Submit button | `hx-patch=".../team-performance/incentives/{id}/submit/"` | `#incentive-row-{id}` | `outerHTML` | Status badge update |
| Approve incentive | Approve button | `hx-patch=".../team-performance/incentives/{id}/approve/"` | `#incentive-row-{id}` | `outerHTML` | Status badge update (G4+ only) |
| Period toggle | Dropdown change | `hx-get` with `?period={value}` | `#tab-content` | `innerHTML` | `hx-trigger="change"` |
| Radar chart | Drawer load | `hx-get=".../team-performance/analytics/radar/{id}/"` | `#radar-chart` | `innerHTML` | Loaded inside drawer |
| Chart load | Chart containers | `hx-get=".../team-performance/analytics/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="load"` |
| Export | Export button | `hx-post=".../team-performance/export/"` | `#export-result` | `innerHTML` | Toast with download link |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
