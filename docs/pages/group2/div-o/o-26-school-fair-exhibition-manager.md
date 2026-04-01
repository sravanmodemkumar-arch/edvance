# O-26 — School Fair & Exhibition Manager

> **URL:** `/group/marketing/enrollment/fairs/`
> **File:** `o-26-school-fair-exhibition-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The School Fair & Exhibition Manager tracks every on-ground fair, exhibition, mall stall, society gate event, and colony activation that the institution group participates in or organises for student acquisition. In the Indian education market, offline events remain one of the highest-ROI lead generation channels — a well-run stall at the Hyderabad School Expo can generate 300–800 leads in two days at ₹40–₹80 per lead, far cheaper than digital ads (₹150–₹400 per lead). Large groups participate in 20–60 events per admission season across multiple cities, spending ₹5L–₹50L on stall bookings, standees, brochures, and staff deployment. Without centralised tracking, each branch does its own events, duplicates effort, loses lead data on paper forms, and nobody knows which events actually converted into enrollments.

The problems this page solves:

1. **Event fragmentation:** A 30-branch group has 30 marketing coordinators, each finding local fairs, society events, and mall opportunities independently. Some branches attend the same city-level expo and book separate stalls (wasting ₹50,000–₹2,00,000 on duplicate bookings). This page centralises all event discovery, booking, and participation into one group-wide calendar so the Campaign Manager can assign branches to shared stalls, avoid duplication, and negotiate group rates with organisers.

2. **Lead leakage from events:** The single biggest failure in fair-based marketing is lead loss. A telecaller collects 200 parent phone numbers on a paper form at a mall stall on Saturday; by Monday, the form is coffee-stained, 30 numbers are illegible, and the remaining 170 get typed into a spreadsheet that nobody follows up on for two weeks. This page provides a digital lead capture mechanism — either via tablet-based forms at the stall or bulk upload immediately after the event — that feeds directly into O-15 (Lead Pipeline) with source tagged as the specific event.

3. **Cost tracking and ROI:** Each event has costs: stall booking (₹15,000–₹3,00,000 for major expos), standee printing (₹2,000–₹8,000), brochure printing (500–5,000 copies at ₹8–₹25 each), staff travel and DA, gift items for parents (bags, pens, notebooks — ₹20–₹100 per visitor). Without tracking total cost per event and attributing conversions back, the group cannot determine whether Hyderabad School Expo (₹2.5L total cost, 400 leads, 45 enrollments = ₹5,556/enrollment) outperforms society gate events (₹8,000 total cost, 25 leads, 5 enrollments = ₹1,600/enrollment).

4. **Material coordination:** Each event requires physical materials — standees, brochures, banners, application forms, gift bags, registration tablets. The Campaign Manager must ensure the right materials reach the right venue on the right date. This page links to O-03 (Marketing Material Library) for material requisition and tracks what was dispatched, what was used, and what was returned.

5. **Staff deployment:** Events need trained staff — branch counsellors who can answer parent queries about curriculum, fees, transport. Deploying the wrong person (e.g., a receptionist who cannot explain the MPC vs BiPC difference) wastes the event opportunity. This page tracks who is assigned to each event stall, their performance (leads collected per hour), and post-event feedback.

**Scale:** 5–50 branches · 20–100 events/season · ₹5L–₹50L total fair/exhibition spend · 2,000–20,000 leads from events · 5–15 event types · 200–1,000 staff deployments/season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create events, book stalls, assign staff, track leads, manage budgets | Primary operator |
| Group Admission Telecaller Executive | 130 | G3 | Read (assigned events) + Log Leads — enter leads collected at fairs into the system | Lead capture at stall |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — manage material dispatch records, upload event photos | Material coordination |
| Group Admission Data Analyst | 132 | G1 | Read + Export — event ROI analytics, lead source attribution | Reporting |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve high-value stall bookings (> ₹1L) | Financial authority |
| Group CFO / Finance Director | 30 | G1 | Read — event spend data, cost per lead, budget utilisation | Financial oversight |
| Branch Principal | — | G3 | Read (own branch events) + Update — mark staff availability, post-event feedback | Branch coordination |
| Branch Counsellor | — | G3 | Read (assigned events) — view event brief, talking points, material list | On-ground staff |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Event creation and stall booking: role 119 or G4+. Lead logging: 119 or 130. Branch staff see only events tagged to `branch_id = user.branch_id`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  School Fair & Exhibition Manager
```

### 3.2 Page Header
```
School Fair & Exhibition Manager                      [+ Add Event]  [Calendar View]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 34 events planned · 18 completed · 4,820 leads collected · ₹12.6L spent
```

---

## 4. KPI Summary Bar (8 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Events | Integer | COUNT(events) WHERE season = current | Static blue | `#kpi-total-events` |
| 2 | Upcoming (30d) | Integer | COUNT WHERE event_date within next 30 days AND status = 'confirmed' | Amber if 0 (no pipeline), Green > 0 | `#kpi-upcoming` |
| 3 | Leads Collected | Integer | SUM(lead_count) across all events | Static green | `#kpi-leads` |
| 4 | Total Spend (₹) | Amount | SUM(total_cost) all events this season | Amber > 90% budget, Green ≤ 90% | `#kpi-spend` |
| 5 | Cost per Lead | ₹ Amount | Total spend / total leads | Green ≤ ₹100, Amber ₹100–₹250, Red > ₹250 | `#kpi-cpl` |
| 6 | Conversions | Integer | COUNT(leads from events) WHERE status = 'enrolled' in O-15 | Static green | `#kpi-conversions` |
| 7 | Conversion Rate | Percentage | Conversions / total leads × 100 | Green ≥ 10%, Amber 5–10%, Red < 5% | `#kpi-conv-rate` |
| 8 | Cost per Enrollment | ₹ Amount | Total spend / conversions | Green ≤ ₹3,000, Amber ₹3,000–₹8,000, Red > ₹8,000 | `#kpi-cpe` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/enrollment/fairs/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Event List** — All fairs and events in table view
2. **Calendar View** — Month/week calendar of upcoming and past events
3. **Lead Tracker** — Leads collected at events with follow-up status
4. **Analytics** — Event ROI, cost analysis, type comparison

### 5.2 Tab 1: Event List

**Filter bar:** Event Type · City · Branch · Status (Planned / Confirmed / Live / Completed / Cancelled) · Date Range · Stall Booked (Yes/No)

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Event Name | Text (link) | Yes | Click → detail drawer |
| Type | Badge | Yes | Education Fair / Mall Stall / Society Gate Event / Colony Event / School Exhibition / RWA Event / Temple/Church/Mosque Gate / Bus Stand Kiosk / Railway Station Stall / Corporate Park Stall / Other |
| City | Text | Yes | Event city |
| Venue | Text | Yes | Venue name / mall name / society name |
| Event Dates | Date range | Yes | Start → End (or single day) |
| Branches | Text | Yes | Branches participating (comma-separated or "All") |
| Stall Cost (₹) | Amount | Yes | Booking cost paid to organiser |
| Total Cost (₹) | Amount | Yes | Stall + materials + staff + logistics |
| Staff Deployed | Integer | Yes | Number of counsellors/telecallers at event |
| Leads Collected | Integer | Yes | Leads entered during/after event |
| Conversions | Integer | Yes | Leads that converted to enrollment (from O-15) |
| CPL (₹) | Amount | Yes | Total cost / leads |
| Status | Badge | Yes | Planned (grey) / Confirmed (blue) / Live (green pulse) / Completed (dark green) / Cancelled (red) |
| Actions | Buttons | No | [View] [Log Leads] [Complete] |

**Default sort:** Event Dates DESC (upcoming first, then recent)
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Calendar View

Monthly calendar (FullCalendar.js or custom HTMX grid) showing:

- **Event blocks:** Each event appears as a coloured bar spanning its date range
- **Colour by type:** Education Fair = blue, Mall Stall = purple, Society Gate = orange, Colony Event = teal, School Exhibition = green, Other = grey
- **Event block content:** Event name + city + lead count (if completed)
- **Click on event:** Opens detail drawer
- **Day click:** Opens "Add Event" modal pre-filled with that date
- **Month navigation:** ← → arrows, "Today" button
- **Mini-legend:** Colour key for event types
- **Conflict detection:** If two events in the same city overlap and share staff, show a warning icon

### 5.4 Tab 3: Lead Tracker

Leads collected specifically from fair/exhibition events, with follow-up status.

**Filter bar:** Event Name · Date Range · Follow-up Status · Assigned Telecaller · Branch

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Lead Name | Text (link) | Yes | Parent/student name → links to O-15 lead detail |
| Phone | Text | No | Masked: 98765XXXXX (full on click, role-gated) |
| Event Source | Text | Yes | Which event this lead came from |
| Event Date | Date | Yes | Date lead was captured |
| Class Interested | Text | Yes | Class/stream parent enquired about |
| Branch Preference | Text | Yes | Preferred branch |
| Captured By | Text | Yes | Staff member who captured the lead |
| Follow-up Status | Badge | Yes | New / Called / Interested / Walk-in Booked / Enrolled / Lost |
| Assigned To | Text | Yes | Telecaller assigned for follow-up |
| Days Since Capture | Integer | Yes | Today − event date (Red > 7, Amber 3–7, Green ≤ 3) |
| Actions | Buttons | No | [View in O-15] [Assign] [Call Now] |

**Colour-coded rows:**
- Red: > 7 days since capture, no follow-up yet
- Amber: 3–7 days, follow-up pending
- Green: followed up within 3 days

### 5.5 Tab 4: Analytics

Charts and metrics (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `add-event` (640px)

- **Title:** "Add Fair / Exhibition Event"
- **Fields:**
  - Event name (text, required — e.g., "Hyderabad School Expo 2026" or "Inorbit Mall Stall — March")
  - Event type (dropdown, required):
    - **Education Fair** — Organised by third-party expo companies (School Expo India, Education World, Brainfeed), 50–200 exhibitors, 2,000–10,000 footfall
    - **Mall Stall** — Rented kiosk/stall in shopping mall (Inorbit, Forum, Sarath City), weekend or week-long, high parent footfall
    - **Society Gate Event** — Permission to set up table/standee at residential society entrance, 1–3 hours, 50–200 interactions
    - **Colony Event** — Pamphlet distribution + registration desk at a residential colony, often combined with free coaching demo
    - **School Exhibition** — Own institution's open day / exhibition / science fair where prospective parents are invited
    - **RWA Event** — Residents' Welfare Association cultural event sponsorship with stall
    - **Temple/Church/Mosque Gate** — Permitted setup at place of worship during festival/weekly gathering
    - **Bus Stand Kiosk** — Temporary kiosk at major bus stands (Mahatma Gandhi Bus Station, etc.)
    - **Railway Station Stall** — Platform or concourse stall at railway station
    - **Corporate Park Stall** — Setup at IT park / corporate campus (parents work here, children need schools)
    - **Other** — Free text
  - City (dropdown, required)
  - Venue / Location (text, required — e.g., "HITEX Exhibition Centre, Madhapur" or "My Home Vihanga Society Gate")
  - Venue address (textarea)
  - GPS coordinates (lat/long, optional — for map plotting)
  - Event dates: Start date + End date (date pickers, required)
  - Timings: Start time + End time per day (time pickers)
  - Organiser (text — third-party organiser name for expos, or "Self-organised")
  - Organiser contact (phone + email, optional)
  - Branches participating (multi-select, required)
  - Stall details:
    - Stall number / location within venue (text, optional)
    - Stall size: dropdown (3×3 / 6×3 / 6×6 / 9×6 / Custom)
    - Stall type: Shell Scheme / Bare Space / Table Only / Standee Only / Kiosk
  - Cost breakdown:
    - Stall booking cost (₹)
    - Stall setup/fabrication (₹)
    - Material printing cost (₹) — linked to O-03 requisition
    - Staff travel & DA (₹)
    - Gift/giveaway cost (₹)
    - Miscellaneous (₹)
    - Total cost (₹, auto-calculated)
  - Budget line from O-09 (dropdown)
  - Materials required (multi-select from O-03 library):
    - Standees (quantity)
    - Brochures (quantity)
    - Application forms (quantity)
    - Banners (quantity)
    - Gift bags (quantity)
    - Registration tablets (quantity)
    - Visiting cards (quantity)
  - Staff deployment:
    - Staff members (multi-select from branch counsellors + telecallers + field staff)
    - Staff lead (dropdown — primary person in charge at venue)
  - Expected footfall (integer, optional — organiser's estimate)
  - Lead target (integer — expected leads to collect)
  - Notes (textarea)
- **Buttons:** Cancel · Save as Planned · Confirm Booking
- **Validation:**
  - End date ≥ Start date
  - At least one branch selected
  - Stall booking cost ≤ budget line remaining (warning if exceeding)
  - Duplicate detection: warn if another event at same venue + overlapping dates exists
- **Access:** Role 119 or G4+

### 6.2 Modal: `log-leads` (640px)

- **Title:** "Log Leads — [Event Name]"
- **Purpose:** Capture leads collected at the event (bulk entry or one-by-one)
- **Mode toggle:** Single Entry / Bulk Upload
- **Single entry fields:**
  - Parent name (text, required)
  - Phone number (tel, required — 10-digit Indian mobile validation)
  - Student name (text, optional)
  - Class interested (dropdown: Nursery–XII + competitive streams)
  - Branch preference (dropdown, pre-filled with event branches)
  - Current school (text, optional)
  - Interest level (radio): Hot / Warm / Cold
  - Notes (textarea — what parent said, specific concerns)
  - Captured by (dropdown — auto-filled with logged-in staff, changeable)
- **Bulk upload:**
  - Excel/CSV upload (template download link provided)
  - Template columns: Parent Name | Phone | Student Name | Class | Branch Preference | Current School | Interest Level | Notes
  - Preview grid after upload: shows parsed rows, highlights errors (invalid phone, missing required fields)
  - Duplicate detection: flags phone numbers already in O-15 pipeline
- **On submit:**
  - Each lead auto-created in O-15 with `source = 'fair'`, `source_detail = event_id`
  - Auto-assigned to telecaller pool via O-19 (Lead Assignment) rules
  - If telecaller (role 130) is logging, leads assigned to them by default
- **Buttons:** Cancel · Add Lead (single) / Upload & Create Leads (bulk)
- **Access:** Role 119 or 130

### 6.3 Drawer: `event-detail` (720px, right-slide)

- **Tabs:** Overview · Staff · Materials · Leads · Costs · Photos
- **Overview tab:**
  - Event name, type, venue, dates, timings, organiser
  - Stall details (number, size, type)
  - Status badge with lifecycle: Planned → Confirmed → Live → Completed
  - Expected footfall vs actual (if logged)
  - Lead target vs actual
  - Quick KPIs: leads collected, CPL, conversions, cost per enrollment
- **Staff tab:**
  - Assigned staff list: name, role, branch, shift timing
  - Per-staff lead count (who collected how many leads)
  - Staff performance rank within this event
  - Post-event staff feedback (rating + comments)
- **Materials tab:**
  - Materials dispatched (from O-03 requisition): item, quantity sent, quantity returned
  - Material utilisation: brochures distributed, application forms filled, gift bags given
  - Shortfall flag: if materials ran out before event ended
- **Leads tab:**
  - All leads from this event (same columns as Tab 3, filtered to this event)
  - Lead funnel: Total → Called → Interested → Walk-in → Enrolled
  - Days-to-first-contact metric: how quickly were event leads followed up
- **Costs tab:**
  - Full cost breakdown (from creation modal)
  - Actual vs budgeted comparison
  - Cost per lead, cost per enrollment
  - Budget line utilisation from O-09
  - Receipt/invoice uploads (file upload for stall booking receipt, vendor bills)
- **Photos tab:**
  - Event photos uploaded by staff: stall setup, crowd, banner, branding
  - Date and uploader metadata per photo
  - Gallery view with lightbox
- **Footer:** [Edit Event] [Log Leads] [Mark Complete] [Duplicate for Next Season] [Archive]

### 6.4 Modal: `complete-event` (560px)

- **Title:** "Complete Event — [Event Name]"
- **Purpose:** Post-event wrap-up with actuals
- **Fields:**
  - Actual footfall at stall (integer — estimated by staff)
  - Total leads collected (auto-filled from logged leads, editable)
  - Materials distributed:
    - Brochures given out (integer)
    - Application forms distributed (integer)
    - Gift bags distributed (integer)
  - Materials returned to office (integer per item)
  - Staff performance ratings (1–5 per staff member)
  - Event quality rating (1–5 — was the expo well-organised? Good footfall?)
  - Would you participate again? (Yes / No / Maybe)
  - Post-event notes (textarea — what worked, what didn't, competitor observations)
  - Actual total cost (₹, if different from estimate)
  - Receipts/invoices (file upload)
- **Buttons:** Cancel · Submit Completion Report
- **Behaviour:** Changes event status to "Completed", locks further lead logging after 7 days, triggers ROI calculation
- **Access:** Role 119 or G4+

### 6.5 Modal: `duplicate-event` (480px)

- **Title:** "Duplicate Event for Next Season"
- **Pre-filled:** All fields from source event (name, venue, type, branches, cost estimates, materials)
- **Editable fields:** Event dates (required — new season dates), cost adjustments, staff
- **Purpose:** Most fairs repeat annually — Hyderabad School Expo happens every January. Duplicating saves 15 minutes of re-entry.
- **Buttons:** Cancel · Create as Planned
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Leads by Event Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Leads Collected by Event Type — Season [Year]" |
| Data | SUM(lead_count) grouped by event type |
| Colour | Distinct colour per type |
| Centre text | Total: [N] leads |
| Tooltip | "[Type]: [N] leads ([Y]% of total)" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/fairs/analytics/leads-by-type/` |

### 7.2 Cost per Lead by Event Type (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Cost per Lead by Event Type" |
| Data | (Total cost / lead count) per event type |
| Colour | Green ≤ ₹100, Amber ₹100–₹250, Red > ₹250 per bar |
| Benchmark line | Group-average CPL (dashed) |
| Tooltip | "[Type]: ₹[X] per lead ([N] leads, ₹[Y] spent)" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/fairs/analytics/cpl-by-type/` |

### 7.3 Event Timeline & Lead Volume (Combo)

| Property | Value |
|---|---|
| Chart type | Combo: bar + line (Chart.js 4.x) |
| Title | "Events & Leads — Monthly Trend" |
| Data | Bars: number of events per month; Line: leads collected per month |
| Bar colour | `#93C5FD` light blue |
| Line colour | `#10B981` green |
| X-axis | Month (season span) |
| Y-axis left | Event count |
| Y-axis right | Lead count |
| API | `GET /api/v1/group/{id}/marketing/enrollment/fairs/analytics/monthly-trend/` |

### 7.4 Event ROI Scatter (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Event ROI — Cost vs Conversions" |
| Data | Each event = dot; X = total cost (₹), Y = conversions (enrollments) |
| Dot size | Proportional to lead count |
| Dot colour | By event type |
| Quadrants | Top-left = high conversion, low cost (best); Bottom-right = high cost, low conversion (worst) |
| Tooltip | "[Event]: ₹[X] spent, [N] leads, [M] enrollments, CPE ₹[Y]" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/fairs/analytics/roi-scatter/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[Name]' added — [Date] at [Venue]" | Success | 3s |
| Event confirmed | "Event '[Name]' confirmed — stall booked" | Success | 3s |
| Leads logged (single) | "Lead '[Parent Name]' added from [Event] — pushed to O-15 pipeline" | Success | 3s |
| Leads logged (bulk) | "[N] leads uploaded from [Event] — [M] duplicates skipped, [K] created in O-15" | Success | 5s |
| Event completed | "Event '[Name]' marked complete — [N] leads, ₹[X] CPL" | Success | 4s |
| High CPL warning | "Warning: [Event] CPL ₹[X] exceeds group benchmark of ₹[Y]" | Warning | 5s |
| Duplicate phone detected | "Phone [XXXXX] already exists in O-15 — lead merged, source updated" | Info | 4s |
| Material shortfall | "Materials ran out at [Event] — [Item] exhausted by [Time]" | Warning | 5s |
| Staff not assigned | "No staff assigned to [Event] starting in [N] days" | Warning | 5s |
| Event duplicated | "Event '[Name]' duplicated for Season [Year] — update dates and confirm" | Info | 3s |
| Budget exceeded | "Event '[Name]' cost ₹[X] exceeds budget line by ₹[Y]" | Error | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No events | 🎪 | "No Fairs or Exhibitions" | "Add your first education fair, mall stall, or society event to start tracking on-ground lead generation." | Add Event |
| No upcoming events | 📅 | "No Upcoming Events" | "All events are completed or cancelled. Plan your next fair to keep the lead pipeline flowing." | Add Event |
| No leads for event | 📋 | "No Leads Logged" | "Leads from this event haven't been entered yet. Log them now before they go cold." | Log Leads |
| No analytics data | 📊 | "Not Enough Data" | "Complete at least 3 events to generate meaningful ROI analytics." | — |
| No events for branch | 🏫 | "No Events for [Branch]" | "No fairs or exhibitions are planned for your branch this season." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 8 KPI shimmer cards + tab bar + table skeleton (12 rows) |
| Tab switch | Content area skeleton |
| Calendar view load | Month grid skeleton with placeholder event blocks |
| Event detail drawer | 720px skeleton: overview header + 6 tab placeholders |
| Lead log modal | Form skeleton (single entry fields) |
| Bulk upload processing | Progress bar with "[N] of [M] rows processed" |
| Chart load | Grey canvas placeholder |
| Photo gallery | Image placeholder grid (6 squares) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/` | G1+ | List all events |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/` | G1+ | Event detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/` | G3+ | Create event |
| PUT | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/` | G3+ | Update event |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/status/` | G3+ | Change status (confirm/complete/cancel) |
| DELETE | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/` | G4+ | Delete event |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/leads/` | G3+ | Log single lead |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/leads/bulk/` | G3+ | Bulk upload leads |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/leads/` | G1+ | List event leads |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/staff/` | G1+ | Event staff list |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/staff/` | G3+ | Assign staff |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/materials/` | G1+ | Materials dispatched |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/complete/` | G3+ | Submit completion report |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/photos/` | G2+ | Upload event photos |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/photos/` | G1+ | List event photos |
| POST | `/api/v1/group/{id}/marketing/enrollment/fairs/{event_id}/duplicate/` | G3+ | Duplicate event for next season |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/calendar/` | G1+ | Calendar view data |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/analytics/leads-by-type/` | G1+ | Leads donut chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/analytics/cpl-by-type/` | G1+ | CPL bar chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/analytics/monthly-trend/` | G1+ | Monthly combo chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/fairs/analytics/roi-scatter/` | G1+ | ROI scatter chart |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../fairs/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get=".../fairs/?tab={list/calendar/leads/analytics}"` | `#fairs-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Filter dropdowns | `hx-get` with params | `#fairs-table-body` | `innerHTML` | `hx-trigger="change"` |
| Event detail drawer | Row click | `hx-get=".../fairs/{event_id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create event | Form submit | `hx-post=".../fairs/"` | `#create-result` | `innerHTML` | Toast + table refresh |
| Log single lead | Lead form submit | `hx-post=".../fairs/{event_id}/leads/"` | `#lead-result` | `innerHTML` | Toast + reset form for next entry |
| Bulk lead upload | File submit | `hx-post=".../fairs/{event_id}/leads/bulk/"` | `#bulk-result` | `innerHTML` | `hx-encoding="multipart/form-data"` · progress bar |
| Complete event | Completion form | `hx-post=".../fairs/{event_id}/complete/"` | `#complete-result` | `innerHTML` | Toast + status badge refresh |
| Calendar load | Calendar tab | `hx-get=".../fairs/calendar/?month={m}&year={y}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Calendar nav | ← → month arrows | `hx-get=".../fairs/calendar/?month={m}&year={y}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Photo upload | Photo form | `hx-post=".../fairs/{event_id}/photos/"` | `#photo-gallery` | `beforeend` | `hx-encoding="multipart/form-data"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#fairs-table-body` | `innerHTML` | Table body only |
| Duplicate event | Duplicate form | `hx-post=".../fairs/{event_id}/duplicate/"` | `#duplicate-result` | `innerHTML` | Toast |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
