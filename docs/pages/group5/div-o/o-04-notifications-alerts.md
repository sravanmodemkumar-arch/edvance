# O-04 — Notifications & Alerts

> **URL:** `/coaching/student-portal/notifications/`
> **File:** `o-04-notifications-alerts.md`
> **Priority:** P2
> **Roles:** Student (self) · Branch Manager (K6) · System (automated)

---

## 1. Notification Centre

```
NOTIFICATION CENTRE — Akhil Kumar (TCC-2401)
As of 31 March 2026

  UNREAD (2):
  ┌──────────────────────────────────────────────────────────────────────┐
  │  🔔 [Today 9:00 AM]  Mock #26 scheduled for 5 April 2026           │
  │     "SSC CGL Full Mock Test #26 — Hall A — 9:00 AM to 12:00 PM     │
  │      Reporting time: 8:45 AM. Bring your ID card."                  │
  │                                        [Mark as read] [View details] │
  ├──────────────────────────────────────────────────────────────────────┤
  │  🔔 [30 Mar 11:00 AM]  Online batch feedback survey open            │
  │     "Online Batch Experience Survey — due 5 April 2026.             │
  │      Your feedback helps us improve. Takes 5 minutes."              │
  │      [Take Survey Now]                 [Dismiss]                    │
  └──────────────────────────────────────────────────────────────────────┘

  READ (recent):
    30 Mar 10:30 AM — Mock #25 result published: 186/200 (Rank #1) ✅
    30 Mar 9:00 AM  — Rank Certificate request received (TCC-RCP tracking)
    28 Mar 8:00 AM  — Class reminder: Quant — Data Tables (9:00 AM today)
    25 Mar 4:00 PM  — Fee receipt for Mar 2026 (no balance due) ✅
    22 Mar 10:00 AM — Doubt answered: "Pipe & Cistern Q#48" [View answer]
```

---

## 2. Notification Types & Channels

```
NOTIFICATION TYPES — TCC Student Portal

  Category          │ Examples                               │ Channel       │ Timing
  ──────────────────┼────────────────────────────────────────┼───────────────┼──────────────
  ACADEMIC          │ Test result published                   │ App + WA + Email│ Immediate
                    │ New study material uploaded             │ App + WA      │ Immediate
                    │ Doubt answered (by faculty)             │ App + WA      │ Immediate
                    │ Rank change notification                │ App           │ Within 1hr
  SCHEDULE          │ Class reminder (tomorrow's class)       │ App + WA      │ 8 PM prior day
                    │ Mock test reminder (3 days before)      │ App + WA      │ 9 AM, D-3
                    │ Class cancellation / reschedule         │ App + WA + SMS│ Immediate
  FINANCIAL         │ Fee due reminder                        │ App + WA      │ 7 days before
                    │ Payment receipt confirmation            │ App + WA + Email│ Immediate
                    │ Overdue fee escalation                  │ App + WA      │ Each 7 days
  WELFARE           │ Counsellor response (to query)          │ App           │ Immediate
                    │ Welfare program update                  │ App           │ As needed
  OPERATIONAL       │ Exam registration (external) reminder   │ App + WA      │ 15 days before
                    │ PTM invite                              │ App + WA      │ 7 days before
                    │ Survey invitation                       │ App + WA      │ Survey open date
  EMERGENCY         │ Safety alert (branch or hostel)         │ App + WA + SMS│ Immediate (all)
  MARKETING         │ Batch opening (if opted in)             │ WA + Email    │ Scheduled
```

---

## 3. Broadcast Management

```
BROADCAST MANAGEMENT — Branch Manager View

  SEND NOTIFICATION:
    To:           [All students ▼]  (or: specific batch, hostel only, etc.)
    Channel:      [✅ App] [✅ WhatsApp] [  Email] [  SMS]
    Message type: [Academic ▼]
    Title:        [Mock Test #26 — Reminder                              ]
    Body:         [SSC CGL Full Mock Test #26 is scheduled for 5 April 2026, 9:00 AM in Hall A.
                   Reporting time is 8:45 AM. Please carry your TCC ID card.
                   No phones allowed in the exam hall.                   ]
    Scheduled:    (●) Now  (○) Schedule: [____]
    Preview:      [Preview as student]  [Send to test user first]

  RECENT BROADCASTS (sent by admin):
    31 Mar 9:00 AM  — Mock #26 schedule (all SSC CGL students: 276) ✅ Sent
    28 Mar 8:00 AM  — March monthly progress report available (all: 856) ✅ Sent
    25 Mar 4:00 PM  — Fee receipts sent (individually auto-triggered) ✅
    22 Mar 5:00 PM  — Survey invitation — Online Batch (392 students) ✅ Sent
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/student-portal/notifications/` | Student's notification inbox |
| 2 | `PATCH` | `/api/v1/coaching/{id}/student-portal/notifications/{nid}/read/` | Mark as read |
| 3 | `POST` | `/api/v1/coaching/{id}/notifications/broadcast/` | Send broadcast (admin only) |
| 4 | `GET` | `/api/v1/coaching/{id}/notifications/broadcast/log/` | Broadcast send log |
| 5 | `GET` | `/api/v1/coaching/{id}/notifications/templates/` | Notification templates |

---

## 5. Business Rules

- Notification volume must be calibrated to avoid fatigue; a student who receives 8 WhatsApp messages from TCC per day will mute the number or block TCC's messages, defeating the purpose; the notification design principle is: send what matters, when it matters, through the right channel; a class schedule reminder is valuable; a "check out our new blog post" notification is not; the marketing and academic notification streams are separate — marketing opt-out (O-03 settings) stops promotional messages but never stops academic or safety notifications
- Class cancellation notifications must reach students at least 2 hours before the class time (target: 24 hours); a student who commutes 45 minutes to reach TCC and finds the class cancelled on arrival has wasted 1.5 hours of travel time and is justifiably upset; WhatsApp + SMS for class cancellation (both channels) ensures delivery even if the student hasn't opened the app; the faculty member cancelling a class must notify the Branch Manager immediately so the notification can be sent; same-day morning cancellations (before 8:30 AM) are treated as an emergency communication
- Emergency safety alerts bypass all notification preferences and DND settings; a fire in the hostel, a security incident at the branch, or a city-wide curfew affecting student movement must reach every student and parent simultaneously; the emergency alert uses all channels (app push, WhatsApp, SMS) regardless of the student's channel preferences; the Branch Manager is the only person authorised to trigger an emergency alert; a false alarm (accidental trigger) must be followed immediately by a correction message; students must be trained (orientation) to take emergency alerts seriously and not dismiss them as spam
- WhatsApp broadcast messages are sent using the Meta Business API with pre-approved templates (L-04); the Branch Manager composes the message using these templates; freeform messages outside approved templates cannot be sent via API to non-contacts (TRAI/Meta policy); if TCC needs to send an urgent message outside an approved template (emergency situation), the fallback is individual WhatsApp messages (limited to TCC's direct contacts) or SMS; the pre-approved template library must include a general-purpose emergency template to handle unforeseen situations
- Notification delivery receipts are logged for important communications; for fee due reminders and exam notices, TCC tracks delivery status (delivered/read/failed) per student; a student who claims "I didn't know about the fee due date" when TCC has a delivery receipt showing the WhatsApp message was read 6 days earlier has a weaker claim; the delivery log is also used to resend failed deliveries (phone off, signal issue); the system automatically retries failed deliveries 3 times before marking as undelivered and flagging the student's contact for manual follow-up

---

*Last updated: 2026-03-31 · Group 5 — Coaching Portal · Division O*
