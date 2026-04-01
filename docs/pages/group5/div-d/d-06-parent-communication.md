# D-06 — Parent Communication

> **URL:** `/coaching/batches/parents/`
> **File:** `d-06-parent-communication.md`
> **Priority:** P2
> **Roles:** Batch Coordinator (K4) · Counsellor (K3)

---

## 1. Parent Communication Dashboard

```
PARENT COMMUNICATION — SSC CGL MORNING BATCH
As of 30 March 2026  |  Coordinator: Ms. Priya Nair

  COMMUNICATION STATS (March 2026):
    Total messages sent:   486
    SMS (auto-alerts):     342  (absence notifications, fee reminders)
    WhatsApp (manual):      86  (progress updates, event alerts)
    Email:                  58  (monthly progress reports)

  PENDING ACTIONS:
    🔴 8 parents — no response to absence alerts (3+ days)
    🟡 5 parents — fee discussion request pending (submitted via portal)
    ✅ Monthly progress reports sent: 236/240 (4 bounced — email invalid)

  PARENT GROUPS (WhatsApp — Coordinator as admin):
    SSC CGL Morning — Parents: 218 members (92 parents, 2 per family)
      Last message: 29 Mar — "Mock #23 result summary — batch avg 124.6/200"
      ⚠️ Rule: No individual student data in group. Aggregate only.
```

---

## 2. Send Communication

```
NEW MESSAGE — PARENT COMMUNICATION

  Type:        (●) SMS  ( ) WhatsApp  ( ) Email
  Recipients:  (●) All parents — SSC CGL Morning  (218 contacts)
               ( ) Specific students' parents  [Select students...]
               ( ) At-risk students' parents only  (14 students)

  Template:    [Monthly Progress Summary ▼]

  Message Preview:
  ┌─────────────────────────────────────────────────────────────────────────────┐
  │ Dear Parent, SSC CGL Morning Batch — March 2026 Update:                    │
  │ Batch Avg Score: 124.6/200 (Full Mock #23). Your ward's individual         │
  │ performance report is available on the Parent Portal:                       │
  │ tcc.eduforge.in/parent — Login with your registered mobile number.          │
  │ Next test: Apr 5 (Full Mock #25, 9 AM). — TCC Hyderabad                   │
  └─────────────────────────────────────────────────────────────────────────────┘
  Characters: 284 / 320 (SMS: 2 parts)

  Schedule:    (●) Send now  ( ) Schedule: [___ date/time ___]

  [Send]   [Save as Template]   [Preview WhatsApp]
```

---

## 3. Inbound Parent Requests

```
PARENT REQUESTS — Open (5 pending)

  #  │ Parent            │ Student        │ Request Type          │ Received    │ Status
  ───┼───────────────────┼────────────────┼───────────────────────┼─────────────┼──────────────
  1  │ Mr. Arjun Reddy   │ Ravi S. (2403) │ Fee instalment change │ 29 Mar 2pm  │ 🟡 Pending
  2  │ Mrs. Lakshmi Rao  │ Priya R. (2402)│ Study material access │ 29 Mar 9am  │ 🟡 Pending
  3  │ Mr. Suresh Naidu  │ Kiran N. (2419)│ Score explanation     │ 28 Mar 6pm  │ ✅ Responded
  4  │ Mrs. Anitha Devi  │ Sravya R.(2418)│ Attendance concern    │ 27 Mar 3pm  │ ✅ Responded
  5  │ Mr. Ravi Kumar    │ Akhil K. (2401)│ Rank certificate req  │ 30 Mar 10am │ 🟡 New

  [View #1]  [Respond]  [Escalate to Counsellor]  [Escalate to Branch Mgr]
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/parents/messages/?month=2026-03` | Outbound message log |
| 2 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/parents/messages/` | Send SMS/WhatsApp/email to parents |
| 3 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/parents/requests/` | Inbound parent requests |
| 4 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/parents/requests/{rid}/respond/` | Respond to parent request |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/parents/directory/` | Parent contact directory for batch |

---

## 5. Business Rules

- Individual student performance data (scores, rank, attendance percentage) must never be shared in batch-level parent groups; the group channel is for aggregate updates, schedule notifications, and event announcements; individual data goes through the Parent Portal (O-01) where each parent sees only their own ward's data; a coordinator who posts a student's rank or score in a group — even in praise ("Congratulations to Akhil for scoring 178!") — violates DPDPA 2023 without explicit student consent
- Parent communication must go through the platform's registered sender ID, not the coordinator's personal phone; all messages sent through the platform are logged with delivery status and read receipts (for WhatsApp); this creates an audit trail that protects TCC if a parent disputes that they were notified about their child's absence, fee due date, or exam schedule; messages sent from personal phones have no audit trail and create liability
- Inbound parent requests must be responded to within 48 hours; requests that involve fee changes, withdrawal, or escalation must be escalated to the Branch Manager within 24 hours; coordinators cannot make commitments on fee waivers, instalment restructuring, or course transfers in parent communication — these decisions belong to the Branch Manager; coordinators should acknowledge the request and inform the parent that the relevant authority will respond
- Minor student parents have an additional right: under POCSO duty-of-care guidelines adopted by TCC, parents of students under 18 must receive weekly attendance summaries (not just absence alerts) and must receive a flag when their child's overall attendance drops below 75%; this is proactive communication, not reactive; coordinators for Foundation batch (predominantly minors) must configure weekly auto-digest for all enrolled parents
- Parent contact information is personal data under DPDPA 2023; the parent directory exported for communication purposes cannot be shared externally or used for marketing without explicit consent; if TCC runs a referral programme ("refer a student, get ₹1,000"), the parent's participation must be opt-in; coordinators cannot enrol parents in marketing campaigns without their recorded consent, which is stored in the CRM

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
