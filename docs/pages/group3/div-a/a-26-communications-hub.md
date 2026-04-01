# A-26 — Principal's Communication Hub

> **URL:** `/school/admin/communications/`
> **File:** `a-26-communications-hub.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Principal (S6) — full · Admin Officer (S3) — full (manage + dispatch) · VP Academic (S5) — view + compose circulars · VP Admin (S5) — view + compose circulars

---

## 1. Purpose

Central hub for all outbound and inbound institutional communication. The Principal uses this to broadcast school-wide announcements to parents and staff, manage the circular dispatch schedule, track message delivery, respond to escalated parent queries, and see the school's communication history.

---

## 2. Page Layout

### 2.1 Tab Bar
```
[Compose & Send] [Scheduled Queue] [Sent History] [Inbox / Inbound] [Templates]
```

---

## 3. Tab: Compose & Send

**Multi-step composer:**

**Step 1: Content**
- Type: Announcement · Circular · Reminder · Emergency · General
- Subject line (mandatory)
- Message body: rich text editor
- Attachments: PDF/images (max 5MB each, 3 files)

**Step 2: Recipients**
- All parents (entire school)
- All staff (entire school)
- Specific classes (multi-select: Class I, Class II, … Class XII)
- Specific sections
- Specific role: only class teachers, only HODs, etc.
- Custom: upload CSV with phone numbers

**Step 3: Channels**
- WhatsApp (business API): ✅ tick if WhatsApp gateway subscribed
- SMS
- In-app notification (student app / parent portal)
- Email (if email IDs available)
- Toggle per channel; delivery estimate shown

**Step 4: Schedule**
- Send now
- Schedule: [Date] [Time] picker
- Recurring: daily/weekly/monthly (for fee reminders etc.)

**Step 5: Preview & Send**
- Per-channel preview (WhatsApp: 1024 char limit; SMS: 160 chars per segment)
- Recipient count: "Sending to 842 parents via WhatsApp + 784 via SMS"
- [Send Now / Schedule] button

---

## 4. Tab: Scheduled Queue

| Message | Audience | Scheduled For | Channels | Status | Action |
|---|---|---|---|---|---|
| Fee Reminder — April | All parents | 1 Apr 2026, 9 AM | WhatsApp · SMS | Scheduled | [Edit] [Cancel] |
| Sports Day Reminder | All parents + staff | 5 Apr 2026, 8 AM | WhatsApp · In-app | Scheduled | [Edit] [Cancel] |

---

## 5. Tab: Sent History

| Date | Subject | Type | Audience | WhatsApp | SMS | In-app | Delivery % |
|---|---|---|---|---|---|---|---|
| 25 Mar 2026 | Exam Result — Class IX | Announcement | 312 parents | 304/312 (97.4%) | 308/312 (98.7%) | 256/312 (82.1%) | 97.4% |
| 22 Mar 2026 | Fee Reminder — March | Reminder | 842 parents | 821/842 (97.5%) | 836/842 (99.3%) | — | 97.5% |

[Resend Failed] per message.

---

## 6. Tab: Inbox / Inbound

Parent and staff replies to school communications (WhatsApp replies) are captured here:

| From | Type | Message Preview | Date | Status | Assigned To |
|---|---|---|---|---|---|
| Parent (Aryan Sharma's father) | Reply to Exam Result | "Can we discuss the marks?" | 25 Mar | Open | [Assign to VP Academic] |
| Parent (Priya's mother) | Fee Query | "When is the last date for payment?" | 24 Mar | Closed | — |

[Assign] to VP/counsellor/accountant for follow-up.

---

## 7. Tab: Templates

Pre-saved message templates:
- Fee Reminder (WhatsApp)
- Exam Date Notification
- PTM Invitation
- Result Available Notification
- Emergency Closure
- Holiday Announcement
- Bus Delay Alert

[+ Create Template] · [Edit] · [Preview] per template

---

## 8. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `POST` | `/api/v1/school/{id}/communications/send/` | Send/schedule message |
| 2 | `GET` | `/api/v1/school/{id}/communications/scheduled/` | Scheduled queue |
| 3 | `DELETE` | `/api/v1/school/{id}/communications/scheduled/{id}/` | Cancel scheduled |
| 4 | `GET` | `/api/v1/school/{id}/communications/sent/` | Sent history |
| 5 | `GET` | `/api/v1/school/{id}/communications/sent/{id}/delivery-stats/` | Delivery stats |
| 6 | `GET` | `/api/v1/school/{id}/communications/inbox/` | Inbound messages |
| 7 | `GET` | `/api/v1/school/{id}/communications/templates/` | Templates |
| 8 | `POST` | `/api/v1/school/{id}/communications/templates/` | Create template |

---

*Last updated: 2026-03-26 · Group 3 — School Portal · Division A*
