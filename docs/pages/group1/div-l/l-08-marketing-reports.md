# L-08 — Marketing Reports

**Route:** `GET /marketing/reports/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary roles:** Marketing Manager (#64), Marketing Analyst (#98)
**Also sees:** SEO Exec (#65) — content section; Social Manager (#66) — social section; Performance Marketing Exec (#67) — campaign section; Brand Manager (#68) — brand section; Email Exec (#100) — email section

---

## Purpose

Consolidated, pre-built reporting layer for Division L. Replaces ad-hoc spreadsheet requests from the Marketing Manager. The Analyst generates and maintains report templates. The Manager uses them in quarterly budget reviews, board presentations, and agency briefings. Each role sees a scoped section relevant to their function — a Social Manager cannot read paid campaign ROAS. Scheduled monthly delivery eliminates the need for manual report generation.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Monthly summary | Pre-aggregated from `mktg_campaign_daily_metric` + `mktg_lead_attribution` + `mktg_content` | 60 min |
| Channel mix | SUM spend + leads by channel for period | 30 min |
| Campaign ROI table | `mktg_campaign` + `mktg_campaign_daily_metric` + `mktg_lead_attribution` + `sales_lead` | 30 min |
| Content performance | `mktg_content` WHERE status='PUBLISHED' + GSC data from `mktg_content.organic_clicks_30d` | 60 min |
| SEO summary | `mktg_keyword` aggregate + `mktg_seo_domain_metric` | 60 min |
| Social performance | `mktg_social_post` aggregate + `mktg_social_platform_metric` | 60 min |
| Email performance | `mktg_email_sequence` + `mktg_email_send` aggregate | 30 min |
| Brand asset activity | `mktg_asset_download_log` aggregate | 60 min |
| Scheduled report log | `mktg_report_delivery_log` | 5 min |

All report data served from pre-aggregated queries. No live cross-tenant scans. `?nocache=true` for Manager + Analyst.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?section` | `summary`, `channel_mix`, `campaign_roi`, `content`, `seo`, `social`, `email`, `brand` | `summary` | Active report section |
| `?period` | `this_month`, `last_month`, `this_quarter`, `last_quarter`, `last_6m`, `ytd`, `custom` | `last_month` | Reporting window |
| `?from` | `YYYY-MM-DD` | — | Custom period start |
| `?to` | `YYYY-MM-DD` | — | Custom period end |
| `?compare` | `previous_period`, `same_period_last_year` | — | Period comparison overlay |
| `?export` | `csv`, `pdf` | — | Export current section |
| `?nocache` | `true` | — | Bypass Memcached (Manager + Analyst only) |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/report-summary/` | Monthly Summary section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-channel-mix/` | Channel Mix section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-campaign-roi/` | Campaign ROI section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-content/` | Content Performance section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-seo/` | SEO Summary section | Section nav | `#l-report-body` |
| `htmx/l/report-social/` | Social Performance section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-email/` | Email Performance section | Section nav + period change | `#l-report-body` |
| `htmx/l/report-brand/` | Brand Activity section | Section nav + period change | `#l-report-body` |

All section loads swap `#l-report-body` only — the nav sidebar and controls remain mounted.

---

## Page Layout

```
┌──────────────────────────────────────────────────────────────────────────┐
│  MARKETING REPORTS                                                       │
│  Period: [Last Month ▼]  [from ____] [to ____]  Compare: [None ▼]       │
│                                                [Export ▼]  [Schedule ▼]  │
├──────────────────────┬───────────────────────────────────────────────────┤
│  SECTION NAV         │  REPORT BODY                                      │
│                      │                                                   │
│  ● Summary           │  (active section content — see below)             │
│  ○ Channel Mix       │                                                   │
│  ○ Campaign ROI      │                                                   │
│  ○ Content           │                                                   │
│  ○ SEO               │                                                   │
│  ○ Social            │                                                   │
│  ○ Email             │                                                   │
│  ○ Brand             │                                                   │
│                      │                                                   │
│  ─────────────────── │                                                   │
│  SCHEDULED REPORTS   │                                                   │
│  Monthly: Active ✓   │                                                   │
│  Next: 1 Apr 2026    │                                                   │
│  [Manage →]          │                                                   │
└──────────────────────┴───────────────────────────────────────────────────┘
```

Visible sections in the nav are scoped per role. Non-permitted sections are hidden from the nav entirely (not just greyed out).

---

## Section 1 — Monthly Summary

Full-portfolio overview. Visible to Manager + Analyst only.

**Top KPI cards (6):**

| KPI | Value | Delta |
|---|---|---|
| Total Ad Spend | ₹4.2L | +12% vs LM |
| Total Impressions | 18.4L | +8% |
| Total MQLs | 38 | +5 |
| Blended CPL | ₹1,105 | -16% |
| Deals Won (attributed) | 8 | +2 |
| Revenue Attributed | ₹18.6L | +28% |

**Month-over-month trend:** Line chart showing 12 months of: Spend (₹) · MQLs · Deals Won · Revenue Attributed. Four series, dual Y-axis.

**Channel mix donut:** % of total spend by channel this month.

**Content output:** Total blog posts published · total words written · avg organic position of published content.

**Social highlights:** Best-performing post (by engagement) per platform.

**Budget health:** Quarter budget burn % per channel (same bar chart as L-01 budget section).

---

## Section 2 — Channel Mix

Detailed spend allocation and performance comparison across all channels.

**Stacked bar chart:** Monthly spend by channel for last 12 months (stacked to show total and channel composition evolution).

**Channel comparison table:**

| Channel | Spend | MQLs | SALs | Won | CPL | CAC | ROAS | Budget % |
|---|---|---|---|---|---|---|---|---|
| Google Search | ₹1.8L | 14 | 9 | 3 | ₹12.9K | ₹60K | 4.7× | 72% |
| Meta Facebook | ₹1.3L | 12 | 7 | 2 | ₹10.8K | ₹65K | 4.0× | 72% |
| Meta Instagram | ₹80K | 6 | 3 | 0 | ₹13.3K | — | 0× | 100% |
| YouTube Ads | ₹40K | 4 | 2 | 1 | ₹10K | ₹40K | 9.0× | 40% |
| Email | ₹8K | 4 | 2 | 1 | ₹2K | ₹8K | 17.5× | 27% |
| Referral | ₹0 | 6 | 4 | 2 | ₹0 | ₹0 | ∞ | — |
| **Total** | **₹4.2L** | **46** | **27** | **9** | **₹9,130** | — | — | 61% |

Sort by any column. Click channel name → L-07 Attribution filtered to that channel.

**Budget reallocation recommendation (rule-based):**
Generated text if ROAS < 2× and budget burn > 70%: "Meta Instagram has 0 won deals despite ₹80K spend this quarter. Consider reducing budget by 50% and reallocating to YouTube Ads (ROAS 9.0×)."

---

## Section 3 — Campaign ROI

Individual campaign-level performance for all campaigns active in the period.

**Summary bar:** Total campaigns active · total spend · avg CPL · avg ROAS

**Campaign ROI Table:**

| Campaign | Channel | Status | Spend | MQLs | Won | CPL | ROAS | Start | End |
|---|---|---|---|---|---|---|---|---|---|
| SSC CGL 2026 — Search | Google Search | ACTIVE | ₹68K | 8 | 2 | ₹8.5K | 7.1× | 01 Apr | 30 Jun |
| Coaching Lead Gen — Meta | Meta Facebook | ACTIVE | ₹42K | 6 | 1 | ₹7K | 6.0× | 01 Mar | Ongoing |
| … | | | | | | | | | |

Sortable. ROAS column: green ≥ 4× · amber 2–4× · red < 2×. Click row → L-03 Campaign Detail.

**Export:** CSV with all columns including attribution model used.

---

## Section 4 — Content Performance

Published content analytics. Visible to Manager, Analyst, SEO Exec, Content Strategist.

**Summary strip:**
- Total articles published (period) · Total organic clicks (30d rolling) · Avg position of tracked keywords · Keywords in top 10

**Content performance table:**

| Title | Domain | Type | Published | Organic Clicks (30d) | Avg Position | Word Count | Status |
|---|---|---|---|---|---|---|---|
| SSC CGL 2026 Study Plan | SSC | EXAM_GUIDE | 15 Mar | 420 | 6.2 | 2,840 | PUBLISHED |
| RRB NTPC Syllabus Guide | RRB | EXAM_GUIDE | 02 Feb | 380 | 8.1 | 3,100 | PUBLISHED |
| … | | | | | | | |

Sortable by organic clicks, position, publish date. Click → L-04 Content Detail Drawer.

**Content pipeline health:**
- BRIEF: N · IN_PROGRESS: N · REVIEW: N · APPROVED: N
- Overdue content (past target_publish_date and not yet PUBLISHED): highlighted in red

---

## Section 5 — SEO Summary

Organic search performance overview. Visible to Manager, Analyst, SEO Exec, Content Strategist.

**Domain-level trend chart:** 12-month line chart of organic clicks (from GSC).

**Keyword rank distribution:**

```
Position 1–3:    ▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓  18 keywords
Position 4–10:   ▓▓▓▓▓▓▓▓▓▓▓▓▓▓      28 keywords
Position 11–20:  ▓▓▓▓▓▓▓▓▓▓          20 keywords
Position 21–50:  ▓▓▓▓▓▓▓▓            16 keywords
Position 51–100: ▓▓▓▓                 8 keywords
Not ranking:     ▓▓                   4 keywords
```

**Top gainers / losers table (last 30 days):**

| Keyword | Domain | Current Position | Prev Position | Δ | Volume |
|---|---|---|---|---|---|
| ssc cgl study plan 2026 | SSC | 4 | 10 | ▲+6 | 12,100 |
| … | | | | | |

---

## Section 6 — Social Performance

Cross-platform social analytics. Visible to Manager, Analyst, Social Manager.

**Platform summary cards:**

| Platform | Followers/Subs | Posts (period) | Total Reach | Avg Engagement Rate | Top Post |
|---|---|---|---|---|---|
| YouTube | 12,480 (+248) | 8 | 24K | 4.8% | SSC Maths Tricks (1,800 views) |
| Instagram | 8,920 (+180) | 14 | 18.2K | 3.9% | Board exam tips (3.2K reach) |
| Twitter/X | 4,200 (+62) | 22 | 14.6K | 1.8% | RRB announcement |

**Follower growth chart:** 12-week line chart per platform (multi-series).

**Post frequency calendar heatmap:** GitHub-style contribution graph showing posting frequency per day per platform.

**Engagement rate benchmark comparison:**
- YouTube: EduForge 4.8% vs Edu-sector benchmark 3.2% (green)
- Instagram: EduForge 3.9% vs benchmark 4.5% (amber)
- Twitter: EduForge 1.8% vs benchmark 2.1% (amber)

---

## Section 7 — Email Performance

Email marketing analytics. Visible to Manager, Analyst, Email Exec.

**Sequence performance table:**

| Sequence Name | Segment | Status | Enrolled | Open Rate | Click Rate | Bounce Rate | Unsubscribes |
|---|---|---|---|---|---|---|---|
| School Admin Drip | SCHOOL | ACTIVE | 280 | 38% | 12% | 1.2% | 3 |
| Post-Demo Follow-up | ALL | ACTIVE | 142 | 52% | 22% | 0.8% | 1 |
| Trial Expiry Nudge | COACHING | ACTIVE | 48 | 61% | 18% | 0.4% | 0 |

**Monthly send volume chart:** Bar chart of emails sent / opened / clicked per month for last 6 months.

**Deliverability metrics:**
- Bounce rate: 0.9% (target < 2%) · Unsubscribe rate: 0.4% (target < 0.5%) · Spam complaint rate: 0.01%
- All rates shown with green/amber/red indicators vs targets defined in `mktg_config`

---

## Section 8 — Brand Activity

Brand asset usage analytics. Visible to Manager and Brand Manager.

**Asset download summary:**
- Total downloads in period: 48 · Unique users: 8 · Most-downloaded asset: SSC Logo (Primary)

**Downloads by domain table:**

| Domain | Assets Available | Downloads (period) | Unique Downloaders |
|---|---|---|---|
| SSC | 18 | 22 | 5 |
| RRB | 12 | 14 | 4 |
| Coaching | 10 | 8 | 3 |
| … | | | |

**Pending approvals status:** Assets awaiting approval. Links to L-06 Brand Library.

**Deprecated assets count:** How many deprecated assets were downloaded in the period (indicates teams using outdated materials — follow up required).

---

## Scheduled Report Delivery

Manager and Analyst can configure automated monthly report delivery.

```
┌──────────────────────────────────────────────────────────────────┐
│  SCHEDULED REPORTS                           [+ Add Schedule]    │
│                                                                  │
│  Monthly Marketing Summary                                       │
│  Sent on: 1st of each month at 08:00 IST                        │
│  Recipients: Vandana M. (Manager), Priya N. (Analyst)            │
│  Format: PDF + CSV data pack                                     │
│  Last sent: 01 Mar 2026 ✓                                        │
│  [Edit]  [Send Now]  [Delete]                                    │
└──────────────────────────────────────────────────────────────────┘
```

**`mktg_report_schedule` table:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| sections | jsonb | Array of section keys to include |
| frequency | varchar(20) | `MONTHLY` · `WEEKLY` · `QUARTERLY` |
| day_of_month | int | For MONTHLY; 1–28 |
| day_of_week | int | For WEEKLY; 0=Mon |
| send_time_ist | time | e.g., 08:00:00 |
| recipient_ids | jsonb | Array of auth_user IDs |
| format | varchar(10) | `PDF` · `CSV` · `BOTH` |
| created_by_id | FK auth_user | |
| is_active | boolean | NOT NULL DEFAULT true |

Scheduled delivery uses Celery task (Task L-6). PDF generated server-side using WeasyPrint from the same HTMX report templates.

**[Send Now]:** Triggers immediate delivery outside the schedule. Confirmation dialog: "Send report to N recipients now?"

---

## Export

**[Export ▼]** dropdown: CSV · PDF

- **CSV:** Section-specific data as flat table. Filename: `eduforge_marketing_{section}_{period}_YYYY-MM-DD.csv`
- **PDF:** Server-rendered PDF of the current section with all charts (static images embedded). WeasyPrint renders from the HTMX template. Filename: `eduforge_marketing_report_{section}_{period}_YYYY-MM-DD.pdf`

Available to Manager and Analyst (full export). Role-scoped users (SEO, Social, etc.) can export their own section only.

---

## Role-Based Section Visibility

| Section | 64 Manager | 65 SEO Exec | 66 Social | 67 Perf. Mktg | 68 Brand | 98 Analyst | 99 Content Strat. | 100 Email Exec |
|---|---|---|---|---|---|---|---|---|
| Summary | Yes | No | No | No | No | Yes | No | No |
| Channel Mix | Yes | No | No | Yes (own) | No | Yes | No | No |
| Campaign ROI | Yes | No | No | Yes (own) | No | Yes | No | No |
| Content | Yes | Yes | No | No | No | Yes | Yes | No |
| SEO | Yes | Yes | No | No | No | Yes | Yes | No |
| Social | Yes | No | Yes | No | No | Yes | No | No |
| Email | Yes | No | No | No | No | Yes | No | Yes |
| Brand | Yes | No | No | No | Yes | No | No | No |

---

## Empty States

| Condition | Message |
|---|---|
| No data for selected period | "No marketing data available for the selected period." |
| No published content | "No content was published in this period." |
| No email sequences active | "No email sequences are active." |
| No scheduled reports | "No scheduled reports configured. [+ Add Schedule]" |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

**Toasts on this page:** export started, export ready (with [Download] link), export failed, report schedule created, report schedule updated, report schedule deleted, [Send Now] triggered, [Send Now] delivery confirmed — see L-00 §2.

**Section-level loading:** Each report section loads independently via HTMX. Sections not yet loaded show a full-section shimmer with a progress bar at top. If a section fails to load (API error or query timeout), it shows an inline error card: "Failed to load {section} data. [Retry]" — other sections continue loading normally.

**PDF generation latency:** PDF generation via WeasyPrint can take 5–30 seconds for full reports. [Export PDF] button replaced with "Generating PDF..." (disabled) while processing. On completion: SUCCESS toast "PDF ready. [Download]" with pre-signed R2 link (60-second TTL). On timeout (> 60 seconds server-side): ERROR toast "PDF generation timed out. Try reducing the date range or exporting individual sections."

**Scheduled report failure (Task L-6):**
If Celery task L-6 fails to deliver a scheduled report:
- Retry 3 times with 10-minute backoff
- After 3 failures: ERROR email to Marketing Manager + Analyst with subject "Scheduled report delivery failed"
- `mktg_report_delivery_log.status` = `FAILED` with `error_message` populated
- In-app notification to all recipients: "Your scheduled report could not be delivered. Check the Reports page."

**Comparison period overlay:**
When comparison mode is active:
- Line charts: current period = solid line, comparison period = dashed line in lighter shade, same colour family
- Bar charts: grouped bars (current vs. comparison side by side per category)
- KPI tiles: current value shown large; comparison value shown small below with delta % arrow
- Comparison mode applies globally to all sections simultaneously (single toggle at top of page)
- Comparison period is always the immediately preceding period of equal length

---

## Missing Spec Closes (Audit)

**`mktg_report_delivery_log` delivery history UI:**

Sub-panel within Scheduled Reports section, expandable per schedule row:

```
Delivery History — Monthly Marketing Summary
  01 Mar 2026  Delivered  Recipients: 2  [View PDF]
  01 Feb 2026  Delivered  Recipients: 2  [View PDF]
  01 Jan 2026  Failed     Error: WeasyPrint timeout
  01 Dec 2025  Delivered  Recipients: 2  [View PDF]
```

[View PDF] links to the archived R2 copy of the delivered report. R2 key: `reports/scheduled/{schedule_id}/{YYYY-MM-DD}.pdf`. Retained for 12 months; automatically expired by R2 lifecycle rule after 365 days.

**`mktg_report_delivery_log` full schema:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| schedule_id | FK mktg_report_schedule | ON DELETE SET NULL |
| delivered_at | timestamptz | NOT NULL DEFAULT now() |
| status | varchar(20) | `DELIVERED` · `FAILED` · `SENDING` |
| recipient_ids | jsonb | Snapshot of recipients at send time |
| format | varchar(10) | `PDF` · `CSV` · `BOTH` |
| r2_key | varchar(1000) | For PDF archive; NULL for CSV |
| error_message | text | NULL unless status = `FAILED` |
| triggered_by | varchar(20) | `SCHEDULE` · `MANUAL` (Send Now) |
| triggered_by_user_id | FK auth_user | NULL if SCHEDULE |

**PDF watermark:**
All exported PDFs include a diagonal watermark text: "EduForge Confidential — {user_full_name} — {export_datetime_IST}". WeasyPrint applies this via CSS `@page` background. Watermark is semi-transparent (opacity 0.08) to not obscure content.

**Per-section export scope:**
When a role-scoped user (e.g., SEO Executive #65 on SEO section) exports, the export contains only the data from their accessible section. The PDF header states: "EduForge Marketing Report — SEO Section — {period}". Full-report export (all sections) is available to Manager (#64) and Analyst (#98) only.

**Comparison period date range validation:**
If user selects a custom date range where the comparison period would fall before the earliest available data (`mktg_campaign_daily_metric` minimum date), comparison period shows "Insufficient data" for affected metrics rather than zeros.

**Report section: Summary — full spec:**
Available to Marketing Manager + Analyst only.
- Period-over-period KPI table: Total Spend · Total Leads · Overall CPL · Total Impressions · Organic Sessions · Social Reach · Emails Sent · WON Deals · ARR Won · ROAS
- Executive summary text box: free-text notes field (Manager can type; saved to `mktg_report_note` table keyed by `(period_start, period_end)`). Shown in PDF export below the KPI table.
- `mktg_report_note` table: `id`, `period_start date`, `period_end date`, `note text`, `written_by_id FK auth_user`, `written_at timestamptz`. UNIQUE on `(period_start, period_end)`.

**Report section: Channel Mix — full spec:**
- Spend share donut chart (same as L-01 but for selected period, not current month)
- Table: Channel · Spend · Leads · CPL · WON Leads · ROAS
- Period-over-period deltas per channel
- Available to Manager + Analyst + Performance Marketing Exec (#67, own channels only)

**Report section: Campaign ROI — full spec:**
- Top 10 campaigns by ROAS for the period
- Campaign ROI table: same columns as L-07 Campaign Attribution table
- "No campaigns in period" empty state if all campaigns started after period end or ended before period start

**Report section: Brand — full spec:**
- Assets uploaded in period: count by type and domain
- Approvals turnaround time: avg days from upload to approval for assets approved in period
- Most downloaded assets: top 10 by `mktg_asset_download_log.downloaded_at` in period
- Available to Marketing Manager + Brand Manager (#68) + Analyst

**Add Schedule drawer full spec:**

```
Add Report Schedule
  Schedule name*   [Monthly Marketing Summary         ]
  Sections*        [Summary] [Channel Mix] [Campaign ROI]
                   [Content] [SEO] [Social] [Email] [Brand]
  Frequency*       [Monthly                          ]
  Day of month*    [1st                              ]   (shown if MONTHLY)
  Send time*       [08:00 IST                        ]
  Recipients*      [Vandana M.] [+ Add recipient     ]
                   (search users by name)
  Format*          [PDF + CSV] [PDF only] [CSV only]
  [Cancel]                         [Save Schedule]
```

POST to `/marketing/reports/schedules/create/`. Validation:
- Name: required, max 300 chars
- At least one section selected
- Frequency: required
- Day of month: 1–28 (capped at 28 to avoid month-end issues)
- At least one recipient
- Recipients must be active users with access to at least one selected section

**Report date range picker — full spec:**
- Presets: Last 7 days · Last 30 days · Last 90 days · This month · Last month · This quarter · Last quarter · This year · Custom
- Custom: date range picker (from/to); max range 365 days
- Default: Last 30 days
- Date range persists in URL (`?from=YYYY-MM-DD&to=YYYY-MM-DD`)
- Comparison period toggle: [Compare to previous period] checkbox; when checked, shows comparison period label: "vs. {from} to {to}"

**Section navigation (sidebar on desktop):**
- Sticky left sidebar on desktop (>= 1024px) with section links
- Active section highlighted as user scrolls (Intersection Observer)
- On mobile: section nav collapses to a top horizontal scrollable tab bar (same as other pages)
- Sections not accessible to current role are hidden from nav (not just greyed out)

**Shareable report link:**
Manager can generate a shareable report link via [Share Report] button. Creates a signed URL with 7-day expiry and `?shared=true&token={uuid}` parameter. Recipient with the link can view the report (read-only, no login required) for 7 days. Token stored in `mktg_report_share` table: `id`, `token uuid`, `created_by_id FK auth_user`, `expires_at timestamptz`, `report_params jsonb` (sections, period, filters). Expired tokens return 410 Gone with "This report link has expired." page.

**Campaign Attribution table — full column spec (L-08 Campaign ROI section):**

| Column | Description |
|---|---|
| Campaign Name | Links to L-03 Campaign Detail |
| Channel | Badge |
| Spend (period) | Total spend in selected period |
| Leads | Attributed leads under selected model |
| CPL | Spend / Leads |
| WON Leads | Count where stage = `CLOSED_WON` |
| ARR Won | Sum of `sales_lead.arr_estimate_paise` for WON |
| ROAS | ARR Won / Spend |

Sorted by ROAS DESC by default.
