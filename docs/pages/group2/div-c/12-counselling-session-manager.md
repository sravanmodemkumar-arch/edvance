# Page 12 — Counselling Session Manager

- **URL:** `/group/adm/counselling/`
- **Template:** `portal_base.html`
- **Theme:** Light

---

## 1. Purpose

The Counselling Session Manager coordinates the human heart of the admissions process: one-on-one and group sessions between prospective students, their parents, and the group's counsellors. These sessions are where branch preferences are understood, financial concerns are addressed, scholarship opportunities are flagged, and the family's trust in the institution is built or lost. A well-managed counselling operation is the single largest driver of enquiry-to-enrolment conversion in competitive educational groups.

For a group operating across 50 branches, counselling sessions run simultaneously across cities every working day. A Counsellor at Branch A and another at Branch B may both have sessions scheduled at the same time for students with similar profiles. The Coordinator needs group-level visibility to understand whether the counselling pipeline is keeping pace with enquiry volume, whether individual counsellors are overloaded, and whether sessions are resulting in applications. Without this centralised view, coordination happens over phone calls and informal messages, leading to missed sessions, no-shows that are not followed up, and scholarship recommendations that are never acted on.

The Scholarship Recommendation Queue (Section 5.3) is a critical integration point: when a counsellor identifies a student who qualifies for a scholarship scheme, they record the recommendation here, which then flows to the Group Scholarship Manager for review. The Session Outcome Summary (Section 5.4) provides per-counsellor conversion analytics that feed into professional development and performance reviews managed by the Group Academic Leadership team. Sessions resulting in no-shows are not simply discarded — they populate a dedicated follow-up queue (Section 5.5) so every missed opportunity is actively pursued.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Read all sessions + override reschedule/cancel | Cannot directly modify session notes unless overriding |
| Group Admission Coordinator (Role 24) | G3 | Full access — all sessions, all branches | Create, edit, reschedule, cancel, assign |
| Group Admission Counsellor (Role 25) | G3 | Own sessions full CRUD; other counsellors' sessions read-only | Can add session notes and scholarship recommendations for own sessions only |
| Group Scholarship Manager (Role 27) | G3 | Read only — scholarship recommendation queue | Sees only Section 5.3 and the scholarship tab in session-detail drawer |
| Group Demo Class Coordinator (Role 29) | G3 | Read only — demo-referral sessions | Sees sessions where `source = 'demo_class'` |

> **Enforcement:** Counsellor querysets are filtered: `CounsellingSession.objects.filter(counsellor=request.user)` for owned sessions; other sessions are read-only via separate serializer fields. `[Edit]`, `[Cancel]`, `[Add Note]` controls are rendered only when `session.counsellor == request.user or request.user.role in ['coordinator','director']`.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal → Admissions → Counselling Sessions
```

### 3.2 Page Header
- **Title:** Counselling Sessions
- **Subtitle:** Manage and track all counselling sessions — `{current_cycle_name}`
- **Right-side actions:** `[+ Schedule Session]` (Coordinator / Counsellor) · `[Export →]` (Coordinator / Director) · `[Refresh ↺]`

### 3.3 Alert Banner

| Trigger | Message |
|---|---|
| Sessions today with no outcome recorded by 6 PM | "{N} session(s) completed today have no outcome recorded. Please update." |
| No-show sessions with no follow-up scheduled | "{N} no-show session(s) have no follow-up action taken. Check no-show queue." |
| Scholarship recommendations pending Scholarship Manager review > 5 days | "{N} scholarship recommendation(s) have been pending review for over 5 days." |
| Pending session feedback forms > 10 | "{N} completed sessions are missing feedback forms." |
| Counsellor capacity alert (>10 sessions in one day) | "{Counsellor name} has {N} sessions scheduled today — review capacity." |

---

## 4. KPI Summary Bar

> Auto-refreshes every 5 minutes via HTMX: `hx-get="/api/v1/group/{group_id}/adm/counselling/kpis/" hx-trigger="every 5m" hx-target="#counselling-kpi-bar" hx-swap="innerHTML"`

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Sessions Today (Group-wide) | Sessions with `date = today` | `CounsellingSession.objects.filter(date=today)` | Neutral (blue) | Filters session table to today |
| Sessions This Week | Sessions with `date__week = current_week` | Weekly filter | Neutral (indigo) | Filters session table to this week |
| Avg Session Duration (min) | Mean of `duration_minutes` for completed sessions this month | `Avg('duration_minutes')` | Green ≤ 45; amber 46–75; red > 75 | Opens session outcome summary (5.4) |
| Conversion % | `(Sessions resulting in application / Total completed sessions) * 100` | Computed | Green ≥ 40%; amber 20–39%; red < 20% | Opens session outcome summary |
| Scholarship Recommendations (this month) | Count of `ScholarshipRecommendation.created_at__month = current_month` | Model count | Neutral (blue) | Opens scholarship recommendation queue (5.3) |
| Pending Feedback Forms | Sessions completed without feedback form submission | Computed | Amber if > 0; green if 0 | Filters session table to `feedback_submitted=False` |

---

## 5. Sections

### 5.1 Session Calendar View

**Display:** Week-view grid. Rows represent counsellors (or branches, switchable via a toggle). Columns represent days (Mon–Sat). Each scheduled session appears as a coloured event block showing: student name, session type badge, and time. Clicking an event block opens the session-detail drawer. Clicking an empty slot opens the new-session-form drawer pre-filled with that date/time/counsellor. Colour coding: Individual (blue), Group (green), Online (indigo), No-show (red), Completed (grey).

**Navigation:** Previous/Next week arrows. `[Today]` button. Branch filter dropdown (Coordinator/Director).

**HTMX Pattern:** Week navigation: `hx-get="/api/v1/group/{group_id}/adm/counselling/calendar/?week={week_start}"` `hx-target="#session-calendar"` `hx-swap="innerHTML"` `hx-trigger="click"`. Event block click: `hx-get="/api/v1/group/{group_id}/adm/counselling/{session_id}/detail/"` `hx-target="#session-detail-drawer"` `hx-swap="innerHTML"`.

**Empty State:** "No sessions scheduled for this week. Use + Schedule Session to add."

---

### 5.2 Session Table

**Display:** Sortable, server-side paginated table. 20 rows per page. Complements the calendar — shows the same data in tabular form. Sticky header.

**Columns:**

| Column | Notes |
|---|---|
| Session ID | Clickable — opens session-detail drawer |
| Date & Time | `DD MMM YYYY HH:MM` |
| Student Name | Clickable — opens student detail (enquiry or application) |
| Parent Attending | Yes / No badge |
| Branch | Branch name |
| Counsellor | Counsellor name |
| Type | Badge: Individual / Group / Online |
| Stream | Stream of interest |
| Status | Badge: Scheduled (blue) / Completed (green) / No-show (red) / Rescheduled (amber) |
| Outcome | Converted / Needs Follow-up / Scholarship Recommended / Lost / Pending |
| [View →] | Opens session-detail drawer |

**Filters:** Date range, Counsellor (Coordinator/Director only), Branch, Status, Outcome

**HTMX Pattern:** Filter changes: `hx-get="/api/v1/group/{group_id}/adm/counselling/?{filters}"` `hx-target="#session-table-body"` `hx-swap="innerHTML"` `hx-trigger="change"`. Pagination: `hx-target="#session-table-wrapper"`.

**Empty State:** Illustration of empty calendar. "No sessions found for the selected filters."

---

### 5.3 Scholarship Recommendation Queue

**Display:** Dedicated table showing sessions where the counsellor has flagged a scholarship recommendation. Visible in full to Coordinator, Director, and Scholarship Manager.

| Column | Notes |
|---|---|
| Student Name | Clickable — opens application/enquiry detail |
| Branch | Branch name |
| Scholarship Scheme | Scheme name as recommended |
| Session Date | Date recommendation was made |
| Recommended By | Counsellor name |
| Review Status | Pending Review (amber) / Approved (green) / Declined (red) / Under Discussion (blue) |
| [View Details →] | Opens scholarship recommendation tab in session-detail drawer |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/counselling/scholarship-queue/"` `hx-trigger="load, every 5m"` `hx-target="#scholarship-queue-table"` `hx-swap="innerHTML"`

**Empty State:** "No scholarship recommendations pending review."

---

### 5.4 Session Outcome Summary

**Display:** Grouped bar chart (Chart.js 4.x). X-axis: Counsellors. Three bars per counsellor: Sessions Completed (blue), Converted to Application (green), No-show Rate % (red). Branch filter dropdown. Date range filter. Hover tooltip shows exact values.

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/counselling/outcome-summary/?{filters}"` `hx-trigger="load"` `hx-target="#outcome-chart-data"` `hx-swap="innerHTML"`; filter change: `hx-trigger="change"` on dropdowns.

**Empty State:** "No session outcome data available for the selected period."

---

### 5.5 No-show Follow-up Queue

**Display:** List panel of students who had a scheduled session and marked as No-show, where no reschedule or follow-up action has been taken yet. Sorted by session date (oldest first).

| Column | Notes |
|---|---|
| Student Name | Name |
| Session Date | Date of missed session |
| Counsellor | Assigned counsellor |
| Branch | Branch |
| Days Since No-show | Integer; red if > 3 |
| Actions | `[Reschedule →]` opens reschedule-modal · `[Mark Lost →]` closes the lead |

**HTMX Pattern:** `hx-get="/api/v1/group/{group_id}/adm/counselling/?status=no_show&follow_up_pending=true"` `hx-trigger="load, every 5m"` `hx-target="#noshow-followup-queue"` `hx-swap="innerHTML"`

**Empty State:** "No no-show follow-ups pending. All missed sessions have been actioned."

---

## 6. Drawers & Modals

### 6.1 Session Detail Drawer
- **Width:** 640px (right-side slide-in)
- **Trigger:** Click Session ID / event block in calendar / `[View →]` in table
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/counselling/{session_id}/detail/`

**Tabs:**

| Tab | Content |
|---|---|
| Student Profile | Name, class, stream interest, branch preference, contact info, guardian details, source, enquiry ID link |
| Session Notes | Structured session notes: discussion topics, concerns raised, preferences, counsellor's narrative notes; timestamp of each note entry |
| Scholarship Recommendation | Toggle: Scholarship Recommended (yes/no); if yes: scheme selector, basis for recommendation, supporting notes — visible to Scholarship Manager |
| Follow-up Action | Outcome dropdown (Converted/Needs Follow-up/Lost/Scholarship Referred); follow-up date picker; action note; `[Schedule Next Session →]` |
| Feedback | Post-session feedback form: student/parent satisfaction rating (1–5), topics covered checklist, counsellor self-assessment, suggestions |

---

### 6.2 New Session Form Drawer
- **Width:** 560px
- **Trigger:** `[+ Schedule Session]` button or click empty calendar slot
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/counselling/new/`

**Fields:** Student (search-as-you-type from leads/applications), Branch, Counsellor, Date, Time, Duration (estimated minutes), Session Type (Individual/Group/Online), Parent attending (toggle), Pre-session notes, Send confirmation to student (toggle).

---

### 6.3 Reschedule Modal
- **Width:** 400px (centred modal)
- **Trigger:** `[Reschedule →]` in no-show queue or session detail
- **HTMX Endpoint:** `GET /api/v1/group/{group_id}/adm/counselling/{session_id}/reschedule/`

**Fields:** New date picker, New time picker, Reason for reschedule (dropdown), Notify student (toggle), Note to student (optional textarea).

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Session scheduled | "Session scheduled for {Student name} on {date} with {Counsellor}." | Success | 4s |
| Session notes saved | "Session notes saved for {Student name}." | Success | 3s |
| Session outcome recorded | "Outcome recorded: {Outcome} for {Student name}'s session." | Success | 4s |
| Session rescheduled | "Session rescheduled to {new date}. {Student name} notified." | Success | 4s |
| Scholarship recommendation submitted | "Scholarship recommendation for {Student name} sent to Scholarship Manager." | Success | 5s |
| Session cancelled | "Session cancelled for {Student name}. Counsellor notified." | Warning | 4s |
| Feedback form submitted | "Feedback recorded for session {Session ID}." | Success | 3s |
| No-show marked | "{Student name}'s session marked as No-show. Added to follow-up queue." | Warning | 4s |
| Session save failed | "Could not save session — {reason}. Please try again." | Error | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No sessions scheduled | Empty calendar graphic | "No Sessions Scheduled" | "No counselling sessions have been scheduled for the selected period." | `[+ Schedule Session]` |
| No sessions matching filters | Search-miss graphic | "No Matching Sessions" | "No sessions match the selected filters." | `[Clear Filters]` |
| No scholarship recommendations | Star graphic | "No Recommendations" | "No scholarship recommendations have been made this cycle." | — |
| No no-show follow-ups pending | Checkmark graphic | "No Pending Follow-ups" | "All no-show sessions have been rescheduled or closed." | — |
| Counsellor — no sessions | Person graphic | "No Sessions Assigned" | "Sessions will appear here once scheduled by the Coordinator." | — |
| No outcome data for chart | Chart (empty) | "No Outcome Data" | "Session outcome data will appear once sessions are completed and outcomes recorded." | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Full-page skeleton (calendar + table + KPI bar shimmer) |
| KPI bar auto-refresh | Inline spinner on each KPI card |
| Calendar week navigation | Calendar area skeleton (grid shimmer) |
| Session table filter/sort change | Table body skeleton (5-row shimmer) |
| Pagination click | Table body skeleton |
| Scholarship queue load/refresh | Panel skeleton |
| No-show queue load/refresh | Panel skeleton |
| Outcome chart load | Chart area spinner |
| Session detail drawer open | Drawer content skeleton |
| Drawer tab switch | Tab content spinner |
| New session form open | Form skeleton |
| Reschedule modal open | Modal skeleton |
| Scholarship recommendation submit | Button spinner |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions are made server-side in the Django template. No client-side JS role checks.

| Element | Dir (23) | Coord (24) | Counsellor (25) | Scholarship Mgr (27) | Demo Coord (29) |
|---|---|---|---|---|---|
| [+ Schedule Session] button | Hidden | Visible | Visible | Hidden | Hidden |
| [Export →] button | Visible | Visible | Hidden | Hidden | Hidden |
| Counsellor filter dropdown | Visible | Visible | Hidden | Hidden | Hidden |
| Session Calendar — all counsellors | Visible | Visible | Own sessions only | Hidden | Hidden |
| Session Table — all branches | Visible | Visible | Own sessions (full) + others (read) | Hidden | Demo-sourced only |
| Scholarship Recommendation Queue | Visible | Visible | Visible (own recs) | Visible | Hidden |
| [Scholarship Recommendation] drawer tab | Visible | Visible | Visible (own sessions) | Visible (read) | Hidden |
| Session Outcome Summary chart | Visible | Visible | Own column only | Hidden | Hidden |
| No-show Follow-up Queue | Visible | Visible | Own no-shows | Hidden | Hidden |
| [Cancel] session control | Visible | Visible | Own sessions only | Hidden | Hidden |
| [Add Note] in session detail | Visible | Visible | Own sessions only | Hidden | Hidden |
| Feedback tab in drawer | Visible | Visible | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/counselling/` | JWT G3+ | List sessions with filters, sort, pagination |
| POST | `/api/v1/group/{group_id}/adm/counselling/` | JWT G3 | Create new session |
| GET | `/api/v1/group/{group_id}/adm/counselling/kpis/` | JWT G3+ | KPI bar data |
| GET | `/api/v1/group/{group_id}/adm/counselling/calendar/` | JWT G3+ | Calendar view data for a given week |
| GET | `/api/v1/group/{group_id}/adm/counselling/scholarship-queue/` | JWT G3+ | Scholarship recommendation queue |
| GET | `/api/v1/group/{group_id}/adm/counselling/outcome-summary/` | JWT G3+ | Per-counsellor outcome stats for chart |
| GET | `/api/v1/group/{group_id}/adm/counselling/{session_id}/detail/` | JWT G3+ | Full session detail (profile, notes, tabs) |
| PATCH | `/api/v1/group/{group_id}/adm/counselling/{session_id}/` | JWT G3 | Update session (notes, outcome, status) |
| POST | `/api/v1/group/{group_id}/adm/counselling/{session_id}/reschedule/` | JWT G3 | Reschedule session |
| POST | `/api/v1/group/{group_id}/adm/counselling/{session_id}/scholarship-recommend/` | JWT G3 | Submit scholarship recommendation |
| POST | `/api/v1/group/{group_id}/adm/counselling/{session_id}/feedback/` | JWT G3 | Submit post-session feedback |
| GET | `/api/v1/group/{group_id}/adm/counselling/new/` | JWT G3 | New session form fragment |
| GET | `/api/v1/group/{group_id}/adm/counselling/export/` | JWT G3+ | Export sessions as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `every 5m` | GET `/api/v1/group/{group_id}/adm/counselling/kpis/` | `#counselling-kpi-bar` | `innerHTML` |
| Calendar week navigation (prev/next) | `click` | GET `/api/v1/group/{group_id}/adm/counselling/calendar/?week={week_start}` | `#session-calendar` | `innerHTML` |
| Calendar event block click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/{session_id}/detail/` | `#session-detail-drawer` | `innerHTML` |
| Calendar empty slot click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/new/?date={date}&time={time}&counsellor={id}` | `#new-session-drawer` | `innerHTML` |
| Session table filter change | `change` | GET `/api/v1/group/{group_id}/adm/counselling/?{filters}` | `#session-table-body` | `innerHTML` |
| Session table pagination click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/?page={n}&{filters}` | `#session-table-wrapper` | `innerHTML` |
| Session table sort click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/?sort={col}&order={dir}` | `#session-table-body` | `innerHTML` |
| [View →] row click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/{session_id}/detail/` | `#session-detail-drawer` | `innerHTML` |
| Drawer tab switch | `click` | GET `/api/v1/group/{group_id}/adm/counselling/{session_id}/detail/?tab={tab}` | `#drawer-tab-content` | `innerHTML` |
| Scholarship queue load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/counselling/scholarship-queue/` | `#scholarship-queue-table` | `innerHTML` |
| No-show queue load/refresh | `load, every 5m` | GET `/api/v1/group/{group_id}/adm/counselling/?status=no_show&follow_up_pending=true` | `#noshow-followup-queue` | `innerHTML` |
| Outcome summary chart load | `load` | GET `/api/v1/group/{group_id}/adm/counselling/outcome-summary/` | `#outcome-chart-data` | `innerHTML` |
| Outcome filter change | `change` | GET `/api/v1/group/{group_id}/adm/counselling/outcome-summary/?{filters}` | `#outcome-chart-data` | `innerHTML` |
| [+ Schedule Session] button click | `click` | GET `/api/v1/group/{group_id}/adm/counselling/new/` | `#new-session-drawer` | `innerHTML` |
| New session form submit | `submit` | POST `/api/v1/group/{group_id}/adm/counselling/` | `#session-table-body` | `innerHTML` |
| Reschedule modal open | `click` | GET `/api/v1/group/{group_id}/adm/counselling/{session_id}/reschedule/` | `#reschedule-modal` | `innerHTML` |
| Reschedule form submit | `submit` | POST `/api/v1/group/{group_id}/adm/counselling/{session_id}/reschedule/` | `#session-table-body` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
