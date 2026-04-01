# 06 — Group Alumni Relations Dashboard

- **URL:** `/group/adm/alumni/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Alumni Relations Manager (Role 28, G3)

---

## 1. Purpose

The Group Alumni Relations Dashboard is the management interface for maintaining, growing, and leveraging the group's alumni network in service of the institution's admissions and reputation goals. Alumni are a measurable channel for new admissions through referrals, and this page makes that channel quantifiable and actionable. The manager can track every referred applicant from initial contact through enrollment, manage the topper profiles featured in marketing materials, and organise alumni events — all from a single page that removes the need for external spreadsheets or separate CRM tools.

The topper profiles section reflects a specific admissions strategy used by educational institutions: featuring past toppers with their achievements, streams, and college admissions as social proof to attract new students. The dashboard lets the manager create, edit, and feature topper cards that are published to the group's marketing pages. The alumni database summary gives demographic insight — which batches, branches, and streams are most represented in the network — helping the manager prioritise outreach to under-connected cohorts and plan reunion or felicitation events accordingly.

Referral tracking closes the loop between alumni engagement and admissions outcomes. Each referred student is tracked from application to enrollment, and referring alumni are ranked on a leaderboard that can support reward and recognition programmes. The alumni engagement metrics chart shows trends in network activity — registrations, referrals, and event RSVPs over the past 12 months — giving the manager evidence for reporting to the Admissions Director on the ROI of alumni relations activities. Together, these features position alumni not merely as a database to be maintained but as an active, measurable admissions channel.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Alumni Relations Manager | G3 | Full read + write + publish | Primary owner of this page |
| Group Admissions Director | G3 | Read-only (all sections) | View only; no actions |
| Group Admission Coordinator | G3 | Read — Section 5.2 (Referral Pipeline) only | Coordination of referred applicants only |
| Group Marketing Director | G3 | Read — Section 5.3 (Topper Profiles) only | Topper content for marketing use |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Alumni Relations
```

### 3.2 Page Header
- **Title:** `Alumni Relations Dashboard`
- **Subtitle:** `Group Admissions · Academic Year: [Year]`
- **Role Badge:** `Group Alumni Relations Manager`
- **Right-side controls:** `[+ Add Alumni]` `[+ Create Event]` `[Export Alumni Database]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Alumni event in < 7 days with RSVP < 50% of expected | "Event '[Name]' on [Date] has only [N] RSVPs against [Target] expected. Send invitations." | Warning (amber) |
| Referred applicant in pipeline > 14 days without action | "[N] referred application(s) have not been actioned in over 14 days." | Warning (amber) |
| No new alumni registrations in > 30 days | "No new alumni have registered in the past 30 days. Consider an outreach campaign." | Info (blue) |
| Topper profiles unpublished for current year | "[N] topper profile(s) for [Year] are drafted but not yet published." | Info (blue) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Alumni in Database | Count of all records in alumni registry | `alumni_registry` | Blue (informational) | Opens alumni database modal |
| Referral Admissions This Year | Alumni who have referred at least one enrolled student this year | `alumni_referral` WHERE enrolled_student IS NOT NULL AND year = current | Green ≥ 20; amber 5–19; red < 5 | Scrolls to Section 5.2 |
| Topper Profiles Published | Count of published topper profiles across all years | `topper_profile` WHERE status = 'published' | Blue (informational) | Scrolls to Section 5.3 |
| Upcoming Alumni Events | Count of events scheduled in next 60 days | `alumni_event` WHERE date ≤ today+60 AND status ≠ 'completed' | Blue (informational) | Scrolls to Section 5.4 |
| Referral Conversion Rate | (Enrolled via referral / Total referred applicants) × 100 this year | `alumni_referral` + `enrollment` | Green ≥ 40%; amber 20–39%; red < 20% | Opens referral pipeline detail |
| New Alumni This Month | Alumni registered this calendar month | `alumni_registry` WHERE created_month = current | Green ≥ 10; amber 1–9; red = 0 | Opens alumni database filtered |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Alumni Database Summary

**Display:** Top row of stat cards (total alumni, by year of passing as a scrollable mini-table, by stream, by branch). Below: Chart.js 4.x doughnut chart by stream. Summary stat row below chart.

**Stat Cards:** Total Alumni | This Year's Batch | Last Year's Batch | By Stream (count per stream) | By Branch (count per branch, top 5)

**Doughnut Chart:** Segments by stream — MPC, BiPC, MEC, CEC, Commerce, Arts, Others. Hover tooltip shows count and %.

**Filters:** Year of Passing (range), Branch, Stream

**HTMX Pattern:**
```html
<div id="alumni-summary"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/summary/"
     hx-trigger="load, change from:#alumni-filters"
     hx-target="#alumni-summary"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: people icon. "No alumni records found. Start building the alumni database by adding records."

---

### 5.2 Referral Admissions Pipeline

**Display:** Sortable, filterable table. Each row is a student referred by an alumni member. Tracks status from application through enrollment.

**Columns:** Applicant Name | Referring Alumni | Referring Alumni Batch | Branch Applied | Status | Applied On | Action

**Status Badge Values:** Enquiry (blue) | Application Submitted (amber) | Under Review (purple) | Offered (teal) | Enrolled (green) | Rejected (red) | Withdrawn (muted)

**Actions per row:** `[View →]` opens referral-pipeline-detail drawer.

**Filters:** Branch, Status, Year, Referring Alumni (search field), Date range

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="referral-pipeline"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/referrals/"
     hx-trigger="load, change from:#referral-filters"
     hx-target="#referral-pipeline"
     hx-swap="innerHTML">
```

**Empty State:** "No referred applications on record for the selected filters. Share alumni referral links to generate referrals."

---

### 5.3 Topper Profiles

**Display:** Card grid (3 columns on desktop, 1 on mobile). Each card is a topper profile. Published profiles have a green "Published" badge; drafts have an amber "Draft" badge; archived profiles are muted.

**Fields per card:** Photo placeholder (or uploaded image) | Student Name | Year | Stream | Rank / Achievement | College Admitted To | Branch | Published/Draft badge | Action buttons

**Actions per card:** `[Edit →]` opens topper-profile-editor drawer | `[View →]` opens public profile preview | `[Feature →]` marks as "Featured" for homepage display | `[Unpublish]` (for published profiles)

**Filters:** Year, Stream, Branch, Status (Published / Draft / Archived / Featured), Search by name

**HTMX Pattern:**
```html
<div id="topper-profiles"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/topper-profiles/"
     hx-trigger="load, change from:#topper-filters"
     hx-target="#topper-profiles"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: trophy icon. "No topper profiles yet. Create profiles to feature on your admissions marketing pages."

---

### 5.4 Upcoming Alumni Events

**Display:** Timeline list. Each event is a card in chronological order. Events within 7 days are highlighted. RSVP count shown with a progress bar toward expected attendance.

**Fields per event card:** Date & Time | Event Name | Type (Reunion / Webinar / Felicitation / Campus Visit / Career Talk) | Expected Attendance | RSVP Count | RSVP % (progress bar) | Status Badge | Action

**Status Badge Values:** Planned (blue) | Invitations Sent (amber) | Registration Open (green) | Concluded (muted) | Cancelled (red)

**Actions per card:** `[Manage →]` opens event-detail drawer.

**Filters:** Event Type, Status, Date range

**HTMX Pattern:**
```html
<div id="alumni-events"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/events/"
     hx-trigger="load, change from:#event-filters"
     hx-target="#alumni-events"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: calendar icon. "No alumni events scheduled. Create an event to engage your alumni network."

---

### 5.5 Top Referring Alumni

**Display:** Leaderboard table. Ranked by number of successful referral enrollments. Top 3 rows have a gold/silver/bronze left-border accent. Ties broken by most recent referral date.

**Columns:** Rank | Alumni Name | Batch Year | Branch | # Successful Referrals | # Pending Referrals | Referral Reward Status | Last Referral Date

**Referral Reward Status Badge:** Pending (amber) | Claimed (green) | Not Eligible (muted)

**Filters:** Year (academic year of referrals), Branch, Batch Year

**HTMX Pattern:**
```html
<div id="referral-leaderboard"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/referral-leaderboard/"
     hx-trigger="load, change from:#leaderboard-filters"
     hx-target="#referral-leaderboard"
     hx-swap="innerHTML">
```

**Empty State:** "No successful referrals recorded yet. The leaderboard will populate as referred students enroll."

---

### 5.6 Alumni Engagement Metrics

**Display:** Chart.js 4.x multi-line chart. Three lines over the last 12 months: New Registrations (blue), Referrals Submitted (green), Event RSVPs (amber). X-axis = month labels, Y-axis = count. Legend with toggle per line.

**Filters:** None (always last 12 months; chart respects no external filters to maintain longitudinal consistency)

**Below Chart Summary Row:** Total registrations (12M) | Total referrals (12M) | Total RSVPs (12M) | Most active month

**HTMX Pattern:**
```html
<div id="engagement-metrics"
     hx-get="/api/v1/group/{{ group_id }}/adm/alumni/engagement-metrics/"
     hx-trigger="load"
     hx-target="#engagement-metrics"
     hx-swap="innerHTML">
```

**Empty State:** "Engagement data will appear here after at least one month of alumni activity."

---

## 6. Drawers & Modals

### 6.1 Alumni Profile Detail Drawer
- **Width:** 640px
- **Trigger:** Click on any alumni name in Section 5.2, 5.5, or the alumni database modal
- **Tabs:**
  - **Profile:** Name, batch year, branch, stream, contact details, current city/college, occupation (if known)
  - **Referrals:** All referrals submitted by this alumni — applicant name, status, date
  - **Events:** Events attended by this alumni
  - **Edit:** Editable profile form (Alumni Manager only) with `[Save Changes]`
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/alumni/{{ alumni_id }}/"`

### 6.2 Referral Pipeline Detail Drawer
- **Width:** 560px
- **Trigger:** `[View →]` in Section 5.2
- **Tabs:**
  - **Referral Details:** Referring alumni info, applicant info, referral date, channel used (personal / link / event)
  - **Application Timeline:** Stage history of the referred applicant
  - **Notes:** Free-text notes field for coordination
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/alumni/referrals/{{ referral_id }}/"`

### 6.3 Topper Profile Editor Drawer
- **Width:** 640px
- **Trigger:** `[Edit →]` in Section 5.3 or `[+ New Topper Profile]`
- **Tabs:**
  - **Details:** Name, year, stream, branch, subjects, rank, achievement, college admitted to, quote
  - **Photo:** Photo upload (JPEG/PNG, max 2MB), preview, crop tool
  - **Publish Settings:** Status (Draft / Published / Featured), Display order, `[Save]` `[Publish]`
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/alumni/topper-profiles/{{ profile_id }}/"` (GET); `hx-post` on save

### 6.4 Alumni Event Detail Drawer
- **Width:** 640px
- **Trigger:** `[Manage →]` in Section 5.4
- **Tabs:**
  - **Event Info:** Name, type, date/time, venue/link, description, organiser
  - **RSVPs:** Table of alumni who have RSVP'd — Name, batch, branch, attendance confirmed, dietary/access notes
  - **Invitations:** Send invitation form — target audience filters (batch / branch / stream), channel (Email / WhatsApp), `[Send Invitations]`
  - **Post-Event:** Attendance count, feedback summary (after event date) — visible post-event only
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/alumni/events/{{ event_id }}/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Alumni record added | "Alumni record for [Name] added to the database." | Success | 4s |
| Alumni profile updated | "Alumni profile for [Name] updated." | Success | 3s |
| Topper profile published | "Topper profile for [Name] published successfully." | Success | 4s |
| Topper profile featured | "[Name]'s profile is now featured on the admissions page." | Success | 4s |
| Topper profile saved as draft | "Profile saved as draft. Publish when ready." | Info | 3s |
| Event created | "Alumni event '[Name]' created for [Date]." | Success | 4s |
| Event invitations sent | "Invitations sent to [N] alumni for '[Event Name]'." | Success | 4s |
| Referral reward marked claimed | "Referral reward for [Alumni Name] marked as claimed." | Success | 3s |
| Alumni export initiated | "Alumni database export started. Download link will be emailed to you." | Info | 5s |
| Topper profile unpublished | "[Name]'s topper profile has been unpublished." | Info | 3s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No alumni in database | People icon | "Empty Alumni Database" | "No alumni records found. Add alumni records to start building your network." | `[+ Add Alumni]` |
| No referrals | Network icon | "No Referrals Yet" | "Share your referral programme with alumni to generate referred admissions." | `[Share Referral Link]` |
| No topper profiles | Trophy icon | "No Topper Profiles" | "Create topper profiles to showcase your institution's achievement to new students." | `[+ Create Profile]` |
| No upcoming events | Calendar icon | "No Alumni Events" | "Plan an alumni event to grow engagement and referral activity." | `[+ Create Event]` |
| No engagement data | Chart icon | "No Activity Data Yet" | "Engagement metrics will appear after your first month of alumni activity." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Alumni summary stat cards + chart load | Skeleton stat cards (4 cards) + doughnut spinner |
| Referral pipeline table load | Skeleton table rows (6 rows) |
| Topper profile card grid load | Skeleton profile cards (6 cards, 3-column grid) |
| Alumni events timeline load | Skeleton event cards (3 items) |
| Referral leaderboard load | Skeleton table rows (5 rows) |
| Engagement metrics chart load | Skeleton line chart (3 lines) |
| Drawer content load | Spinner overlay on drawer panel |
| Send invitations action | Spinner on `[Send Invitations]` button |
| Topper photo upload | Upload progress bar |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Alumni Manager | Admissions Director | Admission Coordinator | Marketing Director |
|---|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Referral cards only | Topper + Event cards only |
| Alumni Database Summary (5.1) | Visible | Read only | Hidden | Hidden |
| Referral Admissions Pipeline (5.2) | Visible | Read only | Read only | Hidden |
| Topper Profiles (5.3) | Visible + all actions | Read only | Hidden | Read only |
| `[Edit →]` / `[Feature →]` / `[Unpublish]` buttons | Visible | Hidden | Hidden | Hidden |
| Upcoming Alumni Events (5.4) | Visible + [Manage] | Read only | Hidden | Hidden |
| Top Referring Alumni (5.5) | Visible | Read only | Hidden | Hidden |
| Engagement Metrics chart (5.6) | Visible | Visible | Hidden | Hidden |
| `[+ Add Alumni]` button | Visible | Hidden | Hidden | Hidden |
| `[+ Create Event]` button | Visible | Hidden | Hidden | Hidden |
| `[Export Alumni Database]` button | Visible | Visible | Hidden | Hidden |
| Alumni Profile Drawer — Edit tab | Visible | Hidden | Hidden | Hidden |
| Topper Profile Editor Drawer | Full (edit + publish) | Hidden | Hidden | Read only |
| Event Detail Drawer — Invitations tab | Visible | Hidden | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/alumni/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/alumni/summary/` | JWT G3+ | Alumni database summary stats + chart data |
| GET | `/api/v1/group/{group_id}/adm/alumni/list/` | JWT G3+ | Paginated alumni database |
| POST | `/api/v1/group/{group_id}/adm/alumni/` | JWT G3 | Add new alumni record |
| GET | `/api/v1/group/{group_id}/adm/alumni/{alumni_id}/` | JWT G3+ | Alumni profile detail |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/{alumni_id}/` | JWT G3 | Update alumni profile |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/` | JWT G3+ | Referral admissions pipeline |
| GET | `/api/v1/group/{group_id}/adm/alumni/referrals/{referral_id}/` | JWT G3+ | Referral detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/alumni/topper-profiles/` | JWT G3+ | Topper profiles list (all statuses) |
| GET | `/api/v1/group/{group_id}/adm/alumni/topper-profiles/{profile_id}/` | JWT G3+ | Single topper profile detail |
| POST | `/api/v1/group/{group_id}/adm/alumni/topper-profiles/` | JWT G3 | Create new topper profile |
| PATCH | `/api/v1/group/{group_id}/adm/alumni/topper-profiles/{profile_id}/` | JWT G3 | Update / publish topper profile |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/` | JWT G3+ | Alumni events list |
| GET | `/api/v1/group/{group_id}/adm/alumni/events/{event_id}/` | JWT G3+ | Event detail for drawer |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/` | JWT G3 | Create new alumni event |
| POST | `/api/v1/group/{group_id}/adm/alumni/events/{event_id}/invite/` | JWT G3 | Send event invitations to alumni |
| GET | `/api/v1/group/{group_id}/adm/alumni/referral-leaderboard/` | JWT G3+ | Top referring alumni ranked list |
| GET | `/api/v1/group/{group_id}/adm/alumni/engagement-metrics/` | JWT G3+ | 12-month engagement trend data |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/alumni/kpis/` | `#kpi-bar` | `innerHTML` |
| Alumni summary filter change | `change from:#alumni-filters` | GET `/api/v1/group/{{ group_id }}/adm/alumni/summary/` | `#alumni-summary` | `innerHTML` |
| Referral pipeline filter change | `change from:#referral-filters` | GET `/api/v1/group/{{ group_id }}/adm/alumni/referrals/` | `#referral-pipeline` | `innerHTML` |
| Open referral detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/alumni/referrals/{{ referral_id }}/` | `#drawer-panel` | `innerHTML` |
| Topper profiles filter change | `change from:#topper-filters` | GET `/api/v1/group/{{ group_id }}/adm/alumni/topper-profiles/` | `#topper-profiles` | `innerHTML` |
| Open topper profile editor | `click` | GET `/api/v1/group/{{ group_id }}/adm/alumni/topper-profiles/{{ profile_id }}/` | `#drawer-panel` | `innerHTML` |
| Save topper profile | `click from:#btn-save-topper` | POST `/api/v1/group/{{ group_id }}/adm/alumni/topper-profiles/{{ profile_id }}/` | `#topper-profiles` | `innerHTML` |
| Alumni events filter change | `change from:#event-filters` | GET `/api/v1/group/{{ group_id }}/adm/alumni/events/` | `#alumni-events` | `innerHTML` |
| Open event detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/alumni/events/{{ event_id }}/` | `#drawer-panel` | `innerHTML` |
| Send event invitations | `click from:#btn-send-invites` | POST `/api/v1/group/{{ group_id }}/adm/alumni/events/{{ event_id }}/invite/` | `#invite-status` | `innerHTML` |
| Leaderboard filter change | `change from:#leaderboard-filters` | GET `/api/v1/group/{{ group_id }}/adm/alumni/referral-leaderboard/` | `#referral-leaderboard` | `innerHTML` |
| Open alumni profile drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/alumni/{{ alumni_id }}/` | `#drawer-panel` | `innerHTML` |
| Save alumni profile edit | `click from:#btn-save-alumni` | PATCH `/api/v1/group/{{ group_id }}/adm/alumni/{{ alumni_id }}/` | `#alumni-summary` | `innerHTML` |
| Engagement metrics load | `load` | GET `/api/v1/group/{{ group_id }}/adm/alumni/engagement-metrics/` | `#engagement-metrics` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
