# Module 35 — Notifications (In-app & FCM)

## 1. Purpose

Module 35 is the centralised notification dispatch layer for the entire EduForge platform. No other module sends notifications independently — every notification event from every module is routed through Module 35, which handles channel selection, user preference enforcement, delivery, retry, fallback, tracking, and compliance.

At 5 crore (50 million) students, notification infrastructure is mission-critical. Module 35 is designed for high-throughput, high-reliability delivery with clear SLA targets, TRAI DLT compliance for SMS, WhatsApp Business API compliance, and DPDPA-compliant data handling. It owns in-app notifications and FCM/APNs push notifications directly; it delegates SMS, WhatsApp, and email to Modules 38, 36, and 37 respectively.

---

## 2. Infrastructure Architecture

### 2.1 Dispatch Architecture

```
Any Module (11, 14, 25, 28, 29...) emits notification event
  → Module 35 Notification Service receives event
  → Resolves recipients (user IDs → device tokens)
  → Applies user preferences (opt-out, DND, digest mode)
  → Selects channels (push / SMS / WhatsApp / email)
  → For large batches: pushes jobs to SQS queue
  → Workers pull from SQS → dispatch to FCM / APNs / Module 38 / Module 36 / Module 37
  → Delivery receipt returned → status updated
  → In-app notification record created
```

### 2.2 FCM / APNs Setup

| Platform | Service | Notes |
|---------|---------|-------|
| Android | Firebase Cloud Messaging (FCM) | Server key + project ID per tenant |
| iOS | Apple Push Notification Service (APNs) | .p8 key file; expiry alert 60/30 days |
| Web / PWA | Web Push via VAPID | Service worker registered on first browser login |

**FCM high-priority:** used for Emergency and Transactional notifications; bypasses Android Doze mode and battery optimisation.
**FCM normal priority:** used for Operational and Promotional; may be batched by OS.

### 2.3 Device Token Management

| Event | Action |
|-------|--------|
| User logs in | Current device FCM/APNs token registered |
| Token refreshed (FCM rotation) | Client app sends new token; Module 35 updates |
| Token invalid ("not_registered" from FCM) | Token removed; notification not retried |
| Multiple devices | All tokens stored; fan-out to all on send |
| User logged out | Token de-registered for that device |

### 2.4 Throughput & Queuing

- Bulk sends (announcements to 50,000+ students): batched into groups of 500; pushed to SQS queue
- Workers: auto-scaled Lambda functions process SQS jobs
- Target: 50,000 notifications delivered in < 60 seconds (Emergency priority)
- Rate limit per tenant: configurable maximum sends per hour (prevents rogue module triggering storm)
- Deduplication: SQS message dedup ID prevents duplicate processing on retry

### 2.5 Retry & Fallback

| Failure Type | Action |
|-------------|--------|
| FCM network error | Retry 3× with exponential backoff (1s, 4s, 16s) |
| FCM "not_registered" | Remove token; no retry |
| FCM quota exceeded | Queue held; retry after 60 seconds |
| Push not delivered in 30 min (Urgent/Emergency) | Auto-trigger SMS fallback |
| Dead letter | After 3 failed retries → DLQ; admin alert |

---

## 3. Notification Type Taxonomy

### 3.1 Priority Tiers

| Tier | Description | Opt-out | DND Override | FCM Priority |
|------|-------------|---------|-------------|-------------|
| Emergency | Campus closure, fire, medical | No | Yes | High |
| Transactional | Fee receipt, OTP, result, login alert | No | No | High |
| Operational | New assignment, attendance marked | Yes | No | Normal |
| Reminder | Fee due, PTM, exam countdown | Yes | No | Normal |
| Promotional | Event invite, achievement recognition | Yes | No | Low |
| System | Password reset, OTP | No | No | High |
| Well-being | Counselling nudge, wellness tip | Yes (generous) | No | Low |

### 3.2 Per-Module Notification Events

| Module | Event | Recipient |
|--------|-------|----------|
| 11 — Attendance | Student marked absent | Parent + student |
| 14 — Homework | New assignment posted | Student |
| 14 — Homework | Submission due tomorrow | Student + parent |
| 17 — Question Bank | New test assigned | Student |
| 19 — Exam Session | Admit card ready | Student |
| 19 — Exam Session | Exam starts in 1 hour | Student |
| 21 — Results | Results published | Student + parent |
| 22 — Mock Tests | Mock score published; rank updated | Student |
| 25 — Fee Collection | Fee receipt generated | Parent |
| 25 — Fee Collection | Payment overdue (escalating) | Parent |
| 28 — Hostel | Gate scan (exit / entry) | Parent |
| 28 — Hostel | Curfew breach alert | Parent + warden |
| 28 — Hostel | Sick bay admission | Parent |
| 29 — Transport | Bus ETA countdown (3 stops away) | Parent |
| 29 — Transport | Child boarded / dropped | Parent |
| 29 — Transport | Bus breakdown | All parents on route |
| 31 — Admission | Application status changed | Applicant + parent |
| 31 — Admission | Offer letter ready | Applicant + parent |
| 32 — Counselling | Appointment confirmed / reminder | Student |
| 33 — PTM | Slot confirmed; reminder; summary ready | Parent + teacher |
| 34 — Announcements | New announcement | Target audience |
| 34 — Announcements | Emergency alert | All users |

### 3.3 Recipient Matrix

Same event produces different notification content for different roles:

| Event: "Result Published" | Recipient | Content |
|--------------------------|----------|---------|
| Student | "Your results are out! Tap to view your scorecard." |
| Parent | "[Student Name]'s results are published. View report card." |
| Class teacher | "Results published for [Class]. View class performance." |
| Principal | "All results for AY 2025-26 published. Summary available." |

Module 35 resolves the correct content per recipient type at dispatch time.

### 3.4 Rich Push Notifications

| Element | Detail |
|---------|--------|
| Title | Short (< 50 chars); event summary |
| Body | Descriptive (< 100 chars); context |
| Image | Optional thumbnail (announcement image, report card preview) |
| Action buttons | Android: up to 3; iOS: up to 4; e.g., "Pay Now", "View Result", "Acknowledge" |
| Deep link | On tap → opens specific in-app screen (fee page, result screen, etc.) |
| Badge count | Increments on delivery; clears on open |
| Sound | Default / custom (emergency uses distinct sound) |

### 3.5 FCM Topic-Based Delivery

For large stable groups (class, batch, campus-wide):
- Group subscribed to FCM topic at creation (e.g., `class-10a-parents`, `campus-main-all-students`)
- Announcement/emergency → single FCM topic message sent once; FCM handles fan-out to all subscribers
- More efficient than individual token targeting for large groups
- Topic subscription managed in Module 35 (subscribe on join, unsubscribe on exit)

### 3.6 Silent Push (Background Sync)

For data updates that don't require user attention:
- Timetable change → silent push → app updates local cache in background
- New syllabus material → silent push → app pre-fetches content
- User does not see a visible notification; no banner, no sound
- FCM content-available flag used; iOS Background App Refresh must be enabled

---

## 4. User Preferences & Opt-out

### 4.1 Notification Preferences Screen

User sees toggle per notification category per channel:

| Category | In-app | Push | SMS | Email |
|---------|-------|------|-----|-------|
| Emergency | Always | Always | Always | Always |
| Fee reminders | On | On | On | On |
| Attendance alerts | On | On | Off | Off |
| Exam reminders | On | On | Off | On |
| Transport updates | On | On | Off | Off |
| Academic updates | On | On | Off | Off |
| Event announcements | On | Off | Off | Off |
| Wellness nudges | On | Off | Off | Off |

Defaults configurable by institution admin. User can customise within allowed range.

### 4.2 Quiet Hours (DND)

User configures:
- Quiet hours start + end (e.g., 10 PM – 7 AM)
- Days: weekdays only / all days
- Behaviour during quiet hours: notifications held → delivered as digest at quiet hours end

Emergency and Transactional (OTP, fee receipt) bypass quiet hours always.

### 4.3 Digest Mode

User opts into daily digest for Operational notifications:
- Real-time push suppressed for Operational category
- At 6 PM (configurable): single "Today's updates" push sent with summary of all held notifications
- In-app notification centre always shows real-time; only push is batched

### 4.4 Global Mute

User mutes all non-Emergency notifications for a period:
- Duration: 1 hour / 4 hours / Until tomorrow / Custom
- Used for: exam concentration, religious observance, family event
- Emergency and Transactional continue during mute
- Mute auto-expires at set time; no action required to unmute

### 4.5 Opt-out Logging

Every opt-out/in action:
- User ID, notification type, channel, action (opt-out / opt-in), timestamp, reason (if provided)
- Used for TRAI DND compliance audit (proof that DND was respected)
- Used for DPDPA data rights audit (user's consent history)

### 4.6 Institution Mandatory Notifications

Institution admin can flag certain notification types as mandatory (cannot be opted out):
- Examples: Emergency alerts, fee overdue notices, exam schedule
- Mandatory flag respected even if user opts out of that category
- User informed in preferences screen: "This notification is required by your institution."

---

## 5. In-app Notification Centre

### 5.1 Notification Centre Features

- All notifications received in last 90 days, newest first
- Unread count badge on tab
- Mark individual as read / mark all as read
- Delete individual notification
- Pin notification (stays at top; useful for exam schedule, fee deadline)
- Search by keyword (title or body)
- Filter by module/category or date range

### 5.2 Notification Grouping

- Multiple notifications from same source grouped: "3 new assignments — [Course]" → expandable
- Emergency notifications always shown ungrouped (full content immediately visible)
- Grouped notifications expand to individual items on tap

### 5.3 Notification Actions from Centre

All action buttons (Pay Now, View Result, Acknowledge) available directly from notification centre:
- Tap notification → specific screen opens (deep link)
- Or tap action button → action performed inline
- Completed actions (payment, acknowledgement) reflected immediately

### 5.4 Daily Digest Card

For digest-mode users:
- Single card: "Today's updates (N items)" — tap to expand
- Expandable list with each notification
- Digest card marked read when user expands it

### 5.5 Admin Notification Health View

Ops/admin sees:
- Queue depth (messages waiting to be dispatched)
- Delivery rate last 5 minutes / last 1 hour
- Failed delivery count
- DLQ count (dead-letter notifications)
- FCM token health (% valid tokens vs stale)
- Alerts: if delivery rate < 90% → page to on-call engineer

---

## 6. Template Management

### 6.1 Template Registry

Every notification type has a registered template:

| Field | Detail |
|-------|--------|
| Template ID | Unique code (e.g., `ATT_ABSENT_PARENT`) |
| Module | Which module owns this notification |
| Title pattern | e.g., `Attendance Alert — {{student_name}}` |
| Body pattern | e.g., `{{student_name}} was marked absent on {{date}}` |
| Action buttons | Button labels + actions |
| Deep link pattern | e.g., `/attendance/{{student_id}}/{{date}}` |
| FCM priority | Emergency / High / Normal / Low |
| Channels | Which channels this template uses |
| SMS template ID | TRAI DLT registered template ID |
| WhatsApp template | HSM template name |

### 6.2 Template Variables

Substitution at send time from event payload:

| Variable | Source |
|----------|--------|
| `{{student_name}}` | Module 07 student profile |
| `{{amount_due}}` | Module 25 fee record |
| `{{due_date}}` | Module 25 invoice |
| `{{bus_stop}}` | Module 29 route stop |
| `{{exam_name}}` | Module 19 exam session |
| `{{result_date}}` | Module 21 |
| `{{counsellor_name}}` | Module 32 |
| `{{institution_name}}` | Tenant settings |

All substituted at dispatch time; never stored with personalised content in template registry.

### 6.3 Multi-language Templates

Each template has variants per supported language:
- English (default)
- Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati

User's preferred language (from Module 07/09 profile) selected at dispatch time.
If translation not available → English used as fallback.

### 6.4 TRAI DLT SMS Template Management

| Field | Detail |
|-------|--------|
| Principal entity ID | Institution's DLT-registered entity ID |
| Sender ID (header) | 6-character registered header (e.g., EDFRGE) |
| Template ID (per template) | DLT-assigned template ID |
| Template status | Approved / Pending / Rejected |
| Template content | Must match DLT-registered content exactly |
| Variable markers | DLT allows {#var#} placeholders |

Rejected or pending templates: cannot be used for SMS dispatch; error raised to admin.

### 6.5 WhatsApp HSM Templates

Pre-approved WhatsApp Business message templates:
- Submitted to WhatsApp via BSP (Business Solution Provider)
- Template name, language, content, variable placeholders
- Approval status (Approved / Pending / Rejected)
- Only approved templates can be used in outbound WhatsApp
- Template rejection reasons stored; admin can revise and resubmit

### 6.6 Template Testing

Admin can send test notification:
- Select template
- Enter mock variable values
- Send to: self / test device / test group
- Preview rendered notification on Android + iOS + email client view

---

## 7. Delivery, Compliance & Reliability

### 7.1 Delivery Status Lifecycle

```
QUEUED → DISPATCHED → SENT_TO_CHANNEL → DELIVERED → OPENED → [ACKNOWLEDGED]
                                      ↓
                                   FAILED (reason code)
```

Every status transition timestamped; stored per notification per device per channel.

### 7.2 SLA Targets

| Priority | Target Delivery | Measurement |
|----------|----------------|------------|
| Emergency | 95% within 60 seconds | FCM delivery receipt |
| Transactional | 95% within 2 minutes | FCM delivery receipt |
| Operational | 95% within 10 minutes | FCM delivery receipt |
| Promotional | 95% within 30 minutes | FCM delivery receipt |

SLA breach: auto-alert to platform operations team.

### 7.3 SMS Compliance (TRAI)

- All commercial SMS sent via DLT-registered route
- Sender ID (header) registered with TSP (Telecom Service Provider)
- Templates registered; template ID included in every SMS API call
- DND scrub: before bulk promotional SMS → NDNC registry check; compliant numbers only
- Transactional SMS (OTP, fee receipt, exam result): can reach DND numbers; template type = Transactional
- Promotional SMS (event, announcement): DND-compliant numbers only; template type = Promotional

### 7.4 WhatsApp Compliance

- Institution uses WhatsApp Business API via approved BSP
- Opt-in: user must have opted in before receiving WhatsApp messages (consent stored with timestamp)
- Template-only: no free-form messages to users who have not had a conversation in last 24 hours
- Opt-out: user sends STOP → immediately unsubscribed; no further WhatsApp from institution
- Opt-out honoured within: 5 seconds of receipt

### 7.5 DPDPA Notification Data

- Notification content, delivery status, open status = personal data per DPDPA 2023
- Stored with data principal ID (user)
- Retention: 90 days for delivery logs; 1 year for audit logs (Module 42)
- Access: user can request their notification history (data rights); exportable
- Deletion: user can request notification history deletion; complied within 30 days for non-audit records

### 7.6 Emergency Notification Protocol

Authorised senders for Emergency tier: Principal, VP, Security Head, designated emergency officer.

On Emergency send:
- All channels dispatched simultaneously (push + SMS + WhatsApp)
- Rate limits and DND bypassed
- Delivery confirmed within 60 seconds target
- All-clear message: sent when emergency resolved
- Log: immutable; time-stamped; accessible to authorised inspectors

---

## 8. Analytics & Reporting

### 8.1 Notification Analytics Dashboard

Per notification:
- Recipients: count sent / delivered / opened / acknowledged / failed
- Channel breakdown: push vs SMS vs WhatsApp vs email (delivery + open per channel)
- Time to open: average minutes from delivery to first open
- Action click-through: if action button included, % who tapped it

### 8.2 Institution Notification Health Score

Composite (0–100):
- Delivery rate (30%)
- Open rate (30%)
- Opt-out rate (inverse) (20%)
- Action click rate (20%)

Benchmarked against EduForge platform average. Shown to institution admin. Below-benchmark score → improvement suggestions shown.

### 8.3 Cost Per Notification Tracking

| Channel | Cost Basis |
|---------|-----------|
| Push (FCM/APNs) | Free (FCM is free; APNs is free) |
| SMS | Per-SMS cost from carrier (₹0.10–₹0.25 per SMS) |
| WhatsApp | Per-message cost from BSP (₹0.30–₹0.80 per message) |
| Email (SES) | Per-email cost ($0.10 per 1,000 emails) |

Monthly cost dashboard: per module, per notification type. SMS + WhatsApp costs visible; helps modules reduce unnecessary sends.

### 8.4 Personalised Send-Time Analytics

Per user segment (parents / students / staff):
- Open rate by hour of day (0–23h) — heatmap
- Open rate by day of week
- Best send-time window: hour with highest open rate
- Used for: smart send-time scheduling suggestions to senders

### 8.5 Opt-out Trend Report

- Opt-out rate per notification type per month
- Spike: if opt-out > 5% in a week for any type → flagged to module owner
- Action: reduce frequency, improve content quality, or make optional

### 8.6 User Engagement Segmentation

| Segment | Definition | Action |
|---------|-----------|--------|
| Highly engaged | > 70% push open rate | Reduce SMS to save cost |
| Moderately engaged | 30–70% push open rate | Normal cadence |
| Low engagement | < 30% push open rate | SMS fallback; re-engagement campaign |
| App-inactive | No app open in 30+ days | All sends escalate to SMS + email |

---

## 9. Smart Notification Features

### 9.1 Notification Intelligence Layer

Central rules engine in Module 35 prevents notification storms:
- Per-user hourly budget: max 5 notifications/hour (non-emergency); configurable
- If budget exceeded: lower-priority notifications held; delivered in next window
- If 3+ notifications from different modules in 15 minutes → consolidated into single digest push: "You have 4 updates from EduForge — [Tap to view]"
- Emergency and Transactional always delivered immediately regardless of budget

### 9.2 Personalised Send-Time Scheduling

ML model per user:
- Trains on historical open-time data (what hour of day did this user open notifications?)
- For Operational and Promotional notifications → auto-schedule at user's personal best-open window
- Example: "Parent XYZ opens app consistently at 7–8 AM and 6–7 PM → schedule non-urgent notifications for these windows"
- Improves open rates 20–35% vs fixed send-time
- Model retrains weekly; adapts to changing user patterns

### 9.3 Smart SMS-to-Push Conversion

Cost optimisation for at-scale deployments:
- Users with > 60% push open rate (last 30 days) = "push-reliable"
- For push-reliable users: SMS for Operational/Reminder notifications suppressed (push is sufficient)
- SMS only triggered for: Urgent, Emergency, and as fallback for push-reliable users who go offline
- At 5 crore students: 10% SMS reduction → significant cost saving
- Savings reported monthly; auto-applied when threshold crossed

### 9.4 Notification Channel Effectiveness Feedback

After each large notification send, Module 35 reports back to originating module:
- "Your last fee reminder had 78% push open rate but 92% SMS open rate → consider using SMS for fee reminders"
- Module owners can use this feedback to tune their notification strategy
- Platform-wide learning: best channel per notification type updated quarterly in template defaults

---

## 10. Integration Map

Module 35 receives events from virtually all modules and dispatches outward:

**Inbound (receives notification requests from):**
- All modules (01–57) — any module that has a user-facing event emits to Module 35

**Outbound (dispatches to channel modules):**

| Module | Channel |
|--------|---------|
| Module 36 — WhatsApp | WhatsApp message dispatch |
| Module 37 — Email | Email dispatch |
| Module 38 — SMS & OTP | SMS dispatch |

**Supporting modules:**

| Module | Integration |
|--------|------------|
| Module 03 — RBAC | Resolves role-based recipient lists |
| Module 07 / 08 / 09 | Device tokens and language preference |
| Module 42 — Audit Log | Delivery status, opt-out, consent audit |

---

## 11. Data Model (Key Tables)

```
notification_device_tokens
  id, user_id, user_type, platform, token, app_version,
  device_model, os_version, registered_at, last_seen_at,
  is_active, invalidated_at

notification_preferences
  id, user_id, user_type, category, channel, is_enabled,
  updated_at

notification_quiet_hours
  id, user_id, start_time, end_time, days_mask,
  active, created_at

notification_templates
  id, template_code, module_id, title_pattern, body_pattern,
  channels_json, fcm_priority, action_buttons_json,
  deep_link_pattern, sms_template_id, wa_template_name,
  language_variants_json, is_active, version

notification_jobs
  id, tenant_id, event_type, module_id, priority,
  audience_type, recipient_ids_json, template_code,
  payload_json, scheduled_at, status, created_at,
  sqs_message_id, dedup_key

notification_sends
  id, job_id, user_id, channel, device_token_id,
  title, body, deep_link, status, queued_at,
  sent_at, delivered_at, opened_at, acknowledged_at,
  failure_reason, retry_count

notification_inbox
  id, user_id, user_type, job_id, title, body,
  deep_link, is_read, is_pinned, is_deleted,
  created_at, read_at, expires_at

notification_opt_outs
  id, user_id, user_type, category, channel,
  action, timestamp, reason

notification_dlt_templates
  id, template_code, entity_id, sender_id,
  dlt_template_id, template_content, status,
  registered_at, rejection_reason

notification_wa_templates
  id, template_code, wa_template_name, language,
  content, variables_json, status, submitted_at,
  approved_at, rejection_reason

notification_delivery_reports
  id, job_id, total_sent, delivered_push, delivered_sms,
  delivered_wa, delivered_email, opened, acknowledged,
  failed, cost_inr, generated_at
```

---

## Cross-Module References

- **All modules**: emit notification events to Module 35 — write (inbound)
- **Module 03**: role-based recipient resolution — read-only
- **Module 07 / 08 / 09**: device tokens + language preference — read-only
- **Module 36**: WhatsApp dispatch delegated — write
- **Module 37**: Email dispatch delegated — write
- **Module 38**: SMS dispatch delegated — write
- **Module 42**: Every send, delivery, opt-out, and consent action audited — write

---

*Module 35 complete. Next: Module 36 — WhatsApp Add-on.*
