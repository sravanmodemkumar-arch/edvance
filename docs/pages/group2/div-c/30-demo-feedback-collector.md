# Page 30: Demo Feedback Collector

**URL:** `/group/adm/demo/feedback/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Demo Classes

---

## 1. Purpose

The Demo Feedback Collector is the quality assurance layer for the entire demo class program. Every demo session is only as good as the impression it leaves on students and parents, and the only reliable way to measure that impression is through structured, systematically collected feedback. This page aggregates feedback submitted by demo attendees — via QR code forms distributed at the end of each session or sent via WhatsApp post-event — and presents the results in a form that enables both tactical follow-up and strategic quality improvement.

For the Demo Coordinator, the page surfaces immediate signals: which sessions scored poorly this week, which teacher consistently receives low ratings, and which branch has a feedback collection rate so low that the data cannot be trusted. These signals feed directly into operational decisions — reassigning a demo teacher whose ratings have dropped below 3.5, investigating a branch where student experience appears to be declining, or revisiting the demo format for a subject that consistently draws comments about pace. Feedback scores are also piped into teacher performance tracking, ensuring that demo delivery quality is factored into overall faculty assessment.

Beyond individual session quality, the page computes an NPS (Net Promoter Score) — the percentage of respondents who would actively recommend the coaching institute to others, minus detractors. For a competitive coaching group, NPS from demo attendees is a direct indicator of word-of-mouth admissions momentum. The Admissions Director uses the NPS trend and the teacher feedback leaderboard to assess whether demo program quality is improving over the admission season and to make resource decisions about which branches deserve more demo investment.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Demo Class Coordinator (29) | G3 | Full — view all feedback, manage form, investigate low-rated sessions, export | Primary owner |
| Group Admissions Director (23) | G3 | View-only across all branches and teachers | Strategic oversight |
| Group Admission Coordinator (24) | G3 | View-only for all feedback | Operational awareness |
| Demo Teacher (Branch Staff) | Branch | Read-only view of own demo feedback only | Cannot see other teachers' feedback |

Access enforcement: All views protected with `@login_required` and `@role_required(['demo_coordinator', 'admissions_director', 'admission_coordinator', 'demo_teacher'])`. Demo Teacher scope enforced via `request.user.staff_id` queryset filter — only feedback rows where `teacher_id = request.user.staff_id` are returned.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Demo Classes → Feedback`

### 3.2 Page Header
**Title:** Demo Feedback Collector
**Subtitle:** Attendee feedback scores, NPS, and teacher ratings from demo sessions
**Actions (right-aligned):**
- `[Export All Responses CSV]` — secondary button
- `[Manage Feedback Form]` — opens feedback-form-editor drawer

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Teachers with avg demo rating < 3.5 exist | Warning (amber) | "N teachers have average demo ratings below 3.5. Review Teacher Feedback Leaderboard." |
| Branches with feedback collection rate < 30% | Warning (amber) | "N branches have collected feedback from fewer than 30% of attendees. Consider improving collection method." |
| New feedback submissions not yet reviewed | Info (blue) | "N new feedback submissions since your last visit. [Review →]" |
| Low-rated demo (avg < 3.0) just flagged | Error (red) | "Demo DM-0499 at [Branch] received an average rating of 2.6. [Investigate →]" |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Feedback Submitted (This Month) | COUNT feedback forms submitted in current month | `demo_feedback` | Blue always | Filters table to current month |
| Avg Demo Rating | AVG overall_rating across all demos this month (out of 5) | `demo_feedback` | Green if ≥ 4.0; amber if 3.0–3.9; red if < 3.0 | No drill-down |
| NPS Score | % Promoters (rating 5) − % Detractors (rating 1–2) | `demo_feedback` | Green if ≥ 50; amber if 20–49; red if < 20 | Scrolls to NPS display in 5.1 |
| Teachers Below 3.5 Rating | COUNT distinct teachers with avg demo rating < 3.5 this month | `demo_feedback` GROUP BY teacher | Red if > 0; green if 0 | Scrolls to Section 5.3 |
| Branches < 30% Collection Rate | COUNT branches where feedback_count / attended_count < 0.3 | `demo_feedback` JOIN `demo_attendance` | Red if > 0; green if 0 | Filters to those branches |
| Pending Review | COUNT feedback submissions with status = new | `demo_feedback` WHERE reviewed = False | Amber if > 0 | Filters table to unreviewed |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/demo/feedback/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Feedback Dashboard (Aggregate View)

**Display:** Four-panel analytics dashboard rendered at the top of the page.

**Panel A — Avg Rating Trend (Chart.js 4.x line chart):**
- X-axis: Last 6 months (month labels)
- Y-axis: Avg rating (0–5)
- Series: Group-wide average line; toggle overlay for individual branches
- Tooltip: Month, avg rating, total responses

**Panel B — Rating Distribution (Chart.js 4.x donut):**
- Segments: 5★ / 4★ / 3★ / 2★ / 1★
- Centre label: overall average rating
- Legend with counts and percentages

**Panel C — NPS Calculation Display:**
- Three stat tiles: Promoters (5★) % | Passives (3–4★) % | Detractors (1–2★) %
- NPS = Promoters% − Detractors% displayed large in centre
- Colour: Green ≥ 50 / Amber 20–49 / Red < 20

**Panel D — Top Themes (Tag List):**
- Keyword/phrase tags extracted from free-text comments (processed server-side)
- Colour intensity indicates frequency: darker = more mentions
- Examples: "excellent teacher", "too fast", "want to enroll", "more examples needed", "good atmosphere"
- Tags are clickable — clicking filters feedback table to responses containing that phrase

**HTMX:** Dashboard panels lazy-loaded via `hx-get="/group/adm/demo/feedback/dashboard/"` with `hx-trigger="load"`, `hx-target="#feedback-dashboard"`.

---

### 5.2 Feedback Table

**Display:** Full-width sortable, selectable, server-side paginated table (20 rows/page). Default sort: submitted_at descending.

**Columns:**

| Column | Notes |
|---|---|
| Date | Demo date |
| Demo Branch | Branch name |
| Subject | Subject / stream |
| Student Name | Respondent name |
| Parent Name | Parent respondent name (if different form) |
| Overall Rating | Star display (1–5) with numeric label |
| Teacher Rating | Star display (1–5) |
| Content Rating | Star display (1–5) |
| Would Recommend | Yes / No / Maybe (badge) |
| Top Comment | Truncated to 60 chars; hover tooltip shows full |
| Conversion Status | Applied / Not Yet / Lost (badge) — linked to admissions record |
| Actions | `[View →]` — opens feedback-detail drawer |

**Filters (filter bar):**
- Branch (dropdown)
- Teacher (searchable dropdown)
- Overall rating range (slider: 1–5)
- Date range (from / to date pickers)
- Conversion status (Applied / Not Yet / Lost / All)
- Reviewed status (All / Unreviewed only)

**HTMX:** Filter inputs use `hx-get="/group/adm/demo/feedback/table/"` with `hx-trigger="change"`, `hx-target="#feedback-table"`, `hx-swap="innerHTML"`. Pagination: `hx-get` with `?page=N`.

**Empty state:** "No feedback submissions match the selected filters."

---

### 5.3 Teacher Feedback Leaderboard

**Display:** Sortable table of all demo teachers ranked by average demo rating (highest first). Includes all teachers who have conducted at least one demo session this month.

**Columns:**

| Column | Notes |
|---|---|
| Rank | # |
| Teacher | Name |
| Branch | Home branch |
| Subject | Demo subject speciality |
| Sessions | Total sessions this month |
| Avg Rating | Out of 5 (colour-coded: green ≥ 4 / amber 3–3.9 / red < 3) |
| NPS | Net promoter score for this teacher |
| Best Comment | Highlighted top comment (highest-rated response) |
| Action | `[View Full →]` — opens teacher-feedback-full drawer |

**Sort:** Clickable column headers. Default: Avg Rating descending.

**HTMX:** Loaded via `hx-get="/group/adm/demo/feedback/teacher-leaderboard/"` on section load.

**Empty state:** "No teacher feedback data for this period."

---

### 5.4 Low Feedback Alerts

**Display:** Alert-style list panel with red left border. Shows all demo sessions where average rating < 3.0 this month.

**Each entry shows:**
Branch | Demo ID | Demo date | Teacher name | Subject | Avg rating (red badge) | Response count | `[Investigate →]` button (opens feedback-detail drawer filtered to that session)

**HTMX:** `hx-get="/group/adm/demo/feedback/low-alerts/"` on load, `hx-target="#low-feedback-alerts"`.

**Empty state (positive):** Green banner — "No demo sessions with average ratings below 3.0 this month."

---

### 5.5 Feedback Form Manager

**Display:** Card panel showing the current active feedback form configuration.

**Content:**
- Form name (e.g., "Post-Demo Feedback Form v3")
- Questions count | Last updated date
- `[Preview QR Code]` — opens modal with QR code image (links to public form URL) and download PNG button
- `[Edit Form]` — opens feedback-form-editor drawer
- `[View Responses Count]` — inline stat: total responses via this form version
- `[Export All Responses CSV]` — downloads all time responses

**HTMX:** Card loaded on page; QR preview via `hx-get="/group/adm/demo/feedback/qr-preview/"` targeting `#modal-container`.

---

## 6. Drawers & Modals

### 6.1 `feedback-detail` Drawer
**Width:** 560px
**Trigger:** `[View →]` in feedback table or `[Investigate →]` in low-feedback alerts
**HTMX endpoint:** `hx-get="/group/adm/demo/feedback/detail/{feedback_id}/"` lazy-loaded
**Content:**
- Session summary (branch, date, teacher, subject)
- Full form response: all questions with answers and ratings
- Student/parent details
- Free-text comments (full, untruncated)
- Conversion outcome (with link to admissions record)
- Mark as reviewed toggle — `hx-post` updates reviewed status

---

### 6.2 `teacher-feedback-full` Drawer
**Width:** 480px
**Trigger:** `[View Full →]` in teacher leaderboard
**HTMX endpoint:** `hx-get="/group/adm/demo/feedback/teacher/{teacher_id}/"` lazy-loaded
**Content:**
- Teacher summary: name, branch, total sessions, overall avg rating, NPS
- Monthly rating trend (mini Chart.js line chart — last 6 months)
- All feedback entries for this teacher (paginated list, 10/drawer-page)
- Top positive and top critical comments highlighted

---

### 6.3 `feedback-form-editor` Drawer
**Width:** 640px
**Trigger:** `[Edit Form]` in Feedback Form Manager card
**HTMX endpoint:** `hx-get="/group/adm/demo/feedback/form-editor/"` lazy-loaded
**Content:**
- Question list (drag-to-reorder)
- Per-question: question text (editable), type (star rating / yes-no-maybe / text / dropdown), mandatory toggle
- `[Add Question]` inline — appends new question row via `hx-post` + `beforeend` swap
- Scale setting (1–5 default; adjustable)
- Form title and description fields
- `[Save Form]` — `hx-post` updates form; existing responses preserved, new version created

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Feedback form saved | "Feedback form updated. New version active." | Success | 4s |
| Marked as reviewed | "Feedback marked as reviewed." | Success | 2s |
| Export triggered | "CSV export is being prepared. Download will start shortly." | Info | 4s |
| QR code downloaded | "QR code image downloaded." | Success | 2s |
| Form question added | "New question added to form." | Success | 2s |
| Form question deleted | "Question removed from form." | Warning | 3s |
| Form editor save failed | "Save failed. Please check all questions have content." | Error | 5s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No feedback submitted yet | Star outline icon | "No feedback collected yet" | "Feedback will appear here after demo attendees submit responses via the QR code form." | `[Preview Feedback Form →]` |
| No feedback matching filters | Filtered list icon | "No feedback matches your filters" | "Try adjusting the branch, teacher, or date range filters." | `[Clear Filters]` |
| Teacher leaderboard — no data | Trophy outline | "No teacher feedback yet" | "Teacher ratings will appear once demo sessions have been rated." | None |
| Low feedback alerts — none | Shield checkmark | "No low-rated sessions" | "All demo sessions this month are above the 3.0 rating threshold." | None |
| Feedback table — all reviewed | Checkmark list | "All feedback reviewed" | "You have reviewed all submitted feedback responses." | None |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Feedback dashboard loading | Skeleton chart placeholders (4 panels) |
| Feedback table loading | Skeleton rows (5 rows, column placeholders) |
| Teacher leaderboard loading | Skeleton rows (4 rows) |
| Low feedback alerts loading | Skeleton list rows (3 rows) |
| Drawer opening (any) | Spinner centred in drawer body |
| Filter change (table reload) | Table body skeleton (3 rows) during fetch |
| QR code modal loading | Spinner in modal container |
| KPI auto-refresh | Subtle pulse on KPI cards (no full skeleton) |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Demo Coordinator (29) | Admissions Director (23) | Admission Coordinator (24) | Demo Teacher (Branch) |
|---|---|---|---|---|
| Feedback table — all sessions | Visible | Visible | Visible | Own feedback only |
| Teacher leaderboard — all teachers | Visible | Visible | Visible | Own row only |
| Low feedback alerts | Visible | Visible | Visible | Own sessions only |
| `[Manage Feedback Form]` button | Visible | Hidden | Hidden | Hidden |
| `[Edit Form]` in form manager | Visible | Hidden | Hidden | Hidden |
| Mark as reviewed toggle | Visible | Hidden | Hidden | Hidden |
| `[Export All Responses CSV]` | Visible | Visible | Visible | Hidden |
| NPS full breakdown | Visible | Visible | Visible | Own sessions only |
| Tag theme list (clickable) | Visible | Visible | Visible | Hidden |
| `[Investigate →]` in low alerts | Visible | Visible | Hidden | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/` | JWT G3+ | List all feedback with filters |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/{id}/` | JWT G3+ | Single feedback detail |
| PATCH | `/api/v1/group/{group_id}/adm/demo/feedback/{id}/reviewed/` | JWT G3 write | Mark feedback as reviewed |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/dashboard/` | JWT G3+ | Dashboard aggregate stats |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/teacher-leaderboard/` | JWT G3+ | Teacher feedback leaderboard |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/teacher/{teacher_id}/` | JWT G3+ | All feedback for one teacher |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/low-alerts/` | JWT G3+ | Sessions with avg rating < 3.0 |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/form/` | JWT G3+ | Current feedback form config |
| PUT | `/api/v1/group/{group_id}/adm/demo/feedback/form/` | JWT G3 write | Update feedback form |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/qr/` | JWT G3+ | Generate QR code for form URL |
| GET | `/api/v1/group/{group_id}/adm/demo/feedback/export/` | JWT G3+ | Export all responses as CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/demo/feedback/kpis/` | `#kpi-bar` | `outerHTML` |
| Feedback dashboard load | `load` | GET `/group/adm/demo/feedback/dashboard/` | `#feedback-dashboard` | `innerHTML` |
| Filter change → reload table | `change` on any filter | GET `/group/adm/demo/feedback/table/` | `#feedback-table` | `innerHTML` |
| Table pagination | `click` on page link | GET `/group/adm/demo/feedback/table/?page=N` | `#feedback-table` | `innerHTML` |
| Theme tag click → filter table | `click` on tag | GET `/group/adm/demo/feedback/table/?theme=keyword` | `#feedback-table` | `innerHTML` |
| Open feedback detail drawer | `click` on `[View →]` | GET `/group/adm/demo/feedback/detail/{id}/` | `#drawer-container` | `innerHTML` |
| Mark as reviewed | `click` on toggle in drawer | POST `/group/adm/demo/feedback/{id}/reviewed/` | `#review-status-{id}` | `innerHTML` |
| Open teacher feedback drawer | `click` on `[View Full →]` | GET `/group/adm/demo/feedback/teacher/{id}/` | `#drawer-container` | `innerHTML` |
| Open investigate drawer | `click` on `[Investigate →]` | GET `/group/adm/demo/feedback/detail/{feedback_id}/` | `#drawer-container` | `innerHTML` |
| Load teacher leaderboard | `load` | GET `/group/adm/demo/feedback/teacher-leaderboard/` | `#teacher-leaderboard` | `innerHTML` |
| Load low feedback alerts | `load` | GET `/group/adm/demo/feedback/low-alerts/` | `#low-feedback-alerts` | `innerHTML` |
| Open form editor drawer | `click` on `[Edit Form]` | GET `/group/adm/demo/feedback/form-editor/` | `#drawer-container` | `innerHTML` |
| Add question in form editor | `click` on `[Add Question]` | POST `/group/adm/demo/feedback/form/question/` | `#question-list` | `beforeend` |
| Save form editor | `submit` | POST `/group/adm/demo/feedback/form-editor/` | `#form-manager-card` | `outerHTML` |
| QR code preview modal | `click` on `[Preview QR Code]` | GET `/group/adm/demo/feedback/qr-preview/` | `#modal-container` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
