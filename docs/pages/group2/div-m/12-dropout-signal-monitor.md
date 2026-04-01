# 12 — Dropout Signal Monitor

> **URL:** `/group/analytics/dropout/`
> **File:** `12-dropout-signal-monitor.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Academic Data Analyst (Role 104, G1) · Analytics Director (Role 102, G1) · MIS Officer (Role 103, G1)

---

## 1. Purpose

Early warning system that identifies students at risk of dropping out before they actually disengage or leave. The system calculates a Dropout Risk Score (0–100) for every enrolled student by combining six signals: attendance trend (last 30/60/90 days), exam score trend (improving or declining), fee payment status (defaulter?), counselling visits logged, welfare incident involvement, and engagement proxies (library usage, extracurricular participation). Students scoring above threshold are flagged. The Academic Data Analyst reviews flagged students, escalates to branch principals for intervention, and monitors whether intervention reduces the risk score. This is a read-only analytics view — the Analyst does not modify student records, only creates escalation notices and internal notes.

**Risk score bands:**
- 0–30: Low Risk (green)
- 31–50: Moderate Risk (amber)
- 51–75: High Risk (orange)
- 76–100: Critical Risk (red) — immediate escalation required

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Academic Data Analyst | 104 | G1 | Full — view all, escalate, mark false positive, add notes | Primary owner |
| Group Analytics Director | 102 | G1 | View + Export — no escalation or note actions | Oversight |
| Group MIS Officer | 103 | G1 | View + Export — no actions | For reporting |
| Group Exam Analytics Officer | 105 | G1 | View only — limited to exam signal column | Partial view |
| All other roles | — | — | No access | Redirected |

> **Access enforcement:** `@require_role(['academic_data_analyst', 'analytics_director', 'mis_officer', 'exam_analytics_officer'])`. Escalation and note endpoints: `@require_role('academic_data_analyst')` only. Role 105 receives a queryset filtered to show only exam-relevant signal columns.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Dropout Signal Monitor
```

### 3.2 Page Header
```
Dropout Signal Monitor                          [Export ↓]  [Refresh Scores ↻]
[Group Name] — Academic Data Analyst  ·  Last score update: [date time]
AY [current academic year]  ·  [N] Students Monitored  ·  [N] High+Critical Risk  ·  [N] Escalations Pending
```

`[Export ↓]` — dropdown: Export to PDF / Export to XLSX (current filtered view). Roles 102, 103, 104.
`[Refresh Scores ↻]` — triggers manual re-calculation of dropout scores for all students (Role 104 only). Shows confirmation modal before running — "This will recalculate risk scores for all [N] enrolled students. It may take 1–3 minutes."

### 3.3 Alert Banners (conditional)

| Condition | Banner Text | Severity |
|---|---|---|
| Critical risk students not yet escalated | "[N] student(s) are at Critical dropout risk and have not been escalated to their branch principal." | Red |
| Escalations without branch response > 7 days | "[N] escalation(s) have had no response from the branch principal for more than 7 days." | Red |
| Month-over-month increase in high-risk students | "High+Critical risk student count increased by [N]% compared to last month." | Amber |
| Branches with disproportionately high risk counts | "[N] branch(es) have more than 10% of students classified as High or Critical risk: [list]." | Amber |
| Scores not refreshed in > 7 days | "Dropout risk scores were last updated [N] days ago. Refresh scores for current accuracy." | Amber |

---

## 4. KPI Summary Bar

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Students Monitored | All enrolled students with a risk score | `DropoutScore.objects.filter(ay=current_ay).count()` | Indigo (neutral) | `#kpi-total-monitored` |
| 2 | High + Critical Risk | Students with risk score > 50 | `DropoutScore.objects.filter(ay=current_ay, score__gt=50).count()` | Red > 100 · Amber 50–100 · Green < 50 | `#kpi-high-critical` |
| 3 | Critical Risk (76–100) | Students with score > 75 | `DropoutScore.objects.filter(ay=current_ay, score__gt=75).count()` | Red if > 0 · Green = 0 | `#kpi-critical` |
| 4 | Escalations Pending | Escalations sent but no branch response | `Escalation.objects.filter(status='pending', ay=current_ay).count()` | Red if > 0 · Green = 0 | `#kpi-escalations-pending` |
| 5 | Interventions Successful | Students whose risk score dropped by ≥ 20 pts after escalation | `Escalation.objects.filter(ay=current_ay, outcome='improved').count()` | Green always | `#kpi-interventions-ok` |
| 6 | Branches with High Concentration | Branches where > 10% of enrolled are High+Critical | `BranchRiskSummary.objects.filter(ay=current_ay, high_risk_pct__gt=10).count()` | Amber if > 0 · Green = 0 | `#kpi-high-concentration` |

**HTMX:** `<div id="dropout-kpi-bar" hx-get="/api/v1/group/{id}/analytics/dropout/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`.

---

## 5. Sections

### 5.1 Dropout Risk Register

**Search bar:** Student name, roll number, branch. Debounced 300ms.

**Filter chips:** `[Risk Level ▾]` `[Branch ▾]` `[Class ▾]` `[Stream ▾]` `[Fee Status ▾]` `[Escalation Status ▾]` `[Date Range ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Student Name | `student_name` | ▲▼ | Clickable → `dropout-student-detail` drawer |
| Roll No. | `roll_no` | ▲▼ | — |
| Branch | `branch_name` | ▲▼ | — |
| Class | `class_name` | ▲▼ | Class 6 / 7 / … / 12 |
| Stream | `stream` | ▲▼ | MPC / BiPC / MEC / CEC / General |
| Risk Score | `risk_score` | ▲▼ | Numeric badge 0–100; colour per band |
| Risk Level | `risk_level` | ▲▼ | Low / Moderate / High / Critical — colour badge |
| Attendance (30d) | `att_30d_pct` | ▲▼ | %; colour: ≥ 75% green · 60–74% amber · < 60% red |
| Last Exam Score | `last_exam_score_pct` | ▲▼ | %; colour coded |
| Fee Status | `fee_status` | ▲▼ | Paid / Partial / Defaulter — colour badge |
| Counselling Visits | `counselling_visits` | ▲▼ | Count this AY |
| Days Since Last Alert | `days_since_last_alert` | ▲▼ | — |
| Escalated? | `escalation_status` | ▲▼ | Not Escalated / Escalated / Responded / Resolved — badge |
| Actions | — | — | `[View]` · `[Escalate]` (Role 104, not-yet-escalated only) · `[False Positive]` (Role 104) |

**Default sort:** Risk Score descending (Critical first).
**Pagination:** 25 rows · `« Previous  Page N of N  Next »` · Rows per page: 25 / 50 / 100.

**Row colour:**
- Critical Risk (76–100): `bg-red-50 border-l-4 border-red-400`
- High Risk (51–75): `bg-orange-50`
- Not-yet-escalated Critical: `bg-red-100` (stronger shade)

### 5.2 Escalation Queue

> Students escalated to branch principals but with no response in > 7 days.

**Panel header:** "Escalations Awaiting Branch Response — [N] pending" with red icon if count > 0.

Collapsible. When expanded:

| Column | Notes |
|---|---|
| Student Name | Clickable → detail drawer |
| Branch | — |
| Risk Score | Badge |
| Escalated On | Date |
| Days Without Response | Red if > 7 |
| Branch Principal | Name |
| Actions | `[Send Reminder]` (Role 104) · `[View Escalation]` |

`[Send Reminder]` → `hx-post` to `remind` endpoint → sends notification to branch principal → toast "Reminder sent to [Principal Name]."

### 5.3 Intervention Outcomes

> Students previously flagged and escalated, showing their current risk status. Tracks whether intervention worked.

Collapsible panel. When expanded, shows table:

| Column | Notes |
|---|---|
| Student Name | — |
| Branch | — |
| Original Risk Score | Score at time of escalation |
| Current Risk Score | Latest score |
| Score Change | Positive delta = improvement (green) · Negative = worsened (red) |
| Escalated On | Date |
| Outcome | Improved / No Change / Worsened / Dropped Out |

---

## 6. Drawers & Modals

### 6.1 `dropout-student-detail` Drawer — 560px, right-slide

**Trigger:** Clicking student name or `[View]` action.

**Header:**
```
[Student Name]  ·  [Roll No.]                               [×]
[Branch]  ·  [Class]  ·  [Stream]
Risk Score: [N] [colour badge]  ·  Level: [band]  ·  Escalated: [Yes/No]
```

**Tab 1 — Risk Profile**

Risk score gauge (large semicircular gauge, colour matches band).

Contributing factors table:

| Signal | Weight | Raw Value | Score Contribution | Status |
|---|---|---|---|---|
| Attendance Trend (30d) | 30% | 61% | 27/30 pts | ⚠️ Below 75% |
| Exam Score Trend | 25% | Declining (−12% last 2 exams) | 22/25 pts | ⚠️ Declining |
| Fee Payment Status | 20% | Defaulter (₹8,400 outstanding) | 20/20 pts | 🔴 Defaulter |
| Counselling Visits | 10% | 0 visits this AY | 0/10 pts | — |
| Welfare Incidents | 10% | 1 Severity 2 incident | 7/10 pts | — |
| Engagement Proxy | 5% | No library/ECa activity | 5/5 pts | — |

**Tab 2 — Attendance Detail**

90-day attendance line chart. Table: Month | Classes Held | Classes Attended | Attendance %.
Pattern analysis: "Most absences on: Monday (12 absences), Friday (9 absences)" — helps identify reason.

**Tab 3 — Academic Detail**

Line chart — last 5 exam scores with class average overlay.
Table: Exam Name | Date | Score | Class Avg | vs Class.
Subject-wise scores for last exam.

**Tab 4 — Actions**

**Escalation section (Role 104 only):**

If not yet escalated:
- `[Escalate to Branch Principal]` button → opens `escalation-create` inline form within tab:
  - Pre-filled: Student name, branch, risk score
  - Editable: To (auto-filled: Branch Principal name — read-only), Message (template pre-populated, editable), Urgency (Standard / High / Critical)
  - `[Send Escalation]` button

If already escalated:
- Escalation details (sent to, date, message, urgency)
- Current status badge (Pending / Responded / Resolved)
- Response from principal (if received) — read-only text
- `[Mark as Resolved]` button (if status = Responded)
- `[Send Reminder]` button (if Pending > 7 days)

**False Positive section (Role 104 only):**
`[Mark as False Positive]` button — confirmation modal: "Are you sure this student is not at genuine dropout risk? This will remove them from the register for this academic year." — Reason required (min 20 chars).

**Internal Notes section (Role 104 only):**
Add analyst note (textarea, min 10 chars, `[Save Note]` button).
Notes history: timestamp, note text.

### 6.2 `score-recalculate` Modal — 420px, centred

**Trigger:** `[Refresh Scores ↻]` header button. Role 104 only.

```
Refresh Dropout Risk Scores
This will recalculate risk scores for all [N] enrolled students.
This process runs in the background and may take 1–3 minutes.
Data sources used: attendance (last 90 days), last 3 exam scores, fee status, counselling records, welfare incidents.
```

**Footer:** `[Cancel]`  `[Start Recalculation]`

On confirm: job queued → status polling via HTMX every 5s → `hx-get` on `/api/v1/.../dropout/recalc-status/` → updates `#recalc-status-badge` until `status = complete` → toast "Risk scores updated for [N] students."

---

## 7. Charts

### 7.1 Risk Score Distribution Histogram

| Property | Value |
|---|---|
| Chart type | Vertical bar (Chart.js 4.x) |
| Title | "Student Dropout Risk Distribution — [Current AY]" |
| Data | Count of students in each risk band: Low / Moderate / High / Critical |
| X-axis | Risk bands (Low 0–30, Moderate 31–50, High 51–75, Critical 76–100) |
| Y-axis | Student count |
| Bar colours | Low: green · Moderate: amber · High: orange · Critical: red |
| Tooltip | "[Band]: [N] students ([N]% of monitored)" |
| Interactive | Click on bar → applies risk level filter to §5.1 table |
| Empty state | "No dropout risk data available." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/dropout/distribution/` |
| HTMX | `<div id="chart-distribution" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

### 7.2 Dropout Risk Trend — Line Chart

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "High + Critical Risk Students — Last 6 Months" |
| Data | Count of High Risk and Critical Risk students per month for last 6 months (2 lines) |
| X-axis | Month names |
| Y-axis | Student count |
| Line colours | High Risk: orange · Critical Risk: red |
| Tooltip | "[Month] · High Risk: [N] · Critical: [N]" |
| Legend | Bottom |
| Trend annotation | If consecutive months increasing: add "↑ Trend" annotation in red |
| Empty state | "Insufficient historical data to show trend." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/dropout/trend/?months=6` |
| HTMX | `<div id="chart-trend" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Escalation sent | "Escalation sent to [Principal Name] at [Branch] for [Student Name]." | Success |
| Escalation reminder sent | "Reminder sent to [Principal Name] for [Student Name]'s escalation." | Success |
| Mark resolved | "[Student Name] escalation marked as resolved." | Success |
| Mark false positive | "[Student Name] marked as false positive and removed from risk register for this AY." | Info |
| Note saved | "Analyst note saved for [Student Name]." | Success |
| Score recalculation started | "Risk score recalculation started. This may take 1–3 minutes." | Info |
| Score recalculation complete | "Risk scores updated for [N] students." | Success |
| Score recalculation failed | "Risk score recalculation failed. Please try again." | Error |
| Escalation — principal not found | "Branch principal role not configured at [Branch]. Please contact Group IT Admin." | Error |
| Export generated | "Dropout risk report exported to [format]." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Drawer load error | "Could not load student details. Please try again." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |
| False positive — missing reason | "Please provide a reason (minimum 20 characters)." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No students monitored | `users` | "No Students in Monitor" | "No enrolled students have a dropout risk score yet. Refresh scores to populate the register." | `[Refresh Scores]` (Role 104) |
| No High/Critical risk students | `check-circle` | "No High-Risk Students" | "No students are currently at High or Critical dropout risk." | — |
| No results matching filters | `funnel` | "No Students Match Filters" | "Try adjusting or clearing your filters." | `[Clear Filters]` |
| Escalation queue — no pending | `check-circle` | "No Pending Escalations" | "All escalations have been responded to by branch principals." | — |
| Intervention outcomes — no data | `chart-bar` | "No Intervention Data" | "No escalations have been tracked to an outcome yet." | — |
| Student detail — no attendance | `calendar` | "No Attendance Data" | "Attendance records are not available for this student." | — |
| Student detail — no exam data | `academic-cap` | "No Exam Data" | "No exam results are linked to this student." | — |
| Student detail — no notes | `pencil` | "No Analyst Notes" | "No internal notes have been added for this student." | `[Add Note]` (Role 104) |
| Charts — no data | `chart-bar` | "No data available" | — | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Risk register table: 8 shimmer rows. Escalation queue: shimmer header. Intervention outcomes: shimmer header. |
| Search/filter change | Table rows replaced by shimmer rows + spinner below toolbar |
| `dropout-student-detail` drawer open | Drawer slides in; shimmer risk gauge + shimmer factor table |
| Tab switch in drawer | Shimmer content per tab |
| Escalation form submit | `[Send Escalation]` button disabled + "Sending…" + spinner |
| Send reminder | `[Send Reminder]` button disabled + "Sending…" + spinner for 2s |
| Mark resolved | Button disabled + spinner |
| Mark false positive — confirm | Modal button disabled + spinner |
| Score recalculation — running | `#recalc-status-badge` shows "Recalculating… [spinner]"; HTMX polls `/recalc-status/` every 5s |
| Export | Button disabled + "Preparing…" + spinner |
| Chart — distribution click filtering | Table shimmer while applying risk band filter |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 104 (Academic Analyst) | Role 102 (Analytics Dir) | Role 103 (MIS Officer) | Role 105 (Exam) |
|---|---|---|---|---|
| Page | ✅ Full | ✅ View | ✅ View | ✅ Limited |
| KPI Bar | Full | Full | Full | Partial (first 3 only) |
| Charts | ✅ Both | ✅ Both | ✅ Both | ✅ Both |
| Risk register table — all columns | ✅ | ✅ | ✅ | Exam score column only |
| `[Export ↓]` button | ✅ | ✅ | ✅ | ❌ |
| `[Refresh Scores ↻]` button | ✅ | ❌ | ❌ | ❌ |
| `[Escalate]` action in table | ✅ | ❌ | ❌ | ❌ |
| `[False Positive]` action in table | ✅ | ❌ | ❌ | ❌ |
| `[View]` action in table | ✅ | ✅ | ✅ | ✅ |
| Student detail drawer — Tab 1–3 | ✅ All | ✅ All | ✅ All | Tabs 1 + 3 only |
| Student detail drawer — Tab 4 Actions | ✅ Full | ❌ Hidden | ❌ Hidden | ❌ Hidden |
| Escalation queue — `[Send Reminder]` | ✅ | ❌ | ❌ | ❌ |
| Alert banners | ✅ All | ✅ All | ✅ All | First 2 only |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/dropout/kpi/
```
Query: `academic_year`.
Response: `{ "total_monitored": N, "high_critical": N, "critical": N, "escalations_pending": N, "interventions_successful": N, "high_concentration_branches": N }`.

### 12.2 Dropout Risk Register
```
GET /api/v1/group/{group_id}/analytics/dropout/students/
```

| Query Parameter | Type | Description |
|---|---|---|
| `academic_year` | string | Default current |
| `risk_level` | string (multi) | `low` · `moderate` · `high` · `critical` |
| `branch` | int | Branch ID |
| `class_name` | string | e.g. `class_10` |
| `stream` | string | `mpc` · `bipc` · `mec` · `cec` · `general` |
| `fee_status` | string | `paid` · `partial` · `defaulter` |
| `escalation_status` | string | `not_escalated` · `escalated` · `responded` · `resolved` |
| `search` | string | Student name, roll number, branch |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · 100 |
| `ordering` | string | `-risk_score` (default) · `student_name` · `att_30d_pct` · `branch_name` |

Response: `{ count, next, previous, results: [...] }`.

### 12.3 Student Dropout Detail
```
GET /api/v1/group/{group_id}/analytics/dropout/students/{student_id}/
```
Response: Full object — risk score, all 6 signal contributions, attendance data, exam scores, escalation history, notes.

### 12.4 Create Escalation
```
POST /api/v1/group/{group_id}/analytics/dropout/students/{student_id}/escalate/
```
Body: `{ "message": "string", "urgency": "standard|high|critical" }`. Role 104 only.
Response: 201 Created — escalation object.

### 12.5 Send Escalation Reminder
```
POST /api/v1/group/{group_id}/analytics/dropout/escalations/{id}/remind/
```
Body: `{}`. Role 104 only; only if status = pending and last reminder > 7 days ago.
Response: 200 OK.

### 12.6 Mark Escalation Resolved
```
POST /api/v1/group/{group_id}/analytics/dropout/escalations/{id}/resolve/
```
Body: `{ "resolution_note": "string" }`. Role 104 only.
Response: 200 OK.

### 12.7 Mark False Positive
```
POST /api/v1/group/{group_id}/analytics/dropout/students/{student_id}/false-positive/
```
Body: `{ "reason": "string" (min 20 chars) }`. Role 104 only.
Response: 200 OK — student removed from risk register for current AY.

### 12.8 Add Analyst Note
```
POST /api/v1/group/{group_id}/analytics/dropout/students/{student_id}/notes/
```
Body: `{ "note": "string" }`. Role 104 only.
Response: 201 Created.

### 12.9 Trigger Score Recalculation
```
POST /api/v1/group/{group_id}/analytics/dropout/recalculate/
```
Body: `{}`. Role 104 only. Queues async job.
Response: 202 Accepted — `{ "job_id": "...", "status": "queued" }`.

### 12.10 Check Recalculation Status
```
GET /api/v1/group/{group_id}/analytics/dropout/recalc-status/
```
Response: `{ "status": "queued|running|complete|failed", "progress_pct": N, "students_processed": N }`.
Used by HTMX polling in score recalculation modal.

### 12.11 Distribution Chart Data
```
GET /api/v1/group/{group_id}/analytics/dropout/distribution/
```
Response: `{ "low": N, "moderate": N, "high": N, "critical": N }`.

### 12.12 Trend Chart Data
```
GET /api/v1/group/{group_id}/analytics/dropout/trend/
```
Query: `months` (default 6).
Response: `{ "labels": [...months], "high_risk": [...], "critical_risk": [...] }`.

### 12.13 Escalation Queue
```
GET /api/v1/group/{group_id}/analytics/dropout/escalations/?status=pending&days_without_response=7
```
Response: paginated list of escalations with no branch response in 7+ days.

### 12.14 Export
```
GET /api/v1/group/{group_id}/analytics/dropout/export/
```
Query: `format` (pdf/xlsx), all filter params from §12.2.
Response: File download.

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="dropout-kpi-bar">` | GET `.../dropout/kpi/` | `#dropout-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"` |
| Chart 7.1 load | `<div id="chart-distribution">` | GET `.../dropout/distribution/` | `#chart-distribution` | `innerHTML` | `hx-trigger="load"` |
| Chart 7.2 load | `<div id="chart-trend">` | GET `.../dropout/trend/` | `#chart-trend` | `innerHTML` | `hx-trigger="load"` |
| Risk register — search | `<input id="dropout-search">` | GET `.../dropout/students/?search=` | `#dropout-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Risk register — filter chips | Filter selects | GET `.../dropout/students/?filters=` | `#dropout-table` | `innerHTML` | `hx-trigger="change"` |
| Risk register — pagination | Pagination buttons | GET `.../dropout/students/?page={n}` | `#dropout-table` | `innerHTML` | `hx-trigger="click"` |
| Distribution chart — bar click | Bar element | GET `.../dropout/students/?risk_level={band}` | `#dropout-table` | `innerHTML` | JS `chartClick` → `hx-get` |
| Open student detail drawer | Student name / `[View]` | GET `/htmx/analytics/dropout/students/{id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Student drawer tab switch | Tab buttons | GET `/htmx/analytics/dropout/students/{id}/tab/{slug}/` | `#dropout-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Send escalation (from drawer Tab 4) | Escalation form | POST `.../dropout/students/{id}/escalate/` | `#escalation-result-{id}` | `innerHTML` | `hx-encoding="application/json"`; `hx-on::after-request="showToast(event);"` |
| Send reminder (escalation queue) | `[Send Reminder]` per row | POST `.../escalations/{id}/remind/` | `#remind-btn-{id}` | `outerHTML` | Shows "Sent ✓" 3s then reverts |
| Mark resolved | `[Mark as Resolved]` | POST `.../escalations/{id}/resolve/` | `#escalation-status-{id}` | `outerHTML` | Confirm first via modal |
| Mark false positive — open modal | `[False Positive]` button | GET `/htmx/analytics/dropout/false-positive-modal/?student={id}` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Mark false positive — confirm | Modal form | POST `.../dropout/students/{id}/false-positive/` | `#student-row-{id}` | `outerHTML` | `hx-on::after-request="closeModal(); showToast(event);"` |
| Open recalculate modal | `[Refresh Scores ↻]` | GET `/htmx/analytics/dropout/recalc-modal/` | `#modal-container` | `innerHTML` | `hx-trigger="click"` |
| Start recalculation | Modal confirm button | POST `.../dropout/recalculate/` | `#recalc-status-badge` | `innerHTML` | `hx-on::after-request="startPolling();"` |
| Poll recalculation status | `<div id="recalc-status-badge">` | GET `.../dropout/recalc-status/` | `#recalc-status-badge` | `innerHTML` | `hx-trigger="every 5s"`; stops when `status=complete` via `hx-swap-oob` or JS check |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
