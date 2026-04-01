# Page 31: Demo-to-Admission Conversion Tracker

**URL:** `/group/adm/demo/conversion/`
**Template:** `portal_base.html` (light theme)
**Division:** C — Group Admissions
**Module:** Demo Classes

---

## 1. Purpose

The Demo-to-Admission Conversion Tracker is the ROI measurement center for the entire demo class program. It answers the most important question any admissions leader can ask: of all the students who sat through a demo class, how many ultimately enrolled? Conversion tracking transforms demo classes from a feel-good activity into a measurable, accountable admissions engine. The Admissions Director reviews this page to evaluate whether the demo program is generating enrollment returns proportionate to the faculty time, venue cost, and coordination effort invested.

The page models the prospect journey as a structured funnel: Demo Attended → Enquiry Registered → Application Submitted → Counselled → Offered Admission → Enrolled. At each stage, prospects either advance or fall out. The funnel chart makes the drop-off points visually explicit — if 40% of demo attendees never register an enquiry, the gap is in post-demo follow-up, not in counselling quality. If 80% of counselled prospects are offered admission but only 30% enroll, the issue is in fee negotiation or competition from rival institutes. Each funnel stage becomes a specific operational problem to solve, not an amorphous "conversion issue."

Beyond the aggregate funnel, the page provides granular breakdowns by branch and by demo teacher. Branch-level conversion data reveals which branches have strong demo-to-enrollment pipelines and which are staging demos that generate interest but fail to close. Teacher-level conversion data (not just feedback ratings, but actual enrollment outcomes from sessions they conducted) is the most rigorous measure of a demo teacher's business impact. The Unconverted Prospects Table drives daily follow-up actions — it lists every demo attendee who hasn't yet applied, with their last contact date and follow-up count, enabling the counselling team to prioritize outreach before prospects go cold.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Demo Class Coordinator (29) | G3 | Full — view all, manage follow-ups, assign counsellors | Primary owner |
| Group Admissions Director (23) | G3 | Full — view all + trigger follow-up escalations | Strategic oversight, approves write-offs |
| Group Admission Coordinator (24) | G3 | View-only across all branches | No follow-up assignment |
| Group Admission Counsellor (25) | G3 | View own assigned prospects only | Cannot see other counsellors' pipelines |

Access enforcement: All views protected with `@login_required` and `@role_required(['demo_coordinator', 'admissions_director', 'admission_coordinator', 'admission_counsellor'])`. Counsellor scope enforced by filtering `unconverted_prospects` queryset to `assigned_counsellor = request.user`.

---

## 3. Page Layout

### 3.1 Breadcrumb
`Group Portal → Admissions → Demo Classes → Conversion Tracker`

### 3.2 Page Header
**Title:** Demo-to-Admission Conversion Tracker
**Subtitle:** Track how demo attendees progress from enquiry to enrollment
**Actions (right-aligned):**
- `[Export Conversion Report CSV]` — secondary button
- Cycle selector (dropdown): "Current Admission Cycle" / "Previous Cycle" / custom date range

### 3.3 Alert Banner

| Condition | Banner Type | Message |
|---|---|---|
| Overall conversion rate drops > 5% vs last cycle | Warning (amber) | "Conversion rate has dropped 6% compared to last admission cycle. Review branch breakdowns." |
| Unconverted prospects > 90 days since demo with no contact | Error (red) | "N prospects have not been contacted for over 90 days since their demo. These are at risk of being lost permanently." |
| Best-performing branch for the week | Success (green) | "[Branch Name] achieved the highest enrollment conversion rate this week at [X]%." |

---

## 4. KPI Summary Bar

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Demo Attendees (This Cycle) | COUNT distinct prospects who attended at least one demo | `demo_attendance` | Blue always | Filters branch table to all |
| Converted to Application % | COUNT applied / COUNT attended × 100 | `demo_attendance` JOIN `applications` | Green if ≥ 40%; amber if 25–39%; red if < 25% | Scrolls to funnel chart |
| Converted to Enrollment % | COUNT enrolled / COUNT attended × 100 | `demo_attendance` JOIN `enrollments` | Green if ≥ 25%; amber if 15–24%; red if < 15% | Scrolls to funnel chart |
| Best-Converting Branch | Branch name with highest enrollment conversion % | `branches` analytics | Blue always | Filters branch table to highlight |
| Best-Converting Demo Teacher | Teacher name with highest application conversion from their sessions | `demo_sessions` analytics | Blue always | Scrolls to teacher leaderboard |
| Avg Days Demo → Application | AVG (application_date − demo_date) for converted prospects | `applications` JOIN `demo_attendance` | Green if ≤ 7; amber if 8–14; red if > 14 | No drill-down |

**HTMX auto-refresh pattern (every 5 minutes):**
```html
<div id="kpi-bar"
     hx-get="/group/adm/demo/conversion/kpis/"
     hx-trigger="load, every 300s"
     hx-target="#kpi-bar"
     hx-swap="outerHTML">
  <!-- KPI cards rendered here -->
</div>
```

---

## 5. Sections

### 5.1 Conversion Funnel Chart

**Display:** Full-width staged funnel visualization (Chart.js 4.x — custom funnel plugin or horizontal bar implementation). Shows the full prospect journey from left to right.

**Stages:**
1. Demo Attended
2. Enquiry Registered
3. Application Submitted
4. Counselled
5. Offered Admission
6. Enrolled

**For each stage:** Absolute count displayed inside the bar; percentage of the stage-1 total shown below.

**Drop-off annotations:** Between each stage, drop-off count and percentage shown (e.g., "−340 / 28% drop-off" between stages 1 and 2).

**Interactivity:** Clicking a funnel stage segment filters the Unconverted Prospects Table (Section 5.3) to show prospects currently stuck at that stage. HTMX: `hx-get="/group/adm/demo/conversion/unconverted/?stage=X"` targeting `#unconverted-table`.

**Period selector:** Toggle buttons above chart — Current Cycle / Last Month / Last Quarter. Change reloads chart via `hx-get`.

---

### 5.2 Branch-wise Conversion Table

**Display:** Sortable server-side paginated table (20/page). Default sort: Enrolled% descending.

**Columns:**

| Column | Notes |
|---|---|
| Branch | Branch name |
| Demo Attendees | Total demo attendees this cycle |
| Applied (%) | Applied / Attended × 100 (colour-coded) |
| Counselled (%) | Counselled / Applied × 100 |
| Enrolled (%) | Enrolled / Attended × 100 (primary metric — colour-coded) |
| Avg Days (Demo → Enroll) | Average calendar days for enrolled prospects |
| Revenue from Demo Conversions (₹) | Total fees collected from demo-originated enrollments |
| Action | `[View Prospects →]` — opens branch-conversion-detail drawer |

**Sort:** All numeric columns sortable.

**HTMX:** `hx-get="/group/adm/demo/conversion/branch-table/"` on load and on sort change, `hx-target="#branch-conversion-table"`.

**Empty state:** "No conversion data available for the selected cycle."

---

### 5.3 Unconverted Prospects Table

**Display:** Sortable, server-side paginated (20/page). Lists demo attendees who have not yet submitted an application. Sorted by days since demo descending by default (most stale at top).

**Columns:**

| Column | Notes |
|---|---|
| Name | Prospect name |
| Branch | Demo branch |
| Demo Date | Date of most recent demo attended |
| Stream Interest | Declared interest |
| Days Since Demo | Calculated; colour: amber > 7 days; red > 14 days |
| Follow-up Count | Number of follow-up calls/contacts logged |
| Last Contact | Date of last contact attempt |
| Reason (if known) | Free text or dropdown reason code (e.g., "Undecided" / "Joined competitor" / "Fee concern") |
| Action | `[Schedule Follow-up →]` `[Mark Lost →]` |

**Filters:**
- Branch (dropdown)
- Days since demo (< 7 / 7–14 / > 14 / > 30 / All)
- Follow-up count (0 / 1–2 / 3+ / All)
- Stream interest

**Bulk actions:** `[Assign Counsellor to Selected]` (dropdown → counsellor name) | `[Export Selected]`

**HTMX:** Filter changes → `hx-get="/group/adm/demo/conversion/unconverted/"` targeting `#unconverted-table`. Stage click from funnel also targets this table.

**Empty state:** "All demo attendees for this cycle have either applied or been marked as lost."

---

### 5.4 Conversion Timeline Analysis

**Display:** Chart.js 4.x line chart. X-axis: days elapsed since demo (0–60 days). Y-axis: cumulative % of eventual converters who had applied by that day. Shows how quickly applicants move after attending a demo.

**Two series:**
- Current cycle (solid line)
- Previous cycle (dashed line, lighter colour)

**Annotations:** Vertical reference line at day 7 ("Most conversions happen within 7 days") and day 30 ("High urgency threshold").

**Interpretation text below chart:** Auto-generated summary, e.g.: "52% of converted prospects applied within 7 days of their demo. Only 8% converted after 30+ days."

**HTMX:** `hx-get="/group/adm/demo/conversion/timeline/"` lazy-loaded on section scroll.

---

### 5.5 Teacher Conversion Rate Leaderboard

**Display:** Sortable table of all demo teachers ranked by application conversion rate (prospects who applied / prospects who attended their sessions × 100).

**Columns:**

| Column | Notes |
|---|---|
| Rank | # |
| Teacher | Name |
| Branch | Home branch |
| Subject | Demo subject |
| Sessions Conducted | Total sessions this cycle |
| Attendees | Total prospects attended |
| Applied from Sessions | Count who applied after attending |
| Application Rate % | Colour-coded: green ≥ 40%; amber 25–39%; red < 25% |
| Enrolled from Sessions | Count who enrolled |
| Enrollment Rate % | Final conversion metric |

**HTMX:** `hx-get="/group/adm/demo/conversion/teacher-leaderboard/"` on section load.

**Empty state:** "No teacher conversion data available for the selected cycle."

---

## 6. Drawers & Modals

### 6.1 `prospect-journey` Drawer
**Width:** 560px
**Trigger:** `[View Prospects →]` in branch table or direct prospect link
**HTMX endpoint:** `hx-get="/group/adm/demo/conversion/prospect/{prospect_id}/"` lazy-loaded
**Content (timeline view):**
- Vertical timeline: Demo Attended → Enquiry Registered → Follow-up Log → Application Submitted → Counselling Session → Offer → Enrollment / Lost
- Each timeline node shows: date, action taken, notes, responsible staff
- Current stage highlighted
- `[Add Follow-up Note]` inline form at bottom

---

### 6.2 `conversion-follow-up` Drawer
**Width:** 400px
**Trigger:** `[Schedule Follow-up →]` in unconverted prospects table
**HTMX endpoint:** `hx-get="/group/adm/demo/conversion/follow-up/{prospect_id}/"` lazy-loaded
**Content:**
- Prospect name, branch, stream interest, days since demo, follow-up count
- Contact method (Call / WhatsApp / Email)
- Call outcome (if calling now): Interested / Needs more time / Fee concern / Joining elsewhere / No answer
- Notes textarea
- Next follow-up date (date picker)
- Assign to counsellor (dropdown)
- `[Save & Schedule]`

---

### 6.3 `branch-conversion-detail` Drawer
**Width:** 560px
**Trigger:** `[View Prospects →]` in branch conversion table
**HTMX endpoint:** `hx-get="/group/adm/demo/conversion/branch/{branch_id}/"` lazy-loaded
**Tabs:**
1. **Funnel** — Branch-specific funnel chart (same structure as Section 5.1)
2. **Prospects** — Paginated list of all demo attendees from this branch with conversion status
3. **Teachers** — Teacher conversion rates within this branch only

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Follow-up scheduled | "Follow-up scheduled for [Name] on [Date]." | Success | 4s |
| Prospect marked as Lost | "[Name] marked as lost. Reason recorded." | Warning | 4s |
| Counsellor assigned | "Counsellor [Name] assigned to N prospects." | Success | 3s |
| Prospect journey note saved | "Follow-up note added to [Name]'s journey." | Success | 2s |
| Export triggered | "Conversion report is being prepared." | Info | 3s |
| Bulk assign completed | "Counsellor assigned to N selected prospects." | Success | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No demo attendance data yet | Funnel outline | "No demo data for this cycle" | "Conversion data will appear once demo sessions have recorded attendance." | `[Go to Attendance →]` |
| No unconverted prospects | Checkmark circle | "All prospects have converted or been closed" | "Every demo attendee has either applied or been marked as lost." | None |
| Branch table — no data | Branch icon | "No branch data for this cycle" | "Branch conversion data populates after demo attendance is submitted." | None |
| Prospect journey — no follow-ups logged | Timeline empty | "No follow-up history" | "No follow-up actions have been logged for this prospect yet." | `[Add First Note]` |
| Teacher leaderboard — no sessions | Trophy outline | "No sessions conducted this cycle" | "Teacher conversion rates will appear after demo sessions are completed." | None |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load (KPI bar) | Skeleton cards (6 cards, grey shimmer) |
| Funnel chart loading | Skeleton funnel bars (6 stages, grey shimmer) |
| Branch conversion table loading | Skeleton rows (5 rows) |
| Unconverted prospects table loading | Skeleton rows (5 rows) |
| Conversion timeline chart loading | Skeleton chart area |
| Teacher leaderboard loading | Skeleton rows (4 rows) |
| Drawer opening (any) | Spinner centred in drawer body |
| Follow-up save | Button spinner + disabled state |
| Bulk assign in progress | Button spinner + "Assigning…" label |
| KPI auto-refresh | Subtle pulse on KPI cards |

---

## 10. Role-Based UI Visibility

All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Demo Coordinator (29) | Admissions Director (23) | Admission Coordinator (24) | Admission Counsellor (25) |
|---|---|---|---|---|
| Funnel chart — all branches | Visible | Visible | Visible | Visible (own assigned only) |
| Branch conversion table — all branches | Visible | Visible | Visible | Hidden |
| Unconverted prospects — all | Visible | Visible | Visible | Own assigned only |
| `[Mark Lost →]` action | Visible | Visible | Hidden | Hidden |
| `[Assign Counsellor]` bulk action | Visible | Visible | Hidden | Hidden |
| Teacher conversion leaderboard | Visible | Visible | Visible | Hidden |
| `[Export Conversion Report CSV]` | Visible | Visible | Visible | Hidden |
| Revenue column in branch table | Visible | Visible | Hidden | Hidden |
| Prospect journey drawer — all prospects | Visible | Visible | Hidden | Own assigned only |
| Cycle selector dropdown | Visible | Visible | Visible | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/kpis/` | JWT G3+ | KPI bar metrics |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/funnel/` | JWT G3+ | Funnel stage counts for chart |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/branch-table/` | JWT G3+ | Branch-wise conversion data |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/branch/{branch_id}/` | JWT G3+ | Single branch detail |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/unconverted/` | JWT G3+ | Unconverted prospects list with filters |
| PATCH | `/api/v1/group/{group_id}/adm/demo/conversion/unconverted/{id}/mark-lost/` | JWT G3 write | Mark prospect as lost |
| POST | `/api/v1/group/{group_id}/adm/demo/conversion/unconverted/assign-counsellor/` | JWT G3 write | Bulk assign counsellor |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/timeline/` | JWT G3+ | Conversion timeline data |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/teacher-leaderboard/` | JWT G3+ | Teacher conversion rates |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/prospect/{id}/` | JWT G3+ | Prospect journey timeline |
| POST | `/api/v1/group/{group_id}/adm/demo/conversion/prospect/{id}/follow-up/` | JWT G3 write | Log follow-up action |
| GET | `/api/v1/group/{group_id}/adm/demo/conversion/export/` | JWT G3+ | Export conversion report CSV |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 300s` | GET `/group/adm/demo/conversion/kpis/` | `#kpi-bar` | `outerHTML` |
| Funnel stage click → filter unconverted table | `click` on funnel bar | GET `/group/adm/demo/conversion/unconverted/?stage=X` | `#unconverted-table` | `innerHTML` |
| Period selector change (funnel chart) | `click` on period toggle | GET `/group/adm/demo/conversion/funnel/?period=P` | `#funnel-chart-container` | `innerHTML` |
| Branch table sort/paginate | `click` on sort header or page link | GET `/group/adm/demo/conversion/branch-table/?sort=X&page=N` | `#branch-conversion-table` | `innerHTML` |
| Unconverted table filter change | `change` on filter input | GET `/group/adm/demo/conversion/unconverted/` | `#unconverted-table` | `innerHTML` |
| Unconverted table pagination | `click` on page link | GET `/group/adm/demo/conversion/unconverted/?page=N` | `#unconverted-table` | `innerHTML` |
| Conversion timeline lazy load | `intersect` (section scrolls into view) | GET `/group/adm/demo/conversion/timeline/` | `#timeline-chart-container` | `innerHTML` |
| Teacher leaderboard load | `load` | GET `/group/adm/demo/conversion/teacher-leaderboard/` | `#teacher-leaderboard` | `innerHTML` |
| Open prospect journey drawer | `click` on `[View Prospects →]` / prospect link | GET `/group/adm/demo/conversion/prospect/{id}/` | `#drawer-container` | `innerHTML` |
| Open follow-up drawer | `click` on `[Schedule Follow-up →]` | GET `/group/adm/demo/conversion/follow-up/{id}/` | `#drawer-container` | `innerHTML` |
| Submit follow-up | `submit` in drawer | POST `/group/adm/demo/conversion/prospect/{id}/follow-up/` | `#unconverted-row-{id}` | `outerHTML` |
| Mark prospect lost | `click` (after inline confirm) | PATCH `/group/adm/demo/conversion/unconverted/{id}/mark-lost/` | `#unconverted-row-{id}` | `outerHTML` |
| Open branch detail drawer | `click` on `[View Prospects →]` in branch table | GET `/group/adm/demo/conversion/branch/{id}/` | `#drawer-container` | `innerHTML` |
| Bulk assign counsellor | `click` on bulk action confirm | POST `/group/adm/demo/conversion/unconverted/assign-counsellor/` | `#unconverted-table` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
