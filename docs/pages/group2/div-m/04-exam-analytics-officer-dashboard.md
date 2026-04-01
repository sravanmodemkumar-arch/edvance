# 04 — Exam Analytics Officer Dashboard

> **URL:** `/group/analytics/exam/`
> **File:** `04-exam-analytics-officer-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Exam Analytics Officer (Role 105, G1) — exclusive post-login landing

---

## 1. Purpose

Primary post-login workspace for the Group Exam Analytics Officer. Provides a command-centre view of exam performance across all branches — covering monthly tests, unit tests, half-yearly and annual exams, JEE/NEET mock tests, and Olympiad internal tests. The officer identifies which branches and subjects have the widest score gaps, surfaces critical topic-level weaknesses, monitors JEE/NEET integrated coaching performance, and generates exam analytics reports that feed into MIS outputs and academic intervention decisions.

Scale: 20–50 branches · 8–15 exams per branch per AY · 15–20 subjects across all streams · 1,00,000+ exam records per large group per AY.

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Exam Analytics Officer | 105 | G1 | Full — all sections, all analytics actions, export | Exclusive dashboard |
| Group Analytics Director | 102 | G1 | — | Has own dashboard `/group/analytics/director/` |
| Group MIS Officer | 103 | G1 | — | Has own dashboard `/group/mis/officer/` |
| Group Academic Data Analyst | 104 | G1 | — | Has own dashboard `/group/analytics/academic/` |
| Group Hostel Analytics Officer | 106 | G1 | — | Has own dashboard `/group/analytics/hostel/` |
| Group Strategic Planning Officer | 107 | G1 | — | Has own dashboard `/group/analytics/strategy/` |
| All other roles | — | — | — | Redirected to own dashboard |

> **Access enforcement:** `@require_role('exam_analytics_officer')` on all views and API endpoints. G1 level — read-only on exam data from Division B; full CRUD on own analytics outputs (reports, gap escalations, export jobs).

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Analytics & MIS  ›  Exam Analytics Officer Dashboard
```

### 3.2 Page Header
```
Welcome back, [Officer Name]                    [Export Exam Report ↓]  [+ New Gap Escalation]
[Group Name] — Exam Analytics Officer · Last login: [date time]
AY [current academic year]  ·  [N] Exams Analysed  ·  [N] Subjects Tracked  ·  [N] Topic Gaps Open
```

`[Export Exam Report ↓]` — dropdown: Export to PDF / Export to XLSX (current AY exam summary). Role 105 only.
`[+ New Gap Escalation]` — opens `gap-escalation-create` drawer. Role 105 only.

### 3.3 Alert Banners (conditional)

Stacked above KPI bar. Each individually dismissible for the session.

| Condition | Banner Text | Severity |
|---|---|---|
| Subjects with group avg < 40% (critical) | "[N] subject(s) have a group average below 40% — immediate intervention required: [Subject list]." | Red |
| Exam data not loaded for current month | "No exam results have been uploaded for [Month]. Branch exam data may be missing." | Red |
| Topic gap escalations pending acknowledgement > 14 days | "[N] topic gap escalation(s) have not been acknowledged by the Academic Director in 14+ days." | Red |
| JEE/NEET mock performance declining 3+ consecutive tests | "JEE/NEET mock performance has declined for [N] consecutive tests across [N] branches." | Amber |
| Branches below group average in 5+ subjects | "[N] branch(es) are below group average in 5 or more subjects. Review required." | Amber |
| No exam records for current AY | "No exam records have been loaded for this academic year. Check data pipeline." | Blue |

---

## 4. KPI Summary Bar

Six metric cards displayed horizontally. Auto-refresh every 5 minutes via HTMX polling.

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Exams Analysed This AY | Count of exams with results loaded in current AY | `Exam.objects.filter(ay=current_ay, results_loaded=True).count()` | Indigo (neutral) | `#kpi-exams-analysed` |
| 2 | Subjects with Avg < 50% | Subjects where group-wide average score < 50% | `SubjectAvg.objects.filter(ay=current_ay, group_avg__lt=50).count()` | Red if > 0 · Green = 0 | `#kpi-subjects-critical` |
| 3 | Branches Below Group Average | Branches whose composite exam score is below the group average | `BranchScore.objects.filter(ay=current_ay, composite_score__lt=group_avg).count()` | Amber if > 30% of branches · Indigo otherwise | `#kpi-branches-below` |
| 4 | JEE/NEET Mock Avg AIR | Average All India Rank equivalent across all integrated coaching branches (latest mock) | `JEEMock.objects.filter(ay=current_ay).order_by('-date').first().avg_air` | Green < 5000 · Amber 5000–15000 · Red > 15000 | `#kpi-jee-air` |
| 5 | Topic Gaps Identified | Open topic gaps (unresolved) across all branches | `TopicGap.objects.filter(resolved=False, ay=current_ay).count()` | Red if > 20 · Amber 10–20 · Green < 10 | `#kpi-topic-gaps` |
| 6 | Escalations Pending | Gap escalations sent to Academic Director, no response | `GapEscalation.objects.filter(status='pending', ay=current_ay).count()` | Red if > 0 · Green = 0 | `#kpi-escalations` |

**HTMX:** `<div id="exam-kpi-bar" hx-get="/api/v1/group/{id}/analytics/exam/kpi/" hx-trigger="load, every 300s" hx-swap="innerHTML" hx-indicator="#kpi-spinner">`. Cards shimmer on first load.

---

## 5. Sections

### 5.1 Recent Exam Results — Branch Summary

> Latest exam with results loaded, showing branch-by-branch breakdown.

**Exam selector:** Dropdown at top of section — select which exam to display (default: most recent). Options show exam name + date + type badge.

**Search bar:** Branch name. Debounced 300ms.

**Filter chips:** `[Stream ▾]` `[Zone ▾]` `[Branch Type ▾]`

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | Clickable — opens `exam-branch-detail` drawer |
| Zone | `zone_name` | ▲▼ | "—" if no zone layer |
| Students Appeared | `appeared_count` | ▲▼ | Count who sat the exam |
| Avg Score (%) | `avg_score_pct` | ▲▼ | Colour: ≥ 80% green · 60–79% amber · 40–59% orange · < 40% red |
| Pass Rate (%) | `pass_rate_pct` | ▲▼ | Pass = score ≥ 35% (configurable threshold) |
| Highest Score | `highest_score` | ▲▼ | — |
| vs Group Avg | `vs_group_avg` | ▲▼ | "+5.2%" green · "-3.1%" red |
| Subject Gaps | `subject_gaps_count` | ▲▼ | Count of subjects where branch avg < 50% · Red badge if > 0 |
| Actions | — | — | `[View Details]` · `[View Heatmap]` |

**Default sort:** Avg Score (%) ascending (worst first — so problems are visible immediately).
**Pagination:** 25 rows · Controls: `« Previous  Page N of N  Next »` · Rows per page: 25 / 50 / All.

### 5.2 Critical Subject Gaps Panel

> Subjects where group-wide average is below 50% — requires immediate action.

**Panel header:** "Critical Subject Gaps — [N] subject(s) below 50% group average" with red icon. Collapsible.

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Subject | `subject_name` | ▲▼ | Badge colour per stream |
| Stream | `stream` | ▲▼ | MPC / BiPC / MEC / All |
| Group Avg (%) | `group_avg_pct` | ▲▼ | Always red (< 50% threshold) |
| Branches Affected | `branches_below_50_count` | ▲▼ | How many branches have avg < 50% for this subject |
| Worst Branch | `worst_branch_name` | — | Branch with lowest avg |
| Worst Branch Score | `worst_branch_score` | ▲▼ | — |
| Trend | `trend` | ▲▼ | ↑ improving · ↓ declining · → stable |
| Escalated? | `escalation_status` | ▲▼ | Green badge if escalated · Red badge if not yet escalated |
| Actions | — | — | `[Escalate to Academic Dir]` · `[View Topic Gaps]` |

**Default sort:** Branches Affected DESC.
**Pagination:** 10 rows · `[View All Subject Gaps →]` links to Page 17 (Exam Performance Heatmap).

### 5.3 JEE/NEET Performance Summary

> Visible only if group has integrated coaching branches. Collapsed by default for non-integrated groups.

**Panel header:** "JEE/NEET Integrated Coaching Performance — [N] Coaching Branches"

| Column | Source Field | Sortable | Notes |
|---|---|---|---|
| Branch | `branch_name` | ▲▼ | — |
| Mock Tests This AY | `mock_count` | ▲▼ | — |
| Latest Mock Avg AIR | `latest_avg_air` | ▲▼ | Lower = better; colour: < 5k green · 5k–15k amber · > 15k red |
| JEE Target Score % | `jee_avg_pct` | ▲▼ | Based on JEE pattern questions |
| NEET Target Score % | `neet_avg_pct` | ▲▼ | Based on NEET pattern questions |
| AIR Trend | `air_trend` | ▲▼ | ↑ (improving) · ↓ (declining) |
| Actions | — | — | `[View Details]` |

### 5.4 Quick Navigation

Six tiles linking to key Division M exam analytics pages:

| Tile | Link |
|---|---|
| Exam Performance Heatmap | Page 17 |
| Topic Gap Analysis | Page 18 |
| Rank Trend Analyser | Page 13 |
| Cross-Branch Performance Hub | Page 10 |
| MIS Report Builder | Page 07 |
| Analytics Export Centre | Page 24 |

---

## 6. Drawers & Modals

### 6.1 `exam-branch-detail` Drawer — 680px, right-slide

**Trigger:** Clicking branch name in §5.1 table or `[View Details]` action.

**Header:**
```
[Branch Name] — Exam: [Exam Name]  [Date]                           [×]
[Exam Type badge]  ·  [Stream]  ·  [N] Students Appeared
Avg Score: [N]%  ·  Pass Rate: [N]%  ·  vs Group Avg: [±N]%
```

**Tab 1 — Score Summary**

Read-only cards: Avg Score, Pass Rate, Highest Score, Lowest Score, Std Deviation, Median Score.
Mini bar chart — score distribution (bands: 0–34, 35–49, 50–59, 60–69, 70–79, 80–89, 90–100).

**Tab 2 — Subject Breakdown**

Table per subject — Subject | Avg Score | Pass Rate | Highest | vs Group Avg | Gap? (badge)
Sorted by vs Group Avg ascending.

**Tab 3 — Topic Gaps**

Auto-detected topics where avg score < 50% for this branch in this exam.
Columns: Subject | Topic | Avg Score | Students Tested | Severity.

**Tab 4 — Trend**

Line chart — last 5 exams (same exam type), tracking avg score trend for this branch vs group average.

### 6.2 `gap-escalation-create` Drawer — 560px, right-slide

**Trigger:** `[+ New Gap Escalation]` header button or `[Escalate to Academic Dir]` in §5.2.

**Header:**
```
Escalate Topic / Subject Gap to Academic Director
```

| Field | Type | Required | Validation |
|---|---|---|---|
| Subject | Select | Yes | All subjects in current AY |
| Topic / Sub-topic | Text input | No | Max 200 chars; leave blank for subject-level escalation |
| Gap Severity | Select | Yes | Critical / High / Moderate |
| Branches Affected | Multi-select checkbox | Yes | All branches |
| Avg Score in Affected Branches (%) | Number input | Yes | 0–100 |
| Description | Textarea | Yes | Min 50 chars; describe the gap and its impact |
| Recommended Action | Textarea | Yes | Min 30 chars; e.g. "Additional revision classes on Organic Chemistry" |
| Urgency | Select | Yes | Standard / High / Critical |
| Attach Supporting Data | File upload | No | PDF or XLSX; max 10 MB |

**Footer:** `[Cancel]`  `[Send Escalation]`

On save: `GapEscalation` record created with `status = pending`; notification dispatched to Academic Director (Role 10, Division B) via platform notification.

### 6.3 `gap-escalation-detail` Drawer — 560px, right-slide

**Trigger:** Clicking escalation record in the escalations list.

Tabs: Overview · Subject/Topic Data · Response History

**Overview tab:** All creation fields read-only + current status badge + Academic Director response (if any) + response date.
**Subject/Topic Data tab:** Chart showing avg score trend for this topic/subject across affected branches.
**Response History tab:** Timeline of status changes and Academic Director comments.

Actions (Role 105 only): `[Mark Resolved]` · `[Re-send Reminder]` (if pending > 7 days)

### 6.4 `exam-score-export` Modal — 480px, centred

**Trigger:** `[Export Exam Report ↓]` header button.

| Field | Type | Required | Notes |
|---|---|---|---|
| Export Type | Select | Yes | Full Exam Summary / Subject Gap Report / JEE-NEET Summary / Topic Gap Register |
| Academic Year | Select | Yes | Current + previous 2 AYs |
| Branches | Multi-select | No | Default: All; can restrict to specific branches |
| Exam Type Filter | Multi-select | No | Monthly / Unit / Half-Yearly / Annual / JEE Mock / NEET Mock |
| Format | Radio | Yes | PDF · XLSX |

**Footer:** `[Cancel]`  `[Generate Export]`

---

## 7. Charts

### 7.1 Subject Performance Overview — Horizontal Bar Chart

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Subject-wise Group Average Score — [Current AY]" |
| Data | Group-wide average score per subject for current AY (most recent exam of each type) |
| Y-axis | Subject names |
| X-axis | Average score (0–100%) |
| Bar colour | Green ≥ 70% · Amber 50–69% · Red < 50% |
| Reference line | Vertical dotted line at 50% (critical threshold) and 70% (target) |
| Tooltip | "[Subject]: [N]% average · [N] branches below 50%: [list]" |
| Empty state | "No exam data available for the current academic year." |
| Export | PNG export button top-right of chart card |
| API endpoint | `GET /api/v1/group/{id}/analytics/exam/subject-averages/?ay={ay}` |
| HTMX | `<div id="chart-subject-avg" hx-get="..." hx-trigger="load" hx-swap="innerHTML" hx-indicator="#chart-subject-spinner">` |

### 7.2 Exam Performance Trend — Multi-Line Chart

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Group Average Score per Exam — [Current AY]" |
| Data | Group average score per exam event in current AY; separate lines for each major subject (Maths, Physics, Chemistry, Biology, English) |
| X-axis | Exam name + date (sorted chronologically) |
| Y-axis | Average score (%) |
| Line colours | Colorblind-safe palette; each subject a distinct colour |
| Tooltip | "[Exam] · [Date] · [Subject]: [N]%" |
| Legend | Right-side; subject names with colour dots |
| Empty state | "No exam trend data for the current academic year." |
| Export | PNG export button |
| API endpoint | `GET /api/v1/group/{id}/analytics/exam/performance-trend/?ay={ay}` |
| HTMX | `<div id="chart-exam-trend" hx-get="..." hx-trigger="load" hx-swap="innerHTML">` |

---

## 8. Toast Messages

| Action | Toast Text | Type |
|---|---|---|
| Gap escalation created | "Escalation sent to Academic Director for [Subject]. They will be notified." | Success |
| Gap escalation — Academic Dir not found | "Academic Director role not configured. Please contact Group IT Admin." | Error |
| Gap marked resolved | "Topic gap for [Subject — Topic] marked as resolved." | Success |
| Re-send reminder sent | "Reminder re-sent to Academic Director for escalation #[N]." | Success |
| Export generated | "Exam report exported to [format]. Download starting." | Success |
| Export failed | "Could not generate export. Please try again." | Error |
| Exam detail drawer — load error | "Could not load exam details. Please try again." | Error |
| KPI refresh error | "Failed to refresh KPI data." | Error |
| Escalation form — required fields | "Please complete all required fields before sending." | Error |
| Escalation form — description too short | "Description must be at least 50 characters." | Error |

---

## 9. Empty States

| Context | Icon | Heading | Sub-text | Action |
|---|---|---|---|---|
| No exams loaded this AY | `academic-cap` | "No Exam Data This Year" | "Exam results have not been loaded for this academic year. Check with Branch IT Admins." | — |
| No critical subject gaps | `check-circle` | "No Critical Subject Gaps" | "All subjects are above the 50% threshold. Keep monitoring." | — |
| No JEE/NEET coaching branches | `building-office` | "No Integrated Coaching Branches" | "This group does not have JEE/NEET integrated coaching branches configured." | — |
| No topic gap escalations | `check-circle` | "No Open Escalations" | "All topic gap escalations have been resolved or none have been raised." | — |
| Branch detail — no subject data | `table-cells` | "No Subject Data" | "Subject-level results were not uploaded for this exam at this branch." | — |
| Branch detail — no topic gap data | `magnifying-glass` | "No Topic Gaps Detected" | "No topics with average below 50% were found for this branch in this exam." | — |
| Chart — no data | `chart-bar` | "No data available" | "No exam data is available for the selected filters." | — |

---

## 10. Loader States

| Context | Loader Behaviour |
|---|---|
| Initial page load | KPI bar: 6 shimmer cards. Charts: 2 shimmer rectangles. Section 5.1 table: 6 shimmer rows. Section 5.2 panel: shimmer header + 4 rows. |
| Exam selector change | Section 5.1 table: 6 shimmer rows with 20px spinner below toolbar |
| Filter/search change | Table rows replaced by shimmer rows |
| `exam-branch-detail` drawer open | Drawer slides in; shimmer tabs + shimmer content rows |
| Tab switch in drawer | Tab content replaced by shimmer while loading |
| `[+ New Gap Escalation]` button | Drawer slides in with shimmer form skeleton until loaded |
| `[Send Escalation]` submit | Button disabled + "Sending…" + spinner; re-enables on response |
| `[Mark Resolved]` action | Button disabled + spinner |
| Export modal — `[Generate Export]` | Button disabled + "Generating…" + spinner; file downloads on ready |
| Chart initial load | Shimmer rectangle with centred spinner per chart |
| KPI auto-refresh | Cards pulse; values update in place |
| Pagination click | Table body replaced by shimmer rows |

---

## 11. Role-Based UI Visibility

| UI Element | Role 105 (Exam Analytics Officer) | All Others |
|---|---|---|
| Page | ✅ Full access | ❌ Redirected to own dashboard |
| KPI Summary Bar | ✅ All 6 cards | — |
| Charts section | ✅ Both charts | — |
| Section 5.1 (Exam Results) | ✅ Full — read-only data | — |
| Section 5.2 (Critical Subject Gaps) | ✅ Full + escalation buttons | — |
| Section 5.3 (JEE/NEET Summary) | ✅ Full (if coaching branches exist) | — |
| `[Export Exam Report ↓]` button | ✅ Visible | — |
| `[+ New Gap Escalation]` button | ✅ Visible | — |
| `[Escalate to Academic Dir]` in §5.2 | ✅ Visible | — |
| `exam-branch-detail` drawer — View | ✅ Visible | — |
| `gap-escalation-create` drawer | ✅ Full | — |
| `[Mark Resolved]` in escalation detail | ✅ Visible | — |
| `[Re-send Reminder]` in escalation detail | ✅ Visible | — |
| Alert banners | ✅ All | — |

---

## 12. API Endpoints

### 12.1 KPI Summary
```
GET /api/v1/group/{group_id}/analytics/exam/kpi/
```
Query: `academic_year` (optional, default current).
Response: `{ "exams_analysed": N, "subjects_critical": N, "branches_below_avg": N, "jee_avg_air": N, "topic_gaps": N, "escalations_pending": N }`.

### 12.2 Exam List (for selector)
```
GET /api/v1/group/{group_id}/analytics/exam/exams/
```
Query: `academic_year`, `exam_type` (monthly/unit/halfyearly/annual/jee_mock/neet_mock).
Response: `[{ "id": N, "name": "...", "date": "YYYY-MM-DD", "exam_type": "...", "results_loaded": true }]` sorted by date DESC.

### 12.3 Branch Results for Selected Exam
```
GET /api/v1/group/{group_id}/analytics/exam/exams/{exam_id}/branch-results/
```

| Query Parameter | Type | Description |
|---|---|---|
| `stream` | string | Filter by stream: `mpc`, `bipc`, `mec`, `all` |
| `zone` | string | Filter by zone ID |
| `branch_type` | string | `day`, `hostel`, `both` |
| `search` | string | Search by branch name |
| `page` | integer | Default 1 |
| `page_size` | integer | 25 · 50 · All |
| `ordering` | string | `avg_score_pct` (default ASC) · `branch_name` · `pass_rate_pct` · `subject_gaps_count` |

Response: `{ count, next, previous, results: [...], group_avg_score: N }`.

### 12.4 Critical Subject Gaps
```
GET /api/v1/group/{group_id}/analytics/exam/subject-gaps/
```
Query: `academic_year`, `stream`, `threshold` (default 50).
Response: `{ count, results: [{ subject, stream, group_avg_pct, branches_affected, worst_branch, trend, escalation_status }] }`.

### 12.5 JEE/NEET Summary
```
GET /api/v1/group/{group_id}/analytics/exam/jee-neet-summary/
```
Query: `academic_year`.
Response: `{ coaching_branches_count, results: [{ branch, mock_count, latest_avg_air, jee_avg_pct, neet_avg_pct, air_trend }] }`.

### 12.6 Exam Branch Detail
```
GET /api/v1/group/{group_id}/analytics/exam/exams/{exam_id}/branches/{branch_id}/
```
Response: Full detail object including score_summary, subject_breakdown, topic_gaps, trend_data (last 5 exams).

### 12.7 Subject Averages Chart Data
```
GET /api/v1/group/{group_id}/analytics/exam/subject-averages/
```
Query: `academic_year`.
Response: `{ labels: [...subjects], data: [...avg_scores], colours: [...hex_colours] }`.

### 12.8 Exam Performance Trend Chart Data
```
GET /api/v1/group/{group_id}/analytics/exam/performance-trend/
```
Query: `academic_year`, `subjects` (comma-separated, default: Maths,Physics,Chemistry,Biology,English).
Response: `{ labels: [...exam_names_dates], datasets: [{ subject, data: [...scores] }] }`.

### 12.9 Create Gap Escalation
```
POST /api/v1/group/{group_id}/analytics/exam/escalations/
```
Body: `{ subject, topic, severity, branches_affected, avg_score_pct, description, recommended_action, urgency, attachment_url }`. Role 105 only.
Response: 201 Created — full escalation object.

### 12.10 List Gap Escalations
```
GET /api/v1/group/{group_id}/analytics/exam/escalations/
```
Query: `status` (pending/acknowledged/resolved), `academic_year`, `severity`, `page`, `page_size`.
Response: paginated list.

### 12.11 Resolve Escalation
```
POST /api/v1/group/{group_id}/analytics/exam/escalations/{id}/resolve/
```
Body: `{ "resolution_note": "string" }`. Role 105 only.
Response: 200 OK.

### 12.12 Re-send Escalation Reminder
```
POST /api/v1/group/{group_id}/analytics/exam/escalations/{id}/remind/
```
Body: `{}`. Role 105 only; only if status = pending and last_reminded > 7 days ago.
Response: 200 OK — `{ "reminded_at": "..." }`.

### 12.13 Export
```
GET /api/v1/group/{group_id}/analytics/exam/export/
```
Query: `export_type`, `academic_year`, `branches` (comma-separated), `exam_type` (comma-separated), `format` (pdf/xlsx).
Response: File download (`Content-Disposition: attachment`).

---

## 13. HTMX Patterns

| Pattern | Trigger Element | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI bar load + auto-refresh | `<div id="exam-kpi-bar">` | GET `.../exam/kpi/` | `#exam-kpi-bar` | `innerHTML` | `hx-trigger="load, every 300s"`; shimmer on first load |
| Chart 7.1 load | `<div id="chart-subject-avg">` | GET `.../exam/subject-averages/` | `#chart-subject-avg` | `innerHTML` | `hx-trigger="load"`; spinner in chart area |
| Chart 7.2 load | `<div id="chart-exam-trend">` | GET `.../exam/performance-trend/` | `#chart-exam-trend` | `innerHTML` | `hx-trigger="load"` |
| Exam selector change | `<select id="exam-selector">` | GET `.../exams/{exam_id}/branch-results/` | `#branch-results-table` | `innerHTML` | `hx-trigger="change"`; shimmer rows during load |
| Branch results table — search | `<input id="branch-search">` | GET `.../exams/{exam_id}/branch-results/?search=` | `#branch-results-table` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Branch results table — filter | Filter chip selects | GET `.../exams/{exam_id}/branch-results/?filters=` | `#branch-results-table` | `innerHTML` | `hx-trigger="change"` |
| Branch results pagination | Pagination buttons | GET `.../exams/{exam_id}/branch-results/?page={n}` | `#branch-results-table` | `innerHTML` | `hx-trigger="click"` |
| Open branch detail drawer | Branch name / [View Details] | GET `/htmx/analytics/exam/exams/{exam_id}/branches/{branch_id}/detail/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Drawer tab switch | Tab buttons | GET `/htmx/analytics/exam/.../tab/{tab_slug}/` | `#exam-drawer-tab-content` | `innerHTML` | `hx-trigger="click"` |
| Open gap escalation drawer | `[+ New Gap Escalation]` button | GET `/htmx/analytics/exam/escalations/create/` | `#drawer-container` | `innerHTML` | `hx-trigger="click"` |
| Submit gap escalation | Escalation form | POST `.../exam/escalations/` | `#escalation-result` | `innerHTML` | `hx-encoding="multipart/form-data"`; `hx-on::after-request="showToast(event); closeDrawer();"` |
| Resolve escalation | `[Mark Resolved]` button | POST `.../escalations/{id}/resolve/` | `#escalation-status-badge-{id}` | `outerHTML` | `hx-confirm="Mark this escalation as resolved?"`; spinner on button |
| Re-send reminder | `[Re-send Reminder]` button | POST `.../escalations/{id}/remind/` | `#remind-btn-{id}` | `outerHTML` | Shows "Sent ✓" state for 3s then reverts |
| Critical gaps panel — `[Escalate]` inline | `[Escalate to Academic Dir]` button | GET `/htmx/analytics/exam/escalations/create/?subject={id}` | `#drawer-container` | `innerHTML` | Pre-fills subject in drawer |
| KPI auto-refresh | `#exam-kpi-bar` | GET `.../exam/kpi/` | `#exam-kpi-bar` | `innerHTML` | `hx-trigger="every 300s"` |

---

*Page spec version: 1.0 · Last updated: 2026-03-22*
