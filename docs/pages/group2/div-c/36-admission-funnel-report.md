# Page 36 — Admission Funnel Report

**URL:** `/group/adm/reports/funnel/`
**Template:** `portal_base.html`
**App:** `group_admissions`
**Django View:** `AdmissionFunnelReportView`

---

## 1. Purpose

The admission funnel report is the single most important analytical view for the Group Admissions Director. It tracks every stage of the admission pipeline from initial enquiry through to final enrollment, quantifying drop-off rates at each transition. For a group targeting 10,000 new enrollments per year across multiple branches and streams, the Director must know precisely where the funnel is leaking — whether enquiries are not converting to applications, whether counselling sessions are not generating offers, whether offers are being rejected, or whether certain counsellors are underperforming relative to peers. This report answers all these questions in a single consolidated view, filterable by branch, stream, date range, and individual counsellor.

The report surfaces five discrete pipeline stages: Enquiry, Application, Counselled, Offered, and Enrolled. At each transition, the absolute count of records passing through and the percentage conversion from the prior stage are displayed. The complementary drop-off count between stages allows the Director to quantify the magnitude of leakage. Stage Bottleneck Heatmap and Source-wise Funnel breakdowns further decompose the data to reveal structural weaknesses — whether a specific lead source converts poorly, whether a specific branch consistently stalls at the Counselled → Offered stage, or whether time-in-stage metrics exceed agreed service-level agreements. These insights directly drive counsellor training, branch resource allocation, and marketing channel decisions.

The Trend Analysis section adds a temporal dimension by comparing weekly and monthly enrollment counts for the current admission cycle against the previous cycle, with a projected forecast line. The Counsellor Performance Table ranks individual counsellors on assigned enquiries, generated applications, completed sessions, conversions, and average days to convert, enabling the Director to reward high performers and support those lagging behind. The Export Panel allows the Director to download a PDF-formatted report for board presentations or export raw data for deeper offline analysis, and to schedule an automated monthly email delivery of the report to the Director's inbox.

---

## 2. Role Access

| Role | Level | Access | Notes |
|---|---|---|---|
| Group Admissions Director (Role 23) | G3 | Full — all filters, all export, schedule email | Primary owner of this report |
| Group Admission Coordinator (Role 24) | G3 | View only — all data visible, no schedule | Cannot schedule automated email delivery |
| Group CEO | G3 | View only — read all data | Accessed via CEO dashboard shortcut |
| Group Analytics Director | G3 | View only — all data | Read access for cross-function analysis |
| Group CAO | G3 | View only — all data | Academic oversight context |
| Group Scholarship Manager (Role 27) | G3 | View only — own scholarship funnel sections | Limited to scholarship-related funnel stages |
| Branch Principal | Branch | No access | Branch-level funnel visible in branch admission pages |

**Enforcement:** Access control is enforced server-side in Django using `@role_required` decorator on `AdmissionFunnelReportView`. Queryset filtering scopes data to the authenticated user's permitted branches. No client-side role logic is used.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group Portal > Admissions > Reports & Analytics > Admission Funnel Report
```

### 3.2 Page Header

| Element | Detail |
|---|---|
| Page title | Admission Funnel Report |
| Subtitle | Cross-branch pipeline analysis · [Current cycle label, e.g. AY 2025-26] |
| Header actions | [Filter Panel] [Download PDF] [Export CSV] [Schedule Report] |
| Cycle selector | Dropdown — current cycle pre-selected; historical cycles selectable |
| Last refreshed | Timestamp with [Refresh Now] button |

### 3.3 Alert Banner

Displayed contextually above KPI bar when triggered.

| Trigger | Message | Severity |
|---|---|---|
| End-to-end conversion rate drops below 20% | "Overall funnel conversion has dropped below 20%. Review counsellor performance and branch drop-off stages immediately." | Critical (red) |
| Any branch shows 0 enrollments in current month | "One or more branches have zero enrollments this month. Check pipeline status for affected branches." | Warning (amber) |
| Any stage SLA exceeded by >50% across 3+ branches | "Pipeline bottleneck detected: [Stage] is averaging [X] days across [N] branches — exceeds SLA by [Y] days." | Warning (amber) |
| Report data not refreshed in >24 hours | "Funnel data may be stale. Last sync: [timestamp]. Contact MIS team if data is delayed." | Info (blue) |
| No data for selected filter combination | "No funnel data found for the selected filters. Adjust branch, stream, or date range." | Info (blue) |

---

## 4. KPI Summary Bar

Refreshes automatically via HTMX every 5 minutes (`hx-trigger="load, every 5m"`).

| Card | Metric | Source | Colour Rule | Drill-down |
|---|---|---|---|---|
| Total Enquiries | Count of all enquiry records in selected cycle/filter | `AdmissionEnquiry` table | Neutral (blue) | Opens Stage Bottleneck Heatmap filtered to Enquiry stage |
| Enquiry → Application Rate | (Applications / Enquiries) × 100 | Derived | Green ≥40% · Yellow 25–39% · Red <25% | Opens 5.2 Branch-wise Funnel Comparison filtered to this transition |
| Application → Offer Rate | (Offers / Applications) × 100 | Derived | Green ≥60% · Yellow 40–59% · Red <40% | Opens 5.3 Counsellor Performance Table |
| Offer → Enrollment Rate | (Enrollments / Offers) × 100 | Derived | Green ≥75% · Yellow 50–74% · Red <50% | Opens 5.2 filtered to Offer → Enrolled transition |
| End-to-End Conversion | (Enrollments / Enquiries) × 100 | Derived | Green ≥15% · Yellow 8–14% · Red <8% | Opens 5.1 Funnel Visualization |
| Avg Days per Stage | Arithmetic mean of stage-duration across all active records | `AdmissionPipelineLog` | Green ≤7d · Yellow 8–14d · Red >14d | Opens 5.4 Stage Bottleneck Heatmap |

---

## 5. Sections

### 5.1 Funnel Visualization

Large centred funnel chart rendered via Chart.js 4.x. Funnel stages displayed top to bottom:

**Stages:** Enquiry → Application → Counselled → Offered → Enrolled

For each stage node:
- Absolute count (e.g., 8,450)
- Percentage conversion from previous stage (e.g., "62% of applications")
- Drop-off count between stages shown in the connector area (e.g., "▼ 3,200 dropped")

**Filter bar above chart:**
| Filter | Type | Options |
|---|---|---|
| Branch | Multi-select dropdown | All branches + individual |
| Stream | Multi-select | MPC / BiPC / MEC / CEC / Commerce / Humanities |
| Date Range | Date picker (from/to) | Default: current cycle start to today |
| Counsellor | Dropdown | All / individual counsellors |

Filter changes trigger HTMX partial reload of the funnel chart container. Chart.js re-renders on data update.

Below the funnel chart, a summary sentence: "Based on current filters, [X] enquiries entered the pipeline; [Y] enrolled — an end-to-end conversion of [Z]%."

### 5.2 Branch-wise Funnel Comparison

Sortable table listing every branch in the group.

| Column | Description |
|---|---|
| Branch | Branch name + city |
| Enquiries | Total enquiry count |
| Applications | Count at Application stage |
| Counselled | Count at Counselled stage |
| Offered | Count at Offered stage |
| Enrolled | Final enrolled count |
| End-to-End % | (Enrolled / Enquiries) × 100 |
| Action | [View Branch Funnel →] — opens branch-funnel-detail drawer |

Sorting: All columns sortable. Default sort: Enrolled descending.
Pagination: 20 rows per page, HTMX-paginated.
Row colour coding: Green if end-to-end ≥ group average; Yellow if 75–99% of group average; Red if <75% of group average.

### 5.3 Counsellor Performance Table

Table listing all active counsellors across permitted branches.

| Column | Description |
|---|---|
| Counsellor Name | Full name + branch |
| Enquiries Assigned | Total enquiries assigned to this counsellor |
| Applications Generated | Applications created from their assigned enquiries |
| Sessions Completed | Counselling sessions logged |
| Conversions | Final enrollments attributed to this counsellor |
| Conversion % | (Conversions / Enquiries Assigned) × 100 |
| Avg Days to Convert | Mean days from enquiry assignment to enrollment |
| Action | [View Profile →] — opens counsellor-performance-detail drawer |

Sorting: Conversion % descending by default. Counsellors with <10 assigned enquiries marked with a footnote.
Top 3 counsellors highlighted with a gold/silver/bronze badge in their name cell.

### 5.4 Stage Bottleneck Heatmap

Matrix table: Rows = Branches · Columns = Pipeline Stages (Enquiry→Application · Application→Counselled · Counselled→Offered · Offered→Enrolled)

Each cell contains: Average days spent in that stage for that branch.

Colour scale:
- White / light green: Within SLA (≤7 days per stage)
- Amber: 8–14 days (approaching SLA breach)
- Red: >14 days (SLA breached)

SLA thresholds configurable by Director in Admission Season Configuration (page 39 §5.5). Default SLA is 7 days per stage.

Clicking a red/amber cell opens an inline tooltip showing: avg days, count of records in this stage, oldest record date, and a [View Records →] link that filters the Application Pipeline (page 08) to matching records.

### 5.5 Source-wise Funnel

Separate mini-funnel for each lead source. Lead sources: Walk-in · Demo Class · Alumni Referral · Online (website/social) · School Fair · Agent Referral · Cold Outreach.

Each mini-funnel is rendered as a compact horizontal bar chart (Chart.js) showing count and conversion % at each stage for that source. Below each mini-funnel: a summary conversion rate badge and a "Best converting source" indicator if applicable.

Sort order: Sources sorted by end-to-end conversion rate descending so the most effective channels appear first.

Clicking any source bar opens the source-funnel-detail drawer with full stage breakdown, branch distribution for that source, and time-trend chart.

### 5.6 Trend Analysis

Line chart (Chart.js 4.x) showing:
- **This cycle:** Weekly or monthly enrolled count (toggle selector)
- **Last cycle:** Corresponding period's enrolled count (dashed line)
- **Forecast line:** Linear projection based on current cycle trend (dotted line, extends to cycle end date)

X-axis: Time (weeks or months).
Y-axis: Enrollment count.
Chart legend: "AY 2025-26 (Current)" · "AY 2024-25 (Previous)" · "Forecast"

Below the chart: delta indicator — "Currently [ahead/behind] last cycle by [N] enrollments at this point. Projected final enrollment: [X] vs target [Y]."

### 5.7 Export Panel

Three export actions displayed as a card with descriptive sub-text:

| Action | Description |
|---|---|
| [Download PDF Report] | Generates a formatted PDF of all visible sections with current filters applied. Includes charts as images. Django generates via WeasyPrint. |
| [Export Raw Data CSV] | Exports the underlying record-level data (anonymised where required) for the selected filter combination. |
| [Schedule Monthly Email] | Director-only. Opens a modal to configure: recipient email(s), day of month to send, report sections to include. Stores schedule in `ReportSchedule` model. |

---

## 6. Drawers & Modals

| ID | Width | Tabs | HTMX Endpoint |
|---|---|---|---|
| `branch-funnel-detail` | 640px | Overview · Counsellors · Stage Timeline · Notes | `GET /api/v1/group/{group_id}/adm/reports/funnel/branch/{branch_id}/` |
| `counsellor-performance-detail` | 480px | Pipeline Summary · Stage Breakdown · History · Notes | `GET /api/v1/group/{group_id}/adm/reports/funnel/counsellor/{user_id}/` |
| `source-funnel-detail` | 480px | Funnel Chart · Branch Distribution · Trend · Notes | `GET /api/v1/group/{group_id}/adm/reports/funnel/source/{source_slug}/` |
| `schedule-report-modal` | 440px (modal) | Configuration · Recipients · History | `POST /api/v1/group/{group_id}/adm/reports/schedule/` |

All drawers slide in from the right. Overlay backdrop dims the main content. Drawer content loaded via HTMX on open trigger; subsequent tab switches load tab content independently.

---

## 7. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| PDF download initiated | "Generating PDF report. Download will start shortly." | Info | 4s |
| PDF generated and ready | "PDF report ready. Downloading now." | Success | 3s |
| PDF generation failed | "PDF generation failed. Please retry or contact support." | Error | 6s |
| CSV export initiated | "Preparing CSV export…" | Info | 3s |
| CSV export ready | "CSV export downloaded successfully." | Success | 3s |
| Monthly schedule saved | "Monthly report schedule saved. First delivery: [date]." | Success | 5s |
| Monthly schedule save failed | "Could not save report schedule. Please try again." | Error | 6s |
| Report data refreshed | "Funnel data refreshed successfully." | Success | 3s |
| Filter applied | "Filters applied. Funnel updated." | Info | 2s |
| No data for filter | "No records found for the selected filters." | Warning | 4s |

---

## 8. Empty States

| Condition | Illustration | Heading | Description | CTA |
|---|---|---|---|---|
| No enquiries in selected cycle | Funnel icon with dashed outline | "No Pipeline Data" | "No enquiry records exist for the selected cycle and filters." | [Clear Filters] [Select a Different Cycle] |
| No counsellors assigned in branch filter | Person icon with question mark | "No Counsellors Found" | "No counsellors are assigned for the selected branch and date range." | [Manage Counsellors] |
| Source-wise funnel: no records for a source | Empty bar chart | "No Data for This Source" | "No enquiries from this source in the selected period." | [Change Date Range] |
| Trend chart: only current cycle data (no prior cycle) | Line chart with single line | "No Comparison Data" | "Prior cycle data is not available for this filter combination." | [View Current Cycle Only] |
| Report schedule list empty | Calendar icon | "No Scheduled Reports" | "You have not scheduled any automated report deliveries." | [Schedule Monthly Email] |

---

## 9. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | Full-page skeleton: KPI bar shimmer + funnel chart placeholder + table row skeletons |
| KPI bar auto-refresh (every 5m) | Inline spinner on each KPI card; cards retain last value during refresh |
| Filter applied to funnel chart | Funnel container overlay spinner; chart fades to 40% opacity |
| Branch-wise table pagination | Table body skeleton rows (3 rows) while next page loads |
| Drawer open | Drawer content area full-height skeleton with tab bar shimmer |
| PDF generation | Button changes to "Generating…" with spinner; disabled state |
| CSV export | Button spinner for duration of export preparation |
| Trend chart load | Chart container shimmer placeholder matching chart height |

---

## 10. Role-Based UI Visibility

> All UI visibility decisions made server-side in Django template. No client-side JS role checks.

| UI Element | Director (23) | Coordinator (24) | CEO | Analytics Director | CAO | Scholarship Manager (27) |
|---|---|---|---|---|---|---|
| All filter controls | Visible + active | Visible + active | Visible + active | Visible + active | Visible + active | Visible — limited to scholarship stages |
| Export: Download PDF | Visible | Visible | Visible | Visible | Visible | Hidden |
| Export: Export CSV | Visible | Visible | Visible | Visible | Visible | Hidden |
| Export: Schedule Monthly Email | Visible | Hidden | Hidden | Hidden | Hidden | Hidden |
| Counsellor Performance Table | Full — all counsellors | Full | Full | Full | Full | Hidden |
| Branch-wise Funnel — [View Branch Funnel →] | Visible | Visible | Visible | Visible | Visible | Hidden |
| Stage Bottleneck Heatmap cell click → View Records | Visible | Visible | Hidden | Visible | Hidden | Hidden |
| Source-wise Funnel — all sources | Visible | Visible | Visible | Visible | Visible | Visible (scholarship source only) |
| Trend Analysis forecast line | Visible | Visible | Visible | Visible | Visible | Hidden |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/` | JWT | Fetch full funnel report data for selected cycle and filters |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/kpi/` | JWT | KPI summary bar data only (used for 5-minute auto-refresh) |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/branch/{branch_id}/` | JWT | Branch-specific funnel detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/counsellor/{user_id}/` | JWT | Counsellor pipeline detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/source/{source_slug}/` | JWT | Source-wise funnel detail for drawer |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/bottleneck/` | JWT | Stage bottleneck heatmap matrix data |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/trend/` | JWT | Trend analysis data (current + previous cycle + forecast) |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/export/pdf/` | JWT | Generate and stream PDF report |
| GET | `/api/v1/group/{group_id}/adm/reports/funnel/export/csv/` | JWT | Generate and stream CSV raw data |
| POST | `/api/v1/group/{group_id}/adm/reports/schedule/` | JWT | Create or update a report schedule (Director only) |
| GET | `/api/v1/group/{group_id}/adm/reports/schedule/` | JWT | List existing report schedules |
| DELETE | `/api/v1/group/{group_id}/adm/reports/schedule/{schedule_id}/` | JWT | Delete a report schedule |

---

## 12. HTMX Patterns

| Interaction | hx-trigger | hx-method + URL | hx-target | hx-swap |
|---|---|---|---|---|
| KPI bar auto-refresh | `load, every 5m` | `GET /api/v1/group/{group_id}/adm/reports/funnel/kpi/` | `#funnel-kpi-bar` | `innerHTML` |
| Apply filter panel | `click` on [Apply Filters] | `GET /group/adm/reports/funnel/?branch=…&stream=…` | `#funnel-main-content` | `innerHTML` |
| Branch comparison table — next page | `click` on pagination control | `GET /group/adm/reports/funnel/branches/?page=N` | `#branch-comparison-table` | `innerHTML` |
| Open branch-funnel-detail drawer | `click` on [View Branch Funnel →] | `GET /api/v1/group/{group_id}/adm/reports/funnel/branch/{branch_id}/` | `#drawer-content` | `innerHTML` |
| Open counsellor-performance-detail drawer | `click` on counsellor name | `GET /api/v1/group/{group_id}/adm/reports/funnel/counsellor/{user_id}/` | `#drawer-content` | `innerHTML` |
| Open source-funnel-detail drawer | `click` on source funnel element | `GET /api/v1/group/{group_id}/adm/reports/funnel/source/{source_slug}/` | `#drawer-content` | `innerHTML` |
| Drawer tab switch | `click` on drawer tab | `GET /group/adm/reports/funnel/drawer-tab/?tab=…&id=…` | `#drawer-tab-content` | `innerHTML` |
| Refresh report data manually | `click` on [Refresh Now] | `GET /api/v1/group/{group_id}/adm/reports/funnel/` | `#funnel-main-content` | `innerHTML` |
| Trend chart — toggle week/month | `change` on toggle | `GET /api/v1/group/{group_id}/adm/reports/funnel/trend/?period=week\|month` | `#trend-chart-container` | `innerHTML` |
| Schedule report modal — submit | `submit` on form | `POST /api/v1/group/{group_id}/adm/reports/schedule/` | `#schedule-modal-response` | `innerHTML` |

---

*Page spec version: 1.0 · Last updated: 2026-03-21*
