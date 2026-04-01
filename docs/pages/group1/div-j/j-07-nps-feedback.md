# J-07 — NPS & Voice of Customer

**Route:** `GET /csm/feedback/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** CSM (#53), CS Analyst (#93)
**Also sees:** Account Manager (#54) — own accounts + send for own; ISM (#94) — own accounts + send for own; Escalation Manager (#55) — read-only; Renewal Executive (#56) — read-only

---

## Purpose

Systematic voice-of-customer programme for 2,050 institutions. At scale, individual relationship memory fails — this page turns feedback into structured data. The CSM uses it to run quarterly NPS campaigns, triage detractors before they churn, identify promoters for case studies, and track CSAT trends over time. The CS Analyst uses it to model correlation between NPS and churn probability.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| NPS KPI strip | `csm_nps_survey` aggregated (promoters/passives/detractors) for last complete quarter | 60 min |
| NPS trend chart | `csm_nps_survey` grouped by month for last 12 months | 60 min |
| CSAT trend chart | `csm_nps_survey` WHERE survey_type='RENEWAL_CSAT' grouped by month | 60 min |
| Score distribution chart | `csm_nps_survey.nps_score` histogram for current period | 60 min |
| NPS by segment chart | `csm_nps_survey` grouped by institution type for current period | 60 min |
| Survey table | `csm_nps_survey` JOIN `institution` JOIN `user` (sent_by) | 5 min |
| Verbatim panel | `csm_nps_survey.verbatim_feedback` WHERE verbatim_feedback IS NOT NULL | 5 min |
| Pending surveys | `csm_nps_survey` WHERE responded_at IS NULL AND link_expires_at > now() | 5 min |
| Follow-up required | `csm_nps_survey` WHERE follow_up_required=true | 5 min |

Cache key includes all filter params. `?nocache=true` for CSM (#53) and CS Analyst (#93).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `this_quarter`, `last_quarter`, `last_6m`, `last_12m`, `custom` | `last_quarter` | Reporting window |
| `?from` | `YYYY-MM-DD` | — | Custom period start |
| `?to` | `YYYY-MM-DD` | — | Custom period end |
| `?survey_type` | `QUARTERLY_NPS`, `POST_ONBOARDING_NPS`, `RENEWAL_CSAT`, `EBR_FEEDBACK`, `AD_HOC` (comma-sep; case-insensitive — view normalises to uppercase before querying) | `all` | Filter survey type |
| `?category` | `promoter`, `passive`, `detractor` | `all` | Filter by promoter category |
| `?type` | `school`, `college`, `coaching`, `group` | `all` | Filter by institution type |
| `?follow_up` | `1` | — | Show only follow_up_required=true |
| `?pending` | `1` | — | Show only unanswered surveys |
| `?sent_by` | user_id | `all` | Filter by who sent the survey |
| `?sort` | `sent_at_desc`, `score_asc`, `score_desc`, `institution_name` | `sent_at_desc` | Survey table sort |
| `?page` | integer | `1` | Survey table page |
| `?export` | `csv` | — | Export filtered survey data (CSM + Analyst) |
| `?nocache` | `true` | — | Bypass Memcached (CSM + CS Analyst only) |

---

## HTMX Part-Load Routes

| Part | Route | Trigger |
|---|---|---|
| NPS KPI strip | `?part=nps_kpi` | Page load + period change |
| NPS trend chart | `?part=nps_trend` | Page load + period change |
| CSAT trend chart | `?part=csat_trend` | Page load + period change |
| Score distribution | `?part=score_dist` | Page load + filter change |
| NPS by segment | `?part=nps_by_segment` | Page load + period change |
| Survey table | `?part=survey_table` | Page load + filter change + sort + page |
| Verbatim panel | `?part=verbatim` | Page load + filter change + text search (300ms debounce, min 3 chars) |
| Pending surveys | `?part=pending` | Page load + auto-refresh every 10 min |
| Follow-up panel | `?part=followups` | Page load |

---

## Page Layout

```
┌────────────────────────────────────────────────────────────────────┐
│  NPS & Voice of Customer   Period: [Last Quarter ▼]  [Send Survey] │
├────────────────────────────────────────────────────────────────────┤
│  NPS KPI STRIP (5 tiles)                                           │
├─────────────────────────┬──────────────────────────────────────────┤
│  NPS TREND CHART        │  CSAT TREND CHART                       │
│  (12 months, line)      │  (12 months, line)                      │
├─────────────────────────┴──────────────────────────────────────────┤
│  SCORE DISTRIBUTION     │  NPS BY INSTITUTION TYPE (grouped bar)   │
├─────────────────────────┴──────────────────────────────────────────┤
│  FILTER ROW                                                        │
│  SURVEY TABLE + PAGINATION                                         │
├────────────────────────────────────────────────────────────────────┤
│  VERBATIM FEEDBACK PANEL   │   PENDING & FOLLOW-UP PANEL           │
└────────────────────────────┴───────────────────────────────────────┘
```

---

## NPS KPI Strip (5 tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ +38          │ │ 54           │ │ 18%          │ │ 62%          │ │ 43%          │
│ NPS Score    │ │ Responses    │ │ Detractor %  │ │ Promoter %   │ │ Response     │
│ (last qtr)   │ │              │ │              │ │              │ │ Rate         │
│ ↑+8 vs Q3   │ │ of 127 sent  │ │ (10 insts)   │ │ (35 insts)   │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- **NPS Score:** `(Promoters/respondents × 100) - (Detractors/respondents × 100)`. "Respondents" = count of surveys where `responded_at IS NOT NULL` (unresponded surveys are excluded from NPS score calculation). Scale: -100 to +100. Delta vs previous period. Green if ≥ 40, amber if 20–39, red if < 20.
- **Responses:** Count where `responded_at IS NOT NULL` in period. Sub-label: "of N sent".
- **Detractor %:** Count(DETRACTOR) / Count(responded) × 100. Red if > 20%.
- **Promoter %:** Count(PROMOTER) / Count(responded) × 100. Green if > 50%.
- **Response Rate:** Count(responded) / Count(sent) × 100. "Sent" includes ALL surveys dispatched in the period — including pending and expired surveys (expired surveys are still counted as "sent" since the recipient received the link; they chose not to respond). Target ≥ 30%.

Tiles shown in selected period. "last_quarter" = Q4 2025 (Oct–Dec 2025) if today is Q1 2026.

Note: NPS formula counts only `QUARTERLY_NPS` surveys by default; includes all NPS-type surveys if `?survey_type=all`. The NPS Score tile shows "— (no data)" if fewer than `csm_config['nps_min_kpi_responses']` (default: 10) responses exist for the period — this threshold is intentionally higher than the per-month trend chart threshold (5) because portfolio-wide KPIs require statistical credibility.

---

## NPS Trend Chart

Line chart (Chart.js) — 12 months of monthly NPS scores.

- X-axis: month labels (MMM YY)
- Y-axis: -100 to +100
- Dotted reference line at 0 (neutral)
- Solid reference line at +40 (good) and +70 (excellent)
- Data points: NPS score per month. Null (shown as gap with tooltip "Not enough responses — need ≥5 for trend") if < 5 responses for that month — per-month samples are naturally smaller; the ≥5 threshold is intentionally lower than the ≥10 threshold used for KPI tiles (which represent portfolio-wide quarterly aggregates requiring higher statistical confidence). A "low sample" indicator icon (⚠) shown on data points with 5–9 responses.
- Secondary bars (right Y-axis, 0–100): response count per month as grey bars

Hover tooltip: NPS score · Promoters% · Detractors% · Response count.

---

## CSAT Trend Chart

Line chart — 12 months of average `csat_score` (1–5 scale) from RENEWAL_CSAT and EBR_FEEDBACK surveys.

- X-axis: month labels
- Y-axis: 1.0 to 5.0
- Reference line at 4.0 (target)
- Data points: monthly avg CSAT. Null if 0 responses.

Hover tooltip: avg CSAT · response count · date range.

---

## Score Distribution Chart

Bar chart — distribution of NPS scores 0–10 for selected period.

```
Count
 12 │  ┌───┐       ┌───┐ ┌───┐
 10 │  │   │       │   │ │   │
  8 │  │   │   ┌───┤   │ │   │ ┌───┐
  6 │  │   │   │   │   │ │   │ │   │
  4 │  │   │   │   │   │ │   │ │   │ ┌───┐ ┌───┐
  2 │  │   │ ┌─┤   │   │ │   │ │   │ │   │ │   │
  0 └──┴───┴─┴─┴───┴───┴─┴───┴─┴───┴─┴───┴─┴───┴
       0   1  2   3   4   5   6   7   8   9  10
   [■ Detractor (0–6)]  [■ Passive (7–8)]  [■ Promoter (9–10)]
```

Bars coloured by range: red=0–6, amber=7–8, green=9–10.

---

## NPS by Institution Type

Grouped bar chart showing NPS score per institution type for selected period.

```
Coaching  [███████████████░░░░░]  +52
Colleges  [████████████░░░░░░░░]  +38
Schools   [█████████░░░░░░░░░░░]  +28
Groups    [██████░░░░░░░░░░░░░░]  +14
```

Horizontal bars sorted by NPS score descending. Shows N responses below each bar label on hover.

---

## Survey Table Filter Row

```
Type: [All ▼]  Category: [All ▼]  Institution type: [All ▼]  Sent by: [All ▼]
[Follow-up required □]  [Pending response □]
Period: [Last Quarter ▼]   [Apply]   [Clear]
Sort: [Sent date ▼]   Showing 127 surveys
```

---

## Survey Table

| Column | Description |
|---|---|
| Institution | Name (link → J-03 Feedback tab) + type badge |
| Survey Type | Badge: QUARTERLY_NPS / POST_ONBOARDING_NPS / RENEWAL_CSAT / EBR_FEEDBACK / AD_HOC |
| Sent To | Name + email (truncated) |
| Sent Date | Date (relative if < 7 days) |
| Score | NPS 0–10 or CSAT 1–5 with star icons. "Pending" if no response |
| Category | PROMOTER (green) / PASSIVE (amber) / DETRACTOR (red) / — if CSAT |
| Responded | Relative time or "Pending" |
| Follow-up | Yellow flag icon if `follow_up_required=true`; tick if resolved |
| Verbatim | First 80 chars of `verbatim_feedback` + [↓ expand] link. "—" if no text |
| Sent By | Sender avatar + name |
| Actions | [Mark Follow-up] [Resend] [View] |

**Pending survey row:** Score + Category columns show "—" in grey italic. Responded column shows "Pending (N days)" — red if > 7 days since sent.

**Expired survey row:** Shows "Expired" badge in Score column. [Resend] action available.

**[Mark Follow-up]:** Toggle `follow_up_required`. Inline PATCH. Changes icon from outline to solid yellow flag. Second click opens follow-up notes input: "Add a note about the required follow-up action:" → saves to `csm_nps_survey.follow_up_notes`.

**[Resend]:** Available for expired or pending surveys. Opens resend modal (same as Send Survey modal, pre-filled). Creates a new `csm_nps_survey` row with a fresh `survey_link_token` (`secrets.token_urlsafe(48)`). Old row updated: `superseded_by_id = new_row.id` (column defined in data model). Old token immediately invalidated — public survey endpoint rejects submissions to superseded tokens.

**[View]:** Opens Survey Detail Drawer.

---

## Survey Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  QUARTERLY_NPS  ·  Delhi Public School               [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Sent to: Dr. Ramesh Kumar (principal@dps.edu)                   │
│  Sent by: Ananya K. (CSM)   ·   Sent: 2 Jan 2026                 │
│  Responded: 5 Jan 2026 (3 days later)                            │
│  Expires: 16 Jan 2026                                            │
├──────────────────────────────────────────────────────────────────┤
│  NPS Score: 9 / 10  ·  PROMOTER  ●●●●●●●●●○  (9/10)            │
├──────────────────────────────────────────────────────────────────┤
│  Verbatim feedback:                                              │
│  "EduForge has transformed how we run exams. The real-time       │
│   reports after each test help teachers adjust their teaching.   │
│   We'd love to see more question variety in the regional         │
│   language section."                                             │
├──────────────────────────────────────────────────────────────────┤
│  Follow-up required: No                                          │
│  [Mark follow-up required]                                       │
│                                                                  │
│  Follow-up notes: —                                              │
└──────────────────────────────────────────────────────────────────┘
```

---

## Send Survey Modal

```
┌──────────────────────────────────────────────────────────────────┐
│  Send Survey                                                     │
├──────────────────────────────────────────────────────────────────┤
│  Institution*   [Search institution...                    ]      │
│  Survey type*   [QUARTERLY_NPS                          ▼]       │
│  Send to (email)* [principal@dps.edu                    ]        │
│  Recipient name* [Dr. Ramesh Kumar                       ]       │
│  Custom message  [Optional personalised intro text       ]       │
│                                                                  │
│  Survey link expires 14 days after sending.                      │
│                                                                  │
│  ⚠  This institution has an active pending survey of the same    │
│     type (sent 2 Jan, not yet responded). Sending a new one will │
│     supersede the old link.  [Proceed ▼]                         │
│                                                                  │
│  [Cancel]                          [Send Survey]                 │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Institution: required
- Survey type: required
- Email: required; valid format
- Recipient name: required; min 2 chars
- Guard: warns but does not block if existing pending survey for same institution + type

POST to `/csm/feedback/surveys/send/`. Triggers dispatch via **F-06 Notification Manager** — email for all institution types; additionally sends WhatsApp via F-06 if `survey_type = QUARTERLY_NPS` and institution_type = `COACHING` (coaching centres have significantly higher WhatsApp open rates than email).

---

## Verbatim Feedback Panel

Below the survey table. Shows all verbatim responses for the selected period with filter controls.

```
┌──────────────────────────────────────────────────────────────────┐
│  Verbatim Feedback (38 responses)                                │
│  Category: [All ▼]  Type: [All ▼]  Sort: [Newest ▼]             │
│                                                                  │
│  PROMOTER · Delhi Public School · 9/10 · 5 Jan 2026             │
│  "EduForge has transformed how we run exams. The real-time..."   │
│  [Read more ↓]   [Flag follow-up]                               │
│  ─────────────────────────────────────────────────────           │
│  DETRACTOR · Excel Coaching Hub · 3/10 · 12 Jan 2026            │
│  "The platform lags during peak exam hours. We lost 15           │
│   minutes in our last mock test. Students were upset."           │
│  [Read more ↓]   [Flag follow-up]   [Create Escalation ↗]       │
│  ─────────────────────────────────────────────────────           │
│  ...                                                             │
└──────────────────────────────────────────────────────────────────┘
```

DETRACTOR verbatim: highlighted with red-50 background. [Create Escalation ↗] button visible to CSM and Escalation Manager — pre-fills escalation drawer with institution and summary from verbatim.

[Read more ↓]: expands full verbatim text inline.

Sorted newest first by default. Filter by category (PROMOTER/PASSIVE/DETRACTOR), survey type, institution type.

**Text search:** `[🔍 Search verbatim feedback...]` — searches `verbatim_feedback` using PostgreSQL full-text search (`to_tsvector('english', verbatim_feedback) @@ plainto_tsquery('english', ?)`) with 300ms debounce. Min 3 chars. Highlights matching terms in results using `<mark>` tags. Useful for surfacing themes (e.g., searching "pricing" to find all price-related detractor feedback before a renewal negotiation).

**Empty state:** "No verbatim feedback received for the selected period."

---

## Pending & Follow-up Panel

Two-column panel at bottom right.

**Left: Pending Surveys**

```
  Pending (no response):    42 of 127 sent
  ─────────────────────────────────────
  Delhi Coaching Hub   Sent 10 Jan (11d ago)  [Resend]
  Victory College      Sent 12 Jan (9d ago)   [Resend]
  Excel Institute      Sent 15 Jan (6d ago)   —
  [View all pending →]
```

[Resend] available after 7 days of no response.

**Right: Follow-up Required**

```
  Follow-ups pending:   5
  ─────────────────────────────────────
  Sunrise Academy    DETRACTOR 2/10  "Platform unstable"  [View]
  Hyderabad Hub      DETRACTOR 4/10  "Missing features"   [View]
  [View all follow-ups →]
```

[View] opens the Survey Detail Drawer.

---

## Bulk NPS Dispatch (Celery Task J-3 control)

Available to CSM (#53) only. Shows current quarter's dispatch schedule:

```
┌──────────────────────────────────────────────────────────────────┐
│  Quarterly NPS Dispatch — Q1 2026 (Jan–Mar)                      │
│                                                                  │
│  Status: Completed on 1 Jan 2026, 10:00 IST                      │
│  Sent: 127 surveys · Skipped: 18 (surveyed < 60 days ago)        │
│  Next dispatch: 1 Apr 2026, 10:00 IST (in 11 days)               │
│                                                                  │
│  [Preview Next Batch]  (shows which institutions will be included)│
│  [Skip Next Dispatch]  (requires confirmation + reason note)     │
└──────────────────────────────────────────────────────────────────┘
```

[Preview Next Batch] → modal listing institutions that Task J-3 will survey on next run: HEALTHY + ENGAGED institutions not surveyed in last 60 days.

[Skip Next Dispatch] → confirmation dialog: "Skip the Q2 2026 NPS dispatch? This cannot be undone." POST to `/csm/feedback/dispatch/skip/`.

---

## Export CSV

Filename: `eduforge_nps_feedback_YYYY-MM-DD.csv`

Columns: survey_id, institution_id, institution_name, institution_type, survey_type, sent_to_email, sent_to_name, sent_by, sent_at, responded_at, nps_score, csat_score, promoter_category, verbatim_feedback, follow_up_required, follow_up_notes

Available to CSM (#53) and CS Analyst (#93).

---

## Empty States

| Condition | Message |
|---|---|
| No surveys in period | "No surveys sent in this period." with [Send Survey] button |
| No verbatim responses | "No verbatim feedback received for the selected period." |
| No follow-ups pending | "No follow-ups required." with green checkmark |
| No pending surveys | "All surveys have been responded to." |

---

## Role-Based UI Visibility Summary

| Element | 53 CSM | 54 AM | 55 Escalation | 56 Renewal | 93 Analyst | 94 ISM |
|---|---|---|---|---|---|---|
| Full NPS charts + KPIs | Yes | Yes | Read | Read | Full + export | Read |
| Survey table | All surveys | Own sent | All (read) | All (read) | All | Own sent |
| Send survey | All institutions | Own accounts | No | No | No | Own accounts |
| Resend survey | Yes | Own | No | No | No | Own |
| Mark follow-up | Yes | Own | No | No | No | Own |
| Create escalation from verbatim | Yes | No | Yes | No | No | No |
| Bulk dispatch control (Task J-3) | Yes | No | No | No | No | No |
| Export CSV | Yes | No | No | No | Yes | No |
| [?nocache=true] | Yes | No | No | No | Yes | No |

---

## Toasts, Loaders & Error States

**Toasts:**

| Action | Type | Message |
|---|---|---|
| Survey sent (single) | SUCCESS | "Survey sent to {recipient_name} at {institution_name}." |
| Survey sent (bulk dispatch) | SUCCESS | "{N} NPS surveys dispatched for Q{Q} {YYYY}." |
| Survey resent | SUCCESS | "Survey resent to {recipient_name}. Previous link has been invalidated." |
| Follow-up flagged | SUCCESS | "Follow-up flagged for {institution_name}." |
| Follow-up unflagged | INFO | "Follow-up flag removed." |
| Follow-up notes saved | SUCCESS | "Follow-up notes saved." |
| Follow-up resolved | SUCCESS | "Follow-up marked as resolved." |
| Next dispatch skipped | WARNING | "Q{Q} {YYYY} NPS dispatch skipped. Recorded reason: {reason}." |
| Export started | INFO | "Preparing export…" |
| Export ready | SUCCESS | "Export ready. [Download]" |
| Export failed | ERROR | "Export failed. Try again or reduce the date range." |
| Escalation created from verbatim | SUCCESS | "Escalation created. [View in J-05]" |

**Skeleton / loading states:**

- **NPS KPI strip:** 5 tile-sized shimmer rectangles on page load and period change.
- **NPS trend chart:** Full chart-area shimmer (same height as rendered chart) while HTMX loads.
- **CSAT trend chart:** Same as NPS trend chart shimmer.
- **Score distribution + NPS by segment:** Side-by-side shimmer blocks.
- **Survey table:** 10 skeleton rows (grey placeholder lines per column) on initial load and filter change. Pagination shows "Loading…" until resolved.
- **Verbatim panel:** 3 skeleton feedback cards (avatar + 2 lines of text placeholder).
- **Pending & follow-up panel:** 3 skeleton rows each side.

All HTMX part-loads use `hx-indicator` pointing to a per-section spinner (`<span class="htmx-indicator">`) inside the target div. Global page spinner is NOT used — each section loads independently.

**Error states:**

- **Survey table load failure:** Inline error card within `#j-survey-table`: "Failed to load surveys. [Retry]". [Retry] re-triggers the HTMX GET.
- **Chart load failure:** Within each chart container: "Chart data unavailable. [Retry]"
- **Send Survey failure (network/5xx):** ERROR toast "Failed to send survey — please try again."
- **Resend to expired survey (race condition):** If survey has already been superseded when [Resend] is clicked, ERROR toast: "This survey has already been superseded. Refresh the page to see the latest state."
- **Export timeout:** ERROR toast after 30 seconds: "Export is taking longer than expected. Try filtering to a shorter period."
- **Public survey endpoint rate limit:** If the institution submits the form multiple times in quick succession, the server returns 429 with message "Too many attempts — please wait a moment."

---

## Missing Spec Closes (Audit)

### HTMX Part-Load Target IDs

| Part | Route | Target ID |
|---|---|---|
| NPS KPI strip | `?part=nps_kpi` | `#j-nps-kpi` |
| NPS trend chart | `?part=nps_trend` | `#j-nps-trend` |
| CSAT trend chart | `?part=csat_trend` | `#j-csat-trend` |
| Score distribution | `?part=score_dist` | `#j-score-dist` |
| NPS by segment | `?part=nps_by_segment` | `#j-nps-segment` |
| Survey table | `?part=survey_table` | `#j-survey-table` |
| Verbatim panel | `?part=verbatim` | `#j-verbatim` |
| Pending surveys | `?part=pending` | `#j-pending` |
| Follow-up panel | `?part=followups` | `#j-followups` |

All part-loads use `hx-push-url="true"` so filter/sort state persists in the URL. Pagination uses `hx-boost` on page links within `#j-survey-table` only.

### Public Survey Endpoint (Institution-Facing Form)

Route: `GET /survey/{token}/` — public, no authentication required. Served by a separate Django view outside the `/csm/` prefix.

**Token validation (server-side, before rendering form):**

| Condition | HTTP Status | Response |
|---|---|---|
| Token not found | 404 | "This survey link is not valid." |
| `superseded_by_id IS NOT NULL` | 410 | "This survey link has been superseded. Please check your email for a newer survey link." |
| `link_expires_at < now()` | 410 | "This survey link has expired. Please contact your Customer Success Manager to receive a new link." |
| `responded_at IS NOT NULL` | 200 | Already-responded page (see below) |
| Valid, not yet responded | 200 | Renders survey form |

**NPS survey form (survey_type IN QUARTERLY_NPS, POST_ONBOARDING_NPS):**

```
┌──────────────────────────────────────────────────────────────┐
│  EduForge                                                    │
│  ─────────────────────────────────────────────────────────  │
│  Hello Dr. Ramesh Kumar,                                     │
│  {custom_message if set, else default intro}                 │
│                                                              │
│  How likely are you to recommend EduForge to a colleague     │
│  or partner institution?                                     │
│                                                              │
│  0    1    2    3    4    5    6    7    8    9    10         │
│  ○    ○    ○    ○    ○    ○    ○    ○    ○    ○    ○          │
│  Not at all likely              Extremely likely             │
│                                                              │
│  What's the main reason for your score? (optional)           │
│  [                                                    ]      │
│  (max 2,000 characters)                                      │
│                                                              │
│                              [Submit Feedback →]             │
└──────────────────────────────────────────────────────────────┘
```

**CSAT survey form (survey_type IN RENEWAL_CSAT, EBR_FEEDBACK, AD_HOC when csat):**

```
┌──────────────────────────────────────────────────────────────┐
│  EduForge                                                    │
│  How would you rate your overall experience with EduForge?   │
│                                                              │
│  ★☆☆☆☆  1 — Very Poor                                        │
│  ★★☆☆☆  2 — Poor                                            │
│  ★★★☆☆  3 — Neutral                                          │
│  ★★★★☆  4 — Good                                            │
│  ★★★★★  5 — Excellent                                        │
│                                                              │
│  What could we improve? (optional)                           │
│  [                                                    ]      │
│                                                              │
│                              [Submit Feedback →]             │
└──────────────────────────────────────────────────────────────┘
```

**AD_HOC survey type:** Can be either NPS (0–10 scale) or CSAT (1–5 scale). Determined by `csm_nps_survey.csat_score IS NULL` (NPS form shown) vs. `csm_nps_survey.nps_score IS NULL` (CSAT form shown). The sender selects "Score type" in the Send Survey modal when `AD_HOC` is chosen.

**Form submission:** POST to `/survey/{token}/submit/`. On success:
- Sets `responded_at = now()`, `nps_score` or `csat_score`, `verbatim_feedback`, `promoter_category` (computed server-side from nps_score)
- Returns 200 with thank-you page:
  > "Thank you, Dr. Ramesh Kumar! Your feedback helps us improve EduForge for institutions across India. You may close this page."
- No redirect, no follow-up actions visible to respondent

**Already-responded page:**
> "You have already submitted this survey on {responded_at date}. Thank you for your feedback!"

**Security:** Token is 48-byte URL-safe random string (`secrets.token_urlsafe(48)`) — brute-force infeasible. No internal IDs exposed. Rate limited to 10 submissions per IP per hour (Django middleware).

### Survey Table — Pagination Spec

- Page size: 25 rows per page
- Pagination controls: `← Previous [1] [2] [3] ... [12] Next →` within `#j-survey-table`
- "Showing {start}–{end} of {total} surveys" above pagination
- Clicking a page number triggers HTMX GET `?part=survey_table&page={n}` — no full page reload
- Filter application resets to `?page=1` silently

### Survey Table — Institution Name Search

Search input above filter row (separate from verbatim search):

```
[🔍 Search institution name...   ] (debounce 300ms, min 2 chars)
```

Appends `?q={term}` to all HTMX part-load requests for `#j-survey-table`. ILIKE on `institution.name`. Search state persists in URL via `hx-push-url`.

### Follow-up Resolution

**[Mark Resolved]** button available when `follow_up_required=true` in Survey Detail Drawer and Follow-up panel.

PATCH to `/csm/feedback/surveys/{id}/follow-up/` with body `{"resolved": true}`.

Adds `follow_up_resolved_at` timestamptz and `follow_up_resolved_by_id FK auth_user` to the survey row. (These two columns are missing from the `csm_nps_survey` data model in div-j-pages-list.md — see addendum below.)

In Follow-up Required panel: resolved items move to a collapsed "Resolved (N)" section below the active list. In survey table: flag icon changes from solid yellow to grey tick.

**Who can resolve:** CSM (#53) can resolve any follow-up. AM (#54) and ISM (#94) can resolve follow-ups on their own accounts only.

### Send Survey Modal — Full Spec

**Institution search:** Typeahead on `institution.name`. Min 2 chars, debounce 200ms, shows top 10 matches. Results include institution type badge. Selecting an institution auto-populates `institution_type` (used internally to determine dispatch channel).

**Score type field (AD_HOC only):**
When `survey_type = AD_HOC` is selected, an additional field appears:
```
  Score type*  [● NPS (0–10)  ○ CSAT (1–5)]
```
Determines whether `nps_score` or `csat_score` column is populated on response.

**Custom message character limit:** 500 characters. Character counter shown below textarea. Stored in `csm_nps_survey.custom_message` (varchar 500). Default intro text used if left blank.

**WhatsApp dispatch indicator:** When `institution_type = COACHING` and `survey_type = QUARTERLY_NPS`, modal shows an additional info badge below the email field:
```
ℹ️ This survey will also be sent via WhatsApp to the institution's primary contact.
```
Both channels are triggered via F-06 Notification Manager. `dispatch_channel` stored as `BOTH` for this case.

**Server-side ownership enforcement (AM + ISM):**
For AM (#54): server validates `csm_account_assignment.account_manager_id = request.user.id` for the selected institution. Rejects with 403 if not assigned.
For ISM (#94): server validates `csm_account_assignment.ism_id = request.user.id` AND `ism_tenure_end_date >= today`. Rejects with 403 if not assigned or tenure ended.

### Survey Detail Drawer — Full Spec

**CSAT variant:**
```
RENEWAL_CSAT  ·  Excel Coaching Centre                [Close ×]
  Sent to: Priya Sharma (priya@excel.com)
  Sent by: Ananya K. (CSM)  ·  Sent: 15 Feb 2026
  Responded: 18 Feb 2026 (3 days later)
  Expires: 1 Mar 2026

  CSAT Score: 4 / 5  ·  ★★★★☆

  Verbatim: "Support team responds fast but the app crashes sometimes."

  Follow-up required: No    [Mark follow-up required]
  Follow-up notes: —

  Dispatch channel: Email
  [View Account Profile ↗]    [Resend]
```

**All drawers include:**
- `Dispatch channel:` EMAIL or WHATSAPP (from `csm_nps_survey.dispatch_channel`)
- `Custom message sent:` {text} or "None" if `custom_message` is null
- `[View Account Profile ↗]`: links to `J-03 /csm/accounts/{institution_id}/?tab=feedback`
- `[Resend]`: available if `responded_at IS NULL` OR `superseded_by_id IS NOT NULL`. Opens Send Survey modal pre-filled.
- Superseded indicator: if `superseded_by_id IS NOT NULL`, amber banner: "This survey was superseded by a newer survey sent on {new survey sent_at}. [View newer survey]"

### Promoter → Case Study Nomination

PROMOTER survey rows (score 9–10) show an additional action in the Survey Detail Drawer:

```
  [Nominate for Case Study]
```

POST to `/csm/feedback/surveys/{id}/case-study-nominate/`. Sets `csm_nps_survey.case_study_nominated = true` and `case_study_nominated_at = now()`. Sends in-app notification to Marketing Manager (#64): "PROMOTER: {institution_name} (NPS 9/10) has been nominated for a case study by {csm_name}. [View account →]"

Available to CSM (#53) only.

Nominated institutions appear in the J-08 CS Reports → Promoter Report section as "Case Study Pipeline."

### NPS by Institution Type — Chart Clarification

The chart is a **horizontal bar chart** (single series, one bar per institution type). The description "grouped bar chart" in the section header was a misnomer — it is not grouped (no second data series). The X-axis shows NPS score (-100 to +100); bars are coloured green if score ≥ 40, amber if 20–39, red if < 20. Each bar label on hover shows: NPS score · N responses · Promoter% / Passive% / Detractor%.

### Bulk Dispatch — Skip Reason Storage

**`csm_nps_dispatch_skip` table:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial PK | — |
| skipped_quarter | varchar(10) NOT NULL | e.g., `Q2_2026` |
| skip_reason | text NOT NULL | Required; entered by CSM in confirmation dialog |
| skipped_by_id | FK auth_user NOT NULL | |
| skipped_at | timestamptz NOT NULL DEFAULT now() | |
| reinstated_at | timestamptz | Set if CSM later re-enables the dispatch via [Reinstate] |

POST `/csm/feedback/dispatch/skip/` requires `{"quarter": "Q2_2026", "reason": "..."}`. Reason min 10 chars.

**[Reinstate] button:** Appears in the Bulk Dispatch panel after a skip, allowing CSM to undo the skip before the dispatch date. POST to `/csm/feedback/dispatch/reinstate/`. Not available after the dispatch date has passed.

**Preview Next Batch modal full spec:**

Opens from [Preview Next Batch]. Modal lists institutions that Task J-3 will include in the next dispatch:

```
┌──────────────────────────────────────────────────────────────┐
│  Preview: Q2 2026 NPS Dispatch (1 Apr 2026)       [Close ×] │
│  Institutions to be surveyed: 134                            │
│  Skipped (surveyed < 60 days ago): 23                        │
│  Skipped (CHURNED_RISK tier): 8 (NPS not sent to CHURNED)   │
│                                                              │
│  Institution           Type        Last Surveyed             │
│  DPS Rohini            School      Q3 2025 (+92d)            │
│  Excel Coaching Hub    Coaching    Q3 2025 (+88d)            │
│  ...                                                         │
│                                                              │
│  [Export preview list as CSV]                                │
└──────────────────────────────────────────────────────────────┘
```

Task J-3 skips CHURNED_RISK institutions from bulk dispatch (sending NPS to an already-churned account is counterproductive and risks damaging the relationship further). CSM can override by sending an AD_HOC survey manually.

### Task J-3 — Full Dispatch Spec

| Step | Action |
|---|---|
| 1 | Check `csm_config['nps_quarterly_enabled']` — abort if false |
| 2 | Check for skip record in `csm_nps_dispatch_skip` for current quarter — abort if found |
| 3 | Select all institutions: `engagement_tier IN ('HEALTHY', 'ENGAGED')` AND last survey `sent_at < now() - interval '60 days'` AND `superseded_by_id IS NULL` |
| 4 | For each institution: create `csm_nps_survey` row; dispatch via F-06 (EMAIL for all; also WHATSAPP if COACHING type) |
| 5 | After 7 days: re-check `responded_at IS NULL AND reminder_sent_at IS NULL` — send reminder email; set `reminder_sent_at = now()` |
| 6 | After `nps_survey_expiry_days` (default 14 days): surveys with `responded_at IS NULL` are treated as expired in UI (no status column — derived from `link_expires_at < now()`) |

### CSAT KPI Tile (6th tile — Analyst-only)

The 5-tile KPI strip shows for all roles. CS Analyst (#93) sees a **6th tile**:

```
┌──────────────┐
│ 4.1 / 5      │
│ Avg CSAT     │
│ (period)     │
│ ↑+0.2 vs Q3  │
└──────────────┘
```

Sourced from `csm_nps_survey` WHERE `survey_type IN ('RENEWAL_CSAT','EBR_FEEDBACK')` AND `csat_score IS NOT NULL` for the selected period. Shows "— (insufficient data)" if fewer than 5 CSAT responses in period. The tile is hidden for all other roles (CSAT data is analytically sensitive and surfaced in full in J-08 CS Reports for non-Analyst roles).

### Chart Accessibility

All 4 charts (NPS Trend, CSAT Trend, Score Distribution, NPS by Segment) implement:
- `role="img"` and `aria-label="{chart_title} — {period}"` on the canvas element
- A visually hidden `<table class="sr-only">` below each chart containing the same data in tabular form, accessible to screen readers
- Chart.js `spanGaps: false` on NPS and CSAT trend charts (missing months render as breaks, not interpolated lines)
- Keyboard-navigable tooltips via Chart.js `options.plugins.tooltip.enabled: true` with focus event handlers

### Verbatim Text Search — Multilingual Handling

`to_tsvector('english', verbatim_feedback)` is used for English-language queries. For non-English feedback (Hindi, Telugu, Marathi etc.), PostgreSQL `pg_trgm` trigram similarity is used as a fallback: if the full-text search returns 0 results, the view automatically retries with `similarity(verbatim_feedback, ?)` > 0.3 using the `pg_trgm` extension. This is transparent to the user — they always see one combined result set with English FTS results first, then trigram matches. Trigram results are marked with a small "~" indicator icon beside the match count.

### Export — Async Spec

Export is **asynchronous** for result sets > 500 rows. Trigger: `?export=csv` appended to current filter URL.

- For ≤ 500 rows: synchronous CSV response (immediate download)
- For > 500 rows: async. [Export CSV] button replaced with "Preparing… ⏳" (disabled). Celery task generates file; on completion SUCCESS toast "Export ready. [Download]" with 60-second pre-signed R2 link. On failure: ERROR toast.

Export includes all columns from the Export CSV section, plus `case_study_nominated` and `dispatch_channel`.

### `csm_nps_survey` — Missing Columns (Addendum to Data Model in div-j-pages-list.md)

These columns are used in J-07 but absent from the `csm_nps_survey` table definition:

| Column | Type | Notes |
|---|---|---|
| custom_message | varchar(500) | Optional personalised intro sent with the survey link; null if not set |
| follow_up_resolved_at | timestamptz | Set when follow-up is marked resolved; null if unresolved |
| follow_up_resolved_by_id | FK auth_user | Who resolved the follow-up |
| case_study_nominated | boolean NOT NULL DEFAULT false | Set by CSM to flag promoters for Marketing case study pipeline |
| case_study_nominated_at | timestamptz | Timestamp of nomination |

### Resend Rate Limiting

A survey can be resent a maximum of **3 times** for the same institution + survey type combination within a 90-day window. On the 4th resend attempt within 90 days, the [Resend] button is disabled with tooltip: "Maximum resends reached for this survey type in this period. Contact your CSM lead if you need an exception." Tracked by counting `csm_nps_survey` rows with the same `institution_id` + `survey_type` where `sent_at >= now() - interval '90 days'`.

### [View All Pending] and [View All Follow-ups] Links

Both links update the main page URL and trigger a full filter refresh:
- [View all pending] → navigates to `?pending=1` (equivalent to checking the "Pending response" checkbox in the filter row, which re-renders the full survey table showing only pending rows)
- [View all follow-ups] → navigates to `?follow_up=1`
These are not modal popups — they apply the filter to the main survey table, bringing full pagination and sort controls.

### Mobile Layout

On viewports < 768px:
- KPI strip: 2×3 grid (2 tiles per row, 3 rows) — last tile (Response Rate or CSAT) spans full width on last row
- NPS trend chart and CSAT trend chart: stack vertically (each full width)
- Score distribution and NPS by segment: stack vertically
- Survey table: collapses to card view. Each card shows: Institution name · Score badge · Category badge · Sent date · Follow-up flag · [View] button. Other columns hidden.
- Verbatim panel and Pending/Follow-up panel: stack vertically
- Bulk Dispatch panel: hidden on mobile (CSM accesses via desktop only — complex control not suited to mobile)
