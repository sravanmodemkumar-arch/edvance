# L-00 — Division L Global Specification

> Cross-cutting concerns that apply to every page in the Marketing Operations portal (`/marketing/`).
> Reference this document from individual page specs instead of duplicating these rules.

---

## 1. Authentication & Access Model

### Platform Level vs. Marketing Portal Level

The **System Access Levels** (0–5) in `group1-platform-roles.md` describe access to the **EduForge student/institution platform** — not to internal operations portals.

| Level | What it gates |
|---|---|
| 0 | "Internal tools only (HR, Marketing, Admin)" — this IS the Marketing portal |
| 1–5 | EduForge student platform (MCQ bank, exam engine, tenant mgmt, etc.) |

**Roles 64–68 have Level 0**, which means "internal tools only" — the `/marketing/` portal IS an internal tool. They have no access to the EduForge student platform, but full access to the Marketing Operations portal per their role definitions.

**Role #98 (Analyst) has Level 1** — read-only on the EduForge platform; within the Marketing portal their permissions are defined by the role matrix in `div-l-pages-list.md`.

### Session

All `/marketing/*` routes require the user to be authenticated via EduForge's shared Django session (same `auth_user` table). Role check on every view via `user.groups` membership.

Unauthenticated: redirect to `/login/?next=/marketing/`
Authenticated but wrong role (e.g., Division C engineer lands on `/marketing/`): 403 page.

```
403 page:
┌──────────────────────────────────────────────┐
│  Access Restricted                            │
│  You don't have access to the Marketing      │
│  Operations portal.                           │
│  [← Back to your dashboard]                  │
└──────────────────────────────────────────────┘
```

---

## 2. Toast / Notification UI System

All action feedback uses a **toast stack** positioned top-right, `z-index: 9999`.

### Toast Types

| Type | Colour | Auto-dismiss | Use for |
|---|---|---|---|
| SUCCESS | Green (#16A34A) | 4 seconds | Successful saves, status changes, sends |
| ERROR | Red (#DC2626) | Manual dismiss (×) | Failed saves, validation errors, API errors |
| WARNING | Amber (#D97706) | 8 seconds | Budget alerts, approaching limits, stale data |
| INFO | Blue (#2563EB) | 4 seconds | Background jobs started, imports triggered |

### Toast Stacking

- Maximum 3 toasts visible simultaneously
- New toasts slide in from top-right
- Older toasts slide down when a new one appears
- If queue > 3: oldest is dismissed automatically
- Each toast: 280px wide, 56px min-height, 12px border-radius, shadow

### Toast Message Reference

Every action across all Division L pages must produce a toast. Complete list:

**Campaign Manager (L-02 / L-03):**
| Action | Toast Type | Message |
|---|---|---|
| Campaign created | SUCCESS | "Campaign '{name}' created." |
| Campaign paused | SUCCESS | "Campaign paused." |
| Campaign resumed | SUCCESS | "Campaign resumed." |
| Campaign archived | SUCCESS | "Campaign archived." |
| Campaign deleted | SUCCESS | "Draft campaign deleted." |
| Campaign duplicated | SUCCESS | "Campaign duplicated as 'Copy of {name}'." |
| Budget increased | SUCCESS | "Budget updated to ₹{amount}." |
| Budget increase request sent | INFO | "Budget increase request sent to Marketing Manager." |
| Budget increase approved | SUCCESS | "Budget increase approved. Campaign budget updated." |
| Budget increase denied | WARNING | "Budget increase request denied. {reason}" |
| Campaign edit saved | SUCCESS | "Changes saved." |
| Campaign status changed by Manager | INFO | "Your campaign '{name}' was {paused/resumed} by the Marketing Manager." |
| External campaign ID validation fail | ERROR | "Invalid campaign ID format for {channel}. Expected: {format}" |
| Bulk pause complete | SUCCESS | "{N} campaigns paused." |
| Bulk activate complete | SUCCESS | "{N} campaigns activated." |
| Bulk archive complete | SUCCESS | "{N} campaigns archived." |
| Export started | INFO | "Preparing export… You'll be notified when it's ready." |
| Export ready | SUCCESS | "Export ready. [Download →]" |
| Export failed | ERROR | "Export failed. Please try again." |

**Content & SEO (L-04):**
| Action | Toast Type | Message |
|---|---|---|
| Content brief created | SUCCESS | "Brief created and assigned to {author}." |
| Content submitted for review | SUCCESS | "Submitted for review. {reviewer} has been notified." |
| Content returned from review | WARNING | "Content returned with notes. Check review comments." |
| Content approved | SUCCESS | "Content approved and ready to publish." |
| Content published | SUCCESS | "'{title}' published. URL saved." |
| Content archived | SUCCESS | "Content archived." |
| Keyword added | SUCCESS | "Keyword '{keyword}' added to tracking." |
| Keyword removed | SUCCESS | "Keyword removed from tracking." |
| Drag-to-reschedule saved | SUCCESS | "Target date updated to {date}." |
| Drag-to-reschedule failed | ERROR | "Could not update date. Please try the edit drawer." |

**Social Media (L-05):**
| Action | Toast Type | Message |
|---|---|---|
| Post scheduled | SUCCESS | "Post scheduled for {date} {time} IST." |
| Post cancelled | WARNING | "Post cancelled. Content not recoverable." |
| Post edited | SUCCESS | "Post updated." |
| Post retry queued | INFO | "Retrying post…" |
| Post retry succeeded | SUCCESS | "Post published successfully." |
| Post retry failed again | ERROR | "Post failed again. Check platform API credentials." |
| Cross-post created | SUCCESS | "{N} posts scheduled across {platforms}." |

**Brand Assets (L-06):**
| Action | Toast Type | Message |
|---|---|---|
| Asset uploaded (pending) | INFO | "Asset uploaded and pending approval." |
| Asset approved | SUCCESS | "Asset approved and now visible to the team." |
| Asset approval requested | INFO | "Changes requested. {uploader} has been notified." |
| Asset deprecated | WARNING | "Asset deprecated. Previous versions remain accessible." |
| Asset downloaded | SUCCESS | "Download started." |
| Download URL expired | ERROR | "Download link expired. Please retry." |

**Lead Attribution (L-07):**
| Action | Toast Type | Message |
|---|---|---|
| Attribution model changed | INFO | "Model changed to {model}. Charts updated." |
| Export started | INFO | "Preparing attribution export…" |
| Export ready | SUCCESS | "Export ready. [Download →]" |

**Reports (L-08):**
| Action | Toast Type | Message |
|---|---|---|
| Schedule created | SUCCESS | "Report schedule created. First delivery: {date}." |
| Schedule edited | SUCCESS | "Schedule updated." |
| Schedule deleted | WARNING | "Report schedule deleted." |
| Send Now triggered | SUCCESS | "Report sent to {N} recipients." |
| Send Now failed | ERROR | "Report delivery failed. Check recipient emails." |
| Export CSV started | INFO | "Preparing CSV…" |
| Export PDF started | INFO | "Generating PDF…" (shown for > 3 seconds render) |
| Export ready | SUCCESS | "Export ready. [Download →]" |

**Email & CRM (L-09):**
| Action | Toast Type | Message |
|---|---|---|
| Sequence created | SUCCESS | "Sequence '{name}' created." |
| Sequence activated | SUCCESS | "Sequence activated. Enrolling leads…" |
| Sequence paused | WARNING | "Sequence paused. Enrolled leads will not receive further steps." |
| Large send approval requested | INFO | "Send request sent to Marketing Manager ({N} contacts)." |
| Large send approved | SUCCESS | "Bulk send approved. {N} emails queued." |
| Large send denied | ERROR | "Send request denied. {reason}" |
| Template saved | SUCCESS | "Template saved." |
| Test email sent | INFO | "Test email sent to {your email}." |

---

## 3. Loading / Skeleton States

All HTMX part-load targets show a skeleton while loading. Implementation: a `hx-indicator` spinner + skeleton class injected on `htmx:beforeRequest`, removed on `htmx:afterSettle`.

### Skeleton Patterns

| Component | Skeleton |
|---|---|
| KPI tile | 80px × 96px grey shimmer rectangle |
| Table row | Full-width 40px grey shimmer stripe; repeat 10 rows |
| Chart area | Full-width 200px grey shimmer rectangle with a horizontal axis line |
| Card grid | N × (160px × 200px) grey shimmer cards matching grid columns |
| Drawer content | 3–5 grey shimmer lines of varying widths |
| Calendar day cells | Individual cell shimmer for days with content dots |

Shimmer animation: `background: linear-gradient(90deg, #E5E7EB 25%, #F3F4F6 50%, #E5E7EB 75%)` with `background-size: 200% 100%` and `animation: shimmer 1.5s infinite`.

### Slow-Load Timeout

If an HTMX part-load takes > 8 seconds, display an amber warning bar inside the target:
```
⚠ Taking longer than expected. [Retry ↺]
```
[Retry] re-triggers the same HTMX request.

### Full-Page Loader

Only for the initial Django template render (before HTMX takes over). Server-side render completes in < 500ms (static HTML + deferred HTMX loads); no full-page spinner needed. If server is slow, show the page shell with skeletons immediately.

---

## 4. Error States

### Network Error (No Connectivity)

Banner at top of page:
```
🔌 No internet connection. Data may be stale. [Retry]
```
HTMX requests will fail gracefully — `htmx:responseError` event shows inline error within target.

### API / Server Error (5xx)

Within the failing HTMX target:
```
┌────────────────────────────────────────────┐
│  ⚠ Could not load this section.            │
│  [Try again]   Last loaded: 5 min ago      │
└────────────────────────────────────────────┘
```
An ERROR toast is also shown: "Failed to load {section}. Please try again."

### 404 — Resource Not Found

Full page:
```
┌────────────────────────────────────────────┐
│  Page not found                            │
│  This resource doesn't exist or was        │
│  removed.                                  │
│  [← Go back]                               │
└────────────────────────────────────────────┘
```

### Permission Denied (403)

Full page (same as auth failure) or inline if it's a drawer action:
```
You don't have permission to perform this action.
```
No toast — action button should not have been visible; this is a defence-in-depth check.

### Stale Data Warning

When the most recent successful import for any Task (L-1 through L-5) is > 24 hours ago, show an amber banner inside affected sections:
```
⚠ Data last updated {N} hours ago. Import may have failed. [View import log]
```

### Form Validation Errors

Inline, below each field that fails. Red border on input. Error message in red text:
```
Campaign name*
[SSC CGL 2026 — Google Search                              ]
⚠ Campaign name must be unique among active campaigns.
```
On submit of invalid form: scroll to first error field; no toast.

---

## 5. `mktg_config` Table

Global marketing configuration key-value store. Only Marketing Manager (#64) can edit values via `/marketing/settings/` (a simple admin-style form, no separate page spec needed).

| Key | Type | Default | Description |
|---|---|---|---|
| `quarterly_total_budget_paise` | bigint | 0 | Finance-approved quarterly total budget. Channel budgets cannot exceed this total. |
| `target_cpl_paise` | bigint | 0 | Blended CPL target. KPI tiles colour against this. |
| `target_cpl_by_channel` | jsonb | `{}` | Per-channel CPL targets: `{"GOOGLE_SEARCH": 1200000, ...}` (in paise) |
| `target_response_rate_nps` | int | 30 | Target NPS response rate %. (Used by Div J; kept here for cross-div reference) |
| `email_bulk_send_threshold` | int | 10000 | Sends above this count require Marketing Manager approval |
| `seo_position_alert_drop` | int | 5 | Alert SEO Exec + Manager if a keyword drops by ≥ this many positions overnight |
| `content_overdue_alert_days` | int | 2 | Days past target_publish_date before content is flagged "overdue" |
| `import_failure_alert_user_ids` | jsonb | `[]` | User IDs to alert on import task failure (in addition to Marketing Manager #64) |
| `cpa_target_by_segment` | jsonb | `{}` | Per-segment CPA targets: `{"SCHOOL": 8000000, ...}` (in paise) |
| `campaign_budget_alert_pct` | int | 80 | Alert exec + Manager when campaign spend exceeds this % of budget |
| `social_schedule_min_advance_minutes` | int | 15 | Minimum lead time for scheduling a social post |

**Table DDL:**
```sql
CREATE TABLE mktg_config (
    key           varchar(100) PRIMARY KEY,
    value         jsonb        NOT NULL,
    description   text,
    updated_by_id bigint       REFERENCES auth_user(id),
    updated_at    timestamptz  NOT NULL DEFAULT now()
);
```

---

## 6. Missing Table Definitions

### `mktg_seo_domain_metric`

One row per day for EduForge's domain-level SEO metrics. Populated by Task L-3 (Google Search Console + third-party SEO API call).

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| metric_date | date | NOT NULL UNIQUE |
| organic_clicks | int | Total organic clicks from GSC for the day |
| organic_impressions | int | Total GSC impressions for the day |
| avg_ctr | numeric(5,4) | Average click-through rate from GSC |
| avg_position | numeric(5,1) | Average position from GSC |
| domain_authority | int | From third-party SEO API (sync weekly; carried forward on daily rows) |
| referring_domains | int | Unique referring domains (weekly sync; carried forward) |
| indexed_pages | int | Pages indexed by Google (weekly sync) |
| synced_at | timestamptz | NOT NULL DEFAULT now() |

Third-party SEO API (Moz/DataForSEO or equivalent) is called once per week; daily GSC fields are imported nightly. If GSC API is unavailable, the row is skipped and `mktg_import_log` records the failure.

### `mktg_asset_review_note`

Comment thread on brand asset review (when Brand Manager or Marketing Manager requests changes before approving).

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| asset_id | FK mktg_brand_asset | ON DELETE CASCADE |
| note | text | NOT NULL; min 10 chars |
| created_by_id | FK auth_user | |
| created_at | timestamptz | NOT NULL DEFAULT now() |

Notes are shown in the Asset Detail Drawer under "Review History". A reviewer can add multiple notes; uploader can reply. No threading depth beyond one level (note → reply).

### `mktg_report_delivery_log`

Audit log for every scheduled or manual report delivery attempt.

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| schedule_id | FK mktg_report_schedule | ON DELETE SET NULL; NULL for manual sends |
| triggered_by | varchar(20) | NOT NULL; enum `SCHEDULED` · `MANUAL` |
| triggered_by_user_id | FK auth_user | NULL if `SCHEDULED` |
| recipient_count | int | NOT NULL |
| sent_at | timestamptz | NOT NULL DEFAULT now() |
| status | varchar(20) | NOT NULL; enum `SUCCESS` · `PARTIAL` · `FAILED` |
| error_detail | text | NULL if SUCCESS |
| pdf_r2_key | varchar(1000) | R2 key of generated PDF (retained 90 days) |

Displayed in L-08 as a "Delivery History" sub-panel on the Scheduled Reports section: last 10 deliveries per schedule with status badges.

### `mktg_bulk_send_approval`

Tracks large-audience email send approval requests from Email Exec (#100) to Marketing Manager (#64).

| Column | Type | Constraints / Notes |
|---|---|---|
| id | bigserial | PK |
| sequence_id | FK mktg_email_sequence | |
| requested_by_id | FK auth_user | Email Exec who requested |
| recipient_count | int | NOT NULL; estimated at time of request |
| request_note | text | Exec's justification for the bulk send |
| status | varchar(20) | NOT NULL DEFAULT `PENDING`; enum `PENDING` · `APPROVED` · `DENIED` |
| reviewed_by_id | FK auth_user | Marketing Manager who reviewed |
| review_note | text | Manager's reason for denial (or approval note) |
| requested_at | timestamptz | NOT NULL DEFAULT now() |
| reviewed_at | timestamptz | |

---

## 7. Notification Triggers

All notifications dispatched through Division F Notification Manager (Role #37 / F-06). Marketing portal triggers these via internal API call to F-06.

### Division L Notification Events

| Event | Recipients | Channel | Trigger |
|---|---|---|---|
| Content submitted for REVIEW | Assigned reviewer (Content Strategist #99 or Manager #64) | Email + in-app | When `mktg_content.status` → `REVIEW` |
| Content RETURNED from review | Author (created_by_id) | Email + in-app | When reviewer adds note and returns |
| Content APPROVED | Author | Email + in-app | When `status` → `APPROVED` |
| Content PUBLISHED | Author + Marketing Manager #64 | In-app | When `status` → `PUBLISHED` |
| Content OVERDUE | Author + Content Strategist #99 | Email | Celery beat daily at 09:00 IST; fires for items where today > target_publish_date + `content_overdue_alert_days` and status NOT IN ('PUBLISHED', 'ARCHIVED') |
| Brand asset uploaded (pending approval) | Brand Manager #68 + Marketing Manager #64 | Email + in-app | When `mktg_brand_asset` row created with `approved_by_id = NULL` |
| Brand asset APPROVED | Uploader (`uploaded_by_id`) + all Division L active users | In-app | When `approved_by_id` set |
| Brand asset DEPRECATED | All Division L active users | In-app | When `is_deprecated` → true |
| Creative flagged as brand non-compliant | Campaign creator (`mktg_campaign.created_by_id`) + Marketing Manager #64 | Email + in-app | When Brand Manager marks creative as non-compliant (`mktg_creative.brand_compliant = false`) |
| Campaign spend > `campaign_budget_alert_pct` % | Campaign creator + Marketing Manager #64 | Email | Celery beat nightly after Task L-1/L-2 complete |
| Campaign spend = 100% budget | Campaign creator + Marketing Manager #64 | Email (urgent) | Same check — separate template for 100% |
| Budget increase requested by exec | Marketing Manager #64 | Email + in-app | When exec submits increase request |
| Budget increase approved/denied | Requesting exec | Email + in-app | When Manager acts on request |
| Import task FAILED (L-1 through L-5) | `mktg_config['import_failure_alert_user_ids']` + Marketing Manager #64 + DevOps (#14) | Email (urgent) | Immediately on task failure; do NOT retry silently |
| Import task PARTIAL (some records failed) | Marketing Manager #64 | In-app | After nightly import completes |
| SEO keyword dropped ≥ `seo_position_alert_drop` positions | SEO Exec #65 + Content Strategist #99 | In-app | After Task L-3 completes nightly |
| Scheduled social post FAILED | Social Media Manager #66 + Marketing Manager #64 | Email + in-app | Immediately on post failure |
| Bulk email send requested (> threshold) | Marketing Manager #64 | Email + in-app | When Email Exec submits bulk send approval request |
| Bulk send APPROVED | Email Exec #100 | Email + in-app | When Manager approves via `mktg_bulk_send_approval` |
| Bulk send DENIED | Email Exec #100 | Email + in-app | When Manager denies; includes `review_note` |
| Email bounce rate > 2% on a sequence | Email Exec #100 + Marketing Manager #64 | In-app | Weekly check (Monday 09:00 IST) |
| Scheduled report delivery FAILED | Marketing Manager #64 + Analyst #98 + DevOps #14 | Email (urgent) | Immediately on Task L-6 failure |
| Quarter end budget analysis (7 days before) | Marketing Manager #64 | Email | Celery beat on 24th of last quarter month |

**In-app notifications:** stored in generic `notification` table (shared across EduForge); shown in bell icon top-right of all internal portals. Unread count badge updates every 60 seconds via HTMX auto-refresh.

---

## 8. Approval Workflows

### 8.1 Content Approval (Sequential, Not Co-Approval)

Correct flow (resolves ambiguity between L-04 and roles spec):

```
Author writes content
       ↓
   status = IN_PROGRESS
       ↓ (author clicks [Submit for Review])
   status = REVIEW → notify Content Strategist #99
       ↓
  Content Strategist reviews
  ├─ [Approve] → status = APPROVED → notify author → [Publish] enabled
  └─ [Return] → adds note → status = IN_PROGRESS → notify author
       ↓ (approved; Manager clicks [Publish] OR Content Strategist clicks [Publish] post-approval)
   status = PUBLISHED → notify author + Manager
```

Marketing Manager (#64) can bypass the Strategist review and directly approve + publish. Content Strategist (#99) can approve but **cannot** publish without Manager-level sign-off UNLESS Marketing Manager has delegated publish permission via `mktg_config['strategist_can_publish']` boolean (default: false).

### 8.2 Brand Asset Approval

```
Brand Manager uploads asset
       ↓
   approved_by_id = NULL → appears in "Pending" panel (Manager + Brand Manager only)
       ↓
  Brand Manager can self-approve for:
    LOGO, COLOR_PALETTE, TYPOGRAPHY, SOCIAL_TEMPLATE, BANNER_TEMPLATE, ICON_SET, PHOTOGRAPHY
  Marketing Manager must approve for:
    PRESENTATION_TEMPLATE, BRAND_GUIDELINES
       ↓ (approved)
   approved_by_id set → asset visible to all permitted Division L roles → team notified in-app
```

If Marketing Manager requests changes (via [Request Changes] → `mktg_asset_review_note`):
→ notification to uploader → uploader uploads revised file → new `mktg_brand_asset` row with `parent_asset_id` set → new approval cycle.

### 8.3 Campaign Budget Increase Approval

```
Performance Marketing Exec clicks [Request Budget Increase] on campaign
       ↓
  Modal: "New budget: [₹____]  Reason: [_____________]"
  [Submit Request]
       ↓
  Notification sent to Marketing Manager #64 (email + in-app)
       ↓
  Manager sees request in pending approvals panel on L-01 or campaign detail on L-03
  Manager clicks [Approve] or [Deny]
       ↓
  APPROVED: mktg_campaign.budget_paise updated → logged in mktg_campaign_log
            → toast + email to exec: "Budget increase approved"
  DENIED:   reason stored → toast + email to exec: "Budget increase denied: {reason}"
```

### 8.4 Bulk Email Send Approval (> 10,000 contacts)

```
Email Exec (#100) sets up sequence and estimates recipients > 10K
       ↓
  [Activate Sequence] button shows: "⚠ {N} contacts. Manager approval required."
  [Request Approval] button → opens approval request modal:
    "Reason for large send: [___________]"
  POST → creates mktg_bulk_send_approval row (status=PENDING)
       ↓
  Manager notified (email + in-app)
  Manager reviews in L-09 or L-01 pending approvals panel
  [Approve] → mktg_bulk_send_approval.status = APPROVED
            → sequence activated → emails queued via F-06
  [Deny] → status = DENIED → reason sent to exec
```

---

## 9. Permission Enforcement UI Patterns

Never show a button/action that a user cannot perform. If the user discovers a URL directly (e.g., `/marketing/campaigns/create/`), the server returns 403.

| Scenario | UI Pattern |
|---|---|
| Action requires a higher role | Button hidden entirely (not disabled) |
| Action requires a specific state (e.g., [Publish] only after APPROVED) | Button disabled with tooltip: "Approve content first" |
| Action requires Manager approval (in progress) | Button replaced with "Pending approval ⏳" text |
| Read-only view (Analyst, Renewal Exec viewing cross-div data) | No action buttons; row actions show "View" only |
| Export restricted to own data | Export button visible; server enforces scope on download |

---

## 10. DPDP Act 2023 Compliance (Email Marketing)

Division L Email & CRM operations must comply with India's Digital Personal Data Protection Act 2023.

**Consent:**
- All email contact lists must be sourced from `sales_lead` records where the lead contact has provided consent at the time of form fill (tracked in `sales_lead.contact_consent = true`).
- Email Exec cannot manually add arbitrary email addresses to sequences — only contacts from `sales_lead` with `contact_consent = true`.
- Consent withdrawal: if a contact unsubscribes (`mktg_email_send.unsubscribed = true`), they are excluded from ALL future sequences automatically (checked before each email queues).

**Unsubscribe:**
- Every email sent via the system must include an unsubscribe link (injected server-side by the email dispatcher).
- Unsubscribe webhook from email service → sets `mktg_email_send.unsubscribed = true` and flags `sales_lead.email_opt_out = true`.
- `sales_lead.email_opt_out` must be checked before enqueueing any email send.

**Data Minimisation:**
- Email Exec sees recipient names and company names (from `sales_lead`). They do NOT see `sales_lead.arr_estimate_paise`, `sales_lead.probability_pct`, or any financial data.
- Export from L-09 excludes contact email addresses unless user has explicit Manager approval for export with PII.

**Retention:**
- `mktg_email_send` records retained for 2 years, then anonymised (email address cleared, lead_id set to NULL).

---

## 11. URL Structure Summary

| Route | Page |
|---|---|
| `/marketing/` | L-01 Dashboard |
| `/marketing/campaigns/` | L-02 Campaign Manager |
| `/marketing/campaigns/{id}/` | L-03 Campaign Detail |
| `/marketing/campaigns/create/` | L-02 Create drawer (POST target) |
| `/marketing/campaigns/{id}/edit/` | L-03 Edit (POST target) |
| `/marketing/campaigns/{id}/status/` | L-02/L-03 Status change (PATCH target) |
| `/marketing/content/` | L-04 Content & SEO Hub |
| `/marketing/content/create/` | L-04 Brief creation (POST target) |
| `/marketing/social/` | L-05 Social Media Hub |
| `/marketing/social/schedule/` | L-05 Post scheduling (POST target) |
| `/marketing/brand/` | L-06 Brand Asset Library |
| `/marketing/brand/upload/` | L-06 Asset upload (POST target) |
| `/marketing/brand/{id}/approve/` | L-06 Asset approval (PATCH target) |
| `/marketing/attribution/` | L-07 Lead Attribution |
| `/marketing/reports/` | L-08 Marketing Reports |
| `/marketing/email/` | L-09 Email & CRM Hub |
| `/marketing/budgets/` | L-01 Budget edit (PATCH target) |
| `/marketing/feedback/surveys/send/` | L-07 Attribution export target |
| `htmx/l/*` | All HTMX part-load routes |

---

## 12. Mobile Responsiveness

The Marketing portal is primarily a desktop tool (data-dense tables, charts). Mobile is secondary.

**Breakpoints:**
- Desktop (≥ 1024px): Full multi-column layouts as spec'd
- Tablet (768–1023px): Side-by-side charts collapse to single column; tables gain horizontal scroll
- Mobile (< 768px): Show banner "Best viewed on desktop" + single-column layout; tables switch to card-based view with key columns only; create/edit actions still functional

**Table on mobile:** Each row becomes a card with 3 primary columns visible + "···" to expand full row.

---

## 13. Chart Accessibility

All Chart.js charts must include:
- `aria-label` on the canvas element describing the chart (e.g., "Line chart showing NPS trend over 12 months")
- `role="img"` on canvas
- A hidden `<table>` with the same data (CSS `sr-only`) for screen readers
- High-contrast colour scheme (minimum 4.5:1 contrast ratio per WCAG AA)
- No colour-only encoding — all data series also differentiated by line style (dashed, dotted, solid) and/or marker shape

---

## 14. Data Freshness Display

All data sections that rely on nightly imports show a data freshness badge:

```
Last updated: 2h ago (today's import)  |  ⚠ Data is 26h old — import may have failed
```

- Freshness computed from `mktg_import_log.run_at` for the relevant task
- Green if < 26h; amber if 26–48h; red if > 48h
- Red state also fires the notification per Section 7 (if not already sent)
- Shown near the section header, not as a page-wide banner (each section may have different freshness)
