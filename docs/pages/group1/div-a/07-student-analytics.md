# div-a-07 — Student Analytics

## 1. Platform Scale Reference

| Dimension | Value |
|---|---|
| Total students | 2.4M–7.6M enrolled |
| Active students (last 30d) | ~1.2M–3.8M |
| Exams taken/day (platform) | ~50,000–200,000 |
| Avg exams per student/month | ~3–8 |
| Coaching centre students | 1M (highest engagement) |
| School students | 1M–5M (largest volume) |
| Peak concurrent students | 500,000 |
| Student data retention | 7 years |

**Why this matters:** Student Analytics is the product health page from the learner's perspective. The COO watches engagement velocity (are students coming back?), the CEO watches NPS/satisfaction, and the data team watches score distribution and drop-off. At 2.4M+ students, this is a big-data page — all aggregates must be pre-computed.

---

## 2. Page Metadata

| Field | Value |
|---|---|
| Page title | Student Analytics |
| Route | `/exec/student-analytics/` |
| Django view | `StudentAnalyticsView` |
| Template | `exec/student_analytics.html` |
| Priority | P1 |
| Nav group | Analytics |
| Required role | `exec`, `superadmin` |
| 2FA required | No |
| HTMX poll | KPI strip: every 60s |
| Cache | All aggregates Redis TTL 60s; Celery refresh every 60s |

---

## 3. Wireframe

```
┌──────────────────────────────────────────────────────────────────────────────┐
│ HEADER: Student Analytics                        [Export ▾] [Date Range ▾]  │
├───────┬────────┬──────────┬────────┬──────────┬─────────────────────────────┤
│ Total │ Active │ Exams    │ Avg    │ DAU /    │  Engagement                 │
│ Enrol │ (30d)  │ Today    │ Score  │ MAU      │  Score                      │
│ 2.4M  │ 1.2M   │ 84,300   │ 67.4%  │  38%     │  74 / 100                   │
├───────┴────────┴──────────┴────────┴──────────┴─────────────────────────────┤
│ TABS: [Engagement] [Score Distribution] [Cohort Analysis] [Leaderboard]     │
│       [Retention] [Drop-off Analysis]                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│ [Institution Type ▾] [State ▾] [Grade ▾] [Subject ▾] [Date Range ▾]        │
├──────────────────────────────────────────────────────────────────────────────┤
│ TAB: ENGAGEMENT                                                              │
│ ┌────────────────────────────────┐ ┌──────────────────────────────────────┐ │
│ │ Daily Active Students (line)   │ │ Exam Attempts per Student (histogram)│ │
│ └────────────────────────────────┘ └──────────────────────────────────────┘ │
│ ┌────────────────────────────────┐ ┌──────────────────────────────────────┐ │
│ │ Session Duration Distribution  │ │ Peak Hours Heatmap (24h × 7d)        │ │
│ └────────────────────────────────┘ └──────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## 4. Sections — Deep Specification

### 4.1 KPI Strip

**Container:** `flex gap-4 p-4` · 6 cards · poll every 60s with pause guard

| # | Card | Format | Alert |
|---|---|---|---|
| 1 | Total Enrolled | `2.4M` (formatted) · `data-count-up` | — |
| 2 | Active (30d) | `1.2M` + % of total `(50%)` | < 30% = amber |
| 3 | Exams Today | `84,300` · delta vs yesterday | — |
| 4 | Avg Score | `67.4%` · delta vs last 30d | — |
| 5 | DAU / MAU | `38%` engagement ratio | < 20% = amber |
| 6 | Engagement Score | `74 / 100` · composite metric | < 60 = red |

**Count-up animation:** `requestAnimationFrame` 600ms · runs once on first load · guarded by `data-animated="true"`

---

### 4.2 Global Filter Bar

`id="student-filters"` · `flex flex-wrap gap-3 p-4 border-b border-[#1E2D4A]`
All filters trigger `hx-get="?part={active_tab}"` on change · `hx-include="#student-filters"`

| Filter | Type | Options |
|---|---|---|
| Institution Type | Multi-select | All / School / College / Coaching / Group |
| State | Searchable multi-select | 28 states + All |
| Grade | Multi-select | Class 6–12 / Undergraduate / Postgraduate |
| Subject | Searchable multi-select | Maths / Physics / Chemistry / Biology / etc. |
| Date Range | Dropdown + custom | Last 7d / 30d / 90d / 6M / 1Y / Custom |

**Active filter chips:** row below filter bar · same pattern as div-a-04 §4.3.1

---

### 4.3 Tab: Engagement

`id="tab-engagement"` · `hx-get="?part=engagement"`

**2×2 chart grid:** `grid grid-cols-2 gap-4 p-4`

#### 4.3.1 Daily Active Students (top-left)

**Chart:** Line · Chart.js · Canvas height 220px
**Series:**
- DAU: `#6366F1` line
- 7-day rolling avg: `#818CF8` dashed `borderDash: [5,5]`
- 30-day rolling avg: `#475569` dashed
**X-axis:** daily dates for selected range
**Y-axis:** student count (formatted with K/M suffix)
**Annotations:** vertical dashed line at peak day with label
**Tooltip:** date + DAU count + delta vs prior day + rolling avgs

#### 4.3.2 Exam Attempts Distribution (top-right)

**Chart:** Histogram (bar) · bins: 0 / 1 / 2–5 / 6–10 / 11–20 / 20+ exams per student in period
**Bar colour:** `#22D3EE`
**Y-axis:** student count
**Tooltip:** bin range + count + % of total
**Click bar:** filters table in §4.3.5 to show students in that bucket

#### 4.3.3 Session Duration Distribution (bottom-left)

**Chart:** Horizontal bar histogram
**Bins:** < 5 min / 5–15 min / 15–30 min / 30–60 min / > 60 min
**Colours:** gradient `#6366F1` → `#22D3EE` (5 stops)
**Tooltip:** duration range + student count + avg score in that session length bucket

#### 4.3.4 Peak Hours Heatmap (bottom-right)

**Rows:** 7 days (Mon–Sun)
**Columns:** 24 hours (0–23)
**Cell colour:** `#1E2D4A` (0) → `#6366F1` (max) · 6-step gradient
**Cell size:** `~28px × 28px` · `text-[10px] font-mono text-center`
**Tooltip:** Day + hour + active students count
**Legend:** below heatmap · "Low → High" gradient bar

#### 4.3.5 Top Engaged Students Table (below charts)

**Controls:** `[Sort by ▾]` (Exams taken / Avg score / Sessions) · `[Institution ▾]`
| Column | Detail |
|---|---|
| Rank | # |
| Student | Name (anonymised in demo mode: "Student #XXXXX") + institution |
| Exams Taken | Count |
| Avg Score | % with coloured bar |
| Sessions | Count |
| Last Active | Relative time |
| Improvement | Delta score last 3 vs first 3 exams |

**Pagination:** 25/page

---

### 4.4 Tab: Score Distribution

`id="tab-scores"` · `hx-get="?part=scores"`

#### 4.4.1 Score Distribution Histogram

**Chart:** Bar histogram · 10 bins: 0–10%, 11–20%, ..., 91–100%
**Bar colour:** gradient from `#EF4444` (0–30%) → `#F59E0B` (31–60%) → `#34D399` (61–100%)
**Y-axis:** student count
**Annotations:** vertical line at mean score (dashed `#6366F1`) + at platform target (dashed `#10B981`)
**Toggle:** [By Institution Type] splits histogram into grouped bars per type

#### 4.4.2 Score Trend (30-day rolling mean)

**Chart:** Line · `#6366F1` · 90-day window
**Y-axis:** 0–100% score
**Bands:** ±1 std dev shaded `rgba(99,102,241,0.15)`
**Tooltip:** date + mean + std dev + sample size

#### 4.4.3 Score by Institution Type

**Chart:** Box-and-whisker plot (implemented as grouped bar with error bars in Chart.js)
4 groups: School / College / Coaching / Group
**Each group:** Q1 bar + median line + Q3 bar + min/max whiskers
**Colour:** same type colours from §4.5 table

#### 4.4.4 Top/Bottom Performers Table

**Toggle:** [Top Performers] [Bottom Performers]
Same columns as §4.3.5

---

### 4.5 Tab: Cohort Analysis

`id="tab-cohort"` · `hx-get="?part=cohort"`

**Same cohort heatmap + retention line chart pattern as div-a-04 §4.5**
but metrics are:
- Retention by exam activity (student took ≥ 1 exam in period = retained)
- Cohort = month of first exam taken

**Cohort selector:** Month / Quarter · Institution type filter

**Heatmap:** Rows = cohort · Columns = months since first exam (0, 1, 3, 6, 12)
**Colours:** same as div-a-04

**Below heatmap:** Cohort comparison line chart
**Click cell:** Cohort Cell Drawer (480px) showing retained vs dropped students

---

### 4.6 Tab: Leaderboard

`id="tab-leaderboard"` · `hx-get="?part=leaderboard"`

**Purpose:** Platform-wide and per-institution leaderboards. Used for coaching centre parent portals (API export). Privacy-safe (student name shown only to authorised roles).

**Scope toggle:** [Platform-wide] [By Institution] [By State]

**Period toggle:** [This Week] [This Month] [This Year] [All Time]

**Subject toggle:** [All Subjects] [Maths] [Physics] [Chemistry] [Biology] ...

**Leaderboard table:**
| Column | Detail |
|---|---|
| Rank | # with medal icon (🥇🥈🥉 for top 3) |
| Student | Name + institution (privacy: shown only to `exec`/`superadmin`) |
| Exams | Count in period |
| Avg Score | % |
| Best Score | % + exam name |
| Percentile | 99th / 95th / 90th / etc. |
| Improvement | MoM score delta |

**Top 3 podium display:** above table · 3 cards with rank, name, score, institution
**Pagination:** 100/page

---

### 4.7 Tab: Retention

`id="tab-retention"` · `hx-get="?part=retention"`

**Definition:** Student retained = took at least 1 exam in current month (M) given they took ≥ 1 in M-1.

**Retention chart (line, 12 months):**
- Platform overall `#6366F1`
- School `#60A5FA`
- College `#34D399`
- Coaching `#FCD34D`
- Group `#A78BFA`

**Retention by state (choropleth map):** same SVG India map as div-a-04 · metric = student retention %
**Metric selector:** Retention % / Churn % / Reactivation %

---

### 4.8 Tab: Drop-off Analysis

`id="tab-dropoff"` · `hx-get="?part=dropoff"`

**Purpose:** Where in the exam funnel do students drop off? (Registered → Logged in → Started → Submitted)

#### 4.8.1 Funnel Chart

**Stages:** Exam Registered → Notified → Login on exam day → Started exam → Submitted
**Counts and drop-off %** at each transition
**Colour:** `#6366F1` with decreasing opacity
**Click stage:** opens Stage Detail Drawer (institutions with highest drop at that stage)

#### 4.8.2 Drop-off by Subject (bar chart)

Horizontal bars per subject · sorted by drop-off rate desc
Tooltip: subject + drop-off % + sample size

#### 4.8.3 Drop-off by Institution Type

Grouped bar: 4 types × 5 funnel stages

---

## 5. Drawers

### 5.1 Student Detail Drawer (560 px)

Triggered from any student name in tables. `body.drawer-open` added.

**Header:** Student name (or anonymised ID) + institution + grade · `[×]`

**Tab bar (4 tabs):**

**Tab A — Profile:**
- Enrolled date · grade · subjects
- Contact (visible to exec/ops only)
- Exam history summary

**Tab B — Exam History:**
Table: Exam name · Subject · Date · Score · Rank · Time taken · Status
Pagination: 25/page
Mini line chart: score over time

**Tab C — Performance:**
- Subject-wise avg score: horizontal bars
- Percentile rank per subject
- Score improvement chart (last 12 exams)
- Strong subjects vs weak subjects

**Tab D — Engagement:**
- Sessions per week (bar chart, last 12 weeks)
- Avg session duration
- Streak: current / longest
- Badges earned

**Footer:** [Export Student Report] [Flag for Review] [Close]

---

## 6. HTMX Architecture

| Part param | Template | Trigger |
|---|---|---|
| `?part=kpi` | `exec/partials/student_kpi.html` | Page load · poll 60s |
| `?part=engagement` | `exec/partials/student_engagement.html` | Tab click · filter change |
| `?part=scores` | `exec/partials/student_scores.html` | Tab click · filter change |
| `?part=cohort` | `exec/partials/student_cohort.html` | Tab click · filter change |
| `?part=leaderboard` | `exec/partials/student_leaderboard.html` | Tab click · filter change |
| `?part=retention` | `exec/partials/student_retention.html` | Tab click · filter change |
| `?part=dropoff` | `exec/partials/student_dropoff.html` | Tab click · filter change |
| `?part=student_drawer&id={id}` | `exec/partials/student_drawer.html` | Row click |

**Django view dispatch:**
```python
class StudentAnalyticsView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "portal.view_exec_analytics"

    def get(self, request):
        ctx = self._build_context(request)
        if _is_htmx(request):
            part = request.GET.get("part", "")
            templates = {
                "kpi": "exec/partials/student_kpi.html",
                "engagement": "exec/partials/student_engagement.html",
                "scores": "exec/partials/student_scores.html",
                "cohort": "exec/partials/student_cohort.html",
                "leaderboard": "exec/partials/student_leaderboard.html",
                "retention": "exec/partials/student_retention.html",
                "dropoff": "exec/partials/student_dropoff.html",
                "student_drawer": "exec/partials/student_drawer.html",
            }
            if part in templates:
                return render(request, templates[part], ctx)
        return render(request, "exec/student_analytics.html", ctx)

    def _build_context(self, request):
        filters = extract_filters(request.GET)
        return {
            "kpi": student_kpi_from_cache(),
            "filters": filters,
        }
```

---

## 7. Performance Requirements

| Metric | Target | Critical |
|---|---|---|
| KPI strip | < 200 ms | > 500 ms |
| Engagement tab (4 charts) | < 800 ms | > 2 s |
| Score distribution tab | < 600 ms | > 1.5 s |
| Cohort heatmap | < 600 ms | > 1.5 s |
| Leaderboard (100 rows) | < 500 ms | > 1.2 s |
| Retention chart | < 400 ms | > 1 s |
| Drop-off funnel | < 400 ms | > 1 s |
| Student drawer | < 300 ms | > 800 ms |
| Full page initial load | < 1.2 s | > 3 s |

**Data strategy:** All aggregates computed by Celery beat every 60s and stored in Redis. No live `COUNT(*)` on student table (2.4M+ rows). Partition student_exam_result table by month for score distribution queries. Use materialized views for cohort heatmap.

---

## 8. States & Edge Cases

| State | Behaviour |
|---|---|
| 0 students match filters | Empty state: "No students match your filters" + [Clear filters] |
| Leaderboard: privacy mode | If viewing institution that has privacy enabled, show "Student #XXXXX" instead of name |
| Score distribution: bimodal | No special handling but tooltip notes sample size |
| Drop-off funnel: < 100 students | Show "Insufficient data for this filter" notice |
| DAU/MAU < 10% | Engagement card background `bg-[#450A0A]` + alert tooltip |
| Coaching centre filter: >15K students | No performance degradation (uses pre-aggregated cache) |
| Custom date range > 1 year | Show "Showing sampled data (1-week intervals)" notice |
| Cohort heatmap: < 3 institutions in cohort | Cell shows "—" to avoid privacy leakage |

---

## 9. Keyboard Shortcuts

| Key | Action |
|---|---|
| `1`–`6` | Switch tabs |
| `F` | Focus filter bar |
| `R` | Refresh active tab |
| `E` | Export current view |
| `Esc` | Close drawer/modal |
| `?` | Keyboard shortcut help |

---

## 10. Template Files

| File | Purpose |
|---|---|
| `exec/student_analytics.html` | Full page shell |
| `exec/partials/student_kpi.html` | KPI strip |
| `exec/partials/student_engagement.html` | Engagement tab (4 charts + table) |
| `exec/partials/student_scores.html` | Score distribution tab |
| `exec/partials/student_cohort.html` | Cohort analysis tab |
| `exec/partials/student_leaderboard.html` | Leaderboard tab |
| `exec/partials/student_retention.html` | Retention tab |
| `exec/partials/student_dropoff.html` | Drop-off funnel tab |
| `exec/partials/student_drawer.html` | Student detail drawer |

---

## 11. Component References

| Component | Used in |
|---|---|
| `KpiCard` | §4.1 |
| `GlobalFilterBar` | §4.2 |
| `TabBar` | §4.3–4.8 |
| `DailyActiveChart` | §4.3.1 |
| `HistogramChart` | §4.3.2, §4.4.1, §4.3.3 |
| `PeakHoursHeatmap` | §4.3.4 |
| `TopStudentsTable` | §4.3.5 |
| `ScoreTrendLine` | §4.4.2 |
| `BoxPlotChart` | §4.4.3 |
| `CohortHeatmap` | §4.5 |
| `RetentionLineChart` | §4.5 |
| `LeaderboardTable` | §4.6 |
| `PodiumDisplay` | §4.6 top 3 |
| `IndiaChoroMap` | §4.7 |
| `FunnelChart` | §4.8.1 |
| `DrawerPanel` | §5.1 |
| `PaginationStrip` | All tables |
| `PollableContainer` | KPI strip |
