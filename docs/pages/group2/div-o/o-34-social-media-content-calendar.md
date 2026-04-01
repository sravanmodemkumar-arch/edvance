# O-34 — Social Media Content Calendar

> **URL:** `/group/marketing/content/social-calendar/`
> **File:** `o-34-social-media-content-calendar.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Campaign Content Coordinator (Role 131, G2) — primary scheduler

---

## 1. Purpose

The Social Media Content Calendar is the group's centralised planning, scheduling, approval, and tracking system for all social media posts across Instagram, Facebook, YouTube, WhatsApp Status/Channels, Twitter/X, and LinkedIn — covering every branch, every platform, and every content category from topper photos to festival greetings. In the Indian education market, social media is now the single largest influence on parent decision-making: a Hyderabad parent choosing between Narayana and Sri Chaitanya will check Instagram before visiting either campus. WhatsApp Channels have emerged as a massive reach amplifier in tier-2/3 cities where parents may not use Instagram but are on WhatsApp daily. A group that posts consistently, showcases toppers within hours of results, publishes festival greetings on every major Indian festival, and runs exam-date reminder posts converts followers into walk-in enquiries.

The problems this page solves:

1. **Posting inconsistency:** Without a calendar, the social media team posts 5 times in one week during results season and then goes silent for 3 weeks. The algorithm punishes inconsistency — reach drops, followers unfollow, and the competitor's page fills the gap. A calendar enforces minimum 4 posts/week across platforms year-round.

2. **Platform-specific formatting chaos:** Instagram requires 1080×1080 square or 1080×1350 portrait images; Facebook tolerates 1200×630 landscape; YouTube needs 1920×1080 thumbnails; LinkedIn works best with text-heavy professional posts. Without a system, the same 1080×1080 image is posted everywhere — looking cropped on Facebook, unprofessional on LinkedIn, and wrong-ratio on YouTube community posts.

3. **Festival and exam date misses:** India has 30+ major festivals across religions and regions (Diwali, Sankranti/Pongal, Eid, Christmas, Onam, Ugadi, Ganesh Chaturthi, Holi, Independence Day, Republic Day, Teachers' Day, Children's Day). Missing a festival greeting post — especially a regional one like Bathukamma in Telangana or Bonalu — signals cultural disconnect to local parents. Similarly, exam date announcement posts (CBSE datesheet, JEE Main registration, NEET application deadline) are high-engagement content that must be posted the same day announcements happen.

4. **Approval delays:** A topper card post with a student's photo, marks, and branch name requires verification before publishing. A festival greeting with the Chairman's message needs CEO approval. Without a workflow, the Content Coordinator creates the post, WhatsApps it to the CEO, waits 3 days for approval, and the moment passes.

5. **Engagement tracking gap:** Which post type gets the most engagement — Topper Card, Campus Video, Festival Greeting, or Exam Reminder? Which platform drives the most profile visits → website clicks → enquiry form fills? Without tracking, the team produces content blindly.

**Important architectural note:** The platform does NOT publish directly to any social media platform. It manages the planning, content creation, approval workflow, and scheduling. The Social Media Manager (role 118, G0) publishes in native tools (Meta Business Suite, YouTube Studio, WhatsApp Business, LinkedIn) and logs the published URL back into the platform. This is a deliberate V1 decision — direct API integration with Meta/Google/LinkedIn is V2 scope.

**Scale:** 60–150 posts per month per group · 4–6 active platforms · 30+ festival posts per year · 3–5 content pieces per day during peak season · 500–5,000 total posts per season · 6–12 content categories · Manual engagement data entry for top 20% posts

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Campaign Content Coordinator | 131 | G2 | Full CRUD — create posts, schedule, manage calendar, upload media, log published URLs | Primary calendar owner |
| Group Admissions Campaign Manager | 119 | G3 | Read + Approve + Create — approve posts, create campaign-linked posts, override schedule | Approval authority |
| Group Topper Relations Manager | 120 | G3 | Read + Create — create topper-related posts, link to O-28/O-30 | Topper content contributor |
| Group Admission Telecaller Executive | 130 | G3 | Read — view published posts for talking points during calls | Reference only |
| Group Admission Data Analyst | 132 | G1 | Read + Export — post performance analytics, engagement reports | MIS and reporting |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — override any post, approve sensitive content (fee, result claims) | Strategic oversight |
| Social Media Manager (reference) | 118 | G0 | No platform login — publishes externally, logs published URL back via link shared by 131 | External executor |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Post creation: role 131, 119, 120, or G4+. Post approval: role 119 or G4+. Engagement logging: role 131 or 119. Performance export: G1+. Delete published: G4+ only.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Content Management  ›  Social Media Content Calendar
```

### 3.2 Page Header
```
Social Media Content Calendar                      [+ New Post]  [Festival Calendar]  [Templates]  [Export]
Content Coordinator — Priya Reddy
Sunrise Education Group · March 2026 · 24 posts scheduled · 18 published · 6 pending approval
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Posts This Month | Integer | COUNT(posts) WHERE month = current AND status IN ('scheduled','published') | Static blue | `#kpi-monthly` |
| 2 | Published | Integer | COUNT WHERE status = 'published' this month | Static green | `#kpi-published` |
| 3 | Pending Approval | Integer | COUNT WHERE status = 'pending_approval' | Amber > 3, Red > 7 | `#kpi-pending` |
| 4 | Avg Engagement Rate | Percentage | AVG((likes + comments + shares) / reach × 100) this month | Green ≥ 3%, Amber 1–3%, Red < 1% | `#kpi-engagement` |
| 5 | Top Platform | Text + number | Platform with highest engagement this month | Static blue | `#kpi-top-platform` |
| 6 | Upcoming (7d) | Integer | COUNT WHERE scheduled_date within 7 days AND status = 'scheduled' | Static blue | `#kpi-upcoming` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/social-calendar/kpis/"` → `hx-trigger="load"`

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Calendar View** — Monthly calendar with posts plotted on dates
2. **List View** — Tabular list of all posts with status and details
3. **Publish Queue** — Posts approved and ready to publish, ordered by schedule
4. **Content Library** — Reusable templates, past posts, asset repository
5. **Engagement Dashboard** — Platform-wise engagement analytics

### 5.2 Tab 1: Calendar View

Interactive monthly calendar showing scheduled and published posts per date.

**Calendar cell layout:**
```
┌─ Mon 16 Mar ────────────────────┐
│  🟢 [IG] Topper Card — Sai K.   │
│  🟡 [FB] Campus Video — Hyd     │
│  🔵 [LI] Achievement Post       │
│  ─────────────────────────       │
│  🎉 Holi (Festival)             │
└─────────────────────────────────┘
```

**Colour coding:**
- 🟢 Green border = Published
- 🟡 Amber border = Scheduled (approved, awaiting publish time)
- 🔴 Red border = Pending approval
- ⚪ Grey border = Draft
- 🎉 Festival/exam date markers (from festival calendar)

**Platform icons:** IG = Instagram, FB = Facebook, YT = YouTube, WA = WhatsApp, LI = LinkedIn, X = X/Twitter

**Interactions:**
- Click post → opens detail drawer
- Click empty date → opens `new-post` modal with date pre-filled
- Drag-and-drop post to reschedule (within same week)
- Month navigation: ◂ Previous | Current Month | Next ▸

**Festival & exam date overlay:** Pre-loaded with Indian festival dates and major exam dates for the academic year. Displayed as background markers on calendar cells. Source: configurable festival master (Group Settings) + exam date master (linked from academic calendar).

**Indian festival calendar (pre-loaded):**

| Month | Festivals / Key Dates |
|---|---|
| January | Republic Day (26), Sankranti/Pongal (14-15), Lohri (13) |
| February | Maha Shivaratri, Valentine's Day (optional — some groups skip) |
| March | Holi, Ugadi/Gudi Padwa, Women's Day (8) |
| April | Ram Navami, Ambedkar Jayanti (14), Good Friday, Easter |
| May | May Day (1), Buddha Purnima, Mother's Day |
| June | Eid-ul-Fitr (date varies), Rath Yatra, World Environment Day (5) |
| July | Guru Purnima, Eid-ul-Adha (date varies), Bonalu (Telangana) |
| August | Independence Day (15), Raksha Bandhan, Krishna Janmashtami, Bathukamma start (Telangana) |
| September | Ganesh Chaturthi, Teachers' Day (5), Onam |
| October | Gandhi Jayanti (2), Navratri, Dussehra, Diwali (date varies) |
| November | Children's Day (14), Guru Nanak Jayanti, Kartik Purnima |
| December | Christmas (25), New Year prep |

**Exam date markers (examples):**
- CBSE Board datesheet release, JEE Main registration deadline, NEET application date, TSBIE exam dates, AP Board exam dates, CUET registration, CLAT exam date

### 5.3 Tab 2: List View

**Filter bar:** Month · Platform (Instagram/Facebook/YouTube/WhatsApp/LinkedIn/X) · Content type · Status (Draft/Pending Approval/Approved/Scheduled/Published/Rejected) · Created by · Date range · Branch

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | — |
| Scheduled Date | Date + Time | Yes | Publish date/time |
| Thumbnail | Image (50×50) | No | Post image/video frame preview |
| Caption | Text (truncated 80 chars) | No | Post caption text |
| Content Type | Badge | Yes | Results / Events / Campus Life / Testimonials / Festivals / Motivational / Announcements / Recruitment / Offers / Competitions / Exam Reminder / Infographic |
| Platform(s) | Badge set | No | IG · FB · YT · WA · LI · X — shows which platforms this post targets |
| Format | Badge | Yes | Image / Carousel / Video / Reel / Story / Text Post |
| Created By | Text | Yes | Content Coordinator / Topper Relations Manager |
| Approval | Badge | Yes | Draft (grey) / Pending (amber) / Approved (green) / Rejected (red) |
| Status | Badge | Yes | Draft / Pending Approval / Scheduled / Published / Failed / Archived |
| Engagement | Text | No | Quick stats: ❤ [likes] 💬 [comments] 🔄 [shares] (published posts only) |
| Actions | Buttons | No | [View] [Edit] [Approve] [Publish Now] |

**Default sort:** Scheduled Date DESC
**Pagination:** Server-side · 25/page

### 5.4 Tab 3: Publish Queue

Ordered list of approved posts ready to publish, sorted by scheduled time.

**Layout:** Card-based timeline view

```
┌─ TODAY ──────────────────────────────────────────────────────────┐
│                                                                   │
│  10:00 AM  [IG] Topper Card — Sai Krishna (JEE AIR 342)         │
│            1080×1080 · Approved by Ramesh · [Publish Now] [Edit]  │
│                                                                   │
│  12:30 PM  [FB] Campus Video — Hyderabad Branch Tour             │
│            1920×1080 MP4 · Approved by Ramesh · [Publish Now]     │
│                                                                   │
│  05:00 PM  [IG+FB] Festival Greeting — Ugadi                     │
│            1080×1350 · CEO quote included · Approved G4           │
│            [Publish Now] [Reschedule]                             │
│                                                                   │
├─ TOMORROW ───────────────────────────────────────────────────────┤
│  09:00 AM  [LI] Achievement Post — Group Results Summary         │
│            Text + infographic · Pending approval                  │
│                                                                   │
└──────────────────────────────────────────────────────────────────┘
```

**Publishing behaviour:** The system does NOT auto-publish to social media platforms (that requires API integration with Meta/Google/LinkedIn which is out of scope for V1). Instead, the "Publish Now" action:
1. Marks the post as "Ready to Publish" with all assets downloadable
2. Copies caption text to clipboard
3. Opens platform-specific download (correctly sized image/video per platform)
4. Content Coordinator manually posts on the platform
5. After posting, logs the live URL and marks as "Published"

**V2 future scope:** Direct API integration with Meta Business Suite (IG/FB), YouTube Data API, LinkedIn Marketing API for auto-publishing.

### 5.5 Tab 4: Content Library

Reusable templates and past successful posts for reference and re-use.

**Sub-tabs:** Templates · Past Posts · Asset Library

#### 5.5.1 Templates

Pre-designed post templates by content type:

| Template | Platform | Format | Dimensions | Elements |
|---|---|---|---|---|
| Topper Card | IG, FB | Image | 1080×1080 | Student photo, name, marks/rank, branch, group logo, background gradient |
| Topper Card (Portrait) | IG | Image | 1080×1350 | Same as above, more vertical space for multiple toppers |
| Festival Greeting | IG, FB | Image | 1080×1080 | Festival art, group logo, Chairman message, regional language text |
| Exam Reminder | IG, FB, X | Image | 1080×1080 | Exam name, date, important links, "All the best" message |
| Campus Video Thumbnail | YT | Image | 1920×1080 | Branch photo, play button overlay, title text |
| Achievement Infographic | LI, FB | Image | 1200×630 | Stats layout — students appeared, passed, toppers, ranks |
| Admission Drive | IG, FB | Carousel | 1080×1080 ×5 | Slide 1: offer, Slides 2-4: features/facilities, Slide 5: CTA with phone |
| Testimonial Quote | IG, FB | Image | 1080×1080 | Student/parent photo, quote text, name, branch |

**Template action:** Select → Auto-populates `new-post` modal with format, dimensions, and element structure. Content Coordinator fills in specifics and uploads designed asset.

#### 5.5.2 Past Posts

Archive of all published posts with engagement data. Sortable by engagement rate to surface top-performing content for re-use or adaptation.

#### 5.5.3 Asset Library

Shared images, videos, logos, backgrounds, fonts linked from O-03 Marketing Material Library. Quick search by category.

### 5.6 Tab 5: Engagement Dashboard

Platform-wise engagement analytics for published posts.

#### 5.6.1 Platform Summary

| Platform | Followers/Subscribers | Posts (Month) | Avg Reach | Avg Engagement Rate | Best Post Type | Profile Visits → Website Clicks |
|---|---|---|---|---|---|---|
| Instagram | 45,200 | 12 | 8,400 | 3.2% | Results (Topper Card) | 1,200 → 340 |
| Facebook | 32,800 | 10 | 12,600 | 1.8% | Campus Life (Video) | 2,400 → 680 |
| YouTube | 8,500 | 4 | 5,200 | 4.1% | Testimonials (Video) | — → 420 |
| WhatsApp Channel | 28,400 | 8 | 22,000 | 5.8% | Announcements | — → — |
| LinkedIn | 4,200 | 6 | 1,800 | 2.4% | Recruitment | 380 → 120 |
| X (Twitter) | 2,100 | 8 | 900 | 1.2% | Exam Reminder | 140 → 45 |

#### 5.6.2 Content Type Performance

| Content Type | Posts | Avg Likes | Avg Comments | Avg Shares | Avg Engagement Rate | Best Platform |
|---|---|---|---|---|---|---|
| Topper Card | 28 | 320 | 45 | 85 | 4.8% | Instagram |
| Event Photo | 22 | 180 | 22 | 30 | 2.4% | Facebook |
| Campus Video | 8 | 420 | 65 | 120 | 5.2% | YouTube |
| Festival Greeting | 18 | 250 | 15 | 55 | 2.1% | Instagram |
| Achievement Post | 12 | 140 | 28 | 42 | 3.1% | LinkedIn |
| Exam Reminder | 15 | 85 | 12 | 65 | 1.8% | X |
| Admission Drive | 10 | 95 | 18 | 22 | 1.5% | Facebook |
| Testimonial | 14 | 280 | 38 | 72 | 3.8% | Instagram |

**Insight callout:** "Topper Cards and Campus Videos generate the highest engagement. Prioritise these during results season (May-June) and admission season (Jan-April)."

#### 5.6.3 Best Posting Times (Heatmap)

Heatmap showing engagement rate by day-of-week × time-of-day based on published post data.

| Time \ Day | Mon | Tue | Wed | Thu | Fri | Sat | Sun |
|---|---|---|---|---|---|---|---|
| 8–10 AM | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 |
| 10–12 PM | 🟡 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 |
| 12–2 PM | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🟡 |
| 2–4 PM | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 |
| 4–6 PM | 🟡 | 🟡 | 🟡 | 🟡 | 🟢 | 🟡 | 🟡 |
| 6–8 PM | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 |
| 8–10 PM | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟢 |

Legend: 🟢 High (≥3%) · 🟡 Medium (1–3%) · 🔴 Low (<1%)

**Indian context insight:** Evening 6–8 PM and post-dinner 8–10 PM are peak engagement windows — parents browse social media after work/dinner. Sunday mornings (8–10 AM) are strong for family-oriented content. Lunch hours show low engagement — parents are working, students are in school.

---

## 6. Drawers & Modals

### 6.1 Modal: `new-post` (720px)

- **Title:** "Create Social Media Post"
- **Fields:**
  - **Content details:**
    - Content type (dropdown, required): Results / Events / Campus Life / Testimonials / Festivals / Motivational / Announcements / Recruitment / Offers / Competitions / Exam Reminder / Infographic / Poll
    - Caption (textarea, required — supports #hashtags and @mentions; character count for each platform: IG 2200, FB unlimited, X 280, LI 3000)
    - Alt text (textarea, optional — for accessibility)
    - Hashtags (text — comma-separated; auto-suggest from group's standard hashtag set)
    - Call to action (text, optional — "Link in bio", "Call 9876543210", "Visit sunrise.edu.in")
  - **Media (per platform tab):**
    - Instagram tab: Upload image/carousel/reel (1080×1080, 1080×1350, or 1080×1920)
    - Facebook tab: Upload image/video (1200×630, 1920×1080)
    - YouTube tab: Upload video (1920×1080) + thumbnail + title + description
    - WhatsApp tab: Upload image/video (1080×1920 for Status, any for Channel post) + text
    - LinkedIn tab: Upload image/document (1200×630) + text
    - X tab: Upload image (1600×900) + text (280 chars)
    - **"Apply to all" toggle:** Use same asset for all platforms (auto-crop per platform specs)
  - **Scheduling:**
    - Scheduled date (date picker, required)
    - Scheduled time (time picker, required — suggest optimal time based on engagement heatmap)
    - Platform(s) (multi-select, required): Instagram / Facebook / YouTube / WhatsApp / LinkedIn / X
    - Repeat (dropdown): One-time / Weekly / Monthly (for recurring content like "Monday Motivation" series)
  - **Linking:**
    - Related toppers (multi-select from O-28 — auto-pulls photo and stats)
    - Related event (dropdown from O-29 — auto-populates event details)
    - Related press release (dropdown from O-32)
    - Related campaign (dropdown from O-08)
  - **Approval settings:**
    - Requires G4 approval (toggle — auto-ON for festival/political/sensitive content)
    - Notes to approver (textarea)
- **Buttons:** Cancel · Save as Draft · Submit for Approval
- **Access:** Role 131, 119, 120

### 6.2 Modal: `approve-post` (640px)

- **Title:** "Review Post — [Content Type] — [Scheduled Date]"
- **Preview:** Rendered post preview for each target platform (tabbed: IG / FB / YT / LI / X)
- **Checklist (for approver):**
  - ☐ Caption verified — no spelling/grammar errors
  - ☐ Student data matches O-28 (if topper content)
  - ☐ No ASCI-violating claims
  - ☐ Brand guidelines followed (logo, colours, fonts)
  - ☐ Correct platform dimensions
  - ☐ Hashtags appropriate and on-brand
  - ☐ Festival/cultural content respectful and accurate
- **Actions:** Approve ✅ / Request Changes (with comments) / Reject ❌ (with reason)
- **Access:** Role 119 (standard posts), G4/G5 (flagged/sensitive posts)

### 6.3 Modal: `publish-confirm` (480px)

- **Title:** "Publish — [Content Type] — [Platform]"
- **Content:** Final preview + caption (copyable) + downloadable assets
- **Platform-specific download:**
  - Instagram: 1080×1080 JPEG + caption text
  - Facebook: 1200×630 JPEG + caption text
  - YouTube: 1920×1080 MP4 + thumbnail + title + description
  - WhatsApp: 1080×1920 JPEG/MP4 + message text (for Status) or channel post text
  - LinkedIn: 1200×630 JPEG + post text
  - X: 1600×900 JPEG + tweet text (280 chars)
- **After posting externally:**
  - Live URL (text — paste the actual post URL from IG/FB/YT/WA/LI/X)
  - Post ID (auto-extracted from URL where possible)
- **Buttons:** Copy Caption · Download Assets · Mark as Published
- **Access:** Role 131 or G3+

### 6.4 Drawer: `post-detail` (720px, right-slide)

- **Tabs:** Preview · Engagement · Platforms · History
- **Preview tab:** Full rendered post with image, caption, hashtags, CTA. Platform selector to see how it looks on each platform.
- **Engagement tab (published posts only):**
  - Per platform: likes, comments, shares, saves, reach, impressions, engagement rate
  - Trend: engagement over first 24h / 48h / 7d (if tracked manually)
  - Link clicks / Profile visits (if available)
- **Platforms tab:** Status per platform — Published (with live URL) / Scheduled / Not applicable. Asset download per platform.
- **History tab:** Audit trail — created, edited, submitted, approved/rejected, published, with timestamps and actors.
- **Footer:** [Edit] [Approve] [Publish Now] [Reschedule] [Duplicate] [Archive]

### 6.5 Modal: `log-engagement` (480px)

- **Title:** "Log Engagement — [Post on Platform]"
- **Description:** "Enter engagement metrics from [Platform] for this post."
- **Fields (per platform):**
  - Likes / Reactions (integer)
  - Comments (integer)
  - Shares / Retweets (integer)
  - Saves / Bookmarks (integer, IG/FB)
  - Reach (integer — from platform insights)
  - Impressions (integer)
  - Link clicks (integer, optional)
  - Profile visits (integer, optional)
  - Video views (integer, optional — for video/reel content)
  - Watch time (minutes, optional — YouTube)
- **Buttons:** Cancel · Save Engagement
- **Note:** Engagement data is entered manually from platform native analytics (V1). V2 will auto-pull via platform APIs.
- **Access:** Role 131, 119, or G4+

### 6.6 Modal: `festival-calendar` (640px)

- **Title:** "Festival & Key Date Calendar — [Academic Year]"
- **Content:** Full list of pre-loaded festivals and exam dates for the year, with:
  - Date
  - Festival/Event name
  - Type (Hindu / Muslim / Christian / Sikh / National / Regional / Exam / Other)
  - Region (National / Telangana / AP / Karnataka / Tamil Nadu / Pan-India)
  - Post required? (toggle — Content Coordinator marks which dates need social media posts)
  - Post status (Not Created / Draft / Scheduled / Published)
  - Template suggestion (auto-suggests matching template)
- **Actions:** [Create Post for Date] — opens `new-post` modal with festival date pre-filled
- **Access:** Role 131 (edit), G1+ (read)

---

## 7. Charts

### 7.1 Engagement by Content Type (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Average Engagement Rate by Content Type" |
| Data | AVG engagement rate per content type (min 3 posts) |
| Colour | Green ≥ 3%, Amber 1–3%, Red < 1% per bar |
| Tooltip | "[Content Type]: [X]% avg engagement ([N] posts)" |
| API | `GET /api/v1/group/{id}/marketing/social-calendar/analytics/by-content-type/` |

### 7.2 Posts Published by Platform (Stacked Bar — Monthly)

| Property | Value |
|---|---|
| Chart type | Stacked bar (Chart.js 4.x) |
| Title | "Monthly Posts by Platform" |
| Data | Per month: count published posts per platform |
| Colour | IG `#E1306C`, FB `#1877F2`, YT `#FF0000`, WA `#25D366`, LI `#0A66C2`, X `#000000` |
| Tooltip | "[Month]: IG [X] · FB [Y] · YT [Z] · WA [W] · LI [V] · X [U]" |
| API | `GET /api/v1/group/{id}/marketing/social-calendar/analytics/by-platform/` |

### 7.3 Engagement Trend (Line Chart)

| Property | Value |
|---|---|
| Chart type | Multi-line |
| Title | "Weekly Engagement Rate Trend" |
| Data | Weekly average engagement rate per platform |
| Colour | Platform-specific colours (same as 7.2) |
| Tooltip | "Week [N]: IG [X]% · FB [Y]% · YT [Z]% · WA [W]% · LI [V]%" |
| API | `GET /api/v1/group/{id}/marketing/social-calendar/analytics/engagement-trend/` |

### 7.4 Posting Heatmap (Time × Day)

| Property | Value |
|---|---|
| Chart type | Heatmap / Matrix (Chart.js matrix plugin) |
| Title | "Best Posting Times — Engagement Heatmap" |
| Data | Average engagement rate by day-of-week × time-slot (2-hour blocks) |
| Colour | Green gradient (higher engagement = darker green) |
| Purpose | Guide Content Coordinator to schedule posts at optimal times |
| API | `GET /api/v1/group/{id}/marketing/social-calendar/analytics/posting-heatmap/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Post created | "Post '[Content Type]' saved as draft — scheduled [Date]" | Success | 3s |
| Submitted for approval | "Post submitted for approval — [Approver] notified" | Success | 3s |
| Approved | "Post approved — ready to publish on [Date] at [Time]" | Success | 4s |
| Changes requested | "Post needs changes — see approver comments" | Warning | 5s |
| Rejected | "Post rejected by [Approver] — [Reason]" | Error | 5s |
| Published | "Post marked as published on [Platform] — [URL]" | Success | 4s |
| Engagement logged | "Engagement data logged for [Platform] post" | Success | 3s |
| Rescheduled | "Post rescheduled from [Old Date] to [New Date]" | Info | 3s |
| Festival post created | "Festival greeting post created for [Festival] on [Date]" | Success | 3s |
| Duplicate created | "Post duplicated — edit and schedule the copy" | Info | 3s |
| Template applied | "Template '[Name]' applied — customise and submit" | Info | 3s |
| Missing festival post | "⚠ [Festival] is in 3 days — no post scheduled yet" | Warning | 6s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No posts this month | 📱 | "No Posts Scheduled" | "Create social media posts to keep your group's presence active across platforms." | New Post |
| No published posts | 📤 | "Nothing Published Yet" | "Approve and publish scheduled posts to start building engagement." | View Queue |
| No engagement data | 📊 | "No Engagement Tracked" | "Log engagement metrics from platform analytics after posts are published." | — |
| No templates | 🎨 | "No Templates Available" | "Create content templates for Topper Cards, Festival Greetings, and other recurring post types." | Create Template |
| No posts for filter | 🔍 | "No Matching Posts" | "Adjust filters to find social media posts." | Clear Filters |
| No festival posts planned | 🎉 | "Festival Calendar Not Set" | "[N] upcoming festivals have no posts planned. Open the festival calendar to plan content." | Festival Calendar |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer + calendar grid skeleton (monthly view) |
| Calendar month change | Calendar grid skeleton (re-render) |
| Tab switch | Content skeleton |
| List view load | Filter bar + table skeleton (12 rows) |
| Post detail drawer | 720px skeleton: tabs + image placeholder + text lines |
| New post modal | Form skeleton with platform tabs |
| Publish queue load | Timeline card skeleton (5 cards) |
| Content library load | Template grid placeholder (8 cards) |
| Engagement dashboard | Summary table skeleton + heatmap placeholder |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/social-calendar/` | G1+ | List posts (paginated, filterable) |
| GET | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/` | G1+ | Post detail |
| POST | `/api/v1/group/{id}/marketing/social-calendar/` | G2+ | Create post |
| PUT | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/` | G2+ | Update post |
| DELETE | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/` | G4+ | Delete post |
| PATCH | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/submit/` | G2+ | Submit for approval |
| PATCH | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/approve/` | G3+ | Approve post |
| PATCH | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/reject/` | G3+ | Reject post |
| PATCH | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/publish/` | G2+ | Mark as published |
| PATCH | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/reschedule/` | G2+ | Reschedule post |
| POST | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/engagement/` | G2+ | Log engagement data |
| GET | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/engagement/` | G1+ | Get engagement data |
| POST | `/api/v1/group/{id}/marketing/social-calendar/{post_id}/duplicate/` | G2+ | Duplicate post |
| GET | `/api/v1/group/{id}/marketing/social-calendar/calendar/` | G1+ | Calendar view data (month param) |
| GET | `/api/v1/group/{id}/marketing/social-calendar/queue/` | G1+ | Publish queue |
| GET | `/api/v1/group/{id}/marketing/social-calendar/templates/` | G1+ | Content templates |
| GET | `/api/v1/group/{id}/marketing/social-calendar/festivals/` | G1+ | Festival calendar |
| PUT | `/api/v1/group/{id}/marketing/social-calendar/festivals/{date}/` | G2+ | Update festival post status |
| GET | `/api/v1/group/{id}/marketing/social-calendar/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/social-calendar/analytics/by-content-type/` | G1+ | Content type chart |
| GET | `/api/v1/group/{id}/marketing/social-calendar/analytics/by-platform/` | G1+ | Platform stacked bar |
| GET | `/api/v1/group/{id}/marketing/social-calendar/analytics/engagement-trend/` | G1+ | Engagement line chart |
| GET | `/api/v1/group/{id}/marketing/social-calendar/analytics/posting-heatmap/` | G1+ | Heatmap data |
| POST | `/api/v1/group/{id}/marketing/social-calendar/export/` | G1+ | Export report |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../social-calendar/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Calendar load | Page load / month change | `hx-get=".../social-calendar/calendar/?month={m}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#calendar-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Dropdowns | `hx-get` with params | `#posts-table-body` | `innerHTML` | `hx-trigger="change"` |
| Post detail drawer | Card/row click | `hx-get=".../social-calendar/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create post | Form submit | `hx-post=".../social-calendar/"` | `#create-result` | `innerHTML` | `hx-encoding="multipart/form-data"` |
| Submit for approval | Button click | `hx-patch=".../social-calendar/{id}/submit/"` | `#status-badge-{id}` | `innerHTML` | Inline badge update |
| Approve post | Approval form | `hx-patch=".../social-calendar/{id}/approve/"` | `#approval-result` | `innerHTML` | Toast + badge update |
| Mark published | Publish form | `hx-patch=".../social-calendar/{id}/publish/"` | `#status-badge-{id}` | `innerHTML` | Badge + engagement form prompt |
| Log engagement | Engagement form | `hx-post=".../social-calendar/{id}/engagement/"` | `#engagement-display-{id}` | `innerHTML` | Updates engagement column |
| Publish queue | Queue tab | `hx-get=".../social-calendar/queue/"` | `#queue-content` | `innerHTML` | Timeline card layout |
| Calendar drag-drop | Drop event | `hx-patch=".../social-calendar/{id}/reschedule/"` | `#calendar-cell-{date}` | `innerHTML` | Optimistic UI + server confirm |
| Festival calendar | Modal open | `hx-get=".../social-calendar/festivals/"` | `#festival-modal-body` | `innerHTML` | Full year list |
| Month navigation | Month arrows | `hx-get=".../social-calendar/calendar/?month={m}"` | `#calendar-grid` | `innerHTML` | `hx-trigger="click"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#posts-table-body` | `innerHTML` | 25/page |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
