# L-04 — Content & SEO Hub

**Route:** `GET /marketing/content/`
**Method:** Django `TemplateView` + HTMX part-loads; server-side pagination
**Primary roles:** SEO / Content Executive (#65), Content Strategist (#99)
**Also sees:** Marketing Manager (#64) — full access + approve; Marketing Analyst (#98) — read-only (keyword data + content performance)

---

## Purpose

Single workspace for the content production pipeline and SEO keyword portfolio. The SEO Executive creates content, tracks keyword positions, and monitors organic performance of published pages. The Content Strategist manages the editorial calendar, assigns briefs to authors, and approves content before it can be published. The Marketing Manager has the final publish gate. The Analyst reads SEO position data to correlate content performance with lead generation. No content reaches the live EduForge website without passing through the REVIEW → APPROVED status chain defined here.

---

## Data Sources

**Content Pipeline tab:**

| Section | Source | Cache TTL |
|---|---|---|
| Editorial calendar | `mktg_content` WHERE target_publish_date IS NOT NULL ORDER BY target_publish_date | 5 min |
| Content list | `mktg_content` JOIN auth_user (author, reviewer) | Live — no cache |
| Status tab counts | `mktg_content` GROUP BY status in current user scope | 5 min |

**SEO Tracker tab:**

| Section | Source | Cache TTL |
|---|---|---|
| Keyword table | `mktg_keyword` WHERE is_tracking=true | 15 min |
| Domain-level metrics | Nightly: domain authority, referring domains, organic traffic from GSC aggregate in `mktg_seo_domain_metric` | 60 min |
| Top organic pages | `mktg_content` WHERE status='PUBLISHED' ORDER BY organic_clicks_30d DESC LIMIT 20 | 60 min |
| Position trend chart | `mktg_keyword_position_history` for selected keyword (last 90 days) | 60 min |

Cache keys include user_id + active filters. `?nocache=true` available to Manager (#64) and Analyst (#98).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?tab` | `pipeline`, `seo` | `pipeline` | Active tab |
| `?status` | `brief`, `in_progress`, `review`, `approved`, `published`, `archived` | `all` | Filter content by status |
| `?type` | content_type enum | `all` | Filter by content type |
| `?domain` | `ssc`, `rrb`, `board`, `intermediate`, `coaching`, `groups`, `corporate` | `all` | Filter by exam domain |
| `?author` | user_id | — (exec sees own; strategist/manager see all) | Filter by author |
| `?due` | `overdue`, `this_week`, `this_month` | — | Filter by target publish date |
| `?q` | string ≥ 2 chars | — | Search on title and target_keyword |
| `?sort` | `due_asc`, `due_desc`, `created_desc`, `position_asc`, `volume_desc` | context-dependent | Sort order |
| `?page` | integer ≥ 1 | `1` | Pagination |
| `?kw` | keyword_id | — | Opens keyword detail panel for SEO tab |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/content-list/` | Content list table | Filter / sort / page change | `#l-content-list` |
| `htmx/l/content-calendar/` | Calendar view | Month navigation | `#l-content-calendar` |
| `htmx/l/keyword-table/` | Keyword table | Filter / sort / page | `#l-keyword-table` |
| `htmx/l/keyword-detail/` | Keyword detail panel | Click keyword row | `#l-keyword-detail` |
| `htmx/l/domain-metrics/` | Domain-level SEO metrics | Tab load | `#l-domain-metrics` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CONTENT & SEO HUB                                    [+ Add Brief]     │
├─────────────────────────────────────────────────────────────────────────┤
│  [Content Pipeline]  [SEO Tracker]                                      │
├─────────────────────────────────────────────────────────────────────────┤
│  (Content Pipeline tab active by default)                               │
│                                                                         │
│  STATUS TABS                                                            │
│  [All(42)] [Brief(8)] [In Progress(12)] [Review(4)] [Approved(3)]       │
│  [Published(14)] [Archived(1)]                                          │
│                                                                         │
│  [📅 Calendar View]  [☰ List View]                                      │
│                                                                         │
│  FILTER BAR                                                             │
│  [🔍 Search title or keyword...]                                        │
│  [Type▼] [Domain▼] [Author▼] [Due▼]  [Clear All]                      │
│                                                                         │
│  ┌─────── CALENDAR / LIST VIEW ──────────────────────────────────────┐  │
│  │ (see below)                                                       │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Content Pipeline Tab

### Status Tabs

| Tab | Colour | Meaning |
|---|---|---|
| All | — | All content items |
| Brief | Blue | Content brief created; not yet in writing |
| In Progress | Yellow | Author is writing |
| Review | Orange | Submitted for review by Content Strategist |
| Approved | Green | Approved; ready to publish |
| Published | Grey-green | Live on website |
| Archived | Grey | Removed from active tracking |

### Calendar View

Monthly calendar grid. Each day shows content items with their `target_publish_date`.

```
                    MARCH 2026
Mon    Tue    Wed    Thu    Fri    Sat    Sun
                                           1
 2      3      4      5      6      7      8
                             ● SSC CGL
                               Guide
 9     10     11     12     13     14     15
        ● RRB         ○ Board
          NTPC           Tips
16     17     18     19     20     21     22
                                    ○ Coach.
                                      Case St.
23     24     25     26     27     28     29
 ● Coach
   Study
30     31
```

- ● = APPROVED (ready to publish); ○ = lower status
- Colour by status: blue=BRIEF, yellow=IN_PROGRESS, orange=REVIEW, green=APPROVED, grey-green=PUBLISHED
- Click item → opens Content Detail Drawer
- Drag-and-drop to change `target_publish_date` (Content Strategist + Manager only)
- [+ Add Brief on date] → opens Brief Creation Drawer with date pre-filled

### List View

Sortable, paginated table of all content items.

| Column | Description |
|---|---|
| Title | Content title. Click → Content Detail Drawer |
| Type | Badge: BLOG_POST · LANDING_PAGE · CASE_STUDY · WHITEPAPER · INFOGRAPHIC · EXAM_GUIDE |
| Domain | Badge: SSC · RRB · BOARD · INTERMEDIATE · COACHING · GROUPS · CORPORATE |
| Status | Status badge with colour from tab scheme |
| Author | Avatar + name |
| Target Date | Date (red if overdue; amber if due within 3 days) |
| Organic Clicks | 30d organic clicks (synced from GSC). "—" if UNPUBLISHED. |
| Avg Position | 30d avg search position. "—" if UNPUBLISHED. |
| Actions | [Review] [Approve] [Publish] [Edit] [Archive] — state-dependent |

**[Review]:** Available to Content Strategist (#99). Opens review drawer. Approve → status = `APPROVED`. Return → opens comment input; status stays `REVIEW`. Notification sent to author.

**[Approve]:** Marketing Manager (#64) final approve gate. Status → `APPROVED`. Enables [Publish].

**[Publish]:** Manager or Content Strategist (if Manager has pre-approved). Sets status = `PUBLISHED`, records `published_at = now()`. Opens URL input modal: "Enter the live URL where this content was published." Sets `mktg_content.url`.

**[Edit]:** Opens Content Edit Drawer. Author can edit own BRIEF/IN_PROGRESS content. Once in REVIEW, only reviewer can edit.

**[Archive]:** Manager only. Confirmation dialog.

---

### Content Detail Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  SSC CGL 2026: Complete 90-Day Study Plan          [Close ×]     │
├──────────────────────────────────────────────────────────────────┤
│  Type: EXAM_GUIDE · Domain: SSC · Status: APPROVED               │
│  Target keyword: "ssc cgl study plan 2026"                       │
│  Author: Rahul Sharma   Reviewer: Priya N. (Content Strategist)  │
│  Target publish date: 22 Mar 2026                                │
│  Word count: 2,840                                               │
├──────────────────────────────────────────────────────────────────┤
│  Organic performance (post-publish):                             │
│  Clicks (30d): 420 · Avg position: 6.2                           │
├──────────────────────────────────────────────────────────────────┤
│  Review notes:                                                   │
│  "Good structure. Add a section on mock test strategy for        │
│   Tier-2 Maths. Target keyword density looks appropriate."       │
│  — Priya N., 18 Mar 2026                                         │
├──────────────────────────────────────────────────────────────────┤
│  [Edit]  [Publish]  [Archive]  [View live →]                     │
└──────────────────────────────────────────────────────────────────┘
```

---

### Create / Edit Content Brief Drawer

```
┌──────────────────────────────────────────────────────────────────┐
│  Create Content Brief                                [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Title*          [SSC CGL 2026 Study Plan — 90 Days         ]    │
│  Content type*   [Exam Guide                              ▼]     │
│  Exam domain*    [SSC                                     ▼]     │
│  Target keyword  [ssc cgl study plan 2026                  ]     │
│  Assign author*  [Rahul Sharma (SEO Exec)                 ▼]     │
│  Target publish  [22 Mar 2026                              ]     │
│                                                                  │
│  Brief details:                                                  │
│  [Outline what this content should cover, target audience,  ]    │
│  [key points, tone, and any reference links.                ]    │
│                                                                  │
│  Word count target  [2500–3000                              ]    │
│                                                                  │
│  [Cancel]                              [Create Brief]            │
└──────────────────────────────────────────────────────────────────┘
```

Validation: Title, type, domain, author, publish date all required. POST to `/marketing/content/create/`. Notification sent to assigned author.

---

## SEO Tracker Tab

### Domain-Level Metrics Strip

```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ DA 28        │ │ 1,240        │ │ 4,820        │ │ 82           │
│ Domain Auth. │ │ Referring    │ │ Organic      │ │ Keywords in  │
│              │ │ Domains      │ │ Clicks (30d) │ │ Top 10       │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

Data sourced from `mktg_seo_domain_metric` (nightly GSC + third-party SEO API import). Trending delta vs 30 days ago shown beneath each tile.

### Keyword Table

Sortable, filterable table of all tracked keywords.

| Column | Description |
|---|---|
| Keyword | Full keyword text. Click → opens Keyword Detail Panel (right side) |
| Domain | Exam domain badge |
| Volume | Monthly search volume |
| Difficulty | 0–100 (colour: green ≤30 · amber 31–70 · red >70) |
| Position | Current GSC position (1–100). "—" if not ranking. Green if 1–3 · blue 4–10 · amber 11–20 · grey >20 |
| Δ Position | Change vs 7 days ago. ▲ green = improved (lower number). ▼ red = dropped. |
| Target URL | Linked page slug (shortened). Click → opens page in new tab if published |
| Tracking | Toggle switch — enabled/disabled. Manager + Strategist can toggle |
| Actions | [View Detail] [Edit] [Remove] |

**Filter bar:** Domain filter (multi-select) · Position range filter · Volume range · Difficulty range · [Overdue pages ☐] (keywords where target_url has no published content yet)

**[+ Add Keyword]:** Opens keyword add drawer (Content Strategist + Manager). Fields: keyword text, exam domain, monthly volume (manual), difficulty (manual), target URL.

### Keyword Detail Panel

Slides in from the right when a keyword row is clicked.

```
┌──────────────────────────────────────────────────────────────────┐
│  "ssc cgl study plan 2026"                          [Close ×]    │
├──────────────────────────────────────────────────────────────────┤
│  Domain: SSC · Volume: 12,100 · Difficulty: 38                   │
│  Current position: 4  (↑ from 10 last week)                      │
│  Target URL: /blog/ssc-cgl-2026-study-plan                       │
├──────────────────────────────────────────────────────────────────┤
│  POSITION TREND (last 90 days, line chart)                       │
│  Y-axis inverted (position 1 at top)                             │
├──────────────────────────────────────────────────────────────────┤
│  Content linked to this keyword:                                 │
│  ● SSC CGL 2026: Complete 90-Day Study Plan (PUBLISHED)          │
│    420 organic clicks (30d) · Avg position: 6.2                  │
├──────────────────────────────────────────────────────────────────┤
│  [Edit keyword]  [Remove from tracking]                          │
└──────────────────────────────────────────────────────────────────┘
```

**`mktg_keyword_position_history`** table:

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| keyword_id | FK mktg_keyword | ON DELETE CASCADE |
| recorded_date | date | NOT NULL |
| position | numeric(5,1) | NULL if not ranking |
| UNIQUE | (keyword_id, recorded_date) | |

### Top Organic Pages

Table of top 20 published content items ranked by `organic_clicks_30d` DESC.

| Page Title | Domain | Clicks (30d) | Avg Position | Published |
|---|---|---|---|---|
| SSC CGL 2026 Study Plan | SSC | 420 | 6.2 | 15 Mar 2026 |
| RRB NTPC Syllabus Guide | RRB | 380 | 8.1 | 02 Feb 2026 |
| … | | | | |

Click row → opens Content Detail Drawer.

---

## Role-Based UI

| Element | 64 Manager | 65 SEO Exec | 98 Analyst | 99 Content Strat. |
|---|---|---|---|---|
| See all content | Yes | Own content | Read all | Yes |
| Create brief | Yes | Submit only | No | Yes |
| Edit content | Yes | Own (BRIEF/IN_PROGRESS) | No | Any at REVIEW+ |
| Review + approve | Yes | No | No | Yes (REVIEW → APPROVED) |
| Publish (final) | Yes | No | No | Yes (after Manager pre-approval) |
| Archive | Yes | No | No | Yes |
| Add keywords | Yes | No | No | Yes |
| Remove keywords | Yes | No | No | Yes |
| Edit keyword metadata | Yes | Read | Read | Yes |
| Toggle tracking | Yes | No | No | Yes |
| View keyword detail + trend | Yes | Yes | Yes | Yes |
| Export keyword data | Yes | No | Yes | Yes |

---

## Empty States

| Condition | Message |
|---|---|
| No content in current filter | "No content items match your filters. [Clear Filters]" |
| No content in pipeline at all | "No content briefs yet. [+ Add Brief →]" |
| No keywords tracked | "No keywords are being tracked. [+ Add Keyword →]" |
| No organic rankings | "No keywords are ranking in the top 100 yet." |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

Toasts: brief created, submitted for review, returned, approved, published, archived, keyword added/removed, date rescheduled — see L-00 §2.

**Content status change notifications:**
- Author submits → REVIEW: reviewer notified (email + in-app). See L-00 §7.
- Reviewer returns: author notified with review comment text.
- Reviewer approves: author notified.
- Manager publishes: author + Manager notified in-app.
- Content overdue: Celery beat daily 09:00 IST alerts author + Content Strategist.

**Skeleton states:** Content list table rows, calendar cells with dot indicators, keyword table rows — all use shimmer while loading.

**GSC API failure:** If Task L-3 fails, `organic_clicks_30d` and `avg_position_30d` show "–" with tooltip "Last GSC sync failed. Showing last known data from {date}."

---

## Missing Spec Closes (Audit)

**`mktg_seo_domain_metric` source:** Third-party SEO API (DataForSEO or equivalent) called WEEKLY (not daily) for domain authority and referring domains. GSC provides organic_clicks, impressions, CTR, avg_position DAILY. Weekly fields are carried forward on daily rows (not NULL) so trend charts remain continuous.

**Content edit concurrency:** If two users attempt to open the edit drawer for the same content item simultaneously, server uses an optimistic lock (`updated_at` check). If the second user saves over a newer version, they receive ERROR: "Content was modified by {name}. Reload to see latest version."

**Auto-save:** Content brief drawer does NOT auto-save (short form). Template editor (L-09) does auto-save. Content edit is drawer-based — no auto-save; explicit [Save Draft] available.

**Multiple keywords per content item:** `mktg_content.target_keyword` is a single primary keyword field. Secondary keywords tracked via a `mktg_content_keyword` join table: `content_id` + `keyword_id` (FK to `mktg_keyword`) — no separate page needed; secondary keywords shown as tags in Content Detail Drawer.

**Division E video brief link:** In Content Detail Drawer (for content_type = `VIDEO_SCRIPT` or INFOGRAPHIC), a [Send to Video Team ↗] button appears. Clicking opens a simple modal: "Submit this content brief to Division E?" → POST creates a record in Division E's production system (implementation: creates a `video_content_brief` row referencing `mktg_content.id`). Status tracked as `VIDEO_BRIEF_SENT` in change log.

**Bulk actions on content list:**
- Bulk archive: [Bulk Actions ▼] → Archive selected (Content Strategist + Manager)
- Bulk reassign author: Manager only → opens author picker modal
- Bulk update target date: Content Strategist + Manager → date picker applies to all selected items

**Overdue content:** Past `target_publish_date + content_overdue_alert_days` (from `mktg_config`) and not PUBLISHED/ARCHIVED → red "Overdue N days" badge in Target Date column. [Create content] button always visible in overdue empty state.

**Keyword removal:** Removing a keyword sets `mktg_keyword.is_tracking = false` (soft delete, not hard delete). Historical position data retained in `mktg_keyword_position_history`. Hard delete only via database admin (not exposed in UI).

**SEO domain metric data source note:** Domain Authority and Referring Domains are sourced from the third-party SEO API. EduForge does not contract with Moz/Ahrefs directly; DataForSEO resells this data at lower cost. API credentials stored in Django settings (`DATAFORSEO_API_KEY`). DA/referring domains values update weekly; if API call fails, last known values are retained and shown with "stale" tooltip.
