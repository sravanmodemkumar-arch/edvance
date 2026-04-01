# Module 34 — Announcements & Circulars

## 1. Purpose

Module 34 owns all institutional communication published by the institution to students, parents, and staff — from general notices and event invitations through formal circulars, emergency alerts, and mandatory regulatory notices. It is the single source of truth for all broadcast communication, ensuring every message is targeted, tracked, acknowledged, and archived.

The module aligns with CBSE/UGC mandatory notice requirements, POCSO 2012 (ICC contact display), UGC Anti-Ragging Regulations (helpline display), DPDPA 2023 (privacy notice), RTI Act (officer display for government-aided institutions), and TRAI guidelines for SMS. It integrates with Module 03 (RBAC), Module 05 (Academic Calendar), Module 26 (Fee Defaulters), Module 32 (Counselling), Module 35 (Notifications), Module 36 (WhatsApp), Module 37 (Email), Module 38 (SMS & OTP), and Module 42 (Audit Log).

---

## 2. Announcement Configuration

### 2.1 Announcement Types

| Type | Description | Typical Sender |
|------|-------------|---------------|
| General circular | Routine institutional notice | Admin / Principal |
| Exam notice | Schedule, admit card, seating | Exam coordinator |
| Holiday notice | Declared holiday; campus closure | Principal |
| Fee reminder | Due date, outstanding notice | Accounts |
| Event invitation | Annual Day, Sports Day, seminar | Event coordinator |
| Emergency alert | Fire, flood, campus closure | Principal / Security |
| Policy update | Rule change, new policy | Principal |
| Result notification | Results published; link | Exam coordinator |
| Admission notice | Admission open; eligibility | Admission team |
| Achievement recognition | Topper, sports win, award | Class teacher / Principal |
| Scholarship notice | Eligibility, deadline, application | Admin |
| Regulatory notice | CBSE/UGC/AICTE circular | Admin |
| Condolence | Death of staff or student | Principal |

### 2.2 Priority Levels

| Priority | Behaviour |
|----------|-----------|
| Normal | Delivered in regular notification queue; respects DND |
| Important | Delivered with sound/vibration alert; unread nudge at 48 hours |
| Urgent | Immediate delivery; SMS fallback if push not delivered |
| Emergency | Push + SMS + WhatsApp simultaneously; overrides all DND settings |

### 2.3 Channel Options

| Channel | When Used | DND Applicable |
|---------|----------|----------------|
| In-app feed | All announcements | No (always shows in feed) |
| Push notification | Important / Urgent / Emergency | Yes (except Emergency) |
| SMS | Urgent / Emergency / SMS fallback | Yes (except Emergency) |
| Email | Formal circulars, event invitations | Yes |
| WhatsApp | Emergency; rich-media announcements | Yes (except Emergency) |
| Notice board | Physical + digital mirror | N/A |

Sender selects channels at composition time. System enforces: Emergency always uses all channels simultaneously.

### 2.4 Multi-Language Support

- Announcement composed in English (or Hindi)
- AI-assisted translation to parent's preferred language (Hindi, Telugu, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati)
- Sender reviews translation before publishing (one-click approve or edit)
- Parent sees announcement in their preferred language (Module 09 profile)
- Both language versions stored in announcement record

### 2.5 Scheduled & Recurring Announcements

**Scheduled:** Compose now → set publish date/time → auto-publishes at scheduled time. Useful for: result day announcement (ready in advance), holiday wishes, exam schedule.

**Recurring:** Configure a template + schedule (weekly/monthly/on a specific calendar trigger):
- "Fee reminder" — auto-sent on 1st of each month to all students with outstanding dues
- "Holiday reminder" — auto-sent 2 days before every declared holiday
- "PTM reminder" — auto-sent 7 days before PTM date

Recurring jobs visible in admin panel; can be paused or edited.

---

## 3. Audience Targeting

### 3.1 Audience Hierarchy

```
Institution (all)
  └── Campus / Branch
        └── Department / Course
              └── Class / Batch / Section
                    └── Individual student / staff / parent
```

Any level can be selected; multiple selections allowed (e.g., Class 10A + 10B + 10C).

### 3.2 Role-Based Targeting

Using Module 03 RBAC role groups:
- All teaching staff
- All hostel wardens
- All parents of boarders
- All Class 12 students
- All parents of fee defaulters (Module 26 filter)
- All CWSN students (Module 32 filter)
- All newly enrolled students (Module 31 filter — current AY)

### 3.3 Custom Audience Lists

- Admission manager creates: "Scholarship recipients 2025–26"
- Transport manager creates: "Bus Route 3 parents"
- Principal creates: "Merit list — Top 50 students"
- Custom lists reusable; updated when underlying data changes

### 3.4 Delivery Preview & Test Send

Before publishing:
- Sender sees: estimated recipient count, channel-wise breakdown
- Test send: announcement sent to sender's own account first
- Confirmation required for bulk sends > 100 recipients
- Final preview in parent app format shown before confirm

### 3.5 Opt-out Handling

- Parents can opt out of non-critical announcements from app settings
- Opt-out respected for Normal and Important priority
- Urgent and Emergency: cannot be opted out; always delivered
- Opt-out log: date, parent, reason; admin can see opt-out trend per announcement type

---

## 4. Approval Workflow

### 4.1 Workflow Configuration

| Sender Role | Approval Required | Approver |
|-------------|------------------|---------|
| Principal / Registrar | No (publish immediately) | — |
| HOD / Dean | Optional (configurable) | Principal |
| Class teacher | Yes | HOD or Principal |
| Admin staff | Yes | Principal |
| Counsellor | Yes | HOD + Principal |
| Student union (if enabled) | Yes | Dean of Students |

### 4.2 Approval Flow

```
Sender drafts announcement
  → Submits for approval → Push notification to approver
  → Approver: Reviews → Approve / Reject (with comment)
  → If approved: published immediately or at scheduled time
  → If rejected: sender notified with comment; revises and resubmits
  → Approval SLA: if no action in 4 hours → escalates to next approver
```

### 4.3 Emergency Override

- Emergency-priority announcements: published immediately by Principal/VP/Security Head
- No approval workflow; immediate multi-channel delivery
- Audit log still captures: who published, when, content, recipients

### 4.4 Post-Publish Editing

- Once published, edit requires new approval cycle
- New version published; old version archived (never deleted)
- Recipients notified: "This announcement has been updated — [original title]"
- Version history visible to admin

---

## 5. Digital Notice Board

### 5.1 Notice Board Structure

| Section | Content |
|---------|---------|
| Pinned (top) | Up to 3 announcements pinned by Principal; always visible |
| Active announcements | All non-expired announcements for this audience; newest first |
| Events calendar | Upcoming events from Module 05; scrollable |
| Mandatory notices | Always-on: anti-ragging helpline, ICC contact, grievance cell, DPDPA notice |
| Archived | Past announcements; searchable |

### 5.2 Mandatory Permanent Notices

Per regulatory requirements — always visible in app; cannot be unpinned:

| Notice | Regulatory Basis |
|--------|-----------------|
| Anti-ragging helpline: 1800-180-5522 | UGC Anti-Ragging Regulations 2009 |
| ICC / POSH contact | UGC (Prevention of Sexual Harassment) 2015 |
| POCSO complaint cell contact | POCSO 2012 |
| Student Grievance Redressal Committee | UGC Grievance Redressal Regulations 2023 |
| RTI officer name + contact | RTI Act 2005 (government-aided institutions) |
| DPDPA privacy notice | DPDPA 2023 |

### 5.3 Physical Notice Board Mirror

QR code displayed on physical campus notice board:
- Scanned by student/parent with phone camera
- Opens the digital notice board filtered to same audience
- Keeps physical board relevant for visitors; digital board for app users

### 5.4 Category Browse

Students and staff can browse by category:
- Academic / Administrative / Events / Sports & Cultural / Scholarships / Jobs (college) / Emergency / Others

### 5.5 Student Union / Association Board

Separate section for student body communications:
- Student body (elected representatives) can submit announcements
- Moderated: Dean of Students must approve before publishing
- Clear labelling: "Student Union — [Date]" vs institutional announcements

---

## 6. Delivery, Tracking & Read Receipts

### 6.1 Delivery Architecture

Every announcement dispatched via Module 35 (Notifications) orchestration layer:
- Module 35 manages push notification routing (FCM/APNS)
- Module 38 manages SMS delivery
- Module 36 manages WhatsApp message delivery
- Module 37 manages email delivery
- Module 34 stores results; does not own delivery infrastructure

### 6.2 Read Receipt Tracking

| Event | When Recorded |
|-------|--------------|
| Delivered (push) | FCM confirms delivery to device |
| Opened (in-app) | User taps announcement; in-app view |
| Opened (email) | Tracking pixel fires (Module 37) |
| Read (WhatsApp) | Blue tick received (Module 36) |
| Acknowledged | User taps "Acknowledge" button |

Per-announcement dashboard: sent / delivered / opened / acknowledged / failed — per channel.

### 6.3 Acknowledgement-Required Announcements

For high-stakes communications:
- Exam schedule
- Fee payment deadline
- Field trip permission
- PTM date + confirmation
- Policy change

"Acknowledge" button displayed. Non-acknowledgement after 48 hours:
- Re-notification sent
- Non-acknowledgers list generated for class teacher / admin follow-up

### 6.4 SMS Fallback

Triggered when:
- Push notification not delivered within 30 minutes (device offline, app uninstalled)
- Announcement priority = Urgent or Emergency

SMS: shortened text version of announcement + app deep link. TRAI-registered template per announcement type.

### 6.5 Unread Nudge

For Important/Urgent announcements:
- 48 hours after send: users who opened app but did not read the announcement → targeted re-push
- 72 hours: remaining unread → SMS nudge (for Important+)
- Nudge sends tracked; nudge count capped at 3 per announcement to prevent harassment

### 6.6 Read Rate Analytics

Per announcement:
- Read rate = opened ÷ delivered × 100%
- Benchmark: school average read rate (computed from last 90 days)
- Comparison shown to sender: "78% read — above your 65% average"
- Low read rate (<40%) for Important announcements → flagged to admin for alternate outreach

---

## 7. Circular Management

### 7.1 Official Circular Format

Every official circular has:
- Institution letterhead (name, logo, address)
- Circular reference number: `CIR/YYYY-YY/001` (sequential per academic year; never reused)
- Date of issue
- Addressee (e.g., "To all students and parents of Class 10")
- Subject line
- Body (formal English; paragraph numbered)
- Signature block: issuing authority name, designation, date
- Generated as PDF via WeasyPrint; delivered via Module 37 + in-app

### 7.2 Circular Register

| Field | Detail |
|-------|--------|
| Reference number | Unique sequential |
| Date | Issue date |
| Subject | Brief subject |
| Addressee | Target audience |
| Issued by | Signing authority |
| Channel | Email / app / physical / all |
| Acknowledgement required | Yes / No |
| Acknowledgement count | If required |
| Status | Active / Archived / Withdrawn |

Searchable by date range, subject, reference number. Available for audit/inspection.

### 7.3 Inward Circular Register

External circulars received (CBSE, AICTE, UGC, State Board, Government):
- Registered on receipt: date received, issuing authority, subject, reference number
- Distributed to: relevant staff via announcement
- Action required: noted; responsible person assigned; due date
- Compliance tracked: if action required by external circular → action completion logged

### 7.4 Formal Parent Circulars

Situations requiring formal written circular to parent:
- Fee structure change (advance notice as per state rule: 30–60 days)
- Policy change (uniform, timing, rules)
- Academic warning (as per Module 33)
- Suspension or expulsion
- Major exam schedule
- Annual report publication

Formal circulars require Principal's digital approval before issue. Delivery via email + in-app. Acknowledgement tracked.

### 7.5 Circular Amendment & Withdrawal

**Amendment:** if circular contains error:
- Amendment circular issued with original reference number
- Body: "This amends Circular CIR/2526/003 dated DD-MM-YYYY. The corrected [section] reads as follows: …"
- Both stored; amendment linked to original

**Withdrawal:** if circular issued in error:
- Withdrawal notice issued; all recipients notified
- Original archived (not deleted); withdrawal notice linked
- Reason for withdrawal documented

### 7.6 Annual Circular Archive

- All circulars of AY compiled into single PDF booklet at year-end
- Sent to all parents as reference document
- Stored in R2; accessible to new staff / parents joining mid-year for context

---

## 8. Emergency Alert System

### 8.1 Emergency Alert Workflow

```
Emergency officer (Principal / Security Head) opens Emergency Alert screen
  → Selects emergency type from preset list
  → Edits message if needed (preset template auto-fills)
  → Taps "Send Emergency Alert" — single confirmation prompt
  → System dispatches: Push + SMS + WhatsApp simultaneously
  → All active users in institution receive within 60 seconds (target)
  → Emergency log entry created immediately (immutable)
```

### 8.2 Emergency Types & Preset Messages

| Type | Preset Message Template |
|------|------------------------|
| Campus closure | "URGENT: [Institution] is closed today due to [reason]. All students please stay home. Classes will resume [date/TBD]. Stay safe." |
| Fire on campus | "EMERGENCY: Fire reported at [location]. All students and staff evacuate immediately via [exit]. Do not use elevators. Assembly point: [location]." |
| Medical emergency | "MEDICAL ALERT: A medical emergency has occurred on campus. Medical team is responding. Parents of affected students will be contacted directly." |
| Cyclone / flood | "SAFETY ALERT: Due to [cyclone/flood] warning, campus will be closed on [date]. All students must reach home safely. Updates will follow." |
| Law and order | "SAFETY NOTICE: As a precaution, campus activities are suspended. Students on campus are safe. Further updates to follow." |
| Gas leak | "EMERGENCY: Gas leak reported. Evacuate the building immediately. Stay upwind. Do not use electrical switches." |
| All clear | "ALL CLEAR: [Institution] has confirmed the situation is resolved. Campus activities will resume normally. Thank you for your cooperation." |

All templates editable; sender adds location-specific details.

### 8.3 Drill Notifications

For fire drills, evacuation drills:
- Same channel as emergency alert
- Message prefixed: "[DRILL — NOT A REAL EMERGENCY]"
- Drill log: date, type, participants, drill duration, evacuation time, issues found

### 8.4 Emergency Log

Immutable after creation:
- Timestamp, sender, emergency type, message sent, channels used, recipient count, delivery count
- Post-incident review attachment: what happened, how alert was managed, improvements
- Accessible to: Principal, management, authorised government inspector

### 8.5 NDMA Alignment

Emergency message content aligned with NDMA (National Disaster Management Authority) guidelines:
- Clear action instruction (what to do, not just what happened)
- No speculation or unverified information
- Single source of truth (no conflicting messages from different staff)
- Follow-up updates at defined intervals (e.g., every 30 minutes during ongoing emergency)

---

## 9. Events, Invitations & RSVPs

### 9.1 Event Announcement

| Field | Detail |
|-------|--------|
| Event name | Full name |
| Category | Annual Day / Sports / Cultural / Seminar / Field Trip / PTM / Other |
| Date + time | Start and end |
| Venue | Room / hall / external address |
| Organiser | Staff in-charge |
| RSVP required | Yes / No |
| RSVP deadline | Date by which to confirm |
| Capacity | Max attendees (if applicable) |
| Guests allowed | Number of guests per invitee |

### 9.2 RSVP Management

- Invitee confirms attendance in-app: "Attending" / "Not attending" / "Maybe"
- Capacity cap: once max reached, late RSVP shows "Waitlist" option
- RSVP count visible to organiser in real-time
- Auto-close RSVP at deadline
- Reminder to non-RSVP'd: D-2 reminder for Important events

### 9.3 Field Trip Permission

- Announcement includes embedded digital permission slip
- Parent reads: date, destination, purpose, transport, cost, emergency contact
- Parent taps "I give permission for [Student Name] to attend this trip"
- Digital signature + timestamp stored
- Trip proceeds only when all participants have signed permission slips
- Non-responding parents: class teacher follow-up; trip exclusion for unsigned participants

### 9.4 Achievement Recognition

- Teacher nominates student (or staff) for recognition
- Approval: class teacher → Principal → published
- Recognition announcement: student name, achievement, photo (with consent)
- Parent + student receive personal notification: "Congratulations — [Student Name] has been featured for [achievement]"
- Positive community building; visible to all students as motivation

### 9.5 Condolence Announcements

- Published by Principal only
- Language: respectful, brief, compassionate
- No operational details (medical cause, circumstances) in public announcement
- Counsellor support noted: "Counselling support is available for students who are affected"
- Comments disabled on condolence announcements (no social media behaviour)

---

## 10. Compliance & Mandatory Notices

### 10.1 Mandatory Notice Compliance Checklist

Auto-verified quarterly by system:

| Notice | Regulatory Basis | Status Check |
|--------|-----------------|-------------|
| Anti-ragging helpline | UGC 2009 | Always visible in app |
| ICC / POSH contact | UGC 2015 | Always visible |
| POCSO complaint cell | POCSO 2012 | Always visible |
| Grievance committee | UGC GRR 2023 | Always visible |
| RTI officer | RTI Act 2005 | Visible for govt-aided |
| DPDPA privacy notice | DPDPA 2023 | Versioned; last updated shown |
| Fee structure display | Consumer Protection Act | Published at admission |
| Admission notice | Affiliating board | Published at admission cycle start |

If any mandatory notice is removed or expired → compliance alert to Principal.

### 10.2 Fee Hike Notice

State-specific advance notice requirements:
- Most states: 30–60 days advance notice to parents before fee revision
- Formal circular with: new fee structure, effective date, reason, appeal process
- Approval trail: management committee approval documented
- Parent acknowledgement tracked (formal legal requirement in some states)

### 10.3 Admission Public Notice

AICTE/UGC/state board requirements:
- Institution must publicly display: available seats, eligibility criteria, reservation breakdown, fee, last date
- Module 34 publishes this as a public-facing announcement (visible even without login)
- Archived after admission cycle closes; retrievable for regulatory audit

### 10.4 DPDPA Privacy Notice

- Stored as a permanent in-app notice
- Versioned: each update creates a new version; previous versions archived
- Last updated date prominently shown
- New user (student/parent) must acknowledge privacy notice on first app login (Module 01)
- Major policy changes: re-acknowledgement required from all users

---

## 11. Analytics & Reporting

### 11.1 Announcement Analytics Dashboard

Per announcement:
- Total recipients, delivered count, opened count, acknowledged count
- Channel-wise breakdown (push / SMS / email / WhatsApp)
- Delivery rate % and open rate % vs institution benchmark
- Time-to-read: average minutes from delivery to open
- Geography of readers (for multi-campus: which campus opened more)

### 11.2 Read Rate Optimisation

- Historical open rate by: hour of day, day of week, audience type
- Best send-time suggestion shown to sender at composition
- A/B testing (limited): same announcement sent at two different times to two groups; winner identified
- Best-performing time window personalised per audience segment

### 11.3 Announcement Fatigue Monitor

- Per parent: count of announcements received in last 24 hours
- If count > 5 → flag to admin: "Parent [X] has received 6 announcements today. Consider consolidating."
- Monthly report: average daily announcements per parent; trend; target < 3/day for non-urgent

### 11.4 Compliance Report

- Mandatory notices: all present / missing / expired
- Emergency drills: conducted / due
- Circular register completeness: sequential numbers; no gaps
- Acknowledgement completion rate for mandatory circulars
- Exported for NAAC / board / regulatory inspection

### 11.5 Year-on-Year Engagement

- Parent read rate trend: improving/declining per year
- Channel preference shift: push vs SMS vs WhatsApp usage over time
- RSVP rate for events: engagement with institution events
- Acknowledgement completion rate for mandatory communications

---

## 12. Strategic Features

### 12.1 Smart Send-Time Optimisation

ML model per audience segment:
- Trains on 90 days of historical open-rate data
- Features: day of week, time of day, audience type (parent vs student vs staff), announcement category
- Recommendation shown at composition: "Best time to send to Class 10 parents: Wednesday 6–7 PM (72% average open rate)"
- Sender can follow or override
- Auto-schedule option: set send time to recommended window automatically

### 12.2 Announcement Fatigue Prevention

System monitors recipient-level notification load:
- If any recipient would receive >5 announcements in 24 hours → sender alerted
- Suggestion: consolidate into one digest announcement
- Digest template: "Here are today's updates: [1] ... [2] ... [3] ..."
- Reduces notification muting behaviour; protects channel effectiveness

### 12.3 Two-Way Replies (Select Types)

For specific announcement types:
- RSVP events: "Attending / Not attending" reply inline
- Field trip: permission slip inline
- PTM: "Confirm I'll attend" inline
- Fee reminder: "Pay now" button (deep-link to Module 25)

Replies visible to sender in announcement dashboard. Reduces admin inbox volume.

### 12.4 AI-Assisted Drafting

- Sender types bullet points: "fee due 15 march, last reminder, pay online or counter"
- AI generates formal announcement text in English + regional language
- Sender reviews, edits, approves
- Template saved: if same type sent regularly, AI learns preferred tone
- Reduces drafting time from 10 minutes to < 2 minutes per announcement

### 12.5 Uninstalled App Fallback Chain

- System checks: parent last opened app > 30 days ago
- Flag: "Likely app-inactive"
- For this parent: all Important/Urgent announcements → immediate SMS + email (no push-only)
- Re-engagement: quarterly in-app re-engagement notification; if no action → parent support team follows up
- Ensures no parent is informationally excluded due to app inactivity

### 12.6 Annual Circular Digest

At academic year end:
- All circulars compiled in reference order into one PDF
- Table of contents: date, reference number, subject
- Sent to all parents as "Year Summary — All Circulars AY 2025-26"
- Stored in R2; accessible to new parents/staff joining the following year

---

## 13. Integration Map

| Module | Integration |
|--------|------------|
| Module 03 — RBAC | Role-based audience targeting (all wardens, all teaching staff, etc.) |
| Module 05 — Academic Calendar | Holiday announcements triggered; PTM reminders; exam schedule |
| Module 26 — Fee Defaulters | Audience filter: send reminders only to defaulters |
| Module 31 — Admission | Admission notices; new student group created for announcements |
| Module 32 — Counselling | Wellness announcements; CWSN exam accommodation reminders |
| Module 33 — PTM | PTM announcements, RSVP, reminder notifications |
| Module 35 — Notifications | Push notification dispatch; delivery status feedback |
| Module 36 — WhatsApp | WhatsApp announcement delivery; emergency alerts |
| Module 37 — Email | Formal circular emails; event invitations; achievement recognition |
| Module 38 — SMS & OTP | SMS delivery for Urgent/Emergency; fallback SMS |
| Module 42 — DPDPA & Audit Log | All announcement creation, approval, delivery audited |

---

## 14. Data Model (Key Tables)

```
announcements
  id, tenant_id, title, body, body_translated_json,
  announcement_type, priority, audience_type, audience_ids_json,
  channels_json, status, scheduled_at, published_at, expires_at,
  requires_acknowledgement, created_by, approved_by, approved_at,
  version, parent_id (for amendments), created_at

announcement_versions
  id, announcement_id, version_no, body, body_translated,
  edited_by, edited_at, reason

announcement_deliveries
  id, announcement_id, recipient_id, recipient_type,
  channel, sent_at, delivered_at, opened_at, acknowledged_at,
  failure_reason

announcement_acknowledgements
  id, announcement_id, user_id, user_type, acknowledged_at,
  ip_address

circulars
  id, tenant_id, reference_no, issue_date, subject, addressee,
  body_pdf_r2_key, issued_by, acknowledgement_required,
  status, amendment_of, withdrawn_on, withdrawal_reason,
  academic_year

circular_acknowledgements
  id, circular_id, parent_id, acknowledged_at

inward_circulars
  id, tenant_id, received_date, issuing_authority, reference_no,
  subject, action_required, responsible_person, due_date,
  completed_at, document_r2_key

emergency_alerts
  id, tenant_id, alert_type, message, sent_by, sent_at,
  is_drill, all_clear_sent_at, recipient_count,
  delivery_count, log_immutable

events
  id, announcement_id, event_name, category, event_date,
  event_time_start, event_time_end, venue, organiser_id,
  rsvp_required, rsvp_deadline, capacity, guests_allowed

event_rsvps
  id, event_id, user_id, user_type, response, responded_at,
  guest_count

field_trip_permissions
  id, event_id, student_id, parent_id, signed_at, ip_address,
  permission_granted

mandatory_notices
  id, tenant_id, notice_type, content, last_updated,
  updated_by, version, is_active

announcement_opt_outs
  id, user_id, user_type, announcement_type, opted_out_at,
  opted_back_in_at
```

---

## Cross-Module References

- **Module 03**: Role-based targeting (all wardens, all teaching staff) — read-only
- **Module 05**: Holiday and PTM triggers for auto-announcements — read-only
- **Module 26**: Fee defaulter audience filter — read-only
- **Module 31**: Admission notices; new-enrolment group creation — read + event
- **Module 32**: Wellness/CWSN targeted announcements — read-only
- **Module 33**: PTM RSVP announcements coordinated — read + write
- **Module 35**: Push notification dispatch and delivery tracking — write
- **Module 36**: WhatsApp announcement and emergency delivery — write
- **Module 37**: Email circular delivery, open tracking — write
- **Module 38**: SMS delivery for urgent/emergency; fallback SMS — write
- **Module 42**: All announcement creation, approval, and delivery audited — write

---

*Module 34 complete. Next: Module 35 — Notifications (In-app & FCM).*
