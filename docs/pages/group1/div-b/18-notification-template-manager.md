# Page 18 — Notification Template Manager

**URL:** `/portal/product/notification-templates/`
**Permission:** `product.manage_notification_templates`
**Priority:** P2
**Roles:** PM Institution Portal, PM Platform, UI/UX Designer

---

## Purpose

Central management system for all notification templates across every channel the platform uses to communicate with students, institution admins, and parents. Covers in-app notifications, push notifications (FCM), SMS, WhatsApp, and email. Every automated message that leaves the platform — from an exam reminder to a password reset — is defined and tested here before going live.

Core responsibilities:
- Define and version all notification templates per channel
- Control which events trigger which notifications
- Configure delivery rules (timing, conditions, throttling)
- Preview and test templates across channels
- Measure notification performance (delivery rate, open rate, click rate, opt-out rate)
- Manage student opt-out preferences and suppression lists
- Ensure DPDPA 2023 compliance for all notifications containing student personal data

**Scale:**
- 2.4M–7.6M students as potential recipients
- 60+ distinct notification event types
- 5 channels: In-App · Push (FCM) · SMS · WhatsApp · Email
- Peak volume: exam results release can trigger 500K+ notifications simultaneously
- Celery task queue handles async delivery

---

## Page Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  "Notification Template Manager"     [New Template]  [New Event]│
├─────────────────────────────────────────────────────────────────┤
│  KPI Strip — 6 cards (auto-refresh every 120s)                  │
├─────────────────────────────────────────────────────────────────┤
│  Tab Bar:                                                       │
│  Templates · Event Map · Delivery Rules · Channel Config        │
│  Analytics · Suppression · Audit Log                            │
├─────────────────────────────────────────────────────────────────┤
│  [Active Tab Content]                                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## KPI Strip — 6 Cards (auto-refresh every 120s)

| # | Label | Value | Delta | Click Action |
|---|---|---|---|---|
| 1 | Total Templates | Count of active templates across all channels | — | Opens Templates tab |
| 2 | Events Configured | Count of event types with at least one template mapped | — | Opens Event Map |
| 3 | Sent (Last 24h) | Total notifications sent in last 24 hours | vs yesterday | Opens Analytics |
| 4 | Delivery Rate | % successfully delivered in last 7 days | vs prev 7d | Opens Analytics |
| 5 | Suppressed Users | Count of students with channel opt-outs | — | Opens Suppression tab |
| 6 | Failed (24h) | Delivery failures in last 24 hours | — | Opens Analytics with failure filter |

---

## Tab 1 — Templates

Full library of all notification templates. Grouped and searchable.

### Toolbar
- Search by template name, event, or content
- Channel filter: All / In-App / Push / SMS / WhatsApp / Email
- Category filter: Exam / Result / Student / Finance / System / Marketing / Security
- Status filter: All / Active / Draft / Under Review / Deprecated

### Template Cards (list view)

Each template row shows:

| Field | Detail |
|---|---|
| Template Name | Descriptive name |
| Event | The trigger event this template is attached to |
| Channel | Channel icon(s) — a template may exist for multiple channels |
| Category | Badge |
| Status | Active (green) · Draft (amber) · Under Review (blue) · Deprecated (grey) |
| Version | v1.x |
| Sent (30d) | Count of sends in last 30 days |
| Delivery Rate | % for last 30 days |
| Open Rate | % (for push/email) |
| Last Modified | Relative date |
| Actions | Edit · Preview · Clone · Deprecate |

### Complete Notification Event and Template List

#### Exam Notifications

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| Exam Scheduled | In-App, Push, Email | When admin schedules exam | student_name, exam_name, exam_date, exam_time, portal_link |
| Exam Reminder — 24h | Push, SMS, Email | 24 hours before exam | student_name, exam_name, exam_time, instructions_link |
| Exam Reminder — 2h | Push, SMS | 2 hours before exam | student_name, exam_name, start_time |
| Exam Reminder — 30min | Push | 30 minutes before exam | student_name, exam_name, join_link |
| Exam Started (Live) | In-App, Push | When live exam begins | exam_name, end_time |
| Exam Ending Soon | In-App, Push | 10 minutes before exam close | exam_name, minutes_remaining |
| Exam Extended | In-App, Push, SMS | When admin extends exam duration | student_name, exam_name, new_end_time |
| Exam Cancelled | In-App, Push, SMS, Email | When admin cancels exam | student_name, exam_name, reason, rescheduled_date |
| Exam Postponed | In-App, Push, SMS, Email | When exam date changes | student_name, exam_name, old_date, new_date, reason |
| Instructions Updated | In-App, Push | When instructions change after student registered | student_name, exam_name, portal_link |

#### Result Notifications

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| Result Published | In-App, Push, SMS, Email | When admin releases results | student_name, exam_name, score, rank, result_link |
| Rank Improved | In-App, Push | When retake improves rank | student_name, exam_name, old_rank, new_rank |
| Topper Badge Awarded | In-App, Push | When student is in top 3 | student_name, exam_name, rank |
| Score Certificate Ready | In-App, Push, Email | When certificate generated | student_name, exam_name, download_link |
| Solution Published | In-App, Push | When solutions are made available | student_name, exam_name, solutions_link |
| Result Disputed | In-App, Email | When admin acknowledges a dispute | student_name, exam_name, dispute_id, support_link |

#### Student Account Notifications

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| Account Created | Email | On registration | student_name, institution_name, login_link |
| Welcome Email | Email | 1h after account creation | student_name, institution_name, getting_started_link |
| Password Reset | Email | On request | student_name, reset_link, expiry_minutes |
| Email Verified | In-App | On verification | student_name |
| Batch Enrolled | In-App, Push, Email | When added to batch | student_name, batch_name, faculty_name, first_exam_date |
| Batch Removed | In-App, Email | When removed from batch | student_name, batch_name |
| Profile Incomplete | In-App, Push | 48h after signup if profile incomplete | student_name, profile_link |
| Account Suspended | Email, SMS | On suspension | student_name, reason, appeal_link |
| Account Reactivated | Email | On reactivation | student_name, login_link |

#### Finance Notifications

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| Fee Reminder | Push, SMS, Email | Configured days before due | student_name, amount_due, due_date, payment_link |
| Payment Received | In-App, Email | On successful payment | student_name, amount, transaction_id, invoice_link |
| Invoice Ready | Email | After invoice generated | student_name, invoice_number, download_link |
| Payment Failed | In-App, Email | On payment failure | student_name, amount, failure_reason, retry_link |
| Refund Processed | Email, In-App | On refund completion | student_name, amount, refund_id, expected_days |

#### System Notifications (Admin-facing)

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| Exam Starting (Admin) | In-App, Push | 15 min before live exam | admin_name, exam_name, enrolled_count |
| Result Approval Needed | In-App, Email | When results ready for review | admin_name, exam_name, portal_link |
| Doubt Submitted | In-App | When student submits doubt | admin_name, student_name, question_ref |
| Low Enrollment Alert | In-App, Email | When enrollment < threshold 48h before exam | admin_name, exam_name, enrolled_count, threshold |
| Storage Limit Warning | In-App, Email | At 80% and 95% of storage quota | admin_name, used_mb, limit_mb, upgrade_link |
| Subscription Expiring | In-App, Email | 30d, 14d, 7d before subscription end | admin_name, plan_name, expiry_date, renew_link |

#### Security Notifications

| Event | Channels | Timing | Key Variables |
|---|---|---|---|
| New Device Login | Email, SMS | On login from new device/IP | user_name, device, location, timestamp, secure_link |
| Failed Login Attempts | Email | After 5 failed attempts | user_name, attempt_count, secure_link |
| 2FA Enabled | Email | On 2FA setup | user_name, timestamp |
| Password Changed | Email | On password change | user_name, timestamp, secure_link |

---

## Template Editor Drawer (720px)

Opens when clicking Edit on any template.

### Editor Header
- Template name (editable)
- Event (read-only — change via Event Map)
- Channel badge
- Version number
- Status badge
- "Save Draft" and "Submit for Review" buttons

### Channel-Specific Editor Fields

**In-App Notification:**
- Title (max 60 chars) with variable insertion button
- Body (max 200 chars) with variable insertion
- Notification type: Info (blue) / Success (green) / Warning (amber) / Alert (red)
- Action button label (e.g. "View Result") — optional
- Action URL (relative portal URL or external link)
- Priority: Normal / High (high = shown as banner, not just bell icon)
- Auto-dismiss: Yes (X seconds) / No

**Push Notification (FCM):**
- Title (max 50 chars) with variable insertion
- Body (max 100 chars) with variable insertion
- Icon: Default app icon / Custom URL
- Click action: Open app (specific screen) / Open URL
- Deep link: select target screen from dropdown (Results / Exam / Dashboard / Profile / etc.)
- Badge count: increment by 1 / set to specific number / clear
- Sound: Default / Silent / Custom (name from mobile assets)
- Android channel: maps to FCM channel category for Android notification preferences

**SMS:**
- Message body (max 160 chars for single SMS, up to 3 segments = 480 chars)
- Character counter (live, colour-coded: green <160 / amber 160–320 / red >320 = 3 SMS cost)
- Variable insertion button
- DLT Template ID field (India's DLT registration ID — mandatory for transactional SMS in India)
- Sender ID: SRAVEX or institution shortcode (if registered)
- SMS type: Transactional (exempt from DND) / Promotional

**WhatsApp (Meta Business API):**
- Template name (must match approved template in Meta Business Manager)
- Template language (en / hi / te / ta / ml / kn / bn / mr)
- Header: Text / Image / Document / Video
- Body text (max 1024 chars) — variable parameters listed as {{1}}, {{2}}, etc.
- Footer (optional, max 60 chars)
- Buttons (optional): up to 3 buttons of type Quick Reply or Call to Action
- Variable mapping: each {{1}}, {{2}} mapped to system variables

**Email:**
- Subject line (max 90 chars) with variable insertion
- Preheader text (max 130 chars)
- Body: rich text editor (HTML/WYSIWYG toggle)
- Available template components: header block / body text / button / divider / image / footer
- Variable reference sidebar
- "Test Send" button → sends to admin's email with sample data substituted

### Preview Panel (right half of drawer)

Live preview updates as text is typed. Toggle:
- Channel: In-App / Push / SMS / WhatsApp / Email
- Device: Mobile / Desktop (for email and in-app)
- With sample data: substitutes variables with realistic sample values (student_name → "Arjun Sharma", exam_name → "SSC CGL Mock Test 1", etc.)

---

## Tab 2 — Event Map

Maps trigger events to notification templates. One event can trigger notifications across multiple channels.

### Event Map Table

| Column | Detail |
|---|---|
| Event Name | With category badge |
| Event Trigger | What causes this event to fire |
| Channels Configured | Channel icons for all templates mapped to this event |
| Templates | Count of templates (one per channel) |
| Active | Yes/No toggle |
| Conditions | Count of delivery conditions set |
| Volume (30d) | Total notifications triggered by this event in last 30 days |
| Actions | Edit Mapping · View Templates · Pause |

### Edit Event Mapping Drawer (560px)

**Header:** Event name and description

**Channel toggles:**
For each of 5 channels: Enable / Disable toggle + template selector dropdown

**Conditions:**
Optional conditions that must be true for notification to fire:
- Student must have verified email
- Student must have push notifications enabled
- Exam enrollment confirmed
- Student has not received this notification in last X hours (throttle)
- Institution has SMS feature enabled
- Time of day: between 8am and 9pm recipient timezone

**Priority override:**
- Default: notification fires after event (async, Celery task)
- High priority: fires synchronously (for critical alerts like exam starting)

---

## Tab 3 — Delivery Rules

Global rules governing notification delivery beyond individual template conditions.

### Global Throttle Rules

| Rule | Current Setting | Edit |
|---|---|---|
| Max push notifications per student per day | 5 | Edit |
| Max SMS per student per week | 3 | Edit |
| Max WhatsApp per student per week | 5 | Edit |
| Quiet hours (no push/SMS) | 10pm – 7am recipient timezone | Edit |
| Exam-day notification boost | During active exam: push limit increased to 10/day | Edit |
| Notification burst cap | No more than 1,000 sends per second per channel | Edit |
| Duplicate suppression window | Same template to same user within 30 minutes: suppress | Edit |

### Channel Priority Order

When multiple channels are enabled for the same event, defines fallback order:
- Primary: Push (if app installed and enabled)
- Secondary: In-App
- Tertiary: SMS (if phone verified)
- Fallback: Email

Can be reordered per event type.

### Delivery Windows

Per institution type and exam category:
- School exams: reminders sent between 7am–8pm IST
- Competitive exam (SSC/RRB): reminders sent between 7am–9pm IST
- Medical (NEET): no restrictions
- Banking (IBPS/SBI): no restrictions

---

## Tab 4 — Channel Config

Technical configuration for each notification channel.

### In-App Config
- Notification bell badge: max count shown (99+)
- Retention: how long notifications are kept in bell history (default 30 days)
- Mark as read: on click / on hover / manual
- Notification grouping: group by type / show individually

### Push (FCM) Config
- Firebase project configuration (masked)
- Android default channel ID and name
- iOS APNs certificate status (expires date shown)
- Background sync allowed: Yes / No
- Delivery analytics: FCM delivery receipts enabled
- Service worker version

### SMS Config
- Primary gateway: Kaleyra / MSG91 (dropdown — active gateway shown)
- Backup gateway: (configured for failover)
- DLT Principal Entity ID (masked)
- Sender ID for transactional: SRAVEX
- Sender ID for OTP: SRAVOTP
- Credits remaining: count with warning threshold
- Monthly SMS budget limit

### WhatsApp Config
- Meta Business Account ID (masked)
- Phone number display (the SRAV WhatsApp business number)
- Template approval status: X of Y templates approved by Meta
- Message credit balance
- Quality rating (Meta shows health status: Green / Yellow / Red)
- Webhook URL for delivery receipts

### Email Config
- Provider: AWS SES
- From address: noreply@srav.in
- Bounce handling: SES bounce topic subscribed
- Complaint handling: SES complaint topic subscribed
- DKIM: Enabled (✓) with domain verification status
- SPF: Enabled (✓)
- DMARC: Enabled (✓)
- Current sending quota: X per day / Y per second (shown from SES API)

---

## Tab 5 — Analytics

Performance metrics for all notification channels.

### Overview Cards (6 cards)

| Card | Value | Delta |
|---|---|---|
| Total Sent (30d) | Count | vs prev 30d |
| Delivery Rate | % | vs prev 30d |
| Open Rate (Push + Email) | % | vs prev 30d |
| Click Rate | % | vs prev 30d |
| Opt-out Rate | % | vs prev 30d |
| Failed Deliveries | Count | vs prev 30d |

### Channel Performance Table

| Channel | Sent (30d) | Delivered | Delivery % | Opened | Open % | Clicked | Click % | Opted Out |
|---|---|---|---|---|---|---|---|---|
| In-App | 1,240,450 | 1,240,210 | 99.98% | 987,342 | 79.6% | 543,210 | 43.8% | 2,341 |
| Push | 3,420,180 | 3,101,420 | 90.7% | 1,240,568 | 36.3% | 432,190 | 12.6% | 8,903 |
| SMS | 420,340 | 415,220 | 98.8% | — | — | — | — | 1,240 |
| WhatsApp | 180,450 | 174,930 | 96.9% | 162,340 | 90.0% | 98,450 | 54.6% | 890 |
| Email | 890,230 | 853,421 | 95.9% | 341,210 | 38.4% | 102,430 | 11.5% | 3,240 |

### Top Performing Templates (last 30 days)

Table: Template name · Channel · Sent · Open Rate · Click Rate · Opt-out Rate — sorted by open rate descending.

### Failure Analysis

Table of failed deliveries grouped by failure reason:
- Invalid token (push): stale FCM token
- Phone unreachable (SMS)
- Email bounced (hard)
- Email bounced (soft)
- WhatsApp number not on WhatsApp
- DLT template rejected

For each failure type: count, percentage of sends, resolution action.

### Notification Volume Chart

Line chart: daily notification volume per channel over the selected period. X-axis: dates. Y-axis: count. One line per channel (In-App / Push / SMS / WhatsApp / Email).

---

## Tab 6 — Suppression

Manages opt-outs, hard bounces, and manual suppressions.

### Suppression Summary Cards

| Card | Value |
|---|---|
| Push Opt-outs | Students who disabled push |
| SMS Opt-outs | Students who replied STOP |
| WhatsApp Opt-outs | Students who blocked or opted out |
| Email Unsubscribes | Students who clicked unsubscribe |
| Hard Bounces | Invalid email addresses |
| Manual Suppression | Admin-added suppressions |

### Suppression List Table

| Column | Detail |
|---|---|
| Student Name | (masked based on DPDPA) |
| Institution | Institution name |
| Suppressed Channel | Badge |
| Reason | Opt-out / Hard Bounce / Soft Bounce / Admin Suppressed / DPDPA Erasure |
| Added On | Date |
| Expiry | Permanent or date |
| Added By | "System" or admin name |
| Actions | Remove Suppression (admin override for re-consent scenarios) |

**Pagination:** 25 / 50 / 100 per page. CSV export.

### Bulk Suppression Import
Upload CSV with student IDs and channels to suppress. Used after DPDPA erasure requests.

---

## Tab 7 — Audit Log

### Filters
- Date range
- Admin name
- Template name
- Action: Template Created / Template Published / Event Mapped / Rule Changed / Channel Configured / Suppression Added

### Audit Table

| Column | Detail |
|---|---|
| Timestamp | Date and time |
| Admin | Name + role |
| Action | Colour badge |
| Template / Event | Affected name |
| Channel | Badge |
| Change | 1-line summary |

---

## Notification Delivery Architecture

Understanding how notifications flow is critical for troubleshooting:

### Delivery Flow

1. **Event fired:** Application code fires a notification event (e.g. `result_published` signal)
2. **Event map lookup:** System checks Event Map for enabled channels and templates
3. **Condition evaluation:** Delivery conditions evaluated (quiet hours, throttle, opt-out status, student preferences)
4. **Celery task queued:** Async notification task queued for each eligible channel+recipient pair
5. **Gateway call:** Celery worker calls channel gateway API (FCM / SMS gateway / AWS SES / Meta API)
6. **Delivery receipt:** Gateway responds with success/failure; stored in delivery_log table
7. **Analytics update:** Counters updated for delivery rate, open rate tracking

### Peak Volume Handling

Result release events can trigger 500K+ notifications within minutes:
- Celery workers auto-scale based on queue depth (auto-scaling configured in infrastructure)
- Task routing: push notifications → `push_queue`; SMS → `sms_queue`; Email → `email_queue`; each with dedicated workers
- Rate limiting enforced per gateway: AWS SES max 14/s by default (burst to 200/s after reputation warm-up); SMS gateway 100 TPS; FCM batched (1000 tokens per batch request)
- At 2.4M–7.6M students: full result release push notification batch can take 10–40 minutes to complete
- Progress visible in Analytics tab under "Current Send Batch" panel (when a bulk send is in progress)

### Retry Policy

| Channel | Max Retries | Retry Delay | Final Action |
|---|---|---|---|
| Push (FCM) | 3 retries | Exponential: 1m, 5m, 15m | Log as failed; remove stale token from DB |
| SMS | 2 retries | 5m, 15m | Log as failed; flag phone for review |
| WhatsApp | 1 retry | 5m | Log as failed |
| Email | 3 retries | 1m, 10m, 60m | Log as failed; hard bounce → suppress |
| In-App | No retry needed | — | Stored in DB; delivered on next page load |

---

## Student Notification Preferences

Students can control their notification preferences in their profile settings on the student portal. The notification template manager shows how these preferences are handled:

### Preference Options (student-controlled)

| Preference | Default | Scope |
|---|---|---|
| Exam reminders | Enabled | Push + SMS + Email |
| Result notifications | Enabled (cannot disable) | All channels |
| Promotional/marketing | Disabled | Email only |
| Fee reminders | Enabled | Push + Email |
| System alerts | Enabled (cannot disable) | In-App only |
| WhatsApp updates | Opt-in (disabled by default) | WhatsApp |
| Monthly progress digest | Enabled | Email |

"Cannot disable" preferences are mandatory for platform operation (result notifications) or safety (system alerts). All others are student-adjustable.

### Institution Control Layer

Institutions can further restrict which notifications their students receive:
- Institution can disable: Promotional email / Monthly digest / Fee reminders (if institution manages fees externally)
- Institution cannot disable: Result notifications, Exam reminders, Security alerts

---

## Template Review and Approval Workflow

All new notification templates and significant edits go through a review process before going live.

### Workflow Stages

| Stage | Description | Responsible |
|---|---|---|
| Draft | Template written | PM Institution Portal or UI/UX Designer |
| Internal Review | Content review (messaging, tone, DPDPA compliance) | PM Platform |
| Legal Review (optional) | For templates containing financial or legal language | Legal team |
| QA Testing | Template tested via "Send Test" to QA email/phone | QA Engineer |
| Published | Template active and deployed | PM Platform |

**Status transitions:**
- Draft → Internal Review: "Submit for Review" button
- Internal Review → QA Testing: "Approve Content" button
- QA Testing → Published: "Approve and Publish" button (2FA required for publishing SMS templates due to DLT compliance)

### Template Versioning

Each published edit creates a new version. Previous versions retained:
- v1.0 (original) · v1.1 (typo fix) · v2.0 (redesign)
- "Compare versions" button: shows diff of template content between two versions
- "Rollback to version" button: creates new Draft identical to selected version

---

## DPDPA Compliance Features

The India Digital Personal Data Protection Act (DPDPA) 2023 imposes specific obligations on notification data handling.

### Compliance Checklist for Notification Templates

Each template is checked against:
- [ ] Contains only data the student has consented to share (no third-party PII)
- [ ] Does not include sensitive categories (health, financial beyond fee) unless necessary
- [ ] Retention period: notification records deleted after 90 days (configurable)
- [ ] Student name in subject line: opt-in consent assumed via registration
- [ ] Unsubscribe mechanism present in all marketing emails
- [ ] Audit trail: all sends logged with timestamp and consent basis

### Data Fiduciary Obligations

The platform acts as a Data Fiduciary. Specific obligations in notifications:
- **Notice:** Students are informed about notification types during registration
- **Consent:** Marketing notifications require explicit opt-in
- **Erasure:** When a student exercises right to erasure, all future notifications are suppressed and historical notification content (templates with PII) is anonymised in logs
- **Portability:** Students can request export of their notification history (last 90 days)

### DPDPA Compliance Tab (within each template)

Toggle to "DPDPA Compliance" view shows:
- Data fields used in this template: student_name / exam_name / score / rank / etc.
- Data category: General / Sensitive (financial) / Special category
- Legal basis for processing: Contractual necessity / Legitimate interest / Consent
- Retention period for delivery logs
- Cross-border transfer: Yes/No (AWS SES routes through Mumbai region by default)

---

## Integration Points

| Page | Integration |
|---|---|
| Page 16 — Portal Templates | Email notification templates are shared between portal templates and this page. Email template editor is the same component. |
| Page 17 — Onboarding Workflow | Onboarding email sequences use templates managed here. Sequence emails can reference templates from this library. |
| Page 15 — Institution Role Config | Institution admins configure which notification types their admin users receive. This page manages the templates that are sent. |
| Page 25 — Defect Tracker | Failed notification delivery (high failure rate) can be escalated to a defect. "Create Defect" button in Analytics failure table. |

---

## Key Design Decisions

| Concern | Decision | Rationale |
|---|---|---|
| DLT template ID field | Required for SMS templates | India's TRAI mandate — transactional SMS without DLT registration is blocked by operators |
| Throttle rules | Global + per-event conditions | Prevents notification fatigue; students who receive too many notifications opt out |
| Quiet hours | 10pm–7am per recipient timezone | India-specific: parents and students in rural areas complain about late-night notifications |
| WhatsApp variable mapping | {{1}} {{2}} to system variables | Meta API requires positional variables — the mapping UI makes this manageable |
| Character counter for SMS | Colour-coded at 160/320 chars | Cost awareness — each 160-char segment is billed separately by gateway |
| Suppression tab | Separate from templates | Suppression management is a compliance and operational concern, not a content concern |
| DPDPA erasure support | Bulk suppression import | When a student exercises erasure right, all their notification history and future sends must be suppressed |
| Exam-day push boost | Configurable throttle override | On exam day, students need timely notifications — standard daily cap is too restrictive |
| Celery queue routing | Separate queue per channel | Prevents SMS queue backup from blocking push notifications; each channel scales independently |
| Retry policy per channel | Different retries and delays | FCM has better delivery guarantees than SMS; SMS gateways are less reliable; retry policy reflects this |
| Student preference layer | Student controls above throttle | Students who opt out should not receive notifications even if throttle rules would otherwise allow it |
| Template versioning | All versions retained | Enables rollback; DPDPA audit trail of what was communicated to students |

