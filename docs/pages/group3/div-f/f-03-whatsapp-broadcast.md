# F-03 — WhatsApp Broadcast Manager

> **URL:** `/school/whatsapp/`
> **File:** `f-03-whatsapp-broadcast.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Communication Coordinator (S3) — send broadcasts · Class Teacher (S3) — own class broadcasts · Academic Coordinator (S4) — approve school-wide campaigns · Principal (S6) — approve urgent/official messages

---

## 1. Purpose

WhatsApp is the dominant communication channel for Indian school-parent communication, with 95%+ delivery rates compared to 40-60% for email. EduForge integrates with the Meta WhatsApp Business API (via approved BSPs — Interakt, Wati, or WATI) to send:
- **Transactional messages** (auto-triggered): daily attendance alerts, fee receipts, exam results, leave approvals
- **Campaign messages** (manual): PTM invitations, circulars, event announcements, fee reminders
- **Alerts** (auto-triggered from E-09, D-09): shortage alerts, fee defaulter escalations

The WhatsApp Broadcast Manager is the school-facing console for managing templates, broadcasts, delivery tracking, and opt-out management. All messages require Meta template approval before use (regulatory requirement of WhatsApp Business API).

---

## 2. Page Layout

### 2.1 Header
```
WhatsApp Broadcast Manager                           [+ New Broadcast]  [Manage Templates]
Month: March 2026

Messages Sent This Month: 2,841
Delivered: 2,790 (98.2%)  ·  Read: 2,340 (82.4%)  ·  Failed: 51 (1.8%)
Opt-outs this month: 3  (cumulative: 12 parents opted out of broadcasts)
```

### 2.2 Broadcast History
```
Date        Broadcast Name                       Recipients  Delivered  Read    Status
27 Mar 2026 Daily absent alert (auto)                 12       12/12    8/12   ✅ Sent
26 Mar 2026 Attendance shortage — Term 2 final        8         8/8     6/8    ✅ Sent
25 Mar 2026 Annual Exam Schedule — Class X           120       117/120  98/120 ✅ Sent
22 Mar 2026 Fee reminder — Due 31 Mar 2026          380       373/380  310/380 ✅ Sent
15 Mar 2026 PTM confirmation reminder — XI           45        43/45   40/45   ✅ Sent
```

---

## 3. Template Manager

```
[Manage Templates] → Template Library:

WhatsApp requires all outbound templates to be pre-approved by Meta.
Template status: Approved / Pending / Rejected

Category: UTILITY (transactional) / MARKETING (promotional) / AUTHENTICATION

─── APPROVED TEMPLATES ─────────────────────────────────────────────────────

ID   Template Name                  Category   Variables           Status
T01  daily_absent_alert             UTILITY    student_name,date   ✅ Approved
T02  attendance_warning             UTILITY    student_name,%      ✅ Approved
T03  attendance_critical            UTILITY    student_name,%      ✅ Approved
T04  attendance_danger_final        UTILITY    student_name,%      ✅ Approved
T05  fee_reminder                   UTILITY    student_name,amount,due_date ✅ Approved
T06  fee_receipt_confirmation       UTILITY    receipt_no,amount   ✅ Approved
T07  exam_schedule_announcement     UTILITY    class,date          ✅ Approved
T08  ptm_invitation                 UTILITY    date,time,slot      ✅ Approved
T09  holiday_notice                 UTILITY    date,holiday_name   ✅ Approved
T10  result_announcement            UTILITY    student_name,class  ✅ Approved
T11  tc_ready_for_collection        UTILITY    student_name        ✅ Approved
T12  fee_defaulter_warning          UTILITY    student_name,amount ✅ Approved
T13  circular_shared                UTILITY    circular_no,title   ✅ Approved
T14  exam_admit_card_ready          UTILITY    student_name,exam   ✅ Approved
T15  custom_announcement            UTILITY    title,body          ✅ Approved

[+ Request New Template] — sends to Meta for approval (2–3 business days)
```

---

## 4. Template Detail & Preview

```
Template: T03 — attendance_critical

Body text (Meta-approved):
  "URGENT: {{1}}'s attendance this year is {{2}}% — at risk of exam disqualification.
  CBSE requires minimum 75%. Please contact the Class Teacher immediately.
  — {{3}} School"

Variables:
  {{1}} = Student first name
  {{2}} = Current attendance %
  {{3}} = School name

Buttons (if applicable):
  [Call Class Teacher] → Click-to-call with class teacher's number
  [View Attendance]    → Deep link to parent portal attendance page

Language: English
Header: None (UTILITY templates — no header allowed by Meta policy)
Footer: "[School Name] — Attendance Alert"

Media attachment: ✅ Can attach PDF (attendance report)

Preview (personalised for Chandana Rao, 60.6%):
  "URGENT: Chandana's attendance this year is 60.6% — at risk of exam disqualification.
  CBSE requires minimum 75%. Please contact the Class Teacher immediately.
  — Greenfields School"
  [Call Class Teacher] [View Attendance]
```

---

## 5. New Broadcast

```
[+ New Broadcast] → wizard:

Step 1 — Select Template
  ● T05 — fee_reminder   "Term 2 Fee Reminder"
  Template preview:
  "Dear Parent, Term 2 school fee of ₹{{1}} for {{2}} is due by {{3}}.
   Please pay at the school counter or online at [portal URL].
   Receipt will be WhatsApped on payment. — {{4}} School"

Step 2 — Select Recipients
  ○ All parents
  ○ Class-wise: [✅ XI-A  ✅ XI-B  ✅ XII-A  ✅ XII-B]
  ● Filter: Fee outstanding > ₹0 as on today (380 → 142 with outstanding)
  ○ Specific students: [Search]

Step 3 — Fill Variables
  Variable fill mode:
  ● Auto-fill from student data (personalised per parent)
    {{1}} = Student's outstanding fee (from D-07 ledger)
    {{2}} = Student name
    {{3}} = 31 March 2026 (due date, manually set)
    {{4}} = School name (auto)
  ○ Same value for all (non-personalised)

Step 4 — Attachments
  ☑ Attach fee statement PDF (D-07 export per student — personalised)
  ☐ No attachment

Step 5 — Schedule
  ● Send immediately
  ○ Schedule: [Date] [Time] (e.g., Monday 8 AM for maximum read rate)

Step 6 — Preview & Confirm
  Sending to: 142 parents (with outstanding fee)
  Cost estimate: 142 messages × ₹0.35/message = ₹49.70 (WhatsApp API cost)
  [Launch Broadcast]
```

---

## 6. Delivery Analytics per Broadcast

```
Broadcast Analytics — Fee Reminder (22 Mar 2026)

Recipients:           142
Sent:                 142
Delivered to device:  139 (97.9%)  ← WhatsApp confirmed delivery
Read (blue ticks):    118 (83.1%)  ← read receipt
Replied:               12 (8.5%)   ← parent replied to message
Errors:                 3 (2.1%)   ← invalid number / WhatsApp not registered

Error details:
  +91 9876-XXXXX — WhatsApp not registered → [SMS fallback sent]
  +91 8765-XXXXX — Invalid number          → [Flag for update in C-05]
  +91 7654-XXXXX — Opted out              → [Skipped — opt-out respected]

Link clicks (if template had URL button):
  "View Outstanding Fee" button clicked: 34 (24%)
  Payments made within 24h of message:  18 parents (correlation, not causation)
```

---

## 7. Opt-Out Management

```
Opt-Out Register (DPDPA + WhatsApp Policy Compliance)

Parents who have replied "STOP" or opted out of broadcasts:
  Parent of Ravi Kumar (XI-A) — opted out 15 Jan 2026 — [Re-enable if consent given]
  Parent of Meena D. (XII-A)  — opted out 3 Mar 2026

Rules:
  → Opted-out parents CANNOT receive marketing/broadcast messages
  → UTILITY messages (receipt confirmation, exam admit card, TC ready) can still be sent
    (these are transactional, not promotional)
  → Attendance shortage alerts (E-09 E-16) are transactional — still sent per CBSE requirement
  → Re-enabling requires fresh consent from parent (WhatsApp / physical form)

[Export Opt-Out List]  [Contact opted-out parents via SMS for consent renewal]
```

---

## 8. Auto-Trigger Configuration

WhatsApp messages that are automatically sent by other modules:

```
Auto-Trigger Configuration:

Trigger                  Source  Template          Enabled   Delay
Daily absent             E-01    daily_absent_alert    ☑     Immediate after submit
Attendance warning       E-09    attendance_warning    ☑     Immediate on threshold cross
Attendance critical      E-09    attendance_critical   ☑     Immediate
Attendance danger        E-09    attendance_danger     ☑     Principal review then send
Fee receipt              D-04    fee_receipt_confirm   ☑     Immediate on receipt
Fee reminder (15 days)   D-09    fee_reminder          ☑     D-9 before due date
Fee defaulter warning    D-09    fee_defaulter_warn    ☑     Day 16 of default
TC ready                 C-13    tc_ready              ☑     On TC generation
Exam admit card          B-12    exam_admit_card_ready ☑     On admit card publish
Result announcement      B-18    result_announcement   ☑     On result publish
Holiday notice           E-15    holiday_notice        ☑     3 days before holiday
```

---

## 9. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/whatsapp/broadcasts/?month={m}&year={y}` | Broadcast history |
| 2 | `POST` | `/api/v1/school/{id}/whatsapp/broadcasts/` | Create and send broadcast |
| 3 | `GET` | `/api/v1/school/{id}/whatsapp/broadcasts/{broadcast_id}/analytics/` | Delivery analytics |
| 4 | `GET` | `/api/v1/school/{id}/whatsapp/templates/` | Template library |
| 5 | `POST` | `/api/v1/school/{id}/whatsapp/templates/` | Request new template |
| 6 | `GET` | `/api/v1/school/{id}/whatsapp/opt-outs/` | Opt-out register |
| 7 | `POST` | `/api/v1/school/{id}/whatsapp/opt-outs/{parent_id}/re-enable/` | Re-enable with consent |
| 8 | `GET` | `/api/v1/school/{id}/whatsapp/config/` | Auto-trigger configuration |
| 9 | `PATCH` | `/api/v1/school/{id}/whatsapp/config/` | Update auto-trigger settings |

---

## 10. Business Rules

- All WhatsApp messages to parents go through Meta-approved templates; free-form messages (outside template) are not permitted by Meta for business-initiated conversations; only allowed if parent messages first (within 24-hour conversation window)
- Opt-outs are permanent until the parent explicitly re-consents; the school cannot override an opt-out (WhatsApp policy + DPDPA compliance)
- Messages with student-specific data (attendance %, fee amount) are sent one-to-one (parent to student linkage from C-20 / C-05) — not group broadcasts that could expose one parent's data to another
- WhatsApp Business API costs are metered; UTILITY template rate is lower than MARKETING; school's monthly cost appears in D-20 petty cash / operational expenses
- BSP (Business Solution Provider) configuration is per-school (BYOG model): school connects their own WhatsApp Business Account or uses EduForge's shared number with school name as sender; dedicated number preferred for high-volume schools (>500 students)
- Message delivery failures are retried once via SMS if SMS fallback is enabled

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
