# O-12 — WhatsApp / SMS Campaign Manager

> **URL:** `/group/marketing/campaigns/messaging/`
> **File:** `o-12-whatsapp-sms-campaign-manager.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P0
> **Role:** Group Admissions Campaign Manager (Role 119, G3) — primary operator

---

## 1. Purpose

The WhatsApp / SMS Campaign Manager handles bulk messaging operations for admission campaigns — the single most cost-effective and highest-reach channel for Indian education groups. A large group like Narayana or Sri Chaitanya sends 5–20 lakh WhatsApp messages and 2–5 lakh SMS per admission season. A small 5-branch trust sends 50,000–2,00,000 messages. WhatsApp has 95%+ penetration among Indian parents, and a well-timed admission broadcast (scholarship exam dates, early-bird fee deadlines, topper results) generates 10–30% of all enquiries.

The problems this page solves:

1. **DLT compliance (TRAI mandate):** Since 2021, every SMS sent in India must use a DLT-registered template with an approved sender ID (entity ID registered on Jio/Vi/Airtel DLT portals). Sending without DLT approval results in message blocking and potential ₹10,000/day penalties. This page stores DLT template IDs, validates every SMS against approved templates, and blocks unapproved content.

2. **WhatsApp Business API management:** WhatsApp Business API (via providers like Gupshup, Wati, Interakt, or Meta's Cloud API) requires pre-approved message templates for outbound business-initiated messages. The platform manages template submission, approval status tracking, and template variable population (student name, branch, fee amount, exam date).

3. **Consent & opt-out (TRAI + DPDPA):** Promotional messages require explicit opt-in consent. The platform tracks consent status per contact, honours opt-out requests ("Reply STOP"), maintains a suppression list, and enforces TRAI's 9 AM–9 PM promotional messaging window. DPDPA (2023) adds data principal consent requirements for personal data usage in marketing.

4. **Contact list management:** Messages target specific segments — past year's enquiries who didn't enroll, current parents for referral asks, new leads from newspaper ads, walk-in parents who haven't returned. The platform builds targeted lists from O-15 (leads), O-17 (walk-ins), and student/parent databases.

5. **Delivery tracking:** Real-time delivery status — sent, delivered, read (WhatsApp blue ticks), failed, bounced. Failed messages trigger retry logic or number validation.

**Scale:** 50,000–20,00,000 messages/season · 5,000–1,00,000 unique contacts · 20–100 DLT templates · 10–50 WhatsApp templates · 5–50 campaigns/season

---

## 2. Role Access

| Role | Role ID | Level | Access | Notes |
|---|---|---|---|---|
| Group Admissions Campaign Manager | 119 | G3 | Full CRUD — create campaigns, manage templates, send broadcasts, view analytics | Primary operator |
| Group Admission Telecaller Executive | 130 | G3 | Send (own queue only) — send individual WhatsApp/SMS to assigned leads | Cannot create bulk campaigns |
| Group Campaign Content Coordinator | 131 | G2 | Read + Upload — manage template content, creative images | Cannot send messages |
| Group Admission Data Analyst | 132 | G1 | Read only — delivery reports, campaign analytics | No send access |
| Group CEO / Chairman | — | G4/G5 | Read + Approve — approve high-volume campaigns (> 10,000 messages) | Approval gate for large blasts |
| Branch Principal | — | G3 | Read (own branch messages only) | Views messages sent to branch contacts |

> **Access enforcement:** `@require_role(min_level=G1, division='O')`. Send operations: role 119 or G4+. Telecallers (130) restricted to individual sends via O-18 integration. Content upload: role 131 or G3+. High-volume campaigns (> configurable threshold) require G4 approval before sending.

---

## 3. Page Layout

### 3.1 Breadcrumb
```
Group HQ  ›  Marketing & Campaigns  ›  Campaign Planning  ›  WhatsApp / SMS Campaign Manager
```

### 3.2 Page Header
```
WhatsApp / SMS Campaign Manager                    [+ New Campaign]  [Manage Templates]  [Contact Lists]  [Export Report]
Campaign Manager — Rajesh Kumar
Sunrise Education Group · Season 2026-27 · 12 active campaigns · 4,82,000 messages sent · 94.2% delivery rate
```

---

## 4. KPI Summary Bar (6 cards)

| # | Card | Metric | Calculation | Colour Rule | HTMX Target |
|---|---|---|---|---|---|
| 1 | Messages Sent (Season) | Integer | COUNT(messages) WHERE season = current AND status IN ('delivered','read') | Static blue | `#kpi-sent` |
| 2 | Delivery Rate | Percentage | (Delivered + Read) / Total Sent × 100 | Green ≥ 90%, Amber 80–90%, Red < 80% | `#kpi-delivery` |
| 3 | Read Rate (WhatsApp) | Percentage | Read / Delivered × 100 (WhatsApp only — blue ticks) | Green ≥ 60%, Amber 40–60%, Red < 40% | `#kpi-read-rate` |
| 4 | Leads Generated | Integer | COUNT(leads) WHERE source = 'whatsapp' OR source = 'sms' (from O-15) | Static green | `#kpi-leads` |
| 5 | Active Campaigns | Integer | COUNT(campaigns) WHERE status = 'active' | Static blue | `#kpi-active` |
| 6 | Opt-outs (This Month) | Integer | COUNT(opt_outs) WHERE month = current | Red > 100, Amber 50–100, Green < 50 | `#kpi-optouts` |

**HTMX:** `hx-get="/api/v1/group/{id}/marketing/campaigns/messaging/kpis/"` → `hx-trigger="load"` → `hx-swap="innerHTML"`

---

## 5. Sections

### 5.1 Tab Navigation

Five tabs:
1. **Campaigns** — All WhatsApp/SMS campaigns with status and metrics
2. **Templates** — DLT and WhatsApp Business template management
3. **Contact Lists** — Audience segments and suppression lists
4. **Delivery Log** — Message-level delivery tracking
5. **Compliance** — Consent status, opt-outs, TRAI/DLT compliance dashboard

### 5.2 Tab 1: Campaigns

**Filter bar:** Channel (WhatsApp / SMS / Both) · Status (Draft / Scheduled / Sending / Completed / Failed / Paused) · Branch · Date Range · Template

**Columns:**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Campaign Name | Text (link) | Yes | Click → campaign detail drawer |
| Channel | Badge | Yes | WhatsApp (green) / SMS (blue) / Both (purple) |
| Template | Text | Yes | Template name used |
| Branch(es) | Text | Yes | Target branches |
| Audience Size | Integer | Yes | Total contacts in list |
| Sent | Integer | Yes | Messages dispatched |
| Delivered | Integer | Yes | Successfully delivered |
| Read | Integer | Yes | Blue-tick read (WhatsApp only; "—" for SMS) |
| Failed | Integer | Yes | Delivery failures |
| Delivery % | Progress bar | Yes | Delivered / Sent |
| Leads | Integer | Yes | Enquiries attributed to this campaign |
| Cost (₹) | Amount | Yes | Total messaging cost |
| Scheduled At | DateTime | Yes | When campaign was/will be sent |
| Status | Badge | Yes | Draft (grey) / Scheduled (blue) / Sending (amber pulse) / Completed (green) / Failed (red) / Paused (amber) |
| Actions | Buttons | No | [View] [Duplicate] [Pause/Resume] |

**Default sort:** Scheduled At DESC
**Pagination:** Server-side · 25/page

### 5.3 Tab 2: Templates

Two sub-tabs: **WhatsApp Templates** and **SMS (DLT) Templates**

#### 5.3.1 WhatsApp Templates

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Template Name | Text | Yes | Internal name |
| Category | Badge | Yes | Marketing / Utility / Authentication |
| Language | Badge | Yes | en / te / hi / ta |
| Header | Text | No | Text / Image / Video / Document / None |
| Body | Text (truncated) | No | Template body with {{variable}} placeholders |
| Footer | Text | No | Optional footer text |
| Buttons | Text | No | CTA buttons (Call / URL / Quick Reply) |
| Status | Badge | Yes | Approved (green) / Pending (amber) / Rejected (red) / Disabled (grey) |
| Last Used | Date | Yes | When last used in a campaign |
| Actions | Buttons | No | [Preview] [Edit] [Submit for Approval] [Delete] |

#### 5.3.2 SMS (DLT) Templates

| Column | Type | Sortable | Notes |
|---|---|---|---|
| Template Name | Text | Yes | Internal name |
| DLT Template ID | Text | Yes | Registered DLT ID (e.g., 1107161234567890123) |
| Entity ID | Text | No | DLT entity registration ID |
| Sender ID | Text | Yes | 6-character sender (e.g., SUNRSE) |
| Category | Badge | Yes | Promotional / Transactional / Service Implicit / Service Explicit |
| Content | Text (truncated) | No | Template text with {#var#} placeholders |
| Status | Badge | Yes | Approved / Pending / Rejected / Expired |
| Registered On | Date | Yes | DLT registration date |
| Expiry | Date | Yes | DLT approval expiry (if applicable) |
| Actions | Buttons | No | [Preview] [Edit] [Re-register] [Delete] |

### 5.4 Tab 3: Contact Lists

**Contact list management — audience segmentation for campaigns.**

| Column | Type | Sortable | Notes |
|---|---|---|---|
| List Name | Text (link) | Yes | E.g., "2025-26 Enquiries — Not Enrolled" |
| Source | Badge | Yes | Manual Upload / Lead Pipeline (O-15) / Walk-in Register (O-17) / Student DB / Parent DB / Custom Query |
| Contact Count | Integer | Yes | Number of valid contacts |
| WhatsApp Eligible | Integer | Yes | Contacts with WhatsApp-capable numbers |
| SMS Eligible | Integer | Yes | Contacts with valid mobile (excluding NDNC for promotional) |
| Consent Status | Badge | Yes | All Consented / Mixed / Unchecked |
| Last Updated | Date | Yes | When list was refreshed |
| Campaigns Used | Integer | No | How many campaigns used this list |
| Actions | Buttons | No | [View] [Refresh] [Export] [Delete] |

**Dynamic lists:** Lists linked to O-15 (lead pipeline) auto-refresh nightly. E.g., "All leads in 'Interested' stage, last contacted > 7 days ago" auto-updates.

**Suppression list:** Global suppression list of contacts who opted out. Applied automatically to every campaign — suppressed contacts are excluded before send.

### 5.5 Tab 4: Delivery Log

Message-level tracking for audit and troubleshooting.

**Filter bar:** Campaign · Channel · Status · Phone Number (search) · Date Range · Branch

| Column | Type | Sortable | Notes |
|---|---|---|---|
| # | Auto-index | No | Row number |
| Phone | Text (masked) | No | +91 XXXXX X1234 (last 4 visible for privacy) |
| Contact Name | Text | Yes | Parent/student name |
| Channel | Badge | Yes | WhatsApp / SMS |
| Campaign | Text | Yes | Campaign name |
| Template | Text | Yes | Template used |
| Sent At | DateTime | Yes | Dispatch timestamp |
| Delivered At | DateTime | Yes | Delivery confirmation timestamp |
| Read At | DateTime | Yes | WhatsApp read receipt timestamp (blank for SMS) |
| Status | Badge | Yes | Sent (blue) / Delivered (green) / Read (dark green) / Failed (red) / Bounced (orange) / Opted Out (grey) |
| Failure Reason | Text | No | If failed: Invalid Number / DND / Template Rejected / Rate Limit / Network Error |
| Cost (₹) | Amount | Yes | Per-message cost |

**Default sort:** Sent At DESC
**Pagination:** Server-side · 50/page (high-volume table)

### 5.6 Tab 5: Compliance

#### 5.6.1 TRAI / DLT Compliance Dashboard

| Metric | Value | Status |
|---|---|---|
| DLT Entity Registration | Active / Expired / Not Registered | Green / Red |
| Sender IDs Registered | N sender IDs | Count |
| Templates Approved | N / M submitted (% approved) | Green ≥ 90% |
| Promotional Time Window | 9 AM – 9 PM enforced | ✅ / ❌ |
| NDNC Scrubbing | Enabled / Disabled | ✅ / ❌ |
| Opt-out Rate (Season) | X% | Green < 2%, Amber 2–5%, Red > 5% |
| Consent Coverage | X% contacts with explicit opt-in | Green ≥ 80%, Amber 50–80%, Red < 50% |

#### 5.6.2 DPDPA Compliance Checklist

| Requirement | Status | Notes |
|---|---|---|
| Purpose of data collection disclosed | ✅ / ❌ | "Marketing communications" purpose must be in consent form |
| Explicit consent obtained | ✅ / ❌ | Per DPDPA Section 6 — consent must be free, specific, informed |
| Consent records stored | ✅ / ❌ | Timestamp + method of consent for each contact |
| Right to withdraw honoured | ✅ / ❌ | Opt-out processed within 7 days (DPDPA requirement) |
| Data retention policy defined | ✅ / ❌ | Marketing contact data retention period set |
| Minor's data (< 18) — guardian consent | ✅ / ❌ | POCSO/DPDPA — student contacts must have parental consent |

#### 5.6.3 Opt-out Management

| Column | Type | Notes |
|---|---|---|
| Phone | Text (masked) | Contact number |
| Name | Text | Contact name |
| Opted Out On | Date | When STOP/opt-out received |
| Source | Badge | Reply STOP / Manual Request / Complaint / NDNC |
| Channel | Badge | WhatsApp / SMS / Both |
| Original Campaign | Text | Which campaign triggered the opt-out |

---

## 6. Drawers & Modals

### 6.1 Modal: `create-messaging-campaign` (640px)

- **Title:** "Create WhatsApp / SMS Campaign"
- **Step 1 — Channel & Template:**
  - Channel (radio): WhatsApp / SMS / Both (sends via both channels)
  - Template (dropdown — from approved templates only; rejected/pending greyed out)
  - Template preview (rendered with sample variables)
  - If WhatsApp with media: upload header image/video/document
- **Step 2 — Audience:**
  - Contact list (dropdown — from Tab 3 lists)
  - Or: Quick filter — Branch + Lead Stage + Date Range → generates dynamic list
  - Audience preview: total contacts, WhatsApp-eligible, SMS-eligible, suppressed (excluded)
  - Estimated reach after suppression and DND removal
- **Step 3 — Variables & Personalisation:**
  - Map template variables to contact fields:
    - `{{1}}` → Student Name / Parent Name
    - `{{2}}` → Branch Name
    - `{{3}}` → Fee Amount / Exam Date / Offer Details
  - Preview with sample contact data
- **Step 4 — Schedule & Review:**
  - Send now / Schedule for later (date + time picker)
  - Time validation: if promotional, must be 9 AM–9 PM (TRAI)
  - Estimated cost: audience × per-message rate
  - Campaign name (auto-generated, editable)
  - Linked campaign from O-08 (optional — for budget tracking)
- **Summary:** Channel · Template · Audience size · Schedule · Cost
- **Buttons:** Cancel · Save as Draft · Schedule · Send Now
- **Validation:**
  - Template must be in "Approved" status
  - Audience must have > 0 eligible contacts after suppression
  - If audience > 10,000 → "Requires G4 approval before sending"
  - If scheduled time is in promotional window violation → block + error
  - If WhatsApp and contact has no WhatsApp → auto-fallback to SMS (if "Both" selected)
- **Access:** Role 119 or G4+

### 6.2 Modal: `create-whatsapp-template` (560px)

- **Title:** "Create WhatsApp Message Template"
- **Fields:**
  - Template name (text, required — lowercase, underscores, e.g., "admission_2026_scholarship")
  - Category (dropdown, required): Marketing / Utility / Authentication
  - Language (dropdown, required): English (en) / Telugu (te) / Hindi (hi) / Tamil (ta) / Bilingual
  - Header (dropdown): None / Text / Image / Video / Document
    - If Text: header text (60 chars max)
    - If Image/Video/Document: sample file upload
  - Body (textarea, required — max 1024 chars)
    - Variable placeholders: `{{1}}`, `{{2}}`, `{{3}}` etc.
    - Bold: `*text*`, Italic: `_text_`, Strikethrough: `~text~`, Monospace: `` `text` ``
    - Sample values for each variable (required for Meta approval)
  - Footer (text, optional — 60 chars max)
  - Buttons (optional, max 3):
    - Quick Reply: button text (20 chars)
    - Call: button text + phone number
    - URL: button text + URL (can include `{{1}}` for dynamic URLs)
- **Preview:** Phone mockup showing rendered template
- **Buttons:** Cancel · Save Draft · Submit to Meta for Approval
- **Note:** Meta approval takes 24–48 hours. Template status updates via webhook.
- **Access:** Role 119 or 131 or G4+

### 6.3 Modal: `create-dlt-template` (560px)

- **Title:** "Register DLT SMS Template"
- **Fields:**
  - Template name (text, required)
  - Sender ID (dropdown — from registered sender IDs, e.g., SUNRSE)
  - Entity ID (auto-filled from group DLT registration)
  - Category (dropdown, required): Promotional / Transactional / Service Implicit / Service Explicit
  - Content (textarea, required)
    - Variables: `{#var#}` format (DLT standard)
    - Max 160 chars per segment (Unicode: 70 chars)
    - Character count + segment count shown live
  - DLT Portal (dropdown): Jio DLT / Vi DLT / Airtel DLT / BSNL DLT
  - DLT Template ID (text — if already registered, paste ID; if new, will be submitted)
- **Preview:** SMS mockup with character/segment count
- **Buttons:** Cancel · Save · Mark as Registered (if ID pasted)
- **Note:** DLT registration is done on operator portals (external). This page stores the approved template for campaign use.
- **Access:** Role 119 or 131 or G4+

### 6.4 Drawer: `campaign-detail` (720px, right-slide)

- **Tabs:** Overview · Delivery Report · Audience · Cost · Responses
- **Overview tab:**
  - Campaign details: name, channel, template (rendered), schedule, status
  - Key metrics: sent, delivered, read, failed, leads generated
  - Timeline: created → scheduled → sending → completed
- **Delivery Report tab:**
  - Delivery funnel: Total → Sent → Delivered → Read → Failed
  - Failure breakdown: Invalid Number / DND / Template Error / Rate Limit / Network
  - Hourly delivery chart (for large campaigns sent over time)
- **Audience tab:**
  - Contact list used, total contacts, eligible, suppressed, NDNC filtered
  - Branch-wise breakdown
- **Cost tab:**
  - Total cost breakdown: WhatsApp messages × rate + SMS segments × rate
  - Per-message cost
  - Linked budget line from O-09
- **Responses tab:**
  - Replies received (WhatsApp — user responses to the broadcast)
  - Opt-outs triggered by this campaign
  - Leads generated (linked to O-15)
  - Click-through rate (if template had URL button)
- **Footer:** [Duplicate] [Pause/Resume] [Download Report] [Archive]

### 6.5 Modal: `manage-contact-list` (640px)

- **Title:** "Create / Edit Contact List"
- **Fields:**
  - List name (text, required)
  - Source (dropdown):
    - **Manual Upload:** Upload CSV/Excel (columns: Name, Phone, Branch, Class/Stream, Tags)
    - **From Lead Pipeline (O-15):** Filter by stage, source, branch, date range
    - **From Walk-in Register (O-17):** Filter by branch, date range, follow-up status
    - **From Student Database:** Current parents (for referral/upsell messages)
    - **Custom Query:** Advanced filter builder (field + operator + value)
  - Auto-refresh (toggle — for dynamic lists): Daily / Weekly / Manual
  - Apply suppression list (toggle, default ON)
  - Apply NDNC filter (toggle, default ON for promotional)
- **Preview:** Sample contacts (first 10), total count, WhatsApp-eligible count, SMS-eligible count
- **Buttons:** Cancel · Save List
- **Access:** Role 119 or G4+

---

## 7. Charts

### 7.1 Delivery Funnel (Horizontal Funnel)

| Property | Value |
|---|---|
| Chart type | Horizontal funnel (CSS/Chart.js) |
| Title | "Message Delivery Funnel — Season [Year]" |
| Stages | Total Queued → Sent → Delivered → Read (WhatsApp) → Lead Generated |
| Colour | Blue → Green → Dark Green → Emerald (progressive) |
| Tooltip | "[Stage]: [N] ([X]% of total)" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/messaging/analytics/delivery-funnel/` |

### 7.2 Channel Performance Comparison (Grouped Bar)

| Property | Value |
|---|---|
| Chart type | Grouped bar (Chart.js 4.x) |
| Title | "WhatsApp vs SMS — Delivery & Read Rates" |
| Data | WhatsApp: delivery %, read %, lead conversion %; SMS: delivery %, lead conversion % |
| Colour | WhatsApp: `#25D366` green; SMS: `#3B82F6` blue |
| Tooltip | "[Channel] — [Metric]: [X]%" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/messaging/analytics/channel-comparison/` |

### 7.3 Monthly Message Volume (Stacked Area)

| Property | Value |
|---|---|
| Chart type | Stacked area (Chart.js 4.x) |
| Title | "Monthly Message Volume — WhatsApp + SMS" |
| Data | Monthly message count, stacked by channel |
| Colour | WhatsApp: `#25D366` green area; SMS: `#3B82F6` blue area |
| Tooltip | "[Month]: WhatsApp [N], SMS [M], Total [N+M]" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/messaging/analytics/monthly-volume/` |

### 7.4 Campaign Cost vs Leads (Scatter)

| Property | Value |
|---|---|
| Chart type | Scatter (Chart.js 4.x) |
| Title | "Campaign Cost vs Leads Generated" |
| Data | Each point = 1 campaign; X = cost (₹), Y = leads generated |
| Colour | Green (above trend — efficient) / Red (below — inefficient) |
| Tooltip | "[Campaign]: ₹[X] spent → [Y] leads (CPL: ₹[Z])" |
| API | `GET /api/v1/group/{id}/marketing/campaigns/messaging/analytics/cost-vs-leads/` |

---

## 8. Toast Messages

| Action | Toast | Type | Duration |
|---|---|---|---|
| Campaign created | "Campaign '[Name]' created — status: Draft" | Success | 3s |
| Campaign scheduled | "Campaign '[Name]' scheduled for [DateTime] — [N] contacts" | Success | 4s |
| Campaign sending | "Campaign '[Name]' is now sending — [N] messages queued" | Info | 3s |
| Campaign completed | "Campaign '[Name]' completed — [N] delivered, [M] failed" | Success | 4s |
| Campaign paused | "Campaign '[Name]' paused — [N] remaining messages held" | Warning | 3s |
| WhatsApp template submitted | "Template '[Name]' submitted to Meta — approval in 24–48 hours" | Info | 4s |
| WhatsApp template approved | "Template '[Name]' approved — ready to use" | Success | 3s |
| WhatsApp template rejected | "Template '[Name]' rejected by Meta: '[Reason]'" | Error | 6s |
| DLT template saved | "DLT template '[Name]' saved — ID: [DLT_ID]" | Success | 3s |
| Contact list created | "Contact list '[Name]' created — [N] contacts, [M] eligible" | Success | 3s |
| Opt-out received | "[N] new opt-outs processed" | Info | 3s |
| Time window violation | "Cannot send promotional messages outside 9 AM – 9 PM (TRAI)" | Error | 5s |
| High-volume approval needed | "Campaign has [N] contacts — requires G4 approval before sending" | Warning | 5s |
| Suppression applied | "[N] contacts suppressed (opt-outs + NDNC)" | Info | 3s |

---

## 9. Empty States

| Condition | Icon | Heading | Description | CTA |
|---|---|---|---|---|
| No messaging campaigns | 💬 | "No Messaging Campaigns" | "Create your first WhatsApp or SMS campaign to reach parents and prospects." | New Campaign |
| No WhatsApp templates | 📝 | "No WhatsApp Templates" | "Create and submit message templates for Meta approval before sending campaigns." | Create Template |
| No DLT templates | 📋 | "No DLT Templates Registered" | "Register your SMS templates on the DLT portal and add them here." | Add DLT Template |
| No contact lists | 👥 | "No Contact Lists" | "Create a contact list from leads, walk-ins, or upload a CSV." | Create Contact List |
| No delivery data | 📊 | "No Delivery Data" | "Message delivery reports will appear here once campaigns are sent." | — |
| No opt-outs | ✅ | "No Opt-outs" | "No contacts have opted out of messaging." | — |

---

## 10. Loader States

| Trigger | Loader Type |
|---|---|
| Initial page load | 6 KPI shimmer cards + tab bar + campaign table skeleton (8 rows) |
| Tab switch | Content area skeleton matching target tab layout |
| Campaign detail drawer | 720px skeleton: metrics bar + delivery funnel placeholder + 5 tabs |
| Template preview | Phone mockup shimmer |
| Contact list load | Table skeleton (10 rows) |
| Delivery log load | 15-row table skeleton (high-volume) |
| Campaign send initiation | Full-width progress bar: "Sending… [N]/[Total]" |
| Chart load | Grey canvas placeholder per chart |

---

## 11. API Endpoints

| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/` | G1+ | List messaging campaigns |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/` | G1+ | Campaign detail |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/` | G3+ | Create campaign |
| PUT | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/` | G3+ | Update campaign |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/send/` | G3+ | Trigger send |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/pause/` | G3+ | Pause campaign |
| PATCH | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/resume/` | G3+ | Resume campaign |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/messaging/{camp_id}/` | G4+ | Delete campaign |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/templates/whatsapp/` | G1+ | List WhatsApp templates |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/templates/whatsapp/` | G2+ | Create WhatsApp template |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/templates/whatsapp/{tid}/submit/` | G3+ | Submit for Meta approval |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/templates/dlt/` | G1+ | List DLT templates |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/templates/dlt/` | G2+ | Add DLT template |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/contacts/` | G1+ | List contact lists |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/contacts/` | G3+ | Create contact list |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/contacts/{list_id}/refresh/` | G3+ | Refresh dynamic list |
| DELETE | `/api/v1/group/{id}/marketing/campaigns/messaging/contacts/{list_id}/` | G3+ | Delete contact list |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/delivery-log/` | G1+ | Delivery log (paginated) |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/compliance/` | G1+ | Compliance dashboard data |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/optouts/` | G1+ | Opt-out list |
| POST | `/api/v1/group/{id}/marketing/campaigns/messaging/optouts/` | G3+ | Manual opt-out entry |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/kpis/` | G1+ | KPI values |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/analytics/delivery-funnel/` | G1+ | Funnel data |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/analytics/channel-comparison/` | G1+ | Channel comparison |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/analytics/monthly-volume/` | G1+ | Monthly volume data |
| GET | `/api/v1/group/{id}/marketing/campaigns/messaging/analytics/cost-vs-leads/` | G1+ | Cost vs leads scatter |

### Webhook Endpoints (Inbound)

| Source | Endpoint | Purpose |
|---|---|---|
| WhatsApp Business API (Gupshup/Wati/Meta) | `/webhooks/whatsapp/delivery/` | Delivery receipts, read receipts |
| WhatsApp Business API | `/webhooks/whatsapp/incoming/` | User replies, opt-out messages |
| SMS Gateway (MSG91/Kaleyra/Gupshup) | `/webhooks/sms/delivery/` | SMS delivery receipts |
| Meta Template Review | `/webhooks/whatsapp/template-status/` | Template approval/rejection notifications |

---

## 12. HTMX Patterns

| Pattern | Trigger | hx-get / hx-post | hx-target | hx-swap | Notes |
|---|---|---|---|---|---|
| KPI load | `<div id="kpi-bar">` | `hx-get=".../messaging/kpis/"` | `#kpi-bar` | `innerHTML` | `hx-trigger="load"` |
| Tab switch | Tab button click | `hx-get=".../messaging/?tab={campaigns/templates/contacts/delivery/compliance}"` | `#messaging-content` | `innerHTML` | `hx-trigger="click"` |
| Filter apply | Filter dropdowns | `hx-get` with filter params | `#messaging-table-body` | `innerHTML` | `hx-trigger="change"` |
| Campaign detail drawer | Row click | `hx-get=".../messaging/{id}/"` | `#right-drawer` | `innerHTML` | `hx-trigger="click"` |
| Create campaign wizard | Step navigation | `hx-get=".../messaging/create/?step={1/2/3/4}"` | `#wizard-content` | `innerHTML` | Multi-step form |
| Send campaign | Send button | `hx-post=".../messaging/{id}/send/"` | `#send-result` | `innerHTML` | Confirmation modal first |
| Template preview | Template select | `hx-get=".../messaging/templates/{tid}/preview/"` | `#template-preview` | `innerHTML` | Phone mockup render |
| Contact list refresh | Refresh button | `hx-post=".../messaging/contacts/{id}/refresh/"` | `#list-count-{id}` | `innerHTML` | Inline count update |
| Delivery log pagination | Page controls | `hx-get` with `?page={n}` | `#delivery-table-body` | `innerHTML` | 50/page |
| Campaign send progress | Polling | `hx-get=".../messaging/{id}/progress/"` | `#send-progress` | `innerHTML` | `hx-trigger="every 5s"` until complete |
| Opt-out webhook update | Server push | — | — | — | Via SSE or polling every 60s |

---

*Page spec version: 1.0 · Last updated: 2026-03-26*
