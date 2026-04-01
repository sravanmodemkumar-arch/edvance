# O-13 — Email Campaign Manager

> **URL:** `/group/marketing/campaigns/email/`
> **File:** `o-13-email-campaign-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The Email Campaign Manager handles bulk email communications for admission campaigns — a supplementary channel to WhatsApp/SMS but important for specific audience segments. In Indian education groups, email penetration among parents is 30–50% (lower than WhatsApp's 95%+), but email is critical for: NRI parent communication (international admissions), corporate-employed parents in Tier-1 cities, alumni engagement, and formal communications (fee structure PDFs, prospectus links, scholarship exam hall tickets).

The problems this page solves:

1. **Professional communication:** Unlike WhatsApp broadcasts which feel personal, email is the channel for formal group-level communications — Chairman's letter to prospective parents, detailed fee structure comparison, prospectus with embedded images, scholarship exam details with attached PDFs. Email allows rich HTML formatting, attachments, and branded templates.

2. **Deliverability management:** Email deliverability in India is challenging — Gmail (dominant provider) aggressively filters bulk education marketing as promotions or spam. The platform manages SPF/DKIM/DMARC authentication, warm-up sequences for new sending domains, bounce handling, and reputation monitoring.

3. **Compliance:** India's IT Act (Section 66A — now read down, but spam provisions remain), DPDPA consent requirements, and CAN-SPAM-like unsubscribe mandates require every email to include: sender identity, physical address, unsubscribe link, and consent basis. The platform enforces these automatically.

4. **Segmented campaigns:** Different email content for different segments — parents of Class 10 students get Jr Inter admission emails, parents of Class 12 get degree programme emails, alumni get referral programme emails, NRI parents get international fee structure emails.

**Scale:** 5,000–50,000 emails/season · 1,000–20,000 unique email contacts · 10–30 campaigns/season · 5–15 email templates

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create campaigns, manage templates, send, view analytics | Primary operator |
| Group Campaign Content Coordinator | 131 | G2 | Read + Edit — design email templates, manage content | Template design only; cannot send |
| Group Admission Data Analyst | 132 | G1 | Read only — open/click analytics, campaign reports | No send access |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve Chairman's letter campaigns | Approval for formal communications |
| Branch Principal | — | G3 | Read (own branch email campaigns) | Views emails sent to branch contacts |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Send operations: role 119 or G4+. Template design: role 131 or G3+.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  Email Campaign Manager
```

### 3.2 Page Header
```
Email Campaign Manager                              [+ New Campaign]  [Email Templates]  [Contact Lists]  [Export]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 8 campaigns sent · 24,200 emails delivered · 32.4% open rate
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Emails Sent (Season) | Integer | COUNT(emails) WHERE season = current AND status = 'delivered' | Static blue | `#kpi-sent` |
| 2 | Open Rate | Percentage | Opened / Delivered × 100 | Green ≥ 25%, Amber 15–25%, Red < 15% | `#kpi-open-rate` |
| 3 | Click Rate | Percentage | Clicked / Delivered × 100 | Green ≥ 5%, Amber 2–5%, Red < 2% | `#kpi-click-rate` |
| 4 | Bounce Rate | Percentage | Bounced / Sent × 100 | Green < 3%, Amber 3–8%, Red > 8% | `#kpi-bounce` |
| 5 | Unsubscribes (Season) | Integer | COUNT(unsubscribes) WHERE season = current | Red > 50, Amber 20–50, Green < 20 | `#kpi-unsubs` |
| 6 | Leads from Email | Integer | COUNT(leads) WHERE source = 'email' (from O-15) | Static green | `#kpi-leads` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/campaigns/email/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Four tabs:
1. **Campaigns** — All email campaigns with metrics
2. **Templates** — Email template design and management
3. **Contact Lists** — Email audience segments
4. **Settings** — Domain authentication, sending configuration

### 5.2 Tab 1: Campaigns

**Filter bar:** Status (Draft / Scheduled / Sent / Failed) · Branch · Date Range · Template

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Campaign Name | Text (link) | Yes | Click → campaign detail drawer |
| Subject Line | Text | Yes | Email subject |
| Template | Text | Yes | Template used |
| Branch(es) | Text | Yes | Target branches |
| Recipients | Integer | Yes | Total email addresses |
| Delivered | Integer | Yes | Successfully delivered |
| Opened | Integer | Yes | Unique opens |
| Clicked | Integer | Yes | Unique clicks |
| Bounced | Integer | Yes | Hard + soft bounces |
| Open % | Progress bar | Yes | Opened / Delivered |
| Click % | Text | Yes | Clicked / Delivered |
| Unsubscribed | Integer | Yes | Unsubscribes from this campaign |
| Sent At | DateTime | Yes | When sent |
| Status | Badge | Yes | Draft / Scheduled / Sending / Sent / Failed |
| Actions | Buttons | No | [View] [Duplicate] [Resend to Unopened] |

**Default sort:** Sent At DESC
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Templates

Card-based grid (3 columns) showing email templates.

**Card layout:**
```
┌─────────────────────────┐
│  [Email Preview Image]  │
│       (300×200 px)      │
│                         │
│  📧 Scholarship Exam    │
│  Type: Marketing        │
│  Last used: 15 Jan 2026 │
│  Open rate: 28%         │
│                         │
│  [Preview] [Edit] [Clone]│
└─────────────────────────┘
```

**Template types:**
- **Admission Announcement** — New session, course offerings
- **Scholarship Exam Invite** — Exam dates, registration link, hall ticket
- **Fee Structure** — Detailed fee breakdown with PDF attachment
- **Prospectus Share** — Digital prospectus link + QR code
- **Topper Showcase** — Results announcement with topper photos
- **Chairman's Letter** — Formal letter from Group Chairman
- **Open Day Invite** — Campus visit RSVP
- **Referral Request** — Parent/alumni referral ask
- **Follow-up** — Enquiry follow-up with branch details

### 5.4 Tab 3: Contact Lists

Shared with O-12 (WhatsApp/SMS) where applicable, but filtered for email-eligible contacts.

| Column | Type | Sortable | Notes |
|---|---|---|---|
| List Name | Text (link) | Yes | Segment name |
| Source | Badge | Yes | Manual Upload / Lead Pipeline / Student DB / Alumni DB |
| Email Count | Integer | Yes | Valid email addresses |
| Verified | Integer | Yes | Email addresses that passed verification |
| Invalid/Bounced | Integer | Yes | Known invalid addresses (from prior bounces) |
| Consent | Badge | Yes | All Consented / Mixed / Unchecked |
| Last Updated | Date | Yes | When refreshed |
| Actions | Buttons | No | [View] [Refresh] [Export] [Delete] |

### 5.5 Tab 4: Settings

#### 5.5.1 Sending Domain Configuration

| Setting | Value | Status |
|---|---|---|
| Sending domain | mail.sunriseedu.com | ✅ Verified |
| From Name | "Sunrise Education Group" | — |
| From Email | admissions@sunriseedu.com | — |
| Reply-To | admissions@sunriseedu.com | — |
| SPF Record | ✅ Valid | Green |
| DKIM Record | ✅ Valid | Green |
| DMARC Policy | p=quarantine | Amber (recommend p=reject) |
| Sender Reputation | 85/100 | Green ≥ 80, Amber 60–80, Red < 60 |

#### 5.5.2 Sending Limits

| Setting | Value | Notes |
|---|---|---|
| Daily sending limit | 10,000 emails/day | Based on domain warm-up stage |
| Warm-up stage | Stage 3 (of 5) | Auto-progresses based on engagement |
| Throttle rate | 500/hour | Prevents spam flags |
| Retry on soft bounce | 3 attempts over 48 hours | Auto-retry logic |

#### 5.5.3 Footer Configuration

Mandatory footer content (auto-appended to every email):

```
---
Sunrise Education Group
Registered Office: Plot 45, Jubilee Hills, Hyderabad 500033, Telangana
Phone: 040-XXXXXXXX | Email: admissions@sunriseedu.com
You received this email because you enquired about admissions at Sunrise Education Group.
[Unsubscribe] | [Update Preferences] | [View in Browser]
```

---

## 6. Drawers & Modals

### 6.1 Modal: `create-email-campaign` (720px)

- **Title:** "Create Email Campaign"
- **Step 1 — Setup:**
  - Campaign name (text, required)
  - Subject line (text, required — 60 chars recommended; 150 max)
  - Preview text (text, optional — 90 chars; shows in inbox preview)
  - From name (pre-filled, editable)
  - Reply-to (pre-filled, editable)
  - Template (dropdown — from approved templates)
  - Linked campaign from O-08 (optional)
- **Step 2 — Content:**
  - Email builder (WYSIWYG editor or HTML code editor toggle)
  - Personalisation variables: `{{parent_name}}`, `{{student_name}}`, `{{branch_name}}`, `{{class}}`, `{{fee_amount}}`
  - Attachments (up to 3 files, max 5 MB each — PDF prospectus, fee structure, hall ticket)
  - Image uploads (hosted on Cloudflare R2; auto-converted to CDN URLs)
- **Step 3 — Audience:**
  - Contact list (dropdown)
  - Or: quick segment from Lead Pipeline / Student DB
  - Audience preview: total, email-verified, invalid excluded
  - A/B test option: split audience 50/50, different subject lines
- **Step 4 — Schedule & Review:**
  - Send now / Schedule (date + time)
  - Send preview to self / test email
  - Summary: recipients, subject, template, schedule
- **Buttons:** Cancel · Save Draft · Send Test · Schedule · Send Now
- **Access:** Role 119 or G4+

### 6.2 Modal: `email-template-editor` (Full-screen overlay)

- **Title:** "Design Email Template"
- **Editor:** Drag-and-drop block editor (similar to Mailchimp/Brevo)
  - **Blocks:** Header (logo + tagline) / Text / Image / Button / Divider / Columns (2 or 3) / Footer / Social Links / Attachment Download
  - **Styling:** Background colour, font family (limited to web-safe), font size, padding, border
  - **Brand preset:** Auto-loads group logo, brand colours, fonts from O-02 (Brand Standards)
  - **Mobile responsive:** Auto-responsive layout; mobile preview toggle
- **Sections:**
  - Left panel: Block library (drag to canvas)
  - Centre: Email canvas (desktop preview, 600px wide)
  - Right panel: Block properties (styling, content editing)
  - Top bar: [Desktop Preview] [Mobile Preview] [HTML Code] [Send Test]
- **Buttons:** Cancel · Save Template · Save & Use in Campaign
- **Access:** Role 131 (Content Coordinator) or 119 or G4+

### 6.3 Drawer: `campaign-detail` (720px, right-slide)

- **Tabs:** Overview · Engagement · Recipients · Links · Bounces
- **Overview tab:**
  - Campaign details, subject, template preview, send date
  - Key metrics: delivered, opened, clicked, bounced, unsubscribed
  - Delivery timeline: queued → sending → delivered (with timestamps)
- **Engagement tab:**
  - Open rate over time (line chart — hourly for first 48 hours, then daily)
  - Click heatmap on email body (which links got most clicks)
  - Device breakdown: Desktop vs Mobile vs Tablet opens
  - Email client breakdown: Gmail / Outlook / Yahoo / Apple Mail / Other
- **Recipients tab:**
  - Searchable list of all recipients with status: Delivered / Opened / Clicked / Bounced / Unsubscribed
  - Filter by status
- **Links tab:**
  - All links in the email with click counts
  - Unique clicks vs total clicks
  - Top-performing CTA button
- **Bounces tab:**
  - Hard bounces (invalid email — permanently remove from list)
  - Soft bounces (mailbox full, temporary — retry)
  - Bounce rate by domain (e.g., gmail.com 2%, yahoo.com 8%)
- **Footer:** [Duplicate] [Resend to Unopened] [Download Report] [Archive]

---

## 7. Charts

### 7.1 Open & Click Rate Trend (Line)

| Property | Value |
|---|---|
| Chart type | Dual-line (Chart.js 4.x) |
| Title | "Email Open & Click Rates — Last 12 Campaigns" |
| Data | Per campaign: open rate (line 1) + click rate (line 2) |
| Colour | Open: `#3B82F6` blue; Click: `#10B981` green |
| X-axis | Campaign name / date |
| Y-axis | Percentage |
| Tooltip | "[Campaign]: Open [X]%, Click [Y]%" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/email/analytics/rate-trend/` |

### 7.2 Engagement by Time of Day (Heatmap)

| Property | Value |
|---|---|
| Chart type | Heatmap grid (CSS/Chart.js matrix) |
| Title | "Best Send Times — Opens by Day & Hour" |
| Data | 7 rows (Mon–Sun) × 12 columns (8 AM–8 PM, 1-hour blocks) |
| Colour | White (0 opens) → Light Blue → Dark Blue (peak opens) |
| Purpose | Identify optimal send time for this group's audience |
| API | `GET /api/v1/group/{id}/marketing/campaigns/email/analytics/engagement-heatmap/` |

### 7.3 Bounce Rate by Domain (Bar)

| Property | Value |
|---|---|
| Chart type | Horizontal bar (Chart.js 4.x) |
| Title | "Bounce Rate by Email Domain" |
| Data | Per domain (gmail.com, yahoo.com, etc.): bounce % |
| Colour | Green < 3%, Amber 3–8%, Red > 8% |
| API | `GET /api/v1/group/{id}/marketing/campaigns/email/analytics/bounce-by-domain/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign created | "Email campaign '[Name]' created — status: Draft" | Success | 3s |
| Campaign scheduled | "Email campaign scheduled for [DateTime] — [N] recipients" | Success | 4s |
| Campaign sent | "Email campaign '[Name]' sent — [N] delivered" | Success | 4s |
| Test email sent | "Test email sent to [email] — check your inbox" | Info | 3s |
| Template saved | "Email template '[Name]' saved" | Success | 3s |
| Resend to unopened | "Resending to [N] recipients who haven't opened" | Info | 4s |
| Bounce alert | "[N] hard bounces detected — addresses removed from list" | Warning | 5s |
| Unsubscribe | "[N] unsubscribes processed from campaign '[Name]'" | Info | 3s |
| Domain verification | "Domain [domain] verified — SPF/DKIM/DMARC all passing" | Success | 4s |
| Sending limit reached | "Daily sending limit reached ([N]/day) — remaining emails queued for tomorrow" | Warning | 5s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No email campaigns | 📧 | "No Email Campaigns" | "Create your first email campaign to reach parents and prospects." | New Campaign |
| No templates | 🎨 | "No Email Templates" | "Design an email template before creating campaigns." | Create Template |
| No contact lists | 👥 | "No Email Lists" | "Import email contacts or create a list from existing leads." | Create Contact List |
| No engagement data | 📊 | "No Engagement Data" | "Open and click data will appear after your first campaign is sent." | — |
| Domain not verified | ⚠️ | "Sending Domain Not Configured" | "Set up SPF, DKIM, and DMARC for your sending domain to start sending." | Configure Domain |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar + campaign table skeleton (8 rows) |
| Tab switch | Content area skeleton |
| Template grid load | 6 card-shaped shimmer blocks |
| Template editor load | Full-screen overlay with canvas placeholder |
| Campaign detail drawer | 720px skeleton: metrics summary + 5 tab placeholders |
| Email preview render | Grey rectangle with "Loading preview…" |
| Chart load | Grey canvas placeholder |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/campaigns/email/` | G1+ | List email campaigns |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/` | G1+ | Campaign detail |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/` | G3+ | Create campaign |
| PUT | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/` | G3+ | Update campaign |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/send/` | G3+ | Trigger send |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/send-test/` | G3+ | Send test email |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/resend-unopened/` | G3+ | Resend to unopened |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/email/{camp_id}/` | G4+ | Delete campaign |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/templates/` | G1+ | List templates |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/templates/` | G2+ | Create template |
| PUT | `/api/v1/group/{id}/marketing/campaigns/email/templates/{tid}/` | G2+ | Update template |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/email/templates/{tid}/` | G3+ | Delete template |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/contacts/` | G1+ | List email contact lists |
| POST | `/api/v1/group/{id}/marketing/campaigns/email/contacts/` | G3+ | Create contact list |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/settings/` | G3+ | Domain and sending settings |
| PUT | `/api/v1/group/{id}/marketing/campaigns/email/settings/` | G4+ | Update settings |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/analytics/rate-trend/` | G1+ | Rate trend data |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/analytics/engagement-heatmap/` | G1+ | Time heatmap |
| GET | `/api/v1/group/{id}/marketing/campaigns/email/analytics/bounce-by-domain/` | G1+ | Bounce data |

### Webhook Endpoints (Inbound)

| Source | Endpoint | Purpose |
|---|---|---|
| Email Service Provider (SES/SendGrid/Brevo) | `/webhooks/email/delivery/` | Delivery, bounce, complaint events |
| Email Service Provider | `/webhooks/email/engagement/` | Open, click events |
| Unsubscribe handler | `/webhooks/email/unsubscribe/` | One-click unsubscribe (RFC 8058) |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../email/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab click | `hx-get=".../email/?tab={campaigns/templates/contacts/settings}"` | `#email-content` | `innerHTML` | `hx-trigger="click"` |
| Campaign detail drawer | Row click | `hx-get=".../email/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create campaign wizard | Step nav | `hx-get=".../email/create/?step={1/2/3/4}"` | `#wizard-content` | `innerHTML` | Multi-step |
| Send campaign | Send button | `hx-post=".../email/{id}/send/"` | `#send-result` | `innerHTML` | Confirm first |
| Send test | Test button | `hx-post=".../email/{id}/send-test/"` | `#test-result` | `innerHTML` | Inline toast |
| Template preview | Card click | `hx-get=".../email/templates/{id}/preview/"` | `#template-preview-modal` | `innerHTML` | Modal render |
| Pagination | Page controls | `hx-get` with `?page={n}` | `#email-table-body` | `innerHTML` | Table body |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
