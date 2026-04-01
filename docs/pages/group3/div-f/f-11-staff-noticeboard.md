# F-11 — Internal Staff Noticeboard

> **URL:** `/school/staff-notices/`
> **File:** `f-11-staff-noticeboard.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P2
> **Roles:** Administrative Officer (S3) — post operational notices · Academic Coordinator (S4) — academic notices · Principal (S6) — official staff notices · All staff (S1+) — view and acknowledge

---

## 1. Purpose

Internal communication channel for staff — notices that should not be visible to parents or students. Separate from F-01 (which is parent-visible). Use cases:
- **Staff meeting notices** (date, agenda, mandatory attendance)
- **Policy changes** (leave policy update, dress code, duty roster)
- **Administrative notices** (salary processing date, holiday declaration, PTM preparation)
- **Academic notices** (exam paper submission deadline, result entry deadline, syllabus completion deadline)
- **Principal circulars to staff** (formal numbered notices)
- **Training announcements** (CPD — Continuing Professional Development sessions; CBSE online training)

---

## 2. Page Layout

### 2.1 Header
```
Staff Noticeboard                                    [+ Post Notice]
Date: 27 March 2026

Unread by me: 2 notices  ·  Posted this week: 5  ·  Pending acknowledgement: 1
```

### 2.2 Notice List (Staff View)
```
📌 PINNED
──────────────────────────────────────────────────────────────────────
  📋 Annual Exam Duty Roster — April 2026        Posted 22 Mar 2026  ⬜ Not read
     Posted by: Admin Officer  ·  Audience: All Teaching Staff
     [View]  [Acknowledge Required ← must read before 28 Mar]

RECENT NOTICES
──────────────────────────────────────────────────────────────────────
  📅 Staff Meeting — 30 Mar 2026 (Monday) 2 PM   Posted 25 Mar 2026  ✅ Read
     Venue: Conference Room  ·  Agenda: Annual exam preparation
     [View]

  💰 March Salary — Processing on 29 Mar         Posted 20 Mar 2026  ✅ Read
     [View]

  📚 Results Entry Deadline — B-16 by 5 Apr      Posted 18 Mar 2026  ✅ Read
     [View]
```

---

## 3. Post Notice

```
[+ Post Notice]

Title: [Annual Exam Duty Roster — April 2026        ]
Category: ● Administrative  ○ Academic  ○ Policy  ○ HR/Payroll  ○ Training  ○ Urgent

Audience:
  ● All staff
  ○ Teaching staff only
  ○ Non-teaching staff only
  ○ Specific role groups: [Class Teachers / Subject Teachers ▼]
  ○ Specific department: [Science / Commerce / Arts ▼]

Content:
  ┌──────────────────────────────────────────────────────────────────────┐
  │ Dear Staff,                                                           │
  │                                                                       │
  │ Please find attached the Annual Exam Invigilation Duty Roster for    │
  │ April 2026. Kindly check your assigned duties and report to the exam  │
  │ hall 15 minutes before the exam.                                      │
  │                                                                       │
  │ Any scheduling conflicts must be reported to Admin Officer by         │
  │ 28 March 2026.                                                        │
  │                                                                       │
  │ Regards, [Admin Officer Name]                                         │
  └──────────────────────────────────────────────────────────────────────┘

Attachments: exam_duty_roster_apr2026.pdf

Acknowledgement required: ☑ Yes — deadline: 28 March 2026

Notify via:
  ☑ In-app notification
  ☑ Staff WhatsApp group (EduForge sends via bot — not personal WhatsApp)
  ☐ SMS

[Post Notice]
```

---

## 4. Staff Acknowledgement Tracking

```
Acknowledgement Status — Annual Exam Duty Roster

Total staff: 48  ·  Required: All Teaching Staff (38)
Acknowledged: 22/38 (58%)  ·  Not yet: 16

Deadline: 28 March 2026 (Tomorrow)

Staff who have NOT acknowledged:
  Ms. Anita Reddy (XI-A Class Teacher) — Not read
  Mr. Ravi Kumar (Science) — Not read
  ...

[Send Reminder to Non-Acknowledged Staff]  ← WhatsApp + in-app notification

Auto-reminder sent if deadline approaching: ☑ 24 hours before deadline
```

---

## 5. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/staff-notices/?role={role}` | Notices visible to current role |
| 2 | `POST` | `/api/v1/school/{id}/staff-notices/` | Create staff notice |
| 3 | `POST` | `/api/v1/school/{id}/staff-notices/{notice_id}/acknowledge/` | Staff acknowledges notice |
| 4 | `GET` | `/api/v1/school/{id}/staff-notices/{notice_id}/ack-status/` | Acknowledgement tracking |
| 5 | `POST` | `/api/v1/school/{id}/staff-notices/{notice_id}/remind/` | Remind non-acknowledged |

---

## 6. Business Rules

- Staff notices are never visible to parents or students — they are strictly internal; any notice accidentally posted as staff-only that contains parent-sensitive content must be retracted immediately
- Acknowledgement is tracked per staff member; for critical operational notices (duty rosters, exam instructions), non-acknowledgement by deadline is escalated to the Academic Coordinator/Principal
- HR/Payroll notices (salary dates, leave balance updates) are visible only to the specific staff member, not all staff (individual vs broadcast)
- Notices are retained for 2 years; HR-related notices for 5 years

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
