# 07 — Group Demo Class Coordinator Dashboard

- **URL:** `/group/adm/demo/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Demo Class Coordinator (Role 29, G3)

---

## 1. Purpose

The Group Demo Class Coordinator Dashboard is the operational centre for managing trial and demonstration classes offered to prospective students across all branches of the group. Demo classes are a direct admissions conversion tool: prospective students attend a sample lesson in their preferred stream, experience the teaching quality first-hand, and are then followed up with a structured outreach effort to convert that positive experience into an enrollment decision. This page gives the coordinator full visibility into all scheduled demos, registered prospects, post-demo outcomes, and pending follow-ups.

A demo class programme spans multiple branches and subjects simultaneously. The coordinator must ensure every branch has scheduled demos within the current admission month, that teaching staff assignments are confirmed, and that registered prospects are confirmed and reminded. The branch coverage alert — highlighting branches with no demos scheduled in the current month — is a proactive governance tool that prevents any branch from falling behind in its admissions activity without explicit visibility to management. The teacher assignment matrix provides a structured view of which teacher is handling each branch × subject combination, enabling quick substitution if someone is unavailable.

Conversion analytics close the loop between demo investment and admissions outcomes. The post-demo conversion funnel chart shows, per branch, how many demo attendees submitted applications and how many ultimately enrolled. This data directly informs decisions about demo frequency, subject selection, and teacher assignment. The feedback summary section — NPS score, average ratings, and common tags — gives the coordinator actionable quality signals about which demos are working and which need improvement. The follow-up queue ensures no warm prospect is left uncontacted after a demo, maintaining momentum through the final conversion step.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Demo Class Coordinator | G3 | Full read + write + manage | Primary owner of this page |
| Group Admission Coordinator | G3 | Read-only (all sections) | Coordination awareness; no actions |
| Group Admissions Director | G3 | Read-only + override actions | Can override teacher assignments or branch scheduling |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Demo Class Coordinator
```

### 3.2 Page Header
- **Title:** `Demo Class Coordinator Dashboard`
- **Subtitle:** `Group Admissions · Admission Month: [Month, Year]`
- **Role Badge:** `Group Demo Class Coordinator`
- **Right-side controls:** `[+ Schedule Demo]` `[Bulk Send Reminders]` `[Export Attendance Report]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Branches with no demo this month | "[N] branch(es) have not scheduled a demo class this admission month." | Critical (red) |
| Demo in < 2 days with unconfirmed registrations | "Demo '[Subject] at [Branch]' on [Date] has [N] unconfirmed registrations." | Warning (amber) |
| Teacher not assigned for an upcoming demo | "[N] demo class(es) have no teacher assigned. Assign teachers immediately." | Critical (red) |
| Follow-ups overdue > 7 days | "[N] demo attendees have not been followed up in over 7 days." | Warning (amber) |
| Feedback score < 3.5 for last 3 demos at a branch | "Average feedback at [Branch] has dropped below 3.5 for 3 consecutive demos." | Warning (amber) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Demos Scheduled This Week | Count of demo classes in current 7-day window | `demo_class` WHERE date BETWEEN today AND today+7 | Blue (informational) | Scrolls to Section 5.1 |
| Total Attendees (Registered) | Total prospects registered for upcoming demos | `demo_registration` WHERE demo.status IN ('scheduled', 'confirmed') | Green if ≥ weekly target; amber 50–99%; red < 50% | Opens registration tracker |
| Conversion Rate (Demo→Application) | (Applications submitted / Demo attendees marked present) × 100 this month | `demo_attendance` + `admissions_application` | Green ≥ 30%; amber 15–29%; red < 15% | Opens conversion funnel |
| Avg Feedback Score (Month) | Mean of all feedback scores from demos this month | `demo_feedback` WHERE demo.month = current | Green ≥ 4.0; amber 3.0–3.9; red < 3.0 | Opens feedback summary view |
| Follow-up Sessions Pending | Prospects who attended demos but have not yet been followed up | `demo_attendance` WHERE followup_status = 'pending' | Red if > 20; amber 5–20; green < 5 | Scrolls to Section 5.7 |
| Branches Without Demo (Month) | Branches that have not hosted any demo in the current admission month | `demo_class` anti-join with `branch` | Red if > 3; amber 1–3; green = 0 | Scrolls to Section 5.5 |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Demo Class Schedule

**Display:** Sortable, filterable table. Upcoming demos first. Demos with unassigned teachers are highlighted red. Demos with < 24 hours to start and unconfirmed registrations are highlighted amber.

**Columns:** Date | Time | Branch | Subject / Stream Demo | Teacher Assigned | Registered Students | Confirmed | Status Badge | Action

**Status Badge Values:** Scheduled (blue) | Confirmed (green) | In Progress (amber) | Completed (muted) | Cancelled (red)

**Actions per row:** `[View Details →]` opens demo-class-detail drawer.

**Filters:** Branch (multi-select), Date range, Subject / Stream, Status, Teacher Assigned (Yes / No)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="demo-schedule"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/schedule/"
     hx-trigger="load, change from:#schedule-filters"
     hx-target="#demo-schedule"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: classroom icon. "No demo classes scheduled. Use [+ Schedule Demo] to create your first demo."

---

### 5.2 Registration Tracker

**Display:** Sortable, searchable table. Each row is a prospect registered for an upcoming demo. Unconfirmed registrations are highlighted amber if demo is within 3 days.

**Columns:** Prospect Name | Parent Name | Phone | Preferred Branch | Demo Date | Demo Subject | Registration Status | Action

**Registration Status Badge Values:** Registered (blue) | Confirmed (green) | Attended (teal) | No-show (red) | Rescheduled (amber)

**Actions per row:** `[Confirm →]` updates status to Confirmed | `[Reschedule →]` opens reschedule flow in demo-class-detail drawer | `[Cancel]` with confirmation.

**Filters:** Branch, Demo Date, Status, Search (prospect name, phone)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="registration-tracker"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/registrations/"
     hx-trigger="load, change from:#reg-filters"
     hx-target="#registration-tracker"
     hx-swap="innerHTML">
```

**Empty State:** "No registrations found for the selected filters. Registrations will appear as prospects sign up for demos."

---

### 5.3 Post-Demo Conversion Funnel

**Display:** Chart.js 4.x grouped bar chart. X-axis = branches. For each branch, three bars: Attended Demo (blue), Submitted Application (amber), Enrolled (green). A line overlay can be toggled to show conversion % per branch. Filter chips above the chart for month/cycle.

**Fields shown below chart (summary row per branch):** Branch | Attended | Applied | Enrolled | Conversion %

**Filters:** Month / Cycle (dropdown), Subject / Stream, Date range

**HTMX Pattern:**
```html
<div id="conversion-funnel"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/conversion-funnel/"
     hx-trigger="load, change from:#funnel-filters"
     hx-target="#conversion-funnel"
     hx-swap="innerHTML">
```

**Empty State:** "No conversion data available for the selected period. Data appears after demo classes are completed and attendance is logged."

---

### 5.4 Demo Feedback Summary

**Display:** Top row of four stat cards (average rating, NPS score, total responses, top positive tag). Below: Table of recent individual feedback records with name, demo attended, score, comments, and `[View →]` link. Stat cards are colour-coded by threshold.

**Stat Cards:**
- Average Rating: Green ≥ 4.0; amber 3.0–3.9; red < 3.0
- NPS Score: Green ≥ 50; amber 0–49; red < 0
- Total Responses This Month: Blue (informational)
- Top Positive Tag: Informational badge (e.g., "Engaging Teacher", "Clear Explanation")

**Feedback Table Columns:** Prospect Name | Demo Date | Branch | Subject | Rating (stars) | NPS | Tags | Comments Preview | Action

**Actions per row:** `[View →]` opens feedback-detail drawer.

**Filters:** Branch, Subject, Rating range, Date range

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="feedback-summary"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/feedback/"
     hx-trigger="load, change from:#feedback-filters"
     hx-target="#feedback-summary"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: star icon. "No feedback received yet. Feedback will appear after demo classes are completed."

---

### 5.5 Branches with No Demo This Month

**Display:** Alert-style list. Each item is a branch that has not scheduled a demo class in the current admission month. Sorted by number of days remaining in the admission month (most urgent first).

**Fields per item:** Branch Name | Last Demo Date (or "Never") | Days Since Last Demo | Days Left in Month | Status Badge | Action

**Status Badge Values:** No Demo Scheduled (red) | Demo Pending Confirmation (amber)

**Actions per item:** `[Schedule Demo →]` opens demo scheduling form with branch pre-selected.

**HTMX Pattern:**
```html
<div id="branches-no-demo"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/branches-without-demo/"
     hx-trigger="load"
     hx-target="#branches-no-demo"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: checkmark shield. "All branches have at least one demo scheduled this month."

---

### 5.6 Teacher Assignment Matrix

**Display:** Matrix table. Rows = Branches, Columns = Subjects (Mathematics, Physics, Chemistry, Biology, English, General — configurable per group). Each cell shows the assigned teacher's name or "— Unassigned —". Unassigned cells are highlighted red. Cells with a recent substitution are highlighted amber with a note.

**Cell Content:** Teacher name | `[Change →]` link (Demo Coordinator only)

**Actions:** `[Change →]` per cell opens teacher assignment modal inline.

**Filters:** Branch (focus a single row), Subject (focus a single column), Unassigned Only toggle

**HTMX Pattern:**
```html
<div id="teacher-matrix"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/teacher-matrix/"
     hx-trigger="load"
     hx-target="#teacher-matrix"
     hx-swap="innerHTML">
```

**Empty State:** "Teacher assignment matrix cannot be displayed — no branches or subjects are configured."

---

### 5.7 Follow-up Queue

**Display:** Sortable, filterable table. Prospects who attended a demo but have not yet applied or been converted. Sorted by days since demo (most urgent first). Rows > 7 days highlighted amber; > 14 days highlighted red.

**Columns:** Prospect Name | Branch | Demo Date | Subject Attended | Days Since Demo | Preferred Stream | Phone | Follow-up Status | Action

**Follow-up Status Badge Values:** Pending (amber) | Attempted (blue) | Scheduled (teal) | Converted (green) | Lost (red)

**Actions per row:** `[Schedule Follow-up →]` opens follow-up-schedule drawer | `[Mark Converted ✓]` | `[Mark Lost]`

**Filters:** Branch, Days Since Demo (Any / 3+ / 7+ / 14+), Follow-up Status, Subject

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="followup-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/demo/followup-queue/"
     hx-trigger="load, change from:#followup-filters"
     hx-target="#followup-queue"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: phone checkmark. "No pending follow-ups. All demo attendees have been contacted or converted."

---

## 6. Drawers & Modals

### 6.1 Demo Class Detail Drawer
- **Width:** 640px
- **Trigger:** `[View Details →]` in Section 5.1
- **Tabs:**
  - **Overview:** Demo name, date/time, branch, subject/stream, venue/room, description, status
  - **Registrations:** Table of registered prospects — Name, phone, confirmation status, attendance (post-demo); `[Mark Attendance]` (post-demo); `[Add Walk-in]`
  - **Teacher:** Current teacher assignment, `[Change Teacher]` form (search teacher by name, subject); substitution history
  - **Feedback:** Post-demo feedback summary for this specific class — ratings, NPS, comments (available after demo date)
  - **Reschedule / Cancel:** Date/time picker for reschedule + reason field; `[Reschedule]` / `[Cancel Demo]` actions with confirmation
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/demo/{{ demo_id }}/"`

### 6.2 Registration Detail Drawer
- **Width:** 560px
- **Trigger:** Click on prospect name in Section 5.2 or `[Reschedule →]` action
- **Tabs:**
  - **Prospect Info:** Name, parent name, phone, email, preferred branch, preferred stream, source (how they heard about demo)
  - **Demo History:** All demos this prospect has registered for — date, subject, attended?, outcome
  - **Reschedule:** Available demo slots for selected branch, `[Confirm Reschedule]`
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/demo/registrations/{{ registration_id }}/"`

### 6.3 Feedback Detail Drawer
- **Width:** 480px
- **Trigger:** `[View →]` in Section 5.4 feedback table
- **Tabs:**
  - **Feedback Content:** Full feedback text, rating breakdown (per dimension if multi-dimension form), tags, NPS score, prospect contact info
  - **Demo Context:** The demo this feedback refers to — date, branch, subject, teacher
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/demo/feedback/{{ feedback_id }}/"`

### 6.4 Follow-up Schedule Drawer
- **Width:** 480px
- **Trigger:** `[Schedule Follow-up →]` in Section 5.7
- **Tabs:**
  - **Schedule:** Date/time picker for follow-up, channel (Call / WhatsApp / Email), assigned to (self or counsellor), notes, `[Save Follow-up]`
  - **History:** Previous contact attempts for this prospect after the demo
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/demo/followup/{{ prospect_id }}/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Demo class scheduled | "Demo class '[Subject] at [Branch]' scheduled for [Date]." | Success | 4s |
| Registration confirmed | "[Prospect Name] confirmed for demo on [Date]." | Success | 3s |
| Registration rescheduled | "[Prospect Name] rescheduled to [New Date] demo." | Success | 4s |
| Registration cancelled | "Registration for [Prospect Name] cancelled." | Info | 3s |
| Teacher assigned | "[Teacher Name] assigned to [Subject] demo at [Branch] on [Date]." | Success | 4s |
| Teacher changed | "Teacher for [Subject] at [Branch] changed to [New Teacher Name]." | Info | 4s |
| Attendance marked | "Attendance recorded for [Demo Name] — [N] present, [N] absent." | Success | 4s |
| Follow-up scheduled | "Follow-up with [Prospect Name] scheduled for [Date]." | Success | 3s |
| Prospect marked converted | "[Prospect Name] marked as converted. Admissions pipeline notified." | Success | 4s |
| Bulk reminders sent | "Reminders sent to [N] registered prospects." | Success | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No demos scheduled | Classroom icon | "No Demo Classes Scheduled" | "Schedule demo classes to begin attracting prospective students." | `[+ Schedule Demo]` |
| No registrations | Clipboard icon | "No Registrations Yet" | "Prospect registrations will appear here once demos are open for signup." | `[Share Registration Link]` |
| No conversion data | Chart icon | "No Conversion Data" | "Conversion data appears after demo classes are completed and attendance is logged." | — |
| No feedback received | Star icon | "No Feedback Yet" | "Feedback from prospects will appear here after demo classes are held." | — |
| All branches covered | Checkmark shield | "All Branches Active" | "Every branch has at least one demo scheduled this month." | — |
| No pending follow-ups | Phone checkmark | "Follow-up Queue Clear" | "All demo attendees have been followed up." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Demo schedule table load | Skeleton table rows (6 rows) |
| Registration tracker table load | Skeleton table rows (8 rows) |
| Conversion funnel chart load | Skeleton bar chart (branches × 3 bars) |
| Feedback stat cards + table load | Skeleton stat cards (4) + skeleton table rows (5) |
| Branches no-demo alert list load | Skeleton list items (3 items) |
| Teacher assignment matrix load | Skeleton grid table (branches × subjects) |
| Follow-up queue table load | Skeleton table rows (6 rows) |
| Drawer content load | Spinner overlay on drawer panel |
| Bulk reminder send | Spinner on `[Bulk Send Reminders]` button with count progress |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Demo Coordinator | Admission Coordinator | Admissions Director |
|---|---|---|---|
| KPI Summary Bar (all cards) | Visible | Visible | Visible |
| Demo Schedule (5.1) | Visible + [View Details] | Read only | Read only + override |
| `[+ Schedule Demo]` button | Visible | Hidden | Visible (override) |
| Registration Tracker (5.2) | Visible + [Confirm] [Reschedule] [Cancel] | Read only | Read only |
| `[Confirm →]` / `[Reschedule →]` / `[Cancel]` | Visible | Hidden | Visible (override) |
| Conversion Funnel chart (5.3) | Visible | Visible | Visible |
| Feedback Summary (5.4) | Visible | Visible | Visible |
| Branches No Demo list (5.5) | Visible + [Schedule Demo →] | Read only | Read only |
| Teacher Assignment Matrix (5.6) | Visible + [Change →] | Read only | Read only + override |
| `[Change →]` teacher button | Visible | Hidden | Visible (override) |
| Follow-up Queue (5.7) | Visible + [Schedule Follow-up] [Mark Converted] [Mark Lost] | Read only | Read only |
| `[Bulk Send Reminders]` button | Visible | Hidden | Hidden |
| `[Export Attendance Report]` button | Visible | Visible | Visible |
| Demo Detail Drawer — Mark Attendance | Visible | Hidden | Visible |
| Demo Detail Drawer — Reschedule/Cancel tab | Visible | Hidden | Visible (override) |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/demo/kpis/` | JWT G3+ | Fetch all 6 KPI card values |
| GET | `/api/v1/group/{group_id}/adm/demo/schedule/` | JWT G3+ | Demo class schedule (filtered) |
| POST | `/api/v1/group/{group_id}/adm/demo/` | JWT G3 | Create / schedule a new demo class |
| GET | `/api/v1/group/{group_id}/adm/demo/{demo_id}/` | JWT G3+ | Demo class detail for drawer |
| PATCH | `/api/v1/group/{group_id}/adm/demo/{demo_id}/` | JWT G3 | Update demo (reschedule, cancel, assign teacher) |
| POST | `/api/v1/group/{group_id}/adm/demo/{demo_id}/attendance/` | JWT G3 | Submit attendance for a completed demo |
| GET | `/api/v1/group/{group_id}/adm/demo/registrations/` | JWT G3+ | Prospects registered for demos (filtered) |
| GET | `/api/v1/group/{group_id}/adm/demo/registrations/{registration_id}/` | JWT G3+ | Registration detail for drawer |
| POST | `/api/v1/group/{group_id}/adm/demo/registrations/{registration_id}/confirm/` | JWT G3 | Confirm a prospect's registration |
| POST | `/api/v1/group/{group_id}/adm/demo/registrations/{registration_id}/reschedule/` | JWT G3 | Reschedule a registration to a different demo |
| POST | `/api/v1/group/{group_id}/adm/demo/registrations/{registration_id}/cancel/` | JWT G3 | Cancel a registration |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion-funnel/` | JWT G3+ | Post-demo conversion funnel data per branch |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/` | JWT G3+ | Demo feedback list (filtered) |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/{feedback_id}/` | JWT G3+ | Single feedback detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/demo/branches-without-demo/` | JWT G3+ | Branches with no demo this admission month |
| GET | `/api/v1/group/{group_id}/adm/demo/teacher-matrix/` | JWT G3+ | Teacher assignment matrix (branch × subject) |
| POST | `/api/v1/group/{group_id}/adm/demo/teacher-matrix/assign/` | JWT G3 | Assign or change teacher for a branch × subject slot |
| GET | `/api/v1/group/{group_id}/adm/demo/followup-queue/` | JWT G3+ | Pending follow-ups list |
| POST | `/api/v1/group/{group_id}/adm/demo/followup/{prospect_id}/schedule/` | JWT G3 | Schedule a follow-up for a prospect |
| POST | `/api/v1/group/{group_id}/adm/demo/followup/{prospect_id}/convert/` | JWT G3 | Mark prospect as converted |
| POST | `/api/v1/group/{group_id}/adm/demo/bulk-remind/` | JWT G3 | Dispatch reminders to all unconfirmed registrations |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/demo/kpis/` | `#kpi-bar` | `innerHTML` |
| Demo schedule filter change | `change from:#schedule-filters` | GET `/api/v1/group/{{ group_id }}/adm/demo/schedule/` | `#demo-schedule` | `innerHTML` |
| Open demo detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/demo/{{ demo_id }}/` | `#drawer-panel` | `innerHTML` |
| Registration tracker filter change | `change from:#reg-filters` | GET `/api/v1/group/{{ group_id }}/adm/demo/registrations/` | `#registration-tracker` | `innerHTML` |
| Confirm registration | `click from:#btn-confirm-{{ id }}` | POST `/api/v1/group/{{ group_id }}/adm/demo/registrations/{{ id }}/confirm/` | `#registration-tracker` | `innerHTML` |
| Cancel registration | `click from:#btn-cancel-{{ id }}` | POST `/api/v1/group/{{ group_id }}/adm/demo/registrations/{{ id }}/cancel/` | `#registration-tracker` | `innerHTML` |
| Open registration detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/demo/registrations/{{ id }}/` | `#drawer-panel` | `innerHTML` |
| Conversion funnel filter change | `change from:#funnel-filters` | GET `/api/v1/group/{{ group_id }}/adm/demo/conversion-funnel/` | `#conversion-funnel` | `innerHTML` |
| Feedback filter change | `change from:#feedback-filters` | GET `/api/v1/group/{{ group_id }}/adm/demo/feedback/` | `#feedback-summary` | `innerHTML` |
| Open feedback detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/demo/feedback/{{ id }}/` | `#drawer-panel` | `innerHTML` |
| Branches no-demo load | `load` | GET `/api/v1/group/{{ group_id }}/adm/demo/branches-without-demo/` | `#branches-no-demo` | `innerHTML` |
| Teacher matrix load | `load` | GET `/api/v1/group/{{ group_id }}/adm/demo/teacher-matrix/` | `#teacher-matrix` | `innerHTML` |
| Assign teacher (inline cell) | `click from:#btn-change-teacher` | POST `/api/v1/group/{{ group_id }}/adm/demo/teacher-matrix/assign/` | `#teacher-matrix` | `innerHTML` |
| Follow-up queue filter change | `change from:#followup-filters` | GET `/api/v1/group/{{ group_id }}/adm/demo/followup-queue/` | `#followup-queue` | `innerHTML` |
| Open follow-up schedule drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/demo/followup/{{ prospect_id }}/` | `#drawer-panel` | `innerHTML` |
| Save follow-up schedule | `click from:#btn-save-followup` | POST `/api/v1/group/{{ group_id }}/adm/demo/followup/{{ prospect_id }}/schedule/` | `#followup-queue` | `innerHTML` |
| Mark prospect converted | `click from:#btn-convert-{{ id }}` | POST `/api/v1/group/{{ group_id }}/adm/demo/followup/{{ id }}/convert/` | `#followup-queue` | `innerHTML` |
| Bulk send reminders | `click from:#btn-bulk-remind` | POST `/api/v1/group/{{ group_id }}/adm/demo/bulk-remind/` | `#bulk-remind-status` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
