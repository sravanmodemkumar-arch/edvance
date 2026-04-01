# 03 — Group Admission Counsellor Dashboard

- **URL:** `/group/adm/counsellor/`
- **Template:** `portal_base.html`
- **Priority:** P0
- **Role:** Group Admission Counsellor (Role 25, G3)

---

## 1. Purpose

The Group Admission Counsellor Dashboard is the personal workspace for every student-facing counsellor in the group admissions team. Large groups typically operate multiple counsellors simultaneously, and each counsellor sees only their own assigned sessions, enquiry queue, scholarship recommendations, and follow-up tasks — this scoped view ensures focus and eliminates noise from colleagues' workloads. The dashboard is designed for high-throughput daily use: everything a counsellor needs from the moment they log in until their last session of the day is surfaced on a single page.

The most prominent section is the day's counselling schedule, presented as a chronological timeline. Each session card displays the prospective student's name, whether a parent is attending, the student's preferred stream and branch, and the enquiry type (fresh enquiry, re-enquiry, scholarship applicant, demo follow-up). A direct `[Start Session →]` link keeps the counsellor just one click away from opening the full student profile. Sessions not started by their scheduled time are highlighted to prompt action.

Scholarship recommendation is embedded into the counsellor's workflow: when the counsellor identifies a student who qualifies for a merit, need-based, or government scholarship scheme, they submit a recommendation from within the session detail drawer. Recommendations are tracked in a dedicated table showing approval status from the Scholarship Manager. The conversion funnel chart gives counsellors personal performance visibility — seeing their own enquiry-to-enrollment conversion rate versus the previous month acts as a motivational feedback loop. Follow-up discipline is enforced through an alert-style list of students whose follow-up deadline is today, ensuring no warm lead is left uncontacted.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admission Counsellor | G3 | Full read + write — own assigned data only | Cannot see other counsellors' sessions or enquiries |
| Group Admission Coordinator | G3 | Read — all counsellors' data across all sections | Cannot create recommendations or log calls on behalf of counsellors |
| Group Admissions Director | G3 | Read — all counsellors' data across all sections | View only; no actions |

> **Enforcement:** All access control is enforced server-side in Django views using `@role_required` decorators and queryset-level filtering. Data is filtered by `assigned_counsellor = request.user` for counsellor role. No role checks are performed in client-side JavaScript. Users without the required role receive an HTTP 403 response.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Counsellor Dashboard
```

### 3.2 Page Header
- **Title:** `Counsellor Dashboard`
- **Subtitle:** `Group Admissions · [Counsellor Full Name] · [Date, Day]`
- **Role Badge:** `Group Admission Counsellor`
- **Right-side controls:** `[+ Add Enquiry]` `[My Session History]` `[Export My Report]`

### 3.3 Alert Banner
Displayed conditionally above the KPI bar. Triggers include:

| Condition | Banner Text | Severity |
|---|---|---|
| Follow-up calls overdue (past due date) | "[N] follow-up(s) are overdue. Please contact these students today." | Critical (red) |
| Session scheduled to start in < 10 min | "Your next session with [Student Name] starts in [X] minutes." | Warning (amber) |
| Scholarship recommendation pending > 7 days | "[N] scholarship recommendation(s) are pending review for over 7 days." | Info (blue) |
| No enquiries assigned | "No enquiries are currently assigned to you. Contact your Coordinator." | Info (blue) |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Today's Sessions Scheduled | Count of counselling sessions for today assigned to this counsellor | `counselling_session` WHERE date = today AND counsellor = me | Blue (informational) | Scrolls to Section 5.1 |
| Sessions Completed This Week | Count of sessions with outcome logged this week | `counselling_session` WHERE week = current AND status = 'completed' | Green if ≥ weekly target; amber if 60–99%; red if < 60% | Scrolls to Section 5.6 history |
| Conversions This Month | Enquiries handled by this counsellor where student enrolled this month | `counselling_session` → `enrollment` JOIN | Green if ≥ monthly target; amber if 50–99%; red if < 50% | Opens conversion detail modal |
| Scholarship Recommendations Pending | Recommendations submitted by this counsellor with status = 'pending' | `scholarship_recommendation` WHERE counsellor = me AND status = 'pending' | Amber if > 0; green = 0 | Scrolls to Section 5.3 |
| Follow-up Calls Due Today | Enquiries with follow_up_date = today assigned to this counsellor | `enquiry` WHERE follow_up_date = today AND counsellor = me | Red if > 5; amber 1–5; green = 0 | Scrolls to Section 5.5 |
| Average Session Rating | Mean of student feedback scores for sessions this month | `session_feedback` WHERE counsellor = me AND month = current | Green ≥ 4.0; amber 3.0–3.9; red < 3.0 | Opens feedback summary view |

**HTMX Refresh Pattern:**
```html
<div id="kpi-bar"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/kpis/"
     hx-trigger="load, every 5m"
     hx-target="#kpi-bar"
     hx-swap="innerHTML">
```

---

## 5. Sections

### 5.1 Today's Counselling Schedule

**Display:** Vertical timeline list for the current day. Each entry is a session card. Sessions are sorted chronologically. Sessions not started past their scheduled time are highlighted amber. Sessions in progress are highlighted with a green left border.

**Fields per session card:** Time slot | Student Name | Parent Attending? (Yes/No badge) | Enquiry Type (Fresh / Re-enquiry / Scholarship / Demo Follow-up) | Preferred Stream | Preferred Branch | Status (Upcoming / In Progress / Completed / No-show) | Action

**Actions per card:** `[Start Session →]` opens session-detail drawer | `[Mark No-show]`

**Filters:** Status (All / Upcoming / Completed / No-show)

**HTMX Pattern:**
```html
<div id="todays-schedule"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/sessions/today/"
     hx-trigger="load"
     hx-target="#todays-schedule"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: calendar icon. "No sessions scheduled for today. New sessions will appear here once assigned."

---

### 5.2 Active Enquiry Queue

**Display:** Sortable, searchable table. Rows with `follow_up_due` = today are highlighted. Rows where last contact > 7 days are flagged with a warning icon.

**Columns:** Student Name | Class | Stream Interest | Contact Number | Source | Last Contact Date | Follow-up Due | Status | Action

**Actions per row:** `[Call]` (tel: link) | `[WhatsApp]` (wa.me link) | `[Log Contact →]` opens follow-up-log drawer

**Filters:** Stream, Source (Walk-in / Online / Demo / Alumni / Referral), Follow-up Due (Today / Overdue / Upcoming), Status (New / In Progress / Converted / Lost)

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="enquiry-queue"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/"
     hx-trigger="load, change from:#enquiry-filters"
     hx-target="#enquiry-queue"
     hx-swap="innerHTML">
```

**Empty State:** "No active enquiries assigned to you. New enquiries will appear here once assigned by the Coordinator."

---

### 5.3 My Scholarship Recommendations

**Display:** Sortable table showing all scholarship recommendations this counsellor has submitted. Status badge colour-coded.

**Columns:** Student Name | Recommended Scheme | Score / Basis (Marks % / Income / RTE) | Submitted On | Status | Action

**Status Badge Rules:** Pending = amber; Approved = green; Rejected = red; Under Review = blue

**Actions per row:** `[View →]` opens session-detail drawer pre-scrolled to recommendation section.

**Filters:** Status (All / Pending / Approved / Rejected), Scheme type, Date range

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="scholarship-recs"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/scholarship-recommendations/"
     hx-trigger="load"
     hx-target="#scholarship-recs"
     hx-swap="innerHTML">
```

**Empty State:** "You have not submitted any scholarship recommendations yet. Recommend eligible students from within a session."

---

### 5.4 Conversion Funnel (Personal)

**Display:** Chart.js 4.x grouped bar chart. Two groups: current month and last month. Each group has three bars: Enquiries, Sessions Held, Enrolled. Displayed as a compact chart, not full-width.

**Fields shown below chart:** This Month: Enquiries [N], Sessions [N], Enrolled [N], Conversion [X%] | Last Month: same fields

**Filters:** None (always personal, always current vs last month)

**HTMX Pattern:**
```html
<div id="conversion-funnel"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/conversion-funnel/"
     hx-trigger="load"
     hx-target="#conversion-funnel"
     hx-swap="innerHTML">
```

**Empty State:** "No conversion data available for this month yet."

---

### 5.5 Follow-up Due Today

**Display:** Alert-style ordered list. Each item is a student with a follow-up due today or overdue. Overdue items (past_due_date) shown first in red; today's items in amber. Quick action buttons inline.

**Fields per item:** Student Name | Phone | Last Contact Date | Preferred Branch | Days Since Last Contact | Follow-up Type (Call / WhatsApp / Email) | Action

**Actions per item:** `[Log Call]` opens follow-up-log drawer | `[Call]` (tel: link) | `[WhatsApp]` (wa.me link) | `[Mark Converted ✓]`

**HTMX Pattern:**
```html
<div id="followup-due"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/followups/due-today/"
     hx-trigger="load"
     hx-target="#followup-due"
     hx-swap="innerHTML">
```

**Empty State:** Illustration: phone with checkmark. "No follow-ups due today. Great work staying on top of your contacts!"

---

### 5.6 Session History

**Display:** Paginated table. All past sessions for this counsellor, most recent first.

**Columns:** Student Name | Date | Duration (mins) | Outcome (Enrolled / Applied / Thinking / Rejected / No-show) | Notes Preview | Action

**Actions per row:** `[View →]` opens session-detail drawer in read-only mode.

**Filters:** Date range, Outcome, Stream

**Pagination:** Server-side, 20 rows default.

**HTMX Pattern:**
```html
<div id="session-history"
     hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/sessions/history/"
     hx-trigger="load, change from:#history-filters"
     hx-target="#session-history"
     hx-swap="innerHTML">
```

**Empty State:** "No completed sessions yet. Your session history will appear here after your first counselling session."

---

## 6. Drawers & Modals

### 6.1 Session Detail Drawer
- **Width:** 640px
- **Trigger:** `[Start Session →]` or `[View →]` in Section 5.1 / 5.6
- **Tabs:**
  - **Student Profile:** Student + parent details, class, contact info, enquiry source, previous enquiry history
  - **Enquiry History:** Chronological log of all contacts with this student — date, type, outcome, notes
  - **Preferences:** Preferred stream, branch, subjects of interest, career goal (free text)
  - **Session Notes:** Rich text area for this session's notes. `[Save Notes]` via HTMX POST. Notes auto-save every 2 minutes.
  - **Scholarship Recommendation:** Form — Scheme selector (Merit / Need-based / RTE / Government), Basis field, Score/Evidence, Remarks, `[Submit Recommendation]`. Hidden if recommendation already submitted for this student.
  - **Outcome:** Session outcome selector (Enrolled / Applied / Thinking / Rejected / No-show) + `[Close Session]`
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/sessions/{{ session_id }}/"`

### 6.2 Follow-up Log Drawer
- **Width:** 480px
- **Trigger:** `[Log Call]` in Section 5.5 or `[Log Contact →]` in Section 5.2
- **Tabs:**
  - **Log Contact:** Contact type (Call / WhatsApp / Email / In-person), Outcome (Interested / Not interested / Call back / No answer), Notes, Next follow-up date, `[Save Log]`
  - **Contact History:** Previous contact logs for this student — date, type, outcome, notes
- **HTMX Endpoint:** `hx-get="/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/{{ enquiry_id }}/followup-log/"`

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Session started | "Session with [Student Name] started." | Info | 3s |
| Session notes saved | "Session notes saved." | Success | 3s |
| Session closed with outcome | "Session closed. Outcome: [Outcome] for [Student Name]." | Success | 4s |
| Scholarship recommendation submitted | "Scholarship recommendation submitted for [Student Name]." | Success | 4s |
| Follow-up log saved | "Follow-up logged for [Student Name]. Next follow-up: [Date]." | Success | 4s |
| Student marked as no-show | "[Student Name] marked as no-show for [Time] session." | Info | 4s |
| Contact reminder sent | "Contact entry saved. Follow-up scheduled for [Date]." | Success | 3s |
| Student marked converted | "[Student Name] marked as converted. Application process will begin." | Success | 5s |
| Recommendation update failed | "Failed to submit recommendation. Please verify all fields." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No sessions today | Calendar icon | "No Sessions Today" | "You have no counselling sessions scheduled for today." | `[View My Schedule]` |
| No enquiries assigned | Inbox icon | "No Active Enquiries" | "No enquiries are currently assigned to you." | `[Contact Coordinator]` |
| No scholarship recommendations | Star icon | "No Recommendations Yet" | "Recommend eligible students for scholarships from within a session." | `[View Sessions]` |
| No follow-ups due | Phone checkmark | "All Follow-ups Complete" | "You have no follow-up calls due today. Well done!" | — |
| No session history | Clock icon | "No Session History" | "Your completed session history will appear here." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| KPI bar initial load / auto-refresh | Skeleton shimmer cards (6 cards) |
| Today's schedule load | Skeleton session cards (3 cards) |
| Enquiry queue load | Skeleton table rows (6 rows) |
| Scholarship recommendations load | Skeleton table rows (4 rows) |
| Conversion funnel chart load | Skeleton bar chart (2 grouped bars) |
| Follow-up due list load | Skeleton list items (4 items) |
| Session history table load | Skeleton table rows (6 rows) |
| Session detail drawer open | Spinner overlay on drawer panel |
| Follow-up log drawer open | Spinner overlay on drawer panel |
| Notes auto-save | Inline spinner next to "Save Notes" label |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Admission Counsellor (own data) | Admission Coordinator (all data) | Admissions Director (all data) |
|---|---|---|---|
| KPI Summary Bar | Visible (own metrics) | Visible (group aggregates) | Visible (group aggregates) |
| Today's Schedule (5.1) | Own sessions | All counsellors' sessions | All counsellors' sessions |
| `[Start Session →]` button | Visible | Hidden | Hidden |
| `[Mark No-show]` button | Visible | Hidden | Hidden |
| Active Enquiry Queue (5.2) | Own enquiries | All enquiries | All enquiries read only |
| `[Call]` / `[WhatsApp]` links | Visible | Visible | Visible |
| `[Log Contact →]` | Visible | Hidden | Hidden |
| Scholarship Recommendations (5.3) | Own recommendations | All recommendations read only | All recommendations read only |
| Conversion Funnel chart (5.4) | Own data | Own data (not aggregated here) | Own data (not aggregated here) |
| Follow-up Due Today (5.5) | Own follow-ups | Read only | Read only |
| `[Log Call]` / `[Mark Converted]` | Visible | Hidden | Hidden |
| Session History (5.6) | Own history | All counsellors read only | All counsellors read only |
| `[+ Add Enquiry]` button | Visible | Hidden | Hidden |
| `[Export My Report]` button | Visible | Visible | Visible |
| Session Detail Drawer — Scholarship tab | Visible (submit form) | Read only | Read only |
| Session Detail Drawer — Outcome tab | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/counsellor/kpis/` | JWT G3+ | Fetch all 6 KPI card values (scoped to counsellor) |
| GET | `/api/v1/group/{group_id}/adm/counsellor/sessions/today/` | JWT G3+ | Today's sessions for this counsellor |
| POST | `/api/v1/group/{group_id}/adm/counsellor/sessions/{session_id}/start/` | JWT G3 | Mark session as started |
| POST | `/api/v1/group/{group_id}/adm/counsellor/sessions/{session_id}/no-show/` | JWT G3 | Mark session as no-show |
| POST | `/api/v1/group/{group_id}/adm/counsellor/sessions/{session_id}/close/` | JWT G3 | Close session with outcome |
| GET | `/api/v1/group/{group_id}/adm/counsellor/sessions/{session_id}/` | JWT G3+ | Session detail (profile, history, notes) |
| POST | `/api/v1/group/{group_id}/adm/counsellor/sessions/{session_id}/notes/` | JWT G3 | Save session notes |
| GET | `/api/v1/group/{group_id}/adm/counsellor/enquiries/` | JWT G3+ | Active enquiry queue for this counsellor |
| POST | `/api/v1/group/{group_id}/adm/counsellor/enquiries/{enquiry_id}/mark-converted/` | JWT G3 | Mark enquiry as converted |
| GET | `/api/v1/group/{group_id}/adm/counsellor/scholarship-recommendations/` | JWT G3+ | Scholarship recommendations by this counsellor |
| POST | `/api/v1/group/{group_id}/adm/counsellor/scholarship-recommendations/` | JWT G3 | Submit new scholarship recommendation |
| GET | `/api/v1/group/{group_id}/adm/counsellor/conversion-funnel/` | JWT G3+ | Personal conversion funnel data |
| GET | `/api/v1/group/{group_id}/adm/counsellor/followups/due-today/` | JWT G3+ | Follow-up items due today |
| GET | `/api/v1/group/{group_id}/adm/counsellor/enquiries/{enquiry_id}/followup-log/` | JWT G3+ | Contact log for a specific enquiry |
| POST | `/api/v1/group/{group_id}/adm/counsellor/enquiries/{enquiry_id}/followup-log/` | JWT G3 | Log a new contact entry |
| GET | `/api/v1/group/{group_id}/adm/counsellor/sessions/history/` | JWT G3+ | Paginated past sessions |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/kpis/` | `#kpi-bar` | `innerHTML` |
| Today's schedule load | `load` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/today/` | `#todays-schedule` | `innerHTML` |
| Open session detail drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/{{ session_id }}/` | `#drawer-panel` | `innerHTML` |
| Mark no-show | `click from:#btn-no-show` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/{{ session_id }}/no-show/` | `#todays-schedule` | `innerHTML` |
| Save session notes | `click from:#btn-save-notes` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/{{ session_id }}/notes/` | `#notes-status` | `innerHTML` |
| Submit scholarship recommendation | `click from:#btn-submit-rec` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/scholarship-recommendations/` | `#scholarship-recs` | `innerHTML` |
| Enquiry queue filter change | `change from:#enquiry-filters` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/` | `#enquiry-queue` | `innerHTML` |
| Open follow-up log drawer | `click` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/{{ enquiry_id }}/followup-log/` | `#drawer-panel` | `innerHTML` |
| Save follow-up log | `click from:#btn-save-log` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/{{ enquiry_id }}/followup-log/` | `#followup-due` | `innerHTML` |
| Mark enquiry converted | `click from:#btn-mark-converted` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/enquiries/{{ enquiry_id }}/mark-converted/` | `#enquiry-queue` | `innerHTML` |
| Session history filter change | `change from:#history-filters` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/history/` | `#session-history` | `innerHTML` |
| Follow-up due list load | `load` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/followups/due-today/` | `#followup-due` | `innerHTML` |
| Conversion funnel load | `load` | GET `/api/v1/group/{{ group_id }}/adm/counsellor/conversion-funnel/` | `#conversion-funnel` | `innerHTML` |
| Close session with outcome | `click from:#btn-close-session` | POST `/api/v1/group/{{ group_id }}/adm/counsellor/sessions/{{ session_id }}/close/` | `#todays-schedule` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
