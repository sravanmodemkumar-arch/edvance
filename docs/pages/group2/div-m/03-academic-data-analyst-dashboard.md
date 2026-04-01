# 104 — Academic Data Analyst Dashboard

> **URL:** `/group/analytics/academic/`
> **File:** `03-academic-data-analyst-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Academic Data Analyst (Role 104, G1) — exclusive post-login landing

---

## 1. Purpose

The Academic Data Analyst Dashboard is the primary analytical workspace for the Group Academic Data Analyst (Role 104), focused on early-warning intelligence for academic health across all branches. The dashboard surfaces dropout risk signals by aggregating attendance, exam scores, and engagement data through a risk-scoring algorithm, enabling proactive intervention before students disengage entirely. It also tracks rank trends per branch, flags teachers whose performance metrics have deteriorated, and provides a branch-level academic health composite. At group scale (20,000–1,00,000 students, 5–50 branches), early identification of the top 1–5% at-risk students can prevent significant dropout events, protecting both student outcomes and group revenue.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Academic Data Analyst | 104 | G1 | Full Read + Manage own analytics outputs | Exclusive landing page |
| Analytics Director | 102 | G1 | Read-only (navigation access) | Not landing page |
| All other roles | Any | Any | No access | HTTP 403 |

Access enforcement: `@role_required(104)` Django decorator. Analytics Director (102) receives read-only rendering — all write controls hidden server-side.

---

## 3. Page Layout

### 3.1 Breadcrumb

```
Group Home > Analytics & MIS > Academic Data Analyst Dashboard
```

### 3.2 Page Header

**Title:** `Academic Data Analyst Dashboard`
**Sub-title:** `[Group Name] · Academic Year: [current AY] · As of: [last data refresh timestamp]`

Action buttons (right-aligned):

| Button | Icon | Behaviour | Visible To |
|---|---|---|---|
| Run Risk Analysis | play-circle | Triggers dropout risk re-scoring job (async) | Role 104 |
| Export Report | download | Opens Export modal (PDF/XLSX) | Role 104 |
| Schedule Analysis | calendar | Opens Schedule modal | Role 104 |
| Refresh | refresh | HTMX re-poll KPIs + tables | Role 104, 102 |

AY Selector: `<select>` listing current + last 4 AYs. Change triggers full dashboard reload.

### 3.3 Alert Banners

Individually dismissible per session via `sessionStorage`.

| Condition | Banner Text | Severity |
|---|---|---|
| High-risk student count increased > 10% vs last month | "⚠ Dropout risk has increased by [N]% this month. [K] new students flagged as high risk." | Error (red) |
| Branch with 3+ consecutive months of rank decline | "📉 [N] branch(es) show 3+ consecutive months of rank decline. Review urgently." | Error (red) |
| Teacher performance alerts > 5 unresolved | "[N] teacher performance alerts are unresolved. Review and take action." | Warning (amber) |
| Last risk analysis run > 7 days ago | "Risk analysis has not been run in [N] days. Run now for current signals." | Warning (amber) |
| No student data for current month | "No student academic data found for the current month. Check data pipeline." | Error (red) |
| Risk analysis running | "Risk analysis is running. Results will update automatically." | Info (blue, auto-dismiss when job complete) |
| All indicators healthy | "All academic indicators are within healthy ranges." | Success (green, auto-dismiss 6s) |

---

## 4. KPI Summary Bar

HTMX auto-refresh every 120 seconds via `hx-trigger="every 120s"`.

| Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|
| Students at High Dropout Risk | Students with risk score ≥ 70 (scale 0–100), current month | COUNT(student_risk_scores WHERE risk_score >= 70 AND month = current AND ay = current) | Green = 0; Amber 1–10; Red ≥ 11 | `#kpi-high-risk` |
| Branches with Declining Rank Trends | Branches with mean rank worse than previous 2 consecutive months | COUNT(branch_rank_trends WHERE direction = 'declining' AND consecutive_months >= 2) | Green = 0; Amber 1–2; Red ≥ 3 | `#kpi-declining-ranks` |
| Teachers with Performance Alerts | Teachers with any unresolved performance flag | COUNT(teacher_alerts WHERE status = 'open') | Green = 0; Amber 1–5; Red ≥ 6 | `#kpi-teacher-alerts` |
| Attendance < 75% Students | Students with cumulative attendance below 75%, current AY | COUNT(student_attendance WHERE cumulative_pct < 75 AND ay = current) | Green = 0; Amber ≤ 50; Red > 50 | `#kpi-low-attendance` |
| Scholarship Merit Trend | Direction of avg merit score for scholarship students vs last month | UP ↑ (green) / DOWN ↓ (red) / STABLE (grey); value = current avg merit score | Arrow colour | `#kpi-merit-trend` |
| Academic Anomalies Flagged | Data anomalies in academic records (duplicates, outliers) flagged in last 30 days | COUNT(academic_anomalies WHERE flagged_at >= NOW()-30d AND status = 'open') | Green = 0; Amber 1–3; Red ≥ 4 | `#kpi-anomalies` |

---

## 5. Sections

### 5.1 Dropout Risk Register

**Purpose:** Lists all students currently flagged by the risk-scoring algorithm, ordered by risk level. Each row shows the key signals that contributed to the score so the analyst can interpret and act.

**Search bar:** Search by student name, roll number, branch. Debounced 300 ms. Placeholder: "Search student name, roll no, or branch…".

**Inline filter chips:**
- Risk Level: All | Critical (≥ 90) | High (70–89) | Medium (50–69)
- Branch: Multi-select branch list
- Class/Grade: All | Class 9 | Class 10 | Class 11 | Class 12 | Other
- Signal Type: All | Low Attendance | Low Score | Disengagement | Combined
- Date Added: All | Added This Week | Added This Month

**Advanced filter drawer (360px, slide-in right):**
- Risk score range slider (0–100)
- Gender: All / Male / Female / Other
- Category: All / SC / ST / OBC / General
- Scholarship holder: All / Yes / No
- Hostel student: All / Yes / No
- "Apply Filters" / "Clear All" buttons; active filters shown as chips; filter count badge

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Student Name | `student.full_name` | Yes | Click → Student Risk Drawer |
| Roll No | `student.roll_no` | Yes | Monospace |
| Class | `student.class_grade` | Yes | |
| Branch | `student.branch_name` | Yes | |
| Risk Score | `student_risk_scores.risk_score` | Yes | 0–100; colour bar (red ≥ 70, amber 50–69, green < 50) |
| Risk Level | Derived | Yes | Critical / High / Medium badge |
| Attendance % | `student_risk_scores.attendance_pct` | Yes | Red < 60%, amber 60–74%, green ≥ 75% |
| Avg Score | `student_risk_scores.avg_exam_score` | Yes | Red < 40%, amber 40–59%, green ≥ 60% |
| Disengagement Score | `student_risk_scores.disengagement_score` | Yes | Internal signal 0–10 (missing submissions, library use, event participation) |
| Flagged Since | `student_risk_scores.flagged_since` | Yes | Date first flagged; relative |
| Score Change | `student_risk_scores.score_delta_30d` | Yes | ↑/↓ X pts vs 30 days ago; red if worsening |
| Actions | — | No | View Detail / Add Note / Dismiss Risk (with confirm) |

**Default sort:** Risk Score descending (Critical first).

**Pagination:** Server-side, 25/page.

**Bulk action:** Checkbox select → "Export Selected" or "Add Bulk Note".

---

### 5.2 Branch Academic Health Summary

**Purpose:** Branch-level academic health composite, giving the analyst a quick view of which branches are excelling and which need attention.

**Search bar:** Branch name or code. Debounced 300 ms.

**Inline filter chips:**
- Health Band: All | Excellent (≥ 80) | Good (60–79) | Needs Attention (40–59) | Critical (< 40)
- Region/Zone: dynamic
- Branch Type: All | Day | Residential | Semi-Residential
- Rank Trend: All | Improving | Stable | Declining

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Branch Name | `branch.name` | Yes | Click → opens Branch Academic Drawer |
| Branch Code | `branch.code` | Yes | Monospace |
| Region | `branch.zone` | Yes | |
| Total Students | `branch_academic.total_students` | Yes | |
| High-Risk Students | `branch_academic.high_risk_count` | Yes | Red if > 5% of total |
| Avg Attendance % | `branch_academic.avg_attendance_pct` | Yes | Colour-coded |
| Avg Exam Score | `branch_academic.avg_exam_score` | Yes | Colour-coded |
| Mean Rank (local) | `branch_academic.mean_rank` | Yes | Lower = better; tooltip: "Rank within branch cohort" |
| Rank Trend | `branch_academic.rank_trend` | Yes | ↑ Improving (green) / → Stable (grey) / ↓ Declining (red) |
| Teacher Alert Count | `branch_academic.open_teacher_alerts` | Yes | Red if ≥ 2 |
| Academic Health Score | `branch_academic.health_score` | Yes | 0–100; colour bar |
| Actions | — | No | View Detail |

**Default sort:** Academic Health Score ascending (worst first).

**Pagination:** Server-side, 25/page.

---

### 5.3 Teacher Performance Alerts

**Purpose:** Lists teachers flagged for performance concerns — declining student outcomes in their class, high failure rates, attendance issues — enabling the analyst to produce evidence-based reports for branch principals.

**Search bar:** Teacher name, subject, branch. Debounced 300 ms.

**Inline filter chips:**
- Alert Type: All | High Failure Rate | Low Attendance Impact | Consistent Low Scores | Syllabus Lag | Multiple Flags
- Branch: Multi-select
- Subject: Multi-select
- Status: All | Open | Under Review | Resolved

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Teacher Name | `teacher.full_name` | Yes | Click → Teacher Alert Drawer |
| Employee ID | `teacher.emp_id` | Yes | Monospace |
| Branch | `teacher.branch_name` | Yes | |
| Subject(s) | `teacher.subjects` | No | Comma list; truncated 40 chars |
| Classes Taught | `teacher.classes` | No | e.g., "11A, 11B, 12A" |
| Alert Type | `teacher_alert.alert_type` | Yes | Colour-coded badge |
| Avg Student Score (this class) | `teacher_alert.avg_student_score` | Yes | Score in teacher's subject for teacher's classes |
| Group Avg (same subject) | `teacher_alert.group_avg_subject_score` | Yes | Comparison benchmark; red if teacher's avg < group avg − 15 pts |
| Consecutive Months Flagged | `teacher_alert.consecutive_months` | Yes | Red if ≥ 3 |
| Status | `teacher_alert.status` | Yes | Open / Under Review / Resolved badge |
| Flagged At | `teacher_alert.flagged_at` | Yes | Datetime, relative |
| Actions | — | No | View Detail / Mark Under Review / Resolve |

**Default sort:** Consecutive Months Flagged descending, then Alert Type severity.

**Pagination:** Server-side, 25/page.

---

### 5.4 Rank Trend Alerts

**Purpose:** Lists branches showing a consistent decline in mean student rank (within their own cohort) over 2+ consecutive months, so the analyst can investigate root causes.

**Search bar:** Branch name or code. Debounced 300 ms.

**Inline filter chips:**
- Trend Duration: All | 2 Months | 3 Months | 4+ Months
- Region/Zone: dynamic
- Severity: All | Critical (4+ months) | High (3 months) | Watch (2 months)

**Table columns:**

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| # | Row index | No | |
| Branch Name | `branch.name` | Yes | Click → opens Branch Academic Drawer |
| Branch Code | `branch.code` | Yes | |
| Region | `branch.zone` | Yes | |
| Mean Rank M-3 | `branch_rank_trend.rank_3m_ago` | Yes | 3 months ago (lower = better) |
| Mean Rank M-2 | `branch_rank_trend.rank_2m_ago` | Yes | 2 months ago |
| Mean Rank M-1 | `branch_rank_trend.rank_1m_ago` | Yes | Last month |
| Mean Rank Current | `branch_rank_trend.rank_current` | Yes | Current month |
| Trend Arrow | Calculated | Yes | ↓↓ worst trend (red, bold) |
| Consecutive Declining Months | `branch_rank_trend.consecutive_months` | Yes | Red if ≥ 3 |
| Primary Suspect Subject | `branch_rank_trend.primary_subject` | Yes | Subject with biggest score drop |
| Note | `branch_rank_trend.analyst_note` | No | Editable inline (Role 104 only, max 200 chars) |
| Actions | — | No | View Detail / Add Note / Flag for Report |

**Default sort:** Consecutive Declining Months descending.

**Pagination:** Server-side, 25/page.

---

## 6. Drawers & Modals

### 6.1 Student Risk Detail Drawer

Triggered by: Student name in Section 5.1.
Width: 600px. Slide from right. ESC / backdrop closes with guard.

**Tabs:**

**Tab 1 — Risk Profile**

| Field | Value |
|---|---|
| Student Name | Full name |
| Roll No | Monospace |
| Class & Section | |
| Branch | |
| Hostel | Yes/No; if yes: hostel name |
| Scholarship | Yes/No; scholarship type |
| Risk Score | Large display: 0–100 + colour gauge |
| Risk Level | Critical / High / Medium badge |
| Score History | Sparkline: last 6 months risk scores |
| Flagged Since | Date |

**Tab 2 — Signal Breakdown**

Table: Signal | Value | Threshold | Status
Rows:
- Attendance % | [value] | < 75% | Triggered / OK
- Avg Exam Score | [value] | < 50% | Triggered / OK
- Disengagement Score | [value] | > 7 | Triggered / OK
- Consecutive Absent Days | [value] | > 10 | Triggered / OK
- Fee Default | Yes/No | — | Triggered / OK
- Parental Contact | Days since last contact | > 30d | Triggered / OK

**Tab 3 — Academic History**

Line chart (inline, 200px height): exam scores per test, last 10 tests.
Table: Exam Name | Date | Score | Branch Avg | Rank

**Tab 4 — Notes & Actions**

Table: Note | Added By | Date
"Add Note" form: Textarea (required, max 500 chars, character counter), "Save Note" button.

**Footer:** "Export Student Risk Report" (PDF) / "Dismiss Risk Flag" (with confirm modal, reason required) / "Close"

---

### 6.2 Teacher Alert Detail Drawer

Triggered by: Teacher name in Section 5.3.
Width: 600px. Slide from right. ESC / backdrop closes.

**Tabs:**

**Tab 1 — Teacher Profile**

| Field | Value |
|---|---|
| Name | Full name |
| Employee ID | |
| Branch | |
| Subject(s) | |
| Classes | |
| Designation | |
| Joining Date | |

**Tab 2 — Performance Metrics**

Table: Month | Subject | Classes Taught | Avg Student Score | Group Avg | Variance | Trend
Last 6 months. Variance highlighted red if < −15 pts.

**Tab 3 — Alert History**

Table: Alert Type | Flagged At | Status | Resolution Note
All historical alerts for this teacher.

**Tab 4 — Analyst Notes**

Same as Student Risk drawer Tab 4.

**Footer:** "Mark Under Review" / "Resolve Alert" (opens Resolve modal with reason field) / "Export Report" / "Close"

---

### 6.3 Branch Academic Detail Drawer

Triggered by: Branch name in 5.2 or 5.4.
Width: 600px.

**Tabs:**

**Tab 1 — Academic Overview**

| Field | Value |
|---|---|
| Branch | Name + Code |
| Type | Day / Residential |
| Total Students | Count |
| Academic Health Score | Gauge |
| Rank Trend | ↑/→/↓ with month count |
| High Risk Students | Count + % |
| Avg Attendance | % |
| Avg Score | % |

**Tab 2 — Subject Breakdown**

Table: Subject | Avg Score | Group Avg | Teacher Name | Status (OK/Alert)

**Tab 3 — Risk Distribution**

Pie chart: Critical / High / Medium / Low risk students.
Table: Risk Level | Count | % of Total

**Tab 4 — Analyst Notes**

Same note format.

**Footer:** "Flag Branch for Report" / "Export" / "Close"

---

### 6.4 Export Modal

Triggered by: "Export Report" button.
Size: 480px centred overlay.

| Field | Type | Required | Validation |
|---|---|---|---|
| Report Title | Text | Yes | Max 150 chars |
| Report Type | Radio: Dropout Risk / Teacher Performance / Branch Health / Full Academic Report | Yes | |
| Format | Radio: PDF / XLSX | Yes | Default: PDF |
| Academic Year | Select | Yes | |
| Branch Scope | Checkbox group | Yes | All / Specific; at least 1 |
| Include Charts | Toggle | No | Default: ON |
| Notes | Textarea | No | Max 500 chars |

**Footer:** "Generate Export" / "Cancel"

---

## 7. Charts

### 7.1 Dropout Risk Trend — Line Chart

| Property | Value |
|---|---|
| Type | Chart.js Line |
| Title | "Dropout Risk Trend — Students Flagged per Month (Last 6 Months)" |
| Data | Monthly count of students with risk_score ≥ 70, split by risk level: Critical (≥ 90), High (70–89). Two lines + total line. |
| X-Axis | Month labels: "Oct 25", "Nov 25", "Dec 25", "Jan 26", "Feb 26", "Mar 26" |
| Y-Axis | "Students Flagged"; integer ticks |
| Colours | Critical line `#EF4444` (red), High line `#F97316` (orange), Total line `#6B7280` (grey, dashed) |
| Tooltip | "[Month]: [N] Critical, [M] High, [Total] total flagged" |
| Data Points | Circle markers, 5px |
| API Endpoint | `GET /api/v1/analytics/academic/dropout-risk-trend/?ay=2025-26` |
| HTMX Pattern | `hx-get` on AY selector change; target `#chart-dropout-trend`; swap `innerHTML` |
| Export | PNG export button top-right |
| Colorblind-safe | Yes — colour + line dash pattern differentiation |
| Empty State | "No risk trend data available for the selected academic year." |

---

### 7.2 Academic Health Score Distribution — Bar Chart

| Property | Value |
|---|---|
| Type | Chart.js Bar (grouped) |
| Title | "Academic Health Score by Branch — [Current AY]" |
| Data | Bar per branch showing academic health score. Horizontal reference line at 60 (benchmark). Bars grouped by region/zone, or sorted by score. |
| X-Axis | Branch short names (rotated 45°) |
| Y-Axis | "Health Score" 0–100 |
| Colours | Score ≥ 80 `#22C55E` (green), 60–79 `#EAB308` (amber), 40–59 `#F97316` (orange), < 40 `#EF4444` (red) |
| Tooltip | "[Branch]: Health Score [X] · High-Risk Students: [N] · Avg Score: [S]%" |
| Reference Line | Dashed line at y=60 labelled "Benchmark" |
| API Endpoint | `GET /api/v1/analytics/academic/health-scores/?ay=2025-26` |
| HTMX Pattern | `hx-get` on AY selector change; target `#chart-health-scores`; swap `innerHTML` |
| Export | PNG export top-right |
| Colorblind-safe | Yes — colour + value labels above bars |
| Empty State | "No academic health data available for the selected academic year." |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Page load success | "Academic Data Analyst Dashboard loaded." | Success |
| Page load error | "Failed to load dashboard data. Please refresh." | Error |
| KPI refresh success | "KPIs refreshed." | Success |
| KPI refresh error | "Could not refresh KPIs." | Error |
| Risk analysis job started | "Risk analysis job started. Results will update automatically." | Info |
| Risk analysis job complete | "Risk analysis complete. [N] students flagged." | Success |
| Risk analysis job error | "Risk analysis failed. Please try again or contact support." | Error |
| Student note saved | "Note saved for [Student Name]." | Success |
| Student note save error | "Failed to save note. Please try again." | Error |
| Risk flag dismissed | "Risk flag dismissed for [Student Name]." | Success |
| Risk flag dismiss error | "Failed to dismiss risk flag." | Error |
| Teacher alert status updated | "Alert status updated to [Status]." | Success |
| Teacher alert update error | "Failed to update alert status." | Error |
| Branch flagged for report | "Branch '[Name]' flagged for inclusion in next report." | Success |
| Branch flag error | "Failed to flag branch. Please try again." | Error |
| Rank trend note saved | "Note saved for branch '[Name]'." | Success |
| Rank trend note error | "Failed to save note." | Error |
| Export queued | "Export job queued. Download will begin when ready." | Info |
| Export failed | "Export generation failed. Please try again." | Error |
| Filter cleared | "All filters cleared." | Info |
| AY changed | "Showing data for [AY]." | Info |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| 5.1 Dropout Risk Register — no students flagged | shield-check (green) | "No Students at Dropout Risk" | "The risk algorithm has not flagged any students in the current period. Run a fresh analysis to verify." | "Run Risk Analysis" button |
| 5.1 Register — search/filter no match | magnify | "No Matching Students" | "Adjust search terms or filters." | "Clear Filters" |
| 5.2 Branch Academic Health — no branches | building (grey) | "No Branch Academic Data" | "Branch academic data will appear once branches submit exam and attendance data." | None |
| 5.2 Branch Health — search/filter no match | magnify | "No Matching Branches" | "Try different search terms or filters." | "Clear Filters" |
| 5.3 Teacher Alerts — no alerts | check-circle (green) | "No Teacher Performance Alerts" | "All teachers are within acceptable performance thresholds." | None |
| 5.3 Alerts — search/filter no match | magnify | "No Matching Alerts" | "Adjust search or filters." | "Clear Filters" |
| 5.4 Rank Trend Alerts — no alerts | trending-up (green) | "No Rank Decline Alerts" | "All branches show stable or improving rank trends. Keep monitoring." | None |
| 5.4 Rank Trends — search/filter no match | magnify | "No Matching Branches" | "Adjust search or filters." | "Clear Filters" |
| 7.1 Dropout Risk chart — no data | chart-line (grey) | "No Risk Trend Data" | "Risk trend data will appear after the first risk analysis run." | "Run Risk Analysis" |
| 7.2 Health Score chart — no data | chart-bar (grey) | "No Health Score Data" | "Branch health scores will appear once branch data is available for the selected AY." | None |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | Skeleton: 6 KPI cards grey pulsing; all 4 tables show 5 skeleton rows; charts show grey rectangle placeholders |
| KPI auto-refresh (120s) | Spinner in KPI card headers; values fade 60% |
| AY selector change | All KPIs + tables + charts show skeletons simultaneously |
| Risk analysis job running | Page-wide info banner: "Risk analysis running…" with progress spinner; KPI #1 card shows spinner overlay |
| Dropout Risk table search/filter | Table body shows 5 skeleton rows; search input shows spinner |
| Branch Health table search/filter | Same — 5 skeleton rows |
| Teacher Alerts table search/filter | Same |
| Rank Trend table search/filter | Same |
| Student Risk drawer opening | Drawer slides in with skeleton: 4 tab headers + skeleton fields + sparkline placeholder |
| Teacher Alert drawer opening | Same pattern |
| Branch Academic drawer opening | Same pattern |
| Export generation | Export button shows spinner + "Generating…"; disabled during job |
| Student note save | "Save Note" button shows spinner; form dims 50% |
| Chart loading | Grey pulsing rectangle until Chart.js data arrives |

---

## 11. Role-Based UI Visibility

| UI Element | Role 104 (Academic Data Analyst) | Role 102 (Analytics Director) | All Others |
|---|---|---|---|
| Full page | Visible | Read-only | Hidden (403) |
| "Run Risk Analysis" button | Visible, enabled | Hidden | N/A |
| "Export Report" button | Visible, enabled | Visible, enabled | N/A |
| "Schedule Analysis" button | Visible, enabled | Hidden | N/A |
| "Refresh" button | Visible | Visible | N/A |
| KPI bar | Visible | Visible | N/A |
| Alert banners | Visible, dismissible | Visible, dismissible | N/A |
| 5.1 "Add Note" / "Dismiss Risk" | Visible, enabled | Hidden | N/A |
| 5.3 "Mark Under Review" / "Resolve" | Visible, enabled | Hidden | N/A |
| 5.4 Inline rank note field | Visible, editable | Read-only | N/A |
| 5.4 "Flag for Report" | Visible, enabled | Hidden | N/A |
| Student Risk drawer — notes/actions | Visible | Read-only | N/A |
| Teacher Alert drawer — status change | Visible, enabled | Hidden | N/A |
| Charts | Visible | Visible | N/A |
| Advanced filter drawer | Visible | Visible | N/A |

All write controls: `{% if request.user.role_id == 104 %}` in Django templates.

---

## 12. API Endpoints

| Method | Endpoint | Auth | Description | Query Parameters |
|---|---|---|---|---|
| GET | `/api/v1/analytics/academic/kpis/` | JWT · Role 104, 102 | All 6 KPI values | `month`, `ay` |
| GET | `/api/v1/analytics/academic/dropout-risk/` | JWT · Role 104, 102 | Paginated dropout risk register | `page`, `page_size`, `search`, `risk_level`, `branch_id`, `class_grade`, `signal_type`, `date_from`, `risk_min`, `risk_max`, `gender`, `category`, `scholarship`, `hostel`, `sort_by`, `sort_dir` |
| GET | `/api/v1/analytics/academic/dropout-risk/{student_id}/` | JWT · Role 104, 102 | Student risk detail (for drawer) | `ay` |
| POST | `/api/v1/analytics/academic/dropout-risk/{student_id}/notes/` | JWT · Role 104 | Add note to student risk record | — (body: `{"note": "..."}`) |
| DELETE | `/api/v1/analytics/academic/dropout-risk/{student_id}/flag/` | JWT · Role 104 | Dismiss student risk flag | — (body: `{"reason": "..."}`) |
| GET | `/api/v1/analytics/academic/branch-health/` | JWT · Role 104, 102 | Branch academic health table | `page`, `page_size`, `search`, `health_band`, `zone`, `branch_type`, `rank_trend`, `sort_by`, `sort_dir` |
| GET | `/api/v1/analytics/academic/branch-health/{branch_id}/` | JWT · Role 104, 102 | Branch academic detail | `ay` |
| GET | `/api/v1/analytics/academic/teacher-alerts/` | JWT · Role 104, 102 | Paginated teacher performance alerts | `page`, `page_size`, `search`, `alert_type`, `branch_id`, `subject`, `status`, `sort_by`, `sort_dir` |
| GET | `/api/v1/analytics/academic/teacher-alerts/{teacher_id}/` | JWT · Role 104, 102 | Teacher alert detail | `ay` |
| PATCH | `/api/v1/analytics/academic/teacher-alerts/{alert_id}/` | JWT · Role 104 | Update alert status | — (body: `{"status": "under_review", "note": "..."}`) |
| GET | `/api/v1/analytics/academic/rank-trends/` | JWT · Role 104, 102 | Rank trend alerts table | `page`, `page_size`, `search`, `duration`, `zone`, `severity`, `sort_by`, `sort_dir` |
| PATCH | `/api/v1/analytics/academic/rank-trends/{branch_id}/note/` | JWT · Role 104 | Update analyst note for branch rank trend | — (body: `{"note": "..."}`) |
| POST | `/api/v1/analytics/academic/rank-trends/{branch_id}/flag/` | JWT · Role 104 | Flag branch for report | — |
| POST | `/api/v1/analytics/academic/risk-analysis/run/` | JWT · Role 104 | Trigger risk analysis job | — (body: `{"ay": "2025-26", "branch_scope": "all"}`) |
| GET | `/api/v1/analytics/academic/risk-analysis/{job_id}/status/` | JWT · Role 104 | Poll analysis job status | — |
| GET | `/api/v1/analytics/academic/dropout-risk-trend/` | JWT · Role 104, 102 | Chart: dropout risk trend data | `ay` |
| GET | `/api/v1/analytics/academic/health-scores/` | JWT · Role 104, 102 | Chart: branch health scores | `ay` |
| POST | `/api/v1/analytics/academic/export/` | JWT · Role 104 | Queue academic report export | — (body: export config) |

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI auto-refresh | `<div id="kpi-bar">` | `hx-get="/htmx/analytics/academic/kpis/"` | `#kpi-bar` | `outerHTML` | `hx-trigger="every 120s"` |
| AY selector change | `<select id="ay-selector">` | `hx-get="/htmx/analytics/academic/?ay={val}"` | `#dashboard-content` | `innerHTML` | |
| Dropout risk table search | `<input id="risk-search">` | `hx-get="/htmx/analytics/academic/dropout-risk/"` | `#risk-table-body` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Dropout risk filter chips | Chip `<button>` elements | `hx-get="/htmx/analytics/academic/dropout-risk/"` | `#risk-table-body` | `innerHTML` | Chip state serialised as params |
| Dropout risk advanced filter | "Apply Filters" `<button>` | `hx-get="/htmx/analytics/academic/dropout-risk/"` | `#risk-table-body` | `innerHTML` | Serialises filter drawer form |
| Dropout risk sort | Column `<th>` | `hx-get="/htmx/analytics/academic/dropout-risk/"` | `#risk-table-body` | `innerHTML` | |
| Dropout risk pagination | `<a>` pagination | `hx-get="/htmx/analytics/academic/dropout-risk/"` | `#risk-table-body` | `innerHTML` | |
| Branch health table search/filter/sort/page | Same pattern | `hx-get="/htmx/analytics/academic/branch-health/"` | `#branch-health-table-body` | `innerHTML` | |
| Teacher alerts table search/filter/sort/page | Same pattern | `hx-get="/htmx/analytics/academic/teacher-alerts/"` | `#teacher-alerts-table-body` | `innerHTML` | |
| Rank trend table search/filter/sort/page | Same pattern | `hx-get="/htmx/analytics/academic/rank-trends/"` | `#rank-trend-table-body` | `innerHTML` | |
| Student risk drawer open | Student name `<a>` | `hx-get="/htmx/analytics/academic/student-risk/{id}/"` | `#detail-drawer-content` | `innerHTML` | |
| Teacher alert drawer open | Teacher name `<a>` | `hx-get="/htmx/analytics/academic/teacher-alert/{id}/"` | `#detail-drawer-content` | `innerHTML` | |
| Branch academic drawer open | Branch name `<a>` | `hx-get="/htmx/analytics/academic/branch-detail/{id}/"` | `#detail-drawer-content` | `innerHTML` | |
| Risk analysis job status poll | `<div id="risk-job-status">` | `hx-get="/htmx/analytics/academic/risk-analysis/{id}/status/"` | `#risk-job-status` | `outerHTML` | `hx-trigger="every 5s"` while 'running'; stops on complete/error via `HX-Trigger` header |
| Rank trend inline note save | Note `<input>` blur | `hx-post="/htmx/analytics/academic/rank-trends/{id}/note/"` | `#rank-note-{id}` | `outerHTML` | `hx-trigger="blur"` |
| Dropout trend chart refresh | AY selector | `hx-get="/htmx/analytics/academic/chart/dropout-trend/"` | `#chart-dropout-trend` | `innerHTML` | |
| Health score chart refresh | AY selector | `hx-get="/htmx/analytics/academic/chart/health-scores/"` | `#chart-health-scores` | `innerHTML` | |
| Alert banner dismiss | Close `<button>` | `hx-post="/htmx/alerts/dismiss/{id}/"` | `#alert-banner-{id}` | `outerHTML` | + `sessionStorage` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
