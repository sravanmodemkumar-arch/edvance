# Division L — Marketing & Growth: Pages List & Architecture

> EduForge platform-level Marketing & Growth covering all 6 exam domains and 2,050 target institutions.
> 5 original roles (IDs 64–68) + 3 new roles (#98, #99, #100) = **8 roles total**.
> Division L owns brand, demand generation, content, SEO, paid performance, social, email/CRM, and lead attribution feeding into Division K (Sales) pipeline.
> **Cross-cutting spec** (toasts, loaders, error states, approval workflows, DPDP, mktg_config, notification triggers): see [L-00 Global Spec](l-00-global-spec.md).
> **Level 0 note:** Roles 64–68 have Level 0 for the EduForge student/institution platform. Level 0 = "Internal tools only (HR, Marketing, Admin)" — the `/marketing/` portal IS an internal tool and is accessible to all 8 Division L roles per their role matrix.

---

## Scale Context

| Segment | Target Institutions | Decision-Maker Persona | Primary Channel | Avg Decision Cycle |
|---|---|---|---|---|
| Schools | 1,000 | Principal / School Management Committee | Google Search + Referral | 4–12 weeks |
| Colleges | 800 | Principal / HOD | Google Display + Referral | 6–16 weeks |
| Coaching Centres | 100 | Owner / Director | Meta Ads + WhatsApp | 2–6 weeks |
| Institution Groups | 150 | Group Admin / Board | Brand Events + Direct | 12–24 weeks |
| **Total** | **2,050** | — | — | — |

Marketing generates MQLs across 6 exam domains: **SSC · RRB · School/Board · Intermediate · Coaching · Groups**.
MQLs handed off to Division K (Sales) as `sales_lead` records with full UTM source/campaign attribution.

---

## Nightly Data Imports (Celery Tasks)

| Task | Source | Schedule (IST) | Target Tables |
|---|---|---|---|
| Task L-1 | Google Ads API | 02:00 | `mktg_campaign_daily_metric` |
| Task L-2 | Meta Ads API (Facebook + Instagram) | 02:30 | `mktg_campaign_daily_metric` |
| Task L-3 | Google Search Console API | 03:00 | `mktg_keyword.current_position` + `mktg_content.organic_clicks_30d` |
| Task L-4 | YouTube Analytics API | 03:30 | `mktg_social_post` metrics (views, watch time, subscriber delta) |
| Task L-5 | Instagram Insights API | 04:00 | `mktg_social_post` metrics (reach, impressions, saves, engagement) |
| Task L-6 | Monthly report generation | 1st of each month, 08:00 | Email PDF + data pack to Marketing Manager (#64) |

All import tasks write to Celery task log (`mktg_import_log`). Failures alert via Notification Manager (F-06) to Marketing Manager and DevOps.

---

## Division L Roles

| # | Role | Level | Can Do | Cannot Do |
|---|---|---|---|---|
| 64 | Marketing Manager | 0 | Brand strategy; approve all content / assets / campaigns; quarterly budget allocation; team performance tracking; full read across all L pages | EduForge platform config; billing; infra; sales pipeline edits |
| 65 | SEO / Content Executive | 0 | Blog, landing page, exam-prep content authoring; keyword tracking; GSC monitoring; content brief submission; own content edit | Approve own content; approve brand assets; paid ad config; view attribution model |
| 66 | Social Media Manager | 0 | Post scheduling across YouTube / Instagram / Twitter; channel analytics; community management; video brief submission to Division E | Performance ad budget; content publishing approval; brand asset upload |
| 67 | Performance Marketing Exec | 0 | Google Ads + Meta Ads campaign CRUD; creative briefing; UTM config; A/B test campaigns; budget tracking within allocation | Content approve; brand asset upload; attribution model config; view other execs' campaigns |
| 68 | Brand Manager | 0 | Brand asset upload + versioning per domain; typography / colour governance; brand compliance review; co-approve assets with Marketing Manager | Performance ad management; content authoring; social post scheduling |
| 98 | Marketing Analyst | 1 | Attribution model config (First/Last/Linear); CAC, ROAS, CPL reporting; conversion funnel analytics; channel mix analysis; lead quality scoring from UTM data; full export | No campaign edits; no content edits; no asset uploads; no customer-facing comms |
| 99 | Content Strategist | 2 | Editorial calendar CRUD; content brief creation and assignment; keyword cluster strategy; content performance review; approve content (co-gate with Marketing Manager before publish) | Performance ad management; brand asset upload; social scheduling; no EduForge platform writes |
| 100 | Email & CRM Marketing Executive | 0 | Drip sequence creation; email template authoring; contact list management; send scheduling; open/click/bounce analytics; WhatsApp broadcast scripts; email A/B tests | Cannot send to >10K contacts without Marketing Manager approval; no access to sales financial data; no platform config |

---

## Page Inventory

| Page | Route | Primary Role | Purpose |
|---|---|---|---|
| L-01 | `/marketing/` | Marketing Manager (#64) | Unified marketing command center — spend, impressions, leads, content calendar, SEO movers, budget burn |
| L-02 | `/marketing/campaigns/` | Perf. Marketing Exec (#67) + Manager (#64) | Campaign manager across Google, Meta, YouTube — create, filter, pause, bulk actions, export |
| L-03 | `/marketing/campaigns/{id}/` | Perf. Marketing Exec (#67) + Analyst (#98) | Campaign detail — daily metrics chart, ad sets, creatives, lead attribution, spend vs budget |
| L-04 | `/marketing/content/` | SEO Exec (#65) + Content Strategist (#99) | Content pipeline + SEO keyword tracker — editorial calendar, status workflow, ranking positions |
| L-05 | `/marketing/social/` | Social Media Manager (#66) | Cross-platform social hub — per-platform analytics tabs, post scheduler, comment monitor |
| L-06 | `/marketing/brand/` | Brand Manager (#68) + Manager (#64) | Brand asset library — per-domain kits, version history, download, deprecation management |
| L-07 | `/marketing/attribution/` | Marketing Analyst (#98) + Manager (#64) | Lead attribution — MQL→SAL→Won funnel, channel contribution, attribution model selector |
| L-08 | `/marketing/reports/` | Marketing Manager (#64) + Analyst (#98) | Marketing performance reports — CAC, ROAS, channel mix, content ROI, monthly summaries |
| L-09 | `/marketing/email/` | Email & CRM Exec (#100) + Manager (#64) | Email sequence manager, template editor, send queue, analytics, bulk-send approval |

---

## Role-to-Page Access Matrix

| Page | 64 Manager | 65 SEO Exec | 66 Social | 67 Perf. Mktg | 68 Brand | 98 Analyst | 99 Content Strat. | 100 Email Exec |
|---|---|---|---|---|---|---|---|---|
| L-09 Email Hub | Full | No access | No access | No access | No access | Read-only analytics | No access | Full CRUD |
| L-01 Dashboard | Full all sections | SEO + content strip | Social strip | Campaign strip | Brand tasks strip | Analytics strip | Content strip | Email strip |
| L-02 Campaigns | Full + approve | No access | No access | Full CRUD (own) | No access | Read-only all | No access | No access |
| L-03 Campaign Detail | Full | No access | No access | Full (own campaigns) | No access | Read-only | No access | No access |
| L-04 Content & SEO | Full + approve | Full own content + SEO tab | No access | No access | No access | Read + keyword data | Full CRUD calendar + approve gate | No access |
| L-05 Social Hub | Full | No access | Full CRUD | No access | No access | Read-only | No access | No access |
| L-06 Brand Library | Full + approve | Read + download | Read + download | Read + download | Full CRUD + approve | No access | Read + download | No access |
| L-07 Attribution | Full | No access | No access | Own campaigns read | No access | Full + model config | No access | No access |
| L-08 Reports | Full all + export | Content section | Social section | Campaign section | Brand section | Full all + export | Content section | Email section |

---

## Data Model

### `mktg_campaign`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| channel | varchar(30) | NOT NULL; enum `GOOGLE_SEARCH` · `GOOGLE_DISPLAY` · `META_FACEBOOK` · `META_INSTAGRAM` · `YOUTUBE_ADS` · `EMAIL` · `ORGANIC_SEO` · `WHATSAPP` · `REFERRAL` |
| objective | varchar(30) | NOT NULL; enum `BRAND_AWARENESS` · `LEAD_GEN` · `RETARGETING` · `ENGAGEMENT` · `APP_INSTALL` |
| target_segment | varchar(20) | NOT NULL DEFAULT `ALL`; enum `SCHOOL` · `COLLEGE` · `COACHING` · `GROUP` · `ALL` |
| target_region | varchar(500) | Comma-separated states/districts |
| status | varchar(20) | NOT NULL DEFAULT `DRAFT`; enum `DRAFT` · `SCHEDULED` · `ACTIVE` · `PAUSED` · `ENDED` · `ARCHIVED` |
| budget_paise | bigint | NOT NULL |
| spend_paise | bigint | NOT NULL DEFAULT 0; synced nightly from ad platform API |
| start_date | date | NOT NULL |
| end_date | date | NULL = ongoing |
| external_campaign_id | varchar(200) | Platform's ID (Google Ads campaign ID / Meta campaign ID); NULL for organic |
| utm_source | varchar(100) | |
| utm_medium | varchar(100) | |
| utm_campaign | varchar(200) | |
| goal_impressions | bigint | NULL if not set |
| goal_leads | int | NULL if not set |
| created_by_id | FK auth_user | |
| created_at | timestamptz | NOT NULL DEFAULT now() |
| updated_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_campaign_daily_metric`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| campaign_id | FK mktg_campaign | ON DELETE CASCADE |
| metric_date | date | NOT NULL |
| impressions | bigint | NOT NULL DEFAULT 0 |
| clicks | bigint | NOT NULL DEFAULT 0 |
| spend_paise | bigint | NOT NULL DEFAULT 0 |
| conversions | int | NOT NULL DEFAULT 0; form fills / demo requests via UTM |
| leads_created | int | NOT NULL DEFAULT 0; `sales_lead` records with this campaign's UTM |
| video_views | bigint | NULL; populated for YouTube / Meta video campaigns |
| reach | bigint | NULL; unique users reached |
| UNIQUE | (campaign_id, metric_date) | |

### `mktg_content`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| title | varchar(500) | NOT NULL |
| content_type | varchar(30) | NOT NULL; enum `BLOG_POST` · `LANDING_PAGE` · `CASE_STUDY` · `WHITEPAPER` · `INFOGRAPHIC` · `EXAM_GUIDE` · `VIDEO_SCRIPT` · `EMAIL_TEMPLATE` · `AD_COPY` |
| exam_domain | varchar(30) | enum `SSC` · `RRB` · `BOARD` · `INTERMEDIATE` · `COACHING` · `GROUPS` · `CORPORATE`; NULL = cross-domain |
| target_keyword | varchar(300) | Primary SEO keyword |
| status | varchar(20) | NOT NULL DEFAULT `BRIEF`; enum `BRIEF` · `IN_PROGRESS` · `REVIEW` · `APPROVED` · `PUBLISHED` · `ARCHIVED` |
| author_id | FK auth_user | Content writer / SEO exec |
| reviewer_id | FK auth_user | Content Strategist or Marketing Manager |
| target_publish_date | date | |
| published_at | timestamptz | Set when status → `PUBLISHED` |
| url | varchar(1000) | Live URL (set after publish) |
| word_count | int | |
| organic_clicks_30d | int | Synced from GSC nightly |
| avg_position_30d | numeric(5,1) | Synced from GSC nightly; NULL if not ranking in top 100 |
| created_by_id | FK auth_user | |
| created_at | timestamptz | NOT NULL DEFAULT now() |
| updated_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_keyword`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| keyword | varchar(500) | NOT NULL UNIQUE |
| exam_domain | varchar(30) | Which domain this keyword targets |
| monthly_volume | int | From keyword research (manually set or external API) |
| difficulty | int | 0–100 |
| current_position | numeric(5,1) | Synced from GSC nightly; NULL if not ranking in top 100 |
| prev_position | numeric(5,1) | Position from 7 days ago; used for delta display |
| target_url | varchar(1000) | Which page we want ranking for this keyword |
| is_tracking | boolean | NOT NULL DEFAULT true |
| added_by_id | FK auth_user | |
| last_synced_at | timestamptz | |

### `mktg_brand_asset`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| asset_type | varchar(30) | NOT NULL; enum `LOGO` · `COLOR_PALETTE` · `TYPOGRAPHY` · `PRESENTATION_TEMPLATE` · `SOCIAL_TEMPLATE` · `BANNER_TEMPLATE` · `ICON_SET` · `PHOTOGRAPHY` · `BRAND_GUIDELINES` |
| domain | varchar(30) | NOT NULL; enum `SSC` · `RRB` · `BOARD` · `INTERMEDIATE` · `COACHING` · `GROUPS` · `CORPORATE` |
| file_r2_key | varchar(1000) | NOT NULL; Cloudflare R2 key |
| file_format | varchar(10) | enum `PNG` · `SVG` · `PDF` · `PPTX` · `FIGMA` · `ZIP` |
| file_size_bytes | bigint | |
| version | varchar(20) | NOT NULL DEFAULT `1.0` |
| parent_asset_id | FK mktg_brand_asset | NULL for original versions; FK to parent for new versions |
| is_current_version | boolean | NOT NULL DEFAULT true |
| is_deprecated | boolean | NOT NULL DEFAULT false |
| deprecation_reason | text | |
| uploaded_by_id | FK auth_user | |
| approved_by_id | FK auth_user | Brand Manager or Marketing Manager |
| created_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_social_post`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| platform | varchar(20) | NOT NULL; enum `YOUTUBE` · `INSTAGRAM` · `TWITTER` · `WHATSAPP_CHANNEL` · `LINKEDIN` |
| content_text | text | NOT NULL |
| media_r2_keys | jsonb | DEFAULT `[]`; array of R2 keys for images/videos |
| scheduled_at | timestamptz | NOT NULL |
| posted_at | timestamptz | Set when successfully posted via platform API |
| status | varchar(20) | NOT NULL DEFAULT `SCHEDULED`; enum `DRAFT` · `SCHEDULED` · `POSTED` · `FAILED` · `CANCELLED` |
| exam_domain | varchar(30) | |
| external_post_id | varchar(200) | Platform post ID (after posting) |
| impressions | bigint | DEFAULT 0; synced nightly |
| reach | bigint | DEFAULT 0; synced nightly |
| likes | int | DEFAULT 0; synced nightly |
| comments | int | DEFAULT 0; synced nightly |
| shares | int | DEFAULT 0; synced nightly |
| created_by_id | FK auth_user | |
| created_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_social_platform_metric`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| platform | varchar(20) | NOT NULL |
| metric_date | date | NOT NULL |
| followers | int | Total follower/subscriber count at end of day |
| follower_delta | int | Change from previous day |
| total_views | bigint | YouTube only |
| watch_time_minutes | bigint | YouTube only |
| avg_view_duration_sec | int | YouTube only |
| reach | bigint | Instagram only |
| story_views | bigint | Instagram only |
| profile_visits | int | Twitter / Instagram |
| UNIQUE | (platform, metric_date) | |

### `mktg_channel_budget`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| channel | varchar(30) | NOT NULL; same enum as `mktg_campaign.channel` |
| quarter | varchar(7) | NOT NULL; e.g., `2026-Q1` |
| allocated_paise | bigint | NOT NULL |
| UNIQUE | (channel, quarter) | |

### `mktg_lead_attribution`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| lead_id | FK sales_lead | ON DELETE CASCADE |
| campaign_id | FK mktg_campaign | ON DELETE SET NULL; NULL if organic / unattributed |
| attribution_type | varchar(20) | NOT NULL; enum `FIRST_TOUCH` · `LAST_TOUCH` · `LINEAR` |
| utm_source | varchar(100) | |
| utm_medium | varchar(100) | |
| utm_campaign | varchar(200) | |
| utm_content | varchar(200) | |
| attributed_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_email_sequence`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| name | varchar(300) | NOT NULL |
| target_segment | varchar(20) | NOT NULL; enum `SCHOOL` · `COLLEGE` · `COACHING` · `GROUP` · `ALL` |
| trigger | varchar(50) | NOT NULL; enum `LEAD_CREATED` · `DEMO_DONE` · `PROPOSAL_SENT` · `TRIAL_EXPIRY` · `MANUAL` |
| status | varchar(20) | NOT NULL DEFAULT `DRAFT`; enum `DRAFT` · `ACTIVE` · `PAUSED` · `ARCHIVED` |
| step_count | int | NOT NULL DEFAULT 0 |
| enrolled_count | int | NOT NULL DEFAULT 0; leads currently in this sequence |
| open_rate_pct | numeric(5,2) | Computed on last sync |
| click_rate_pct | numeric(5,2) | Computed on last sync |
| created_by_id | FK auth_user | |
| created_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_email_send`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| sequence_id | FK mktg_email_sequence | |
| lead_id | FK sales_lead | |
| step_number | int | NOT NULL |
| sent_at | timestamptz | |
| opened_at | timestamptz | |
| clicked_at | timestamptz | |
| bounced | boolean | NOT NULL DEFAULT false |
| unsubscribed | boolean | NOT NULL DEFAULT false |
| status | varchar(20) | NOT NULL DEFAULT `QUEUED`; enum `QUEUED` · `SENT` · `OPENED` · `CLICKED` · `BOUNCED` · `UNSUBSCRIBED` |

### `mktg_keyword_position_history`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| keyword_id | FK mktg_keyword | ON DELETE CASCADE |
| recorded_date | date | NOT NULL |
| position | numeric(5,1) | NULL if not ranking in top 100 |
| UNIQUE | (keyword_id, recorded_date) | |

### `mktg_seo_domain_metric`

> Defined fully in [L-00 Global Spec §6](l-00-global-spec.md). Summary:

One row per day for EduForge domain-level SEO (GSC organic clicks, impressions, avg CTR, avg position, domain authority, referring domains, indexed pages). Populated by Task L-3.

### `mktg_asset_review_note`

> Defined fully in [L-00 Global Spec §6](l-00-global-spec.md). Summary:

Comment thread on brand asset review — reviewer notes when requesting changes before approval. `asset_id` FK, `note` text, `created_by_id`, `created_at`.

### `mktg_report_delivery_log`

> Defined fully in [L-00 Global Spec §6](l-00-global-spec.md). Summary:

Audit log for every scheduled/manual report delivery. `schedule_id`, `triggered_by` enum, `recipient_count`, `status` (SUCCESS/PARTIAL/FAILED), `error_detail`, `pdf_r2_key`.

### `mktg_bulk_send_approval`

> Defined fully in [L-00 Global Spec §6](l-00-global-spec.md). Summary:

Tracks large-audience email send approval requests (> `mktg_config['email_bulk_send_threshold']` contacts). PENDING → APPROVED/DENIED by Marketing Manager.

### `mktg_config`

> Defined fully in [L-00 Global Spec §5](l-00-global-spec.md). Summary:

Key/value configuration store for marketing targets and thresholds (CPL targets, bulk send threshold, budget alert %, content overdue alert days, etc.).

### `mktg_email_template`

> Defined fully in [L-09 Email & CRM Hub](l-09-email-crm-hub.md). Summary:

Email templates: `name`, `template_type` enum, `exam_domain`, `subject_default`, `html_body` (must contain `{{unsubscribe_link}}`), `text_fallback`, `merge_tags` jsonb.

### `mktg_email_sequence_step`

> Defined fully in [L-09 Email & CRM Hub](l-09-email-crm-hub.md). Summary:

Steps within a sequence: `sequence_id`, `step_number`, `template_id`, `delay_days`, `subject_override`, `condition` jsonb.

### `mktg_social_platform_metric`

> Defined fully in [L-05 Social Media Hub](l-05-social-media-hub.md). Summary:

Daily platform metrics per social platform (followers, follower_delta, total_views, watch_time_minutes, avg_view_duration_sec, reach, story_views, profile_visits).

### `mktg_import_log`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| task_name | varchar(50) | NOT NULL; e.g., `Task L-1` |
| run_at | timestamptz | NOT NULL |
| status | varchar(20) | NOT NULL; enum `SUCCESS` · `PARTIAL` · `FAILED` |
| records_updated | int | |
| error_detail | text | NULL if status = `SUCCESS` |

### `mktg_creative`

| Column | Type | Constraints / Notes |
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

### `mktg_campaign_log`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| campaign_id | FK mktg_campaign | ON DELETE CASCADE |
| action | varchar(50) | enum `CREATED` · `STATUS_CHANGED` · `BUDGET_UPDATED` · `FIELD_UPDATED` · `CREATIVE_ADDED` |
| old_value | jsonb | Previous value |
| new_value | jsonb | New value |
| performed_by_id | FK auth_user | |
| logged_at | timestamptz | NOT NULL DEFAULT now() |

### `mktg_asset_download_log`

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| asset_id | FK mktg_brand_asset | ON DELETE CASCADE |
| downloaded_by_id | FK auth_user | |
| downloaded_at | timestamptz | NOT NULL DEFAULT now() |
| format | varchar(10) | Which format was downloaded |

### `mktg_report_schedule`

| Column | Type | Constraints / Notes |
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

---

## Cross-Division Dependencies

| Division | Dependency | Direction |
|---|---|---|
| Division K (Sales) | `sales_lead.source` + UTM params → `mktg_lead_attribution`; MQL handoff via form → lead create | Marketing → Sales |
| Division F (Exam Ops / Notification) | Email sends >10K contacts routed via F-06 Notification Manager; WhatsApp broadcast scripts | Marketing → F |
| Division E (Video & Learning) | Video content briefs for marketing explainers / YouTube ads passed to Div E production pipeline | Marketing → E |
| Division H (Data & Analytics) | Marketing Analyst reads `analytics_*` tables; campaign spend/lead data fed to Div H MIS | Bidirectional |
| Division I (Support) | Onboarding collateral (exam guides, portal walkthroughs) created by #65/#99 used by Div I Training Coordinator (#52) | Marketing → I |
