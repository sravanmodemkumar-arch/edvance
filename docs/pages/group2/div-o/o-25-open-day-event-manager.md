# O-25 — Open Day & Event Manager

> **URL:** `/group/marketing/enrollment/open-days/`
> **File:** `o-25-open-day-event-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The Open Day & Event Manager is the highest-conversion weapon in the Indian admission funnel. When a parent walks through the school gate on an open day, sees the labs, meets the principal, watches their child attend a demo class, and sits through a 20-minute counselling session — the conversion rate is 50–70%. No newspaper ad (2–5% response), no WhatsApp blast (8–12% click-through), no telecall (15–20% conversion) comes close. Open days are the nuclear option of admission marketing, and this page manages the entire lifecycle: event creation, invite targeting, RSVP collection, day-of-event attendance tracking, counsellor assignment, campus tour routing, demo class scheduling, parent feedback, and post-event follow-up.

The problems this page solves:

1. **Event fragmentation:** A 30-branch group runs 100–200 open-day-type events per admission season: campus visit Saturdays, full open days, parent–teacher meets for prospective parents, demo classes, orientation sessions. Without a central system, each branch runs its own events with different formats, no shared calendar, no RSVP tracking, and no attendance data flowing back into the lead pipeline. This page centralises event planning across all branches.

2. **Invite targeting:** The highest-ROI open day is one where you invite 500 parents from your lead pipeline who are at the "Interested but not yet applied" stage — not a generic newspaper announcement. The system integrates with O-15 (Lead Pipeline) to pull leads by stage, branch, class interest, and source, then sends targeted WhatsApp invites via O-12. A parent who receives "Dear Mrs. Sharma, we invite Ananya for a demo Physics class this Saturday at our Kukatpally campus" converts at 3× the rate of a generic "Open Day — All Welcome" ad.

3. **RSVP management:** Capacity planning is critical. If 800 parents RSVP but the campus can handle 300 at a time, you need time-slot management. If only 200 RSVP, you need a WhatsApp reminder blast 2 days before. If 600 RSVP but historically only 55% show up, you can plan for 330 actual visitors. The RSVP system tracks: Invited → RSVP Yes → RSVP No → Reminded → Confirmed → Attended → No-show.

4. **Day-of-event operations:** On the actual day, chaos reigns. Parents arrive, queue at the gate, get a token, wait for a counsellor, take a campus tour, attend a demo class, collect a prospectus, sit for fee counselling, and leave — with or without submitting an application. The system provides a live check-in dashboard: who has arrived, who is waiting, who is in counselling, who has completed, and who left without conversion. Branch staff use this on a tablet at the reception desk.

5. **Post-event conversion tracking:** The real metric is not "how many parents attended" but "how many enrolled within 14 days of attending." The system links open-day attendance to O-15 pipeline stages, tracking each attendee's journey from visit to enrollment (or drop-off), enabling ROI calculation per event.

**Scale:** 5–50 branches · 2–8 events/branch/season · 50–500 invites/event · 30–300 attendees/event · 50–200 total events/season across group · 50–70% conversion rate for attendees

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create events, configure invites, view all branches, export | Primary event planner |
| Group Topper Relations Manager | 120 | G3 | Read + Create (topper showcase events) — felicitation open days | Topper-linked events |
| Group Admission Telecaller Executive | 130 | G3 | Read (own branch) + Check-in — gate check-in, RSVP calls | Day-of-event operations |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — event creative assets, invite templates | Creative support |
| Group Admission Data Analyst | 132 | G1 | Read — event analytics, conversion data, ROI | Reporting |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve high-budget events, review event ROI | Strategic authority |
| Branch Principal | — | G3 | Read + Update (own branch) — view events, manage on-ground execution, counselling | Branch execution lead |
| Branch Counsellor | — | G3 | Read (own branch, assigned attendees) — counselling notes, feedback | Counselling at event |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Event creation: role 119 or G4+. Check-in operations: role 130 or Branch Principal. Branch staff restricted to `branch_id = user.branch_id`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Enrollment Drives  ›  Open Day & Event Manager
```

### 3.2 Page Header
```
Open Day & Event Manager                              [+ Create Event]  [Event Calendar]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 14 events this season · 3,840 RSVPs · 2,180 attended · 64% conversion
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Upcoming Events | Integer | COUNT(events) WHERE status = 'scheduled' AND event_date ≥ today | Static blue | `#kpi-upcoming` |
| 2 | Total RSVPs (Season) | Integer | COUNT(rsvps) WHERE season = current AND rsvp_status = 'yes' | Static blue | `#kpi-rsvps` |
| 3 | Total Attended | Integer | COUNT(attendees) WHERE check_in_time IS NOT NULL AND season = current | Static blue | `#kpi-attended` |
| 4 | Show-up Rate | Percentage | Attended / RSVP Yes × 100 | Green ≥ 60%, Amber 40–60%, Red < 40% | `#kpi-showup` |
| 5 | Conversion Rate | Percentage | (Enrolled within 14 days of event) / Attended × 100 | Green ≥ 50%, Amber 30–50%, Red < 30% | `#kpi-conversion` |
| 6 | Next Event In | Countdown | MIN(event_date) WHERE status = 'scheduled' − today | Red ≤ 3 days, Amber 4–7, Green > 7 | `#kpi-next-event` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Event Calendar** — Visual calendar of all scheduled events across branches
2. **Event List** — Table of all events with status and metrics
3. **RSVP & Attendance** — Consolidated RSVP tracking across events
4. **Analytics** — Event effectiveness, conversion, branch comparison

### 5.2 Tab 1: Event Calendar

**Monthly calendar view (fullcalendar-style, server-rendered via HTMX):**

```
┌─────────────────────────────────────────────────────────────────┐
│  ◀  March 2026  ▶                     [Month] [Week] [List]    │
│                                                                  │
│  Mon    Tue    Wed    Thu    Fri    Sat    Sun                   │
│  ...    ...    ...    ...    ...    7      8                     │
│                                    ┌──────┐                      │
│                                    │🏫 Open│                     │
│                                    │Day —  │                     │
│                                    │Kukpally│                    │
│                                    │142 RSVP│                    │
│                                    └──────┘                      │
│  9      10     11     12     13    14      15                   │
│                                    ┌──────┐                      │
│                                    │📚 Demo│                     │
│                                    │Class —│                     │
│                                    │Miyapur│                     │
│                                    │68 RSVP│                     │
│                                    └──────┘                      │
│  ...                                                             │
└─────────────────────────────────────────────────────────────────┘
```

**Event badge colours:**
- Blue: Campus Visit (small, individual/few families)
- Green: Open Day (mass, 100–500 parents)
- Amber: Parent–Teacher Meet (prospective parents)
- Purple: Demo Class (subject-specific)
- Teal: Orientation (post-admission, pre-joining)

**Click on event badge:** Opens event detail drawer (§6.3).

**Filters above calendar:** Branch (dropdown) · Event Type (multi-select) · Status (Scheduled / Ongoing / Completed / Cancelled)

### 5.3 Tab 2: Event List

**Table view — all events for the season:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Event Name | Text (link) | Yes | Click → event detail drawer |
| Type | Badge | Yes | Campus Visit / Open Day / Parent–Teacher Meet / Demo Class / Orientation |
| Branch | Text | Yes | Branch name + city |
| Date | Date | Yes | Event date |
| Time Slot | Text | No | e.g., "9:00 AM – 1:00 PM" |
| Capacity | Integer | No | Max parents/families |
| Invited | Integer | Yes | COUNT invites sent |
| RSVP Yes | Integer | Yes | Confirmed RSVPs |
| Attended | Integer | Yes | Checked-in attendees (post-event) |
| Show-up % | Percentage | Yes | Attended / RSVP Yes |
| Applications | Integer | Yes | Applications submitted on event day or within 7 days |
| Enrolled | Integer | Yes | Enrolled within 14 days of event |
| Conversion % | Percentage | Yes | Enrolled / Attended × 100 |
| Status | Badge | Yes | Draft / Scheduled / Invites Sent / Ongoing / Completed / Cancelled |
| Actions | Buttons | No | [View] [Send Invites] [Check-in Mode] [Clone] |

**Filter bar:** Branch · Type · Date Range · Status
**Default sort:** Date DESC
**Pagination:** Server-side · 25/page

### 5.4 Tab 3: RSVP & Attendance

**Cross-event RSVP tracker — a consolidated view of all invitees across upcoming events.**

**Filter bar:** Event (dropdown) · Branch · RSVP Status · Lead Stage (from O-15) · Class Sought

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Parent Name | Text | Yes | — |
| Student Name | Text (link) | Yes | Click → lead detail in O-15 |
| Phone | Text | Yes | — |
| Event | Text | Yes | Event name + date |
| Branch | Text | Yes | — |
| Class Sought | Badge | Yes | — |
| Lead Stage | Badge | Yes | Current O-15 stage |
| Invite Sent | Badge | No | ✅ WhatsApp / ✅ SMS / ✅ Call / ❌ Not Yet |
| RSVP Status | Badge | Yes | Pending / Yes / No / Maybe / No Response |
| Reminder Sent | Badge | No | ✅ / ❌ (auto-sent 2 days before) |
| Check-in | Badge | Yes | ✅ Checked In (time) / ❌ No-show / — (upcoming) |
| Counsellor | Text | No | Assigned counsellor (day-of) |
| Outcome | Badge | Yes | Applied / Follow-up / Not Interested / — (pending) |
| Actions | Buttons | No | [Send Invite] [Mark RSVP] [Check In] [Assign Counsellor] |

### 5.5 Tab 4: Analytics

Charts and tables showing event effectiveness (see §7).

---

## 6. Drawers & Modals

### 6.1 Modal: `create-event` (640px)

- **Title:** "Create Open Day / Event"
- **Fields:**
  - Event name (text, required — e.g., "Open Day — Kukatpally Campus — 15 Mar 2026")
  - Event type (dropdown, required):
    - **Campus Visit** — Small group or individual family visit; 5–20 families; by appointment
    - **Open Day (Mass)** — Large-scale open house; 100–500 families; advertised publicly
    - **Parent–Teacher Meet** — Prospective parents meet current faculty; 50–150 families; invite-only
    - **Demo Class** — Subject-specific demo (Physics/Chemistry/Maths); 30–80 students; targeted invite
    - **Orientation** — Post-admission, pre-joining orientation for confirmed students; 100–300 families
  - Branch (dropdown, required — or multi-select for group-wide simultaneous events)
  - Date (date, required)
  - Start time (time, required)
  - End time (time, required)
  - Venue details (text — "Main Auditorium + Lab Block" / "Entire Campus")
  - Capacity (integer, required — max families/parents)
  - Time slots? (toggle — if yes, divide into slots):
    - Slot duration (dropdown: 30 min / 1 hour / 2 hours)
    - Max per slot (integer)
    - Auto-generates slot grid
  - Event agenda (textarea or rich text):
    - Example: "9:00 Registration → 9:30 Welcome by Principal → 10:00 Campus Tour → 10:45 Demo Class → 11:30 Counselling → 12:30 Refreshments"
  - Invite source (multi-select):
    - **From Lead Pipeline (O-15)** — Select lead stages: Interested / Enquired / Walk-in Done / Follow-up Pending
    - **From Previous Events** — Re-invite no-shows from past events
    - **Manual Upload** — CSV of phone numbers (new leads)
    - **Walk-in Welcome** — No pre-invite; open to anyone who walks in
  - Invite channel (multi-select):
    - WhatsApp (via O-12)
    - SMS
    - Phone call (telecaller task created in O-18)
    - Email (via O-13)
  - Invite message template (dropdown — pre-approved templates from O-12):
    - Preview shown inline
    - Personalisation variables: {parent_name}, {student_name}, {branch_name}, {event_date}, {time_slot}, {rsvp_link}
  - Staffing plan:
    - Counsellors on duty (multi-select from branch staff)
    - Reception/check-in staff (multi-select)
    - Campus tour guides (integer — number needed)
    - Demo class teachers (multi-select + subject)
  - Budget (₹, optional — linked to O-09 budget line)
  - Special arrangements (checkboxes):
    - [ ] Refreshments / snacks
    - [ ] Transport arrangement (bus from key pickup points)
    - [ ] Gift/goodie bag for attendees
    - [ ] Printed prospectus copies (quantity)
    - [ ] Standees and banners
    - [ ] Student volunteers
  - Internal notes (textarea)
- **Buttons:** Cancel · Save as Draft · Schedule & Send Invites
- **Validation:**
  - Date must be in future
  - Capacity > 0
  - End time > Start time
  - At least one invite source selected (except for walk-in-welcome type)
  - If WhatsApp selected, template must be chosen
- **Post-save:**
  - Draft: saved but no invites sent
  - Schedule: event published to calendar; invites queued for sending via selected channels
  - Auto-creates RSVP tracking records for all invitees
- **Access:** Role 119 or G4+

### 6.2 Modal: `send-invites` (560px)

- **Title:** "Send Event Invites — [Event Name]"
- **Purpose:** Send or re-send invites to targeted leads
- **Fields:**
  - Target audience (pre-filled from event config, editable):
    - Lead stage filter (from O-15)
    - Branch filter
    - Class/stream filter
    - Exclude already-invited (toggle, default on)
    - Exclude RSVP No (toggle, default on)
  - Preview: "[N] parents will receive invites"
  - Channel: WhatsApp / SMS / Call / Email (from event config)
  - Schedule: Send Now / Schedule for [date + time]
  - Reminder configuration:
    - Auto-remind RSVP-pending (toggle, default on) — 3 days before event
    - Auto-remind RSVP-yes (toggle, default on) — 1 day before event, "See you tomorrow!"
    - Auto-remind no-response (toggle) — 5 days before event, re-invite
- **Summary:** "Will send [N] WhatsApp invites + create [M] telecall tasks"
- **Buttons:** Cancel · Send Invites
- **Access:** Role 119, 130, or G4+

### 6.3 Drawer: `event-detail` (720px, right-slide)

- **Tabs:** Overview · Invites & RSVP · Attendance · Feedback · Conversions · History
- **Overview tab:**
  - Event name, type, branch, date/time, venue, capacity
  - Agenda timeline
  - Staffing plan (counsellors, guides, reception)
  - Budget and special arrangements
  - Status badge + progress: Invited [N] → RSVP Yes [N] → Attended [N] → Applied [N] → Enrolled [N]
  - Funnel visualisation (horizontal bar):
    ```
    Invited:  ████████████████████████████████████  500
    RSVP Yes: ████████████████████████              320
    Attended: ██████████████████                    240
    Applied:  ████████████████                      200
    Enrolled: ██████████████                        168
    ```
- **Invites & RSVP tab:** Table of all invitees with RSVP status, invite channel, reminder status. Bulk actions: [Resend to Non-responders] [Send Reminder to RSVP Yes]
- **Attendance tab:** Live check-in list (during event) or final attendance list (post-event). Columns: Parent name, Student name, Check-in time, Counsellor assigned, Campus tour (done/not), Demo class (attended/not), Time spent, Outcome
- **Feedback tab:** Post-event feedback from parents (see §6.5). Summary: avg rating, top comments, improvement suggestions
- **Conversions tab:** Attendees who applied/enrolled within 14 days. Conversion funnel with timelines. Revenue attributed to this event
- **History tab:** Event lifecycle log — created, invites sent, reminders sent, event day, completed, follow-ups; all actions with who/when
- **Footer:** [Edit Event] [Send More Invites] [Download Attendance] [Clone for Next Month] [Cancel Event]

### 6.4 Modal: `check-in` (480px, optimised for tablet)

- **Title:** "Event Check-in — [Event Name]"
- **Purpose:** Gate reception staff check in arriving parents
- **Layout:** Large touch-friendly buttons for tablet use at reception desk
- **Search bar:** Phone number or parent name → instant lookup against RSVP list
- **If found (RSVP'd):**
  ```
  ┌────────────────────────────────────────┐
  │  ✅ Found: Mrs. Anita Sharma           │
  │  Student: Ananya Sharma                │
  │  Class Sought: Jr Inter MPC            │
  │  RSVP: Yes (via WhatsApp)              │
  │  Lead Stage: Interested                │
  │                                        │
  │  [CHECK IN]  [Assign Counsellor ▼]     │
  │                                        │
  │  Token: OD-042                         │
  └────────────────────────────────────────┘
  ```
- **If not found (walk-in, no RSVP):**
  - Quick registration form: Parent name, phone, student name, class sought, source ("How did you hear about today's event?")
  - Auto-creates lead in O-15 (linked to O-17 walk-in register)
  - Check in immediately after registration
- **Counsellor assignment:** Dropdown of available counsellors with current load (e.g., "Priya — 3 active / Suresh — 1 active / Meena — 0 active")
- **Post check-in flow options (checkboxes, checked as parent progresses):**
  - [ ] Campus tour assigned (Guide: [name])
  - [ ] Demo class (Subject: [dropdown], Teacher: [name])
  - [ ] Counselling session (Counsellor: [name])
  - [ ] Prospectus given
  - [ ] Fee structure discussed
  - [ ] Application form given / submitted
- **Token:** Auto-generated sequential token: OD-001, OD-002 (per event per day)
- **Access:** Role 130, Branch Principal, 119, or G4+

### 6.5 Modal: `feedback` (480px)

- **Title:** "Parent Feedback — [Event Name]"
- **Purpose:** Collect feedback from parents before they leave (or via WhatsApp post-event)
- **Fields:**
  - Overall experience (1–5 stars, required)
  - Campus & facilities (1–5 stars)
  - Teaching quality impression (1–5 stars)
  - Staff behaviour & responsiveness (1–5 stars)
  - Would you recommend this school? (Yes / Maybe / No)
  - What impressed you most? (checkboxes): Labs / Library / Sports / Faculty / Infrastructure / Location / Fee / Discipline / Safety / Other
  - Concerns or suggestions (textarea)
  - Likelihood to enroll (dropdown): Will enroll / Likely / Undecided / Unlikely / Will not enroll
  - If unlikely/no: reason (dropdown): Fee Too High / Location Far / Better Options Available / Facilities Not Up to Mark / Other
- **Delivery modes:**
  - Tablet at exit gate (staff hands tablet to parent)
  - WhatsApp link (auto-sent 2 hours after event ends)
- **Buttons:** Submit Feedback
- **Access:** Public (feedback form) — linked to event token; no login required for parent

### 6.6 Modal: `post-event-follow-up` (560px)

- **Title:** "Post-Event Follow-up — [Event Name]"
- **Purpose:** Configure follow-up actions for attendees who didn't apply on event day
- **Fields:**
  - Target: Attendees without application (auto-calculated: [N] parents)
  - Follow-up type (multi-select):
    - Telecall within 48 hours (creates tasks in O-18)
    - WhatsApp thank-you + offer (via O-12) — "Thank you for visiting! Here's an exclusive 5% early-bird discount valid for 7 days"
    - Email with prospectus PDF (via O-13)
    - Invite to next event (if another event is scheduled)
  - Follow-up deadline: [N] days after event (default 7)
  - Assign telecallers (auto-assign based on O-19 rules, or manual)
  - Special offer link (optional — link to O-23 offer campaign)
- **Preview:** "[N] telecall tasks + [M] WhatsApp messages will be created"
- **Buttons:** Cancel · Schedule Follow-ups
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Event Conversion Funnel (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal funnel / stacked bar (Chart.js 4.x) |
| Title | "Event Conversion Funnel — Season [Year]" |
| Data | Aggregated across all events: Invited → RSVP Yes → Attended → Applied → Enrolled |
| Colour | Invited: light blue → RSVP: blue → Attended: teal → Applied: green → Enrolled: emerald |
| Labels | Count + % drop-off at each stage |
| API | `GET /api/v1/group/{id}/marketing/enrollment/open-days/analytics/funnel/` |

### 7.2 Events Over Time (Bar + Line Combo)

| Property | Value |
|---|---|
| Chart type | Combo — bar (attendees) + line (conversion %) |
| Title | "Event Attendance & Conversion — Monthly Trend" |
| Data | Per month: total attendees (bar) + avg conversion rate (line) |
| Bar colour | `#3B82F6` blue |
| Line colour | `#10B981` green |
| X-axis | Month (season timeline) |
| Tooltip | "[Month]: [N] attendees, [X]% converted" |
| API | `GET /api/v1/group/{id}/marketing/enrollment/open-days/analytics/monthly-trend/` |

### 7.3 Branch Event Performance (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Branch-wise Event Performance" |
| Data | Per branch: total attended (bar 1) vs enrolled from events (bar 2) |
| Purpose | Shows which branches run the most effective events |
| Colour | Attended: light blue / Enrolled: emerald |
| API | `GET /api/v1/group/{id}/marketing/enrollment/open-days/analytics/branch-performance/` |

### 7.4 Event Type Effectiveness (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Enrollments by Event Type" |
| Data | COUNT(enrolled) per event type (Campus Visit / Open Day / Parent–Teacher / Demo Class / Orientation) |
| Colour | Per type (matching calendar badge colours) |
| Centre text | Total: [N] enrolled |
| Purpose | Identify which event types drive the most enrollments |
| API | `GET /api/v1/group/{id}/marketing/enrollment/open-days/analytics/type-effectiveness/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[Name]' created for [Date] — [Branch]" | Success | 3s |
| Invites sent | "[N] invites sent via [Channel] for '[Event Name]'" | Success | 4s |
| RSVP received | "RSVP received from [Parent Name] for '[Event Name]'" | Info | 3s |
| Parent checked in | "[Parent Name] checked in — Token OD-[XXX]" | Success | 2s |
| Walk-in registered | "Walk-in registered: [Parent Name] — new lead created" | Info | 3s |
| Counsellor assigned | "[Parent Name] assigned to [Counsellor] for counselling" | Success | 2s |
| Feedback submitted | "Feedback received from [Parent Name] — Rating: [X]/5" | Success | 3s |
| Event completed | "Event '[Name]' completed — [N] attended, [M] applications" | Success | 5s |
| Follow-ups scheduled | "[N] post-event follow-ups scheduled for '[Event Name]'" | Success | 4s |
| Low RSVP alert | "⚠️ '[Event Name]' has only [N] RSVPs — [X] days away. Send reminders?" | Warning | 6s |
| High no-show alert | "⚠️ '[Event Name]' show-up rate is [X]% — below expected 55%" | Warning | 5s |
| Event cancelled | "Event '[Name]' cancelled — [N] parents notified" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No events | 📅 | "No Events Planned" | "Create your first open day or campus visit to start converting pipeline leads into enrollments." | Create Event |
| No upcoming events | 🏫 | "No Upcoming Events" | "All scheduled events are complete. Plan your next open day to keep the enrollment momentum." | Create Event |
| No RSVPs for event | 📩 | "No RSVPs Yet" | "Invites have been sent. RSVPs will appear as parents respond." | Send Reminder |
| No attendance data | 🚶 | "No Check-ins Yet" | "Attendance will be recorded as parents check in at the event." | Start Check-in |
| No feedback | 💬 | "No Feedback Received" | "Parent feedback will appear after the event or when they respond to the feedback link." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + calendar/table skeleton |
| Calendar month change | Calendar grid shimmer (month view skeleton) |
| Event detail drawer | 720px skeleton: overview + 6 tabs |
| RSVP table load | 15-row table skeleton |
| Check-in modal | Search bar + result card placeholder |
| Chart load | Grey canvas placeholder |
| Invite sending | Progress bar: "Sending [N] of [M] invites…" |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/` | G1+ | List all events (filterable by branch, type, status, date) |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/` | G1+ | Event detail |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/` | G3+ | Create event |
| PUT | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/` | G3+ | Update event |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/status/` | G3+ | Change status (schedule/cancel/complete) |
| DELETE | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/` | G4+ | Delete event (draft only) |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/calendar/` | G1+ | Calendar view data (month/week) |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/invites/` | G3+ | Send invites to targeted leads |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/rsvps/` | G1+ | List RSVPs for event |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/rsvps/{rsvp_id}/` | G3+ | Update RSVP status |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/reminders/` | G3+ | Send reminders to RSVP-pending or confirmed |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/check-in/` | G3+ | Check in attendee (by phone or RSVP ID) |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/attendance/` | G1+ | Attendance list with check-in times and outcomes |
| PATCH | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/attendance/{att_id}/` | G3+ | Update attendee progress (tour, demo, counselling, outcome) |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/feedback/` | Public | Submit parent feedback (token-authenticated, no login) |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/feedback/` | G1+ | List feedback for event |
| POST | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/follow-ups/` | G3+ | Create post-event follow-up tasks |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/{event_id}/conversions/` | G1+ | Conversion data — attendees who applied/enrolled |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/analytics/funnel/` | G1+ | Conversion funnel chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/analytics/monthly-trend/` | G1+ | Monthly trend chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/analytics/branch-performance/` | G1+ | Branch comparison chart |
| GET | `/api/v1/group/{id}/marketing/enrollment/open-days/analytics/type-effectiveness/` | G1+ | Event type donut |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../open-days/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#openday-content` | `innerHTML` | `hx-trigger="click"` |
| Calendar load | Calendar tab | `hx-get=".../open-days/calendar/?month={m}&year={y}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="load"` |
| Calendar month nav | ◀ ▶ buttons | `hx-get=".../open-days/calendar/?month={m}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Event detail drawer | Event click (calendar/table) | `hx-get=".../open-days/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create event | Form submit | `hx-post=".../open-days/"` | `#create-result` | `innerHTML` | Toast + calendar/table refresh |
| Send invites | Invite form | `hx-post=".../open-days/{id}/invites/"` | `#invite-result` | `innerHTML` | Toast + progress bar |
| RSVP table | RSVP tab | `hx-get=".../open-days/{id}/rsvps/"` | `#rsvp-table-body` | `innerHTML` | `hx-trigger="load"` |
| Check-in search | Phone input | `hx-get=".../open-days/{id}/rsvps/?phone={val}"` | `#checkin-result` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Check-in submit | Check In button | `hx-post=".../open-days/{id}/check-in/"` | `#checkin-confirm` | `innerHTML` | Toast + token display |
| Attendance update | Progress checkbox | `hx-patch=".../open-days/{id}/attendance/{att_id}/"` | `#att-row-{att_id}` | `innerHTML` | Inline update |
| Feedback submit | Feedback form | `hx-post=".../open-days/{id}/feedback/"` | `#feedback-result` | `innerHTML` | Thank-you message |
| Follow-up create | Follow-up form | `hx-post=".../open-days/{id}/follow-ups/"` | `#followup-result` | `innerHTML` | Toast |
| Filter apply | Dropdowns | `hx-get` with params | `#event-table-body` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#event-table-body` | `innerHTML` | 25/page |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
