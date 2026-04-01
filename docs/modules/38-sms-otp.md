# Module 38 — SMS & OTP

## 1. Purpose

Module 38 manages all SMS delivery and OTP generation/verification for EduForge institutions. It is the SMS channel module delegated to by Module 35 (Notifications) and Module 01 (Auth). It ensures TRAI DLT (Distributed Ledger Technology) compliance for every outbound SMS, manages dual-provider redundancy for OTP reliability, tracks delivery receipts, and optimises cost through smart routing.

At 5 crore (50 million) students, SMS is the lowest-common-denominator channel — every mobile number receives SMS regardless of app install status, internet connectivity, or WhatsApp registration. Module 38 ensures no critical message is missed.

The module aligns with TRAI Commercial Communications Customer Preference Regulations (CCPR) 2018 and subsequent amendments requiring DLT compliance, NDNC (National Do Not Call) scrub, Principal Entity registration, and template registration for every commercial SMS.

---

## 2. SMS Provider Architecture

### 2.1 Provider Setup

EduForge supports pluggable SMS provider adapters. Supported providers:

| Provider | Use Case |
|---------|---------|
| AWS SNS | Simple transactional; good for low-volume |
| Kaleyra | High-volume; good India DLT support |
| MSG91 | OTP specialist; high OTP delivery rate |
| Textlocal | Cost-effective for bulk promotional |
| Exotel | Voice + SMS combined use |
| Twilio | International SMS (NRI parents) |

Institution selects primary and fallback provider. API credentials stored encrypted.

### 2.2 Dual-Provider OTP

OTP is the most critical SMS flow — login, payment, parent consent:
- Primary provider: Kaleyra / MSG91 (fastest India OTP delivery < 5 seconds target)
- Secondary provider: different carrier route; auto-activated if primary fails
- Failover: if primary returns error → retry once after 5 seconds → switch to secondary
- OTP target SLA: 95% delivered within 30 seconds

### 2.3 Sender ID (Header)

| Institution Type | Sender ID Example | Notes |
|-----------------|------------------|-------|
| School | SCHSMS | 6-char; DLT-registered |
| College/University | CLGSMS or institution abbreviation | 6-char |
| Coaching | COACHS | 6-char |
| Platform-level | EDFRGE | Used for system-level OTPs |

Different sender IDs for transactional vs promotional (DLT requirement for some operators).

### 2.4 SMS Character Limits

| Encoding | Single SMS | Multi-part SMS |
|---------|-----------|---------------|
| ASCII (English) | 160 characters | 153 chars per part |
| Unicode (regional language) | 70 characters | 67 chars per part |

Multi-part SMS: operator concatenates and delivers as one message to handset; billed per part.

Module 38 shows character count + cost multiplier when admin composes or reviews templates.

---

## 3. TRAI DLT Compliance

### 3.1 DLT Registration Requirements

| Element | Required By | Stored In |
|---------|------------|---------|
| Principal Entity ID | TRAI mandate; institution registers on DLT portal | Module 38 tenant settings |
| Telemarketer ID | SMS provider's DLT registration | Module 38 provider config |
| Sender ID (Header) | Registered per operator (Airtel/Jio/Vi/BSNL) | Module 38 sender config |
| Template ID | Per message template; DLT-assigned on approval | Module 38 template record |

Every API call to SMS provider must include: Principal Entity ID + Template ID + Sender ID. Calls without these are rejected by operators.

### 3.2 SMS Categories (TRAI)

| Category | DND Compliance | Examples |
|----------|---------------|---------|
| Transactional | Can reach DND numbers | OTP, fee receipt, exam result, emergency |
| Service Implicit | Can reach DND if service relationship exists | Attendance alert, PTM reminder (for enrolled students) |
| Service Explicit | Can reach DND if explicit consent given | Library overdue, transport update |
| Promotional | DND compliance required (non-DND numbers only) | Event invitations, scholarship notices |

Classification must match DLT registration; mismatch → operator blocks.

### 3.3 Template Registration Workflow

```
Admin defines SMS template content
  → Module 38 validates: character count, variable format, no prohibited content
  → Submitted to DLT portal via provider API (or manual portal entry)
  → DLT portal assigns Template ID; status tracked:
      Pending → Approved (typically 24–72 hours)
      or Rejected (reason provided; template revised)
  → Approved template → active in Module 38 template registry
  → Template ID stored; included in every send
```

### 3.4 Template Variables (TRAI Format)

DLT requires variable fields to use regex-matched placeholders:
- `{#var#}` pattern used in DLT registration
- Module 38 maps internal variables (`{{student_name}}`) to DLT `{#var#}` at template registration
- Variable values must not exceed the character count registered in template

Example registered template:
```
Dear {#var#}, fee of Rs.{#var#} for {#var#} is due on {#var#}. Pay: {#var#} -EDFRGE
```

### 3.5 NDNC Scrub

Before any promotional or service-explicit bulk SMS:
- Phone numbers checked against TRAI NDNC (National Do Not Call) registry via provider API
- DND-flagged numbers removed from send list
- Scrub result cached per number for 24 hours (TRAI allows caching)
- Scrub log: date, numbers checked, numbers excluded — stored for compliance

### 3.6 DLT Audit Log

Every SMS sent:
- DLT Principal Entity ID
- Telemarketer ID
- Template ID
- Sender ID
- Timestamp
- Recipient number (hashed for DPDPA)
- DLR status

Stored in Module 42 (audit log); available for TRAI inspection.

---

## 4. OTP System

### 4.1 OTP Generation

```python
# Pseudocode
import secrets
otp = str(secrets.randbelow(900000) + 100000)  # 6-digit, 100000–999999
otp_hash = sha256(otp + salt + user_id + timestamp)
store(otp_hash, expiry=now+600s, attempts=0)
send_sms(phone_number, template="OTP_AUTH", vars={"otp": otp})
```

- 6 digits, cryptographically random
- Never sequential, never derived from date/time
- Salt unique per request; stored alongside hash
- Plain-text OTP never stored — only hash

### 4.2 OTP Use Cases

| Use Case | Validity | Module |
|---------|---------|--------|
| Login authentication | 10 minutes | Module 01 |
| New device registration | 10 minutes | Module 01 |
| Mobile number verification | 24 hours | Module 01, 07 |
| Payment authorisation | 5 minutes | Module 25 |
| Parent consent for sensitive action | 10 minutes | Module 32, 28 |
| Password reset | 10 minutes | Module 01 |
| Admission application verification | 24 hours | Module 31 |
| WhatsApp bot authentication | 5 minutes | Module 36 |

### 4.3 OTP Delivery Channels

1. **SMS (primary)**: sent immediately via dual-provider; TRAI-registered authentication template
2. **WhatsApp (secondary)**: if parent is WhatsApp-opted-in → authentication template sent simultaneously or as fallback
3. **Email (tertiary)**: for email-verified users or where SMS fails; 6-digit OTP in email body

Channel priority configurable per use case.

### 4.4 OTP Rate Limiting

| Limit | Threshold | Action |
|-------|-----------|--------|
| Per number per 10 minutes | 3 requests | 4th request blocked; wait required |
| Per number per hour | 10 requests | Blocked for 1 hour |
| Per IP per 10 minutes | 10 requests | Rate limited |
| Per IP per hour | 50 requests | IP temporarily blocked; WAF rule |

Rate limit status returned in API response; app shows countdown timer to user.

### 4.5 OTP Verification

```
User submits OTP
  → Fetch stored hash for (user_id, use_case)
  → Check: not expired AND attempts < 5
  → Compute hash(submitted_otp + salt)
  → Compare with stored hash (constant-time comparison; timing-safe)
  → If match: OTP marked used; session created
  → If no match: attempts incremented
  → If attempts = 5: OTP invalidated; new request required
```

### 4.6 Android SMS Autofill

Android Autofill Service (SMS Retriever API):
- App registers for SMS with unique app hash
- OTP SMS ends with app hash: `[OTP] is your EduForge OTP. Valid 10 min. [APP_HASH]`
- Android reads SMS → auto-fills OTP field → user does not need to switch apps
- Module 38 appends app hash to OTP SMS template (Android version only)
- iOS: Manual entry required (or iCloud Keychain autofill if same device as email)

### 4.7 OTP Security Log

Per OTP request (all stored; immutable):
- Request timestamp
- Recipient number (hashed)
- IP address of requester
- Use case
- Delivery status
- Verification result (success / failed / expired / invalidated)
- Number of incorrect attempts

Accessible to security audit; used for fraud detection.

---

## 5. Transactional SMS Templates

All templates registered on DLT. Examples per module:

### 5.1 Authentication & System

```
OTP (Login):
"[Institution] OTP: {#var#}. Valid 10 mins. Do not share with anyone. -EDFRGE"

Password Reset:
"Your [Institution] password reset OTP is {#var#}. Valid 10 mins. Ignore if not requested. -EDFRGE"
```

### 5.2 Fee & Finance (Module 25/26)

```
Fee Due Reminder:
"Dear {#var#}, fee of Rs.{#var#} for {#var#} is due on {#var#}. Pay: {#var#} -EDFRGE"

Fee Receipt:
"Payment Rs.{#var#} received for {#var#} on {#var#}. Receipt: {#var#} -EDFRGE"

Overdue Notice:
"Fee overdue: Rs.{#var#} for {#var#}. Dues must be cleared by {#var#}. Contact accounts. -EDFRGE"
```

### 5.3 Attendance (Module 11)

```
Absent Alert:
"{#var#} marked absent on {#var#}. If unplanned, please inform school. -EDFRGE"

Low Attendance Warning:
"{#var#} attendance is {#var#}%. Minimum 75% required. Please contact class teacher. -EDFRGE"
```

### 5.4 Exam & Results (Modules 19, 21)

```
Exam Reminder:
"{#var#} exam on {#var#} at {#var#}. Venue: {#var#}. Bring admit card. -EDFRGE"

Result Published:
"{#var#}'s result is published. Score: {#var#}. View report: {#var#} -EDFRGE"
```

### 5.5 Transport (Module 29)

```
Boarding Confirmation:
"{#var#} boarded bus at {#var#} at {#var#}. -EDFRGE"

Drop Confirmation:
"{#var#} dropped at {#var#} at {#var#}. -EDFRGE"

Bus Delay:
"Bus on route {#var#} is running {#var#} mins late. New ETA: {#var#}. -EDFRGE"

Breakdown Alert:
"Bus on route {#var#} has broken down near {#var#}. Alternate transport being arranged. -EDFRGE"
```

### 5.6 Hostel (Module 28)

```
Gate Exit:
"{#var#} exited hostel at {#var#}. Expected return by {#var#}. -EDFRGE"

Curfew Breach:
"ALERT: {#var#} has not returned by curfew ({#var#}). Contact warden: {#var#} -EDFRGE"

Sick Bay:
"{#var#} admitted to sick bay at {#var#}. Contact warden: {#var#} -EDFRGE"
```

### 5.7 Emergency (Module 34)

```
Emergency Alert:
"URGENT: {#var#} is closed today. {#var#}. All students stay home. More updates on app. -EDFRGE"
```

### 5.8 Admission (Module 31)

```
Application Status:
"Application {#var#} status: {#var#}. View details: {#var#} -EDFRGE"

Offer Letter:
"Congratulations! Offer letter for {#var#} ready. Accept by {#var#}: {#var#} -EDFRGE"
```

---

## 6. Bulk SMS Management

### 6.1 Bulk Send Flow

```
Admin/Module composes bulk SMS
  → Audience selected (class / campus / fee defaulters / all parents)
  → NDNC scrub (if promotional/service-explicit)
  → Character count check + cost estimate shown
  → Template ID validated (DLT-approved)
  → Confirm send
  → Jobs pushed to SQS queue
  → Workers dispatch at provider rate limit (1,000/min typical)
  → DLR webhook updates delivery status
  → Completion report: sent / delivered / failed / pending
```

### 6.2 Cost Estimate Before Send

Before confirming any bulk send:
- Recipient count: N
- SMS count per message: 1 (English < 160 chars) or 2 (160–320 chars) or Unicode count
- Estimated cost: N × SMS_count × per_SMS_rate
- Displayed in INR; admin must acknowledge

### 6.3 Regional Language SMS

For parents with Hindi/Telugu/Tamil/Kannada preference:
- Same template translated to respective language
- Unicode encoding; 70 chars per SMS part
- Language-specific DLT templates registered separately (same DLT portal; language tagged)
- Sent in parent's preferred language from Module 09 profile

### 6.4 SMS Short Links

All URLs in SMS shortened (20–22 chars):
- `https://app.institution.edu.in/fees/inv/12345` → `https://s.edfrge.in/ab3Xk`
- Click tracked: when parent taps link → redirect logged → Module 37/35 analytics
- Short link expiry: 30 days (configurable per use case)
- Short domain: `s.edfrge.in` (platform-level) or `s.institution.edu.in` (institution-branded)

---

## 7. Delivery Tracking

### 7.1 DLR (Delivery Receipt) Processing

Provider sends DLR to Module 38 webhook:
- Message ID, recipient number, status, timestamp, error code (if failed)
- Processed within 5 seconds of receipt
- Status enum: Delivered / Undelivered / Buffered (will retry) / Expired / Failed (invalid number)

### 7.2 DLR Status Actions

| Status | Action |
|--------|--------|
| Delivered | Record updated; no further action |
| Buffered | Wait 30 minutes; then re-check |
| Expired (> 24 hours undelivered) | Mark failed; if Urgent → fallback channel triggered |
| Undelivered — Invalid number | Flag contact as invalid in Module 07/09 |
| Undelivered — Not reachable | Retry after 30 minutes (once); if fails → mark inactive |
| Failed — DLT violation | Admin alerted; template reviewed; DLT issue resolved |

### 7.3 OTP-Specific DLR

- OTP DLR not received in 30 seconds → user sees "Resend OTP" option in app (countdown from 60s)
- OTP DLR not received in 2 minutes → auto-trigger WhatsApp OTP or email OTP
- OTP delivery failure rate monitored: target > 95% delivered within 30 seconds

### 7.4 Delivery Dashboard

Per day / per week:
- Total SMS sent, delivered, failed, pending, expired
- By module source (fee reminders vs attendance alerts vs OTP vs transport)
- By SMS category (transactional vs service vs promotional)
- Delivery rate by carrier (Airtel / Jio / Vi / BSNL)
- OTP-specific: sent, delivered, verified, expired, failed

---

## 8. Smart Routing & Cost Optimisation

### 8.1 Channel Selection Logic (With Module 35)

Before sending any notification as SMS:
1. Is recipient WhatsApp-opted-in AND last seen on WhatsApp < 7 days? → WhatsApp first, SMS as fallback
2. Is notification type = Operational/Reminder + recipient is push-active (app open < 3 days)? → Push only; skip SMS
3. Is notification type = Transactional (fee receipt, result)? → Push + SMS simultaneously (important; confirm delivery)
4. Is notification type = Emergency? → Push + SMS + WhatsApp simultaneously (all channels)
5. Is recipient phone number inactive (3× undelivered)? → Skip SMS; email only

This logic is in Module 35's dispatch engine; Module 38 executes what Module 35 decides.

### 8.2 WhatsApp OTP Cost Saving

For WhatsApp-opted-in users:
- OTP delivered via WhatsApp authentication template (₹0.30–₹0.40 per message vs ₹0.10–₹0.25 for SMS)
- Wait — WhatsApp is MORE expensive for OTP in many cases; use SMS as primary for OTP
- Exception: international numbers (NRI parents) where international SMS costs ₹2–₹5 per SMS; WhatsApp is cheaper

Cost decision table:
| Scenario | Primary Channel | Reason |
|---------|----------------|--------|
| Domestic OTP | SMS | Cheaper; faster |
| International OTP (NRI) | WhatsApp | Cheaper than international SMS |
| Operational reminder (WhatsApp-active) | WhatsApp | No cost (session window) or Utility rate |
| Emergency | All channels | Reach > Cost |

### 8.3 Message Length Optimisation

- Templates reviewed quarterly: if any template routinely splits into 2 SMS → rewritten to fit in 1
- Abbreviations used carefully (must not reduce clarity)
- URL shortening saves 30–50 chars per SMS (critical for staying under 160 chars)
- Cost saved: reducing 2-part SMS to 1-part = 50% cost saving for that template

---

## 9. Compliance & DPDPA

### 9.1 TRAI Compliance Checklist

| Requirement | Status |
|------------|--------|
| Principal Entity registered on DLT | Tenant onboarding step |
| Sender ID registered (all 4 operators) | Tenant onboarding step |
| All templates DLT-approved before use | Enforced in Module 38 (blocked if not approved) |
| NDNC scrub before promotional send | Automated pre-send |
| Template ID in every API call | Enforced in provider adapter |
| No unapproved content in templates | Admin review + DLT validation |

### 9.2 DPDPA Compliance

- Recipient mobile number: personal data; stored hashed in delivery logs
- SMS content contains student name: personal data; log content hashed after 90 days
- OTP request log: mobile number hashed; full log retained 1 year for security audit
- Delivery receipts: retained 1 year
- Right to access: user can see list of SMS sent to their number (anonymised in logs; request via support)
- Right to deletion: delivery metadata retained for audit; content anonymised within 30 days of request

### 9.3 Children's SMS Policy

- Students under 13: SMS sent only to parent's registered mobile; never to student's number
- Students 13–18: attendance/results SMS to parent; OTP to student's own number
- Age from Module 07

### 9.4 Prohibited SMS Content

Module 38 template validator blocks:
- URLs to non-HTTPS domains
- Phone numbers in body (except institution contact; DLT allows one verified contact)
- Alcohol, tobacco, gambling content
- Misleading sender names
- No harassment (complaints received → number blocked from further send)

---

## 10. Analytics & Reporting

### 10.1 SMS Analytics Dashboard

| Metric | View |
|--------|------|
| Daily SMS volume | Total + by category + by module |
| Delivery rate | Overall + by carrier + by category |
| OTP success rate | Sent → Delivered → Verified |
| OTP drop rate | Sent but not verified |
| Cost today / this month | INR; by module |
| DLT compliance rate | Template ID present in all sends? |
| Failed sends | Count + reason breakdown |
| Inactive numbers | Count flagged this month |

### 10.2 OTP Dashboard

- Total OTPs sent (today / week / month)
- Delivery rate: % delivered within 30 seconds
- Verification rate: % OTPs successfully verified
- Failure reasons: expired / too many attempts / invalid / not delivered
- Average time to verify: seconds from delivery to user entry
- Abuse detection: OTP requests per number distribution; spike detection

### 10.3 Monthly Cost Report

| Module | SMS Sent | Cost (₹) |
|--------|---------|---------|
| Module 01 (OTP) | X | ₹X |
| Module 11 (Attendance) | X | ₹X |
| Module 25 (Fee) | X | ₹X |
| Module 29 (Transport) | X | ₹X |
| Module 34 (Announcements) | X | ₹X |
| Total | X | ₹X |
| Cost per student per month | — | ₹X |

Compared to WhatsApp and email costs for the same notifications → informs channel strategy.

### 10.4 Carrier-Level Delivery Analysis

| Carrier | Delivery Rate | Avg Delivery Time |
|---------|--------------|-----------------|
| Airtel | % | seconds |
| Jio | % | seconds |
| Vi | % | seconds |
| BSNL | % | seconds |
| International | % | seconds |

Carrier with persistent low delivery → provider route change triggered.

---

## 11. Integration Map

| Module | Integration |
|--------|------------|
| Module 01 — Auth | OTP for login, password reset, device registration |
| Module 11 — Attendance | Absence alerts to parents |
| Module 19 — Exam Session | Exam reminders; admit card notification |
| Module 21 — Results | Result published SMS |
| Module 25 — Fee Collection | Fee reminder, receipt confirmation |
| Module 26 — Fee Defaulters | Overdue notices, legal notices |
| Module 28 — Hostel | Gate scan, curfew breach, sick bay |
| Module 29 — Transport | Boarding, drop, delay, breakdown |
| Module 31 — Admission | Application status, offer letter |
| Module 34 — Announcements | Emergency alerts, holiday notices |
| Module 35 — Notifications | All SMS dispatches orchestrated by Module 35 |
| Module 36 — WhatsApp | Fallback coordination; OTP dual-channel |
| Module 42 — Audit Log | All sends, DLR, OTP events audited |

---

## 12. Data Model (Key Tables)

```
sms_providers
  id, tenant_id, provider_name, api_endpoint, api_key_encrypted,
  sender_id, dlt_entity_id, dlt_telemarketer_id, is_primary,
  is_otp_provider, is_active, created_at

sms_templates
  id, tenant_id, template_code, module_source, category,
  body_pattern, char_count, is_unicode, sms_parts,
  dlt_template_id, dlt_status, dlt_submitted_at,
  dlt_approved_at, dlt_rejection_reason, is_active

sms_sends
  id, tenant_id, recipient_number_hash, user_id, user_type,
  template_id, provider_id, provider_message_id,
  body_preview, sent_at, dlr_status, delivered_at,
  failure_reason, cost_inr, module_source, category

otp_requests
  id, user_id, use_case, phone_hash, ip_address,
  otp_hash, salt, expires_at, created_at,
  delivery_channel, delivered_at, dlr_status,
  attempts, verified_at, status, invalidated_at

sms_suppression_list
  id, tenant_id, phone_hash, reason, suppressed_at,
  suppression_type, manually_added, removed_at

sms_ndnc_scrub_log
  id, tenant_id, scrub_date, numbers_checked,
  dnd_count, non_dnd_count, campaign_id

sms_delivery_stats
  id, tenant_id, date, provider_id, category,
  total_sent, delivered, failed, pending, expired,
  total_cost_inr, avg_delivery_seconds
```

---

## Cross-Module References

- **Module 01**: OTP for login and device verification — write (requests OTP generation)
- **Module 11**: Absence alert delivery — event write
- **Module 19 / 21**: Exam and result SMS — event write
- **Module 25 / 26**: Fee reminder, receipt, overdue — event write
- **Module 28 / 29**: Hostel and transport alerts — event write
- **Module 31**: Admission status SMS — event write
- **Module 34**: Emergency + announcement SMS — event write
- **Module 35**: All SMS dispatches orchestrated by Module 35; Module 38 executes — write (receives)
- **Module 36**: OTP dual-channel coordination; fallback — coordination
- **Module 42**: All send events, DLR, OTP audit — write

---

*Module 38 complete. Next: Module 39 — Certificates & TC.*
