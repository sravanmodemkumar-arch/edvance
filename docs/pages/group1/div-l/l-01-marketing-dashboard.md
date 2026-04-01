# L-01 — Marketing Command Center

**Route:** `GET /marketing/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Marketing Manager (#64)
**Also sees (restricted view):** SEO Exec (#65) — SEO + content strip only; Social Media Manager (#66) — social strip only; Performance Marketing Exec (#67) — campaign strip only; Brand Manager (#68) — brand tasks strip only; Marketing Analyst (#98) — analytics strip + read-only all; Content Strategist (#99) — content strip + calendar; Email & CRM Exec (#100) — email strip only

---

## Purpose

Morning briefing screen for the Marketing Manager. Consolidates paid spend burn, organic traffic, content pipeline status, social performance, lead generation, SEO movers, and budget utilisation into one viewport. Replaces the need to open five external dashboards before the daily standup. Each strip is scoped to the viewer's role — a Performance Marketing Exec landing here sees only their campaign KPIs and pending approvals, not social analytics or brand tasks.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| KPI strip — total ad spend MTD | SUM `mktg_campaign_daily_metric.spend_paise` WHERE metric_date in current month | 15 min |
| KPI strip — impressions MTD | SUM `mktg_campaign_daily_metric.impressions` WHERE metric_date in current month | 15 min |
| KPI strip — leads generated MTD | SUM `mktg_campaign_daily_metric.leads_created` WHERE metric_date in current month | 10 min |
| KPI strip — blended CPL | Total spend / total leads_created MTD | 10 min |
| KPI strip — budget burn % | SUM spend_paise current quarter / SUM `mktg_channel_budget.allocated_paise` current quarter × 100 | 30 min |
| Spend by channel chart | `mktg_campaign_daily_metric` JOIN `mktg_campaign.channel` GROUP BY channel for current month | 30 min |
| Weekly impressions trend | `mktg_campaign_daily_metric` GROUP BY ISO week for last 8 weeks | 60 min |
| Leads by channel chart | `mktg_lead_attribution` JOIN `mktg_campaign` GROUP BY channel for current month | 15 min |
| Content calendar strip | `mktg_content` WHERE target_publish_date BETWEEN today AND today+14d ORDER BY target_publish_date | 10 min |
| SEO movers | `mktg_keyword` WHERE (prev_position - current_position) != 0 ORDER BY ABS(delta) DESC LIMIT 10 | 60 min |
| Top campaigns strip | `mktg_campaign` + `mktg_campaign_daily_metric` aggregate WHERE status='ACTIVE' ranked by leads_created DESC LIMIT 5 | 15 min |
| Social performance strip | `mktg_social_post` aggregate by platform for last 7 days | 60 min |
| Budget utilisation bars | `mktg_channel_budget` + SUM `mktg_campaign_daily_metric.spend_paise` per channel current quarter | 30 min |
| Pending approvals | `mktg_content` WHERE status='REVIEW'; `mktg_brand_asset` WHERE approved_by_id IS NULL; `mktg_campaign` WHERE status='DRAFT' and created_by_id ≠ current_user | 5 min |
| Import health | `mktg_import_log` latest row per task_name | 5 min |

Cache keyed on `(user_id, current_month)`. `?nocache=true` available to Marketing Manager (#64) and Analyst (#98).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?period` | `this_month`, `last_month`, `this_quarter`, `last_quarter` | `this_month` | Sets reporting window for KPI strip and spend charts |
| `?nocache` | `true` | — | Bypass Memcached (Manager + Analyst only) |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Auto-refresh | Target ID |
|---|---|---|---|---|
| `htmx/l/kpi-strip/` | KPI Strip (5 tiles) | Page load + period change | 15 min | `#l-kpi-strip` |
| `htmx/l/spend-channel-chart/` | Spend by Channel donut | Page load + period change | 30 min | `#l-spend-channel` |
| `htmx/l/weekly-impressions/` | Weekly Impressions trend | Page load | 60 min | `#l-weekly-impressions` |
| `htmx/l/leads-by-channel/` | Leads by Channel bar | Page load + period change | 15 min | `#l-leads-channel` |
| `htmx/l/content-calendar-strip/` | Content Calendar peek | Page load | 10 min | `#l-content-calendar` |
| `htmx/l/seo-movers/` | SEO Rank Movers | Page load | 60 min | `#l-seo-movers` |
| `htmx/l/top-campaigns/` | Top Campaigns strip | Page load | 15 min | `#l-top-campaigns` |
| `htmx/l/social-strip/` | Social Performance strip | Page load | 60 min | `#l-social-strip` |
| `htmx/l/budget-bars/` | Budget Utilisation bars | Page load | 30 min | `#l-budget-bars` |
| `htmx/l/pending-approvals/` | Pending Approvals panel | Page load | 5 min | `#l-pending-approvals` |
| `htmx/l/import-health/` | Import Health badges | Page load | 5 min | `#l-import-health` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  MARKETING COMMAND CENTER     Period: [This Month ▼]        [Refresh]   │
├─────────────────────────────────────────────────────────────────────────┤
│  KPI STRIP (5 tiles)                                                    │
├───────────────────────────────┬─────────────────────────────────────────┤
│  SPEND BY CHANNEL (donut)     │  WEEKLY IMPRESSIONS TREND (line, 8w)   │
│                               │                                         │
├───────────────────────────────┴─────────────────────────────────────────┤
│  LEADS BY CHANNEL (bar chart)  │  BUDGET UTILISATION (progress bars)   │
├────────────────────────────────┴────────────────────────────────────────┤
│  TOP CAMPAIGNS (5 rows)        │  SOCIAL PERFORMANCE STRIP             │
├────────────────────────────────┴────────────────────────────────────────┤
│  CONTENT CALENDAR PEEK (next 14 days)                                   │
├────────────────────────────────┬────────────────────────────────────────┤
│  SEO RANK MOVERS (10 keywords) │  PENDING APPROVALS                    │
├────────────────────────────────┴────────────────────────────────────────┤
│  IMPORT HEALTH (5 task badges)                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip (5 Tiles)

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ ₹4.2L        │ │ 18.4L        │ │ 38           │ │ ₹1,105       │ │ 61%          │
│ Ad Spend MTD │ │ Impressions  │ │ Leads MTD    │ │ Blended CPL  │ │ Budget Burn  │
│              │ │ MTD          │ │              │ │              │ │ (Q1 2026)    │
│ ↑+12% vs LM  │ │ ↑+8% vs LM  │ │ ↑+5 vs LM   │ │ ↓-₹210 vs LM │ │ 61 of 100%  │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

- **Ad Spend MTD:** SUM of `spend_paise` / 100 formatted as ₹. Amber if > 80% of monthly budget allocation; red if > 100%.
- **Impressions MTD:** Total across all channels. Formatted with L/K suffix for readability.
- **Leads MTD:** Count of `sales_lead` records attributed to any campaign this month via `mktg_lead_attribution`.
- **Blended CPL (Cost per Lead):** Total spend / total leads. Formatted as ₹ per lead. Green if below target (set in `mktg_config`); red if above.
- **Budget Burn %:** Total quarter spend / total quarter budget × 100. Progress bar below tile. Red if burn % > 90% with > 30% of quarter remaining.

Delta shown vs same period last month. Click any tile → navigates to L-08 Reports with relevant section pre-selected.

---

## Spend by Channel Chart

Donut chart (Chart.js). Segments: Google Search · Google Display · Meta Facebook · Meta Instagram · YouTube Ads · Email · Referral.

- Hover: channel name · ₹ spend · % of total
- Legend below chart showing ₹ value per channel
- Click segment → L-02 Campaigns filtered to that channel

---

## Weekly Impressions Trend

Line chart — 8 weeks of weekly total impressions across all channels.

- X-axis: ISO week labels (Wk 1, Wk 2, …)
- Y-axis: impressions count
- Dotted reference line at 8-week average
- Hover: week label · impressions · % change vs previous week

---

## Leads by Channel Chart

Horizontal bar chart — leads generated by channel for the selected period.

```
Google Search    ████████████████  14 leads
Meta Facebook    ██████████        10 leads
Meta Instagram   ████████           8 leads
YouTube Ads      ██████             6 leads
Referral         ████               4 leads
Email            ██                 2 leads
```

Bars colour-coded by channel. Click bar → L-07 Attribution filtered to channel.

---

## Budget Utilisation

Progress bars per channel for the current quarter.

```
Google Search    [████████████░░░░░░░░]  ₹1.8L / ₹2.5L (72%)
Meta Facebook    [█████████████░░░░░░░]  ₹1.3L / ₹1.8L (72%)
Meta Instagram   [████████████████████]  ₹80K / ₹80K  (100%) ← RED
YouTube Ads      [████████░░░░░░░░░░░░]  ₹40K / ₹1.0L  (40%)
Email            [████░░░░░░░░░░░░░░░░]  ₹8K  / ₹30K   (27%)
```

Red bar = at or over budget. Amber = 80–99%. Values in ₹. [Edit Budgets] button (Manager only) → opens budget edit drawer.

**Budget Edit Drawer** (Manager #64 only):
- Table: channel · current allocation · new allocation (input)
- Quarter selector
- [Save] → PATCH `/marketing/budgets/`; updates `mktg_channel_budget`
- Validation: total across channels cannot exceed Finance-approved quarterly budget (stored in `mktg_config['quarterly_total_budget_paise']`)

---

## Top Campaigns Strip

Table of top 5 active campaigns ranked by leads generated MTD.

| Campaign | Channel | Spend MTD | Impressions | Leads | CPL |
|---|---|---|---|---|---|
| SSC CGL 2026 — Google Search | Google Search | ₹68K | 2.4L | 12 | ₹5,667 |
| Coaching Owner — Meta Lead Gen | Meta Facebook | ₹42K | 1.8L | 9 | ₹4,667 |
| … | | | | | |

Click row → L-03 Campaign Detail. Click [View All] → L-02 Campaigns.

---

## Social Performance Strip

Three platform summary cards (YouTube · Instagram · Twitter) for the last 7 days.

```
┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ YouTube          │ │ Instagram        │ │ Twitter/X        │
│ 12.4K views      │ │ 8.2K reach       │ │ 14.6K impressions│
│ 3 posts published│ │ 5 posts          │ │ 7 tweets         │
│ +248 subscribers │ │ 4.2% eng. rate   │ │ 1.8% eng. rate   │
└──────────────────┘ └──────────────────┘ └──────────────────┘
```

Click any card → L-05 Social Hub on that platform's tab.

---

## Content Calendar Peek (Next 14 Days)

Timeline view of upcoming content publish targets.

```
Mar 22  ● SSC CGL Strategy Guide (APPROVED) — SEO Exec
Mar 23  ○ RRB NTPC Mock Series Landing Page (REVIEW) — SEO Exec
Mar 25  ● Coaching Centre Case Study: Excel Hub (APPROVED) — Content Strategist
Mar 28  ○ School Exam Prep: CBSE Board Tips (IN_PROGRESS) — SEO Exec
Apr 02  ○ EduForge Platform Overview Whitepaper (BRIEF) — Content Strategist
```

- ● = APPROVED (ready to publish); ○ = lower status
- Status badge coloured: blue=BRIEF, yellow=IN_PROGRESS, orange=REVIEW, green=APPROVED
- Click item → L-04 Content & SEO Hub with that content item's drawer open
- [+ Add Brief] → opens content brief creation drawer (Content Strategist + Manager only)

---

## SEO Rank Movers (10 Keywords)

Top 10 keywords with biggest rank change in the last 7 days.

```
Keyword                         Domain      Vol    Pos   Δ
─────────────────────────────────────────────────────────
ssc cgl study plan 2026         SSC        12,100   4   ▲+6
coaching centre management app  COACHING    1,900   8   ▲+5
online mock test for rrb ntpc   RRB        22,000  11   ▲+3
school exam portal software     BOARD       3,600  18   ▲+2
…
intermediate exam preparation   INTERMED.   8,100  24   ▼-4
```

Green rows = improved rank; red rows = dropped rank. Click row → L-04 Content & SEO Hub with keyword detail panel open.

---

## Pending Approvals Panel

```
┌─────────────────────────────────────────────────────────────┐
│  PENDING APPROVALS                                          │
│                                                             │
│  Content (REVIEW stage)          3 items                    │
│  ○ SSC CGL Tips — awaiting review (Submitted by Rahul, 2d)  │
│  ○ Board Exam Landing Page (Submitted by Priya, 1d)         │
│  [View all content in review →]                             │
│                                                             │
│  Brand Assets (pending approval)  2 items                   │
│  ○ SSC Brand Kit v2.1 (Uploaded by Vandana, 5h)             │
│  [View all pending assets →]                                │
│                                                             │
│  Campaign Drafts                  1 item                    │
│  ○ RRB Group D — Meta Lead Gen (Created by Arjun, 3h)       │
│  [View all draft campaigns →]                               │
└─────────────────────────────────────────────────────────────┘
```

Visible only to Marketing Manager (#64) and Content Strategist (#99) (content approvals only). Each [View all →] link navigates to the relevant page pre-filtered to the approval-needed state.

---

## Import Health

Row of 5 status badges — one per Celery import task.

```
[✓ Google Ads  02:00]  [✓ Meta Ads  02:31]  [✓ GSC  03:02]  [✓ YouTube  03:33]  [⚠ Instagram  FAILED 04:01]
```

- Green check = last run succeeded
- Amber warning = partial import (some records failed)
- Red X = task failed; shows time of failure
- Click any badge → opens detail modal with `mktg_import_log` rows for that task (last 7 runs + error detail if failed)
- Failed task alerts already sent to DevOps + Marketing Manager via Notification Manager

Only visible to Marketing Manager (#64) and Marketing Analyst (#98).

---

## Role-Based Strip Visibility

| Section | 64 Manager | 65 SEO Exec | 66 Social | 67 Perf. Mktg | 68 Brand | 98 Analyst | 99 Content Strat. | 100 Email |
|---|---|---|---|---|---|---|---|---|
| KPI Strip (all 5) | Yes | CPL + Leads | Reach tile only | Spend + CPL | No | Yes | Leads tile | Email open rate tile |
| Spend by Channel | Yes | No | No | Yes (own) | No | Yes | No | No |
| Weekly Impressions | Yes | No | No | Yes | No | Yes | No | No |
| Leads by Channel | Yes | No | No | Yes | No | Yes | No | No |
| Budget Utilisation | Yes | No | No | Own channels | No | Yes | No | No |
| Top Campaigns | Yes | No | No | Own campaigns | No | Yes | No | No |
| Social Performance | Yes | No | Yes (full) | No | No | Read-only | No | No |
| Content Calendar | Yes | Own content | No | No | No | Read | Yes (full) | No |
| SEO Movers | Yes | Yes (full) | No | No | No | Read | Yes | No |
| Pending Approvals | Yes (all) | No | No | No | Own assets | No | Content only | No |
| Import Health | Yes | No | No | No | No | Yes | No | No |

---

## Empty States

| Condition | Message |
|---|---|
| No active campaigns | "No active campaigns this period. [Create Campaign →]" |
| No leads generated | "No leads attributed to marketing campaigns this period." |
| No content due in 14 days | "No content scheduled for the next 14 days. [Add Brief →]" |
| No SEO rank changes | "No keyword rank movements in the last 7 days." |
| No pending approvals | "All caught up — no items pending approval." with green checkmark |

---

## Toasts, Loaders & Error States

> Full toast message reference and loader/skeleton patterns: see [L-00 Global Spec](l-00-global-spec.md).

**Toasts on this page:**
- Budget saved: SUCCESS "Budget updated."
- Budget validation fail: ERROR "Total exceeds quarterly cap of ₹{amount}."
- Budget reduced below current spend: ERROR "Cannot reduce budget below current spend of ₹{spend}."

**Skeleton states:** All 11 HTMX targets show grey shimmer while loading (see L-00 §3).

**Stale data warning:** If any import task's last successful run > 24h ago, an amber banner appears inside the affected section (Import Health is always visible to Manager + Analyst regardless). See L-00 §14.

---

## Missing Spec Closes (Audit)

**Email strip (for Email Exec #100):**
The email strip shown on the dashboard to Email Exec (#100) contains:
- Emails sent MTD (SUM `mktg_email_send.sent_at` in current month)
- Avg open rate (30d)
- Active sequences count
- Pending bulk-send approval count (links to L-09 Approvals tab)

**Budget channel floor:** Channel budget can be set to ₹0 (pauses that channel's spending). Cannot be set below 0. Cannot reduce to below current quarter spend.

**SEO movers — unranked keywords:** A keyword moving from "not ranking" (NULL) to a ranked position shows "NEW" badge in the Δ column rather than a numeric delta.

**Import history modal:** Clicking any import health badge shows last 30 days of `mktg_import_log` rows for that task (not just 7). Each row: run_at, status badge, records_updated, error_detail (collapsed by default, [expand]).

**`?nocache=true` server enforcement:** Server validates that `request.user` is in role 64 or 98 before bypassing Memcached. Non-permitted users who craft the URL get cached data regardless (no 403 — silent enforcement).
