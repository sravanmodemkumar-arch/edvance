# E-16 — Parent Absence Notifications

> **URL:** `/school/attendance/notifications/`
> **File:** `e-16-parent-absence-notifications.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Class Teacher (S3) — own class · Administrative Officer (S3) — configure templates · Academic Coordinator (S4) — bulk campaigns + escalations · Principal (S6) — final warning notices

---

## 1. Purpose

Manages outbound communication to parents specifically about their child's attendance. While E-09 shortage alerts manage the school-side view and action tracking, E-16 manages the notification dispatch system — the templates, delivery channels, schedules, and delivery confirmations. Distinct capabilities:
- **Day-level absent notification:** Auto-sent when a student is marked absent each day (optional, school-configurable)
- **Weekly summary:** Each Sunday, parents receive the week's attendance summary
- **Threshold alerts:** When student crosses 85%, 75%, 65% attendance thresholds (fed from E-09)
- **Bulk campaigns:** Academic Coordinator sends reminder to all parents of below-threshold students
- **Demand notices:** Formal written notices for chronic absentees
- **Two-way acknowledgement:** Parent must acknowledge critical notices (legal protection for school)

---

## 2. Page Layout

### 2.1 Header
```
Parent Absence Notifications                     [+ Send Custom Notice]  [Bulk Campaign]
Academic Year: [2026–27 ▼]   Month: [March 2026 ▼]

Today's Notifications: 12 sent  ·  Delivery failures: 1
This Month: 284 messages sent  ·  Open rate: 87%  (WhatsApp delivery receipts)
Pending acknowledgements: 3 (critical notices requiring parent confirmation)
```

### 2.2 Notification Log
```
Filter: [All ▼]  Type: [All ▼]  Class: [All ▼]  Status: [All ▼]

Timestamp           Student         Class  Type              Channel    Status
27 Mar 2026 09:15   Vijay S.        X-B   Daily absent       WhatsApp   ✅ Delivered
27 Mar 2026 09:15   Meena D.       XII-A  Daily absent       WhatsApp   ✅ Delivered
27 Mar 2026 09:15   Chandana Rao   XI-A   Daily absent       WhatsApp   ❌ Failed (number invalid)
26 Mar 2026 18:00   Suresh K.       IX-A  Weekly summary     WhatsApp   ✅ Read
25 Mar 2026 11:30   Chandana Rao   XI-A   Critical alert     WhatsApp   ⬜ Sent (unread)
20 Mar 2026 10:00   Vijay S.        X-B   Danger — Final     WhatsApp   ✅ Delivered (unread)
15 Mar 2026 09:00   All 28 at-risk  —     Bulk reminder      WhatsApp   26/28 delivered
```

---

## 3. Notification Types & Triggers

### 3.1 Automatic Daily Absent Notification
```
Configuration (per school):
  ☑ Send daily absent notification (configurable ON/OFF)
  Trigger: Student marked Absent in E-01 daily attendance (after submit, not draft)
  Timing: Immediately after Class Teacher submits E-01 (typically 8:30–9:00 AM)
  Channel: WhatsApp (primary)  ·  SMS (fallback if WhatsApp fails)

Message template (editable):
  "Dear Parent, your ward [Student Name], Class [Class], was absent from school today
  [Date]. If this is unplanned, please contact the class teacher. — [School Name]"

Exclusions:
  → Medical leave (E-04) already approved: no notification (parent already aware)
  → On-duty (E-04): no notification
  → Holiday (E-15): attendance not taken, no notification
  → Pre-approved leave: no notification
```

### 3.2 Weekly Attendance Summary
```
Configuration:
  ☑ Send weekly summary every Sunday evening (6:00 PM)
  Includes:
    → Days present this week: [N] / [N working days]
    → Year-to-date attendance: [X%]
    → Running status: ✅ Eligible / ⚠️ Warning / 🔴 At risk

Template:
  "Dear Parent, Arjun Sharma's attendance this week: 4/5 days (Mon–Fri).
  Year-to-date: 87% ✅ Eligible. Minimum required: 75%.
  — [School Name]"
```

### 3.3 Threshold Alert Notifications (from E-09)
```
Threshold  Trigger Condition           Message Tone    Approval Required
Warning     Student falls below 85%    Informational   Auto (no approval)
Critical    Student falls below 75%    Urgent          Auto (no approval)
Danger      Student falls below 65%    Final warning   Principal review before send
             (or cannot reach 75%)
```

### 3.4 Demand Notice (Formal Written Communication)
```
Triggered from: E-09 [Generate Parent Notice] or D-10 fee demand (separate)

Format options:
  ● WhatsApp (immediate, informal proof of delivery)
  ● PDF letter (printable, requires parent signature)
  ● Registered post (for court-admissible proof)

Level 1 (Warning):
  "Dear [Parent Name], this is to inform you that [Student Name], Class [Class],
  has [X%] attendance this academic year. The minimum required by CBSE is 75%.
  We request you to ensure regular attendance. Please contact the class teacher
  if there is any specific reason for absence. — [Principal], [School Name]"

Level 2 (Critical — requires parent acknowledgement):
  "IMPORTANT NOTICE: [Student Name]'s attendance is [X%] — at risk of being
  debarred from the annual examination. You are requested to meet the Principal
  within 7 days. Failure to do so will result in further action as per school rules."
  → Parent must tap "I Acknowledge" in WhatsApp (interactive button)
  → If no acknowledgement in 3 days → system flags for phone call follow-up

Level 3 (Danger / Final):
  "FINAL NOTICE: [Student Name]'s attendance is [X%] which is below the minimum
  required. He/She may be debarred from appearing in the [Annual/Board] examination.
  Please meet the Principal IMMEDIATELY. — [Principal Name], [School Name]"
  → Principal reviews and approves before sending
  → Sent as both WhatsApp AND physical letter (registered post)
  → Delivery confirmation tracked (postal acknowledgement)
```

---

## 4. Bulk Campaign

```
[Bulk Campaign] → wizard:

Step 1 — Select Recipients
  ● Students below 75%  (8 students)
  ○ Students below 85%  (25 students)
  ○ Students absent 3+ consecutive days
  ○ Custom filter: [Absent > 15 days this month]
  ○ Entire class(es): [Select class ▼]

Step 2 — Choose Template
  ○ Daily absent reminder
  ● Attendance shortage warning
  ○ Meeting invitation (PTM)
  ○ Custom message [Text field]

Step 3 — Channel
  ● WhatsApp  ○ SMS  ○ Both  ○ App notification

Step 4 — Schedule
  ● Send immediately
  ○ Schedule: [Date] [Time]

Step 5 — Preview
  Preview message for: Suresh K. (IX-A, 71.7%):
  "Dear Parent, URGENT: Suresh Kumar's attendance is 71.7% this academic year.
  CBSE requires minimum 75% for exam eligibility. He needs to attend school
  every day without fail. Please contact class teacher Mr. Vijay at [phone].
  — Principal, [School Name]"

  [Send to 8 students]
```

---

## 5. Delivery Failure Handling

```
Delivery Failures — 27 Mar 2026

Student         Parent Number   Failure Reason          Action
Chandana Rao    +91 9876-XXXXX  WhatsApp not registered  [Try SMS]  [Update Number]
Ravi K.         +91 8765-XXXXX  Invalid number (7 digits) [Alert Admin to fix]

Fallback options:
  1. SMS fallback (auto, if WhatsApp fails and SMS fallback is enabled)
  2. Email (if parent email registered in C-05)
  3. App notification (if parent has installed parent app)
  4. Manual phone call log: [Log Call Attempt] → staff manually called parent

Monthly delivery stats:
  WhatsApp delivered: 94.2%
  SMS fallback delivered: 3.1%
  Failed (no valid contact): 1.4%  → 3 families flagged for contact update
  App notification: 1.3%
```

---

## 6. Two-Way Interaction Log

When parents respond to notifications:

```
Parent Responses — March 2026

Student         Date        Parent Response                       Handled By
Chandana Rao   15 Mar 26   "She has been sick — medical cert      Class Teacher
                            attached (photo)"                     [View Photo] [Approve Leave]
Vijay S.       20 Mar 26   "We are aware, he is appearing for     Logged; Academic Coord
                            state-level chess tournament"         [Mark On-Duty] [Escalate]
Meena D.       22 Mar 26   No response (3 messages unread)        [Escalate: Phone call]
```

---

## 7. PTM Attendance Reminder (Pre-Meeting Notification)

```
PTM Notification Campaign:

Event: Parent-Teacher Meeting — Class XI (8 Mar 2026, 9 AM – 1 PM)
Target: Parents of Class XI students

Message:
  "Dear Parent, Parent-Teacher Meeting for Class XI is scheduled on 8 Mar 2026
  (Sunday) from 9 AM to 1 PM. Your ward's attendance report, academic progress,
  and exam preparation will be discussed. Kindly confirm attendance:
  [YES, I will attend] [NO, I cannot attend]  — [School Name]"

RSVP summary (day before PTM):
  Confirmed: 38/45 parents  (84%)
  Not attending: 4  → Class Teacher to call individually
  No response: 3
```

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/attendance/notifications/?month={m}&year={y}` | Notification log |
| 2 | `POST` | `/api/v1/school/{id}/attendance/notifications/send/` | Send custom notice (single student) |
| 3 | `POST` | `/api/v1/school/{id}/attendance/notifications/bulk/` | Bulk campaign |
| 4 | `GET` | `/api/v1/school/{id}/attendance/notifications/templates/` | Notification templates |
| 5 | `PATCH` | `/api/v1/school/{id}/attendance/notifications/templates/{id}/` | Update template |
| 6 | `GET` | `/api/v1/school/{id}/attendance/notifications/delivery-failures/?month={m}&year={y}` | Failed deliveries |
| 7 | `GET` | `/api/v1/school/{id}/attendance/notifications/{student_id}/log/` | Per-student notification history |
| 8 | `POST` | `/api/v1/school/{id}/attendance/notifications/config/` | School-level notification settings |

---

## 9. Notification Configuration (Admin)

```
Notification Settings — [School Name]

Daily absent notification:      ☑ Enabled   Timing: [After E-01 submit ▼]
Weekly summary:                 ☑ Enabled   Day: Sunday  Time: 6:00 PM
Warning threshold (85%) alert:  ☑ Enabled   Frequency: Once per crossing
Critical threshold (75%) alert: ☑ Enabled   Frequency: Once per crossing + monthly reminder
Danger (<65%) alert:            ☑ Enabled   Requires Principal review before send

WhatsApp integration:  ☑ Connected (via Interakt / Meta Business API)
SMS fallback:          ☑ Enabled (via MSG91)  ← only fires if WhatsApp fails
App push notification: ☑ Enabled (if parent app installed)

Parent response handling: ☑ Log all incoming replies in notification log
                          ☑ Alert Class Teacher if parent sends document (leave evidence)
```

---

## 10. Business Rules

- Daily absent notifications are sent only after E-01 is in submitted state (not draft) — this prevents false alarms from teachers who have partially filled the register
- If a student's absence is converted to Medical Leave (E-03 correction) after the daily notification has already been sent, the system sends a follow-up correction message: "We note that [Name]'s absence on [Date] has been updated to Medical Leave. No action needed."
- The school is required to maintain proof of parent notification for CBSE condonation applications (E-11) — the notification log in E-16 serves as this proof
- Parent contact numbers are sourced from C-05 enrollment form; a failed notification flags the student's profile for contact information update
- DPDPA 2023 compliance: parents receive only their child's data; bulk messages are personalised per parent and sent individually (not group messages)
- WhatsApp Business API messages are subject to Meta template approval; demand notice templates must be pre-approved by Meta; EduForge maintains a library of pre-approved templates
- A parent opting out of WhatsApp notifications (via "Stop" reply) must still receive critical/danger notices via SMS or physical letter — CBSE requires documented parent notification for exam eligibility matters

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division E*
