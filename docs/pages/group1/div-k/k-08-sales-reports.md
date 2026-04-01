# K-08 — Sales Reports

**Route:** `GET /group1/k/reports/`
**Method:** Django `TemplateView` + HTMX part-loads per report tab
**Primary role:** B2B Sales Manager (#57)
**Also sees:** Sales Ops Analyst (#95 — full access, read-only), Sales Executives #58–60 (own-data reports only, no Quota tab)

---

## Purpose

**Viewport:** Desktop-only. Report charts (Chart.js) require minimum 800px width for readable funnel bars. Cohort table with 6+ columns requires horizontal scroll on narrower viewports. Not optimized for mobile.

Analytics hub for the Sales division. Provides win/loss analysis, funnel conversion rates, lead source attribution, quota attainment summary, activity volume reports, and cohort analysis — all in one consolidated view. At 2,050 institutions and with deal sizes ranging from ₹80K to ₹5L+ ARR, even a 5-percentage-point improvement in funnel conversion translates to significant revenue. All reports use pre-aggregated data from `analytics_sales_funnel` where possible; live queries are used only for drill-down exports to avoid page latency. The Manager uses this page for weekly pipeline reviews, monthly board decks, and diagnosing specific funnel bottlenecks. The Sales Ops Analyst uses it for quota reporting and attribution analysis. Sales Executives can review their own funnel and activity data but cannot see team-wide metrics or peers' performance.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Funnel conversion | `analytics_sales_funnel` (pre-aggregated by Celery Task K-1 every 6 hours — NOT nightly). Cache TTL: 1 hour. | 1 hour |
| Win/loss detail (charts) | `sales_lead` aggregated WHERE `won_at` or `lost_at` IS NOT NULL | 1 hour |
| Win/loss drill-down table | `sales_lead` live query (used only on tab open + export) | No cache |
| Lead source attribution | `sales_lead` GROUP BY `lead_source` | 1 hour |
| Quota attainment | `sales_quota` + `sales_lead` actuals | 15 min |
| Activity volume | `sales_activity` GROUP BY `activity_type`, `owner_id`, `date_trunc` | 1 hour |
| Cohort analysis | `sales_lead` GROUP BY DATE_TRUNC('month', created_at) vs won_at | Nightly Celery |

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?report` | `funnel`, `winloss`, `source`, `quota`, `activity`, `cohort` | `funnel` | Active report tab |
| `?period_from` | ISO date (YYYY-MM-DD) | First day of current quarter | Report start date |
| `?period_to` | ISO date (YYYY-MM-DD) | Today | Report end date |
| `?segment` | `all`, `school`, `college`, `coaching` | `all` | Institution segment filter |
| `?owner` | `user_id` | `all` (Manager/Ops) or self (Exec) | Exec-level filter |
| `?territory` | Territory string | `all` | Territory filter |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/k/reports/funnel/` | Funnel chart + table | Filter apply | `#k-report-content` |
| `htmx/k/reports/winloss/` | Win/loss charts | Tab switch + filter | `#k-report-content` |
| `htmx/k/reports/source/` | Lead source chart | Tab switch + filter | `#k-report-content` |
| `htmx/k/reports/quota-summary/` | Quota grid | Period change, 15 min | `#k-report-content` |
| `htmx/k/reports/activity/` | Activity volume chart | Tab switch + filter | `#k-report-content` |
| `htmx/k/reports/cohort/` | Cohort table | Period change | `#k-report-content` |

Note: All report tabs share `#k-report-content` as target — the tab switch completely replaces the content area. The tab bar itself (`#k-report-tabs`) is NOT swapped — only the content below it.

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  SALES REPORTS                         [Export All Reports ↓]   │
│  [From: 01 Jan 2026 ▼]  [To: 21 Mar 2026 ▼]                    │
│  [Segment: All ▼]  [Exec: All ▼]  [Territory: All ▼]  [Apply]  │
├─────────────────────────────────────────────────────────────────┤
│  [Funnel][Win/Loss][Lead Source][Quota][Activity][Cohort]        │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  FUNNEL CONVERSION (default view)                               │
│                                                                  │
│  Prospect ████████████████████████ 250  →78%→  Contacted        │
│  Contacted ████████████████ 195   →52%→  Demo Scheduled         │
│  Demo Scheduled ██████████ 101    →65%→  Demo Done              │
│  Demo Done ████████ 66            →70%→  Proposal Sent          │
│  Proposal Sent ██████ 46          →70%→  Negotiation            │
│  Negotiation ████ 32              →58%→  Closed Won             │
│  Closed Won ███ 18                                               │
│                                                                  │
│  Overall Lead-to-Close: 7.2%                                     │
│                                                                  │
│  Stage     │ Entered │ Won → │ Dropped │ Med.Days │ Conv %       │
│  Prospect    250       195      55       2.1        78%          │
│  ...                                                             │
│                                    [Export Funnel CSV ↓]        │
└─────────────────────────────────────────────────────────────────┘
```

---

## Components

### 1. Global Filters Bar

Persisted across tab switches within the session.

```
[From: 01 Jan 2026 ▼]  [To: 21 Mar 2026 ▼]
[Segment: All ▼]  [Exec: All ▼]  [Territory: All ▼]  [Apply]  [Clear]
```

- **From / To:** Date pickers. Default: first day of current quarter → today. Max range warning if > 12 months (see Toast Messages).
- **Segment:** All / School / College / Coaching.
- **Exec:** Manager (#57) and Ops (#95) see all exec names. Sales Exec sees own name only (dropdown disabled with "Your data").
- **Territory:** All / individual territory strings from `sales_lead.territory`.
- **[Apply]:** Triggers HTMX reload of currently active report tab. Other tabs reload lazily on next click.
- **[Clear]:** Resets all filters to defaults. Refreshes active tab.

---

### 2. Report Tab Bar

Six tabs. Active tab underlined + bold. Clicking tab updates `?report=` URL param and loads the HTMX partial for that tab.

```
[Funnel ◼]  [Win/Loss]  [Lead Source]  [Quota]  [Activity]  [Cohort]
```

Sales Executives (#58–60) do not see the Quota tab (redirect to K-07 own quota row if navigated directly via URL).

---

### 3. Tab: Funnel Conversion Report

Loaded via `htmx/k/reports/funnel/`. Source: `analytics_sales_funnel` pre-aggregated.

**Chart:**
Chart.js horizontal bar chart (funnel/waterfall style). Each stage shows a proportionally scaled bar based on lead count that entered that stage during the period. Conversion % annotated between consecutive stage bars.

```
PROSPECT          ██████████████████████████ 250
                   ↓ 78% progressed
CONTACTED         ████████████████████ 195
                   ↓ 52% progressed
DEMO_SCHEDULED    ██████████ 101
                   ↓ 65% completed
DEMO_DONE         ██████ 66
                   ↓ 70% moved forward
PROPOSAL_SENT     ████ 46
                   ↓ 70% entered negotiation
NEGOTIATION       ███ 32
                   ↓ 58% closed won
CLOSED_WON        ██ 18     (7.2% overall lead-to-close)
```

Hovering a stage bar: tooltip "DEMO_SCHEDULED — 101 leads entered; 66 advanced; 35 dropped/lost."

**Summary table** below chart:

| Stage | Entered | Advanced | Dropped | Median Days in Stage | Conversion % |
|---|---|---|---|---|---|
| PROSPECT | 250 | 195 | 55 | 2.1 days | 78% |
| CONTACTED | 195 | 101 | 94 | 5.3 days | 52% |
| DEMO_SCHEDULED | 101 | 66 | 35 | 4.2 days | 65% |
| DEMO_DONE | 66 | 46 | 20 | 7.0 days | 70% |
| PROPOSAL_SENT | 46 | 32 | 14 | 9.5 days | 70% |
| NEGOTIATION | 32 | 18 | 14 | 12.0 days | 58% |
| CLOSED_WON | 18 | — | — | — | — |

- **Overall lead-to-close rate** displayed prominently below table: "Overall: [N] of [total] leads closed — [%]%"
- **Stage row click:** Deep-link to K-02 Pipeline view pre-filtered to that stage + current filters. Opens in new tab.
- **[Export Funnel CSV]:** Generates CSV with all table columns. Filename: `funnel-report-[from]-[to].csv`.

**Lead-to-close rate edge cases:**
- 0 leads created in period → entire funnel shows "No data for this period. Adjust date range or filters." empty state. No chart rendered.
- Leads created but none closed → shows funnel with CLOSED_WON = 0. Overall rate shows "0%" in amber with tooltip "No deals closed in this period."
- <5 leads at any stage → that stage shows "Low data" tooltip: "Fewer than 5 leads — statistics may not be representative."
- Division by zero in conversion % (0 leads entered a stage) → shows "—" not "0%".

**Chart interactivity:**
- Legend: Positioned below the funnel chart. When multiple execs selected (Manager view), each exec has a legend entry with colour dot. Clicking legend item toggles that exec's data on/off in the chart.
- Click-through: Clicking a stage bar navigates to K-02 with `?stage=[stage]&period_from=[from]&period_to=[to]` params pre-applied. Opens in same tab (hx-boost false — full page navigation to K-02).
- Tooltip on hover: "DEMO_SCHEDULED — 101 leads entered; 66 advanced (65%); 35 dropped/lost." Appears within 300ms on mouse-over.
- Mobile: Touch tap opens tooltip; second tap navigates to K-02 drill-down.

---

### 4. Tab: Win/Loss Analysis

Loaded via `htmx/k/reports/winloss/`. Two sub-charts side by side with a detail table below.

**Left sub-chart — Win/Loss Ratio Donut:**

```
        CLOSED_WON   ████ 18 deals  ₹74L
        CLOSED_LOST  ████████ 32 deals  ₹120L
        Win Rate: 36%  |  Win Rate by ARR: 38%
```

Chart.js donut. Centre label shows win rate %. Toggle between "by deal count" and "by ARR value" with a small toggle button.

Below donut: breakdown table by segment:

| Segment | Won Deals | Lost Deals | Win Rate % | Won ARR |
|---|---|---|---|---|
| School | 10 | 18 | 36% | ₹38L |
| College | 6 | 11 | 35% | ₹27L |
| Coaching | 2 | 3 | 40% | ₹9L |

**Right sub-chart — Lost Reason Breakdown:**

Chart.js horizontal bar chart. Each bar: one `lost_reason` enum value with count and % of total lost.

Colour coding:
- PRICE_TOO_HIGH = red
- COMPETITOR_WON = orange
- BUDGET_CUT = amber
- FEATURE_GAP = indigo
- TIMING_NOT_RIGHT = blue
- NO_RESPONSE = grey
- WENT_INHOUSE = purple
- TENDER_LOST = teal

Tooltip: "COMPETITOR_WON — 9 deals (28% of lost)"

**Lost Deals Detail Table** — below both charts. Live query. Sortable. Max 100 rows; "Load More" on scroll. Default sort: lost_at DESC (most recently lost deals first). Sortable by: institution_name (A–Z), arr_estimate (high to low), lost_at (newest/oldest), stage_at_loss.

| Column | Detail |
|---|---|
| Institution Name | Text; link → K-03 Account Profile |
| Segment | SCHOOL / COLLEGE / COACHING badge |
| Stage Lost At | Which stage was active when `stage` moved to CLOSED_LOST |
| Owner | Exec name |
| ARR Estimate | `arr_estimate_paise` formatted |
| Lost Reason | Colour-coded badge matching chart |
| Lost Date | `lost_at` formatted |

**[Export Win/Loss CSV]:** All rows including `institution_name`, `segment`, `stage_lost_at`, `owner`, `arr`, `lost_reason`, `lost_at`. Filename: `winloss-report-[from]-[to].csv`.

---

### 5. Tab: Lead Source Attribution

Loaded via `htmx/k/reports/source/`.

**Pie chart:**
Chart.js pie chart. Slices: each distinct `lead_source` value. Default: by CLOSED_WON deal count. Toggle button: "By Deal Count" / "By ARR Value" — swaps pie values without full reload.

Tooltip: "REFERRAL — 28 deals, 42% of total won ARR"

**Attribution table:**

| Lead Source | Leads Created | Deals Won | Win Rate % | Total ARR Won | Avg Deal Size | Avg Sales Cycle (days) |
|---|---|---|---|---|---|---|
| REFERRAL | 40 | 28 | 70% | ₹31.2L | ₹1.11L | 42 |
| INBOUND_FORM | 80 | 22 | 27% | ₹18.5L | ₹84K | 68 |
| CHANNEL_PARTNER | 35 | 18 | 51% | ₹14.0L | ₹78K | 55 |
| COLD_OUTREACH | 95 | 12 | 13% | ₹9.8L | ₹82K | 74 |
| CONFERENCE | 20 | 8 | 40% | ₹7.2L | ₹90K | 51 |
| GOVT_TENDER | 5 | 2 | 40% | ₹5.6L | ₹2.8L | 115 |

**Key Insight Callout** — computed on render, shown in an indigo info card above table:

```
┌──────────────────────────────────────────────────────────────────┐
│  ℹ  Top source this period: REFERRAL — 42% of ARR from 28% of   │
│     leads. Highest win rate (70%). Shortest sales cycle (42d).  │
└──────────────────────────────────────────────────────────────────┘
```

Logic: source with highest `total_arr_won` wins the callout. Secondary stat: source with highest win rate noted if different.

**[Export Source CSV]:** Filename: `source-attribution-[from]-[to].csv`.

---

### 6. Tab: Quota Attainment Summary

Loaded via `htmx/k/reports/quota-summary/`. Uses 15-min cache. Period selector within this tab overrides global date range (since quota periods are fixed monthly/quarterly, not arbitrary date ranges).

**Period selector within tab:**

```
[◀ Mar 2026 ▶]  [Monthly ▼]   (mirrors K-07 period selector)
```

**Attainment table** — report-format version of K-07 quota data:

| Exec | Segment | Period | Target Deals | Actual | Attainment % | Target ARR | Actual ARR | ARR Attainment % | Trend |
|---|---|---|---|---|---|---|---|---|---|
| Rahul Sharma | SCHOOL | Mar 2026 | 10 | 8 | 80% | ₹35L | ₹28L | 80% | → |
| Priya Nair | COLLEGE | Mar 2026 | 10 | 6 | 60% | ₹35L | ₹21L | 60% | ↓ |
| Suresh Reddy | COACHING | Mar 2026 | 5 | 5 | 100% | ₹25L | ₹25L | 100% | ↑ |
| Arjun Das | INBOUND | Mar 2026 | 20 | 14 | 70% | ₹50L | ₹35L | 70% | → |

**Trend column:** Compares current period attainment % vs previous period: ↑ (improved ≥5pp) / ↓ (declined ≥5pp) / → (within ±5pp). Green/red/grey icons.

**Historical comparison:** Additional columns for last 2 prior periods shown in lighter grey. Allows side-by-side comparison without switching periods.

**Historical bar chart** — below table:

Chart.js grouped bar chart. X-axis: last 6 periods. Y-axis: ARR. One bar group per period showing each exec as a different colour. Dotted line per exec: their target for that period. Toggle by exec name via legend.

**[Export Quota Report CSV]:** All periods × execs in the current filter range. Filename: `quota-report-[period_type]-[year].csv`.

---

### 7. Tab: Activity Volume Report

Loaded via `htmx/k/reports/activity/`. Source: `sales_activity` table.

**Stacked bar chart:**

```
Activity Volume — Week by Week (Jan–Mar 2026)

Count ▲
  60 │ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗ ╔══╗
  40 │ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
  20 │ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║ ║  ║
     └─ W1  W2  W3  W4  W5  W6  W7  W8  W9  W10 W11 W12
     ■ CALL  ■ EMAIL  ■ MEETING  ■ DEMO  ■ PROPOSAL  ■ NOTE
```

- X-axis: weeks (if range ≥ 14 days) or days (if range < 14 days)
- Each bar is stacked by `activity_type`
- Toggle by exec via legend (Manager/Ops see all; Exec sees own)
- Hover tooltip: "Week of 10 Mar — Rahul: 12 calls, 8 emails, 3 meetings = 23 activities"

**Activity summary table** — below chart:

| Exec | CALL | EMAIL | MEETING | DEMO | PROPOSAL | TOTAL | Avg per Lead | Deals Closed |
|---|---|---|---|---|---|---|---|---|
| Rahul Sharma | 48 | 32 | 12 | 8 | 6 | 106 | 4.2 | 8 |
| Priya Nair | 31 | 28 | 9 | 6 | 5 | 79 | 3.4 | 6 |
| Suresh Reddy | 22 | 14 | 8 | 5 | 5 | 54 | 5.2 | 5 |
| Arjun Das | 62 | 45 | 7 | 14 | 12 | 140 | 3.1 | 14 |

**Insight callout** (computed on render):

```
┌──────────────────────────────────────────────────────────────────┐
│  ℹ  Execs who logged ≥ 3 activities per lead before sending a   │
│     proposal had a 40% higher close rate this period.           │
│     Rahul (4.2 acts/lead) closed 80% of proposals sent.        │
└──────────────────────────────────────────────────────────────────┘
```

Computed: correlation between `Avg per Lead` and win rate using current period data. Shown only if ≥ 2 execs' data is available for comparison.

**[Export Activity CSV]:** All activity rows with `exec`, `activity_type`, `date`, `lead_id`, `institution_name`. Filename: `activity-report-[from]-[to].csv`.

---

### 8. Tab: Cohort Analysis

Loaded via `htmx/k/reports/cohort/`. Source: nightly Celery job. Read-only; no exec filter (always team-level).

**Monthly cohort table** — rows are months when leads were created; columns are months elapsed since creation (Month 0 through Month 6+):

```
Cohort (Created)  M+0    M+1    M+2    M+3    M+4    M+5    M+6   Med.Close
Oct 2025          100%   72%    58%    41%    28%    22%    18%   91 days
Nov 2025          100%   68%    55%    38%    24%    —      —     — (ongoing)
Dec 2025          100%   74%    61%    42%    —      —      —     — (ongoing)
Jan 2026          100%   69%    54%    —      —      —      —     — (ongoing)
Feb 2026          100%   71%    —      —      —      —      —     — (ongoing)
Mar 2026          100%   —      —      —      —      —      —     — (ongoing)
```

**Cell values:** Percentage of that cohort's leads still active (not CLOSED_LOST) or already CLOSED_WON. Cell colour: green (high retention / fast closure) → yellow → red (high drop-off). Heat-map colouring using viridis-inspired scale.

**Median Close column:** Median days from `created_at` to `won_at` for leads that closed won. "—" for cohorts still maturing.

**Reading the table:** Declining % across a row = leads dropping out over time. Steeper decline = faster attrition. Comparisons across rows show seasonality: Jan cohort converting 54% at M+2 vs Oct cohort at 58% suggests Jan leads are slightly weaker quality.

**Key observations card** (auto-generated):

```
┌──────────────────────────────────────────────────────────────────┐
│  ℹ  Oct 2025 cohort (most mature): 18% closed won at 6 months — │
│     in line with overall lead-to-close rate. Nov–Dec cohorts    │
│     are tracking slightly below Oct at same age, suggesting     │
│     Q4 leads may need additional nurturing.                     │
└──────────────────────────────────────────────────────────────────┘
```

**[Export Cohort CSV]:** Full cohort matrix. Filename: `cohort-analysis-[year].csv`.

---

### 9. Export All Reports Button

Positioned at top right, always visible regardless of active tab.

```
[Export All Reports ↓]
```

On click: triggers async export job. Downloads ZIP containing all 6 report CSVs for current filter settings.

- **Sync (date range ≤ 3 months):** ZIP generated immediately; browser download initiated.
- **Async (date range > 3 months):** "Export queued. You'll receive an email at [user_email] when the export is ready. Large exports may take up to 10 minutes." Toast shown. Email dispatched with download link (pre-signed S3 URL, 24-hour expiry) when Celery job completes.

Individual tab-level export buttons (within each report) are always synchronous and generate only that report's data regardless of global date range.

**Export All Reports ZIP contents:**
File structure inside ZIP:
```
eduforge_sales_report_[YYYYMMDD]_[from]_[to].zip
├── 01_funnel_conversion.csv
│   Columns: Stage, Count Entered, Count Advanced, Count Dropped, Conversion %, Median Days in Stage
├── 02_win_loss_analysis.csv
│   Columns: Institution Name, Type, Segment, Stage at Loss, Owner, ARR ₹, Won/Lost At, Lost Reason, Lead Source
├── 03_lead_source_attribution.csv
│   Columns: Lead Source, Leads Created, Deals Won, Win Rate %, Total ARR ₹, Avg Deal Size ₹, Avg Sales Cycle (days)
├── 04_quota_attainment.csv
│   Columns: Exec Name, Segment, Period, Target Deals, Actual Deals, Attainment %, Target ARR ₹, Actual ARR ₹, ARR Attainment %
├── 05_activity_volume.csv
│   Columns: Exec Name, Week, CALL, EMAIL, MEETING, DEMO, PROPOSAL, RFP_RESPONSE, SITE_VISIT, TOTAL, Deals Closed
└── 06_cohort_analysis.csv
    Columns: Cohort Month, Total Leads, Month 1 Active %, Month 2 Active %, Month 3 Active %, Month 6 Active %, Closed Won %, Median Days to Close
```

Async threshold: If date range > 3 months OR total leads > 500, export is async. User receives "Export queued" amber toast + email notification with download link (valid 24 hours, S3 pre-signed URL) when ready.
Sync threshold: date range ≤ 3 months AND total leads ≤ 500 → immediate download.

**Export threshold check:**
- Client-side: When date range is selected (on Apply), JS computes date range in days. If > 90 days (3 months), amber inline notice shows below the date pickers: "Large date range — export may be queued for background processing." This is informational only.
- Server-side: POST /group1/k/reports/export/ receives the filter params. Server queries COUNT(sales_lead WHERE filters). If count > 500 OR date range > 90 days: responds 202 Accepted with job_id (async). Else: responds 200 with CSV stream (sync). Client handles both: 202 → show amber toast + polling for email; 200 → trigger browser download.

---

## Empty States

| Condition | Message |
|---|---|
| No leads created in period (Funnel tab) | "No leads created between [from] and [to] matching the current filters." |
| No closed deals in period (Win/Loss tab) | "No closed deals in the selected period. Adjust the date range to see win/loss data." |
| No activity data (Activity tab) | "No activity logged in this period. Activities are recorded when Sales Execs log calls, emails, and meetings from lead profiles." |
| Cohort data insufficient | "Not enough data for cohort analysis — at least 2 months of lead history required." |
| Quota tab with no quota records | "No quotas set for this period. Go to Territory & Quota to set targets." with [Go to K-07 →] link |
| Lead source — all deals in one source | Full table shown; pie chart shows single slice with note "All won deals sourced from [source] in this period." |
| Filter combination returns no data | "No data matches the current filters. Try broadening the date range or removing segment/exec filters." |

---

## Toast Messages

| Action | Toast |
|---|---|
| Export started (sync) | No toast — browser download dialog appears |
| Export queued (async) | "Export queued. You'll receive an email at [email] when ready." (blue) |
| Export ready (email link clicked, return to page) | "Your sales report export is ready. [Download ↓]" (green) — shown if returning via notification link |
| Filters applied | No toast — silent HTMX reload |
| Date range > 12 months selected | "Date ranges over 12 months may take longer to load. Consider narrowing the range for faster results." (amber) |
| Individual report export done | No toast — immediate file download |

---

---

## Authorization

**Route guard:** `@division_k_required(allowed_roles=[57, 95, 58, 59, 60])` applied to `SalesReportsView`.

| Scenario | Behaviour |
|---|---|
| Sales Manager (#57) | Full access — all tabs, all execs, export all |
| Sales Ops (#95) | Full read-only — all tabs, all execs, export all |
| Sales Execs (#58–60) | All tabs visible but data filtered to `owner_id = request.user.id`. Quota tab replaced with direct link to K-07 own quota row. Export scoped to own data only. |
| Inside Sales Exec (#97) | No access — 403 redirect |
| All other roles | 403 Forbidden |
| Export ALL endpoint POST `/k/reports/export/` | Only #57 and #95. Execs get 403 on "Export All" button; "Export My Data" is separate endpoint `/k/reports/export/own/`. |
| HTMX partial routes | Same role restrictions. Direct partial calls without session return 403. |

## Role-Based View Summary

| Feature | #57 Manager | #95 Ops Analyst | #58–60 Execs | #61/62/63/96/97 |
|---|---|---|---|---|
| Funnel tab | Full — all execs | Full — read-only | Own data only | No access |
| Win/Loss tab | Full | Full — read-only | Own data only | No access |
| Lead Source tab | Full | Full — read-only | Own data only | No access |
| Quota tab | Full | Full — read-only | No access (→ K-07) | No access |
| Activity tab | Full — all execs | Full — read-only | Own data only | No access |
| Cohort tab | Full (team-level) | Full — read-only | No access | No access |
| Exec filter (`?owner=`) | All exec options | All exec options | Own ID locked | No access |
| Export individual report | Yes | Yes | Yes (own data only) | No |
| Export All Reports ZIP | Yes | Yes | No | No |
| Async export (>3 months) | Yes | Yes | No | No |
