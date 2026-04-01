# F-15 — Fee & Exam Reminder Campaigns

> **URL:** `/school/reminder-campaigns/`
> **File:** `f-15-reminder-campaigns.md`
> **Template:** `portal_base.html` (light theme)
> **Priority:** P1
> **Roles:** Communication Coordinator (S3) — manage campaigns · Academic Coordinator (S4) — approve exam reminders · Principal (S6) — approve fee escalation campaigns · Administrative Officer (S3) — fee campaign trigger

---

## 1. Purpose

Scheduled, automated reminder campaigns tied to the academic calendar (A-10). Rather than manually sending reminders before each exam date, fee due date, or registration deadline, this module allows administrators to configure once-per-year campaign schedules that auto-trigger at the right time.

Key reminder types for Indian schools:
- **Fee due date reminders** (D-04): 15 days before, 7 days before, 1 day before, on due date, 5 days after
- **Exam schedule reminders**: "Annual exam starts in 3 days"
- **Board exam registration deadlines** (B-33 LOC submission)
- **Scholarship application deadlines** (NSP, PM Yashasvi, state scholarships)
- **APAAR / document submission deadlines**
- **Application deadlines** (NCC/NSS camps, inter-school competitions)
- **Report card collection reminders** post-result

---

## 2. Page Layout

### 2.1 Header
```
Reminder Campaign Manager                            [+ New Campaign]  [Schedule Builder]
Academic Year: [2026–27 ▼]

Active Campaigns: 3  ·  Sent This Month: 8 automated reminders  ·  Next: "Annual Exam begins" in 2 days
```

### 2.2 Campaign List
```
Campaign Name              Type     Triggers  Next Trigger   Status       Audience
Fee — Term 2 Reminder      Fee      5 msgs    Completed      ✅ Done      Outstanding fee parents
Annual Exam Countdown      Exam     4 msgs    29 Mar 2026    🟢 Active    All parents (Classes X, XII)
NSP Scholarship Deadline   Academic 2 msgs    15 Apr 2026    ⏳ Upcoming  NSP-eligible students
Board LOC Deadline         Board    1 msg     Completed      ✅ Done      Class X & XII parents
Report Card Collection     Results  2 msgs    Upcoming       ⏳ Upcoming  All parents
```

---

## 3. Create Campaign

```
[+ New Campaign]

Campaign Name: [Annual Exam Countdown — Class X & XII          ]
Category: ● Examination  ○ Fee  ○ Scholarship  ○ Admission  ○ Event  ○ General

Audience:
  ● Filter by class: [☑ Class X-A  ☑ Class X-B  ☑ XII-A  ☑ XII-B  ☑ XII-C]
  ○ Fee-based filter (e.g., outstanding > ₹0)
  ○ All parents

Trigger-based messaging (configure each reminder):

  Reminder 1:
    Send: [7 days before] [Annual Exam Start Date (A-10)]
    Channel: ☑ WhatsApp  ○ SMS  ○ Both
    Template: T07 — exam_schedule_announcement
    Message: "Dear Parent, [Name]'s Annual Exam begins in 7 days (1 Apr 2026).
      Syllabus and exam schedule: [Link to portal]. All the best!
      — Greenfields School"

  Reminder 2:
    Send: [3 days before] [Annual Exam Start Date]
    Channel: ☑ WhatsApp  ☑ SMS (both — closer to exam)
    Message: "REMINDER: Annual Exam begins on 1 Apr 2026 (in 3 days).
      Please ensure [Name] has their admit card and required stationery."

  Reminder 3:
    Send: [1 day before] [Annual Exam Start Date]
    Channel: ☑ WhatsApp  ☑ SMS
    Message: "Tomorrow: Annual Exam Day 1. [Name] must report by 8:45 AM.
      Carry admit card. No mobile phones in exam hall. — Greenfields School"

  Reminder 4:
    Send: [Day of exam — 7:00 AM]
    Channel: ☑ WhatsApp
    Message: "Exam Day! Best wishes to [Name] for today's [Subject] exam.
      Report time: 8:45 AM, Exam Hall: [Hall]. — Greenfields School"

  [+ Add Another Reminder]

Active dates:
  Campaign start: [22 Mar 2026 — first reminder]
  Campaign end: [1 Apr 2026 — day-of reminder]

[Save Campaign]  [Save & Activate]
```

---

## 4. Fee Reminder Campaign (Pre-built)

```
Fee Reminder Campaign — Term 2 (Auto-configured from D-04 due date)

Due date: 31 March 2026

Reminder schedule:
  Day -15 (16 Mar): "Term 2 fee of ₹{amount} due on 31 Mar. Pay online or at counter."
  Day -7  (24 Mar): "REMINDER: Term 2 fee due in 7 days. Pay now to avoid late fee."
  Day -1  (30 Mar): "FINAL REMINDER: Term 2 fee due tomorrow (31 Mar). Late fee of ₹50/month applies after."
  Day 0   (31 Mar): "Today is the fee due date. Please pay now to avoid late fee."
  Day +5  (5 Apr):  "OVERDUE: ₹{outstanding} fee for {name} is overdue. Late fee of ₹50 has been added."

Audience: Parents with outstanding Term 2 fee > ₹0 (as of message date — live query)
Channel: WhatsApp (primary) + SMS fallback
Template: DLT-approved T05 variants

Results so far:
  Day -15 message: 142 sent, 138 delivered (97%), 118 read (85%)
  Day -7 message: 98 outstanding parents sent (44 paid after Day -15 reminder)
  Day -1 message: 82 outstanding parents
  Day 0: 71 outstanding (11 paid on reminder day)
```

---

## 5. Scholarship Deadline Campaign

```
NSP Scholarship Campaign — 2026–27

Scholarship: National Scholarship Portal — SC/ST/OBC Pre-Matric
Eligible students: 18 (from C-07 RTE + D-13 scholarship records)
Last date to apply: 31 October 2026

Campaign messages:
  1 Oct 2026: "NSP Scholarship application portal opens. [Name] may be eligible.
               Apply at scholarships.gov.in. Documents needed: Caste cert, income cert,
               attendance certificate (E-12). Deadline: 31 Oct 2026. — School"
  20 Oct 2026: "REMINDER: NSP Scholarship deadline in 11 days. If not applied,
                contact school for help. — Greenfields School"
  28 Oct 2026: "FINAL REMINDER: NSP deadline in 3 days. Come to school for form
                assistance if needed. — Greenfields School"

Attached to first message: NSP application guide PDF
```

---

## 6. Campaign Analytics

```
Campaign Performance — Annual Exam Countdown

Reminder       Date        Recipients  Delivered  Read     Action Taken
7-day ahead    22 Mar 26      165        161        144     32 parents logged into portal
3-day ahead    28 Mar 26      165        162        155     —
1-day ahead    31 Mar 26      165        163        159     —
Day-of         1 Apr 26       165        160        148     —

Open rate trend: 87% → 94% → 96% (open rate increases as exam approaches — expected)
```

---

## 7. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/school/{id}/reminder-campaigns/?year={y}` | Campaign list |
| 2 | `POST` | `/api/v1/school/{id}/reminder-campaigns/` | Create campaign |
| 3 | `GET` | `/api/v1/school/{id}/reminder-campaigns/{camp_id}/` | Campaign detail |
| 4 | `PATCH` | `/api/v1/school/{id}/reminder-campaigns/{camp_id}/` | Update campaign |
| 5 | `POST` | `/api/v1/school/{id}/reminder-campaigns/{camp_id}/activate/` | Activate campaign |
| 6 | `POST` | `/api/v1/school/{id}/reminder-campaigns/{camp_id}/pause/` | Pause campaign |
| 7 | `GET` | `/api/v1/school/{id}/reminder-campaigns/{camp_id}/analytics/` | Campaign performance |

---

## 8. Business Rules

- Campaign triggers are computed relative to event dates from A-10 Academic Calendar — if the exam date changes in A-10, all relative reminders automatically shift
- Fee reminders use live outstanding balance queries — a parent who pays between "15 days before" and "7 days before" does not receive the "7 days before" reminder
- Scholarship campaigns target students in the eligible category (from D-13 / C-07 records) — manually verified list that the school updates annually
- Campaign messages must use DLT-registered SMS templates and Meta-approved WhatsApp templates — the campaign builder only allows templates from the approved library
- Campaign can be paused at any time (e.g., if exam is postponed due to a holiday); pausing suspends all future triggers until reactivated or updated
- A test run (send to 1 admin phone number) is available before activating a campaign for real recipients

---

*Last updated: 2026-03-27 · Group 3 — School Portal · Division F*
