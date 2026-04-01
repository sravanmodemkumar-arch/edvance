# O-31 — Student Success Stories

> **URL:** `/group/marketing/topper-relations/success-stories/`
> **File:** `o-31-student-success-stories.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Role:** Group Topper Relations Manager (Role 120, G3) — primary operator

---

## 1. Purpose

The Student Success Stories page manages the creation, editorial workflow, multi-format publishing, and performance tracking of long-form student narratives that go beyond marks and ranks. In the Indian education market, parents make admission decisions based on emotion as much as data — and nothing triggers that emotion more powerfully than a well-told story. "Ramesh, son of a rickshaw driver in Warangal, joined our institution on an RTE scholarship in Class 6, scored 98.6% in TSBIE, cracked JEE Advanced with AIR 2,340, and is now studying at IIT Madras." This story, shared on a WhatsApp family group in a Tier-2 city, reaches 200 families within 24 hours and influences 5–10 admission decisions. No newspaper ad, no hoarding, no Google Ad can match this conversion rate per rupee spent. Groups like Narayana, Allen Career Institute, and Sri Chaitanya invest lakhs in video production teams specifically to capture these stories during results season.

The problems this page solves:

1. **Stories exist only in people's heads:** Every group has dozens of incredible student journeys — first-generation learners cracking NEET, rural girls topping CBSE boards, hostel students from remote districts making it to IITs. But these stories live in the principal's memory or a teacher's anecdote. Nobody writes them down in a structured, media-ready format. When the marketing team needs content for the prospectus, they scramble and get two paragraphs of generic praise instead of a compelling narrative with specific details, before/after photos, and parent quotes. This page provides a structured story database linked to the topper DB (O-28) so every story is backed by verified data.

2. **No editorial workflow:** A Topper Relations Manager or Content Coordinator writes a story draft, but there is no review gate. Factual errors slip through — wrong marks, wrong branch, wrong exam name. Sensitive details get published — family income, caste background, medical conditions — without consent. The system enforces a 4-stage workflow: **Draft** (Topper Relations Mgr 120 or Content Coordinator 131) to **Review** (Campaign Mgr 119) to **Approve** (G4/G5 for high-profile stories) to **Publish**. Each stage has accountability and audit trail. For stories involving minors' personal backgrounds, DPDPA compliance requires explicit parental consent before publishing.

3. **Single-format output:** A story written for the website cannot be directly used in a WhatsApp broadcast (too long), a newspaper insert (wrong format), a video script (different structure), or a prospectus (needs formal tone). The system manages multiple output formats from a single source story: web article (500–1,000 words), WhatsApp summary (150 words max), social media card (key quote + photo), print-ready excerpt (for prospectus/newspaper insert), video script template (for recording team), and parent testimonial standalone extract.

4. **No performance tracking:** The marketing team publishes 30 success stories across website, WhatsApp, and social media, but has no idea which stories drive engagement. The system tracks: views (website), shares (WhatsApp forward count estimates), likes/comments (social media), and most importantly — enquiry attribution (did a prospect mention a specific story during admission counselling?). This data feeds back into story strategy — more stories of the type that convert.

5. **Content consent and DPDPA compliance:** Success stories contain personal data — student name, family background, marks, photos, sometimes health or socioeconomic details. Under DPDPA (Digital Personal Data Protection Act 2023), publishing this requires explicit consent. For minors (most school students under 18), parental consent is mandatory under Section 9 of DPDPA. The system tracks consent status per story and blocks publishing if consent is missing or expired. Stories mentioning caste, religion, disability, or income require additional G4/G5 approval.

6. **Scattered media assets:** A single success story might involve: a professional portrait photo, a casual campus photo, a video testimonial (2–5 min), a parent video quote, scanned marksheets, before/after photos (Class 6 admission photo vs Class 12 felicitation photo), and press clippings. These assets are scattered across phones, WhatsApp groups, and photographer hard drives. The system centralises all media per story and makes them available to downstream consumers — O-03 (Material Library), O-12 (WhatsApp Campaigns), O-08 (Campaign Builder).

**Content types managed:** Written narratives (500–1,000 words), video testimonials (2–5 minutes), parent testimonials (written or video), teacher attribution stories ("My Maths teacher personally coached me for 6 months"), journey stories (where the student started vs where they reached — most powerful for underprivileged/scholarship students), and alumni career updates ("Former topper now at Google/ISRO/AIIMS").

**Scale:** 20–100 success stories per group per season · 6 story types · 4-step editorial workflow · 5+ output formats · 5–8 publishing channels · Linked to O-28 (Topper Database), O-30 (Brand Ambassadors), O-03 (Material Library), O-12 (WhatsApp Campaigns), O-08 (Campaign Builder)

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Topper Relations Manager | 120 | G3 | Full CRUD — create stories, manage workflow, assign writers, review, publish | Primary operator and editor-in-chief |
| Group Admissions Campaign Manager | 119 | G3 | Read + Review — review stories before publish, assign stories to campaigns, request new stories | Editorial reviewer; uses stories in campaign materials |
| Group Campaign Content Coordinator | 131 | G2 | Create + Edit (drafts only) — write story drafts, upload media, format content for channels | Primary story writer; cannot publish or approve |
| Group Admission Data Analyst | 132 | G1 | Read — story performance analytics, engagement metrics, channel ROI, content MIS | Reporting and MIS |
| Group Admission Telecaller Executive | 130 | G3 | Read (published only) — reference stories during prospect calls for persuasion | Uses stories as talking points during telecalling |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — final approval for high-profile stories (Platinum ambassador stories, press-worthy narratives, stories involving sensitive personal backgrounds) | Brand and compliance gatekeeper |
| Branch Principal | — | G3 | Read + Suggest (own branch) — nominate students for stories, provide teacher quotes, verify facts | Source of story leads and fact-checking |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Story creation: role 120 or 131. Story review: role 119 or G4+. Story final approval: G4/G5 required for stories tagged as high-profile or sensitive. Story publishing: role 120 (with approval chain complete). Media upload: role 120, 131, or G4+. Consent management: role 120 or G4+.

**Content workflow (enforced):**
1. **Draft** — Created by Topper Relations Mgr (120) or Content Coordinator (131). Writer composes narrative, uploads media, formats for channels.
2. **Review** — Submitted to Campaign Mgr (119). Reviewer checks facts against O-28 data, editorial quality, brand compliance, consent status.
3. **Approve** — G4/G5 approval required for: Platinum ambassador stories, stories mentioning caste/religion/income/disability, stories intended for newspaper/press, and any story flagged as sensitive. Non-sensitive stories can be approved by role 119.
4. **Publish** — Role 120 publishes to selected channels. System blocks if consent is missing.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  >  Marketing & Campaigns  >  Topper Relations  >  Student Success Stories
```

### 3.2 Page Header
```
Student Success Stories                               [+ Create Story]  [Editorial Calendar]  [Export]
Topper Relations Manager — Lakshmi Naidu
Sunrise Education Group · Season 2025-26 · 42 total stories · 28 published · 8 pending review · 6 video testimonials · 18 parent testimonials · 24,600 avg views
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Total Stories | Integer | COUNT all stories WHERE season = current | Static blue | `#kpi-total` |
| 2 | Published Stories | Integer | COUNT WHERE status = 'published' AND season = current | Static green | `#kpi-published` |
| 3 | Pending Review | Integer | COUNT WHERE status IN ('submitted','in_review') AND season = current | Red > 15, Amber 5–15, Green < 5 | `#kpi-pending` |
| 4 | Video Testimonials | Integer | COUNT WHERE story_type = 'video_testimonial' AND season = current | Static blue | `#kpi-videos` |
| 5 | Parent Testimonials | Integer | COUNT WHERE story_type IN ('parent_quote','parent_video') AND season = current | Static blue | `#kpi-parent` |
| 6 | Avg Story Views | Integer | AVG(view_count) WHERE status = 'published' AND season = current | Green >= 500, Amber 100–499, Red < 100 | `#kpi-views` |

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Story Library** — All stories with status, type, and performance summary
2. **Editorial Pipeline** — Kanban-style workflow view: Draft / Submitted / In Review / Approved / Published
3. **Publishing Tracker** — Where each story has been published and channel-wise performance
4. **Media Gallery** — All photos, videos, and assets across stories
5. **Story Analytics** — Performance metrics, top stories, channel ROI

### 5.2 Tab 1: Story Library

**Filter bar:** Status (Draft/Submitted/In Review/Approved/Published/Archived) · Story Type (Written Narrative/Video Testimonial/Parent Quote/Teacher Attribution/Journey Story/Alumni Career Update) · Branch · Board/Exam · Season · Writer · Has Video (Yes/No) · Consent Status (Obtained/Pending/Expired) · Tags (Inspirational/Underprivileged/Rural/etc.)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Thumbnail | Image (60x60) | No | Student photo or video frame thumbnail |
| Story Title | Text (link) | Yes | Click opens story detail drawer |
| Student Name | Text | Yes | Linked to O-28 topper record if available |
| Story Type | Badge | Yes | Written Narrative (blue) / Video Testimonial (red) / Parent Quote (green) / Teacher Attribution (amber) / Journey Story (purple) / Alumni Career Update (cyan) |
| Branch | Text | Yes | Branch where student studied |
| Achievement | Text | Yes | "JEE Adv AIR 2,340" or "CBSE 98.6%" |
| Word Count / Duration | Text | Yes | Word count for written; mm:ss for video |
| Writer | Text | Yes | Who drafted the story (role 120 or 131) |
| Status | Badge | Yes | Draft (grey) / Submitted (blue) / In Review (amber) / Approved (green) / Published (emerald) / Archived (slate) |
| Consent | Badge | No | Obtained (green) / Pending (amber) / Expired (red) / N/A |
| Channels Published | Integer | Yes | Number of channels this story is live on |
| Views | Integer | Yes | Aggregate views across all channels |
| Last Updated | Date | Yes | Most recent edit or status change |
| Actions | Buttons | No | [View] [Edit] [Submit for Review] [Publish] [Archive] |

**Default sort:** Status priority (Published > Approved > In Review > Submitted > Draft), then Views DESC
**Pagination:** Server-side, 25/page

### 5.3 Tab 2: Editorial Pipeline

**Kanban board layout — 4 columns (matching the 4-step workflow):**

```
Draft               Review              Approved            Published
-----------         -----------         -----------         -----------
| Story A  |        | Story D  |        | Story F  |        | Story H  |
| Student X|        | Student Y|        | Student Z|        | Student W|
| Written  |        | Video    |        | Journey  |        | Written  |
| 5 days   |        | 2 days   |        | Today    |        | Published|
| By: Coord|        | Rev: Mgr |        | Appr: CEO|        | 3 chnls  |
| [Edit]   |        | [Review] |        | [Publish]|        | [View]   |
-----------         -----------         -----------         -----------
| Story B  |        | Story E  |        | Story G  |        | Story I  |
| ...      |        | ...      |        | ...      |        | ...      |
-----------         -----------         -----------         -----------
```

- Cards are draggable between adjacent columns only (Draft to Review, Review to Approved, Approved to Published) — no skipping stages
- Backward movement allowed: Review to Draft (changes requested), Approved to Review (revoke approval)
- Each card shows: story title, student name, story type badge, days in current stage, writer/reviewer name, thumbnail
- Colour coding: > 5 days in stage = red border, > 3 days = amber border, <= 3 days = green border
- Column counts in header: "Draft (8) | Review (4) | Approved (2) | Published (28)"
- Drag-drop access: Role 120 can move between all columns; Role 131 can only move Draft to Review (submit); Role 119 can move Review to Approved/Draft

**Also available as table view (toggle):**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Student Name | Text (link) | Yes | Click opens detail drawer |
| Story Title | Text | Yes | Short title |
| Story Type | Badge | Yes | Written / Video / Parent / Teacher / Journey / Alumni |
| Writer | Text | Yes | Content coordinator or topper manager name |
| Pipeline Stage | Badge | Yes | Draft / Submitted / In Review / Approved / Published |
| Days in Stage | Integer | Yes | Calculated; red highlight if > 5 days |
| Reviewer | Text | Yes | Assigned reviewer (role 119) |
| Due Date | Date | Yes | Target completion date |
| Sensitive Flag | Badge | No | Yes (needs G4/G5) / No |
| Actions | Buttons | No | [View] [Advance] [Return] [Assign Reviewer] |

**Default sort:** Days in Stage DESC (longest-pending first)
**Pagination:** Server-side, 30/page (table view)

### 5.4 Tab 3: Publishing Tracker

**Filter bar:** Story · Channel · Date Range · Performance Tier (High/Medium/Low based on views)

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Story Title | Text (link) | Yes | Story name; click opens detail |
| Student Name | Text | Yes | Student featured |
| Story Type | Badge | Yes | Written / Video / Parent / Teacher / Journey / Alumni |
| Channel | Badge | Yes | Website / WhatsApp Broadcast / Instagram / YouTube / Facebook / Newspaper Insert / Prospectus / Flex Banner |
| Published Date | Date | Yes | When published on this channel |
| Format Used | Badge | No | Full Article / Summary (150 words) / Social Card / Print Excerpt / Video Clip / Banner Layout |
| Views | Integer | Yes | Channel-specific view count (website analytics, YouTube views, Instagram reach) |
| Shares | Integer | Yes | Estimated shares (WhatsApp forward count) or actual shares (social media) |
| Enquiry Attribution | Integer | Yes | Prospects who mentioned this story during counselling (linked to O-15, O-18) |
| Status | Badge | Yes | Live (green) / Scheduled (blue) / Taken Down (red) / Expired (grey) |
| Actions | Buttons | No | [View] [Take Down] [Republish] [Performance Detail] |

**Default sort:** Published Date DESC (newest first)
**Pagination:** Server-side, 30/page

### 5.5 Tab 4: Media Gallery

**Filter bar:** Story · Media Type (Photo/Video/Document/Quote Card) · Upload Date Range · Consent Status (Consented/Pending)

**Grid layout (responsive 4-column):**
- Thumbnail cards (200x200 for photos, 320x180 for videos)
- Each card shows: preview image, student name, media type badge, file size, upload date
- Video cards show play button overlay and duration (mm:ss)
- Consent badge on each card: green checkmark (consented) / amber warning (pending)
- Hover actions: [View Full] [Download] [Use in Story] [Add to O-03 Library] [Delete]

**Bulk actions bar (top):** Select All / Download Selected as ZIP / Push Selected to O-03 Material Library / Delete Selected (G4+ only for delete)

**Storage note:** All media stored on Cloudflare R2 via CDN. Thumbnails auto-generated on upload. Max file sizes: photo 10 MB (JPEG/PNG/WebP), video 500 MB (MP4/MOV), document 20 MB (PDF).

### 5.6 Tab 5: Story Analytics

Charts and summary tables (see Section 7). Key metrics:
- Top 10 performing stories by views and enquiry attribution
- Story type effectiveness: which types drive the most engagement
- Channel performance: which publishing channels generate the most views and enquiries
- Monthly story creation trend: production rate with results-season spike analysis
- Pipeline velocity: average days from Draft to Published
- Consent compliance: percentage of published stories with valid, current consent

---

## 6. Drawers & Modals

### 6.1 Modal: `create-story` (720px)

- **Title:** "Create Student Success Story"
- **Fields:**
  - **Student details (auto-fill from O-28 if linked):**
    - Search O-28 topper database (typeahead — pulls name, photo, achievement, branch, marks, parent details)
    - Or search O-30 brand ambassador database (if ambassador — pulls additional data)
    - Student name (text, required — auto-filled from O-28)
    - Student photo (upload or pulled from O-28, max 10 MB — JPEG/PNG)
    - Branch (dropdown, required)
    - Board/Exam (dropdown: CBSE / ICSE / TSBIE / AP Board / JEE Main / JEE Adv / NEET / CLAT / CUET / Other)
    - Achievement (text — "JEE Advanced AIR 2,340, 2026")
    - Class/Year (dropdown)
  - **Story details:**
    - Story title (text, required — e.g., "From a Government School to IIT: Ramesh's Journey")
    - Story type (dropdown, required):
      - **Written Narrative** — Long-form text story (500–1,000 words); the most versatile format; used for website, prospectus, newspaper inserts; backbone of the content library
      - **Video Testimonial** — 2–5 minute recorded student testimonial; highest engagement on social media and WhatsApp; requires studio or campus recording session
      - **Parent Quote** — Short parent testimonial (100–300 words written or 30–90 sec video); "As a mother, I am grateful to Sunrise Academy..." — emotionally powerful for other parents considering admission
      - **Teacher Attribution** — Story crediting specific teachers; "My Maths teacher, Srinivas Sir, personally coached me daily for 6 months before JEE" — builds teacher brand and institutional trust
      - **Journey Story** — Before-and-after narrative (where student started vs where they reached); most powerful for underprivileged, scholarship, RTE, rural, and first-generation learner stories
      - **Alumni Career Update** — Post-graduation story; "Former topper now Software Engineer at Google / Resident Doctor at AIIMS / Research Scholar at MIT" — demonstrates long-term institutional value
    - Story narrative (rich text editor with formatting — bold, italic, headings, blockquotes, lists):
      - **Writing guidance (shown as collapsible helper panel):**
        - Open with a hook: the most dramatic moment or achievement
        - Include: family background (with consent), admission context, academic journey, key turning points, teacher/mentor influence, exam preparation approach, result day moment, parent reaction, current status
        - Close with a quote from the student or parent
        - Target: 500–1,000 words for written narratives; 150 words for WhatsApp summary (auto-generated)
    - Key quote (text, required — the one-liner for social media cards and WhatsApp: "I never imagined a boy from Srikakulam could get into IIT. Sunrise Academy made it happen.")
    - Parent quote (textarea, optional — "We are daily-wage workers. We never dreamed our son would study at IIT. Sunrise gave him everything.")
    - Teacher quote (textarea, optional — "Ramesh used to stay back every day till 8 PM. His dedication was extraordinary.")
  - **Media attachments:**
    - Student portrait photo (required before publishing — professional photo preferred)
    - Additional photos (upload multiple: family photo, campus photo, felicitation photo, before/after photos, result day celebration)
    - Video file (upload max 500 MB — MP4/MOV; or YouTube/Vimeo URL for externally hosted)
    - Parent video clip (upload or URL — 30–90 sec)
    - Supporting documents (marksheet scan for fact verification — internal only, not published)
  - **Publishing preferences:**
    - Target channels (multi-select): Website / WhatsApp Broadcast / Instagram / YouTube / Facebook / Newspaper Insert / Prospectus / Flex Banner
    - Scheduled publish date (date, optional — for editorial calendar alignment)
    - Priority: Urgent (publish within 24h — results season) / Normal (within 1 week) / Low (queue for next batch)
    - Linked campaign (dropdown from O-08, optional — ties story to a campaign for attribution)
  - **Consent and compliance:**
    - Student consent obtained? (toggle, required for publishing)
    - Parent/guardian consent obtained? (toggle, required if student is minor under 18)
    - Consent form upload (PDF — signed physical consent form or screenshot of digital consent via WhatsApp/email)
    - Sensitive content flag (toggle — MUST be ON if story mentions: caste, religion, income level, disability, medical condition, family disputes, single-parent status)
    - If sensitive flag ON: "This story requires G4/G5 approval before publishing" (auto-enforced)
  - **Tags (multi-select):** Inspirational / Underprivileged Background / Rural / Girl Student / First-Generation Learner / Scholarship / Hostel / RTE / Single Parent / Differently Abled / NRI / Repeater / Career Switch
  - **Internal notes:** (textarea — editorial notes, interview notes, not published)
- **Buttons:** Cancel | Save as Draft | Submit for Review
- **Access:** Role 120 (full), Role 131 (draft only), or G4+

### 6.2 Drawer: `story-detail` (720px, right-slide)

- **Tabs:** Content | Media | Publishing History | Performance | Audit Trail
- **Content tab:**
  - Student photo (prominent, 200x200) with name, branch, achievement badge
  - Story title (large heading), story type badge, status badge
  - Full narrative text (rendered with formatting, scrollable)
  - Key quote highlighted in styled blockquote
  - Parent quote (if available) in secondary blockquote
  - Teacher quote (if available) in tertiary blockquote
  - Word count / video duration
  - Tags displayed as pill badges
  - Consent status panel: Student consent (green/amber/red), Parent consent (green/amber/red/N/A), Sensitive flag (yes/no)
  - Writer name, reviewer name, approver name, last edited date
- **Media tab:**
  - Grid of all attached media — photos (portrait, family, campus, before/after, felicitation), videos, documents
  - Video player for testimonials (inline playback within drawer)
  - Photo lightbox on click (full resolution)
  - Download individual files or all as ZIP
  - [Upload Additional Media] button
- **Publishing History tab:**
  - Table of all publishing instances:

  | Channel | Format Used | Published Date | Status | URL/Link | Views | Shares |
  |---|---|---|---|---|---|---|
  | Website | Full Article | 15 May 2026 | Live | [link] | 1,240 | — |
  | WhatsApp | Summary | 16 May 2026 | Sent | Batch #1842 | — | ~450 |
  | Instagram | Social Card | 16 May 2026 | Live | [link] | 3,800 | 120 |

  - [Publish to New Channel] button
  - [Take Down] button per channel (with reason field)
- **Performance tab:**
  - Summary cards: Total Views (all channels), Total Shares, Enquiry Attributions, Best Channel
  - Per-channel breakdown with metrics
  - Engagement trend mini-chart (sparkline: daily views since first publish)
  - Enquiry list: prospects who mentioned this story during counselling (linked to O-15 Lead Pipeline, O-18 Telecalling)
  - Comparison rank: "This story ranks #[N] out of [Total] published stories by views"
- **Audit Trail tab:**
  - Full lifecycle log with timestamps:
    - Created by [Name] (role) on [date]
    - Submitted for review by [Name] on [date]
    - Reviewed by [Name] (role 119) on [date] — [Approved/Changes Requested with comments]
    - Approved by [Name] (G4/G5) on [date] (if sensitive)
    - Published to [Channel] by [Name] on [date]
    - Taken down from [Channel] by [Name] on [date] — Reason: [reason]
  - Review comments thread (back-and-forth between writer and reviewer)
  - Edit history: what changed between versions
- **Footer:** [Edit] [Submit for Review] [Approve] [Publish to Channel] [Generate Social Card] [Take Down] [Archive] [Delete (G4+ only)]

### 6.3 Modal: `publish-to-channel` (560px)

- **Title:** "Publish Story — [Story Title]"
- **Pre-checks (shown as status panel at top, blocking if failed):**
  - Story status: Must be "Approved" — BLOCKS if Draft/Submitted/In Review
  - Student consent: Obtained — BLOCKS if missing
  - Parent consent (if minor): Obtained — BLOCKS if missing
  - Student photo: Available — WARNING if missing (does not block but shows "story will publish without photo")
  - Sensitive content: G4/G5 approved — BLOCKS if flagged but not approved
- **Fields:**
  - Channel (dropdown, required):
    - **Website** — Full article published on group website success stories section; URL slug auto-generated
    - **WhatsApp Broadcast** — Short summary (auto-generated from full story, 150 words max) sent via O-12 WhatsApp Campaign Manager
    - **Instagram** — Social card (student photo + key quote overlay, 1080x1080) or carousel (multiple photos + story excerpts)
    - **YouTube** — Video testimonial; video must be attached to story; provides title, description, tags for upload
    - **Facebook** — Post with student photo and story excerpt (300 words)
    - **Newspaper Insert** — Print-ready excerpt (300 words, formal tone, formatted for press); generates downloadable PDF
    - **Prospectus** — Formatted block for next admission season prospectus (O-06 notified)
    - **Flex Banner** — Photo + key quote + achievement for branch gate display; generates print-ready layout
  - Format (auto-selected based on channel, manually adjustable):
    - Full Article (website, prospectus)
    - Summary (WhatsApp — auto-truncated to 150 words with "Read more" link)
    - Social Card (Instagram, Facebook — photo + key quote overlay)
    - Print Excerpt (newspaper — 300 words, no informal language)
    - Video (YouTube — requires video attachment)
    - Banner Layout (flex — photo + quote + achievement headline)
  - Scheduled date (date + time, optional — immediate publish if blank)
  - Campaign link (dropdown from O-08, optional — ties this publish instance to a campaign for ROI attribution)
  - Custom CTA text (text, optional — "Admissions open for 2026-27. Call 1800-XXX-XXXX" — appended to WhatsApp and social formats)
- **Preview:** Rendered output in selected channel format (scrollable preview pane)
- **Buttons:** Cancel | Preview | Publish Now | Schedule for Later
- **Access:** Role 120 or G4+ (only if approval workflow is complete)

### 6.4 Drawer: `story-performance-analytics` (640px, right-slide)

- **Title:** "Story Performance — [Story Title]"
- **Summary cards (top row):**
  - Total Views (all channels combined)
  - Total Shares (estimated across WhatsApp, social)
  - Enquiry Attributions (prospects who mentioned this story)
  - Days Since First Published
  - Best Performing Channel (by views)
- **Per-channel breakdown table:**

| Channel | Format | Published Date | Views | Shares | Enquiries | Status |
|---|---|---|---|---|---|---|
| Website | Full Article | 15 May 2026 | 1,240 | — | 8 | Live |
| WhatsApp | Summary | 16 May 2026 | — | ~450 | 12 | Sent |
| Instagram | Social Card | 16 May 2026 | 3,800 | 120 | 3 | Live |
| YouTube | Video | 18 May 2026 | 8,200 | 340 | 5 | Live |

- **Engagement trend chart:** Line chart showing daily views since first publish date (aggregated across channels)
- **Enquiry detail list:** Prospects who mentioned this story during counselling (name, phone, branch interested in, counselling date — linked to O-15 Lead Pipeline and O-18 Telecalling Manager)
- **Comparison panel:** How this story ranks against other published stories:
  - Percentile rank by views
  - Percentile rank by enquiry attribution
  - "Similar stories" — other stories of the same type for benchmarking
- **Footer:** [Take Down from Channel] [Republish to New Channel] [Export Performance Report]

---

## 7. Charts

### 7.1 Stories by Type (Donut)

| Property | Value |
|---|---|
| Chart type | Donut (Chart.js 4.x) |
| Title | "Stories by Type — Season 2025-26" |
| Data | COUNT per story_type WHERE season = current |
| Colour | Written Narrative = `#3B82F6` blue, Video Testimonial = `#EF4444` red, Parent Quote = `#10B981` green, Teacher Attribution = `#F59E0B` amber, Journey Story = `#8B5CF6` purple, Alumni Career Update = `#06B6D4` cyan |
| Centre text | Total: [N] stories |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/by-type/` |

### 7.2 Publishing Channel Distribution (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Stories Published by Channel" |
| Data | COUNT of publishing instances per channel (one story published on 3 channels = 3 counts) |
| Colour | Website = `#3B82F6`, WhatsApp = `#22C55E`, Instagram = `#E11D48`, YouTube = `#EF4444`, Facebook = `#1D4ED8`, Newspaper = `#64748B`, Prospectus = `#F59E0B`, Flex Banner = `#8B5CF6` |
| Tooltip | "[Channel]: [N] stories published, [M] total views" |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/by-channel/` |

### 7.3 Monthly Story Creation Trend (Line)

| Property | Value |
|---|---|
| Chart type | Multi-line (Chart.js 4.x) |
| Title | "Story Creation & Publishing Trend — Last 12 Months" |
| Data | 2 lines — Created (all stories entering Draft) and Published (stories reaching Published status) per month |
| Colour | Created = `#3B82F6` blue (solid line), Published = `#10B981` green (solid line) |
| X-axis | Monthly (Apr 2025 – Mar 2026) |
| Y-axis | Story count |
| Purpose | Show content production rate; highlight results season spike (May–Jun when board/JEE/NEET results arrive) and pre-admission push (Jan–Mar) |
| Annotations | Vertical dashed lines at "CBSE Results", "JEE Results", "NEET Results" dates |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/monthly-trend/` |

### 7.4 Top Performing Stories (Horizontal Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Top 10 Stories by Total Views" |
| Data | Top 10 published stories sorted by aggregate view_count across all channels |
| Colour | Gradient — highest = `#10B981` dark green to lowest = `#D1FAE5` light green |
| Tooltip | "[Story Title] — [Student Name]: [N] views across [M] channels, [P] enquiries attributed" |
| Labels | Truncated story title (max 40 chars) |
| Secondary metric (right-aligned) | Enquiry attribution count per story (shown as small number) |
| API | `GET /api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/top-stories/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Story created | "Story '[Title]' created for [Student Name]" | Success | 3s |
| Story submitted for review | "Story '[Title]' submitted for review — pending Campaign Manager review" | Success | 3s |
| Story approved | "Story '[Title]' approved by [Reviewer] — ready to publish" | Success | 4s |
| Changes requested | "Story '[Title]' needs revisions — see review comments" | Warning | 5s |
| Story published | "Story '[Title]' published to [Channel]" | Success | 3s |
| Story published (multi-channel) | "Story '[Title]' published to [N] channels" | Success | 4s |
| Story taken down | "Story '[Title]' taken down from [Channel]" | Info | 3s |
| Media uploaded | "[N] files uploaded for '[Title]'" | Success | 3s |
| Consent missing (publish blocked) | "Cannot publish '[Title]' — student consent not obtained" | Error | 5s |
| Parent consent missing | "Cannot publish '[Title]' — parent/guardian consent required (student is a minor)" | Error | 5s |
| Sensitive content flag | "Story '[Title]' flagged as sensitive — requires G4/G5 approval before publishing" | Warning | 5s |
| Story archived | "Story '[Title]' archived" | Info | 3s |
| Social card generated | "Social media card generated for '[Student Name]' — download or share" | Success | 3s |
| High performance alert | "Story '[Title]' has crossed [N] views — consider publishing on additional channels" | Info | 4s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No stories created | Book | "No Success Stories" | "Create your first student success story. In Indian education, a well-told topper story drives more admissions than any advertisement." | Create Story |
| No published stories | Megaphone | "No Stories Published" | "You have [N] approved stories waiting to be published. Push them to website, WhatsApp, and social media before the admission season peaks." | Publish Stories |
| No stories pending review | Clipboard | "Review Queue Empty" | "All submitted stories have been reviewed. New drafts will appear here when writers submit them." | — |
| No video testimonials | Video | "No Video Testimonials" | "Record video testimonials with toppers — videos drive 3x more engagement than text on WhatsApp and social media." | Create Video Story |
| No parent testimonials | Heart | "No Parent Testimonials" | "Parent quotes are the most trusted content for other parents. Collect written or video testimonials from proud parents during felicitation events (O-29)." | Create Parent Story |
| No media uploaded | Image | "No Media Attached" | "Upload student photos, videos, and supporting documents to build a rich media library for your stories." | Upload Media |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + story library table skeleton (15 rows) |
| Tab switch | Content area skeleton matching target tab layout |
| Editorial pipeline (kanban) | 4 column skeleton with 3 card placeholders per column |
| Story detail drawer | 720px skeleton: photo placeholder + 5 tabs |
| Publishing tracker table | Filter bar shimmer + table skeleton (20 rows) |
| Media gallery grid | 4x4 image placeholder grid with shimmer effect |
| Create story modal | Form skeleton with rich text editor placeholder area |
| Story performance drawer | Summary cards shimmer + breakdown table + chart placeholder |
| Chart load | Grey canvas placeholder with chart-type outline |
| Video playback | Video player skeleton with centered play button |
| Publish to channel modal | Pre-check status panel + channel selector + preview area skeleton |
| Social card generation | Spinner: "Generating social card..." |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/` | G1+ | List all stories (filterable by status, type, branch, season, writer, consent, tags) |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/` | G1+ | Story detail with all tabs data |
| POST | `/api/v1/group/{id}/marketing/topper-relations/success-stories/` | G2+ | Create new story (role 120 or 131) |
| PUT | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/` | G2+ | Update story content (only in Draft or Changes Requested status) |
| DELETE | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/` | G4+ | Delete story (audit logged, irreversible) |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/submit/` | G2+ | Submit story for review (Draft to Submitted) |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/review/` | G3+ | Review story — approve or request changes; body includes review_action and comments (role 119 or G4+) |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/approve/` | G4+ | Final G4/G5 approval for sensitive/high-profile stories |
| POST | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/publish/` | G3+ | Publish to selected channel (role 120 or G4+); body includes channel, format, schedule_date, campaign_id |
| PATCH | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/publish/{pub_id}/takedown/` | G3+ | Take down from specific channel; body includes reason |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/media/` | G1+ | List all media attached to story |
| POST | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/media/` | G2+ | Upload media (photos, videos, documents); multipart/form-data |
| DELETE | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/media/{media_id}/` | G3+ | Delete media attachment |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/publishing/` | G1+ | Publishing history — all channel instances with status and metrics |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/performance/` | G1+ | Aggregated performance metrics across all channels |
| POST | `/api/v1/group/{id}/marketing/topper-relations/success-stories/{story_id}/social-card/` | G2+ | Generate social media card (quote card) for story |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/pipeline/` | G1+ | Editorial pipeline data (kanban column counts and card list) |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/kpis/` | G1+ | KPI summary bar data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/by-type/` | G1+ | Stories by type donut chart data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/by-channel/` | G1+ | Channel distribution bar chart data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/monthly-trend/` | G1+ | Monthly creation/publishing trend line data |
| GET | `/api/v1/group/{id}/marketing/topper-relations/success-stories/analytics/top-stories/` | G1+ | Top performing stories bar chart data |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | Page load | `hx-get=".../success-stories/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get` with tab param | `#stories-content` | `innerHTML` | `hx-trigger="click"` |
| Story detail drawer | Row/card click | `hx-get=".../success-stories/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create story | Form submit | `hx-post=".../success-stories/"` | `#create-result` | `innerHTML` | `hx-encoding="multipart/form-data"` for media upload; toast + redirect to editor |
| Submit for review | Submit button | `hx-patch=".../success-stories/{id}/submit/"` | `#status-badge-{id}` | `innerHTML` | Inline status badge update + toast |
| Review action | Approve/Return button | `hx-patch=".../success-stories/{id}/review/"` | `#status-badge-{id}` | `innerHTML` | Body includes review_action (approve/request_changes) + comments |
| G4/G5 approval | Approve button | `hx-patch=".../success-stories/{id}/approve/"` | `#approval-badge-{id}` | `innerHTML` | Only shown for sensitive-flagged stories |
| Publish to channel | Publish form submit | `hx-post=".../success-stories/{id}/publish/"` | `#publishing-table-body` | `beforeend` | Adds new row to publishing history; toast |
| Take down | Take down button | `hx-patch=".../success-stories/{id}/publish/{pub_id}/takedown/"` | `#pub-status-{pub_id}` | `innerHTML` | Inline status badge update |
| Kanban drag | Card drop to column | `hx-patch=".../success-stories/{id}/submit/"` or `.../review/` | `#pipeline-board` | `innerHTML` | Drag triggers appropriate status transition endpoint |
| Media upload | Drop zone submit | `hx-post=".../success-stories/{id}/media/"` | `#media-grid` | `beforeend` | `hx-encoding="multipart/form-data"`; progress bar per file |
| Social card generate | Generate form | `hx-post=".../success-stories/{id}/social-card/"` | `#card-preview` | `innerHTML` | Shows generated card in modal with download options |
| O-28 topper search | Typeahead input | `hx-get="/api/v1/group/{id}/marketing/topper-relations/database/?q={term}"` | `#topper-suggestions` | `innerHTML` | `hx-trigger="keyup changed delay:300ms"` |
| Filter apply | Dropdowns change | `hx-get` with filter params | `#story-table-body` | `innerHTML` | `hx-trigger="change"` |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#story-table-body` | `innerHTML` | 25/page (library), 30/page (pipeline table, publishing tracker) |
| Performance drawer load | Performance tab click | `hx-get=".../success-stories/{id}/performance/"` | `#performance-content` | `innerHTML` | Loads metrics + inline chart |
| Chart load | Tab/page load | `hx-get=".../success-stories/analytics/..."` | `#chart-{name}` | `innerHTML` | `hx-trigger="intersect once"` — lazy load on scroll into viewport |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
