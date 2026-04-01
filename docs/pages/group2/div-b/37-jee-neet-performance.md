# 37 — JEE/NEET Performance Tracker

> **URL:** `/group/acad/jee-neet/performance/`
> **File:** `37-jee-neet-performance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** JEE/NEET Integration Head G3 · CAO G4 · Academic Director G3 · Academic MIS Officer G1

---

## 1. Purpose

The JEE/NEET Performance Tracker is a per-student longitudinal performance monitoring system for every student enrolled in the group's Integrated JEE or Integrated NEET coaching programmes. Unlike the test series manager, which tracks tests as events, this page tracks students as subjects — showing how each individual's performance evolves across the full series from the first mock to the most recent.

The critical operational purpose of this tracker is early identification of declining students. A student who shows a downward trend across three or more consecutive tests is automatically flagged with a "Declining Trend" alert. These students are at risk of demoralisation, parent anxiety, or coaching programme dropout — all of which are commercially and academically harmful to the group. The JEE/NEET Integration Head uses this alert list as the primary input for weekly intervention reviews: which students need counselling, which need a different batch placement, and which need remedial focus on specific subjects.

The AIR (All India Rank) estimate per student is calculated from the student's percentile position within the mock cohort, mapped to national JEE/NEET rank distributions. These estimates become more accurate as more official tests are included in the series. They are displayed with appropriate disclaimers — the estimates are directional, not definitive — but they give students and parents a meaningful progress indicator that is specific to JEE/NEET preparation rather than just raw marks.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All students, all branches | ✅ View · Export | Read with export authority |
| Group Academic Director | G3 | ✅ All students, all branches | ✅ View · Export | Full read access |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ✅ All students | ❌ | Read-only reference |
| Group Stream Coord — MPC | G3 | ✅ JEE students only | ❌ | Filtered to JEE stream |
| Group Stream Coord — BiPC | G3 | ✅ NEET students only | ❌ | Filtered to NEET stream |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ All students, all branches | ✅ Full — view · export · act on alerts | Primary operator |
| Group IIT Foundation Director | G3 | ❌ | ❌ | No access |
| Group Olympiad & Scholarship Coord | G3 | ❌ | ❌ | No access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All students | ✅ Export only | Read-only — all data |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  JEE/NEET  ›  Performance Tracker
```

### 3.2 Page Header
```
JEE/NEET Performance Tracker                        [Export XLSX ↓]  [Export Alerts PDF ↓]
[Group Name] · Academic Year [YYYY–YY] · [JEE | NEET] toggle
```

**JEE / NEET toggle:** Switches the entire page between JEE performance view and NEET performance view. Default: JEE.

### 3.3 Summary Stats Bar

| Stat (JEE view) | Value |
|---|---|
| Total JEE Students | 6,240 |
| Students — 3+ Tests Completed | 5,870 |
| Improving Trend | 2,340 (39.9%) |
| Stable | 1,960 (33.4%) |
| Declining Trend (3+ tests) | 580 (9.9%) |
| Avg Percentile (Latest Test) | 62.4 |
| Est. AIR Median | ~28,500 |

**Alert banner (shown when declining trend students > 0):**
> "580 students showing declining trend for 3+ consecutive tests. Review required."
> [View Declining Students →] — filters table to declining trend only

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Student name or roll number — 300ms debounce, highlights match in Name column.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select | All 50 branches |
| Class | Multi-select | Class 11 · Class 12 |
| Improvement Trend | Multi-select | Improving · Stable · Declining · Insufficient Data (fewer than 3 tests) |
| Percentile Band | Select | P90+ (Excellent) · P75–90 (Good) · P50–75 (Average) · Below P50 (Needs Support) |
| Tests Completed | Select | 1+ tests · 3+ tests · 5+ tests · All tests |
| AIR Estimate Band | Select | Under 10,000 · 10,000–30,000 · 30,000–1,00,000 · Over 1,00,000 |
| Alert Status | Checkbox | Show only students with declining trend alert |

Active filter chips: Dismissible, "Clear All" link, count badge.

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Roll Number | Text | ✅ | |
| Student Name | Text | ✅ | |
| Branch | Text | ✅ | Name + code |
| Class | Text | ✅ | Class 11 / 12 |
| Tests Completed | Number | ✅ | Count of tests taken in current series |
| Latest Percentile | Number | ✅ | Percentile in most recent test (1 decimal) |
| Avg Score | Number | ✅ | Average marks across all completed tests |
| AIR Estimate | Text | ✅ | e.g. ~22,000–26,000 (range, not single number) |
| Trend | Badge | ✅ | Improving (green ↑) · Stable (blue →) · Declining (red ↓) · Insufficient Data (grey ?) |
| Trend Streak | Number | ✅ | Number of consecutive tests in current trend direction |
| Last Test | Date | ✅ | Date of most recent test |
| Alert | Badge | ❌ | "Declining 3+" red badge — shown only when applicable |
| Actions | — | ❌ | See row actions |

**Declining trend alert row highlight:** Rows with "Declining 3+" badge have a light red row background `bg-red-50`.

**Default sort:** Alert status first (declining trend students), then Trend streak descending within alert group, then Latest Percentile ascending.

**Pagination:** Server-side · Default 50/page · Selector 25/50/100.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Student Detail | Eye | All with access | `student-detail` drawer 560px | Full test history + subject breakdown |
| Flag for Counselling | Flag | JEE/NEET Head · CAO | Confirm modal 380px | Logs counselling referral |
| Send Progress Update (to Branch) | Mail | JEE/NEET Head · CAO | `progress-update` modal 420px | Sends report to branch coaching coordinator |

### 4.4 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | JEE/NEET Head · CAO · MIS · Academic Dir | Student performance data for selected rows |
| Flag Selected for Counselling | JEE/NEET Head · CAO | Batch counselling flag |
| Export Declining Alerts (PDF) | JEE/NEET Head · CAO | Alert report for weekly intervention review |

---

## 5. Drawers & Modals

### 5.1 Drawer: `student-detail`
- **Trigger:** Eye icon row action or click student name
- **Width:** 560px
- **Tabs:** All Tests History · Subject-wise · Weak Topics · AIR Trend

#### Tab: All Tests History
Table: Test # · Test Name · Test Date · Score · Max · % · Percentile · Rank in Group (for that test) · Trend from previous

Sorted: newest first.

Mini summary: Best test · Worst test · Average across all tests · Total tests taken.

#### Tab: Subject-wise

For JEE: Physics · Chemistry · Mathematics — each subject as a column.
For NEET: Physics · Chemistry · Botany · Zoology — each subject as a column.

Table rows: One per test. Columns: Test # · Date · Physics score · Chemistry score · [Maths/Bio] score.

Bottom row: Average per subject.

**Subject radar chart:** Hexagonal radar — one axis per subject — plots this student's average performance vs group average. Coloured fills: blue (student) · grey dashed (group avg). Shows instantly which subjects are strong or weak relative to peers.

#### Tab: Weak Topics
Auto-generated from question-level performance across all tests:

Table: Subject · Topic · Questions Attempted · Avg Marks % · vs Group Avg % · Appeared in N tests

Sorted: Weakest first (lowest Avg Marks %).

Actionable suggestion (auto-generated): "This student struggles with [Topic] in [Subject]. Review study material from the Content Library." — with [View Library Resources →] link.

#### Tab: AIR Trend
Line chart: X-axis = Test sequence · Y-axis = Estimated AIR (inverted — lower = better)

Data points: One per test. Each point shows estimated AIR at that point in the series.

Trend line (regression): Shows overall direction — improving, stable, or declining.

**Declining trend alert rendering (if applicable):**
Red alert box at top of this tab: "This student has shown a declining AIR trend for [N] consecutive tests. Consider counselling or batch reassignment."

Disclaimer below chart: "AIR estimates are approximations based on this group's mock cohort percentile position. Actual JEE/NEET AIR will differ based on national competition."

---

### 5.2 Modal: `flag-counselling-confirm`
- **Trigger:** "Flag for Counselling" row action
- **Width:** 380px
- **Title:** "Flag [Student Name] for Counselling"
- **Content:**
  - Student summary: Branch · Class · Latest Percentile · Trend (Declining — N tests)
  - Counselling reason: Auto-filled "Declining trend for [N] consecutive JEE/NEET tests" — editable
  - Notify: Branch coaching coordinator (checkbox, default on) · Branch principal (checkbox, default off)
- **Buttons:** [Flag for Counselling] (amber warning) + [Cancel]
- **On confirm:** Counselling referral logged in system · Branch coordinator notified (if selected) · Student marked as "Flagged for Counselling" in tracker

---

### 5.3 Modal: `progress-update`
- **Trigger:** "Send Progress Update" row action
- **Width:** 420px
- **Title:** "Send Progress Update — [Student Name]"
- **Content:**
  - Recipient: Branch Coaching Coordinator (pre-filled, editable)
  - Progress summary auto-generated:
    > "Student: [Name] | Roll: [N] | Class: [N] | Tests: [N] | Avg %: [N] | Trend: Declining/Stable/Improving | Latest AIR Estimate: [Range]"
  - Additional notes field (optional)
  - Send via: WhatsApp (default on) · Email (default on)
- **Buttons:** [Send Update] + [Cancel]

---

## 6. Charts

### 6.1 Group Percentile Trend — All Students (Area Line)
- **Type:** Area line chart
- **X-axis:** Test numbers in series (JEE-01 through JEE-10 / NEET-01 through NEET-08)
- **Y-axis:** Group average percentile
- **Areas (stacked):** P90+ (dark green) · P75–90 (green) · P50–75 (blue) · Below P50 (amber/red)
- **Tooltip:** Test # · Date · Count in each percentile band · Group avg percentile
- **Purpose:** Shows how the overall distribution of the cohort shifts as the series progresses
- **Export:** PNG
- **Shown:** Above main table in "Cohort Trend" collapsible card

### 6.2 Improving vs Declining vs Stable (Donut)
- **Type:** Donut chart
- **Segments:** Improving (green) · Stable (blue) · Declining (red) · Insufficient Data (grey)
- **Centre text:** Total students tracked
- **Tooltip:** Segment · Count · %
- **Export:** PNG
- **Shown:** Alongside stats bar

### 6.3 Per-Student Radar (Subject-wise) — in drawer
- Described in student-detail drawer above — Tab: Subject-wise

### 6.4 AIR Trend Line — in drawer
- Described in student-detail drawer above — Tab: AIR Trend

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Student flagged for counselling | "[Student Name] flagged for counselling. Branch coordinator notified." | Warning | 5s |
| Progress update sent | "Progress update for [Student Name] sent to [Branch Coordinator Name]." | Success | 4s |
| XLSX export started | "Student performance XLSX preparing — download will begin shortly." | Info | 4s |
| Alerts PDF export started | "Declining trend alert report preparing — download will begin shortly." | Info | 4s |
| Bulk counselling flag | "[N] students flagged for counselling. Branch coordinators notified." | Warning | 5s |
| No students in alert filter | "No students currently showing a declining trend." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No coaching students | "No Students Enrolled" | "No students are currently enrolled in the JEE/NEET coaching programme" | [Manage Test Series →] |
| No tests completed | "Awaiting First Test" | "Student performance data will appear after the first mock test results are published" | — |
| No students match filters | "No Students Match" | "Try adjusting your filters or search term" | [Clear Filters] |
| No declining students | "No Declining Trends" | "All tracked students are improving or stable — no alerts to action" | — |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + alert banner (conditional) + table (10 skeleton rows) |
| JEE/NEET toggle switch | Full page body skeleton reload |
| Table filter/search/sort/page | Inline skeleton rows (10) |
| Student detail drawer open | Spinner in drawer body + skeleton tabs |
| Drawer tab switch | Spinner in tab content area |
| Charts (cohort trend / donut) | Spinner centred in chart card |
| Export triggers | Spinner in respective export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | JEE/NEET Head G3 | CAO G4 | Academic Dir G3 | Stream Coords G3 | MIS G1 |
|---|---|---|---|---|---|
| Alert banner | ✅ | ✅ | ✅ | ✅ (own stream) | ✅ |
| Flag for Counselling action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Send Progress Update action | ✅ | ✅ | ❌ | ❌ | ❌ |
| Bulk Counselling Flag | ✅ | ✅ | ❌ | ❌ | ❌ |
| Export XLSX | ✅ | ✅ | ✅ | ❌ | ✅ |
| Export Alerts PDF | ✅ | ✅ | ✅ | ❌ | ✅ |
| AIR Estimate column | ✅ | ✅ | ✅ | ✅ | ✅ |
| Weak Topics tab in drawer | ✅ | ✅ | ✅ | ✅ | ❌ |
| Student name (full) | ✅ | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/` | JWT | Student performance list (filtered/sorted/paginated) |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/stats/` | JWT | Summary stats bar + alert count |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/` | JWT | Student detail drawer — all tabs data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/history/` | JWT | All tests history tab |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/subject-wise/` | JWT | Subject-wise tab + radar chart data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/weak-topics/` | JWT | Weak topics tab |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/air-trend/` | JWT | AIR trend chart data |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/flag-counselling/` | JWT (JEE/NEET Head / CAO) | Flag student for counselling |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/performance/{student_id}/send-progress/` | JWT (JEE/NEET Head / CAO) | Send progress update to branch |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/performance/bulk-flag-counselling/` | JWT (JEE/NEET Head / CAO) | Bulk counselling flag |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/export/?format=xlsx` | JWT | Export student performance XLSX |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/export/alerts/?format=pdf` | JWT | Export declining trend alert PDF |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/charts/cohort-trend/` | JWT | Cohort percentile trend area chart |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/performance/charts/trend-distribution/` | JWT | Improving/Declining/Stable donut chart |

Query params for main list: `type` (jee/neet), `branch_ids`, `class_level`, `trend`, `percentile_band`, `min_tests`, `air_band`, `alert_only`, `q` (search), `sort`, `page`, `page_size`.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| JEE/NEET toggle | `click` | GET `.../performance/?type=jee` or `?type=neet` | `#performance-page-body` | `innerHTML` |
| Student search | `input delay:300ms` | GET `.../performance/?q=&type=` | `#performance-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../performance/?filters=&type=` | `#performance-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../performance/?sort=&page=&type=` | `#performance-table-section` | `innerHTML` |
| Student detail drawer open | `click` | GET `.../performance/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../performance/{id}/history/` or `.../subject-wise/` etc. | `#student-detail-tab-content` | `innerHTML` |
| Flag counselling confirm | `click` | POST `.../performance/{id}/flag-counselling/` | `#student-row-{id}` | `outerHTML` |
| Alert banner quick filter | `click` | GET `.../performance/?alert_only=true&type=` | `#performance-table-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
