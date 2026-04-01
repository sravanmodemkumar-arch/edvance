# L-05 — Social Media Hub

**Route:** `GET /marketing/social/`
**Method:** Django `TemplateView` + HTMX part-loads
**Primary role:** Social Media Manager (#66)
**Also sees:** Marketing Manager (#64) — full access; Marketing Analyst (#98) — read-only analytics; Performance Marketing Exec (#67) — no access

---

## Purpose

Cross-platform social media operations centre for EduForge's external channels. The Social Media Manager uses this daily to schedule posts, monitor engagement, review platform-level analytics, and surface top-performing content for repurposing. Analytics data is imported nightly from YouTube Analytics, Instagram Insights, and Twitter/X API. The platform is not a publishing API bridge — posts are scheduled here for planning, then published manually or via a lightweight webhook to buffer integrations. Metrics are read-back nightly from each platform into `mktg_social_post`.

---

## Data Sources

| Section | Source | Cache TTL |
|---|---|---|
| Platform KPI strips | `mktg_social_post` aggregate by platform for selected period | 30 min |
| Engagement trend chart | `mktg_social_post` grouped by week for last 12 weeks | 60 min |
| Top posts table | `mktg_social_post` WHERE status='POSTED' ORDER BY (likes + comments + shares) DESC | 30 min |
| Post scheduler | `mktg_social_post` WHERE scheduled_at > now() ORDER BY scheduled_at | 5 min |
| Platform-specific deep metrics | `mktg_social_platform_metric` (subscriber count, follower count, watch time) — nightly import | 60 min |
| Comment feed | External platform API calls at page-load time (not cached); limited to last 50 comments | Live |

`?nocache=true` available to Manager (#64) and Social Manager (#66).

---

## URL Parameters

| Param | Values | Default | Effect |
|---|---|---|---|
| `?platform` | `youtube`, `instagram`, `twitter`, `all` | `all` | Active platform tab |
| `?period` | `7d`, `30d`, `90d` | `30d` | Analytics aggregation window |
| `?domain` | exam domain enum | `all` | Filter posts by exam domain |
| `?status` | `scheduled`, `posted`, `failed`, `draft` | `all` | Filter scheduler by post status |

---

## HTMX Part-Load Routes

| Route | Component | Trigger | Target ID |
|---|---|---|---|
| `htmx/l/social-kpi/{platform}/` | Platform KPI strip | Tab change + period change | `#l-social-kpi` |
| `htmx/l/social-trend/{platform}/` | Engagement trend chart | Tab change + period change | `#l-social-trend` |
| `htmx/l/social-top-posts/{platform}/` | Top posts table | Tab change + period change | `#l-social-top-posts` |
| `htmx/l/social-scheduler/` | Upcoming posts queue | Page load; auto-refresh 5 min | `#l-social-scheduler` |
| `htmx/l/social-comments/{platform}/` | Comment feed | Tab change | `#l-social-comments` |

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────────────┐
│  SOCIAL MEDIA HUB                                   [+ Schedule Post]  │
├─────────────────────────────────────────────────────────────────────────┤
│  [All Platforms]  [YouTube]  [Instagram]  [Twitter/X]                   │
│                                                    Period: [30 Days ▼]  │
├─────────────────────────────────────────────────────────────────────────┤
│  PLATFORM KPI STRIP (5 tiles)                                           │
├─────────────────────────────────────────────────────────────────────────┤
│  ENGAGEMENT TREND CHART (line, 12 weeks)    │  TOP POSTS TABLE          │
│                                             │                           │
├─────────────────────────────────────────────┴───────────────────────────┤
│  POST SCHEDULER (upcoming + recent)                                     │
├─────────────────────────────────────────────────────────────────────────┤
│  COMMENT FEED (live)                                                    │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Platform Tabs

| Tab | Data Source |
|---|---|
| All Platforms | Aggregate across YouTube + Instagram + Twitter |
| YouTube | `mktg_social_post` WHERE platform='YOUTUBE' + `mktg_social_platform_metric` WHERE platform='YOUTUBE' |
| Instagram | `mktg_social_post` WHERE platform='INSTAGRAM' + platform metrics |
| Twitter/X | `mktg_social_post` WHERE platform='TWITTER' + platform metrics |

---

## Platform KPI Strip (5 Tiles)

**All Platforms view:**
```
┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 14           │ │ 42.8K        │ │ 28.4K        │ │ 3.8%         │ │ +614         │
│ Posts        │ │ Total Reach  │ │ Impressions  │ │ Avg Eng.     │ │ Followers/   │
│ Published    │ │ (30 days)    │ │ (30 days)    │ │ Rate         │ │ Subs Gained  │
│              │ │              │ │              │ │              │ │ (30 days)    │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘
```

**YouTube-specific KPIs:**
- Views (30d) · Watch Time (hours, 30d) · Subscribers gained · Avg view duration · Top video title

**Instagram-specific KPIs:**
- Reach · Impressions · Engagement Rate · Follower gain · Stories views

**Twitter-specific KPIs:**
- Impressions · Engagements · Engagement Rate · Profile visits · Follower gain

Deltas shown vs previous period. Green = positive change.

**`mktg_social_platform_metric` table:**

| Column | Type | Notes |
|---|---|---|
| id | bigserial | PK |
| platform | varchar(20) | NOT NULL |
| metric_date | date | NOT NULL |
| followers | int | Total follower / subscriber count at end of day |
| follower_delta | int | Change from previous day |
| total_views | bigint | YouTube only |
| watch_time_minutes | bigint | YouTube only |
| avg_view_duration_sec | int | YouTube only |
| reach | bigint | Instagram only |
| story_views | bigint | Instagram only |
| profile_visits | int | Twitter / Instagram |
| UNIQUE | (platform, metric_date) | |

---

## Engagement Trend Chart

Line chart — 12 weeks of weekly engagement metrics for selected platform.

**Engagement = likes + comments + shares (or equivalent per platform)**

- X-axis: ISO week labels
- Y-axis: engagement count
- Secondary Y-axis: post count per week (bar chart overlay)
- Reference line: 12-week average engagement
- Hover: week · total engagement · posts published · top post title

---

## Top Posts Table

Top 10 posts ranked by total engagement for selected platform and period.

| Column | Description |
|---|---|
| Post Preview | Thumbnail (images) or title (YouTube). Click → opens post in new tab |
| Platform | Badge icon |
| Domain | Exam domain badge |
| Published | Relative date |
| Reach | Unique users reached |
| Impressions | Total impressions |
| Likes | |
| Comments | |
| Shares | |
| Engagement Rate | (likes + comments + shares) / reach × 100 |
| Actions | [Repurpose as Content Brief] [View Details] |

**[Repurpose as Content Brief]:** Opens Content Brief Drawer (L-04) pre-filled with the post topic and exam domain. Allows high-performing social content to be expanded into full blog posts or guides.

---

## Post Scheduler

Chronological list of upcoming scheduled posts and recent posts (last 7 days).

```
┌──────────────────────────────────────────────────────────────────────────┐
│  UPCOMING POSTS                                          [+ Schedule]    │
│                                                                          │
│  Thu 22 Mar  10:00  Instagram  ● SSC CGL motivational post (SCHEDULED)  │
│  Thu 22 Mar  15:00  Twitter    ● RRB NTPC exam date reminder (SCHEDULED) │
│  Sat 24 Mar  10:00  YouTube    ● Short: 5 mins on Reasoning (SCHEDULED)  │
│                                                                          │
│  RECENT POSTS (last 7 days)                                              │
│  Mon 18 Mar  Instagram   ✓ Board exam tips post  Reach: 3.2K  Eng: 4.1% │
│  Sun 17 Mar  YouTube     ✓ SSC video            Views: 1,800             │
│  ✗ Fri 15 Mar Twitter   ✗ Post failed (API error)  [Retry]              │
└──────────────────────────────────────────────────────────────────────────┘
```

- SCHEDULED: blue dot; POSTED: green tick; FAILED: red X with [Retry]
- [Retry]: re-queues the failed post for immediate send via platform API
- Click any scheduled post → opens Post Detail Drawer
- FAILED posts send alert to Social Manager + Marketing Manager via Notification Manager

---

## Schedule Post Drawer

Opens from [+ Schedule Post] button.

```
┌──────────────────────────────────────────────────────────────────┐
│  Schedule Post                                       [Close ×]   │
├──────────────────────────────────────────────────────────────────┤
│  Platform*   [☐ YouTube]  [☑ Instagram]  [☐ Twitter/X]           │
│              (can select multiple for cross-posting)             │
│                                                                  │
│  Exam domain  [SSC                                          ▼]   │
│                                                                  │
│  Caption / Post text*                                            │
│  [✏ Write your post here...                                  ]   │
│  280 chars remaining (Twitter limit applies if Twitter selected) │
│                                                                  │
│  Media (images / video)                                          │
│  [🖼 Upload media]   (max 4 images or 1 video; R2 upload)        │
│  Supported: JPG, PNG, MP4, MOV — max 200MB per file             │
│                                                                  │
│  Schedule date & time*                                           │
│  [22 Mar 2026   ] [10:00 IST  ]                                  │
│                                                                  │
│  [Cancel]                              [Schedule Post]           │
└──────────────────────────────────────────────────────────────────┘
```

**Validation:**
- Platform: at least one required
- Caption: required; Twitter cap at 280 chars if Twitter is selected
- Schedule date: must be in the future (≥ 15 minutes from now)
- Media: optional; max file size 200MB; formats validated server-side

POST to `/marketing/social/schedule/`. Creates one `mktg_social_post` row per selected platform. For cross-posts, each platform gets its own row with same content; Platform-specific constraints (Twitter char limit) are applied per-platform.

**Edit Post:** Available for SCHEDULED posts. Opens same drawer pre-filled. PUT to `/marketing/social/{id}/edit/`. Cannot edit POSTED posts — [Repurpose] available instead.

**Cancel Post:** PATCH to `/marketing/social/{id}/cancel/` → sets status = `CANCELLED`. Only for SCHEDULED posts.

---

## Comment Feed

Live comment feed from the last 50 comments across active posts (pulled at page load from platform APIs).

> Note: EduForge does not store comment text in the database — this is a pass-through read from platform APIs. No user data is persisted.

```
┌──────────────────────────────────────────────────────────────────┐
│  COMMENT FEED (last 50 comments — not cached)                    │
│  Platform: [All ▼]  [Refresh]                                    │
│                                                                  │
│  @student_rakesh · YouTube · 2h ago                              │
│  "Great explanation of the ratio topic! When is the next         │
│   Maths video coming?"                                           │
│  Post: SSC CGL Maths Tricks (18 Mar)         [Reply ↗]           │
│  ─────────────────────────────────────────────────────           │
│  @coaching_owner_ap · Instagram · 4h ago                         │
│  "Do you have resources for CLAT preparation too?"               │
│  Post: EduForge Platform intro (17 Mar)      [Reply ↗]           │
│  ─────────────────────────────────────────────────────           │
│  @ravi_ssc · Twitter · 5h ago                                    │
│  "Is the SSC mock test series available now?"                    │
│  Post: Exam series announcement (17 Mar)     [Reply ↗]           │
└──────────────────────────────────────────────────────────────────┘
```

- [Reply ↗] opens the actual post on the platform in a new tab (Social Manager replies directly on the platform)
- No in-app reply — this avoids the complexity of OAuth token management for posting replies
- [Refresh] re-fetches comments via platform API

---

## Role-Based UI

| Element | 64 Manager | 66 Social Manager | 98 Analyst |
|---|---|---|---|
| View all analytics | Yes | Yes | Yes (read) |
| Schedule post | Yes | Yes | No |
| Edit / Cancel scheduled post | Yes | Yes | No |
| Retry failed post | Yes | Yes | No |
| Repurpose post as content brief | Yes | Yes | No |
| View comment feed | Yes | Yes | No |
| Budget edit (social ad spend) | Manager only | No | No |

---

## Empty States

| Condition | Message |
|---|---|
| No posts scheduled | "No posts scheduled. [+ Schedule Post →]" |
| No posts published in period | "No posts published in the selected period." |
| No social data imported | "Social analytics will appear after the first nightly import." |
| Comment feed empty | "No recent comments found." |

---

## Toasts, Loaders & Error States

> Full reference: [L-00 Global Spec](l-00-global-spec.md).

Toasts: post scheduled, cancelled, edited, retry queued/succeeded/failed, cross-post created — see L-00 §2.

**Post FAILED notification:** Immediate email + in-app to Social Manager (#66) + Marketing Manager (#64). See L-00 §7.

**Skeleton states:** Platform KPI strip tiles, engagement trend chart, top posts table — all shimmer while loading.

**Platform API rate limiting:** If comment feed API is rate-limited, the section shows: "Rate limited — try again in {N} minutes." No auto-retry for comment feed (user must manually [Refresh]). All other metrics come from nightly imports (not real-time API), so rate limiting only affects the comment feed.

---

## Missing Spec Closes (Audit)

**LinkedIn tab:**
LinkedIn is in the `mktg_social_post.platform` enum but was missing from the tab spec.

**Updated Platform Tabs:** All · YouTube · Instagram · Twitter/X · LinkedIn

LinkedIn-specific KPIs (LinkedIn tab view):
- Followers · Post impressions · Engagements · Engagement rate · Follower gain (30d)
- Note: LinkedIn Insights API requires the EduForge LinkedIn Company Page to be linked. Credentials in `LINKEDIN_ACCESS_TOKEN` Django setting.

LinkedIn posts are institutional (B2B) — target audience is school principals, college HODs, coaching owners. Post character limit: 3,000 chars. No media size restriction beyond LinkedIn API limits (10MB images, 5GB video).

**Platform-specific character limits enforced in Schedule Post drawer:**
- Twitter/X: 280 chars (hard limit; counter shows "280/280" when at limit; submit blocked)
- Instagram: 2,200 chars (soft warning at 2,000; no hard block)
- LinkedIn: 3,000 chars (soft warning at 2,800)
- YouTube: no char limit on post text (YouTube Shorts description); 5,000 chars for community posts
- Character counter updates live on every keypress.

**Cross-posting row structure:** When a post is scheduled to 3 platforms simultaneously, 3 separate `mktg_social_post` rows are created (one per platform), each with identical `content_text` and `media_r2_keys`. A `group_id` UUID column is added to `mktg_social_post` to link them for display purposes (show as one card in scheduler with platform badges). If one platform's post fails, the others are not affected.

**Post approval workflow:** Social Media Manager (#66) can schedule posts directly without Manager approval. There is no approval gate for social posts. (Marketing Manager can edit/cancel any post at any time.)

**Schedule conflict:** If two posts are scheduled to the same platform within 30 minutes of each other, a WARNING dialog: "Another post is scheduled {N} minutes before this. Proceed?" — not a hard block.

**Retry mechanism:** Failed posts are retried automatically 3 times with exponential backoff: 5 min → 15 min → 45 min. After 3 failures, status = `FAILED` and notification sent. [Retry] button re-queues as a fresh attempt (reset retry counter).

**Figma assets in social post:** Figma files stored in brand library (L-06) are accessed via Figma export API, not stored in R2. Social Manager selects "Import from Brand Library" in media upload → sees brand assets filtered to `SOCIAL_TEMPLATE` type → Figma files trigger a server-side Figma API export (PNG/JPG) → stored temporarily in R2 → used in post. Not cached permanently (temporary R2 key with 7-day TTL).
