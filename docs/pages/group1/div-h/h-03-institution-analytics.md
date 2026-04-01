# H-03 — Institution Analytics

> **Route:** `/analytics/institutions/`
> **Division:** H — Data & Analytics
> **Primary Role:** Analytics Manager (42) · Data Analyst (44)
> **Supporting Roles:** Platform Admin (10) — full
> **File:** `h-03-institution-analytics.md`
> **Priority:** P1 — churn detection and engagement health monitoring

---

## 1. Page Name & Route

**Page Name:** Institution Analytics
**Route:** `/analytics/institutions/`
**Part-load routes:**
- `/analytics/institutions/?part=summary-bar` — summary KPI bar
- `/analytics/institutions/?part=geo-map` — India choropleth map
- `/analytics/institutions/?part=engagement-table` — institution engagement table
- `/analytics/institutions/{institution_id}/?part=detail-drawer` — institution detail drawer

---

## 2. Purpose

H-03 is the analytical perspective on institution health — **distinct from Division A's institution list (which is operational) and Division J's CSM view (which is relationship-focused)**. This page answers:

- Which institutions are showing early churn signals (declining engagement) before they lapse?
- Which states/regions have the highest platform concentration?
- What's the distribution of engagement scores across institution types and subscription tiers?
- Which Enterprise institutions are underusing their subscription?
- How does exam frequency correlate with subscription renewal likelihood?
- Are newly onboarded institutions activating successfully within 90 days?

**Who needs this page:**
- Analytics Manager (42) — monthly institution health reporting, churn analysis
- Data Analyst (44) — deep institution investigations, segmentation analysis

**Data source note:** All data reads from `analytics_institution_engagement` (pre-aggregated). Institution names and types displayed here are denormalized and re-synced weekly during the `compute_institution_engagement` Celery task (Sunday 03:00 IST). Subscription/billing data in the institution drawer is read-only from the platform billing module (`institution_subscription` table) — H-03 makes a direct DB read, no editing capability. Name changes made Monday–Saturday appear in H-03 the following Sunday.

---

## 3. Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  Page header: "Institution Analytics"   [Export Engagement Report]│
│  Filters: Period | Type | Tier | Region | Churn Risk | Onboarded  │
├──────┬──────┬──────┬──────┬──────┬──────┬────────────────────────┤
│Total │Active│Avg   │CRIT  │Avg   │Below │ New Institutions       │
│Inst. │(period)│Eng.│Churn │Exam  │Sub.  │ (period, activating %) │
│      │      │Score │Risk  │Freq  │Usage │                        │
├──────┴──────┴──────┴──────┴──────┴──────┴────────────────────────┤
│  India Choropleth Map (state-level)  │  Engagement Distribution  │
│  (institutions density + avg score) │  (score histogram by tier) │
├──────────────────────────────────────┴────────────────────────────┤
│  Institution Engagement Table (server-side paginated, 25 rows)   │
├───────────────────────────────────────────────────────────────────┤
│  Institution Detail Drawer (slides in on row click)              │
└───────────────────────────────────────────────────────────────────┘
```

---

## 4. Section-Wise Detailed Breakdown

---

### Section A — Filters

| Filter | Control | Notes |
|---|---|---|
| Period | Select: Last 30D / 90D / 6M / 1Y | Drives all metrics except engagement score (score is always latest week's snapshot) |
| Institution Type | Multiselect: School / College / Coaching / Group / All | — |
| Subscription Tier | Multiselect: Starter / Standard / Professional / Enterprise / All | — |
| Region / State | Select: All / State list (29 states + UTs) | — |
| Churn Risk | Multiselect: LOW / MEDIUM / HIGH / CRITICAL | From `analytics_institution_engagement.churn_risk` |
| Onboarded After | Date picker | Filter to recently onboarded institutions |

Active filter chips below filter bar. [Reset All].

**URL pre-filter support:** H-03 reads the following URL params on page load and pre-selects the corresponding filters: `?churn_risk=CRITICAL` (from H-01 KPI tile), `?institution_type=SCHOOL` (from institution type filters elsewhere), `?region=Telangana` (from choropleth map state click — state name URL-encoded). Choropleth state clicks append `?region={state_name}` to the URL and programmatically set the Region filter.

---

### Section B — Summary KPI Bar

| Tile | Description | Colour Rule |
|---|---|---|
| Total Institutions | Current count of all institutions on platform | Neutral |
| Active (period) | Institutions with ≥1 exam attempt in period | Green ≥90% of total; Amber 70–90%; Red <70% |
| Avg Engagement Score | Mean score across all `analytics_institution_engagement` latest records | Green ≥70; Amber 50–70; Red <50 |
| CRITICAL Churn Risk | Count where `churn_risk = CRITICAL` | Green = 0; Amber 1–5; Red > 5 |
| Avg Exam Frequency | Average `exam_frequency_per_month` across all active institutions | Green ≥4/month |
| Below Subscription Usage | Institutions using <50% of question bank available to their tier | Red count if > 10% of total |
| New Institutions (period) | Onboarded in period · `(activated ÷ new)%` activation rate | Green if activation ≥70% |

**Activation rate definition:** Institution is "activated" if they conducted ≥1 exam within 90 days of onboarding.

---

### Section C — India Choropleth Map

**Purpose:** Geographic distribution of platform institutions and their engagement health. Identifies regional concentration and regional engagement disparities.

**Implementation:** Leaflet.js with India state GeoJSON boundaries. Rendered server-side as an HTMX partial on page load.

**Map behaviour:**
- Each state coloured by avg engagement score of institutions in that state
  - Dark green: avg ≥ 70
  - Yellow-green: 50–70
  - Amber: 30–50
  - Red: < 30
  - Grey: 0 institutions in this state
- State boundary hover tooltip: `{State Name} — {N} institutions · Avg score: {X} · {M} CRITICAL risk`
- State click → applies "Region" filter to table below (shows only institutions from that state)

**Legend:** Colour scale with 5 bands. Toggleable overlay:
- [By Institution Count] — colour by number of institutions (dark = more)
- [By Engagement Score] — default
- [By Churn Risk] — colour by % institutions with CRITICAL/HIGH risk

**Responsive:** On tablet/mobile: map hidden, replaced with "Top 10 States by Institution Count" table.

---

### Section D — Engagement Score Distribution

Histogram showing distribution of engagement scores (0–100) across institutions. Side by side with the map.

**X-axis:** Score bands: 0–9, 10–19, ..., 90–100 (11 bands).
**Y-axis:** Institution count.
**Colour fill:** Matches churn risk thresholds (red for 0–29 = CRITICAL, amber 30–49 = HIGH, yellow 50–69 = MEDIUM, green 70–100 = LOW).
**Breakdown toggle:** [By Institution Type] — stacked bars per type. [By Subscription Tier] — stacked bars per tier.

Tooltip: "{N} institutions in {band}. {churn_risk_label} zone."

---

### Section E — Institution Engagement Table

Main table. Server-side paginated, 25 rows per page. Source: `analytics_institution_engagement` latest weekly snapshot.

| Column | Sortable | Notes |
|---|---|---|
| Institution Name | Yes | Truncated at 35 chars, full name in tooltip |
| Type | Yes | School / College / Coaching / Group badge |
| Subscription Tier | Yes | Starter / Standard / Professional / Enterprise |
| Region | Yes | State name |
| Engagement Score | Yes (default: ASC — worst first) | Progress bar (0–100) with score value. Red <30, Amber 30–49, Yellow 50–69, Green ≥70 |
| Churn Risk | Yes | CRITICAL (red) · HIGH (amber) · MEDIUM (yellow) · LOW (green) |
| Exam Freq/Month | Yes | Last 90 days avg. Red if < 1/month for paid tier |
| Active Students % | Yes | `student_active_rate` — active ÷ enrolled |
| Last Exam | Yes | Date of most recent exam. Red if > 60 days ago for paid tier |
| Actions | — | [View →] opens detail drawer; [Share to CSM] (Analytics Manager only) |

**Default sort:** Engagement Score ASC (worst institutions first — actionable view).

**Bulk actions** (rows selected):
- [Export Selected CSV] — downloads engagement data for selected institutions
- [Share to CSM Team] — sends in-app notification to all Customer Success Managers (53, Division J) with a list of selected institutions and their churn risk levels. Confirmation required: "Send {N} institution alerts to Customer Success team?" **30-day deduplication:** institutions already notified within the last 30 days are excluded. Pre-confirmation message shows: "{M} of {N} selected institutions will be notified ({K} already notified within 30 days — skipped)."

**Row click** → opens detail drawer.

---

### Section F — Institution Detail Drawer

450px right-side drawer. Tabs: **Overview | Trend | Exam History | Comparison**

#### Overview Tab

**Engagement scorecard:**
| Metric | Value | Weight in Score |
|---|---|---|
| Exam frequency/month | — | 30% |
| Student active rate | — | 30% |
| Question bank usage % | — | 20% |
| Admin login days/30 | — | 20% |
| **Composite Score** | **{N}/100** | — |

Each metric shown as a mini progress bar with its contribution to the overall score. Helps the analyst understand which specific metric is dragging the score down.

**Churn risk factor breakdown:**
The primary driver of churn risk is shown: "Primary risk signal: Exam frequency dropped from 6.2/month to 1.1/month (last 30 days vs prior 60 days)."

**BGV compliance link:** "BGV Coverage: {N}% — {status}" — read-only, links to G-04 for context. Shown because poor BGV compliance is correlated with institution non-renewal.

**Subscription info:** Plan tier, renewal date (days remaining), MRR. Read-only. Sourced from billing module.

**CSM assignment:** Shows the assigned Customer Success Manager (Division J, role 53) for this institution. [Notify CSM] button — sends in-app message to assigned CSM with engagement data.

#### Trend Tab

**Engagement score over time:** Line chart showing `engagement_score` for this institution over the last 12 weekly snapshots. Shows if the institution is declining, stable, or improving.

**Metric breakdown trends:** Four mini-charts (one per engagement score component):
- Exam frequency/month (last 12 weeks)
- Student active rate (last 12 weeks)
- Question bank usage % (last 12 weeks)
- Admin login days (last 4 weeks as bar chart)

Data from: `analytics_institution_engagement` historical records (one row per week per institution, retained up to 2 years per data retention policy). Chart defaults to showing the last 12 weekly snapshots (~3 months) for readability; a [Show 24 weeks] toggle extends the chart to ~6 months. Full 2-year data is available via H-09 Institution Engagement Export.

#### Exam History Tab

Table of all exams conducted by this institution (read from `analytics_daily_snapshot` filtered to institution_id).

| Column | Notes |
|---|---|
| Exam Name | — |
| Domain | — |
| Date | — |
| Students | Enrolled count |
| Attempts | Attempt count |
| Avg Score % | — |
| Completion Rate | — |

Pagination: 10 rows. Filter: Date Range, Domain. [View in H-05 →] link to open H-05 filtered to this institution (if H-05 supports institution filter).

#### Comparison Tab

**Benchmarking against peer institutions.** "This institution vs. similar institutions (same type + tier + region)."

| Metric | This Institution | Peer Avg | Percentile |
|---|---|---|---|
| Engagement Score | 42 | 68 | 18th percentile |
| Exam Frequency/month | 1.1 | 4.8 | 9th percentile |
| Student Active Rate | 34% | 61% | 12th percentile |
| Question Bank Usage | 28% | 52% | 15th percentile |

Peer group: Institutions with same type, tier, and region. Min peer group size: 5 institutions. If fewer than 5 peers: "Peer comparison not available — fewer than 5 similar institutions in your region/tier."

---

## 5. Access Control

| Gate | Rule |
|---|---|
| Page access | Analytics Manager (42), Data Analyst (44), Platform Admin (10) |
| [Export Engagement Report] | Analytics Manager (42), Platform Admin (10) |
| [Share to CSM Team] bulk action | Analytics Manager (42) only — Data Analyst cannot send CSM notifications |
| CSM notification deduplication | System-enforced: 30-day cooldown per institution. Tracked via `analytics_audit_log` (action=`CSM_NOTIFIED`, object_type=`institution`). |
| [Notify CSM] in drawer | Analytics Manager (42) only |
| Engagement score data | Read-only for all roles on this page |
| Subscription / billing details in drawer | Read — visible; no edit capability on this page |
| Division J CSM contact info in drawer | Visible to all permitted roles |

---

## 6. Edge Cases & Error States

| Scenario | Behaviour |
|---|---|
| Institution engagement score not yet computed (new institution onboarded this week) | Row shows "Score: Pending — first weekly computation on Sunday" with info tooltip |
| Institution has 0 exams ever (onboarded but not activated) | Engagement score = 0. `churn_risk = CRITICAL` (zero activation). Last Exam: "Never". Special badge: "NOT ACTIVATED". |
| Institution Group (type=GROUP) | Shows aggregate stats (weighted average of child engagement scores). Clicking row: drawer tabs change to **Group Overview \| Child Institutions \| Exam History \| Comparison**. "Group Overview" shows aggregate engagement scorecard + weighted composite score. "Child Institutions" shows a sub-table of all child institutions with their individual engagement scores, churn risk, and [View →] link to that child's full drawer. "Exam History" and "Comparison" are disabled for GROUP type (benchmarking groups against individual institutions is not meaningful). |
| Peer comparison group has < 5 members | "Peer comparison unavailable — fewer than 5 similar institutions" message in Comparison tab. Shows platform average as fallback comparison. |
| CSM not assigned to institution | [Notify CSM] button disabled: "No CSM assigned. Assign in Division J." |
| State has 0 institutions | State shows grey on map. Hover: "{State} — No institutions." Not shown in table. |
| Export > 2,000 rows | "Export is large ({N} rows). Processing in background — you'll be notified when ready (est. 2–3 min)." |
| Weekly engagement not recomputed (Sunday pipeline missed) | Table shows "⚠ Scores from {date} — weekly refresh pending" banner. Old scores shown with staleness indicator. |

---

## 7. UI Patterns

### Loading States
- Summary bar: 7-tile shimmer
- Choropleth map: grey India-shaped placeholder with "Loading map..." text
- Engagement distribution: bar chart skeleton
- Table: 10-row shimmer
- Drawer: header shimmer + 4 tab labels + content skeleton

### Toasts
| Action | Toast |
|---|---|
| Export queued | ✅ "Engagement report queued — notified when ready" (4s) |
| CSM notification sent | ✅ "{N} institutions shared with CSM team. {K} skipped (notified recently). [View Skipped →]" (persistent until dismissed — shows a modal with skipped institution names + their last notification date) |
| CSM notify (drawer) | ✅ "CSM {name} notified for {institution}" (3s) |

### Responsive
| Breakpoint | Behaviour |
|---|---|
| Desktop (≥1280px) | Full layout with side-by-side map + histogram |
| Tablet | Map + histogram stacked. Table: 5 visible columns (Name, Type, Score, Churn Risk, Actions). |
| Mobile | Map replaced with top-10 state list. Table card view. Drawer full-screen. |

---

*Page spec complete.*
*H-03 covers: institution KPI bar → India choropleth engagement map → engagement score histogram → 8-column engagement table (worst-first default) → institution detail drawer (scorecard / 12-week trend / exam history / peer benchmarking) → CSM notification workflow → bulk export.*
