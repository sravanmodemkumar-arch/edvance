# F-04 — SMS & Email Campaigns

> **URL:** `/school/sms-email/`
> **File:** `f-04-sms-email-campaigns.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Communication Coordinator (S3) — send campaigns · Academic Coordinator (S4) — approve · Principal (S6) — official communications

---

## 1. Purpose

SMS and Email serve as fallback channels when WhatsApp is unavailable, and as primary channels for specific use cases:
- **SMS:** Reaches parents without smartphones or WhatsApp (common in semi-urban/rural areas); mandatory for critical safety alerts (E-F10 emergency); regulatory compliance when WhatsApp delivery cannot be confirmed
- **Email:** Professional communications (circulars with attachments, detailed notices, fee statements); parents prefer email for record-keeping of important documents; mandatory for government-scheme parents who submit email-linked bank accounts
- **School-to-government:** CBSE, state education department, UDISE communications often require email

WhatsApp (F-03) is primary; SMS/Email are supplementary. This module manages bulk campaigns on both channels.

---

## 2. Page Layout

### 2.1 Header
```
SMS & Email Campaigns                                [+ New SMS Campaign]  [+ New Email Campaign]
Month: March 2026

SMS This Month: 342 messages  ·  Delivered: 334 (97.7%)
Email This Month: 89 messages  ·  Opened: 52 (58.4%)  ·  Bounced: 3 (3.4%)
```

### 2.2 Campaign History
```
Date        Type   Campaign Name                  Recipients  Delivered  Status
27 Mar 2026  SMS   Daily absent alert (fallback)       3           3/3    ✅
22 Mar 2026  SMS   Fee reminder (WhatsApp failed)       8           7/8    ✅
20 Mar 2026  Email  Annual report to parents (XI)      45          43/45   ✅
15 Mar 2026  Email  Scholarship application circular    38          37/38   ✅
10 Mar 2026  SMS   PTM reminder (all parents)         380         371/380  ✅
```

---

## 3. SMS Campaign

### 3.1 Create SMS Campaign
```
[+ New SMS Campaign]

Campaign name: [Fee reminder — Outstanding parents (22 Mar)]
SMS Type:
  ● Transactional (DLT registered — higher delivery, no promotional content)
  ○ Promotional (OTP exempted sender ID — blocked during DND hours)

Note: All SMS must use DLT-registered templates (TRAI regulation, India).
DLT registration is per school; EduForge pre-registers common templates.

Select Template (DLT-approved):
  ● SMS-T01: fee_reminder — "Dear Parent, fee of Rs.{amount} for {name} is due by
    {date}. Contact school: {phone}. — {school}"
  ○ SMS-T02: attendance_alert — "ALERT: {name} absent today {date}. — {school}"
  ○ SMS-T03: exam_notice — "{name}'s exam on {date}. Report {time}. — {school}"
  ○ SMS-T04: general_notice — "Important notice from {school}: {message} (max 120 chars)"
  ○ Custom (must be DLT-registered first — 3-5 working days)

Recipients: 8 parents (WhatsApp failed for these)
Auto-fill variables from student data: ☑ Yes

Preview (personalised):
  "Dear Parent, fee of Rs.8,500 for Vijay is due by 31 Mar 2026.
   Contact school: 040-23456789. — Greenfields School"
  (160 characters — 1 SMS unit)

[Send Now]  [Schedule]
```

### 3.2 DLT Compliance Note
```
⚠️ TRAI DLT (Distributed Ledger Technology) Requirement:
  All commercial SMS in India must be registered on TRAI's DLT platform.
  EduForge pre-registers common school templates.
  Custom messages outside templates require new DLT registration (3-5 days).

DLT registration status:
  Sender ID: "EDUFRG" (EduForge shared)  OR  school's own sender ID
  Registered templates: 12  ·  Pending: 0
  [Manage DLT Registration]
```

---

## 4. Email Campaign

### 4.1 Create Email Campaign
```
[+ New Email Campaign]

Campaign name: [Annual Exam Schedule — Class XI (March 2026)]
From name: [Greenfields School — Administration      ]
From email: [admin@greenfields.edu.in] (must be verified domain)
Reply-to: [principal@greenfields.edu.in]

Subject: [Annual Examination Schedule — Class XI — 2026-27]
         Character count: 52/60 ✅

Email body (WYSIWYG editor):
  ┌─────────────────────────────────────────────────────────┐
  │  [School Logo]                                           │
  │                                                          │
  │  Dear Mr./Ms. {parent_name},                             │
  │                                                          │
  │  Please find attached the Annual Examination Schedule   │
  │  for Class XI (2026-27). {student_name} is enrolled in  │
  │  Class XI-A.                                             │
  │                                                          │
  │  Key dates:                                              │
  │  - Exam begins: 1 April 2026                             │
  │  - Last exam: 30 April 2026                              │
  │                                                          │
  │  For any queries, contact: 040-23456789                  │
  │                                                          │
  │  Regards,                                                │
  │  [Principal Name], Principal                             │
  │  Greenfields School                                      │
  └─────────────────────────────────────────────────────────┘

Attachments: exam_schedule_xi.pdf (220 KB) ✅ (max 2 MB per email)

Personalisation tokens available:
  {parent_name}, {student_name}, {class}, {roll_no}, {fee_outstanding}

Recipients: Parents of Class XI (45 students with email registered)
  Note: 12 parents have no email on record → [Send via WhatsApp instead]

[Preview for Anjali Das]  [Send Test to self]  [Schedule]  [Send Now]
```

### 4.2 Email Analytics
```
Email Analytics — Annual Exam Schedule (20 Mar 2026)

Sent:     45
Delivered: 43  (2 bounced — invalid email)
Opened:   38 (88.4%)   ← 1st open within 1 hour: 22 (51%)
Clicked:  12 (attachment downloaded)
Bounced:   2  → [Update email in C-05]
Unsubscribed: 0

Device breakdown: Mobile 74%  ·  Desktop 26%
Open time distribution: 8-10 AM: 45%  ·  6-8 PM: 35%  ·  Other: 20%
```

---

## 5. SMS Delivery Failure Report

```
SMS Failures — March 2026

Parent          Number          Failure           Action
Parent of Ravi  +91 9876-XXXXX  Invalid number    [Update in C-05]
Parent of Sita  +91 8765-XXXXX  DND registered    [Try email / WhatsApp]
Parent of Meena +91 7654-XXXXX  Number not active [Contact admin to update]

DND (Do Not Disturb) note:
  TRAI DND-registered numbers cannot receive promotional SMS.
  Transactional SMS (fee receipts, exam alerts) are DND-exempt.
  Promotional SMS (event invitations) are blocked on DND numbers.
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/sms-email/campaigns/?month={m}&year={y}` | Campaign history |
| 2 | `POST` | `/api/v1/school/{id}/sms-email/sms/` | Send SMS campaign |
| 3 | `POST` | `/api/v1/school/{id}/sms-email/email/` | Send email campaign |
| 4 | `GET` | `/api/v1/school/{id}/sms-email/campaigns/{campaign_id}/analytics/` | Campaign analytics |
| 5 | `GET` | `/api/v1/school/{id}/sms-email/dlt-templates/` | DLT-registered templates |
| 6 | `GET` | `/api/v1/school/{id}/sms-email/delivery-failures/?month={m}&year={y}` | Failure report |

---

## 7. Business Rules

- All SMS use DLT-registered templates (TRAI requirement); free-form SMS are not sent through the system to avoid TRAI compliance violations
- Promotional SMS cannot be sent to DND-registered numbers (10 PM–9 AM blocked regardless); transactional SMS (critical alerts, receipts) are exempt from DND and time restrictions
- Email sender domain must be verified (SPF/DKIM) to avoid spam classification; EduForge provides a shared `notifications@eduforge.in` domain for schools without their own domain, but schools with `school.edu.in` domains should configure their own
- Email addresses are validated at collection (C-05) with a format check; periodic bounce cleanup removes invalid addresses from the active list
- DPDPA compliance: parent email and phone are used only for school-related communication; not shared with third parties; unsubscribe link in all marketing emails is mandatory (transactional emails do not need unsubscribe)

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
