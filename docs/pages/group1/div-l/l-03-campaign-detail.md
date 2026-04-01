# L-03 — Campaign Detail

**Route:** `GET /marketing/campaigns/{id}/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Performance Marketing Exec (#67) — own campaigns; Marketing Manager (#64) — all campaigns
**Also sees:** Marketing Analyst (#98) — read-only all

---

## Purpose

Full profile for a single campaign. The Performance Marketing Exec reviews daily spend curves and lead trends before deciding to increase budget or pause. The Marketing Manager uses it to evaluate ROI before approving additional spend. The Analyst reads the lead attribution breakdown to understand which UTM content variants are driving the most sales-qualified leads. Creatives panel shows all ad copy and imagery for brand compliance checks by the Brand Manager.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Campaign header | `mktg_campaign` + `auth_user` (created_by) | 5 min |
| Budget vs spend tile | `mktg_campaign.budget_paise` + SUM `mktg_campaign_daily_metric.spend_paise` for campaign lifetime | 5 min |
| Daily metric chart | `mktg_campaign_daily_metric` for campaign lifetime ordered by metric_date | 15 min |
| KPI tiles | SUM aggregates from `mktg_campaign_daily_metric` for selected period | 10 min |
| Ad set breakdown table | `mktg_campaign_daily_metric` WHERE ad_set_id IS NOT NULL (if structured; else single row) | 15 min |
| Lead attribution panel | `mktg_lead_attribution` JOIN `sales_lead` WHERE campaign_id = this campaign | 5 min |
| Creatives panel | `mktg_creative` WHERE campaign_id = this campaign (see below) | 30 min |
| Change log | `mktg_campaign_log` WHERE campaign_id = this campaign ORDER BY logged_at DESC | 5 min |

`?nocache=true` available to Manager (#64) and Analyst (#98).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `7d`, `30d`, `90d`, `lifetime` | `30d` | Sets aggregation window for KPI tiles + daily chart |
| `?nocache` | `true` | — | Bypass Memcached (Manager + Analyst only) |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/campaign-kpi/{id}/` | KPI tiles | Page load + period change | `#l-camp-kpi` |
| `htmx/l/campaign-chart/{id}/` | Daily metric chart | Page load + period change | `#l-camp-chart` |
| `htmx/l/campaign-attribution/{id}/` | Lead attribution panel | Page load | `#l-camp-attribution` |
| `htmx/l/campaign-log/{id}/` | Change log | Page load | `#l-camp-log` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  ← Back to Campaigns                                                    │
│  SSC CGL 2026 — Google Search          [ACTIVE ●]    [Edit] [Pause]    │
│  Google Search · Lead Generation · Target: ALL · AP, TS, KA            │
│  Created by Arjun K. · 01 Apr 2026 → 30 Jun 2026                       │
├─────────────────────────────────────────────────────────────────────────┤
│  BUDGET vs SPEND            │  Period: [30 Days ▼]                      │
│  ₹68,420 spent of ₹75,000   │                                           │
│  ██████████████████░░  91%  │  KPI TILES (5)                            │
├─────────────────────────────────────────────────────────────────────────┤
│  DAILY METRIC CHART (line chart — spend / clicks / leads overlay)       │
├─────────────────────────────────────────────────────────────────────────┤
│  LEADS ATTRIBUTED TO THIS CAMPAIGN                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  CREATIVES PANEL              │  CHANGE LOG                             │
└───────────────────────────────┴─────────────────────────────────────────┘
```

---

## Campaign Header

```
┌──────────────────────────────────────────────────────────────────┐
│  SSC CGL 2026 — Google Search                         [ACTIVE ●] │
│  Channel: Google Search · Objective: Lead Generation             │
│  Segment: ALL · Region: Andhra Pradesh, Telangana, Karnataka     │
│  UTM: google / cpc / ssc-cgl-2026-search                         │
│  External ID: AW-98765432                                        │
│  Created by Arjun K.  · 01 Apr 2026 → 30 Jun 2026               │
│                                         [Edit] [Pause] [Archive] │
└──────────────────────────────────────────────────────────────────┘
```

**[Edit]:** Opens Edit Campaign Drawer (same fields as Create; channel cannot be changed after creation). POST to `/marketing/campaigns/{id}/edit/`. All changes logged to `mktg_campaign_log`.

**[Pause]:** PATCH `/marketing/campaigns/{id}/status/` sets status to `PAUSED`. Button label toggles to [Resume]. Inline swap via HTMX.

**[Archive]:** Confirmation dialog → sets status to `ARCHIVED`. Removes from active views; data preserved.

---

## Budget vs Spend Tile

```
┌──────────────────────────────────────────┐
│  Budget           ₹75,000               │
│  Spent (lifetime) ₹68,420    91% ████░   │
│  Remaining        ₹6,580                 │
│                                          │
│  Daily avg burn:  ₹2,281  (last 30 days) │
│  Est. budget end: 3 days from today ⚠    │
└──────────────────────────────────────────┘
```

- Red warning if remaining budget covers < 7 days at current burn rate
- Manager can click [Increase Budget] → opens inline budget edit (PATCH `budget_paise`); logged in change log
- Exec can request budget increase; actual increase requires Manager approval

---

## KPI Tiles (5 tiles, period-scoped)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 18.4L        │ │ 82,400       │ │ 0.45%        │ │ 12           │ │ ₹5,702       │
│ Impressions  │ │ Clicks       │ │ CTR          │ │ Leads        │ │ CPL          │
│              │ │              │ │              │ │              │ │              │
│ (30 days)    │ │ (30 days)    │ │              │ │ (30 days)    │ │              │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- **Impressions:** SUM `mktg_campaign_daily_metric.impressions` in period
- **Clicks:** SUM `mktg_campaign_daily_metric.clicks`
- **CTR (Click-Through Rate):** clicks / impressions × 100. Green if > channel benchmark in `mktg_config`
- **Leads:** SUM `mktg_campaign_daily_metric.leads_created`
- **CPL:** spend_paise / leads_created for period, formatted as ₹

---

## Daily Metric Chart

Line chart (Chart.js) with three series overlaid on dual Y-axes.

- Primary Y-axis (left): Spend (₹) and Clicks
- Secondary Y-axis (right): Leads
- X-axis: date labels (D Mon format)
- Three toggleable series: Spend (blue) · Clicks (green) · Leads (purple)
- Reference line: daily budget target = `budget_paise / campaign_duration_days`

Hover tooltip: date · spend · clicks · CTR · leads · CPL for that day

Dotted vertical lines mark: campaign start date, any pauses, any budget changes (from `mktg_campaign_log`).

---

## Lead Attribution Panel

Leads attributed to this campaign from `mktg_lead_attribution` + `sales_lead`.

```
┌──────────────────────────────────────────────────────────────────────────────┐
│  LEADS ATTRIBUTED TO THIS CAMPAIGN  (12 leads · ₹68,420 spend · CPL ₹5,702)│
│                                                                              │
│  Attribution model: [Last Touch ▼]           [?nocache=true link]           │
│                                                                              │
│  Institution Name          Segment   Stage           ARR Estimate  Date     │
│  ──────────────────────────────────────────────────────────────────────      │
│  KIMS Senior Secondary Sch  SCHOOL   DEMO_DONE       ₹1.2L         Mar 14   │
│  Excel Coaching Centre       COACHING  PROPOSAL_SENT  ₹3.8L        Mar 18   │
│  …                                                                          │
│                                                                              │
│  [View all 12 in Sales Pipeline →]   [Export Leads CSV]                     │
└──────────────────────────────────────────────────────────────────────────────┘
```

- Attribution model dropdown: First Touch · Last Touch · Linear (changes which leads are attributed to this campaign based on `mktg_lead_attribution.attribution_type`)
- Institution name links → K-03 Account Profile (Sales pipeline)
- Stage badges use Div K colour scheme
- ARR Estimate sourced from `sales_lead.arr_estimate_paise`
- [Export Leads CSV]: downloads leads attributed to this campaign; available to Manager + Analyst
- Analyst can change attribution model to see different attribution views

---

## Creatives Panel

Grid of creative assets associated with this campaign (ads, banners, copy variants).

> Note: `mktg_creative` is a lightweight supplementary table — actual creative management happens in the external ad platforms. This panel is for internal reference and brand compliance review.

```
┌──────────────────────────────────────────────────────────────────┐
│  CREATIVES (4 assets)                          [+ Add Creative]  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐           │
│  │  [thumbnail] │  │  [thumbnail] │  │  [AD COPY]   │           │
│  │ Banner 1200× │  │ Square 1080× │  │ Headline A   │           │
│  │ 628 (Google) │  │ 1080 (Meta)  │  │ (Text)       │           │
│  │ v1.0 ✓       │  │ v1.0 ✓       │  │ v1.0         │           │
│  └──────────────┘  └──────────────┘  └──────────────┘           │
│                                                                  │
│  [Download All]                                                  │
└──────────────────────────────────────────────────────────────────┘
```

**`mktg_creative` table (simplified):**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| campaign_id | FK mktg_campaign | ON DELETE CASCADE |
| name | varchar(300) | |
| creative_type | varchar(30) | enum `BANNER` · `SQUARE_IMAGE` · `AD_COPY_TEXT` · `VIDEO` |
| file_r2_key | varchar(1000) | NULL for text creatives |
| headline | varchar(300) | For text ad copy |
| description | text | For text ad copy |
| version | varchar(20) | DEFAULT `1.0` |
| approved_by_id | FK auth_user | Brand Manager or Marketing Manager |
| created_at | timestamptz | |

Brand Manager (#68) can flag a creative as brand non-compliant — adds a red ⚠ badge on the creative card and sends a notification to the campaign owner.

[+ Add Creative] → opens creative upload drawer (Performance Marketing Exec + Manager only).

---

## Change Log

Audit trail of all changes to this campaign.

```
┌──────────────────────────────────────────────────────────────────┐
│  CHANGE LOG                                                      │
│                                                                  │
│  Mar 19, 2026 14:32  Budget increased: ₹50,000 → ₹75,000        │
│                      by Arjun K. (approved by Vandana M.)        │
│  Mar 15, 2026 09:00  Status: PAUSED → ACTIVE                     │
│                      by Arjun K.                                 │
│  Mar 12, 2026 18:41  Status: ACTIVE → PAUSED                     │
│                      by Vandana M. (Marketing Manager)           │
│  Mar 01, 2026 00:00  Campaign created                            │
│                      by Arjun K.                                 │
└──────────────────────────────────────────────────────────────────┘
```

**`mktg_campaign_log` table:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| campaign_id | FK mktg_campaign | ON DELETE CASCADE |
| action | varchar(50) | enum `CREATED` · `STATUS_CHANGED` · `BUDGET_UPDATED` · `FIELD_UPDATED` · `CREATIVE_ADDED` |
| old_value | jsonb | Previous value for the changed field |
| new_value | jsonb | New value |
| performed_by_id | FK auth_user | |
| logged_at | timestamptz | NOT NULL DEFAULT now() |

---

## Role-Based UI

| Element | 64 Manager | 67 Perf. Mktg | 98 Analyst |
|---|---|---|---|
| View own / others' campaigns | All | Own only | All (read) |
| Edit campaign | Yes | Own | No |
| Pause / Resume | Yes | Own | No |
| Archive | Yes | No | No |
| Increase budget | Yes (inline) | Request only | No |
| Add creative | Yes | Own | No |
| Flag creative brand non-compliance | Deferred to #68 Brand Manager | No | No |
| Change attribution model | Yes | No | Yes |
| Export leads CSV | Yes | Own | Yes |
| Change log | Full | Own | Read |

---

## Empty States

| Condition | Message |
|---|---|
| No leads attributed | "No leads have been attributed to this campaign yet." |
| No creatives uploaded | "No creatives uploaded. [+ Add Creative]" |
| No daily metrics yet | "Metrics will appear after the first nightly import following campaign activation." |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

Toasts on this page: campaign edit saved, budget increased, budget increase requested, creative uploaded, brand non-compliance flagged — see L-00 §2.

**Skeleton states:** KPI tiles, daily chart, attribution panel each show shimmer during HTMX load.

**Stale metrics warning:** If `mktg_import_log` last successful run for this campaign's channel > 24h: amber banner inside KPI tiles section: "Metrics last updated {N}h ago."

---

## Missing Spec Closes (Audit)

**Budget increase request UI (Exec flow):**
Performance Marketing Exec sees [Request Budget Increase] button (instead of inline edit). Clicking opens:
```
┌──────────────────────────────────────────────────────────┐
│  Request Budget Increase                      [Close ×]  │
│  Current budget: ₹75,000                                  │
│  New budget*  [₹ _________ ]                              │
│  Reason*      [Why is additional budget needed?     ]    │
│  [Cancel]                       [Submit Request]         │
└──────────────────────────────────────────────────────────┘
```
POST to `/marketing/campaigns/{id}/budget-request/`. Creates row in `mktg_campaign_log` with action=`BUDGET_REQUESTED`. INFO toast: "Budget increase request sent to Marketing Manager."
Notification to Manager: email + in-app (see L-00 §7).

**Creative upload drawer full spec:**
```
┌──────────────────────────────────────────────────────────┐
│  Add Creative                                 [Close ×]  │
│  Creative name*   [SSC CGL Banner — 1200×628      ]      │
│  Type*            [Banner                       ▼]       │
│  Upload file      [🖼 Drop file or browse         ]      │
│                   Max 10MB. PNG, JPG, GIF, MP4, MOV.    │
│                                                          │
│  OR  Ad copy text                                        │
│  Headline         [EduForge — India's Exam Platform  ]   │
│  Description      [Prepare smarter with 50K+ MCQs…   ]  │
│                                                          │
│  [Cancel]                          [Upload Creative]     │
└──────────────────────────────────────────────────────────┘
```
POST to `/marketing/campaigns/{id}/creatives/`. For images/videos: pre-signed R2 POST URL.
`mktg_creative.approved_by_id` = NULL until Brand Manager (#68) approves.

**Brand non-compliance flow:**
Brand Manager (#68) viewing a campaign (read-only) can click [···] → [Flag as Non-Compliant] on any creative card:
→ Opens: "Compliance issue: [text input]" + [Flag]
→ Sets `mktg_creative.brand_compliant = false` + stores note in `mktg_creative.brand_note`
→ Red ⚠ banner on creative card: "Flagged: {note}"
→ Notification to campaign creator (email + in-app): "Creative '{name}' flagged by Brand Manager: {note}. Please upload a revised version."
→ Campaign owner can then [Upload New Creative] to replace it.

**Channel edit lock:** In Edit Campaign Drawer, `channel` field rendered as static text (not a dropdown). Tooltip on hover: "Channel cannot be changed after creation."

**Partial metrics (import failed some days):** If some metric_date rows exist but others are missing (partial import), chart shows dotted line for missing dates with tooltip: "Data not available for this date." Full gap days are shown as `null` data points (Chart.js `spanGaps: false`).

**Attribution model selection persistence:** Model selection stored in user's browser localStorage (`l-attr-model` key). Same default applied across L-03 and L-07.

**K-03 link when lead not found:** If `sales_lead.id` referenced in attribution panel no longer exists (deleted in K), show "—" in institution name column with tooltip "Lead removed from sales pipeline."
