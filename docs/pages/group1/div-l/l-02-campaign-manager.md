# L-02 — Campaign Manager

**Route:** `GET /marketing/campaigns/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** Performance Marketing Exec (#67), Marketing Manager (#64)
**Also sees:** Marketing Analyst (#98) — read-only all campaigns; no write access

---

## Purpose

Master workspace for all paid and organic campaigns across Google Search, Google Display, Meta Facebook, Meta Instagram, YouTube Ads, Email, and Referral. Performance Marketing Exec creates, monitors, pauses, and archives their own campaigns. Marketing Manager has full visibility across all execs and can approve, bulk-pause, or reallocate budgets. Analyst reads everything to build attribution and ROI reports. The page is the single source of truth for campaign lifecycle management — external tools (Google Ads, Meta Ads) remain the execution layer; this page tracks strategic state, attribution config, and internal approvals.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Campaign table rows | `mktg_campaign` JOIN auth_user (created_by) LEFT JOIN SUM(`mktg_campaign_daily_metric`) for current month | Live — no cache |
| Channel tab counts | `mktg_campaign` GROUP BY channel + status in current user scope | 5 min |
| Status tab counts | `mktg_campaign` GROUP BY status in current user scope | 5 min |
| Budget utilisation per row | `mktg_channel_budget` + SUM spend_paise per campaign for current quarter | 5 min |
| Owner dropdown (Manager filter) | auth_user WHERE role IN (67) AND is_active=True | 60 min |

Campaign table is live (no Memcached) — spend and lead counts update after nightly import; status changes reflect immediately.

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?status` | `all`, `draft`, `scheduled`, `active`, `paused`, `ended`, `archived` | `active` | Filter by campaign status |
| `?channel` | `google_search`, `google_display`, `meta_facebook`, `meta_instagram`, `youtube_ads`, `email`, `referral` (comma-sep) | `all` | Filter by channel |
| `?objective` | `brand_awareness`, `lead_gen`, `retargeting`, `engagement`, `app_install` | `all` | Filter by campaign objective |
| `?segment` | `school`, `college`, `coaching`, `group`, `all` | `all` | Filter by target segment |
| `?owner` | user_id | — (exec sees own; manager sees all) | Filter by campaign creator (Manager only) |
| `?q` | string ≥ 2 chars | — | Search on campaign name and utm_campaign |
| `?sort` | `spend_desc`, `spend_asc`, `leads_desc`, `cpl_asc`, `created_desc`, `name_asc` | `spend_desc` | Table sort order |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?export` | `csv` | — | Export filtered campaign data (Manager + Analyst) |

All params persist in URL via `hx-push-url="true"`.

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/campaign-table/` | Campaign table body + pagination | Filter / sort / page change | `#l-campaign-table` |
| `htmx/l/campaign-tab-counts/` | Status + channel tab badges | After campaign create / status change | `#l-campaign-tabs` |
| `htmx/l/campaign-export/` | Async export trigger | Export button click | `#l-export-status` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CAMPAIGNS                                          [+ Create Campaign] │
├─────────────────────────────────────────────────────────────────────────┤
│  STATUS TABS                                                            │
│  [All(48)] [Active(12)] [Paused(6)] [Draft(4)] [Ended(22)] [Archived(4)]│
├─────────────────────────────────────────────────────────────────────────┤
│  CHANNEL TABS                                                           │
│  [All] [Google Search(8)] [Meta FB(5)] [Meta IG(3)] [YouTube(2)] [...]  │
├─────────────────────────────────────────────────────────────────────────┤
│  FILTER BAR                                                             │
│  [🔍 Search campaign name or UTM...]                                    │
│  [Objective▼]  [Segment▼]  [Owner▼]  [Clear All]                       │
├──────┬──────────────────────────┬──────────┬───────┬────────┬─────┬────┤
│  ☐   │ Campaign Name            │ Channel  │ Status│ Spend  │Leads│CPL │
├──────┼──────────────────────────┼──────────┼───────┼────────┼─────┼────┤
│  ☐   │ SSC CGL 2026 — Search   │ Google   │ACTIVE │ ₹68K   │  12 │₹5.7K│
│      │ Target: ALL INDIA, SCHOOL│ Search   │       │ 68%bgt │     │    │
├──────┼──────────────────────────┼──────────┼───────┼────────┼─────┼────┤
│  ☐   │ Coaching Owner Lead Gen  │ Meta FB  │ACTIVE │ ₹42K   │   9 │₹4.7K│
│      │ Target: COACHING, AP/TS  │          │       │ 52%bgt │     │    │
├──────┴──────────────────────────┴──────────┴───────┴────────┴─────┴────┤
│ [Budget%] [Start] [End] [Owner] [Actions ···]  ← columns continue →    │
├─────────────────────────────────────────────────────────────────────────┤
│  Showing 1–25 of 48   [Bulk Actions▼]   [Export CSV]   ← 1 2 3 →      │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Status Tabs

| Tab | Label | Badge source |
|---|---|---|
| All | All campaigns in scope | Total `mktg_campaign` for current user |
| Active | Currently running | status = `ACTIVE` |
| Paused | Manually paused | status = `PAUSED` |
| Draft | Not yet activated | status = `DRAFT` |
| Scheduled | Start date in future | status = `SCHEDULED` |
| Ended | Past end_date or manually ended | status = `ENDED` |
| Archived | Archived | status = `ARCHIVED` |

---

## Channel Tabs

Secondary tab row below status tabs. Filters the table to a single channel. Counts reflect campaigns in the currently selected status tab.

Channels shown: All · Google Search · Google Display · Meta Facebook · Meta Instagram · YouTube Ads · Email · Referral

---

## Campaign Table Columns

| Column | Description |
|---|---|
| ☐ | Checkbox for bulk selection |
| Campaign Name | Name + target segment badge + target region (2-line). Click → L-03 Campaign Detail |
| Channel | Channel badge with icon (G / M / YT / ✉ / 🔗) |
| Status | Badge: ACTIVE (green) · PAUSED (amber) · DRAFT (grey) · SCHEDULED (blue) · ENDED (grey-dark) · ARCHIVED (grey-light) |
| Spend MTD | ₹ spend this month + budget burn % as mini progress bar below. Red if >90% |
| Leads MTD | Count of `leads_created` this month from `mktg_campaign_daily_metric` |
| CPL | spend_paise / leads_created for MTD. Green if below target CPL from `mktg_config`; red if above |
| Budget % | Quarter budget burn % (spend_paise / budget_paise × 100) |
| Start Date | `start_date`. Future dates shown as countdown: "in 3 days" |
| End Date | `end_date` or "Ongoing" |
| Owner | Avatar + name of `created_by`. Manager sees all; exec sees own only |
| Actions | Context menu: [View] [Edit] [Pause / Resume] [Duplicate] [Archive] [Delete] |

**Row states:**
- ACTIVE: normal
- PAUSED: amber left border
- DRAFT: grey italic name — [Activate] action in menu
- ENDED: strikethrough on dates; [Reactivate] action (creates new campaign)
- ARCHIVED: collapsed to single line with [Restore] action

---

## Filter Bar

```
[🔍 Search campaign name or UTM campaign tag...]
[Objective: All ▼]  [Segment: All ▼]  [Owner: All ▼]  [Date Range: Custom ▼]  [Clear All Filters]
```

- **Search:** ILIKE on `mktg_campaign.name` + `mktg_campaign.utm_campaign`. Min 2 chars. Debounced 300ms.
- **Objective:** Multi-select (comma-separated). Options: Brand Awareness · Lead Gen · Retargeting · Engagement · App Install.
- **Segment:** Multi-select. Options: School · College · Coaching · Group · All.
- **Owner:** Single-select dropdown (Manager only; Exec sees own campaigns only).
- **Date Range:** Filter campaigns active within a date range (`start_date ≤ to AND (end_date IS NULL OR end_date ≥ from)`).

---

## Bulk Actions

Available when ≥1 campaign selected.

| Action | Who Can | Confirmation Required |
|---|---|---|
| Pause selected | Manager (#64); Exec (own) | Yes — "Pause N campaigns?" |
| Activate selected | Manager (#64); Exec (own, if DRAFT/PAUSED) | Yes |
| Archive selected | Manager (#64) | Yes — "Archive N campaigns? This removes them from active views." |
| Reassign owner | Manager (#64) | Yes + owner picker modal |
| Export selected | Manager + Analyst | No |

Bulk actions only apply to campaigns within the user's scope. A Performance Marketing Exec cannot bulk-act on other execs' campaigns even if they select them (server validates ownership before applying).

---

## Create Campaign Drawer

Opens from [+ Create Campaign] button. Full-page right drawer.

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Campaign                                     [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Campaign name*  [SSC CGL 2026 — Google Search              ]    │
│                                                                  │
│  Channel*        [Google Search                            ▼]    │
│  Objective*      [Lead Generation                          ▼]    │
│  Target segment* [All                                      ▼]    │
│  Target region   [Andhra Pradesh, Telangana, Karnataka      ]    │
│                  (comma-separated states / districts)            │
│                                                                  │
│  Budget (₹)*    [75,000                                     ]    │
│  Start date*     [01 Apr 2026              ]                     │
│  End date        [30 Jun 2026              ] (leave blank = ongoing)│
│                                                                  │
│  External campaign ID  [AW-98765432                         ]    │
│  (Google Ads campaign ID or Meta campaign ID)                    │
│                                                                  │
│  UTM tracking                                                    │
│  utm_source*     [google                                    ]    │
│  utm_medium*     [cpc                                       ]    │
│  utm_campaign*   [ssc-cgl-2026-search                       ]    │
│  utm_content     [ad-variant-a                              ]    │
│                                                                  │
│  Goals (optional)                                               │
│  Goal impressions  [500000                                  ]    │
│  Goal leads        [50                                      ]    │
│                                                                  │
│  [Cancel]                              [Create Campaign]         │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Name: required, max 300 chars, unique within active campaigns
- Channel: required
- Objective: required
- Segment: required
- Budget: required, positive integer (in ₹ — stored as paise server-side)
- Start date: required, must be ≥ today
- End date: if set, must be > start_date
- UTM source + medium + campaign: required; utm_campaign must be URL-safe (validated against `[a-z0-9\-_]+` regex)
- External campaign ID: optional; if provided and channel is `GOOGLE_SEARCH` or `GOOGLE_DISPLAY`, validated format `AW-\d+`

POST to `/marketing/campaigns/create/`. Returns HTMX response to close drawer + refresh table + update tab counts.

**Duplicate action:** Pre-fills the drawer from an existing campaign row. Campaign name prefixed with "Copy of …". UTM campaign gets `-v2` suffix to avoid duplicate attribution collisions.

---

## Inline Actions

**[Pause / Resume]:** PATCH `/marketing/campaigns/{id}/status/`. Flips `ACTIVE ↔ PAUSED`. Inline — no page reload. Row status badge updates via HTMX swap.

**[Archive]:** Moves campaign to ARCHIVED. Removes from default Active/Paused views. Spend data retained for reporting.

**[Delete]:** Hard delete only for DRAFT campaigns with zero spend. Confirmation dialog: "Delete this draft campaign? This cannot be undone." DELETE `/marketing/campaigns/{id}/`.

---

## Export CSV

Filename: `eduforge_campaigns_YYYY-MM-DD.csv`
Columns: campaign_id, name, channel, objective, target_segment, status, budget_inr, spend_mtd_inr, leads_mtd, cpl_inr, start_date, end_date, utm_source, utm_medium, utm_campaign, created_by, created_at

Available to Marketing Manager (#64) and Marketing Analyst (#98). Performance Marketing Exec can export their own campaigns only.

---

## Role-Based UI

| Element | 64 Manager | 67 Perf. Mktg | 98 Analyst |
|---|---|---|---|
| See all campaigns | Yes | Own only | Yes (read) |
| Create campaign | Yes | Yes (own) | No |
| Pause / Resume | Yes (any) | Own only | No |
| Archive | Yes | No | No |
| Delete draft | Yes | Own draft | No |
| Bulk reassign owner | Yes | No | No |
| Export CSV | Yes | Own only | Yes (all) |
| Owner filter dropdown | Yes | No (always `me`) | Yes |

---

## Empty States

| Condition | Message |
|---|---|
| No campaigns in current filter | "No campaigns match your filters. [Clear Filters]" |
| No active campaigns at all | "No active campaigns. [Create your first campaign →]" |
| Exec with no campaigns | "You haven't created any campaigns yet. [+ Create Campaign]" |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

Toasts: campaign created/paused/resumed/archived/deleted/duplicated/bulk actions — see L-00 §2 toast reference table.

**Export progress:** Async export. [Export CSV] button replaced with "Preparing… ⏳" (disabled) while generating. On completion: SUCCESS toast "Export ready. [Download →]". On failure: ERROR toast with retry option. Export file includes active attribution model label in header row.

**DRAFT → ACTIVE activation:** Exec clicks [Activate] (context menu on DRAFT row) → validation check:
1. `start_date ≥ today` (IST, server-side)
2. `budget_paise > 0`
3. At least one `mktg_creative` row exists (optional but warned if none: amber warning dialog "No creatives attached — proceed?")
4. If estimated recipients > `email_bulk_send_threshold` (email channel only): approval flow
→ PATCH `/marketing/campaigns/{id}/status/` → status = `ACTIVE` if validation passes.

**Pagination reset on filter:** If applying a filter results in fewer pages than the current `?page`, page resets to 1 silently (no error).

**Duplicate → utm_campaign uniqueness:** Server appends `-v2` (then `-v3`, etc.) until unique within ACTIVE + SCHEDULED campaigns. If `utm_campaign` is already unique, no suffix added.

**Bulk action scope enforcement:** Server rejects bulk operations on campaigns not owned by the requesting exec (role 67). Manager (role 64) can act on all. If partial rejection occurs, server returns: "Applied to {N} campaigns. Skipped {M} campaigns — insufficient permissions." Shown as WARNING toast.

**Campaign end-date auto-transition:** A Celery beat task runs nightly at 00:01 IST and sets `status = ENDED` for all campaigns where `end_date < today` and `status = ACTIVE`. No manual action required. Campaign owner receives IN-APP notification: "Your campaign '{name}' has ended."

---

## Missing Spec Closes (Audit)

**Meta campaign ID validation:** `external_campaign_id` for Meta campaigns: numeric string 15–16 digits (no prefix). Regex: `^\d{15,16}$`. For Google Display: same `AW-\d+` pattern as Search. For YouTube Ads: `^\d{10,12}$`. For email/referral: field disabled (no external ID).

**`utm_campaign` uniqueness scope:** Checked within currently ACTIVE + SCHEDULED campaigns only. Archived/ended campaigns do not block reuse of a utm_campaign value.

**Analyst sort/filter:** Analyst (#98) sees full filter bar in read-only mode. All filter controls enabled (they need to filter for report purposes). No write actions exposed.

**Channel budget progress bar colour:** Amber at 80–89%; red at 90–99%; dark-red at 100%+. Budget % shown per campaign uses the campaign's own `budget_paise` denominator, not the channel-level quarterly budget.
