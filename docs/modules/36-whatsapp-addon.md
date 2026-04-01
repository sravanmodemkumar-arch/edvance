# Module 36 — WhatsApp Add-on

## 1. Purpose

Module 36 provides EduForge institutions with WhatsApp Business API integration as a first-class communication channel — not merely a fallback to SMS. It covers outbound messaging (transactional, reminders, announcements, emergency alerts), inbound message handling, the admission enquiry bot, HSM template management, WABA quality monitoring, and cost tracking.

WhatsApp is the primary digital communication channel for parents in tier-2 and tier-3 Indian cities. For institutions serving first-generation education families, WhatsApp often reaches parents more reliably than a dedicated app. Module 36 is an optional paid add-on; institutions enable it per their subscription.

The module integrates with Module 31 (Admission CRM), Module 25 (Fee Collection), Module 28 (Hostel), Module 29 (Transport), Module 33 (PTM), Module 34 (Announcements), Module 35 (Notifications), Module 37 (Email), Module 38 (SMS), and Module 42 (Audit Log).

---

## 2. WhatsApp Business Setup

### 2.1 WABA Configuration

| Parameter | Detail |
|-----------|--------|
| BSP (Business Solution Provider) | Gupshup / Kaleyra / ValueFirst / Twilio / custom |
| Phone Number ID | Meta-assigned; unique per registered number |
| WABA ID | WhatsApp Business Account ID from Meta |
| Access Token | BSP API access token; stored encrypted |
| Business display name | Institution's verified name; shown in recipient's WhatsApp |
| Green tick status | Verified / Pending / Not applied |
| Daily message limit tier | Standard (1k) / Medium (10k) / High (100k) — based on quality score |

### 2.2 BSP Setup

EduForge supports pluggable BSP adapters. Each BSP adapter implements:
- Send message (template + session)
- Receive webhook (inbound messages)
- Delivery status webhook
- Template management API

Switching BSP: institution migrates phone number to new BSP; API credentials updated; no message history loss (stored in Module 36, not BSP).

### 2.3 Opt-in Mechanism

Per WhatsApp Business Policy and DPDPA:
- Opt-in displayed at app onboarding (Module 01): "Would you like to receive updates via WhatsApp?" — checkbox; not pre-ticked
- Opt-in at admission (Module 31): parent consent form includes WhatsApp opt-in
- Re-opt-in: if phone number changes → re-consent required
- Opt-in record: user ID, phone number, channel = WhatsApp, timestamp, consent text shown, IP address — immutable

### 2.4 Opt-out Handling

- User sends STOP to institution's WhatsApp number → immediately unsubscribed
- User disables WhatsApp in app notification preferences (Module 35) → unsubscribed
- Opt-out honoured within 5 seconds of receipt
- Post opt-out: no outbound WhatsApp except authentication OTP (transactional exception)
- Opt-out record stored with timestamp; DPDPA compliant

### 2.5 24-Hour Session Window

WhatsApp Business policy:
- User sends any message to institution's number → 24-hour session window opens
- During window: institution can send free-form messages (any content)
- After window closes: only approved HSM templates can be sent
- Session tracking: Module 36 stores last-inbound-message timestamp per number; session expiry computed

---

## 3. HSM Template Management

### 3.1 Template Categories & Costs

| Category | Use Case | Approval Time | Cost (approx) |
|----------|---------|--------------|--------------|
| Utility | Fee receipt, admit card, result, boarding | 1–2 hours | ₹0.30–₹0.50 per message |
| Authentication | OTP, login verification | 1–2 hours | ₹0.30–₹0.40 per message |
| Marketing | Event invite, scholarship, open house | 24–48 hours | ₹0.60–₹0.80 per message |

Costs vary by BSP and Meta's pricing schedule (updated periodically). Cost per message tracked in Module 36.

### 3.2 Template Record

| Field | Detail |
|-------|--------|
| Template name | Unique across WABA (e.g., `eduforge_fee_reminder_v2`) |
| Category | Utility / Authentication / Marketing |
| Language | One template per language |
| Body | Text with `{{1}}`, `{{2}}` variable placeholders |
| Header | Optional: image / document / video / text |
| Footer | Optional: short text |
| Buttons | CTA (URL/phone) or Quick Reply; up to 3 |
| Status | Draft / Submitted / Approved / Rejected / Paused |
| Submission date | When submitted to Meta |
| Approval date | When approved |
| Rejection reason | If rejected |
| Usage count | Total sends (last 30 days) |
| Opt-out rate | % recipients who blocked after receiving |

### 3.3 Template Submission Workflow

```
Module owner defines template content (body + buttons + language)
  → Admin reviews for WhatsApp policy compliance
  → Submitted to Meta via BSP API
  → Status tracked: Pending → Approved / Rejected
  → If rejected: rejection reason shown; admin revises + resubmits
  → Approved templates visible in notification template registry (Module 35)
```

### 3.4 Template Variables

Variables substituted at send time from event payload:
- `{{1}}` = student name
- `{{2}}` = amount / date / course / exam name (context-dependent)
- `{{3}}` = institution name (many templates end with "— [Institution Name]")

Variable values must match approved template length constraints.

### 3.5 Template Analytics

Per template per week:
- Sent count
- Delivered count + delivery rate %
- Read count + read rate %
- Button click count + CTR %
- Opt-out (block) count + opt-out rate %

Templates with opt-out rate > 0.5% in any week → flagged to admin; paused if > 1% in 3 consecutive days.

### 3.6 Template Lifecycle

- Active: in use; metrics tracked
- Paused: auto-paused if opt-out rate too high or usage = 0 for 30 days
- Deprecated: replaced by newer version; old version no longer sendable
- Rejected: cannot be used; admin notified to revise

---

## 4. Outbound Messaging

### 4.1 Transactional WhatsApp (Auto-triggered)

Triggered by event from other modules via Module 35:

| Event | Template | Recipient |
|-------|---------|----------|
| Fee receipt generated | `eduforge_fee_receipt` | Parent |
| Admit card ready | `eduforge_admit_card` | Student + Parent |
| Result published | `eduforge_result_published` | Student + Parent |
| Child boarded bus | `eduforge_bus_boarding` | Parent |
| Child dropped | `eduforge_bus_drop` | Parent |
| Sick bay admission | `eduforge_sickbay_admission` | Parent |
| Curfew breach | `eduforge_curfew_breach` | Parent + Warden |
| Appointment confirmed | `eduforge_counselling_appointment` | Student |
| Application status updated | `eduforge_admission_status` | Applicant |
| Offer letter ready | `eduforge_offer_letter` | Applicant + Parent |

### 4.2 Reminder WhatsApp (Scheduled)

| Reminder | Trigger | Template |
|----------|---------|---------|
| Fee due reminder | 7 days / 3 days / 1 day before due | `eduforge_fee_reminder` |
| PTM reminder | D-2, D-0 (morning) | `eduforge_ptm_reminder` |
| Exam reminder | D-1 | `eduforge_exam_reminder` |
| Library book due | 2 days before due date | `eduforge_library_due` |
| Document submission deadline | 5 days before | `eduforge_doc_reminder` |

### 4.3 Announcement WhatsApp

Routed from Module 34 → Module 35 → Module 36:
- Emergency: immediate dispatch; all opted-in users
- Holiday notice: template with date + name
- Event invitation: RSVP button included in template
- Achievement recognition: personalised (student name + achievement)

### 4.4 Bulk Send Management

For large broadcasts (e.g., fee reminder to 5,000 parents):
- Batched per Meta's daily limit for institution's tier
- Rate: 20 messages/second (default BSP rate); burst handled by queue
- Before send: opt-out list refreshed; opted-out numbers excluded
- Personalised: each message has recipient-specific variable substitution
- Delivery report: sent / delivered / read / failed — real-time dashboard
- Cost estimate shown before confirming bulk send

### 4.5 WhatsApp Payment Link

Fee reminder templates include a "Pay Now" CTA button:
- Button URL: deep link to Module 25 payment page (personalised per student/invoice)
- Parent taps → payment gateway opens in browser
- Payment completed → receipt sent back via WhatsApp (auto-triggered by Module 25)
- Eliminates need for parent to log into app for routine fee payment

### 4.6 Rich Media Outbound

| Media Type | Use Case |
|-----------|---------|
| PDF | Admit card, fee receipt, report card, offer letter |
| Image | Timetable (as image), event poster, achievement certificate |
| Location | Campus location, event venue |
| Contact (vCard) | Counsellor / class teacher contact to save |
| Audio | Pronunciation guide (language learning context) |

All media stored in R2; WhatsApp URL provided to BSP (must be public HTTPS URL with valid content-type header).

---

## 5. Inbound Message Handling

### 5.1 Inbound Webhook Processing

BSP sends POST to Module 36 webhook on each inbound message:
- Message type, content, from-number, timestamp, WABA ID
- Module 36 processes within 200ms (sync response to BSP; async processing)
- Duplicate handling: message ID dedup; same message not processed twice

### 5.2 Message Routing Logic

```
Inbound message received
  → Is sender opted-in?
      No → "To receive updates via WhatsApp, please register via our app."
      Yes → Is there an active bot session?
          Yes → Route to bot engine
          No → Is there an open staff assignment?
              Yes → Route to assigned staff conversation
              No → Start bot session (main menu)
```

### 5.3 Keyword Auto-responses

Configurable keyword → auto-response mapping:

| Keyword | Auto-response |
|---------|--------------|
| FEE / FEES | "[Student Name]'s outstanding fee: ₹[amount]. Due: [date]. Pay: [link]" |
| RESULT | "[Student Name]'s latest result: [score]. View full report: [link]" |
| TIMETABLE | "Today's timetable for [Student Name]: [formatted schedule]" |
| HOLIDAY | "Next holiday: [date] — [reason]. Next working day: [date]" |
| STOP | Opt-out confirmed; no further messages |
| HELP | Main menu displayed |

Keywords case-insensitive; partial match supported (e.g., "my fees" triggers FEE handler).

### 5.4 Staff Reply Interface

Admin panel (web + app) for staff to reply to inbound messages:
- Conversation view: full thread per number; student/parent profile linked
- Staff sees: sender name, student linked, class, recent events (attendance, fee status, exam score)
- Reply: free-form (within 24-hour session window) or template (outside window)
- Assignment: conversation assigned to specific staff (class teacher, accounts, admission counsellor)
- Status: Open / Pending reply / Resolved / Escalated
- SLA: reply within 2 hours during business hours; auto-flag if unresponded

### 5.5 Media Received from Parents

Parents can send:
- Photo of medical certificate → linked to student's health record
- Photo of fee payment receipt (NEFT screenshot) → linked to pending fee record; accounts team verifies
- Document (migration certificate, caste certificate) → linked to student's admission documents

Storage: R2; linked record created with pending-approval status; staff reviews and approves linkage.

### 5.6 Conversation History

- All inbound and outbound messages stored per phone number
- 180-day retention (DPDPA compliant)
- Searchable by: keyword, date, student name, staff who replied
- Exportable per student for audit

---

## 6. Admission Enquiry Bot

### 6.1 Bot Architecture

Rule-based state machine (not LLM-dependent):
- Predictable, fast, low-cost
- States: Greeting → Language selection → Main menu → Sub-menu → Completion / Escalation
- State stored per conversation session (Redis-equivalent in-memory; 30-minute TTL)

### 6.2 Conversation Flow

```
User messages institution's WhatsApp
  → Bot: "Welcome to [Institution Name]! Please select language:
          1. English  2. हिंदी  3. తెలుగు  4. தமிழ்  5. Other"
  → User selects language
  → Bot: "How can I help you?
          1. Admission enquiry
          2. Fee enquiry
          3. Results
          4. Timetable
          5. Talk to a person"
```

**Path 1 — Admission Enquiry:**
```
Bot: "Which course are you interested in?"
  → [List of courses shown as numbered options or typing]
User selects course
  → Bot: "For [Course], here are the details:
          ✅ Eligibility: [criteria]
          📅 Admission open: [date]
          🗓 Last date: [date]
          💺 Seats: [number]
          💰 Fee: ₹[amount] per year
          📝 Apply here: [application link]"
  → Bot: "Would you like us to call you? Send your name and we'll connect you to an admission counsellor."
User sends name → lead created in Module 31 → counsellor notified
```

**Path 2 — Fee Enquiry:**
```
Bot: "Please share your registered mobile number for verification."
  → OTP sent → User enters OTP → Authenticated
  → Bot: "[Student Name]'s outstanding fee: ₹[amount]
          Due date: [date]
          Pay securely: [payment link]"
```

**Path 3 — Results:**
```
OTP authentication →
  → Bot shares result as formatted message + link to full report card PDF
```

**Path 4 — Timetable:**
```
OTP authentication →
  → Today's class schedule shown as formatted text
```

**Path 5 — Human Escalation:**
```
Bot: "Connecting you to our team. Please describe your query briefly."
User types → Bot stores → Assigns to relevant staff → Staff notified
Bot: "Our team has received your message and will respond within 2 hours."
```

### 6.3 Bot Fallback

If user input doesn't match any expected response:
- First fallback: "I didn't catch that. Please choose: 1. Admission 2. Fee 3. Results 4. Other"
- Second fallback (same session): "Let me connect you to our team. [Human escalation triggered]"
- Never leaves user stuck

### 6.4 Bot Analytics

| Metric | Description |
|--------|-------------|
| Sessions started | Total bot conversations initiated |
| Language distribution | % per language selected |
| Menu path distribution | Which option selected most |
| Completion rate | % sessions completed without human escalation |
| Escalation rate | % sessions escalated to human |
| Leads generated | Leads created in Module 31 via bot |
| Lead-to-enrolment rate | % bot-generated leads that enrolled |
| Drop-off points | Where do users abandon the conversation? |

---

## 7. WABA Quality & Compliance

### 7.1 Quality Score Monitoring

Meta assigns each WABA a quality score based on:
- Block rate (users who block the number)
- Read rate (users who read messages)
- Opt-out rate

| Score | Tier | Daily Limit | Action |
|-------|------|------------|--------|
| Green (High) | Very High | 100,000/day | Normal operation |
| Yellow (Medium) | High | 10,000/day | Warning; review templates |
| Red (Low) | Standard | 1,000/day | Immediate review; pause low-performing templates |

Module 36 polls quality score daily; alert to admin if drops from High to Medium or below.

### 7.2 Block Rate Alert

- Block rate > 0.3% in any day → warning to admin
- Block rate > 0.5% in any day → messaging paused; admin must review before resuming
- Root cause analysis: which template caused the spike? → that template paused
- Resolution: template content/frequency reviewed; opt-out process improved

### 7.3 Anti-Spam Measures

- Rate limiting per recipient: max 3 non-transactional WhatsApp messages per day per user
- Frequency capping: no marketing/promotional template more than once per 7 days to the same user
- DND respect: users who opt-out receive no further messages (within 5 seconds)
- Monitoring: weekly review of opt-out patterns; high-opt-out templates flagged

### 7.4 DPDPA Compliance

- All WhatsApp communication = personal data
- Opt-in stored with consent text, timestamp, IP
- Delivery and read status stored per message
- Retention: 180 days conversation history; 1 year audit log
- User can request: list of all WhatsApp messages sent (Module 42 export)
- User can request deletion: conversation history deleted (non-audit records) within 30 days
- BSP data localisation: preference for India-based BSP to support DPDPA data residency

### 7.5 Minor Protection

- Students under 13: WhatsApp sent only to parent number, never to student number
- Students 13–18: WhatsApp sent to both student + parent for academic updates; counselling-related only to student (confidentiality)
- Age derived from Module 07 student profile

---

## 8. Two-Way Communication Use Cases

### 8.1 Absence Alert with Reply

When student marked absent (Module 11):
- Parent receives: "Your child [Name] was marked absent today (Period 1–6). Reply 'R [reason]' to inform the school."
- Parent replies: "R Medical appointment"
- Module 36 parses reply → absence reason auto-recorded in Module 11 → teacher notified
- Eliminates phone calls to school for absence reasons

### 8.2 Weekly Attendance Summary

Every Sunday evening (configurable):
- Parent receives: "[Name]'s attendance this week: 4/5 days (80%). Month-to-date: 85%."
- No action required; informational
- Parents who reply with concern → auto-routed to class teacher

### 8.3 PTM Booking via WhatsApp

PTM booking without app:
- Institution sends: "PTM is on [date]. Reply with your preferred slot: A (10–12 AM) or B (2–4 PM)"
- Parent replies: "A"
- Slot booked in Module 33; confirmation sent back via WhatsApp
- Reduces app dependency for PTM booking; reaches app-inactive parents

### 8.4 WhatsApp Report Card

On result publication:
- Student receives formatted message:
  ```
  📊 [Name]'s Results — [Exam Name]

  📚 Mathematics: 87/100
  📚 Science: 79/100
  📚 English: 91/100
  📚 Social Studies: 82/100
  📚 Hindi: 88/100

  🏆 Total: 427/500 (85.4%)
  🥇 Class Rank: 8/60

  Full report card: [PDF link]
  ```
- Parent shares with family; positive experience; institution brand building

### 8.5 Conversational Fee Payment

Fee reminder includes "Pay Now" CTA:
- Parent taps → payment gateway
- Alternatively: parent replies "PAY" → bot sends UPI deeplink or payment gateway link
- Payment completed → Module 25 updates → receipt sent back via WhatsApp within 30 seconds
- Complete payment cycle without opening EduForge app

---

## 9. Cost Management

### 9.1 Cost Structure

| Message Type | Cost Range | Notes |
|-------------|-----------|-------|
| Utility template | ₹0.30–₹0.50 | Fee receipt, admit card, result |
| Authentication template | ₹0.30–₹0.40 | OTP |
| Marketing template | ₹0.60–₹0.80 | Event invite, scholarship |
| Session message (free text) | ₹0.00 | Within 24-hour window |

Costs vary by BSP negotiated rate and Meta pricing. Module 36 uses actual invoiced rate per BSP.

### 9.2 Cost Dashboard

Per institution per month:
- Messages sent by category (Utility / Auth / Marketing)
- Cost per category
- Total WhatsApp spend
- Cost per student per month (total ÷ enrolled students)
- Cost trend: month-on-month
- Comparison: WhatsApp vs SMS cost (for same notifications)

### 9.3 Cost Optimisation

- Push-reliable users (Module 35 segment): WhatsApp send suppressed for Operational reminders (push is enough)
- Free-window messaging: when parent messages in → all replies within 24 hours are free; counsellors encouraged to reply proactively within the free window
- Template category optimisation: some marketing templates can be reclassified as Utility (lower cost) if content qualifies; admin review suggested
- Annual cost budget: set by admin; alert when monthly spend > 80% of monthly budget

---

## 10. Integration Map

| Module | Integration |
|--------|------------|
| Module 01 — Auth | WhatsApp OTP option; opt-in at onboarding |
| Module 25 — Fee Collection | Payment link in reminders; receipt via WhatsApp |
| Module 26 — Fee Defaulters | Defaulter reminder + lawyer notice templates |
| Module 28 — Hostel | Boarding/drop, sick bay, curfew alerts |
| Module 29 — Transport | ETA, boarding, breakdown alerts |
| Module 31 — Admission CRM | Bot lead creation; offer letter delivery |
| Module 33 — PTM | PTM reminder; two-way booking |
| Module 34 — Announcements | Emergency + event announcement delivery |
| Module 35 — Notifications | All WhatsApp sends routed through Module 35 |
| Module 37 — Email | Fallback if WhatsApp delivery fails |
| Module 38 — SMS | Fallback if WhatsApp opt-out or failure |
| Module 42 — Audit Log | All send events, opt-in/out, quality score changes |

---

## 11. Data Model (Key Tables)

```
wa_accounts
  id, tenant_id, bsp_name, phone_number_id, waba_id,
  display_name, green_tick_status, daily_limit_tier,
  quality_score, last_quality_check, is_active, created_at

wa_opt_ins
  id, user_id, user_type, phone_number, opted_in_at,
  consent_text, ip_address, channel, opted_out_at,
  opt_out_method, is_active

wa_templates
  id, wa_account_id, template_name, category, language,
  body, header_type, header_content, footer, buttons_json,
  status, submitted_at, approved_at, rejection_reason,
  usage_count_30d, opt_out_rate, is_active

wa_outbound_messages
  id, wa_account_id, recipient_number, user_id, user_type,
  template_id, variables_json, message_id_bsp, sent_at,
  delivered_at, read_at, status, failure_reason,
  cost_inr, module_source, event_type

wa_inbound_messages
  id, wa_account_id, sender_number, user_id, message_id_bsp,
  message_type, content, media_r2_key, received_at,
  session_active, assigned_to, assignment_role, status,
  resolved_at

wa_bot_sessions
  id, sender_number, user_id, started_at, current_state,
  language, last_input, completed_at, outcome,
  escalated_to_human, lead_created_id

wa_staff_replies
  id, inbound_message_id, staff_id, reply_content,
  reply_type, sent_at, template_id, message_id_bsp

wa_conversations
  id, wa_account_id, number, user_id, user_type,
  session_expires_at, last_inbound_at, last_outbound_at,
  message_count, status

wa_quality_log
  id, wa_account_id, checked_at, quality_score,
  tier, block_rate, read_rate, daily_limit,
  alert_triggered
```

---

## Cross-Module References

- **Module 01**: WhatsApp OTP at login; opt-in collected at onboarding — read + event
- **Module 25**: Payment link in fee reminders; receipt sent post-payment — event write
- **Module 26**: Defaulter templates; lawyer notice templates — event write
- **Module 28**: Hostel event alerts (boarding, curfew, sick bay) — event write
- **Module 29**: Transport event alerts (ETA, boarding, breakdown) — event write
- **Module 31**: Bot creates leads in CRM; offer letter PDF sent — write
- **Module 33**: PTM reminders + two-way slot booking — read + write
- **Module 34**: Emergency and announcement delivery — event write
- **Module 35**: All WhatsApp sends orchestrated through Module 35 — write
- **Module 37**: Fallback for WhatsApp delivery failures — event write
- **Module 38**: Fallback for opt-out numbers — event write
- **Module 42**: All outbound sends, opt-in/out events, quality score changes audited — write

---

*Module 36 complete. Next: Module 37 — Email (AWS SES).*
