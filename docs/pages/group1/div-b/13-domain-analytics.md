# Page 13 — Domain Analytics

**URL:** `/portal/product/domain-analytics/`
**Permission:** `product.view_domain_analytics`
**Priority:** P1
**Roles:** PM Exam Domains, PM Platform

---

## Purpose

Central analytics hub for all 8 exam domains managed by the SRAV platform. This page is the primary decision-making surface for the PM Exam Domains role and provides cross-domain visibility to PM Platform. Every strategic decision about question bank investment, syllabus coverage, test series quality, and institutional domain adoption is grounded in data surfaced here.

Core questions this page answers:
- Which domains are growing enrollment fastest and which are stagnating?
- Where are question bank coverage gaps causing students to encounter repeated or imbalanced questions?
- Which test series have high enrollment but low completion — a product quality issue?
- Which institutions subscribed to a domain but never actually used it — churn risk?
- How do score distributions compare across exam categories and time periods?
- Which topics are high-frequency in official exams but low-coverage in the question bank?
- What is the week-over-week and month-over-month attempt trend for each domain?

**Scale context:**
- 8 domains: SSC, RRB, NEET, JEE, AP Board, TS Board, IBPS, SBI
- 42 exam categories spread across these 8 domains
- 1,000 schools × avg 1,000 students = ~1M students from schools
- 800 colleges × avg 500 students = ~400K students from colleges
- 100 coaching centres × avg 10,000 members = ~1M students from coaching
- Total active students: 2.4M–7.6M depending on season
- Monthly test attempts: 800K+
- Question bank: 2M+ approved items across all domains

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────┐
│  "Domain Analytics"    Period ▾  [Compare Domains]  [Export PDF]│
├────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards (auto-refresh every 120s)                 │
├────────────────────────────────────────────────────────────────┤
│  Domain Tab Bar:                                               │
│  SSC · RRB · NEET · JEE · AP Board · TS Board · IBPS · SBI    │
├─────────────────┬──────────────────────────────────────────────┤
│  Domain Grid    │  Sub-tab Bar:                                │
│  Sidebar (3col) │  Enrollment · Attempts · Score Dist          │
│                 │  Coverage · Gap Analysis · Series · Institutions│
│  8 domain       ├──────────────────────────────────────────────┤
│  summary cards  │                                              │
│                 │  Active Tab Content Area                     │
│  Click any card │  Charts + Tables + Pagination                │
│  = switch domain│                                              │
│                 │                                              │
├─────────────────┴──────────────────────────────────────────────┤
│  Compare Mode Panel (hidden by default)                        │
│  Domain checkboxes · Metric ▾ · Period ▾ → Multi-line chart    │
└────────────────────────────────────────────────────────────────┘
```

---

## Header Controls

| Control | Behaviour |
|---|---|
| Period Selector | Dropdown: Last 7 days / Last 30 days / Last 90 days / Last 6 months / Last 12 months. Changes all charts and tables in the active tab. Default: Last 30 days. |
| Compare Domains | Toggle button. Shows or hides the Compare Mode Panel at the bottom of the page. |
| Export PDF | Generates a full domain analytics report for the active domain and selected period. Includes all charts, KPIs, gap list, and series table. Opens download dialog. |

---

## KPI Strip — 6 Cards

Auto-refresh every 120 seconds. Refresh paused if any drawer or modal is open. All values animate count-up from 0 to final value over 600ms on page load and after each refresh.

### Card 1 — Total Enrollments
- Value: Total active domain enrollments across all 8 domains combined
- Delta: percentage change vs previous 30-day period (green arrow if positive, red if negative)
- Sub-label: "across 8 domains"
- Clicking opens the domain grid sidebar with "All" filter active

### Card 2 — Monthly Attempts
- Value: Total test attempts submitted in the last 30 days across all domains
- Delta: percentage change vs previous 30-day period
- Sub-label: "tests submitted"
- Clicking switches detail panel to Attempts tab

### Card 3 — Question Bank
- Value: Count of approved, active question bank items across all domains
- Delta: count added in last 30 days shown as "+ X new"
- Sub-label: "approved questions"
- Clicking navigates to Syllabus Builder page with question count view

### Card 4 — Avg Coverage
- Value: Platform-wide average topic coverage percentage across all active syllabus topic nodes
- Display: percentage value with a thin horizontal progress bar below
- Colour coding: ≥75% green · 50–74% amber · 25–49% orange · <25% red
- Sub-label: "of syllabus topics covered"
- Clicking switches detail panel to Coverage tab

### Card 5 — Active Domains
- Value: Count of active domains out of 8 total (e.g. "8 / 8")
- Sub-label: "all operational" if all active, or count of inactive domains with warning icon
- Clicking navigates to Exam Domain Config page (page 09)

### Card 6 — Institutions Using
- Value: Distinct institution count with at least one active domain subscription
- Delta: percentage change vs last week
- Sub-label: "institutions subscribed"
- Clicking switches detail panel to Institutions tab

---

## Domain Tab Bar

8 tabs displayed horizontally. Each tab:
- Shows domain name
- Shows a small colour dot unique to each domain:
  - SSC: indigo
  - RRB: green
  - NEET: red
  - JEE: amber
  - AP Board: blue
  - TS Board: purple
  - IBPS: teal
  - SBI: orange
- Active tab: coloured background + white text + soft shadow
- Inactive tabs: muted text + hover highlight

Clicking any tab:
1. Highlights that tab
2. Updates the domain grid sidebar to show the clicked domain as selected
3. Reloads all detail sub-tab content for the selected domain
4. Passes `?domain=X` parameter to all HTMX sub-requests

---

## Domain Grid Sidebar

Always-visible left panel (3 columns wide). Contains 8 stacked cards, one per domain. Persists while user browses sub-tabs.

### Each Domain Card Shows:

| Field | Detail |
|---|---|
| Domain name | Bold, with colour dot |
| Enrollment delta badge | Green ↑X% or Red ↓X% vs previous 30 days |
| Total active enrollments | Formatted with thousands separator |
| Monthly attempts | Attempts in last 30 days |
| Active series count | Test series with status = active |
| Coverage % | Average topic coverage, colour-coded green/amber/orange/red |
| Coverage mini-bar | Thin 1-pixel horizontal bar proportional to coverage % |

Clicking any card:
- Highlights that card with border
- Switches the domain tab bar to that domain
- Reloads the detail sub-tab area for that domain
- Scrolls detail area to top

Cards refresh every 120 seconds together with KPI strip.

---

## Detail Sub-tabs (7 tabs)

### Sub-tab 1 — Enrollment

**Enrollment Trend Chart**

Chart type: Line chart (toggleable to Bar via Type button in chart header). Height 256px. Full width of content area.

- X-axis: Date labels. Daily intervals for periods ≤30 days. Weekly intervals for 90 days and above.
- Y-axis: Count of new domain enrollments per day (or week for longer periods)
- Single dataset: New enrollments for the active domain
- Tooltip on hover: exact date, exact count
- Chart title: "Enrollment Trend — [Domain Name]"
- Sub-label: "New domain enrollments per day"
- Refreshes automatically when domain tab or period selector changes

**Enrollment Breakdown — 2 Charts Side by Side**

Left chart — By Institution Tier (Doughnut chart):
- 4 segments: Starter / Standard / Professional / Enterprise
- Each segment labelled with count and percentage
- Legend below chart
- Hover tooltip: tier name, enrollment count, % of domain total

Right chart — By State (Horizontal bar chart):
- Top 10 states by enrollment count for this domain
- X-axis: enrollment count
- Y-axis: state names
- Each bar labelled with count
- Tooltip: state name, count, % of total

---

### Sub-tab 2 — Attempts

**Daily Attempts Chart**

Chart type: Grouped bar chart. Height 256px.

- X-axis: date labels (same interval logic as enrollment chart)
- Y-axis: attempt count
- Two datasets per day: Started (indigo bars) and Submitted (green bars)
- Horizontal reference line drawn at 65% completion rate threshold with label "Target: 65%"
- Tooltip: date, started count, submitted count, submission rate %
- Refreshes on domain or period change

**Attempt Funnel**

Horizontal animated progress bars showing the student drop-off funnel:

| Stage | Colour | Percentage | Absolute Count |
|---|---|---|---|
| Started | Indigo | 100% (base) | Count with commas |
| Submitted | Green | % of started | Count with commas |
| Reviewed Solutions | Amber | % of started | Count with commas |

- All counts animate on load (count-up 600ms)
- Percentage bars are proportional width
- Below the funnel: "Drop-off insight" — e.g. "22% of students who start do not submit. Likely causes: session timeout, internet disconnect."

**Completion Rate Trend**

Small line chart below the funnel. Shows daily completion rate (submitted/started %) over the selected period. Reference line at 65% threshold. Used to spot days with abnormal drop-off (e.g. platform issues during exam day).

---

### Sub-tab 3 — Score Distribution

**Exam Category Filter**

Dropdown positioned above the chart. Options: "All Categories" + one option per exam category belonging to the active domain. Example for SSC domain: SSC CGL · SSC CHSL · SSC MTS · SSC CPO · SSC GD · SSC Stenographer. Selecting a category refreshes the histogram and percentile table for that category only.

**Score Distribution Histogram**

Chart type: Bar chart. 20 buckets, each spanning 5 marks (0–5, 5–10, … 95–100). Height 256px.

- X-axis: score range labels (0–5, 5–10, …)
- Y-axis: number of students in that score range
- Vertical annotation line at mean score (amber colour, labelled "Mean: XX.X%")
- Vertical annotation line at median score (dashed, labelled "Median: XX.X%")
- Tooltip on hover: score range, student count, percentage of total attempts
- Below chart: three stat badges — Mean, Median, Std Dev

**Percentile Breakdown Table**

| Percentile Range | Score Range | Students | % of Total | Visual Bar |
|---|---|---|---|---|
| Top 1% (99th–100th) | 92–100 | 8,423 | 1.0% | narrow bar |
| 90th–99th percentile | 78–91 | 75,811 | 9.0% | medium bar |
| 75th–90th percentile | 65–77 | 125,432 | 14.9% | wide bar |
| 50th–75th percentile | 48–64 | 209,721 | 24.9% | wider bar |
| 25th–50th percentile | 30–47 | 209,721 | 24.9% | wider bar |
| Bottom 25% | 0–29 | 211,392 | 25.1% | full bar |

Footer row: Total Attempts · Average Score · Pass Rate (if cut-off defined for category)

---

### Sub-tab 4 — Coverage

**Coverage Heatmap**

Grid layout:
- Rows: Subjects in the active domain
- Columns: Chapters within each subject (up to 12 columns, scroll horizontally if more)

Each cell represents one chapter:
- Cell fill colour: based on average topic coverage % across all topics in that chapter
  - Green: ≥80% coverage
  - Amber: 50–79%
  - Orange: 25–49%
  - Red: <25%
- Cell size: proportional to number of topics (larger cell = more topics)
- Hover tooltip shows: Chapter name · Coverage % · Question count · Topic count · Covered topics count

Clicking any cell:
- Opens a mini panel below the heatmap showing chapter detail
- Subject name, chapter name, topic list with individual topic coverage bars
- "Open in Syllabus Builder" link that deep-links to page 10 with that chapter pre-selected

**Coverage Legend** (top-right of heatmap section)
Shows colour scale: Green ≥80% · Amber 50–79% · Orange 25–49% · Red <25%

**Coverage Summary Stats — 4 Cards**

| Card | Value | Colour |
|---|---|---|
| Avg Coverage | % average across all topics in domain | Colour-coded |
| Under-covered Topics | Count of topics with coverage < 25% | Red if > 0 |
| Total Questions | Approved questions in this domain | Neutral |
| Syllabus Nodes | Total topic nodes in domain | Neutral |

**Subject Coverage Bar Chart** (below heatmap cards)

Horizontal bar chart:
- One bar per subject
- Sorted ascending by coverage % (worst-covered subject at top)
- Each bar labelled with subject name, coverage %, question count
- Clicking a bar expands the heatmap to zoom into that subject's chapters

---

### Sub-tab 5 — Gap Analysis

**Gap Resolution Progress Panel**

Positioned at the top. Contains:
- Donut gauge showing % of identified gaps resolved in last 30 days
- 4 stat boxes beside the gauge:
  - Identified: total gap count
  - In Progress: assigned and being worked on
  - Resolved: closed in last 30 days
  - Critical: severity = critical, unresolved
- "Assign Bulk" button: select multiple gaps and assign to a team member
- "Export Gap List" button: download gap list as CSV

**Gap List**

Ranked table, sorted by severity (Critical first, then High, then Medium). Top 100 gaps shown.

| Column | Detail |
|---|---|
| Topic Name | Full name of the under-covered topic |
| Path | Subject → Chapter breadcrumb in small muted text |
| Severity | Colour badge: Critical (red) · High (orange) · Medium (amber) |
| Coverage % | Colour-coded percentage |
| Current Questions | Count of existing approved questions for this topic |
| Recommended Min | Platform minimum (typically: ≥20 questions per topic) |
| Shortfall | Recommended − Current (shown in red if > 0) |
| Exam Frequency | How often this topic has appeared in official past exams (categorised: Very High / High / Medium / Low) |
| Assigned To | Content team member email link or "Unassigned" in muted text |
| Due Date | If assigned, target completion date |
| Action | "Assign" button → opens Assignment Modal |

**Severity Rules:**

| Severity | Criteria |
|---|---|
| Critical | Coverage < 15% OR question count < 5 AND exam frequency ≥ High |
| High | Coverage < 30% OR question count < 10 |
| Medium | Coverage < 50% |
| Watch | Coverage 50–65% — informational, not actionable |

**Gap Assignment Modal:**
- Topic name (pre-filled, read-only)
- Assign to (team member dropdown — content team members)
- Due date picker
- Notes field (optional)
- Submit button

---

### Sub-tab 6 — Series

**Toolbar (row above table)**
- Search input: searches series name, 300ms debounce
- Status filter dropdown: All / Active / Draft / Archived
- Sort indicator showing current sort column
- Result count badge: "X series found"

**Series Table — 9 columns**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Series Name | Text link to series detail drawer | Yes | Truncated at 40 chars with tooltip |
| Status | Badge | Yes | Active (green) · Draft (amber) · Archived (grey) |
| Exam Count | Integer | Yes | Number of exams in series |
| Enrollments | Integer with commas | Yes | Total enrolled students |
| Avg Score | Colour-coded % | Yes | ≥60% green · 40–59% amber · <40% red |
| Attempt Rate | % | Yes | Attempts / Enrollments |
| Completion Rate | Progress bar + % | Yes | Submitted / Started |
| Created Date | Short date | Yes | DD Mon YYYY |
| Actions | Link | No | "View →" appears on row hover |

**Completion Rate Column Detail:**
- Thin progress bar (16px wide) + numeric % beside it
- Bar colour: ≥70% green · 50–69% amber · <50% red

**Empty State:** "No series found for this domain" with an illustration and "Create Test Series" link.

**Pagination:**
- "Showing X–Y of Z series"
- Page number pills (show up to 7 pills, ellipsis for more)
- Previous / Next buttons
- Per-page selector: 10 / 25 / 50 / 100

---

### Sub-tab 7 — Institutions

**Toolbar (row above table)**
- Search input: institution name, 300ms debounce
- Tier filter: All / Starter / Standard / Professional / Enterprise
- Type filter: All / School / College / Coaching / Group
- **"⚠ Churn Risk Only"** button: applies churn risk filter (no activity in last 14 days AND domain coverage < 40%)
- Result count badge

**Churn Risk Logic:**
An institution is flagged as churn risk for a domain when:
1. No test attempt by any student of that institution in that domain in the last 14 days, AND
2. Domain coverage % (how much of the domain's series they have accessed) < 40%

This combination means they subscribed but are not using the domain — likely candidate for cancellation.

**Institution Table — 9 columns**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Institution Name | Link to institution profile | Yes | With type icon (school/college/coaching) |
| Type | Badge | Yes | School · College · Coaching · Group |
| Plan Tier | Badge | Yes | Starter · Standard · Professional · Enterprise |
| Student Count | Integer | Yes | Enrolled students in this domain |
| Adoption Score | 0–100 gauge bar | Yes | Composite: logins + attempts + completion + coverage |
| Domain Coverage % | Colour-coded % | Yes | % of domain's series/topics accessed |
| Last Activity | Relative time | Yes | "2 days ago" / "3 weeks ago" |
| Churn Risk | ⚠ red badge or — | Yes | Badge shown if criteria met |
| Actions | Link | No | "View Profile →" on hover |

**Adoption Score Breakdown (tooltip on hover):**
- Login frequency: 25 points
- Exam attempts per student: 25 points
- Completion rate: 25 points
- Content coverage breadth: 25 points

**Empty State:** "No institutions subscribed to this domain" with "Go to Institution Management" link.

**Pagination:**
- "Showing X–Y of Z institutions"
- Page pills + Previous / Next
- Per-page selector: 10 / 25 / 50 / 100

---

## Compare Mode Panel

Hidden by default. Activated by the "Compare Domains" toggle button in the page header. When activated, a panel slides down below the main content grid.

**Controls (all in one row):**

| Control | Options |
|---|---|
| Domain checkboxes | All 8 domains listed, each with its colour dot. Default: SSC, RRB, NEET pre-checked. Maximum 6 can be selected simultaneously. |
| Metric selector | Enrollment / Test Attempts / Avg Score / Coverage % / Completion Rate |
| Period selector | Last 30 days / Last 90 days / Last 12 months |

**Compare Chart:**
- Multi-line chart, one line per selected domain
- Each line coloured with its domain colour
- X-axis: date labels for selected period
- Y-axis: selected metric value
- Legend shows domain name + current value
- Tooltip on hover: date, all domain values at that date
- Chart updates immediately when any checkbox or selector changes

---

## Domain Detail Drawer (720px wide, right side)

Opened by clicking the "→" icon on any domain card in the sidebar grid. Slides in from the right. Backdrop overlay dims the rest of the page.

**Drawer Header:**
- Domain name with colour dot
- Category badge (Central Govt / Medical / Engineering / State Board / Banking)
- "View in Exam Domain Config →" quick link
- Close button (×)

**5 Tabs inside the Drawer:**

### Drawer Tab 1 — Overview

**4 Stat Cards (top row):**
- Total Questions: approved questions in this domain
- Active Series: test series with status active
- Active Institutions: subscribed + active institutions
- Last Updated: most recent config change timestamp

**Exam Categories Table:**

| Column | Detail |
|---|---|
| Category Name | With shortcode |
| Series Count | Active test series for this category |
| Avg Score | Average across all attempts |
| Monthly Attempts | Attempts in last 30 days |
| Enrollments | Total enrolled |
| Status | Active / Inactive badge |

**Domain Description:**
- Full text description of the domain
- Target audience (e.g. "Central government job aspirants: SSC exams target 10th/12th pass candidates applying for Group C/D posts")
- Typical exam frequency (e.g. "2–3 official exams per year per category")

### Drawer Tab 2 — Coverage

**Horizontal Bar Chart — Per Subject:**
- One bar per subject in this domain
- Sorted ascending (lowest coverage first — worst at top for action priority)
- Bar labelled: Subject name · Coverage % · Question count
- Bar colour: green/amber/orange/red matching coverage threshold

**Coverage Summary Stats:**
- Subjects with ≥80% coverage: count
- Subjects with <25% coverage: count (shown in red)
- Most recent question added: timestamp + topic name
- Content team members assigned to this domain: count

### Drawer Tab 3 — Top Performers

Two tables side-by-side:

**Left: Top 10 Institutions by Adoption Score**

| Column | Detail |
|---|---|
| Rank | 1–10 with medal icons for top 3 |
| Institution | Name + type badge |
| Adoption Score | 0–100 |
| Student Count | Domain-enrolled students |

**Right: Top 10 Institutions by Student Count**

| Column | Detail |
|---|---|
| Rank | 1–10 |
| Institution | Name + type badge |
| Students | Count |
| Completion Rate | % of students who completed at least 1 series |

### Drawer Tab 4 — Trends

**12-Month Enrollment Trend:**
- Line chart: monthly enrollment count for this domain over last 12 months
- Points at month boundaries with values labelled

**12-Month Attempt Trend:**
- Line chart: monthly attempt count (started) over last 12 months
- Secondary line: monthly submissions

**Month-over-Month Change Table:**

| Month | Enrollments | MoM Change | Attempts | MoM Change | Avg Score |
|---|---|---|---|---|---|
| Mar 2026 | 12,450 | +8.3% | 84,230 | +12.1% | 52.4% |
| Feb 2026 | 11,495 | +3.1% | 75,134 | +5.7% | 51.8% |
| Jan 2026 | 11,148 | +15.6% | 71,078 | +18.2% | 50.9% |
| … | … | … | … | … | … |

### Drawer Tab 5 — Quick Actions

- "View Full Analytics" → closes drawer, navigates to this page with domain pre-selected
- "Open in Exam Domain Config" → navigates to page 09 with domain pre-selected
- "Open in Syllabus Builder" → navigates to page 10 filtered by domain
- "Assign Gap Tasks" → opens gap assignment workflow for this domain
- "Export Domain Report" → PDF download covering all analytics for this domain

---

## Data Refresh Strategy

| Section | Refresh Interval | Cache TTL | Notes |
|---|---|---|---|
| KPI strip | Every 120s | 120s Redis | Paused if drawer or modal is open |
| Domain grid sidebar | Every 120s | 120s Redis | Same pause guard |
| Enrollment chart | On domain / period change | 300s Redis | Key: domain + period |
| Attempt chart | On domain / period change | 300s Redis | Key: domain + period |
| Coverage heatmap | On domain change | 300s Redis | Expensive — node aggregation |
| Score distribution | On domain + exam_cat change | 300s Redis | Key: domain + exam_cat |
| Gap analysis list | On domain change | 300s Redis | Sorted server-side |
| Series table | On filter / search / page change | None | Always live — pagination |
| Institution table | On filter / search / page change | None | Always live — pagination |
| Compare chart | On any control change | 300s Redis | Key: domains[] + metric + period |

---

## Export — PDF Report Contents

When "Export PDF" is clicked, the report includes:

1. Cover page: Domain name, period, exported by (admin name), export timestamp
2. KPI summary table (all 6 KPIs)
3. Enrollment trend chart (image)
4. Attempt funnel stats
5. Score distribution histogram (image) + percentile table
6. Coverage heatmap summary (image)
7. Top 10 gap topics table
8. Top 10 series by enrollment
9. Top 10 institutions by adoption score
10. Churn risk institutions list

Report is generated server-side using a background Celery task. User receives a download link via in-portal notification when ready (typically < 30 seconds).

---

## Permissions

| Codename | Who Has It | What It Allows |
|---|---|---|
| view_domain_analytics | PM Exam Domains, PM Platform | View all tabs and charts |
| export_domain_analytics | PM Exam Domains, PM Platform | Export PDF reports |
| view_gap_analysis | PM Exam Domains, PM Platform | View gap analysis tab |
| assign_gap_task | PM Exam Domains | Assign gap remediation to team members |
| compare_domains | PM Exam Domains, PM Platform | Use domain comparison panel |

---

## Business Rules

1. **Coverage % calculation:** Average of `coverage_pct` across all active topic-level syllabus nodes for the domain. A topic node's `coverage_pct` = (approved questions for this topic / recommended minimum questions) × 100, capped at 100%.

2. **Adoption score formula:** (login_frequency_score × 0.25) + (attempt_score × 0.25) + (completion_score × 0.25) + (coverage_breadth_score × 0.25). Each sub-score is normalised to 0–100.

3. **Churn risk threshold:** 14 days of inactivity + domain coverage < 40%. Both conditions must be true. Configurable by PM Exam Domains in settings.

4. **Exam frequency data source:** Historical official exam paper metadata stored in `ExamPaperTopic` table. Tagged manually by content team when uploading official papers.

5. **Score distribution scope:** Only submitted attempts are counted. Abandoned (started but not submitted) are excluded from score stats but included in the attempt funnel.

6. **Series completion rate:** Submitted attempts / Started attempts per series. Not student completion of the series (some students enroll but never start an exam — those do not affect completion rate, they affect attempt rate).

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| Domain selector | 8-tab bar, not dropdown | 8 fits inline; instant switch via HTMX without page reload |
| Domain grid sidebar | Always-visible left panel | Cross-domain comparison without losing active tab state |
| Heatmap approach | Subject × Chapter grid with colour cells | Instantly surfaces chapter-level gaps at a glance |
| Gap severity | Coverage % + exam frequency combined | High-frequency + low-coverage = highest student impact |
| Score distribution | 20-bucket histogram + percentile table | Histogram for shape; table for precise percentile planning |
| Compare mode | Slide-down panel below main | Advanced feature; keeps default view uncluttered |
| Churn risk filter | 14-day inactivity + coverage < 40% | Objective, actionable threshold for customer success team |
| Series/institution tables | No cache — live paginated query | Must be accurate; stale institution data misleads |
| Compare chart max 6 | Prevents line chart from becoming unreadable | More than 6 overlapping lines are indistinguishable |
| PDF export async | Celery background task | 2M+ record aggregation cannot block the web request |

---

## Amendment G11 — Benchmarking Section

**Gap:** No comparison of platform content coverage against official syllabi or past exam papers. PM Exam Domains has no visibility into whether the question bank covers 60% or 95% of the syllabus, and no data on whether question difficulty distribution matches historical paper patterns. This leads to institution churn ("your question bank doesn't cover the full syllabus") that cannot be objectively addressed.

### New Section: "Benchmarking" (per-domain tab, below Heatmap)

Available in each domain tab (SSC, NEET, JEE, etc.) as a collapsible section triggered by `[Show Benchmarking ▼]`.

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│ BENCHMARKING — SSC CGL                               [Refresh] [Export PDF]    │
│ Question bank coverage vs official syllabus · Difficulty vs past papers        │
├───────────────────────────────────────────────────────────┬─────────────────────┤
│ SYLLABUS COVERAGE                                         │ OVERALL COVERAGE    │
│                                                           │                     │
│ Tier 1 — General Intelligence & Reasoning                 │   ██████████░ 91%  │
│  ├─ Analogies             ████████████ 100%               │                     │
│  ├─ Coding-Decoding       ████████████ 100%               │ Tier 1:  94%       │
│  ├─ Blood Relations       ██████████░░  84%               │ Tier 2:  88%       │
│  ├─ Matrix               ████████░░░░  68%                │ Tier 3:  72%       │
│  └─ [8 more topics...]                                    │ Tier 4:  91%       │
│                                                           │                     │
│ Tier 1 — General Awareness                               │ 🟡 2 gaps below 70% │
│  ├─ Current Affairs (2024) ████████░░░  79%               │ [View all gaps]     │
│  ├─ History               ████████████ 100%               │                     │
│  ├─ Geography             ███████████░  92%               │                     │
│  └─ [6 more topics...]                                    │                     │
│                                                           │                     │
│ Tier 1 — Quantitative Aptitude                           │                     │
│  ├─ Simple Interest       ████████████ 100%               │                     │
│  ├─ Data Interpretation   ██████░░░░░░  54%  ← ⚠️ GAP    │                     │
│  └─ [10 more topics...]                                   │                     │
├───────────────────────────────────────────────────────────┴─────────────────────┤
│ DIFFICULTY DISTRIBUTION vs PAST PAPERS                                          │
│                                                                                 │
│ Compare platform question difficulty against SSC CGL papers:                   │
│ Reference paper: [SSC CGL 2024 Tier 1 ▼] (latest available)                   │
│                                                                                 │
│ ┌─────────────────────────────────────────────────────────────────────────────┐ │
│ │ Difficulty │ Past Paper │ Platform Bank │ Gap        │                     │ │
│ ├────────────┼────────────┼───────────────┼────────────┤                     │ │
│ │ Easy       │    35%     │     48%       │ +13% ↑     │ Too many easy Qs    │ │
│ │ Medium     │    45%     │     38%       │ -7%  ↓     │ Slight shortage     │ │
│ │ Hard       │    20%     │     14%       │ -6%  ↓     │ Hard Qs deficit     │ │
│ └─────────────────────────────────────────────────────────────────────────────┘ │
│ Recommendation: Add ~800 Hard questions in Quant & Reasoning to match paper    │
│                 distribution. Reduce Easy question proportion in GK section.   │
│                                                                                 │
│ QUESTION AGE vs PAST PAPERS                                                     │
│  Questions updated after 2023: 78%  |  Pre-2020 questions: 8% (flag for review)│
│  Past paper overlap (Q bank vs official papers): 2.3% duplication detected    │
│  (Questions identical to official past papers — should be flagged/removed)     │
│  [View Duplicate Matches] [Flag All for Review]                                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### Syllabus Coverage Data Model

Benchmarking data is maintained as a structured syllabus imported from official sources and mapped to question topics:

```python
class OfficialSyllabus(models.Model):
    """Master syllabus imported from official exam bodies."""
    exam_domain = models.CharField(max_length=50)  # SSC, NEET, JEE, etc.
    exam_name = models.CharField(max_length=200)   # SSC CGL, SSC CHSL, etc.
    tier_or_paper = models.CharField(max_length=50, blank=True)  # Tier 1, Tier 2
    version = models.CharField(max_length=20)      # 2024, 2025
    source_url = models.URLField(blank=True)
    is_current = models.BooleanField(default=True)
    imported_at = models.DateTimeField(auto_now_add=True)
    imported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


class SyllabusSection(models.Model):
    """Hierarchical section of an official syllabus."""
    syllabus = models.ForeignKey(
        OfficialSyllabus, on_delete=models.CASCADE, related_name='sections'
    )
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True, related_name='children'
    )
    name = models.CharField(max_length=200)
    order = models.PositiveSmallIntegerField(default=0)
    # Mapped to platform topic taxonomy
    mapped_topic_ids = models.JSONField(default=list)


class SyllabusCoverageSnapshot(models.Model):
    """Nightly computed coverage metrics per syllabus section."""
    syllabus = models.ForeignKey(OfficialSyllabus, on_delete=models.CASCADE)
    section = models.ForeignKey(SyllabusSection, on_delete=models.CASCADE)
    total_subtopics = models.IntegerField()
    covered_subtopics = models.IntegerField()
    coverage_pct = models.DecimalField(max_digits=5, decimal_places=2)
    question_count = models.IntegerField()
    computed_at = models.DateField()

    class Meta:
        unique_together = ('syllabus', 'section', 'computed_at')
        ordering = ['-computed_at', 'section__order']


class PastPaperDifficultyBenchmark(models.Model):
    """Difficulty distribution from official past papers — manually entered."""
    syllabus = models.ForeignKey(OfficialSyllabus, on_delete=models.CASCADE)
    paper_year = models.PositiveSmallIntegerField()
    easy_pct = models.DecimalField(max_digits=5, decimal_places=2)
    medium_pct = models.DecimalField(max_digits=5, decimal_places=2)
    hard_pct = models.DecimalField(max_digits=5, decimal_places=2)
    source_notes = models.TextField(blank=True)
    entered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    entered_at = models.DateTimeField(auto_now_add=True)
```

### Celery Task

```python
@shared_task(queue='analytics')
def compute_syllabus_coverage():
    """
    Runs nightly at 03:00 IST.
    For each active OfficialSyllabus, compute coverage_pct per section
    by counting questions tagged with mapped_topic_ids.
    """
    today = date.today()
    for syllabus in OfficialSyllabus.objects.filter(is_current=True):
        for section in syllabus.sections.filter(parent__isnull=False):
            topic_ids = section.mapped_topic_ids
            q_count = Question.objects.filter(
                topic_id__in=topic_ids,
                status='published'
            ).count()
            subtopics = len(topic_ids) or 1
            covered = min(subtopics, q_count // 5)  # heuristic: 5 Qs per subtopic = covered
            coverage_pct = Decimal(covered) / Decimal(subtopics) * 100

            SyllabusCoverageSnapshot.objects.update_or_create(
                syllabus=syllabus,
                section=section,
                computed_at=today,
                defaults={
                    'total_subtopics': subtopics,
                    'covered_subtopics': covered,
                    'coverage_pct': coverage_pct,
                    'question_count': q_count,
                }
            )
```

### Coverage Threshold Alerts

- Section with `coverage_pct < 70%` → flagged as gap (amber in heatmap, listed in gap panel)
- Section with `coverage_pct < 40%` → critical gap (red), email to PM Exam Domains lead
- PM can set custom threshold per domain: `[Coverage alert threshold: 70% ▼]`

### Past Paper Overlap Detection

Nightly task compares `Question.text` (normalised, stopwords stripped) against stored past paper question text using MinHash LSH (locality-sensitive hashing). Matches above 85% similarity flagged as duplicates, surfaced in the "Question Age vs Past Papers" row. PM can review and remove or re-author flagged questions.
