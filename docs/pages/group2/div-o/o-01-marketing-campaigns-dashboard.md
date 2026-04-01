# O-01 — Marketing & Campaigns Dashboard

> **URL:** `/group/marketing/dashboard/`
> **File:** `o-01-marketing-campaigns-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary landing page for entire Marketing & Admissions Campaigns division

---

## 1. Purpose

The Marketing & Campaigns Dashboard is the central command centre for the Group Admissions Campaign Manager and all marketing-related roles within an Institution Group. It aggregates admission campaign health data from all branches into a single unified view: how many enquiries came in today, how many converted, what percentage of seats are filled, which branches are lagging, which campaigns are burning budget without returns, and which telecallers are under-performing.

In the Indian education market, admission season is a 7-month war (November–July). A large group like Narayana or Sri Chaitanya runs 50+ branches, each with different seat targets (Day Scholar MPC, Day Scholar BiPC, Hosteler Boys AC, Hosteler Girls Non-AC, Integrated JEE/NEET). The total seat count can exceed 50,000. Every unfilled seat is lost revenue for 12 months — there is no mid-year recovery. This dashboard exists to ensure not a single seat slips through the cracks.

The dashboard serves three audiences simultaneously:

1. **Admissions Campaign Manager (Role 119, G3):** Daily operational view — leads today, calls made, conversions, pending follow-ups, campaign status, branch-wise seat fill. This is the role's morning briefing and end-of-day review screen.
2. **Telecaller Executives (Role 130, G3):** Quick summary of own performance — calls made, leads converted, follow-ups due. Limited view filtered to own data.
3. **CEO/Chairman (G4/G5):** Executive summary — group-wide seat fill percentage, total spend vs budget, cost-per-admission trend, top/bottom branches. One glance = admissions health.

The page is the mandatory landing page when any Division O user logs in. Data refreshes every 2 minutes during peak season (Feb–Apr), every 5 minutes otherwise. All metric cards, alert banners, and charts are driven by HTMX polling or on-load lazy fetch. No write operations are available from this page — it is a read-only synthesis layer; actual actions are performed on the respective sub-module pages.

**Scale:** 5–50 branches · 200–10,000 leads per day during peak · 15,000–50,000 total seats · ₹2–10 Cr annual marketing budget

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Marketing Director | 114 | G0 | No Platform Access | External tools only — no login |
| Group Brand Manager | 115 | G0 | No Platform Access | External tools only |
| Group Digital Marketing Executive | 116 | G0 | No Platform Access | External tools only |
| Group PR & Communications Manager | 117 | G0 | No Platform Access | External tools only |
| Group Social Media Manager | 118 | G0 | No Platform Access | External tools only |
| Group Admissions Campaign Manager | 119 | G3 | Full Dashboard — all widgets, all branches | Primary user; morning briefing screen |
| Group Topper Relations Manager | 120 | G3 | Read — Topper KPI card + Topper section only | Limited to topper-related widgets |
| Group Admission Telecaller Executive | 130 | G3 | Read — Own performance card + own lead count | Filtered to own data only |
| Group Campaign Content Coordinator | 131 | G2 | Read — Material library KPI card only | Limited view |
| Group Admission Data Analyst | 132 | G1 | Read — Full Dashboard (all widgets) | View-only; no actions; export enabled |

> **Access enforcement:** `@require_role(min_level=G1, division='O')` on all views and API endpoints. Telecaller view uses `queryset.filter(assigned_to=request.user)`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Dashboard
```

### 3.2 Page Header
```
Marketing & Campaigns Dashboard                [Season: 2026-27 ▾]  [Export PDF]  [Settings ⚙]
Group Admissions Campaign Manager — Ramesh Venkataraman
Sunrise Education Group · 28 branches · Admission Season: Active (Phase 4 — Peak)
Last refreshed: 1 min ago · Auto-refresh: ON (every 2 min)
```

**Season selector:** Dropdown showing all admission seasons (2026-27, 2025-26, 2024-25). Current season is default. Historical seasons are read-only for comparison.

### 3.3 Alert Banner (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Any branch below 50% seat fill after March 31 | "CRITICAL: [N] branch(es) below 50% seat fill — immediate intervention required" | Critical (red) |
| Group-wide seat fill below 70% after April 15 | "WARNING: Group seat fill at [X]% — below 70% threshold. Escalate to CEO." | Critical (red) |
| Daily lead count drops > 30% vs same day last week | "Lead volume dropped [X]% vs last week. Check campaign status and spend." | High (amber) |
| Campaign budget exhausted for any active campaign | "Campaign '[Name]' budget exhausted — [X] days remaining in schedule. Pause or top-up." | High (amber) |
| Telecaller team: > 20% follow-ups overdue | "[N] overdue follow-ups across telecalling team. Escalate pending callbacks." | Medium (yellow) |
| WhatsApp/SMS DLT template expiring within 7 days | "DLT template '[Name]' expires in [N] days. Renew to avoid message failures." | Medium (yellow) |
| No leads recorded for any branch in last 48 hours | "No enquiries received for [Branch] in 48 hours. Verify campaign is live." | High (amber) |

---

## 4. KPI Summary Bar (10 cards)

### Row 1 — Admission Health (5 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Seats (Group) | Integer | SUM(branch_seats) for current season, all branches, all streams | Static blue | `#kpi-total-seats` |
| 2 | Seats Filled | Integer + % | SUM(enrolled_students) / SUM(branch_seats) × 100 | Green ≥ 85%, Amber 60–84%, Red < 60% | `#kpi-seats-filled` |
| 3 | Leads Today | Integer | COUNT(enquiries) WHERE created_date = TODAY | Green > daily target, Amber 50–100% of target, Red < 50% | `#kpi-leads-today` |
| 4 | Conversions This Month | Integer | COUNT(enrolled) WHERE enrollment_date within current month | Green ≥ monthly target, Amber 50–99%, Red < 50% | `#kpi-conversions-month` |
| 5 | Conversion Rate (Season) | Percentage | COUNT(enrolled) / COUNT(enquiries) × 100 for current season | Green ≥ 15%, Amber 8–14%, Red < 8% | `#kpi-conversion-rate` |

### Row 2 — Operations & Spend (5 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 6 | Calls Made Today | Integer | COUNT(call_logs) WHERE call_date = TODAY | Green ≥ daily team target, Amber 50–99%, Red < 50% | `#kpi-calls-today` |
| 7 | Pending Follow-ups | Integer | COUNT(follow_ups) WHERE due_date ≤ TODAY AND status = 'pending' | Red > 50, Amber 20–50, Green < 20 | `#kpi-pending-followups` |
| 8 | Budget Spent (Season) | ₹ Amount + % | SUM(campaign_spend) / SUM(campaign_budget) × 100 | Green < 80% spent, Amber 80–95%, Red > 95% | `#kpi-budget-spent` |
| 9 | Cost per Admission (CPA) | ₹ Amount | SUM(campaign_spend) / COUNT(enrolled) | Green ≤ ₹2,000, Amber ₹2,001–₹5,000, Red > ₹5,000 | `#kpi-cpa` |
| 10 | Active Campaigns | Integer | COUNT(campaigns) WHERE status = 'active' | Static blue | `#kpi-active-campaigns` |

**HTMX:** All 10 cards use `hx-get="/api/v1/group/{id}/marketing/dashboard/kpis/"` with `hx-trigger="load, every 120s"` (2 min during peak season). Individual targets allow partial refresh. 120-second refresh ensures lead volume and call counts stay near real-time during admission rush.

---

## 5. Sections

### 5.1 Seat Fill Progress — Branch-wise

The most critical section. Shows every branch with its total seats, filled seats, fill percentage, and a progress bar. This is what the CEO looks at first.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Branch | Text + City | Yes | Branch name + city; click opens O-22 filtered to branch |
| Zone | Text | Yes | Zone name (large groups only; blank for small) |
| Total Seats | Integer | Yes | All streams combined for this branch |
| Filled | Integer | Yes | Enrolled + fee paid |
| Fill % | Progress bar + % | Yes | Filled / Total × 100; green ≥ 85, amber 60–84, red < 60 |
| Leads (This Month) | Integer | Yes | Enquiries received this month for this branch |
| Conversion % | Percentage | Yes | Enrolled / Enquiries this season |
| Top Source | Badge | No | Highest-lead source for this branch: Newspaper / Digital / Walk-in / Referral |
| Trend | Sparkline | No | Weekly fill % trend — last 8 weeks |
| Action | Button | No | "Details →" opens O-22 filtered |

**Default sort:** Fill % ASC (worst-performing first — intervention priority)
**Pagination:** Server-side · Default 25/page · Shows all branches if ≤ 50
**Filter chips:** `All` · `Below 60%` · `60–85%` · `Above 85%` · `Zone: [dropdown]`
**Search:** Branch name — debounced 350ms

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/seat-fill/"` → `hx-target="#seat-fill-table-body"` → `hx-trigger="load, every 300s"`

### 5.2 Lead Pipeline Summary

Funnel visualization showing the admission pipeline stages group-wide. Each stage shows count and drop-off from previous stage.

**Pipeline Stages:**

| Stage | Count Source | Drop-off Calc |
|---|---|---|
| New Enquiries | COUNT leads WHERE status = 'new' | — |
| Contacted | COUNT leads WHERE status = 'contacted' | (New − Contacted) / New × 100 |
| Interested | COUNT leads WHERE status = 'interested' | (Contacted − Interested) / Contacted × 100 |
| Walk-in / Demo Booked | COUNT leads WHERE status IN ('walkin_booked', 'demo_booked') | (Interested − Booked) / Interested × 100 |
| Counselling Done | COUNT leads WHERE status = 'counselled' | (Booked − Counselled) / Booked × 100 |
| Application Submitted | COUNT leads WHERE status = 'applied' | (Counselled − Applied) / Counselled × 100 |
| Seat Offered | COUNT leads WHERE status = 'offered' | (Applied − Offered) / Applied × 100 |
| Fee Paid (Enrolled) | COUNT leads WHERE status = 'enrolled' | (Offered − Enrolled) / Offered × 100 |

**Display:** Horizontal funnel bar chart. Each stage is a coloured bar; width proportional to count. Drop-off percentages shown between bars in red text. Click on any stage opens O-15 filtered to that stage.

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/pipeline-summary/"` → `hx-target="#pipeline-funnel"` → `hx-trigger="load, every 300s"`

### 5.3 Today's Activity Feed

Real-time feed of notable events across all branches, sorted newest first. Maximum 50 items displayed; older items accessible via "View All →" link to audit log.

**Event Types:**

| Event | Icon | Example Text |
|---|---|---|
| New lead (bulk) | 📋 | "42 new enquiries added from WhatsApp campaign 'Early Bird 2026' — Nampally branch" |
| Conversion | ✅ | "Rajesh K. (MPC, Hosteler Boys AC) enrolled — Kukatpally branch — Source: Newspaper" |
| Walk-in recorded | 🚶 | "Walk-in enquiry: Parent Mrs. Lakshmi — interested in Class 6 IIT Foundation — Dilsukhnagar" |
| Campaign launched | 🚀 | "Campaign 'February Blitz' activated — 8 branches, budget ₹12L, channels: Newspaper + WhatsApp" |
| Campaign paused/ended | ⏸️ | "Campaign 'January Early Bird' ended — 2,340 leads, 186 conversions, CPA ₹1,890" |
| Budget alert | ⚠️ | "Campaign 'Digital Push Q1' — 90% budget consumed, 18 days remaining" |
| Telecalling milestone | 📞 | "Telecalling team: 500 calls completed today (target: 400)" |
| Topper added | 🏆 | "New topper: Priya S. — JEE Advanced AIR 234 — added to Topper Database" |
| Follow-up overdue | 🔴 | "28 follow-ups overdue > 3 days — escalated to Campaign Manager" |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/activity-feed/"` → `hx-target="#activity-feed"` → `hx-trigger="load, every 60s"` (1-min refresh for near real-time)

### 5.4 Campaign Status Cards

Horizontal scrollable row of cards showing each active campaign. Each card is a mini-dashboard for one campaign.

**Card Layout:**

```
┌──────────────────────────────────────────┐
│  📰 February Newspaper Blitz             │
│  Status: Active · Day 12 of 30           │
│                                          │
│  Budget: ₹8,00,000                       │
│  Spent:  ₹4,20,000 (52%)  ████████░░░░  │
│                                          │
│  Leads: 1,240    Conversions: 86         │
│  CPL: ₹339       CPA: ₹4,884            │
│                                          │
│  Branches: 12/28  Channels: Newspaper    │
│  [View Details →]                        │
└──────────────────────────────────────────┘
```

**Fields per card:**
- Campaign name + channel icon (📰 newspaper, 📱 digital, 💬 WhatsApp, 🏗️ outdoor, 📧 email)
- Status badge: Active (green) / Paused (amber) / Ended (grey) / Scheduled (blue)
- Day X of Y progress
- Budget bar: spent vs total
- Lead count + conversion count
- CPL (Cost per Lead) + CPA (Cost per Admission)
- Branch count targeted
- "View Details →" link to O-08 campaign detail

**Max visible:** 4 cards; horizontal scroll for more
**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/campaign-cards/"` → `hx-target="#campaign-cards"` → `hx-trigger="load, every 300s"`

### 5.5 Telecalling Team Summary

Table showing telecaller-wise performance for today and this month. Visible to Campaign Manager (119) and G4/G5. Telecallers (130) see only own row.

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Telecaller | Text | Yes | Name + employee ID |
| Calls Today | Integer | Yes | Total calls made today |
| Connected | Integer | Yes | Calls where conversation happened (not voicemail/no-answer) |
| Interested | Integer | Yes | Leads marked 'interested' after call |
| Conversions (Month) | Integer | Yes | Leads that enrolled this month from this telecaller's pipeline |
| Follow-ups Due | Integer | Yes | Pending follow-ups due today or overdue |
| Avg Call Duration | Time | Yes | Average duration of connected calls today |
| Conversion Rate | Percentage | Yes | Conversions / Total assigned leads × 100 |

**Default sort:** Calls Today DESC
**Pagination:** None (max 10–15 telecallers)
**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/telecalling-summary/"` → `hx-target="#telecalling-table"` → `hx-trigger="load, every 120s"`

### 5.6 Source-wise Lead Breakdown

Horizontal bar chart showing lead volume by source for the current month. Each bar is colour-coded by source type.

**Sources tracked:**

| Source | Colour | Typical Share |
|---|---|---|
| Newspaper Ad | `#1E40AF` (dark blue) | 25–35% |
| WhatsApp Campaign | `#059669` (green) | 15–25% |
| Walk-in (Direct) | `#D97706` (amber) | 15–20% |
| Digital (Google/Meta) | `#7C3AED` (purple) | 10–15% |
| Parent Referral | `#DC2626` (red) | 8–12% |
| School Fair / Exhibition | `#0891B2` (teal) | 5–8% |
| Open Day Event | `#BE185D` (pink) | 3–5% |
| Alumni Referral | `#4B5563` (grey) | 2–3% |
| Other / Unattributed | `#9CA3AF` (light grey) | 2–5% |

Click on any bar opens O-16 filtered to that source.

### 5.7 Topper Spotlight (Seasonal)

Visible only during results season (May–July). Shows the latest toppers added to the platform with their rank, branch, and stream. Quick link to O-28 Topper Database.

**Columns:**

| Column | Type | Notes |
|---|---|---|
| Photo | Thumbnail (48px) | Student photo from profile |
| Name | Text | Student full name |
| Exam | Badge | Board / JEE Main / JEE Adv / NEET |
| Rank / Score | Text | AIR or marks/percentage |
| Branch | Text | Branch name |
| Stream | Badge | MPC / BiPC / MEC / CEC |
| Added | Relative time | "2 hours ago" |

**Max rows:** 10 (latest toppers)
**HTMX:** `hx-get="/api/v1/group/{id}/marketing/dashboard/topper-spotlight/"` → `hx-target="#topper-spotlight"` → `hx-trigger="load"`

---

## 6. Drawers & Modals

### 6.1 Drawer: `branch-seat-detail` (640px, right-slide)
Opens when clicking any branch row in the Seat Fill table (Section 5.1).

- **Tabs:** Seat Breakdown · Lead Sources · Campaigns · Timeline
- **Seat Breakdown tab:** Stream-wise seat fill table:

| Stream | Total | Filled | Fill % | Progress Bar |
|---|---|---|---|---|
| Day Scholar — MPC | 240 | 198 | 82.5% | ████████░░ |
| Day Scholar — BiPC | 180 | 121 | 67.2% | ██████░░░░ |
| Hosteler Boys AC | 80 | 78 | 97.5% | █████████░ |
| Hosteler Boys Non-AC | 120 | 89 | 74.2% | ███████░░░ |
| Hosteler Girls AC | 60 | 60 | 100% | ██████████ |
| Hosteler Girls Non-AC | 80 | 52 | 65.0% | ██████░░░░ |
| Integrated JEE/NEET | 100 | 67 | 67.0% | ██████░░░░ |
| IIT Foundation (Class 6–10) | 60 | 43 | 71.7% | ███████░░░ |

- **Lead Sources tab:** Pie chart of enquiry sources for this branch
- **Campaigns tab:** Active campaigns targeting this branch with spend + leads
- **Timeline tab:** Week-by-week seat fill progression line chart
- **Footer:** "Open Branch Detail →" button navigates to O-22 filtered

### 6.2 Drawer: `lead-quick-view` (640px, right-slide)
Opens when clicking any lead-related item in the Activity Feed.

- **Tabs:** Lead Info · Call History · Timeline
- **Lead Info tab:** Parent name, phone, student name, class, stream interest, source, current stage, assigned telecaller, branch preference
- **Call History tab:** All calls made to this lead — date, duration, disposition, notes
- **Timeline tab:** Stage transitions with timestamps
- **Footer:** "Open in Pipeline →" → O-15 filtered; "Schedule Follow-up →" → O-21

### 6.3 Drawer: `campaign-quick-view` (640px, right-slide)
Opens when clicking a campaign card (Section 5.4).

- **Tabs:** Overview · Budget · Leads · Branches
- **Overview tab:** Campaign name, type, channels, date range, status, description
- **Budget tab:** Allocated vs spent, daily spend trend line chart, projected exhaustion date
- **Leads tab:** Lead count by stage (funnel mini-chart), top 5 performing branches
- **Branches tab:** Branch-wise lead count and conversion for this campaign
- **Footer:** "Open Campaign →" → O-08 detail

### 6.4 Modal: `export-dashboard`
- **Width:** 480px
- **Title:** "Export Marketing Dashboard Report"
- **Fields:**
  - Date range (from/to)
  - Include sections (checkboxes): KPIs, Seat Fill, Lead Pipeline, Campaigns, Telecalling, Source Breakdown
  - Format: PDF / XLSX
  - Recipient email (optional — sends download link)
- **Buttons:** Cancel · Generate Report
- **Behaviour:** POST to `/api/v1/group/{id}/marketing/dashboard/export/` → async task → toast on completion

### 6.5 Modal: `settings-panel`
- **Width:** 560px
- **Title:** "Dashboard Settings"
- **Fields:**
  - Auto-refresh interval: 1 min / 2 min / 5 min / Off
  - Peak season mode: ON/OFF (toggles 2-min refresh during Feb–Apr)
  - Daily lead target (group-wide): integer input
  - Daily call target (per telecaller): integer input
  - Seat fill alert threshold: percentage slider (default 60%)
  - Email alerts: toggle per alert type (seat fill critical, budget exhausted, lead drop)
  - Notification recipients: multi-select user list
- **Access:** G4/G5 only
- **Buttons:** Cancel · Save Settings

---

## 7. Charts

### 7.1 Seat Fill Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Group Seat Fill % — Current Admission Season" |
| Data | Weekly seat fill percentage for the group as a whole |
| X-axis | Week (W1 Nov, W2 Nov, … W4 Jul) — ~36 weeks |
| Y-axis | Fill % (0–100) |
| Lines | Current season (solid blue `#3B82F6`), Previous season (dashed grey `#9CA3AF`) |
| Reference | Horizontal dashed red line at target fill date milestones: 30% by Jan 31, 60% by Mar 31, 85% by May 31 |
| Tooltip | "Week [N]: [X]% filled ([Y] students) — Last year: [Z]%" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/seat-fill-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-seat-fill-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.2 Lead Volume Trend (Bar + Line Combo)

| Property | Value |
|---|---|
| Chart type | Combo — Bar (daily leads) + Line (7-day moving average) |
| Title | "Daily Lead Volume — Last 30 Days" |
| Data | Bar: daily enquiry count. Line: 7-day moving average |
| X-axis | Date (last 30 days) |
| Y-axis (left) | Lead count |
| Y-axis (right) | Moving average |
| Colour | Bars: `#3B82F6` (blue); Line: `#EF4444` (red) |
| Tooltip | "[Date]: [N] leads (7-day avg: [M])" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/lead-volume-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-lead-volume"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.3 Source-wise Lead Distribution (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Enquiry Sources — Current Month" |
| Data | Lead count per source type |
| X-axis | Count |
| Y-axis | Source name |
| Colour | Each source has distinct colour (see Section 5.6) |
| Tooltip | "[Source]: [N] leads ([X]% of total)" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/lead-sources/` |
| HTMX | `hx-get` on load → `hx-target="#chart-lead-sources"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.4 Campaign ROI Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Campaign ROI — Active Campaigns" |
| Data | Per campaign: Budget (bar 1), Spend (bar 2), Revenue equivalent (bar 3 = enrolled × avg fee) |
| X-axis | Campaign name |
| Y-axis | ₹ Amount |
| Colour | Budget: `#93C5FD` (light blue); Spend: `#3B82F6` (blue); Revenue: `#10B981` (green) |
| Tooltip | "[Campaign]: Budget ₹[X], Spent ₹[Y], Est. Revenue ₹[Z], ROI: [R]x" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/campaign-roi/` |
| HTMX | `hx-get` on load → `hx-target="#chart-campaign-roi"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.5 Conversion Funnel (Funnel Chart)

| Property | Value |
|---|---|
| Chart type | Funnel / Horizontal stacked bar (Chart.js 4.x with plugin) |
| Title | "Admission Funnel — Current Season" |
| Data | Count at each pipeline stage (see Section 5.2) |
| Stages | New → Contacted → Interested → Booked → Counselled → Applied → Offered → Enrolled |
| Colour | Gradient from `#DBEAFE` (lightest, New) to `#1E40AF` (darkest, Enrolled) |
| Tooltip | "[Stage]: [N] leads — Drop-off from previous: [X]%" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/pipeline-summary/` |
| HTMX | `hx-get` on load → `hx-target="#chart-funnel"` → `hx-swap="innerHTML"` |
| Export | PNG |

### 7.6 Cost per Admission Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Cost per Admission (CPA) — Monthly Trend" |
| Data | Monthly CPA: total spend / total enrollments for that month |
| X-axis | Month |
| Y-axis | ₹ Amount |
| Lines | Current season (solid `#EF4444` red), Previous season (dashed `#9CA3AF` grey) |
| Reference | Horizontal dashed green line at target CPA (₹2,000 default) |
| Tooltip | "[Month]: CPA ₹[X] ([N] enrolled, ₹[Y] spent) — Last year: ₹[Z]" |
| API endpoint | `GET /api/v1/group/{id}/marketing/dashboard/cpa-trend/` |
| HTMX | `hx-get` on load → `hx-target="#chart-cpa-trend"` → `hx-swap="innerHTML"` |
| Export | PNG |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Dashboard data refreshed | "Dashboard refreshed successfully" | Success | 2s |
| Seat fill critical alert | "CRITICAL: [Branch] below 50% seat fill — immediate action required" | Error | 10s (sticky) |
| Budget exhausted alert | "Campaign '[Name]' budget exhausted — pausing recommended" | Warning | 8s |
| Lead volume drop alert | "Lead volume dropped [X]% vs last week — verify campaign status" | Warning | 5s |
| Export report triggered | "Generating marketing dashboard report — download link via email shortly" | Info | 4s |
| Export report ready | "Marketing Dashboard Report is ready. Click to download." | Success | 8s |
| Settings saved | "Dashboard settings updated" | Success | 3s |
| Filter applied | "Showing [N] branches matching filter: [filter name]" | Info | 2s |
| API error on refresh | "Dashboard refresh failed. Retrying in 30 seconds." | Warning | 5s |
| Season switched | "Viewing admission season [Year]. Data is historical (read-only)." | Info | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No admission season configured | 📅 | "No Admission Season Active" | "Create an admission season to start tracking campaigns and leads." | Create Season |
| No campaigns created | 📢 | "No Campaigns Yet" | "Create your first campaign to start tracking leads and spend." | Create Campaign → O-08 |
| No leads in pipeline | 📋 | "No Leads Recorded" | "Leads will appear here once enquiries start coming in from campaigns." | View Campaign Calendar → O-07 |
| No telecallers assigned | 📞 | "No Telecallers Configured" | "Add telecaller executives to start tracking call performance." | Manage Team → O-42 |
| No branches configured | 🏫 | "No Branches Added" | "Branch configuration is required before marketing campaigns can target them." | Configure Branches (Div A) |
| Season ended — no active season | 📊 | "Admission Season Closed" | "The [Year] season has ended. View historical data or create a new season." | View Season Report → O-39 |
| New group — first-time setup | 🚀 | "Welcome to Marketing & Campaigns" | "Set up your first admission season, configure branches, and create campaigns." | Setup Wizard |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: 10 grey shimmer cards (2 rows of 5) + table skeleton + chart placeholders |
| KPI card refresh | Inline spinner inside each card container (24px) |
| Seat fill table load | Table skeleton: 8 grey shimmer rows matching column widths |
| Pipeline funnel load | Funnel placeholder: 8 grey horizontal bars descending in width |
| Activity feed load | 5 grey shimmer rows with icon placeholder + 2 text lines each |
| Campaign cards load | 4 card-shaped grey shimmer blocks (horizontal row) |
| Telecalling table load | Table skeleton: 5 grey shimmer rows |
| Chart data fetch | Chart placeholder with grey canvas + "Loading chart data..." label |
| Drawer open | Right-slide skeleton with 4 tab-shaped placeholders |
| Export generation | Modal: progress bar with "Generating report… [X]%" |

---

## 11. Role-Based UI Visibility

| Element | Campaign Mgr (119, G3) | Topper Mgr (120, G3) | Telecaller (130, G3) | Content Coord (131, G2) | Data Analyst (132, G1) | CEO/Chairman (G4/G5) |
|---|---|---|---|---|---|---|
| All 10 KPI Cards | All visible | Seats + Conversion only | Calls + Follow-ups only | — (not visible) | All visible | All visible |
| Seat Fill Table | All branches | All branches | — | — | All branches | All branches |
| Lead Pipeline Funnel | Full funnel | — | Own leads only | — | Full funnel | Full funnel |
| Activity Feed | All events | Topper events only | Own call events only | Material events only | All events | All events |
| Campaign Status Cards | All campaigns | — | — | — | All campaigns | All campaigns |
| Telecalling Summary | All telecallers | — | Own row only | — | All telecallers | All telecallers |
| Source Breakdown Chart | Visible | — | — | — | Visible | Visible |
| Topper Spotlight | Visible | Visible (highlighted) | — | — | Visible | Visible |
| All 6 Charts | Visible | Seat fill + Funnel only | — | — | All visible | All visible |
| Export PDF Button | Visible | Not visible | Not visible | Not visible | Visible | Visible |
| Settings Button | Not visible | Not visible | Not visible | Not visible | Not visible | G4/G5 only |
| Alert Banners | All banners | Topper-related only | Follow-up overdue only | — | All banners | All banners |

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/dashboard/kpis/` | G1+ | Returns all 10 KPI values |
| GET | `/api/v1/group/{id}/marketing/dashboard/seat-fill/` | G1+ | Branch-wise seat fill table data |
| GET | `/api/v1/group/{id}/marketing/dashboard/seat-fill-trend/` | G1+ | Weekly seat fill trend for chart |
| GET | `/api/v1/group/{id}/marketing/dashboard/pipeline-summary/` | G1+ | Stage-wise lead counts for funnel |
| GET | `/api/v1/group/{id}/marketing/dashboard/activity-feed/` | G1+ | Recent activity events (paginated) |
| GET | `/api/v1/group/{id}/marketing/dashboard/campaign-cards/` | G1+ | Active campaign summary cards |
| GET | `/api/v1/group/{id}/marketing/dashboard/telecalling-summary/` | G3+ | Telecaller performance table |
| GET | `/api/v1/group/{id}/marketing/dashboard/lead-sources/` | G1+ | Source-wise lead breakdown |
| GET | `/api/v1/group/{id}/marketing/dashboard/lead-volume-trend/` | G1+ | Daily lead volume — last 30 days |
| GET | `/api/v1/group/{id}/marketing/dashboard/campaign-roi/` | G1+ | Campaign ROI comparison data |
| GET | `/api/v1/group/{id}/marketing/dashboard/cpa-trend/` | G1+ | Monthly CPA trend |
| GET | `/api/v1/group/{id}/marketing/dashboard/topper-spotlight/` | G1+ | Latest toppers for spotlight widget |
| POST | `/api/v1/group/{id}/marketing/dashboard/export/` | G1+ | Trigger async PDF/XLSX report |
| GET | `/api/v1/group/{id}/marketing/dashboard/export/{task_id}/status/` | G1+ | Poll export task status |
| PATCH | `/api/v1/group/{id}/marketing/dashboard/settings/` | G4+ | Update dashboard configuration |

### Query Parameters — Seat Fill Table

| Parameter | Type | Description |
|---|---|---|
| `zone_id` | integer | Filter to specific zone |
| `fill_min` | integer | Minimum fill % (e.g., 0 for "below target") |
| `fill_max` | integer | Maximum fill % |
| `branch_id` | integer | Filter to specific branch |
| `stream` | string | Filter by stream (mpc, bipc, hosteler_boys, etc.) |
| `sort` | string | Column to sort by (default: fill_pct) |
| `order` | string | asc / desc (default: asc) |
| `page` | integer | Page number (default: 1) |
| `page_size` | integer | Items per page (default: 25, max: 100) |

### Query Parameters — Activity Feed

| Parameter | Type | Description |
|---|---|---|
| `event_type` | string | Filter: lead, conversion, campaign, telecalling, topper, alert |
| `branch_id` | integer | Filter to specific branch |
| `since` | datetime | Only events after this timestamp |
| `page` | integer | Page number |
| `page_size` | integer | Items per page (default: 50, max: 200) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| Auto-refresh KPIs | `<div id="kpi-bar">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 120s"` |
| Seat fill table load | `<div id="seat-fill-section">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/seat-fill/"` | `#seat-fill-table-body` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Seat fill filter | Filter chip buttons | `hx-get` with `?fill_min=0&fill_max=60` | `#seat-fill-table-body` | `innerHTML` | `hx-trigger="click"` |
| Pipeline funnel load | `<div id="pipeline-funnel">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/pipeline-summary/"` | `#pipeline-funnel` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Activity feed load | `<div id="activity-feed">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/activity-feed/"` | `#activity-feed` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Campaign cards load | `<div id="campaign-cards">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/campaign-cards/"` | `#campaign-cards` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Telecalling table load | `<div id="telecalling-table">` | `hx-get="/api/v1/group/{id}/marketing/dashboard/telecalling-summary/"` | `#telecalling-table` | `innerHTML` | `hx-trigger="load, every 120s"` |
| Open branch drawer | Row click in seat fill table | `hx-get="/api/v1/group/{id}/marketing/branches/{branch_id}/seat-detail/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` + `hx-push-url="false"` |
| Open lead drawer | Activity feed lead click | `hx-get="/api/v1/group/{id}/marketing/leads/{lead_id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Open campaign drawer | Campaign card click | `hx-get="/api/v1/group/{id}/marketing/campaigns/{campaign_id}/summary/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Seat fill search | Search input | `hx-get` with `?q={query}` | `#seat-fill-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:350ms"` |
| Export trigger | Export PDF button | `hx-post="/api/v1/group/{id}/marketing/dashboard/export/"` | `#export-status` | `innerHTML` | Shows progress modal |
| Season switch | Season dropdown | `hx-get` with `?season_id={id}` | `#dashboard-content` | `innerHTML` | Reloads entire dashboard body |
| Pagination — seat fill | Pagination controls | `hx-get` with `?page={n}` | `#seat-fill-table-body` | `innerHTML` | Table body only |

---

## 14. Admission Season Configuration

The dashboard operates within the context of an "Admission Season" — a time-bounded entity that defines the scope of all metrics.

| Field | Type | Example |
|---|---|---|
| Season Name | Text | "Admission Season 2026-27" |
| Academic Year | Text | "2026-27" |
| Start Date | Date | 2025-10-01 |
| End Date | Date | 2026-07-31 |
| Status | Enum | Planning / Active / Closing / Closed |
| Phase | Auto-calculated | Based on current date vs phase date ranges |
| Total Seat Target | Integer | 42,000 |
| Total Budget | Currency | ₹5,60,00,000 |
| Target CPA | Currency | ₹2,000 |
| Target Conversion Rate | Percentage | 15% |

**Phase auto-detection:** The system automatically determines the current phase based on the date ranges defined in O-07 Campaign Calendar. Phase information is displayed in the page header and affects refresh intervals.

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
