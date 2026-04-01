# Module 37 — Email (AWS SES)

## 1. Purpose

Module 37 manages all institutional email communication through AWS Simple Email Service (SES) — from transactional emails (fee receipts, admit cards, offer letters) through operational emails (PTM summaries, report cards), bulk announcements, and formal regulatory documents. It ensures high deliverability, sender reputation management, DPDPA-compliant consent handling, and full tracking (open, click, bounce, complaint).

Module 37 is the email channel module delegated to by Module 35 (Notifications). It does not decide what to send; it receives dispatch instructions from Module 35 and executes. The module integrates with Module 25 (Fee Collection), Module 19 (Exam Session), Module 21 (Results), Module 31 (Admission), Module 33 (PTM), Module 34 (Announcements), Module 35 (Notifications), Module 39 (Certificates & TC), Module 42 (Audit Log), and Cloudflare R2 for attachment storage.

---

## 2. AWS SES Configuration

### 2.1 Account Architecture

| Setting | Value |
|---------|-------|
| Primary SES region | ap-south-1 (Mumbai) — India data residency |
| Failover region | ap-southeast-1 (Singapore) |
| Account type | Multi-tenant shared (small institutions) / Dedicated account (large institutions > 50k emails/month) |
| Sending mode | API (not SMTP) |
| Configuration set | Per tenant; enables per-tenant event tracking |

### 2.2 Domain & Identity Verification

Each institution's sending domain verified in SES:

| Record | Type | Purpose |
|--------|------|---------|
| DKIM 1/2/3 | CNAME | 2048-bit RSA signing; auto-rotated annually |
| SPF | TXT | `v=spf1 include:amazonses.com ~all` |
| DMARC | TXT | `v=DMARC1; p=quarantine; rua=mailto:dmarc@institution.edu.in` |
| Custom MAIL FROM | MX + TXT | `mail.institution.edu.in` for DMARC alignment |

DMARC progression: start with `p=none` (monitoring) → `p=quarantine` → `p=reject` as domain reputation builds over 60 days.

### 2.3 Sending Identities

| From Address | Purpose |
|-------------|---------|
| `noreply@institution.edu.in` | System emails, OTP, password reset |
| `fees@institution.edu.in` | Fee receipts, payment reminders |
| `admissions@institution.edu.in` | Offer letters, application status |
| `results@institution.edu.in` | Result notifications, report cards |
| `principal@institution.edu.in` | Formal letters, suspension, expulsion |
| `events@institution.edu.in` | Event invitations, announcements |

All from-addresses verified in SES. Reply-to set to functional mailbox monitored by admin.

### 2.4 Dedicated IP (High-Volume Institutions)

For institutions sending > 1 lakh emails/month:
- Dedicated sending IP allocated from SES dedicated IP pool
- IP warmup schedule: 25 → 100 → 500 → 2,000 → 10,000 → 50,000/day over 6 weeks
- IP reputation isolated from other EduForge tenants
- Blacklist monitoring: daily check against Spamhaus, Barracuda, MX Toolbox
- Fallback: if dedicated IP blacklisted → temporary switch to shared pool + remediation

### 2.5 Bounce & Complaint Handling

SES publishes events to SNS → Lambda processes:
- Hard bounce (invalid address) → address suppressed immediately; contact record flagged in Module 07/09
- Soft bounce (mailbox full, server unavailable) → retry: 1 hour, 4 hours, 24 hours (3 retries); then suppress
- Complaint (ISP feedback loop) → address suppressed; admin alerted; frequency/content review triggered
- SES account-level suppression list synced with Module 37 suppression list

### 2.6 SES Sending Limits

| Limit | Default | Notes |
|-------|---------|-------|
| Sending rate | 200 messages/second | SES default; can be increased |
| Daily quota | 50,000 (production) | Increased on request |
| Maximum message size | 40 MB | Including attachments |

Module 37 manages per-tenant rate limits within SES totals. Bulk sends batched to respect 200/sec limit.

---

## 3. Email Types & Templates

### 3.1 Email Tiers

| Tier | Examples | Consent Required | Unsubscribe |
|------|---------|-----------------|------------|
| Transactional | Fee receipt, OTP, admit card, TC | No | No (legally required communication) |
| System | Password reset, login alert, security notification | No | No |
| Operational | PTM summary, report card, assignment notification | Implicit (service relationship) | Yes |
| Formal document | Offer letter, suspension letter, academic warning | No (statutory) | No |
| Promotional | Event invitations, scholarship notices, open house | Yes | Yes (mandatory) |

### 3.2 HTML Email Templates

Each template:
- Responsive HTML (tested across Gmail, Outlook, Apple Mail, Yahoo)
- Plain-text fallback (multipart/alternative MIME structure)
- Institution branding: logo URL, primary colour, font family — from tenant settings
- Header: institution logo + name
- Body: personalised content with variable substitution
- Footer: institution address, phone, website, unsubscribe link, privacy policy link
- Preview text: configured per template; shown in inbox before opening

### 3.3 Template Variables

Substituted at dispatch time from event payload:

| Variable | Source |
|----------|--------|
| `{{recipient_name}}` | Module 07/09 |
| `{{student_name}}` | Module 07 |
| `{{institution_name}}` | Tenant settings |
| `{{institution_logo_url}}` | Tenant settings → R2 URL |
| `{{amount}}` | Module 25 invoice |
| `{{due_date}}` | Module 25 |
| `{{exam_name}}` | Module 19 |
| `{{exam_date}}` | Module 19 |
| `{{venue}}` | Module 19 |
| `{{result_link}}` | Module 21 |
| `{{offer_letter_link}}` | Module 31 / R2 |
| `{{payment_link}}` | Module 25 |
| `{{unsubscribe_link}}` | Module 37 (generated per recipient) |

### 3.4 Attachment Handling

- PDFs generated by WeasyPrint in relevant modules (fee receipt, admit card, report card, TC)
- Stored in Cloudflare R2 with pre-signed URL (7-day validity)
- Email body: "Your [document] is attached. You can also view it here: [R2 link]"
- Attachment in email: PDFs < 2 MB attached directly; PDFs > 2 MB linked from R2 (reduces SES bandwidth cost)
- SES maximum message size: 40 MB (generous for PDF attachments)

### 3.5 List-Unsubscribe Header

Per Gmail/Yahoo 2024 bulk sender requirements:
- `List-Unsubscribe: <mailto:unsub@mail.institution.edu.in?subject=unsub_{{token}}>, <https://app.institution.edu.in/unsubscribe/{{token}}>`
- `List-Unsubscribe-Post: List-Unsubscribe=One-Click`
- Enables one-click unsubscribe directly from Gmail/Yahoo inbox
- Unsubscribe processed within 10 seconds; Module 35 opt-out updated

---

## 4. Deliverability Management

### 4.1 Email Authentication Stack

All three layers configured:

```
SPF: v=spf1 include:amazonses.com ~all
DKIM: 2048-bit RSA; signed on all outbound messages
DMARC: p=quarantine; pct=100; rua=mailto:dmarc-reports@institution.edu.in
```

DMARC aggregate reports (rua): weekly XML report from receiving ISPs; processed to show pass/fail rates.
DMARC forensic reports (ruf): per-message failure reports; used for debugging spoofing attempts.

### 4.2 Sender Reputation Monitoring

| Tool | Metric Monitored | Alert Threshold |
|------|-----------------|----------------|
| Google Postmaster Tools | Domain reputation, IP reputation, spam rate | Reputation drops to Medium |
| SES Dashboard | Bounce rate, complaint rate | Bounce > 2%; Complaint > 0.1% |
| Blacklist check (daily) | IP + domain vs Spamhaus/Barracuda/MXToolbox | Any listing |
| DMARC report | Pass rate | Pass rate < 95% |

Alerts: email to admin + push notification to Platform Ops (Module 35).

### 4.3 Email Warmup Protocol

New sending domain / dedicated IP:

| Week | Max Daily Volume | ISPs Targeted First |
|------|-----------------|-------------------|
| 1 | 25–100 | Gmail (highest volume) |
| 2 | 100–500 | Gmail + Yahoo |
| 3 | 500–2,000 | Gmail + Yahoo + Outlook |
| 4 | 2,000–10,000 | All ISPs |
| 5 | 10,000–50,000 | All ISPs |
| 6+ | Full volume | All ISPs |

Warmup sends: only to most-engaged users first (those who have previously opened/clicked emails).

### 4.4 Bounce Management

| Bounce Type | Action |
|------------|--------|
| Hard bounce (5.1.1) | Immediate suppression; contact flagged in Module 07/09 |
| Hard bounce (5.1.2 — domain not found) | Immediate suppression; contact flagged |
| Soft bounce (4.2.1 — mailbox full) | Retry 3× over 24 hours; then suppress if persistent |
| Soft bounce (4.4.7 — message delay) | Retry 3× over 48 hours |
| Transient bounce | Retry with backoff; max 72 hours |

Bounce rate tracking:
- Institution-level bounce rate: total bounces ÷ total sends × 100%
- Target < 2%; above 2% → sending paused; suppression list reviewed
- Bounce spike alert: if bounce rate > 5% on any single send → immediate pause + admin alert

### 4.5 Complaint Handling

- SES FBL (Feedback Loop) integrated with Gmail/Yahoo/Outlook
- Complaint (mark as spam) → subscriber suppressed within 30 seconds
- Complaint rate: target < 0.1%; above 0.3% → immediate review
- High-complaint template → paused; content/frequency reviewed
- Complaint trend: weekly trend per template; rising trend = early warning

---

## 5. Tracking & Analytics

### 5.1 Event Tracking Architecture

SES CloudWatch event streams → Lambda → Module 37 database:

| SES Event | Module 37 Action |
|-----------|----------------|
| Send | Record created |
| Delivery | Delivery timestamp stored |
| Open | Open timestamp; device/client parsed |
| Click | Link + timestamp stored |
| Bounce | Address suppressed; reason stored |
| Complaint | Address suppressed; admin alerted |
| Rendering failure | Admin alerted; template reviewed |

All events processed within 30 seconds of SES publishing them.

### 5.2 Open Tracking

- 1×1 transparent PNG pixel (`/track/open/{{message_id}}.png`) embedded in HTML email
- Pixel request → Module 37 logs open; returns 1×1 transparent PNG
- Apple Mail Privacy Protection (MPP): Apple auto-downloads images in iOS 15+ Mail, causing false opens
  - MPP detection: if open occurs within 5 seconds of delivery AND from Apple Mail user-agent → flagged as probable MPP open; not counted as genuine engagement
  - Module 37 reports: MPP-adjusted open rate (more accurate) alongside raw open rate

### 5.3 Click Tracking

- All links in email body rewritten: `https://original.com/page` → `https://track.institution.edu.in/r/{{message_id}}/{{link_id}}`
- Click → Module 37 records click → 302 redirect to original URL
- Click latency: redirect must complete in < 300ms to avoid user-perceived delay
- Unsubscribe link: click tracked and also triggers opt-out immediately
- PDF attachment link (R2 pre-signed): click tracked via same redirect mechanism

### 5.4 Per-Email Analytics

| Metric | Description |
|--------|-------------|
| Sent | Accepted by SES |
| Delivered | Confirmed delivered by receiving server |
| Delivery rate | Delivered ÷ Sent × 100% |
| Opened | Unique opens (MPP-adjusted) |
| Open rate | Opened ÷ Delivered × 100% |
| Clicked | Unique clicks |
| CTR | Clicked ÷ Delivered × 100% |
| CTOR | Clicked ÷ Opened × 100% (click-to-open ratio) |
| Bounced | Hard + soft bounces |
| Complained | Spam complaints |
| Unsubscribed | Via unsubscribe link |

### 5.5 Engagement Segmentation

| Segment | Definition | Email Strategy |
|---------|-----------|---------------|
| Highly engaged | > 50% open rate last 30 days | Full email cadence |
| Moderately engaged | 20–50% open rate | Normal cadence |
| Low engagement | < 20% open rate | Reduce frequency; test subject lines |
| Dormant | No open in 90 days | Re-engagement email → if no open in 14 days → suppress email; shift to WhatsApp/SMS |
| Bounced | Hard bounce | No email; alternative contact |

---

## 6. Formal Document Emails

### 6.1 Fee Receipt Email

Triggered by Module 25 (payment confirmed):
- From: `fees@institution.edu.in`
- Subject: "Payment Receipt — ₹[amount] — [Student Name]"
- Body: payment summary (date, amount, head, balance if any)
- Attachment: fee receipt PDF (WeasyPrint; < 500 KB typical)
- SES message ID stored in Module 25 for reconciliation
- Delivery confirmation: tracked; admin alert if delivery fails within 10 minutes

### 6.2 Offer Letter Email

Triggered by Module 31 (selection confirmed):
- From: `admissions@institution.edu.in`
- Subject: "Offer Letter — [Course] — [Institution Name]"
- Body: congratulations; key details; instructions; acceptance deadline
- Attachment: offer letter PDF
- CTA button: "Accept Offer" (deep link to Module 31 acceptance screen)
- Acceptance tracking: Module 31 tracks; email engagement shows if candidate opened + clicked

### 6.3 Report Card Email

Triggered by Module 21 (report card generated):
- From: `results@institution.edu.in`
- Subject: "[Student Name]'s Report Card — [Exam] — [AY]"
- Body: key subject scores (top-level summary); overall percentage; rank
- Attachment: full report card PDF
- Parents and student both receive (separate personalised emails)

### 6.4 Admit Card Email

Triggered by Module 19:
- From: `results@institution.edu.in`
- Subject: "Admit Card — [Exam Name] — [Date]"
- Body: exam date, time, venue, instructions; "Do not forget to bring this admit card"
- Attachment: admit card PDF
- Reminder email: D-1 before exam (no attachment; just reminder + app link)

### 6.5 Academic Warning / Suspension / Expulsion Letter

Triggered by Module 33 / Principal action:
- From: `principal@institution.edu.in`
- Subject: "Important — Academic Notice for [Student Name]"
- Formal tone; PDF attached (Principal-signed digital signature)
- Delivery confirmation: tracked; if no delivery in 1 hour → admin alerted; SMS fallback sent
- Legal hold flag: if disciplinary email → flagged for 7-year retention (legal reference)

### 6.6 Transfer Certificate (TC) Email

Triggered by Module 39:
- Formal email with TC PDF attached
- Unique TC number in subject
- Sent to student + parent
- Acknowledgement tracked

---

## 7. Bulk Email Management

### 7.1 Campaign Workflow

```
Admin creates campaign: template + audience + subject + schedule
  → Suppression check: exclude bounced + unsubscribed addresses
  → Delivery preview: recipient count + sample personalised preview
  → Test send: to 5 admin addresses for quality check
  → Approval (if required: Principal for announcements)
  → Scheduled dispatch: SQS-queued; batched at 200/sec
  → Real-time tracking: open/click/bounce/unsubscribe dashboard
  → Completion report: full analytics summary
```

### 7.2 Frequency Capping

- Promotional emails: max 1/day + max 3/week per recipient
- Operational emails: max 2/day per recipient
- Transactional emails: no cap (triggered by action; not marketing)
- System emails: no cap

Cap enforced at Module 35 level; Module 37 simply dispatches what Module 35 approves.

### 7.3 Re-send to Non-Openers

For Important campaigns:
- 48 hours after initial send → identify non-openers (not opened; not bounced)
- Re-send with different subject line (A/B subject test retrospectively)
- One re-send maximum per campaign; excessive re-sends increase unsubscribe risk
- Re-send analytics tracked separately from initial send

### 7.4 Email Personalisation at Scale

- Every email in a bulk send is personalised: recipient's name, student's name, relevant data points
- Personalisation done at send time (not pre-generated): variable substitution from database query per recipient
- No "Dear Parent/Student" generic emails; every recipient addressed by name
- Personalisation improves open rate 20–30% vs generic

---

## 8. Compliance

### 8.1 DPDPA Compliance

- Email address = personal data; communication history = personal data
- Consent for promotional emails: stored per user (timestamp, consent text, channel)
- Transactional/system emails: lawful basis = contract performance; no consent required
- Data subject rights: user can request email history → exported from Module 42
- Deletion: email content records anonymised on deletion request; delivery metadata retained for audit (1 year)
- Data localisation: SES ap-south-1 (Mumbai) used; data does not leave India for primary processing

### 8.2 Email Retention Policy

| Email Type | Retention Period | Reason |
|-----------|-----------------|--------|
| Fee receipt | 7 years | Income Tax, GST audit |
| TC, migration certificate | Permanent | Institutional records |
| Suspension / expulsion | 7 years | Legal reference |
| Offer letter | 3 years | Admission audit |
| OTP / login alert | 90 days | Security audit |
| Promotional | 1 year | Opt-out audit |
| System / operational | 1 year | General audit |

After retention period: content archived (anonymised); delivery metadata retained in Module 42.

### 8.3 Children's Email Policy

- Students under 13: emails sent only to parent's email address (from Module 09 profile)
- Students 13–18: academic/results emails to both student + parent; counselling-related to student only
- Age derived from Module 07 DOB

### 8.4 CAN-SPAM / DPDPA Equivalent

Indian equivalent requirements met:
- Physical address in every promotional email footer
- Unsubscribe mechanism functional within 10 seconds
- No deceptive subject lines
- Sender identity clear (institution name in From display name)
- Unsubscribe requests honoured within 10 business days (DPDPA guidance; Module 37 honours within seconds)

---

## 9. Cost Management

### 9.1 SES Pricing

| Component | Cost |
|-----------|------|
| Outgoing email | $0.10 per 1,000 emails |
| Attachment data transfer | $0.12 per GB |
| Dedicated IP | $24.95 per IP per month |
| CloudWatch logs | $0.50 per GB ingested |

At 5 crore students (hypothetical full platform): roughly ₹50,000–₹1,00,000/month for email (within ₹0.60/student/year cost target).

### 9.2 Cost Optimisation

- Large PDF attachments (> 2 MB): linked from R2 (pre-signed URL) instead of attached; saves SES bandwidth cost
- Dormant users: email suppressed; WhatsApp/SMS used instead (no SES cost, but WhatsApp has per-message cost)
- HTML vs plain text: plain-text emails for OTP/system (no images, no tracking overhead, lowest size)
- Deduplication: bulk send dedup key prevents accidental double-sends; cost contained

### 9.3 Cost Dashboard

- Monthly SES spend: emails sent × rate + attachment data
- Per-module cost attribution: fee emails vs result emails vs announcements vs admissions
- Cost per student per month
- Cost trend: month-on-month; anomaly alert if cost spikes > 20%

---

## 10. Integration Map

| Module | Integration |
|--------|------------|
| Module 19 — Exam Session | Admit card PDF delivery; exam reminder |
| Module 21 — Results | Report card PDF; result notification |
| Module 25 — Fee Collection | Fee receipt PDF; payment reminder |
| Module 31 — Admission | Offer letter; application status updates |
| Module 33 — PTM | PTM summary; academic warning letter |
| Module 34 — Announcements | Bulk announcement emails; circular distribution |
| Module 35 — Notifications | All email dispatches received from Module 35 |
| Module 39 — Certificates & TC | TC email delivery |
| Module 42 — DPDPA & Audit Log | All send events, opens, clicks, bounces audited |
| Cloudflare R2 | PDF attachment storage and pre-signed URL delivery |

---

## 11. Data Model (Key Tables)

```
email_sending_identities
  id, tenant_id, from_address, display_name, purpose,
  ses_identity_arn, dkim_status, spf_status, dmarc_status,
  is_active, created_at

email_templates
  id, tenant_id, template_code, subject_pattern,
  html_body, plain_text_body, from_identity_id,
  has_attachment, attachment_source_module,
  list_unsubscribe_enabled, is_transactional, version,
  is_active, created_at

email_sends
  id, tenant_id, recipient_email, user_id, user_type,
  template_id, subject, ses_message_id, from_address,
  sent_at, status, attachment_r2_keys

email_events
  id, email_send_id, event_type, timestamp, bounce_type,
  bounce_subtype, complaint_feedback_type, click_link,
  open_device_type, open_email_client, user_agent,
  is_mpp_probable

email_suppressions
  id, tenant_id, email_address, reason, suppressed_at,
  bounce_type, complaint_type, manually_added, removed_at

email_opt_outs
  id, user_id, user_type, email_address, category,
  opted_out_at, opted_back_in_at, method

email_campaigns
  id, tenant_id, name, template_id, subject,
  audience_type, audience_ids_json, scheduled_at,
  sent_at, status, total_recipients, delivered,
  opened, clicked, bounced, complained, unsubscribed,
  cost_usd

email_deliverability_logs
  id, tenant_id, date, domain_reputation,
  ip_reputation, bounce_rate, complaint_rate,
  dmarc_pass_rate, blacklist_status, recorded_at
```

---

## Cross-Module References

- **Module 19**: Admit card delivery; exam reminder emails — event write
- **Module 21**: Report card email; result notification — event write
- **Module 25**: Fee receipt delivery; payment reminder — event write
- **Module 31**: Offer letter; application status update emails — event write
- **Module 33**: PTM summary; academic warning letter — event write
- **Module 34**: Bulk announcement and circular emails — event write
- **Module 35**: All email dispatches orchestrated by Module 35 — write (receives requests)
- **Module 39**: TC email delivery — event write
- **Module 42**: All send events, opt-out, delivery status audited — write
- **Cloudflare R2**: PDF attachments stored; pre-signed URL in email — read

---

*Module 37 complete. Next: Module 38 — SMS & OTP.*
