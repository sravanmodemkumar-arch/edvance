# O-18 — Admission Telecalling Manager

> **URL:** `/group/marketing/leads/telecalling/`
> **File:** `o-18-telecalling-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admission Telecaller Executive (Role 130, G3) — primary operator; Campaign Manager (119) — oversight/assignment

---

## 1. Purpose

The Admission Telecalling Manager is the operational workstation for telecalling executives — the people who convert raw enquiries into walk-ins and ultimately enrollments through phone calls. In a large Indian education group, 5–10 telecallers handle 50,000–1,50,000 calls during a 6-month admission season. Each telecaller works a queue of 30–80 leads per day, making 50–100 calls, achieving 40–60% contact rates, and converting 15–25% of contacted parents into walk-in visits. Telecalling is the highest-labour-intensity, highest-direct-impact marketing activity.

The problems this page solves:

1. **Call queue management:** Each telecaller needs a clear, prioritised list of "who to call next" — not a spreadsheet they have to sort through. The system auto-queues leads by: priority (hot first), SLA urgency (follow-ups due today first), last attempt time (not called in 7+ days float to top), and assignment (only their leads).

2. **Call logging and dispositions:** After every call, the telecaller must log: did they reach the parent? What was the outcome? When to follow up? The system enforces structured dispositions — no call can be marked complete without a disposition code. This data feeds pipeline analytics.

3. **NDNC compliance:** The National Do Not Call registry (TRAI) prohibits calling registered numbers for promotional purposes. The platform scrubs call queues against NDNC data. Calling an NDNC number can result in ₹25,000 penalty per call.

4. **Supervisor dashboard:** The Campaign Manager needs to see: which telecaller is productive (calls/hour, contacts/hour, conversions), which telecaller has idle queues, which leads haven't been called in 3+ days. Real-time productivity monitoring enables same-day intervention.

5. **Call recording integration:** For quality monitoring and training, calls made through the platform's VoIP integration (or tracked via cloud telephony providers like Exotel, Knowlarity, Ozonetel) are recorded and linked to lead records.

**Scale:** 5–50 telecallers · 50–100 calls/day/person · 30–80 leads in queue per person · 50,000–1,50,000 calls/season · 500–5,000 call hours/season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admission Telecaller Executive | 130 | G3 | Full operations — own queue only: view queue, make calls, log dispositions, schedule follow-ups | Cannot see other telecallers' queues |
| Group Admissions Campaign Manager | 119 | G3 | Full operations + supervision — all telecallers' queues, assign/reassign leads, view productivity, listen to recordings | Supervisor |
| Group Admission Data Analyst | 132 | G1 | Read only — productivity reports, call analytics | No call operations |
| Group CEO / Chairman | — | G4/G5 | Read — team productivity dashboard | Strategic oversight |
| Branch Principal | — | G3 | Read (own branch calls) — view call outcomes for branch leads | Branch oversight |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Telecallers (130) see only `assigned_to = user.id`. Campaign Manager (119) sees all. Call recordings: 119 and G4+ only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Lead Management  ›  Admission Telecalling Manager
```

### 3.2 Page Header (Telecaller View)
```
Admission Telecalling Manager                       [Start Calling]  [My Queue]  [Today's Log]
Telecaller — Priya Reddy
Kukatpally Branch · Queue: 62 leads · Today: 34 calls made · 18 contacted · 7 walk-ins booked
```

### 3.3 Page Header (Supervisor View — Role 119)
```
Admission Telecalling Manager — Supervisor          [Assign Leads]  [Team Dashboard]  [Export]
Campaign Manager — Rajesh Kumar
All Branches · 8 telecallers active · Queue: 480 leads · Today: 312 calls · 168 contacts · 52 walk-ins
```

---

## 4. KPI Summary Bar

### 4.1 Telecaller KPIs (6 cards — when role 130)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | My Queue | Integer | COUNT(leads) WHERE assigned_to = me AND stage IN active stages | Static blue | `#kpi-queue` |
| 2 | Calls Today | Integer | COUNT(calls) WHERE telecaller = me AND date = today | Static blue | `#kpi-calls-today` |
| 3 | Contact Rate | Percentage | Contacted / Total calls today × 100 | Green ≥ 50%, Amber 30–50%, Red < 30% | `#kpi-contact-rate` |
| 4 | Walk-ins Booked Today | Integer | COUNT WHERE disposition = 'walk_in_booked' AND date = today | Static green | `#kpi-walkins` |
| 5 | Follow-ups Due Today | Integer | COUNT WHERE follow_up_date = today AND done = false | Red > 15, Amber 5–15, Green < 5 | `#kpi-followups-due` |
| 6 | Overdue Follow-ups | Integer | COUNT WHERE follow_up_date < today AND done = false | Red > 0, Green = 0 | `#kpi-overdue` |

### 4.2 Supervisor KPIs (8 cards — when role 119)

| # | Card | Metric | Calculation | Colour Rule |
|---|---|---|---|---|
| 1 | Total Queue | Integer | COUNT all active assigned leads | Static blue |
| 2 | Unassigned Leads | Integer | COUNT WHERE assigned_to IS NULL AND stage = 'new' | Red > 100, Amber 20–100, Green < 20 |
| 3 | Total Calls Today | Integer | All telecaller calls combined | Static blue |
| 4 | Team Contact Rate | Percentage | AVG contact rate across telecallers | Green ≥ 50% |
| 5 | Walk-ins Booked Today | Integer | All telecallers combined | Static green |
| 6 | Conversion Rate | Percentage | Enrolled from telecaller-sourced leads / total telecaller leads | Green ≥ 20% |
| 7 | Avg Calls/Telecaller | Decimal | Total calls today / active telecallers | Green ≥ 40, Amber 25–40, Red < 25 |
| 8 | SLA Breaches | Integer | Leads not called within SLA | Red > 0, Green = 0 |

---

## 5. Sections

### 5.1 Telecaller View — Sections

#### 5.1.1 Call Queue (Primary workspace)

Prioritised list of leads to call. Auto-sorted by the system.

**Queue priority algorithm:**
1. Overdue follow-ups (follow_up_date < today) — highest priority
2. Follow-ups due today
3. Hot leads not contacted in 48+ hours
4. New leads (never called) ordered by lead score
5. Warm leads due for re-contact
6. Cold leads (lowest priority)

**Queue columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Priority | Badge | No | 🔴 Overdue / 🟡 Due Today / 🟢 Scheduled / ⚪ New |
| Student Name | Text | Yes | Student name |
| Parent Name | Text | Yes | Parent name |
| Phone | Text (click-to-call) | No | Primary contact |
| Class Sought | Badge | Yes | Jr Inter MPC / BiPC / etc. |
| Branch | Text | Yes | Target branch |
| Source | Badge | No | Lead source |
| Lead Score | Badge | No | Hot / Warm / Cold |
| Last Call | DateTime | Yes | When last attempted |
| Attempts | Integer | Yes | Total call attempts |
| Last Disposition | Badge | Yes | Last call outcome |
| Follow-up Date | Date | Yes | Scheduled follow-up |
| Days Since Contact | Integer | Yes | Days since last successful contact |
| Action | Button | No | [📞 Call] |

**Default sort:** Priority algorithm order (not user-sortable by default)
**Queue size:** 50 leads per page, auto-loads more on scroll

#### 5.1.2 Active Call Panel (When call is in progress)

Appears as a sticky top bar or side panel when the telecaller clicks "Call":

```
┌──────────────────────────────────────────────────────────────┐
│  📞 ACTIVE CALL — Rajesh Kumar (Father of Sai Krishna)       │
│  +91 98765 43210 · Connected · Duration: 02:34               │
│  Branch: Kukatpally · Class: Jr Inter MPC · Source: Newspaper │
│                                                               │
│  Previous calls: 2 attempts · Last: "Callback requested"     │
│  Lead score: 🔴 Hot (72 pts) · Pipeline: Interested          │
│                                                               │
│  Quick Notes: [________________________________]              │
│                                                               │
│  [End Call & Log Disposition]  [Transfer to Branch]  [Hold]  │
└──────────────────────────────────────────────────────────────┘
```

#### 5.1.3 Disposition Logger (Post-call)

After ending a call, mandatory disposition form:

| Field | Type | Required | Options |
|---|---|---|---|
| Call outcome | Dropdown | ✅ | Connected / Not Reachable / Busy / Switched Off / Wrong Number / DND / Call Back Later |
| If Connected → Interest | Dropdown | ✅ | Interested / Not Interested / Thinking / Already Enrolled Elsewhere |
| If Interested → Action | Dropdown | ✅ | Walk-in Booked / Demo Class Booked / Brochure Sent / Callback Requested / Application Link Sent |
| Walk-in date/time | DateTime | If booked | Date + time + branch |
| Follow-up date | Date | If callback | When to call back |
| Notes | Textarea | No | Call conversation summary |

#### 5.1.4 Today's Call Log

Table of all calls made today:

| Column | Type | Notes |
|---|---|---|
| Time | DateTime | Call timestamp |
| Lead | Text | Student/parent name |
| Phone | Text | Number called |
| Duration | Duration | Call length |
| Direction | Badge | Outbound / Inbound |
| Disposition | Badge | Outcome code |
| Next Action | Text | Follow-up date or walk-in date |

### 5.2 Supervisor View — Sections

#### 5.2.1 Team Dashboard

Real-time telecaller performance grid:

| Column | Type | Notes |
|---|---|---|
| Telecaller Name | Text | — |
| Branch | Text | Primary branch |
| Status | Badge | Online / On Call / Idle / Break / Offline |
| Queue Size | Integer | Leads in their queue |
| Calls Today | Integer | Total calls made |
| Contacts Today | Integer | Successfully connected |
| Contact Rate | Percentage | Contacts / Calls |
| Walk-ins Booked | Integer | Today's walk-in bookings |
| Avg Call Duration | Duration | Average call length |
| Overdue Follow-ups | Integer | Red if > 0 |
| Last Call | DateTime | When they last made a call |
| Actions | Buttons | [View Queue] [Assign Leads] [Listen to Calls] |

**Auto-refresh:** Every 60 seconds. Telecaller status updates in real-time.

**Colour coding:**
- Green row: productive (contact rate ≥ 50%, calls ≥ 40 today)
- Amber row: moderate (contact rate 30–50%)
- Red row: underperforming (contact rate < 30% or calls < 20 by 2 PM)

#### 5.2.2 Unassigned Lead Queue

Leads that haven't been assigned to any telecaller:

- Same columns as telecaller queue but with "Assign" action
- Bulk select + assign to telecaller dropdown
- Auto-assign button: distributes unassigned leads round-robin across active telecallers

#### 5.2.3 Call Quality Monitoring

| Feature | Description |
|---|---|
| Call recordings | List of recorded calls with play button (cloud telephony integration) |
| Quality score | Post-listen scoring: Greeting / Pitch / Objection Handling / Closing / Overall (1–5) |
| Flag for training | Mark specific calls as training examples (good or bad) |

---

## 6. Drawers & Modals

### 6.1 Modal: `log-disposition` (480px)

- **Title:** "Log Call Disposition — [Parent Name]"
- **Fields:** As described in §5.1.3
- **Buttons:** Cancel · Log & Next Call (auto-loads next in queue)
- **Access:** Role 130 (own calls) or 119 (any call)

### 6.2 Modal: `assign-leads` (560px, Supervisor)

- **Title:** "Assign Leads to Telecaller"
- **Fields:**
  - Leads to assign: Select from unassigned queue (checkbox) or bulk (N leads)
  - Assignment method:
    - **Specific telecaller** (dropdown)
    - **Round-robin** (distribute equally across selected telecallers)
    - **Branch-based** (assign to telecallers in the lead's branch)
    - **Load-balanced** (assign to telecaller with smallest current queue)
  - Priority override (optional): set all assigned leads to Hot/Warm/Cold
- **Preview:** "Assigning [N] leads to [Telecaller] — their queue will go from [X] to [X+N]"
- **Buttons:** Cancel · Assign
- **Access:** Role 119 or G4+

### 6.3 Modal: `reassign-lead` (480px)

- **Title:** "Reassign Lead — [Student Name]"
- **Current assignment:** [Telecaller Name]
- **New assignment:** Dropdown of active telecallers
- **Reason:** Dropdown: Workload Balancing / Branch Change / Telecaller Absent / Performance Issue / Language Preference / Other
- **Notes:** Textarea
- **Buttons:** Cancel · Reassign
- **Access:** Role 119 or G4+

### 6.4 Drawer: `telecaller-performance` (640px, right-slide, Supervisor)

- **Tabs:** Today · This Week · This Month · Season
- **Per tab:**
  - Total calls, contacts, contact rate
  - Walk-ins booked, enrollments attributed
  - Avg call duration, peak calling hours
  - Disposition breakdown (donut chart)
  - Top converting leads
  - SLA compliance: % of leads called within SLA
  - Call quality scores (if available)
  - Comparison with team average
- **Footer:** [Assign More Leads] [View Queue] [Export Report]

### 6.5 Modal: `call-recording-player` (560px)

- **Title:** "Call Recording — [Parent Name] — [Date]"
- **Player:** Audio player with play/pause/seek/speed (1×/1.5×/2×)
- **Call details:** Telecaller, parent, phone, duration, disposition
- **Quality scoring form:**
  - Greeting (1–5)
  - Institution pitch (1–5)
  - Objection handling (1–5)
  - Closing / CTA (1–5)
  - Overall impression (1–5)
  - Flag as: Excellent Example / Needs Improvement / Training Material
  - Notes (textarea)
- **Buttons:** Close · Save Score
- **Access:** Role 119 or G4+ only (privacy — telecaller cannot listen to own calls unless allowed)

---

## 7. Charts

### 7.1 Team Productivity — Calls per Day (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "Daily Calls by Telecaller — This Week" |
| Data | Per telecaller per day: calls made |
| X-axis | Day of week |
| Y-axis | Call count |
| Colour | One colour per telecaller |
| Tooltip | "[Telecaller] — [Day]: [N] calls, [M] contacts" |
| API | `GET /api/v1/group/{id}/marketing/leads/telecalling/analytics/daily-calls/` |

### 7.2 Disposition Distribution (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Call Dispositions — This Month" |
| Data | COUNT per disposition type |
| Colour | Connected-Interested: green / Connected-Not Interested: red / Not Reachable: grey / Busy: amber / Wrong Number: dark grey |
| Tooltip | "[Disposition]: [N] calls ([X]%)" |
| API | `GET /api/v1/group/{id}/marketing/leads/telecalling/analytics/dispositions/` |

### 7.3 Hourly Call Volume (Line)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Hourly Call Volume — Today" |
| Data | Calls per hour (8 AM – 8 PM) |
| Colour | `#3B82F6` blue |
| X-axis | Hour |
| Y-axis | Call count |
| Purpose | Identify peak calling hours and idle periods |
| API | `GET /api/v1/group/{id}/marketing/leads/telecalling/analytics/hourly-volume/` |

### 7.4 Contact Rate Trend (Line)

| Property | Value |
|---|---|
| Chart type | Line (Chart.js 4.x) |
| Title | "Contact Rate Trend — Last 30 Days" |
| Data | Daily contact rate (%) |
| Colour | `#10B981` green |
| Benchmark line | 50% target (dashed grey) |
| API | `GET /api/v1/group/{id}/marketing/leads/telecalling/analytics/contact-rate-trend/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Call started | "Calling [Parent Name] at [Phone]…" | Info | 2s |
| Disposition logged | "Disposition logged — [Outcome]" | Success | 2s |
| Walk-in booked | "Walk-in booked for [Name] on [Date] at [Branch]" | Success | 3s |
| Follow-up scheduled | "Follow-up scheduled for [Date]" | Success | 2s |
| Leads assigned | "[N] leads assigned to [Telecaller]" | Success | 3s |
| Lead reassigned | "Lead reassigned from [Old] to [New Telecaller]" | Info | 3s |
| SLA breach alert | "[N] leads not called within SLA — immediate action required" | Error | 6s |
| Queue empty | "Your queue is empty! Request more leads from your supervisor." | Info | 4s |
| Call quality scored | "Call quality score saved — [Overall]/5" | Success | 2s |
| Overdue follow-up | "You have [N] overdue follow-ups — call these first!" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| Empty queue (telecaller) | 📞 | "Queue Empty" | "You have no leads in your queue. Ask your Campaign Manager for assignment." | — |
| No calls today | 📱 | "No Calls Yet" | "Start your calling session by clicking the first lead in your queue." | Start Calling |
| No unassigned leads (supervisor) | ✅ | "All Leads Assigned" | "Every lead has been assigned to a telecaller." | — |
| No call recordings | 🎙️ | "No Recordings Available" | "Call recordings will appear when cloud telephony integration is active." | — |
| No team members | 👥 | "No Telecallers Configured" | "Add telecaller executives to start assigning leads." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | KPI shimmer + queue table skeleton (15 rows) |
| Queue refresh | Silent refresh (no visible loader) |
| Call initiation | "Connecting…" overlay on active call panel |
| Disposition save | Button spinner → toast |
| Supervisor dashboard | Team grid skeleton (8 rows) + chart placeholders |
| Call recording load | Audio player shimmer with waveform placeholder |
| Performance drawer | 640px skeleton: metrics bar + 4 tab placeholders |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/queue/` | G3+ | Telecaller's call queue (own leads) |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/queue/unassigned/` | G3+ (119) | Unassigned leads queue |
| POST | `/api/v1/group/{id}/marketing/leads/telecalling/calls/` | G3+ | Log a call (start/disposition) |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/calls/today/` | G3+ | Today's call log |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/calls/{call_id}/` | G1+ | Call detail |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/calls/{call_id}/recording/` | G3+ (119/G4+) | Call recording audio |
| POST | `/api/v1/group/{id}/marketing/leads/telecalling/calls/{call_id}/quality-score/` | G3+ (119) | Save quality score |
| POST | `/api/v1/group/{id}/marketing/leads/telecalling/assign/` | G3+ (119) | Assign leads to telecaller |
| PATCH | `/api/v1/group/{id}/marketing/leads/telecalling/reassign/{lead_id}/` | G3+ (119) | Reassign lead |
| POST | `/api/v1/group/{id}/marketing/leads/telecalling/auto-assign/` | G3+ (119) | Auto-distribute unassigned leads |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/team/` | G3+ (119) | Team dashboard data |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/team/{user_id}/performance/` | G1+ | Telecaller performance detail |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/analytics/daily-calls/` | G1+ | Daily calls chart |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/analytics/dispositions/` | G1+ | Disposition donut |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/analytics/hourly-volume/` | G1+ | Hourly chart |
| GET | `/api/v1/group/{id}/marketing/leads/telecalling/analytics/contact-rate-trend/` | G1+ | Contact rate trend |

### Cloud Telephony Integration

| Provider | Integration | Purpose |
|---|---|---|
| Exotel / Knowlarity / Ozonetel | Click-to-call API | Initiate calls from browser; auto-log duration |
| Cloud telephony CDR webhook | `/webhooks/telephony/cdr/` | Call detail records — duration, recording URL |
| NDNC Registry API | Batch scrub | Remove DNC numbers from call queues |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../telecalling/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Queue load | Telecaller view | `hx-get=".../telecalling/queue/"` | `#call-queue` | `innerHTML` | `hx-trigger="load"` |
| Queue refresh | After disposition | `hx-get=".../telecalling/queue/"` | `#call-queue` | `innerHTML` | Triggered by disposition save |
| Call initiate | Call button | JS-initiated (click-to-call API) + `hx-get=".../pipeline/{id}/"` | `#active-call-panel` | `innerHTML` | Shows lead details during call |
| Log disposition | Disposition form | `hx-post=".../telecalling/calls/"` | `#disposition-result` | `innerHTML` | Toast + queue refresh |
| Today's log | Log tab | `hx-get=".../telecalling/calls/today/"` | `#today-log` | `innerHTML` | `hx-trigger="load"` |
| Team dashboard | Supervisor tab | `hx-get=".../telecalling/team/"` | `#team-dashboard` | `innerHTML` | `hx-trigger="load, every 60s"` |
| Assign leads | Assign form | `hx-post=".../telecalling/assign/"` | `#assign-result` | `innerHTML` | Toast + unassigned queue refresh |
| Auto-assign | Auto button | `hx-post=".../telecalling/auto-assign/"` | `#auto-result` | `innerHTML` | Toast + both queues refresh |
| Performance drawer | Telecaller row click | `hx-get=".../telecalling/team/{id}/performance/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Call recording | Play button | `hx-get=".../telecalling/calls/{id}/recording/"` | `#recording-modal` | `innerHTML` | Audio player modal |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
