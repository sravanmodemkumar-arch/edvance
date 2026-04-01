# 09 — JEE/NEET Integration Head Dashboard

> **URL:** `/group/acad/jee-neet/`
> **File:** `09-jee-neet-dashboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Roles:** Group JEE/NEET Integration Head (G3) — exclusive landing page

---

## 1. Purpose

Primary post-login landing for the Group JEE/NEET Integration Head. This role is responsible for managing the integrated coaching programmes that run alongside the regular MPC (JEE track) and BiPC (NEET track) streams across all branches. The dashboard surfaces test-series progress, NTA syllabus coverage, mock test score trends, and student AIR potential tracking in a single command view.

The JEE/NEET Integration Head coordinates between the coaching layer and the regular academic layer — ensuring coaching schedules do not conflict with branch timetables, that mock test results are moderated and published on time, and that high-potential students (those likely to achieve national-level AIR ranks) are identified early and receive enhanced attention. This role also monitors parent communication queues related to coaching fees and schedule clarifications.

The dashboard covers both JEE (IIT/NIT/IIIT-focused, MPC students + coaching) and NEET (Medical-focused, BiPC students + coaching) programmes. Data is presented side-by-side for both tracks to enable comparative oversight. All AIR estimates shown are internal mock-based percentile projections — they are labelled clearly as projections, not official NTA figures.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group JEE/NEET Integration Head | G3 | Full — all sections, all actions | This is their exclusive dashboard |
| Chief Academic Officer (CAO) | G4 | Full read + override actions | CAO can access all academic dashboards |
| Group Academic Director | G3 | Read — syllabus coverage and score trend sections | Cross-function visibility |
| Group Stream Coordinator — MPC | G3 | Read — JEE-track sections only | Stream-level coordination |
| Group Stream Coordinator — BiPC | G3 | Read — NEET-track sections only | Stream-level coordination |
| Group Exam Controller | G3 | Read — test series schedule and moderation queue | Exam coordination |
| Group Results Coordinator | G3 | Read — mock test score trend only | Results coordination |
| Group Curriculum Coordinator | G2 | Read — NTA syllabus coverage heatmap only | Content alignment |
| Group IIT Foundation Director | G3 | Read — high-performer leaderboard (students transitioning from Foundation to JEE track) | Transition tracking |
| Group Olympiad & Scholarship Coord | G3 | Read — high-performer table (scholarship eligibility) | Cross-function |
| Group Special Education Coordinator | G3 | — | Has own dashboard |
| Group Academic MIS Officer | G1 | Read-only — all sections | No write controls visible |
| Group Academic Calendar Manager | G3 | Read — coaching schedule conflict section only | Calendar coordination |

> **Access enforcement:** Django view decorator `@require_role('jee_neet_head')`. CAO admitted via role-union check. MIS Officer admitted as read-only via role-union check. All other roles are redirected to their own dashboard unless explicitly listed above.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Academic Leadership  ›  JEE / NEET Integration  ›  Integration Head Dashboard
```

### 3.2 Page Header
```
Welcome back, [Head Name]                          [Schedule Mock Test +]  [Settings ⚙]
Group JEE/NEET Integration Head  ·  Last login: [date time]  ·  [Group Logo]
```

### 3.3 Alert Banner (conditional — shown only when alerts exist)
- Collapsible panel above KPI row
- Background: `bg-red-50 border-l-4 border-red-500` for Critical · `bg-yellow-50 border-l-4 border-yellow-400` for Warning
- Each alert: icon + message + branch name + [Take Action →] link
- "Dismiss" per alert (stored in session, reappears next login if unresolved)
- Maximum 5 alerts shown; "View all →" link

**Alert trigger examples:**
- Mock test result moderation overdue > 72 hrs after test date
- Coaching timetable conflict detected in ≥ 1 branch for the coming week
- NTA syllabus coverage < 60% for a high-weight chapter with JEE/NEET exam < 60 days away
- Coaching fee query from parent unresolved > 5 days
- Test series milestone missed — planned mock not conducted on scheduled date

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| JEE Integrated Students | Total MPC+coaching students across all branches + trend | Enrollment module | Green if ≥ target · Yellow 80–99% · Red < 80% | → Section 5.2 Integrated Student Count |
| NEET Integrated Students | Total BiPC+coaching students across all branches + trend | Enrollment module | Green if ≥ target · Yellow 80–99% · Red < 80% | → Section 5.2 Integrated Student Count |
| NTA Syllabus Coverage | `XX%` of NTA topics covered group-wide (weighted JEE + NEET avg) | Syllabus tracking | Green ≥ 80% · Yellow 60–80% · Red < 60% | → Section 5.4 Coverage Heatmap |
| Mock Test Series Progress | Tests conducted / Tests planned this series · e.g., `8 / 12` | Test series module | Green if on schedule · Yellow 1 behind · Red ≥ 2 behind | → Section 5.1 Test Series Tracker |
| High-Performer Count | Students in top-5% mock percentile nationally (AIR potential tier) | Analytics module | Green ≥ 50 · Yellow 20–49 · Red < 20 | → Section 5.5 High Performers |
| Pending Moderation | Coaching test results awaiting approval across all branches | Results module | Green = 0 · Yellow 1–5 · Red > 5 (pulsing badge) | → Section 5.7 Moderation Queue |

**HTMX:** Cards auto-refresh every 5 minutes via `hx-trigger="every 5m"` `hx-get="/api/v1/group/{group_id}/acad/jee-neet/kpi-cards/"` `hx-swap="innerHTML"` targeting `#kpi-bar`.

---

## 5. Sections

### 5.1 JEE/NEET Test Series Progress

> Milestone tracker showing planned vs conducted vs results-published status across the full test series.

**Display:** Milestone tracker — horizontal step-by-step timeline with status indicators.

**Track grouping:** Two parallel tracks — JEE Series (top) and NEET Series (bottom).

**Milestone columns:**

| Column | Description |
|---|---|
| Test # | Mock test number in the series (e.g., Mock 1, Mock 2 … Mock 12) |
| Planned Date | Scheduled test date |
| Status | Conducted (green check) · Upcoming (grey) · Missed (red X) · Rescheduled (amber) |
| Results Published | Y (green) / N (red) |
| Branches Participated | Count of branches that ran this mock |
| Avg Score | Group avg % for this mock (shown after results published) |
| Actions | [View Results →] · [Reschedule] (G3 only) · [Publish Results] (G3 only, if results uploaded) |

**Summary strip (above tracker):** Tests planned: X · Conducted: Y · Results published: Z · Missed: W (red badge if W > 0)

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/test-series/"` · `hx-trigger="load"` · `hx-target="#test-series-section"` · `hx-swap="innerHTML"`.

---

### 5.2 Integrated Student Count

> Enrollment breakdown for JEE and NEET coaching tracks across all branches.

**Display:** Dual stat-card columns — JEE track (left panel) and NEET track (right panel).

**JEE Track cards:**
- Total JEE integrated students (group-wide)
- Branch count offering JEE coaching
- Class XI enrolled · Class XII enrolled
- New enrollments this month

**NEET Track cards:**
- Total NEET integrated students (group-wide)
- Branch count offering NEET coaching
- Class XI enrolled · Class XII enrolled
- New enrollments this month

**Branch breakdown table (below stat cards):**

| Column | Sortable | Notes |
|---|---|---|
| Branch Name | ✅ | Link to branch detail |
| JEE Students | ✅ | 0 = red if coaching offered but zero enrolled |
| NEET Students | ✅ | 0 = red if coaching offered but zero enrolled |
| Total Coaching | ✅ | JEE + NEET |
| JEE Capacity % | ✅ | Enrolled / Batch capacity |
| NEET Capacity % | ✅ | Enrolled / Batch capacity |

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/student-count/"` · `hx-trigger="load"` · `hx-target="#student-count-section"`.

---

### 5.3 Mock Test Score Trend

> Group average score per mock test across the JEE and NEET test series — tracks trajectory over time.

**Display:** Line chart (Chart.js 4.x)

**X-axis:** Mock test number (Mock 1 → Mock N) across the current year's series.

**Y-axis:** Average score percentage (0–100%)

**Series:** JEE avg (blue solid line) · NEET avg (green solid line) · JEE target line (blue dashed) · NEET target line (green dashed)

**Tooltip:** Mock # · JEE avg · NEET avg · JEE highest branch · NEET highest branch · Branches participating

**Filters within chart card:**
- Track toggle: All / JEE only / NEET only
- Branch filter: All branches or single branch selection
- Year selector: Current year / Previous year (for comparison overlay)

**Export:** "Export PNG" button top-right of chart card.

**Empty state:** "No mock test data yet. Conduct and publish the first mock test to see trends."

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/score-trend/"` · filter changes trigger `hx-get` with params · `hx-target="#score-trend-chart"` · `hx-swap="innerHTML"`.

---

### 5.4 NTA Syllabus Coverage Heatmap

> Shows which NTA syllabus topics have been covered vs not yet covered, by subject.

**Display:** Heatmap grid (subject × topic-group)

**Coverage tracks:** JEE (Physics, Chemistry, Maths) and NEET (Physics, Chemistry, Biology) shown as separate heatmap panels.

**Rows:** Chapter / unit names within each subject (NTA-standard chapter groupings)

**Columns:** Branches (branch name abbreviated; full name in tooltip)

**Cell colours:**
- Dark green: ≥ 85% of this chapter's topics taught across the group
- Light green: 70–85%
- Amber: 50–70%
- Red: < 50% — critical gap
- Grey: Chapter not yet scheduled for this stage of the year

**Interaction:** Click any cell → opens coverage detail drawer showing topic-level status within that chapter for that branch.

**Drawer: `nta-coverage-detail`**
- Width: 560px
- Content: Topic list within selected chapter · Each topic: Status (Taught / Partial / Not started) · Last taught date · Teacher name
- Filter: Sort by coverage % ascending

**High-weight chapter badges:** NTA high-weight chapters (≥ 10 marks in JEE/NEET) are marked with a star badge — coverage failures here are surfaced in alert banner.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/nta-coverage/"` · `hx-trigger="load"` · `hx-target="#nta-coverage-section"` · cell click triggers drawer load.

---

### 5.5 High-Performer Tracking (AIR Potential)

> Students in the top 5% national mock percentile — likely candidates for strong JEE/NEET AIR ranks.

**Display:** Table (sortable)

**Important notice strip (above table):** "AIR estimates shown are internal mock-based projections only. These are not official NTA scores or ranks."

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Rank (Internal) | ✅ | Group-level rank by mock percentile |
| Student Code | ✅ | Anonymised code — actual name visible only to G3+ |
| Branch | ✅ | Branch name |
| Track | ✅ | JEE / NEET |
| Class | ✅ | XI / XII |
| Mock Percentile | ✅ | Best percentile achieved in last 3 mocks |
| AIR Projection Tier | ✅ | Top 100 / Top 500 / Top 1000 / Top 5000 — internal estimate |
| Trend | ❌ | ↑ Improving / ↓ Declining / → Stable (3-mock trend) |
| Actions | ❌ | [View Profile →] [Add to Enhanced Program] |

**Filters:** Track (JEE / NEET) · Branch · Class · AIR Projection Tier · Trend direction

**[Add to Enhanced Program]:** POST to enrol student in additional support — triggers notification to branch coordinator.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/high-performers/"` · search/filter triggers `hx-get` with params · `hx-target="#high-performers-section"`.

---

### 5.6 Coaching Schedule Conflicts

> Alerts where integrated coaching sessions clash with regular branch timetable periods.

**Display:** Alert list (card-style)

**Card fields:** Branch name · Conflict date · Conflict time · Coaching session (subject + type) · Regular class clashing (subject + class section) · Severity (Hard conflict = same room/teacher · Soft conflict = student double-booked) · Days until conflict · [Resolve →]

**Severity colour:** Red card = Hard conflict (same resource) · Amber = Soft conflict (student schedule clash)

**[Resolve →] action:** Opens conflict resolution drawer.

**Drawer: `coaching-conflict-resolve`**
- Width: 560px
- Tabs: Conflict Details · Proposed Resolutions · History
- Proposed Resolutions tab: System suggests 3 alternatives (reschedule coaching / reschedule regular class / split session)
- Action: [Apply Resolution] → POST + notifies branch coordinator

**Bulk action:** [Send conflict report to all affected branches] → generates report email/WhatsApp.

**Empty state:** "No coaching schedule conflicts detected for the coming week." — green checkmark.

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/conflicts/"` · `hx-trigger="load"` · `hx-target="#conflicts-section"`.

---

### 5.7 Result Moderation Queue — Coaching Tests

> Coaching test results uploaded by branches that are awaiting group-level moderation and approval before publication.

**Display:** Counter badge + action list (card per pending result set)

**Card fields:** Mock test name · Test date · Track (JEE / NEET) · Branch · Results uploaded by · Uploaded at · Marks range (min–max) · [Review & Approve →] [Flag for Review]

**Urgency:** Red badge on card if > 72 hrs since upload without moderation.

**[Review & Approve] action:** Opens moderation drawer.

**Drawer: `result-moderation`**
- Width: 640px
- Tabs: Score Distribution · Outlier Check · Approve / Return
- Score Distribution: Histogram of marks distribution for this test
- Outlier Check: Students with scores > 2 standard deviations above mean — flag for verification
- Approve / Return tab: [Approve and Publish] [Return with Query] (requires reason, min 20 chars)

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/moderation-queue/"` · `hx-trigger="load"` · `hx-target="#moderation-section"` · Approve: `hx-post="/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/approve/"`.

---

### 5.8 Parent Communication Queue

> Coaching-related parent queries (fee, schedule, performance) assigned to the JEE/NEET Integration Head.

**Display:** Table (sortable by age of query)

**Columns:**

| Column | Sortable | Notes |
|---|---|---|
| Query # | ✅ | System-generated ref |
| Parent / Student | ✅ | Name + branch |
| Track | ✅ | JEE / NEET |
| Query Type | ✅ | Fee · Schedule · Performance · Enrolment |
| Submitted | ✅ | Date submitted |
| Age (days) | ✅ | Red if > 5 days |
| Status | ✅ | Pending · In Progress · Resolved |
| Actions | ❌ | [Respond →] [Assign to Branch] [Mark Resolved] |

**Filters:** Track · Query Type · Status · Age (> 3 days / > 5 days / > 7 days)

**[Respond →]:** Opens response composer drawer.

**Drawer: `parent-query-respond`**
- Width: 560px
- Tabs: Query Detail · Communication History · Respond
- Respond tab: Rich text response field · Channel selector (Email / WhatsApp / Portal) · [Send & Resolve] [Send & Keep Open]

**HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/parent-queries/"` · sort/filter triggers `hx-get` with params · `hx-target="#parent-queries-section"`.

---

## 6. Drawers & Modals

### 6.1 Drawer: `nta-coverage-detail`
- **Trigger:** Heatmap cell click in Section 5.4
- **Width:** 560px
- **Content:** Topic-level status within selected chapter for selected branch; sortable by coverage %
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/nta-coverage/{branch_id}/{chapter_id}/"` `hx-target="#drawer-body"` `hx-swap="innerHTML"`

### 6.2 Drawer: `coaching-conflict-resolve`
- **Trigger:** [Resolve →] in Section 5.6 conflict card
- **Width:** 560px
- **Tabs:** Conflict Details · Proposed Resolutions · History
- **Action:** [Apply Resolution] → POST resolution choice + notifies branch
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/conflicts/{conflict_id}/"` `hx-target="#drawer-body"`

### 6.3 Drawer: `result-moderation`
- **Trigger:** [Review & Approve →] in Section 5.7 moderation card
- **Width:** 640px
- **Tabs:** Score Distribution · Outlier Check · Approve / Return
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/review/"` `hx-target="#drawer-body"`

### 6.4 Drawer: `parent-query-respond`
- **Trigger:** [Respond →] in Section 5.8 query table
- **Width:** 560px
- **Tabs:** Query Detail · Communication History · Respond
- **HTMX:** `hx-get="/api/v1/group/{group_id}/acad/jee-neet/parent-queries/{query_id}/"` `hx-target="#drawer-body"`

### 6.5 Modal: `reschedule-mock-test`
- **Trigger:** [Reschedule] action in Section 5.1 milestone tracker
- **Width:** 440px
- **Content:** Current date · New date picker · Reason (required, min 20 chars) · Branches affected (auto-listed) · [Confirm Reschedule] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/reschedule/"` → toast + tracker updates

### 6.6 Modal: `publish-results-confirm`
- **Trigger:** [Publish Results] action in Section 5.1 milestone tracker
- **Width:** 420px
- **Content:** "Publish results for [Mock Test Name]? This will make results visible to students and parents across [N] branches." + [Confirm Publish] [Cancel]
- **On confirm:** `hx-post="/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/publish/"` → toast + tracker row updates

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Results moderation approved | "Results approved and published for [Mock Test Name]" | Success (green) | 5s auto-dismiss |
| Results returned | "Query sent to [Branch Name] for [Mock Test Name] results" | Info (blue) | 4s |
| Mock test rescheduled | "Mock test rescheduled to [new date] — branches notified" | Info | 5s |
| Conflict resolved | "Schedule conflict resolved — [Branch Name] branch notified" | Success | 4s |
| Student added to enhanced program | "Student [Code] added to Enhanced Coaching Program" | Success | 4s |
| Parent query responded | "Response sent to parent via [channel]" | Success | 4s |
| Parent query resolved | "Query marked as resolved" | Success | 4s |
| KPI load error | "Failed to load KPI data. Retrying…" | Error (red) | Manual dismiss |
| Coverage data unavailable | "Syllabus coverage data unavailable. Check branch reporting." | Warning (yellow) | 6s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No test series configured | Calendar outline | "No test series set up" | "Configure the JEE/NEET mock test series to get started" | [Configure Series] |
| No high performers yet | Trophy outline | "No high-performer data" | "Complete at least 3 mock tests to identify high-potential students" | — |
| No coaching conflicts | Checkmark circle | "No schedule conflicts" | "No coaching timetable conflicts detected for the coming week" | — |
| No pending moderation | Checkmark circle | "No results pending moderation" | "All coaching test results have been reviewed and published" | — |
| No parent queries | Inbox outline | "No open parent queries" | "All coaching-related parent queries have been resolved" | — |
| No NTA coverage data | Document outline | "Coverage data unavailable" | "No syllabus coverage data reported. Branches must update progress." | [Send Reminder] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Page initial load | Skeleton screens: KPI bar (6 cards) + test series tracker (8 milestone rows) + chart placeholder |
| Test series section load | Skeleton milestone rows — 5 rows |
| Score trend chart load | Spinner centred in chart area |
| NTA heatmap load | Grey placeholder grid |
| High-performer table load | Skeleton table rows — 5 rows |
| Conflict list load | Skeleton alert cards — 3 cards |
| Drawer open | Skeleton rows inside drawer body |
| Approve/publish button click | Spinner inside button + button disabled |
| KPI auto-refresh | Subtle shimmer over existing card values |

---

## 10. Role-Based UI Visibility

| Element | JEE/NEET Head (G3) | CAO (G4) | MPC/BiPC Coords (G3) | MIS Officer (G1) | All others |
|---|---|---|---|---|---|
| Page itself | ✅ Rendered | ✅ Rendered (override) | ✅ Partial read | ✅ Read-only | ❌ Redirected |
| Alert Banner | ✅ Shown | ✅ Shown | ✅ Shown (read) | ✅ Shown | N/A |
| [Publish Results] action | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Reschedule] action | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Review & Approve] moderation | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Apply Resolution] on conflict | ✅ Enabled | ✅ Enabled | ❌ Hidden | ❌ Hidden | N/A |
| [Add to Enhanced Program] | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| [Respond →] parent queries | ✅ Shown | ✅ Shown | ❌ Hidden | ❌ Hidden | N/A |
| High-performer student names | ✅ Visible | ✅ Visible | ✅ Visible (own stream) | ❌ Code only | N/A |
| AIR Projection Tier column | ✅ Visible | ✅ Visible | ✅ Visible | ✅ Visible | N/A |

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/acad/jee-neet/dashboard/` | JWT (G3+) | Full page data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/kpi-cards/` | JWT (G3+) | KPI card values only (auto-refresh) |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/test-series/` | JWT (G3+) | Test series milestone data |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/test-series/{test_id}/reschedule/` | JWT (G3) | Reschedule a mock test |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/student-count/` | JWT (G3+) | Integrated student enrollment breakdown |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/score-trend/` | JWT (G3+) | Mock test score trend chart data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/nta-coverage/` | JWT (G3+) | NTA syllabus coverage heatmap data |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/nta-coverage/{branch_id}/{chapter_id}/` | JWT (G3+) | Topic-level coverage for one chapter/branch |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/high-performers/` | JWT (G3+) | High-performer table |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/high-performers/{student_id}/enhanced/` | JWT (G3) | Add student to enhanced program |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/conflicts/` | JWT (G3+) | Coaching schedule conflicts |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/conflicts/{conflict_id}/` | JWT (G3+) | Conflict detail + proposed resolutions |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/conflicts/{conflict_id}/resolve/` | JWT (G3) | Apply resolution |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/moderation-queue/` | JWT (G3+) | Results awaiting moderation |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/review/` | JWT (G3+) | Moderation drawer data |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/approve/` | JWT (G3) | Approve and publish results |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/return/` | JWT (G3) | Return results with query |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/results/{result_id}/publish/` | JWT (G3) | Publish approved results to students |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/parent-queries/` | JWT (G3+) | Parent query list |
| GET | `/api/v1/group/{group_id}/acad/jee-neet/parent-queries/{query_id}/` | JWT (G3+) | Query detail and history |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/parent-queries/{query_id}/respond/` | JWT (G3) | Send response |
| POST | `/api/v1/group/{group_id}/acad/jee-neet/parent-queries/{query_id}/resolve/` | JWT (G3) | Mark resolved |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI auto-refresh | `every 5m` | GET `/api/.../jee-neet/kpi-cards/` | `#kpi-bar` | `innerHTML` |
| Test series load | `load` | GET `/api/.../jee-neet/test-series/` | `#test-series-section` | `innerHTML` |
| Score trend filter change | `change` | GET `/api/.../score-trend/?track={}&branch={}&year={}` | `#score-trend-chart` | `innerHTML` |
| NTA heatmap load | `load` | GET `/api/.../nta-coverage/` | `#nta-coverage-section` | `innerHTML` |
| Heatmap cell click | `click` | GET `/api/.../nta-coverage/{branch_id}/{chapter_id}/` | `#drawer-body` | `innerHTML` |
| High-performer filter | `change` | GET `/api/.../high-performers/?track={}&tier={}` | `#high-performers-section` | `innerHTML` |
| Add to enhanced program | `click` | POST `/api/.../high-performers/{id}/enhanced/` | `#toast-container` | `afterbegin` |
| Conflict resolve apply | `click` | POST `/api/.../conflicts/{id}/resolve/` | `#conflicts-section` | `innerHTML` |
| Open moderation drawer | `click` | GET `/api/.../results/{id}/review/` | `#drawer-body` | `innerHTML` |
| Approve results | `click` | POST `/api/.../results/{id}/approve/` | `#moderation-section` | `innerHTML` |
| Publish results confirm | `click` | POST `/api/.../results/{id}/publish/` | `#test-series-section` | `innerHTML` |
| Parent query sort/filter | `change` | GET `/api/.../parent-queries/?type={}&status={}` | `#parent-queries-section` | `innerHTML` |
| Open parent query drawer | `click` | GET `/api/.../parent-queries/{id}/` | `#drawer-body` | `innerHTML` |
| Reschedule mock confirm | `click` | POST `/api/.../test-series/{id}/reschedule/` | `#test-series-section` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
