# 41 — Foundation Performance Tracker

> **URL:** `/group/acad/iit-foundation/performance/`
> **File:** `41-foundation-performance.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** IIT Foundation Director G3 · CAO G4 · Olympiad & Scholarship Coordinator G3 · Academic MIS Officer G1

---

## 1. Purpose

The Foundation Performance Tracker provides longitudinal per-student performance monitoring for every student in the group's Class 6–10 IIT Foundation programme. It serves two primary operational functions: identifying students who show consistent high performance (top 10% across three or more tests) for scholarship nomination, and identifying students who are struggling for early remedial intervention.

The scholarship eligibility auto-flag is the most important feature on this page. Students who consistently score in the top 10% of their class level across three or more Foundation tests are automatically flagged as scholarship-eligible. This flag is visible to the IIT Foundation Director and the Olympiad & Scholarship Coordinator, who can then nominate them for internal merit scholarships through the Div-C flow. The threshold is three tests to prevent a single outlier performance from triggering a nomination — sustained excellence, not a lucky test day, is the criterion.

For the IIT Foundation Director, this tracker also serves as an early identification pipeline for future JEE/NEET coaching intake. A student who ranks consistently in the top 5% of their class in Class 8 and Class 9 Foundation is a strong candidate for the intensive coaching programme in Class 11. This tracker makes that identification systematic rather than dependent on individual teacher memory or branch-level reporting, which is unreliable across 50 branches.

---

## 2. Role Access

| Role | Level | Can View | Can Act | Notes |
|---|---|---|---|---|
| Chief Academic Officer (CAO) | G4 | ✅ All classes, all branches | ✅ View · Export · Approve nominations | Full visibility |
| Group Academic Director | G3 | ✅ All classes | ❌ | Read-only |
| Group Curriculum Coordinator | G2 | ❌ | ❌ | No access |
| Group Exam Controller | G3 | ❌ | ❌ | No access |
| Group Results Coordinator | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MPC | G3 | ✅ Class 9–10 (pipeline) | ❌ | Read-only |
| Group Stream Coord — BiPC | G3 | ❌ | ❌ | No access |
| Group Stream Coord — MEC/CEC | G3 | ❌ | ❌ | No access |
| Group JEE/NEET Integration Head | G3 | ✅ Class 9–10 (pipeline awareness) | ❌ | Read-only |
| Group IIT Foundation Director | G3 | ✅ All classes, all branches | ✅ Full — view · export · nominate · flag | Primary operator |
| Group Olympiad & Scholarship Coord | G3 | ✅ All classes (scholarship eligibility) | ✅ View · Nominate for Scholarship | Scholarship-specific access |
| Group Special Education Coordinator | G3 | ❌ | ❌ | No access |
| Group Academic MIS Officer | G1 | ✅ All classes | ✅ Export only | Read-only |
| Group Academic Calendar Manager | G3 | ❌ | ❌ | No access |

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic  ›  IIT Foundation  ›  Performance Tracker
```

### 3.2 Page Header
```
Foundation Performance Tracker                      [Export XLSX ↓]  [Export Scholarship List ↓]
[Group Name] · Academic Year [YYYY–YY]
```

### 3.3 Class Filter Tabs

Six tabs: **All Classes** · **Class 6** · **Class 7** · **Class 8** · **Class 9** · **Class 10**

Selecting a class tab filters the main student table to that class. "All Classes" shows all Foundation students.

### 3.4 Summary Stats Bar (all classes or selected class)

| Stat | Value |
|---|---|
| Total Foundation Students (Tracked) | 14,320 |
| Students with 3+ Tests | 11,840 |
| Scholarship Eligible (Top 10%, 3+ Tests) | 342 |
| Already Nominated | 118 |
| Pending Nomination | 224 |
| Improving Trend | 5,240 (44.3%) |
| Declining Trend | 1,180 (10.0%) |

**Scholarship alert banner (if eligible students > 0 and pending nomination > 0):**
> "224 students are scholarship-eligible but not yet nominated. Review and nominate."
> [View Eligible Students →] — filters table to scholarship eligible, not yet nominated

---

## 4. Main Content

### 4.1 Search / Filters / Table

**Search:** Student name or roll number — 300ms debounce.

**Advanced Filters:**

| Filter | Type | Options |
|---|---|---|
| Class | Multi-select | Class 6 · 7 · 8 · 9 · 10 |
| Branch | Multi-select | All 50 branches |
| Improvement Trend | Multi-select | Improving · Stable · Declining · Insufficient Data |
| Scholarship Eligibility | Select | Eligible (Top 10%, 3+ tests) · Not Eligible · Nominated · Awarded |
| Tests Completed | Select | 1+ · 3+ · 5+ |
| Percentile Band (Latest Test) | Select | Top 10% · 10–25% · 25–50% · Bottom 50% |

Active filter chips: Dismissible, "Clear All" link, count badge.

### 4.2 Columns

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Roll Number | Text | ✅ | |
| Student Name | Text | ✅ | |
| Branch | Text | ✅ | Name + code |
| Class | Badge | ✅ | Class 6–10 |
| Tests Taken | Number | ✅ | Total Foundation tests sat |
| Avg Score | Number | ✅ | Avg marks across all tests |
| Avg % | Number | ✅ | Avg percentage |
| Latest Percentile | Number | ✅ | Percentile within class (1 decimal) |
| Improvement Trend | Badge | ✅ | Improving (↑) · Stable (→) · Declining (↓) · Insufficient Data |
| Scholarship Eligible | Badge | ✅ | Eligible (green) · Not Eligible (grey) · Nominated (blue) · Awarded (gold) |
| Actions | — | ❌ | See row actions |

**Scholarship Eligible badge logic:**
- **Eligible:** Student has 3+ tests, appears in top 10% of their class group for all 3+ tests
- **Not Eligible:** Does not meet both criteria yet
- **Nominated:** Eligible and nomination submitted to Div-C
- **Awarded:** Scholarship granted by Div-C

**Scholarship Eligible rows:** Rows with "Eligible" badge have a subtle green left border — `border-l-4 border-green-400` — to draw attention without overwhelming.

**Default sort:** Scholarship Eligible (Eligible first, then Nominated) → Latest Percentile descending.

**Pagination:** Server-side · Default 50/page · Selector 25/50/100.

### 4.3 Row Actions

| Action | Icon | Visible To | Opens | Notes |
|---|---|---|---|---|
| View Student Detail | Eye | All with access | `student-detail` drawer 480px | Full test history + trends |
| Nominate for Scholarship | Award | Foundation Dir · Olympiad Coord · CAO | `nominate-scholarship` modal 460px | Only for Eligible students |
| Flag for Academic Review | Flag | Foundation Dir · CAO | Confirm modal 380px | For struggling students |

### 4.4 Bulk Actions

| Action | Visible To | Notes |
|---|---|---|
| Export Selected (XLSX) | Foundation Dir · CAO · MIS | Student performance export |
| Nominate Selected for Scholarship | Foundation Dir · Olympiad Coord · CAO | Batch nomination for eligible students |
| Export Scholarship List (PDF) | Foundation Dir · Olympiad Coord · CAO | Formatted list for scholarship review committee |
| Flag Selected for Academic Review | Foundation Dir · CAO | Batch flag for struggling students |

---

## 5. Drawers & Modals

### 5.1 Drawer: `student-detail`
- **Trigger:** Eye icon row action or student name click
- **Width:** 480px
- **Tabs:** Test History · Subject Breakdown · Trend Chart

#### Tab: Test History
Table: Test # · Test Name · Class · Date · Score · Max Marks · % · Percentile · Class Rank

Sorted: newest first.

Summary row: Best result · Worst result · Avg % · Total tests · Tests in top 10%: N / Total.

**Scholarship eligibility indicator:** Below summary —
- "This student appears in the top 10% for [N] of [Total] tests."
- If N ≥ 3: Green badge "Scholarship Eligible" + [Nominate →] button (authorised roles)
- If N < 3: Grey badge "Not Yet Eligible — needs top 10% in [3-N] more tests"

#### Tab: Subject Breakdown
For each subject in the Foundation programme for this class:
| Metric | Value |
|---|---|
| Subject | Maths · Physics · Chemistry |
| Avg Score | X / Max |
| Avg % | |
| Tests Included | Count |
| Best Subject | Auto-calculated |
| Weakest Subject | Auto-calculated |

Mini radar chart: Subject performance vs class average — same colours as page 37 (student vs group).

#### Tab: Trend Chart
- **Type:** Line chart
- **X-axis:** Foundation test sequence (chronological)
- **Y-axis:** Percentile (within class level)
- **Line:** Student's percentile per test
- **Reference band:** Top 10% threshold line (dashed green) · Class average (dashed grey)
- **Tooltip:** Test # · Date · Percentile · Class rank
- **Annotation:** If student has been consistently above top 10% for 3+ tests, a badge/annotation: "Scholarship Eligible — sustained top 10%"

---

### 5.2 Modal: `nominate-scholarship`
- **Trigger:** "Nominate for Scholarship" row action or button in student detail drawer
- **Width:** 460px
- **Title:** "Nominate [Student Name] for Foundation Merit Scholarship"
- **Content:**
  - Student summary: Name · Roll · Class · Branch · Tests in Top 10%: N
  - Auto-evidence: "Top 10% in [N] Foundation tests — Class [X] — [Academic Year]"
  - Scholarship scheme: Select from Div-C schemes accepting Foundation nominations
  - Scholarship type: Merit (auto-selected for Foundation)
  - Basis for nomination: Pre-filled "Consistent top 10% performance across [N] Foundation tests in Class [X]" — editable
  - Attachments: Optional — download student's test history report [Download PDF] + attach
- **Buttons:** [Submit Nomination to Div-C] (primary) + [Cancel]
- **On confirm:** Nomination submitted to Div-C Group Scholarship Manager · Scholarship Eligible badge updated to "Nominated" · Toast shown

---

### 5.3 Modal: `flag-academic-review`
- **Trigger:** "Flag for Academic Review" row action
- **Width:** 380px
- **Title:** "Flag [Student Name] for Academic Review"
- **Content:**
  - "This student will be flagged for academic review at the branch level."
  - Performance summary shown
  - Reason: Textarea (required, min 20 chars) — e.g. "Declining trend for 4 consecutive tests — consider remedial support"
  - Notify branch Foundation coordinator: Toggle (default on)
- **Buttons:** [Flag for Review] (amber) + [Cancel]

---

### 5.4 Modal: `bulk-nominate-confirm`
- **Width:** 480px
- **Title:** "Bulk Scholarship Nomination — [N] Students"
- **Content:** Scrollable list of selected students with Name · Class · Branch · Tests in Top 10%: N
- **Scholarship scheme:** Single selector applies to all
- **Batch note:** Required, min 30 chars
- **Note:** "Only students with 3+ top-10% test results are eligible. [M] of your selected students meet this criteria."
- **Non-eligible note:** "The remaining [N-M] students will be excluded from this batch nomination."
- **Buttons:** [Nominate [M] Eligible Students] + [Cancel]

---

## 6. Charts

### 6.1 Scholarship Eligibility Funnel (Horizontal Stacked Bar)
- **Type:** Horizontal stacked bar
- **Y-axis:** Class levels (Class 6–10)
- **X-axis:** Student count
- **Stacks per class:** Eligible (green) · Nominated (blue) · Awarded (gold) · Not Eligible (grey)
- **Tooltip:** Class · Eligible: N · Nominated: N · Awarded: N
- **Export:** PNG
- **Shown:** Above main table in "Scholarship Pipeline" collapsible card

### 6.2 Foundation Rank Trend by Class (Multi-line)
- **Type:** Multi-line chart
- **X-axis:** Test sequence (1 through N)
- **Y-axis:** Class-level group average % (0–100%)
- **Lines:** Class 6 · 7 · 8 · 9 · 10 — 5 distinct colours + dash patterns
- **Tooltip:** Test # · Class · Avg %
- **Purpose:** Shows whether the programme is improving group performance over the series for each class
- **Export:** PNG
- **Shown:** In "Group Performance" collapsible card

### 6.3 Improvement vs Declining Distribution (Donut — per class tab)
- **Type:** Donut chart
- **Segments:** Improving (green) · Stable (blue) · Declining (red) · Insufficient Data (grey)
- **Centre text:** Total tracked students for selected class
- **Tooltip:** Segment · Count · %
- **Export:** PNG

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Scholarship nomination submitted | "Nomination for [Student Name] submitted to Div-C. Scholarship badge updated." | Success | 5s |
| Student flagged for review | "[Student Name] flagged for academic review. Branch coordinator notified." | Warning | 5s |
| Bulk nomination submitted | "[N] Foundation scholarship nominations submitted to Div-C." | Success | 5s |
| Non-eligible in bulk | "[M] of [N] selected students were ineligible and excluded from batch nomination." | Warning | 6s |
| XLSX export started | "Performance data XLSX preparing." | Info | 4s |
| Scholarship list PDF started | "Scholarship list PDF preparing — download will begin shortly." | Info | 4s |

---

## 8. Empty States

| Condition | Heading | Description | CTA |
|---|---|---|---|
| No Foundation students | "No Foundation Students Tracked" | "No students are currently enrolled in the Foundation programme" | [Manage Foundation Programme →] |
| No tests completed | "Awaiting Test Data" | "Student performance data will appear after the first Foundation test results are published" | — |
| No students match filters | "No Students Match" | "Try adjusting your filters or search term" | [Clear Filters] |
| No scholarship-eligible students | "No Eligible Students Yet" | "No students have achieved top 10% in 3 or more tests yet for this class" | — |
| Class tab — no students | "No Students for Class [N]" | "No Foundation students are enrolled at Class [N] yet" | [Manage Foundation Programme →] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton: stats bar + scholarship alert banner placeholder + table (10 rows) |
| Class tab switch | Inline table skeleton rows (10) + stats bar shimmer |
| Filter/search/sort/page | Inline skeleton rows (10) |
| Student detail drawer open | Spinner in drawer body + skeleton tabs |
| Trend chart in drawer | Spinner in chart area |
| Nomination submit | Spinner inside [Submit Nomination] + button disabled |
| Charts (funnel / group trend / donut) | Spinner centred in chart card |
| Export triggers | Spinner in export button (momentary) |

---

## 10. Role-Based UI Visibility

| Element | Foundation Dir G3 | CAO G4 | Olympiad Coord G3 | MIS G1 |
|---|---|---|---|---|
| Scholarship alert banner | ✅ | ✅ | ✅ | ✅ (count only) |
| Nominate for Scholarship action | ✅ | ✅ | ✅ | ❌ |
| Bulk Nominate | ✅ | ✅ | ✅ | ❌ |
| Flag for Academic Review | ✅ | ✅ | ❌ | ❌ |
| Scholarship Eligible badge in table | ✅ | ✅ | ✅ | ✅ |
| Export XLSX | ✅ | ✅ | ❌ | ✅ |
| Export Scholarship List PDF | ✅ | ✅ | ✅ | ❌ |
| Scholarship Eligibility tab in drawer | ✅ | ✅ | ✅ | ❌ |
| Trend chart in drawer | ✅ | ✅ | ✅ | ❌ |
| Scholarship Funnel chart | ✅ | ✅ | ✅ | ✅ |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/` | JWT | Student performance list |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/stats/` | JWT | Summary stats bar + scholarship counts |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/` | JWT | Student detail — all tabs |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/history/` | JWT | Test history tab |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/subject/` | JWT | Subject breakdown + radar chart data |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/trend/` | JWT | Trend chart data |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/nominate/` | JWT (Foundation Dir / Olympiad Coord / CAO) | Submit scholarship nomination |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/performance/bulk-nominate/` | JWT (Foundation Dir / Olympiad Coord / CAO) | Bulk scholarship nomination |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/performance/{student_id}/flag-review/` | JWT (Foundation Dir / CAO) | Flag for academic review |
| POST | `/api/v1/group/{group_id}/acad/iit-foundation/performance/bulk-flag-review/` | JWT (Foundation Dir / CAO) | Bulk flag for review |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/export/?format=xlsx` | JWT | Export XLSX |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/export/scholarship-list/?format=pdf` | JWT (Foundation Dir / Olympiad Coord / CAO) | Scholarship list PDF |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/charts/scholarship-funnel/` | JWT | Scholarship funnel stacked bar |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/charts/rank-trend/` | JWT | Group avg trend multi-line |
| GET | `/api/v1/group/{group_id}/acad/iit-foundation/performance/charts/trend-distribution/` | JWT | Improving/Declining/Stable donut |

Query params: `class_level`, `branch_ids`, `trend`, `scholarship_eligibility`, `min_tests`, `percentile_band`, `q`, `sort`, `page`.

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| Class tab switch | `click` | GET `.../performance/?class_level=` | `#foundation-perf-section` | `innerHTML` |
| Student search | `input delay:300ms` | GET `.../performance/?q=&class_level=` | `#perf-table-body` | `innerHTML` |
| Filter apply | `click` | GET `.../performance/?filters=` | `#perf-table-section` | `innerHTML` |
| Sort / paginate | `click` | GET `.../performance/?sort=&page=&class_level=` | `#perf-table-section` | `innerHTML` |
| Student detail drawer open | `click` | GET `.../performance/{id}/` | `#drawer-body` | `innerHTML` |
| Drawer tab switch | `click` | GET `.../performance/{id}/history/` or `.../subject/` or `.../trend/` | `#student-detail-tab-content` | `innerHTML` |
| Scholarship alert quick filter | `click` | GET `.../performance/?scholarship_eligibility=eligible&nomination=pending` | `#perf-table-section` | `innerHTML` |
| Nominate submit | `click` | POST `.../performance/{id}/nominate/` | `#student-row-{id}` | `outerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
