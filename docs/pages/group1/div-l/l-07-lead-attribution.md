# L-07 — Lead Attribution

**Route:** `GET /marketing/attribution/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Marketing Analyst (#98), Marketing Manager (#64)
**Also sees:** Performance Marketing Exec (#67) — own campaigns only (read-only)

---

## Purpose

Answers the question every Marketing Manager needs answered before quarterly budget reviews: "Which channels and campaigns are actually generating revenue?" This page bridges Division L (Marketing) and Division K (Sales) — it maps `mktg_lead_attribution` records to `sales_lead` pipeline data to compute true cost-per-won-deal, not just cost-per-lead. The Analyst configures attribution models and builds the weekly data pack. The Manager uses it to reallocate budgets from low-ROI channels to high-ROI ones. Performance Marketing Exec can see attribution data for their own campaigns only.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip | `mktg_lead_attribution` JOIN `sales_lead` aggregate for selected period | 15 min |
| Marketing funnel chart | `mktg_lead_attribution` JOIN `sales_lead` — count at each stage | 15 min |
| Channel contribution table | `mktg_lead_attribution` JOIN `mktg_campaign` JOIN `sales_lead` GROUP BY channel | 15 min |
| Campaign attribution table | `mktg_lead_attribution` JOIN `mktg_campaign` JOIN `sales_lead` GROUP BY campaign | 15 min |
| UTM content breakdown | `mktg_lead_attribution` GROUP BY utm_content for selected channel/campaign | 15 min |
| Unattributed leads | `sales_lead` WHERE lead_id NOT IN (SELECT lead_id FROM mktg_lead_attribution) | 30 min |
| Won revenue chart | `sales_lead` WHERE stage='CLOSED_WON' JOIN `mktg_lead_attribution` GROUP BY channel for period | 30 min |

Cache keyed on `(user_id, period, attribution_model)`. `?nocache=true` for Analyst + Manager.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `this_month`, `last_month`, `this_quarter`, `last_quarter`, `last_6m`, `ytd` | `this_quarter` | Reporting window |
| `?model` | `first_touch`, `last_touch`, `linear` | `last_touch` | Attribution model applied to all metrics |
| `?channel` | channel enum | `all` | Filter to one channel |
| `?segment` | segment enum | `all` | Filter by institution segment |
| `?nocache` | `true` | — | Bypass Memcached (Manager + Analyst only) |
| `?export` | `csv` | — | Export attribution data (Manager + Analyst only) |

Attribution model selection persists in URL and affects all counts, CPL, and CAC calculations on the page.

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/attr-kpi/` | KPI strip | Page load + period/model change | `#l-attr-kpi` |
| `htmx/l/attr-funnel/` | Marketing funnel | Page load + period/model change | `#l-attr-funnel` |
| `htmx/l/attr-channel/` | Channel contribution table | Page load + filter/model change | `#l-attr-channel` |
| `htmx/l/attr-campaigns/` | Campaign attribution table | Channel click + filter change | `#l-attr-campaigns` |
| `htmx/l/attr-won-revenue/` | Won revenue by channel | Page load + period change | `#l-attr-won-revenue` |
| `htmx/l/attr-unattributed/` | Unattributed leads | Page load | `#l-attr-unattributed` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  LEAD ATTRIBUTION                                                       │
│  Period: [This Quarter ▼]   Model: [Last Touch ▼]  [?] [Export CSV]    │
│                               Segment: [All ▼]                          │
├─────────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                                    │
├─────────────────────────────────────────────────────────────────────────┤
│  MARKETING FUNNEL (horizontal)   │  WON REVENUE BY CHANNEL (bar chart)  │
│                                  │                                      │
├──────────────────────────────────┴──────────────────────────────────────┤
│  CHANNEL CONTRIBUTION TABLE                                             │
├─────────────────────────────────────────────────────────────────────────┤
│  CAMPAIGN ATTRIBUTION TABLE (filtered by selected channel)              │
├─────────────────────────────────────────────────────────────────────────┤
│  UTM CONTENT BREAKDOWN (for selected campaign)  │  UNATTRIBUTED LEADS   │
└─────────────────────────────────────────────────┴───────────────────────┘
```

---

## Attribution Model Selector

```
Model:  ○ First Touch  ●Last Touch  ○ Linear
        [?] Model explanation
```

**First Touch:** 100% credit to the first campaign/channel that touched the lead (earliest `mktg_lead_attribution` record per lead).

**Last Touch (default):** 100% credit to the most recent campaign/channel before the lead was created or advanced to DEMO stage.

**Linear:** Credit distributed equally across all touchpoints for a given lead. A lead with 3 touch points splits credit 33%/33%/33%.

[?] icon opens an info popover explaining each model and when to use it.

Model selection affects: all KPI calculations, channel contribution table, campaign table, and won revenue chart. All numbers are clearly labelled with the active model to prevent misinterpretation in exports.

---

## KPI Strip (5 Tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 38           │ │ 22           │ │ 8            │ │ ₹1,105       │ │ ₹18.6L       │
│ MQLs         │ │ SALs         │ │ Deals Won    │ │ Blended CPL  │ │ Revenue      │
│ (this qtr)   │ │ 58% SAL rate │ │ 36% conv.    │ │ (per MQL)    │ │ Attributed   │
│              │ │              │ │              │ │              │ │ to Marketing │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- **MQLs (Marketing Qualified Leads):** Count of `sales_lead` records with a `mktg_lead_attribution` row in the period.
- **SALs (Sales Accepted Leads):** Count of attributed leads where `sales_lead.stage` has progressed past `CONTACTED` (i.e., sales team accepted the lead).
- **Deals Won:** Count of attributed leads with `stage='CLOSED_WON'` in period.
- **Blended CPL:** Total marketing spend (all channels) / MQL count for period.
- **Revenue Attributed:** SUM `sales_lead.arr_estimate_paise` WHERE stage='CLOSED_WON' AND lead has attribution in period. Formatted as ₹ with L suffix.

MQL → SAL conversion rate shown under SAL tile. SAL → Won rate shown under Deals Won tile.

---

## Marketing Funnel

Horizontal funnel chart showing drop-off at each stage.

```
Marketing Funnel — Q1 2026 (Last Touch model)

  ╔══════════════════════════════════════════════════════╗
  ║  TOTAL LEADS IN PERIOD          138  (100%)          ║
  ╟──────────────────────────────────────────────────────╢
  ║  MQLs (has marketing attribution)  38  (28%)         ║
  ╟─────────────────────────────────────────────────────╢
  ║  SALs (progressed to DEMO+)       22  (58% of MQLs) ║
  ╟───────────────────────────────────────────────────╢
  ║  Proposals Sent                   14  (64% of SALs)║
  ╟──────────────────────────────────────────────────╢
  ║  CLOSED WON                        8  (57% of prop)║
  ╚══════════════════════════════════════════════════╝

  Unattributed leads: 100 (72%) — no marketing touch recorded
```

Click any funnel stage → filters the Channel Contribution table to show only leads at that stage.

---

## Won Revenue by Channel

Horizontal bar chart — ₹ ARR won per channel for the period.

```
Google Search   ████████████████████  ₹8.4L  (3 deals)
Meta Facebook   ████████████          ₹5.2L  (2 deals)
Referral        ████████              ₹3.6L  (2 deals)
Email           ████                  ₹1.4L  (1 deal)
Meta Instagram  ██                    ₹0.0L  (0 deals)
```

Only channels with ≥1 won deal shown. Hover: channel name · won ARR · deal count · avg deal size · avg CAC (spend per won deal).

---

## Channel Contribution Table

Master attribution table by channel.

| Channel | MQLs | SALs | SAL Rate | Proposals | Won | Win Rate | Spend | CPL | CAC | ARR Won | ROAS |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Google Search | 14 | 9 | 64% | 6 | 3 | 33% | ₹1.8L | ₹12,857 | ₹60,000 | ₹8.4L | 4.7× |
| Meta Facebook | 12 | 7 | 58% | 5 | 2 | 40% | ₹1.3L | ₹10,833 | ₹65,000 | ₹5.2L | 4.0× |
| Referral | 6 | 4 | 67% | 3 | 2 | 67% | ₹0 | ₹0 | ₹0 | ₹3.6L | ∞ |
| Email | 4 | 2 | 50% | 2 | 1 | 50% | ₹8K | ₹2,000 | ₹8,000 | ₹1.4L | 17.5× |
| … | | | | | | | | | | | |

**Column definitions:**
- **CPL:** Spend / MQLs
- **CAC (Cost to Acquire Customer):** Spend / Won deals
- **ROAS (Return on Ad Spend):** ARR Won ₹ / Spend ₹ (lifetime contract value basis). "∞" for zero-spend channels (referral, organic).

Click a channel row → expands / filters the Campaign Attribution Table below to show campaigns within that channel.

Sort by any column. Default sort: ARR Won DESC.

---

## Campaign Attribution Table

Drills one level deeper — shows individual campaigns for the selected channel.

| Campaign | MQLs | Won | Spend | CPL | CAC | ARR Won | ROAS | Status |
|---|---|---|---|---|---|---|---|---|
| SSC CGL 2026 — Search | 8 | 2 | ₹68K | ₹8,500 | ₹34,000 | ₹4.8L | 7.1× | ACTIVE |
| Board Exam Retargeting | 6 | 1 | ₹32K | ₹5,333 | ₹32,000 | ₹3.6L | 11.3× | ENDED |
| … | | | | | | | | |

Click a campaign row → opens UTM Content Breakdown for that campaign. Click campaign name → L-03 Campaign Detail.

---

## UTM Content Breakdown

For a selected campaign, shows which ad variants (utm_content) drove the most leads.

```
┌──────────────────────────────────────────────────────────────────┐
│  UTM CONTENT BREAKDOWN — SSC CGL 2026 — Search                  │
│                                                                  │
│  utm_content        MQLs  Won  CPL      CAC                      │
│  ad-variant-a         5    1   ₹6,800   ₹34,000                  │
│  ad-variant-b         2    1   ₹9,500   ₹19,000                  │
│  ad-variant-c         1    0   ₹22,000  —                        │
│                                                                  │
│  Insight: Variant B has higher CPL but better win rate.          │
│  Consider pausing Variant C.                                     │
└──────────────────────────────────────────────────────────────────┘
```

The "Insight" line is a rule-based generated text:
- If one variant's win rate > 2× another's: surfaces the difference
- If a variant has 0 wins after 10+ MQLs: flags it for review
- Not AI-generated — deterministic business logic in the view

---

## Unattributed Leads Panel

Leads with no `mktg_lead_attribution` row — entered the pipeline without a tracked marketing source.

```
┌──────────────────────────────────────────────────────────────────┐
│  UNATTRIBUTED LEADS (100 of 138 total — 72%)                     │
│                                                                  │
│  These leads entered the pipeline with no marketing attribution. │
│  Most common sources:                                            │
│  • ORGANIC_INBOUND (74) — website visitors; no UTM on form      │
│  • REFERRAL (no campaign) (18) — ref=existing_customer on URL   │
│  • DIRECT (8) — no referrer or UTM                              │
│                                                                  │
│  Recommendation: Add UTM parameters to all website forms to     │
│  reduce unattributed rate.                                       │
│                                                                  │
│  [View unattributed leads in pipeline →] (links to K-02)        │
└──────────────────────────────────────────────────────────────────┘
```

Data source: `sales_lead.lead_source` for leads without `mktg_lead_attribution`. Grouped by `lead_source` enum values.

---

## Export CSV

Filename: `eduforge_attribution_YYYY-MM-DD_{model}.csv`

Columns: lead_id, institution_name, segment, lead_source, attribution_type, campaign_name, channel, utm_source, utm_medium, utm_campaign, utm_content, stage, arr_estimate_inr, won_at, spend_allocated_inr (for linear model: fractional spend), cpl_inr, cac_inr

Header row notes the active attribution model. Available to Manager + Analyst.

---

## Role-Based UI

| Element | 64 Manager | 67 Perf. Mktg | 98 Analyst |
|---|---|---|---|
| View full attribution data | Yes | Own campaigns | Yes |
| Change attribution model | Yes | No | Yes |
| Export CSV | Yes | Own data | Yes |
| View unattributed panel | Yes | No | Yes |
| View UTM content breakdown | Yes | Own campaigns | Yes |
| View won revenue chart | Yes | No | Yes |

---

## Empty States

| Condition | Message |
|---|---|
| No attributed leads in period | "No marketing-attributed leads in the selected period." |
| No won deals from marketing | "No deals closed from marketing-attributed leads in this period." |
| No campaign attribution for selected channel | "No campaigns tracked for this channel in the selected period." |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

**Toasts on this page:** attribution model changed (INFO), export started, export ready, export failed — see L-00 §2.

**Skeleton states:** All 5 KPI tiles shimmer on page load and period change. Funnel chart shows placeholder bars. Channel Contribution table shows 6 skeleton rows. Campaign Attribution table shows 8 skeleton rows. All shimmers resolve within their respective cache TTLs.

**Attribution model change latency:** When user switches model via dropdown, all HTMX partials re-fetch simultaneously (parallel `hx-trigger`). INFO toast: "Attribution recalculated using {Model} Touch." Recalculation is server-side (no client-side re-computation).

**No data for period:** If `mktg_lead_attribution` has no rows for the selected period, funnel collapses to: "No attribution data for this period. Try extending the date range." KPI tiles show `—` (em dash) instead of zeros.

**Stale import warning:** If `mktg_import_log` last successful run > 24h for any channel, amber banner below the period picker: "Attribution data may be incomplete — last import was {N}h ago for {channel}." Same stale data logic as L-00 §4.

---

## Missing Spec Closes (Audit)

**Attribution sync frequency:**
`mktg_lead_attribution` rows are created/updated by the nightly Celery import tasks (L-1 through L-5). Each task reconciles attributions for leads created or updated in the last 48 hours (overlap window to handle late-arriving conversion events). Attribution for a lead can change if a new touchpoint arrives after the initial sync — the last attribution row for that lead is updated in place (not appended). The attribution model shown on this page is a calculation over the stored rows, not a stored result — changing the model dropdown recomputes from the raw `mktg_lead_attribution` rows.

**Linear model rounding spec:**
For the Linear attribution model, when a lead has N touchpoints, each campaign receives `1/N` credit. If N does not divide evenly into the CPL/spend figures, values are rounded to 2 decimal places (₹). The KPI tile "Total Leads (attributed)" under Linear model counts fractional leads summed and rounded to the nearest whole number per channel. Example: 3 channels each get 0.33 → displayed as 1 lead per channel (not 0).

**Pre-period lead handling:**
Leads whose first touchpoint was before the selected period start date, but whose conversion (stage = `WON` or `DEMO_DONE`) falls within the period, are included in the attribution panel under the "Converted in period" filter. Leads with first touch AND conversion both outside the period are excluded entirely. This matches standard marketing attribution convention.

**UTM Content Breakdown empty state:**
If no `utm_content` values are tracked (all leads have NULL `utm_content` in `mktg_lead_attribution`), the UTM Content Breakdown section shows: "No UTM content variants tracked in this period. Add `utm_content` tags to your campaign creative URLs to enable variant-level analysis."

**Unattributed leads panel — definition:**
A lead is "unattributed" if `sales_lead.id` has NO corresponding row in `mktg_lead_attribution` for the selected period. This can occur when: (a) the lead was created by direct Sales team input without a marketing touchpoint, or (b) the nightly import has not yet processed recent leads.

Unattributed panel columns:
- Institution Name → links to K-03 Account Profile
- Stage badge
- Created date
- Created by (Sales Rep name)
- ARR Estimate

[Export Unattributed] downloads as CSV: `eduforge_unattributed_leads_{period}_{YYYY-MM-DD}.csv`. Available to Manager + Analyst.

**ROAS (Return on Ad Spend) calculation:**
ROAS = ARR of WON deals attributed to paid channels / total paid channel spend for period.
- Only CLOSED_WON leads count toward ROAS numerator (not DEMO_DONE or PROPOSAL_SENT)
- Paid channels: Google Search, Google Display, Meta Facebook, Meta Instagram, YouTube Ads
- Organic channels (SEO, Referral, Email) are excluded from ROAS denominator
- ROAS displayed as ratio (e.g., 4.2×) and as ₹ return per ₹ spent

**CAC (Customer Acquisition Cost) calculation:**
CAC = total marketing spend (all channels) / count of CLOSED_WON leads for period.
Shown in Channel Contribution table per channel (channel-specific spend / channel WON leads).

**Attribution model stored in localStorage:**
`l-attr-model` key in browser localStorage. Default: `LAST_TOUCH`. Shared across L-03 (Campaign Detail attribution panel) and L-07. If localStorage is unavailable (private browsing), defaults to `LAST_TOUCH` silently with no error.

**Funnel stage counts:**
Funnel stages pulled from `sales_lead.stage` enum, mapped as:
- MQL: leads where `mktg_lead_attribution` row exists (any model)
- SQL: stage IN (`DEMO_DONE`, `PROPOSAL_SENT`, `NEGOTIATION`, `CLOSED_WON`, `CLOSED_LOST`)
- Demo Done: stage IN (`DEMO_DONE`, `PROPOSAL_SENT`, `NEGOTIATION`, `CLOSED_WON`)
- Proposal Sent: stage IN (`PROPOSAL_SENT`, `NEGOTIATION`, `CLOSED_WON`)
- Won: stage = `CLOSED_WON`

Stage names and colours use the same Div K colour scheme for visual consistency across the platform.

**Period comparison mode:**
When comparison mode is enabled (period picker → [Compare to previous period]), funnel bars show two bars side by side per stage (current period in solid colour; previous period in lighter shade). KPI tile deltas show arrow + % change vs. comparison period. Channel Contribution table gains two numeric columns per metric (current + previous). Comparison period is always the immediately preceding period of equal length (e.g., 30d vs. prior 30d; not calendar month vs. prior calendar month).

**Export with model label:**
CSV export filename: `eduforge_lead_attribution_{model}_{period}_{YYYY-MM-DD}.csv`
Where `{model}` = `first-touch` | `last-touch` | `linear`.
Header row includes: `Attribution model: Last Touch (as of export date)` as first row comment before column headers.

**Campaign Attribution table — full column spec:**

| Column | Description |
|---|---|
| Campaign Name | Links to L-03 Campaign Detail |
| Channel | Badge |
| Leads (attributed) | Count under selected model |
| Spend (period) | ₹ from `mktg_campaign_daily_metric` |
| CPL | Spend / Leads |
| WON Leads | Count where stage = `CLOSED_WON` |
| ARR Won | Sum of `sales_lead.arr_estimate_paise` for WON |
| ROAS | ARR Won / Spend |

Sorted by Leads DESC by default. Sortable by all numeric columns.
