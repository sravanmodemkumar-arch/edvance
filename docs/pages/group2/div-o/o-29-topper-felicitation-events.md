# O-29 — Topper Felicitation & Events

> **URL:** `/group/marketing/toppers/events/`
> **File:** `o-29-topper-felicitation-events.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Topper Relations Manager (Role 120, G3) — primary operator

---

## 1. Purpose

The Topper Felicitation & Events page is the operational hub for planning, executing, and documenting every topper celebration event the group conducts — from grand district-level felicitation ceremonies with the Chief Minister on stage to small branch-level gatherings honouring subject toppers. In the Indian education market, felicitation events are not mere celebrations; they are the single highest-ROI marketing investment a group can make. A well-photographed stage with 200 toppers in convocation gowns, a Chief Guest who is a sitting MLA or IAS officer, weeping parents receiving bouquets, and a 40-foot flex backdrop with the group's logo — this one event generates a full-page newspaper ad (free editorial coverage), 50 WhatsApp-shareable photos, 10 video clips for social media, and word-of-mouth that no paid campaign can replicate.

The problems this page solves:

1. **Event chaos at scale:** A group with 30 branches and 1,500 toppers cannot felicitate everyone in one event. Felicitation must be tiered: Grand Felicitation (top 50 across group), Branch-level (top 20 per branch), Subject Topper (centum achievers), Competitive Exam (JEE/NEET qualifiers), Alumni Homecoming (previous-year toppers now at IIT/AIIMS). Without a system, scheduling overlaps, venue double-bookings, and guest conflicts are inevitable.

2. **Chief Guest and VIP management:** The Chairman wants the Education Minister at the Grand Felicitation. The branch wants the local MLA. The PR team wants a Bollywood celebrity alumnus. Managing invite lists, confirmations, protocol requirements (security, seating, welcome address order), and last-minute cancellations requires structured tracking — not WhatsApp group chaos.

3. **RSVP and attendance:** 200 toppers are invited but only 140 confirm. 30 parents say they'll come but 50 show up. Venue capacity is 300 but 400 walk in. The RSVP system must handle confirmations, dietary preferences (for banquet), transport arrangements (AC bus pickup from branches), and day-of attendance marking.

4. **Media and press coordination:** Every Grand Felicitation must have: press invite list (20–50 journalists), press kit (topper data, photos, group achievements, chairman's quote), designated photo opportunities (chief guest with top 3 rankers, group photo, parent moments), and post-event press release. Without structured press management, the event gets zero coverage despite ₹10–20L spend.

5. **Post-event asset capture:** The event produces 500–2,000 photos, 5–20 video clips, press clippings, and social media posts. These assets feed O-03 (Material Library), O-31 (Success Stories), O-12 (WhatsApp campaigns), and next season's prospectus. The system must collect, tag, and distribute these assets within 24 hours.

**Scale:** 3–8 events/season per group · 50–2,000 invitees per event · 5–15 chief guests across events · 20–100 press invites · 500–5,000 photos per season · ₹2L–₹25L budget per event

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Topper Relations Manager | 120 | G3 | Full CRUD — create events, manage RSVP, assign tasks, upload media | Primary operator |
| Group Admissions Campaign Manager | 119 | G3 | Read + Contribute — view events, add campaign tie-ins | Cross-promote with enrollment drives |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — upload photos/videos, download press kits | Post-event asset management |
| Group Admission Data Analyst | 132 | G1 | Read — event analytics, attendance reports, media reach | MIS and reporting |
| Branch Principal | — | G3 | Read + RSVP (own branch) — confirm branch topper attendance, submit logistics | Branch-level coordination |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve chief guest invites, event budgets, press releases | Final authority |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Event creation/editing: role 120 or G4+. Chief guest invite approval: G4/G5. RSVP management: 120 + Branch Principals. Press kit release: 120 with G4 approval.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Topper Relations  ›  Topper Felicitation & Events
```

### 3.2 Page Header
```
Topper Felicitation & Events                         [+ Create Event]  [Press Kit Builder]  [Export]
Topper Relations Manager — Lakshmi Naidu
Sunrise Education Group · Season 2025-26 · 5 events planned · 3 completed · 1,240 toppers felicitated · 8 chief guests
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Events This Season | Integer | COUNT WHERE season = current | Static blue | `#kpi-events` |
| 2 | Toppers Felicitated | Integer | SUM(attendance) WHERE role = 'topper' across all completed events | Static green | `#kpi-felicitated` |
| 3 | RSVP Pending | Integer | COUNT WHERE rsvp_status = 'invited' AND event_date > today | Red > 100, Amber 20–100, Green < 20 | `#kpi-rsvp-pending` |
| 4 | Chief Guests Confirmed | N/M | Confirmed / Invited across upcoming events | Green = all confirmed, Red = any unconfirmed within 7 days | `#kpi-chief-guests` |
| 5 | Media Coverage | Integer | COUNT(press_mentions) across all events this season | Static blue | `#kpi-media` |
| 6 | Total Budget Spent | ₹ Amount | SUM(actual_spend) / SUM(budgeted) across events | Red > 110%, Amber 90–110%, Green < 90% | `#kpi-budget` |

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Upcoming Events** — Events in planning or confirmed stage
2. **Completed Events** — Past events with outcomes and media
3. **RSVP Tracker** — Cross-event RSVP and attendance dashboard
4. **Press & Media** — Press invites, coverage, clippings across all events

### 5.2 Tab 1: Upcoming Events

**Card-based layout (1 card per event):**

```
┌─────────────────────────────────────────────────────────────────┐
│  🏆 Grand Topper Felicitation 2025-26                          │
│  Type: Grand Felicitation · Status: ✅ Confirmed                │
│  Date: 15 Jun 2026 · 10:00 AM – 2:00 PM                       │
│  Venue: Shilpakala Vedika, Hyderabad (Cap: 2,000)             │
│  Chief Guest: Hon. Minister of Education (Confirmed ✅)         │
│                                                                 │
│  Invitees: 320 toppers · 320 parents · 50 teachers · 30 VIPs  │
│  RSVP: 280/320 confirmed ████████████░░░ 87%                   │
│  Budget: ₹18,50,000 allocated                                  │
│  Press: 35 journalists invited · 22 confirmed                  │
│                                                                 │
│  [View Details] [Manage RSVP] [Press Kit] [Edit] [Cancel]     │
└─────────────────────────────────────────────────────────────────┘
```

**Also available as table (toggle view):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Event Name | Text (link) | Yes | Click → detail drawer |
| Type | Badge | Yes | Grand / Branch-level / Subject Topper / Competitive Exam / Alumni Homecoming |
| Date & Time | Datetime | Yes | — |
| Venue | Text | Yes | Venue name + city |
| Chief Guest | Text | Yes | Name + designation; badge if confirmed/pending |
| Invitees | Integer | Yes | Total invited count |
| RSVP % | Progress bar | Yes | Confirmed / Invited |
| Budget (₹) | Amount | Yes | Allocated amount |
| Press Confirmed | Integer | Yes | — |
| Status | Badge | Yes | Draft / Planning / Confirmed / In Progress / Completed / Cancelled |
| Actions | Buttons | No | [View] [Edit] [RSVP] [Press Kit] |

**Default sort:** Date ASC (nearest event first)
**Pagination:** Server-side · 20/page

### 5.3 Tab 2: Completed Events

Same table structure as Tab 1, plus outcome columns:

| Additional Column | Type | Notes |
|---|---|---|
| Attendance | Integer | Actual attendees vs invited |
| Photos Uploaded | Integer | Count of event photos in system |
| Press Mentions | Integer | Newspaper/TV/online mentions captured |
| Post-Event Rating | Stars (1–5) | Internal quality rating by G4/G5 |

### 5.4 Tab 3: RSVP Tracker

**Filter bar:** Event · Branch · RSVP Status (Invited/Confirmed/Declined/Attended/No-show) · Role (Topper/Parent/Teacher/VIP/Press)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Invitee Name | Text | Yes | — |
| Role | Badge | Yes | Topper / Parent / Teacher / VIP / Chief Guest / Press |
| Event | Text | Yes | — |
| Branch | Text | Yes | — |
| Phone | Text | No | For follow-up calls |
| RSVP Status | Badge | Yes | Invited / Confirmed / Declined / Waitlisted |
| Transport | Badge | No | Self / Group Bus / Need Pickup |
| Dietary | Badge | No | Veg / Non-veg / Jain / No preference |
| Attendance | Badge | Yes | — (blank) / ✅ Present / ❌ No-show |
| Actions | Buttons | No | [Confirm] [Decline] [Call] [Mark Attended] |

### 5.5 Tab 4: Press & Media

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Event | Text | Yes | — |
| Journalist Name | Text | Yes | — |
| Publication | Text | Yes | Eenadu / Sakshi / Deccan Chronicle / TV9 / etc. |
| Type | Badge | Yes | Print / TV / Online / Wire Agency |
| Invite Status | Badge | Yes | Invited / Confirmed / Attended / Not Responded |
| Press Kit Sent | Badge | No | ✅ / ❌ |
| Coverage | Badge | Yes | Published / Not Yet / No Coverage |
| Clipping Link | URL | No | Link to scan/screenshot of published coverage |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-event` (720px)

- **Title:** "Create Felicitation Event"
- **Fields:**
  - **Event details:**
    - Event name (text, required — e.g., "Grand Topper Felicitation 2025-26")
    - Event type (dropdown, required):
      - **Grand Felicitation** — Group-level mega event for top rankers across all branches; 500–2,000 attendees; chief guest mandatory
      - **Branch-level Felicitation** — Single branch celebrates its toppers; 50–200 attendees; local chief guest
      - **Subject Topper Ceremony** — Centum achievers (100/100) felicitated; often combined with branch event
      - **Competitive Exam Felicitation** — JEE/NEET/CLAT qualifiers; focused event with career guidance session
      - **Alumni Homecoming** — Previous-year toppers now at IIT/AIIMS/NLU return to inspire current batches
    - Branches (multi-select): All / Specific branches (for branch-level events)
    - Season (dropdown): 2025-26 / 2024-25 / etc.
  - **Schedule:**
    - Date (date, required)
    - Start time (time, required)
    - End time (time, required)
    - Rehearsal date & time (datetime, optional)
  - **Venue:**
    - Venue name (text, required)
    - Venue address (textarea)
    - City (text)
    - Capacity (integer, required)
    - Venue type (dropdown): Auditorium / Convention Centre / School Hall / Open Ground / Hotel Banquet
    - Venue cost (₹, optional)
    - Parking capacity (integer, optional)
    - AC available? (toggle)
  - **Chief Guest:**
    - Chief guest name (text)
    - Designation (text — "Hon. Education Minister, Govt. of Telangana")
    - Contact person (text — PA/secretary name)
    - Contact phone (text)
    - Invite status (dropdown): Not Yet Invited / Invited / Confirmed / Declined / Tentative
    - Protocol notes (textarea — security requirements, arrival time, seating, address duration)
    - Backup chief guest (text, optional)
  - **Budget:**
    - Estimated budget (₹, required)
    - Budget breakdown (repeating rows):
      - Line item (text — Venue / Catering / Decoration / Printing / Transport / Gifts / AV Equipment / Photography / Press Kits / Miscellaneous)
      - Amount (₹)
  - **Agenda template:**
    - Agenda items (repeating rows, sortable):
      - Time (text — "10:00 AM")
      - Item (text — "Welcome Address by Principal")
      - Speaker/Presenter (text)
      - Duration (minutes)
  - **Topper selection:**
    - Auto-select from O-28 (filter: branch, board/exam, percentage/rank threshold)
    - Manual add (search O-28 database)
    - Minimum criteria (e.g., ≥ 95% for Grand, ≥ 90% for Branch-level)
  - **Notes:** Internal notes (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 120 or G4+

### 6.2 Modal: `manage-chief-guest` (560px)

- **Title:** "Chief Guest Management — [Event Name]"
- **Sections:**
  - **Primary guest:** Name, designation, invite letter (upload PDF), invite status, confirmation date
  - **Protocol checklist:**
    - ☐ Official invite letter sent (registered post + email)
    - ☐ PA/secretary confirmation received
    - ☐ Security clearance (if govt. official)
    - ☐ Stage seating arrangement confirmed
    - ☐ Welcome bouquet and memento arranged
    - ☐ Address duration agreed (typically 10–15 min)
    - ☐ Departure protocol confirmed
  - **Backup guests:** List of 2–3 alternatives with invite status
  - **History:** All communication log with chief guest office
- **Buttons:** Close · Update Status · Send Reminder
- **Access:** Role 120 or G4+

### 6.3 Modal: `press-kit-builder` (640px)

- **Title:** "Press Kit — [Event Name]"
- **Auto-populated sections:**
  - Group name, event name, date, venue, chief guest
  - Topper summary: total toppers, board-wise breakdown, top 10 with photos
  - Key statistics: "4,200 students scored above 90%," "312 cracked JEE Advanced Top 10,000"
  - Chairman's quote (textarea — editable)
  - Director's quote (textarea — editable)
  - Group achievements bullet points (textarea)
  - Contact person for media queries
- **Attachments:**
  - High-res group logo (auto-attached from O-02)
  - Top 10 topper photos (auto-pulled from O-28)
  - Previous press coverage samples
- **Output formats:**
  - PDF press kit (branded)
  - Plain text (for email to journalists)
  - WhatsApp-friendly summary (short version)
- **Buttons:** Cancel · Preview · Download PDF · Email to Press List
- **Access:** Role 120, 131, or G4+

### 6.4 Drawer: `event-detail` (720px, right-slide)

- **Tabs:** Overview · Agenda · Invitees · Chief Guest · Budget · Media · Post-Event
- **Overview tab:** Event card (type, date, venue, status), key metrics (invited, confirmed, budget)
- **Agenda tab:** Timeline view of event programme; drag-reorder items; print-ready agenda
- **Invitees tab:** Topper list with RSVP status, parent confirmations, teacher list; bulk actions (send reminder, mark confirmed)
- **Chief Guest tab:** Guest details, protocol checklist, communication log
- **Budget tab:** Line-item budget vs actual spend; variance; approval status
- **Media tab:** Uploaded photos (grid), videos, press clippings; tag photos by moment (stage, group photo, chief guest, parents)
- **Post-Event tab:** Attendance summary, media coverage count, internal rating, lessons learned (textarea)
- **Footer:** [Edit] [Send RSVP Reminders] [Generate Press Kit] [Upload Photos] [Complete Event] [Cancel Event]

### 6.5 Modal: `rsvp-bulk-action` (480px)

- **Title:** "Bulk RSVP Action"
- **Select:** All pending / All from branch X / Custom selection
- **Action:** Send WhatsApp reminder / Send SMS / Mark as Confirmed / Mark as Declined
- **Message template:** Pre-filled (editable) — "Respected Parent, your ward [Name] is invited to the Grand Topper Felicitation on [Date] at [Venue]. Please confirm attendance by [Deadline]. Reply YES to confirm."
- **Buttons:** Cancel · Send to [N] recipients
- **Access:** Role 120 or G4+

### 6.6 Modal: `upload-event-media` (640px)

- **Title:** "Upload Event Media — [Event Name]"
- **Upload:** Drag-and-drop zone (JPEG/PNG/MP4, max 20 MB per file, max 200 files per batch)
- **Auto-tag options:** Stage Photos / Group Photo / Chief Guest Moments / Parent Moments / Award Ceremony / Press Conference / Candid
- **Photographer credit:** (text, optional)
- **Watermark:** Toggle — apply group logo watermark to all photos
- **Post-upload:** Auto-sync selected photos to O-03 (Material Library)
- **Buttons:** Cancel · Upload [N] Files
- **Access:** Role 120, 131, or G4+

---

## 7. Charts

### 7.1 Events by Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Events by Type — This Season" |
| Data | COUNT per event_type |
| Colour | Per type (Grand = gold, Branch = blue, Subject = green, Competitive = purple, Alumni = teal) |
| Centre text | Total: [N] events |
| API | `GET /api/v1/group/{id}/marketing/toppers/events/analytics/by-type/` |

### 7.2 RSVP Funnel (Horizontal Stacked Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal stacked bar |
| Title | "RSVP Status — [Event Name]" |
| Data | Per event: Invited / Confirmed / Declined / Waitlisted / Attended / No-show |
| Colour | Invited = grey, Confirmed = green, Declined = red, Waitlisted = amber, Attended = emerald, No-show = rose |
| API | `GET /api/v1/group/{id}/marketing/toppers/events/analytics/rsvp-funnel/` |

### 7.3 Budget vs Actual (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar |
| Title | "Budget vs Actual Spend by Event" |
| Data | Per event: budgeted (bar 1) vs actual (bar 2) |
| Colour | Budgeted = `#3B82F6` blue, Actual = `#10B981` green (red if > 110% of budget) |
| API | `GET /api/v1/group/{id}/marketing/toppers/events/analytics/budget-vs-actual/` |

### 7.4 Media Coverage by Event (Bar)

| Property | Value |
|---|---|
| Chart type | Bar |
| Title | "Press Mentions per Event" |
| Data | COUNT(press_mentions) per event, split by type (Print / TV / Online) |
| Colour | Print = `#6366F1`, TV = `#EC4899`, Online = `#14B8A6` |
| API | `GET /api/v1/group/{id}/marketing/toppers/events/analytics/media-coverage/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Event created | "Event '[Name]' created — [Type] on [Date]" | Success | 3s |
| Event approved | "Event '[Name]' approved by [Approver]" | Success | 3s |
| Chief guest confirmed | "Chief Guest '[Name]' confirmed for '[Event]'" | Success | 4s |
| Chief guest declined | "Chief Guest '[Name]' declined — activate backup" | Warning | 5s |
| RSVP reminder sent | "RSVP reminders sent to [N] invitees" | Success | 3s |
| Bulk RSVP confirmed | "[N] invitees confirmed for '[Event]'" | Success | 3s |
| Press kit generated | "Press kit for '[Event]' ready — download or email" | Success | 4s |
| Photos uploaded | "[N] photos uploaded for '[Event]' — tagging in progress" | Success | 3s |
| Event completed | "Event '[Name]' marked complete — [N] attended" | Success | 4s |
| Event cancelled | "Event '[Name]' cancelled" | Warning | 4s |
| Budget exceeded | "Warning: '[Event]' actual spend exceeds budget by ₹[X]" | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No events this season | 🏆 | "No Felicitation Events" | "Plan your first topper felicitation event for this results season." | Create Event |
| No upcoming events | 📅 | "No Upcoming Events" | "All events are completed or no new events have been planned." | Create Event |
| No RSVP data | 📋 | "No Invitees Yet" | "Add toppers from O-28 database to start sending invitations." | Select Toppers |
| No press invites | 📰 | "No Press Invites" | "Add journalists to the press invite list for media coverage." | Add Press Contact |
| No photos uploaded | 📸 | "No Event Photos" | "Upload photos from the completed event for marketing assets." | Upload Photos |
| No chief guest | 🎤 | "No Chief Guest Assigned" | "Invite a chief guest to add prestige to the felicitation ceremony." | Add Chief Guest |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + event cards skeleton (3 cards) |
| Tab switch | Content skeleton |
| Event detail drawer | 720px skeleton: overview card + 7 tabs |
| RSVP table load | Filter bar + table skeleton (20 rows) |
| Press kit generation | Spinner: "Generating press kit…" |
| Photo upload | Progress bar per file + overall progress |
| Chief guest modal | Form skeleton |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/toppers/events/` | G1+ | List all events (filterable) |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/` | G1+ | Event detail |
| POST | `/api/v1/group/{id}/marketing/toppers/events/` | G3+ | Create event |
| PUT | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/` | G3+ | Update event |
| DELETE | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/` | G4+ | Delete event |
| PATCH | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/status/` | G3+ | Change status (confirm/complete/cancel) |
| PATCH | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/approve/` | G4+ | Approve event |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/invitees/` | G1+ | List invitees with RSVP status |
| POST | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/invitees/` | G3+ | Add invitees (from O-28) |
| PATCH | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/invitees/{invitee_id}/rsvp/` | G3+ | Update RSVP status |
| POST | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/invitees/remind/` | G3+ | Send bulk RSVP reminders |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/chief-guest/` | G1+ | Chief guest details |
| PUT | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/chief-guest/` | G3+ | Update chief guest |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/agenda/` | G1+ | Event agenda |
| PUT | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/agenda/` | G3+ | Update agenda |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/budget/` | G1+ | Budget breakdown |
| PUT | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/budget/` | G3+ | Update budget |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/press/` | G1+ | Press invite list |
| POST | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/press/` | G3+ | Add press contacts |
| POST | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/press-kit/` | G2+ | Generate press kit |
| GET | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/media/` | G1+ | List event media |
| POST | `/api/v1/group/{id}/marketing/toppers/events/{event_id}/media/` | G2+ | Upload photos/videos |
| GET | `/api/v1/group/{id}/marketing/toppers/events/kpis/` | G1+ | KPIs |
| GET | `/api/v1/group/{id}/marketing/toppers/events/analytics/by-type/` | G1+ | Type donut |
| GET | `/api/v1/group/{id}/marketing/toppers/events/analytics/rsvp-funnel/` | G1+ | RSVP funnel |
| GET | `/api/v1/group/{id}/marketing/toppers/events/analytics/budget-vs-actual/` | G1+ | Budget chart |
| GET | `/api/v1/group/{id}/marketing/toppers/events/analytics/media-coverage/` | G1+ | Media chart |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../events/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#events-content` | `innerHTML` | `hx-trigger="click"` |
| Event detail drawer | Card/row click | `hx-get=".../events/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create event | Form submit | `hx-post=".../events/"` | `#create-result` | `innerHTML` | Toast + redirect |
| RSVP update | Status button | `hx-patch=".../events/{id}/invitees/{iid}/rsvp/"` | `#rsvp-badge-{iid}` | `innerHTML` | Inline badge update |
| Bulk RSVP remind | Remind form | `hx-post=".../events/{id}/invitees/remind/"` | `#remind-result` | `innerHTML` | Toast |
| Press kit generate | Generate button | `hx-post=".../events/{id}/press-kit/"` | `#press-kit-preview` | `innerHTML` | Shows PDF preview |
| Photo upload | Drop zone | `hx-post=".../events/{id}/media/"` | `#media-grid` | `beforeend` | `hx-encoding="multipart/form-data"` |
| Status change | Status button | `hx-patch=".../events/{id}/status/"` | `#status-badge-{id}` | `innerHTML` | Inline update |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#events-table-body` | `innerHTML` | 20/page |
| Chart load | Tab/page load | `hx-get=".../events/analytics/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
