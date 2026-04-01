# G-03 — EMI & Installment Tracker

> **URL:** `/coaching/finance/installments/`
> **File:** `g-03-emi-installments.md`
> **Priority:** P1
> **Roles:** Accounts (K5) · Branch Manager (K6) · Batch Coordinator (K4 — read-only)

---

## 1. Installment Schedule Overview

```
INSTALLMENT TRACKER — All Active Students
As of 30 March 2026

  OVERVIEW:
    Students on installment plan:    856  (all students — TCC's standard 2-instalment plan)
    Instalment 1 (collected):        836  (97.7%) — enrolled this batch cycle
    Instalment 2 (upcoming/due):     442  (collected: 180 / due: 262)

  UPCOMING DUE (Next 30 Days — April 2026):
    Due date range    │ Count │ Amount due     │ Status
    ──────────────────┼───────┼────────────────┼─────────────────────────────
    Apr 1–7           │  88   │ ₹ 8,61,400    │ Auto-reminder sent Mar 25 ✅
    Apr 8–15          │  64   │ ₹ 6,24,800    │ Auto-reminder due Mar 30 ✅
    Apr 16–30         │  48   │ ₹ 4,68,000    │ Reminders scheduled Apr 1
    ──────────────────┴───────┴────────────────┴─────────────────────────────
    TOTAL DUE (April):          262  students  |  ₹ 25,60,800  (₹ 25.6 L)

  OVERDUE (past due date, not paid):
    1–15 days overdue:   32 students  |  ₹ 3,06,400   → 2nd reminder sent
    16–30 days overdue:  18 students  |  ₹ 1,72,800   → Counsellor call initiated
    > 30 days overdue:   12 students  |  ₹ 1,08,000   → Escalated to Branch Manager
    TOTAL OVERDUE:       62 students  |  ₹ 5,87,200
```

---

## 2. Individual Installment Schedule

```
INSTALLMENT DETAIL — Suresh Babu Rao (TCC-2026-2501)
Course: SSC CGL 2026–27  |  Total: ₹ 20,060 (incl. GST)

  Schedule:
    Instalment │ Due Date   │ Amount      │ Status    │ Receipt
    ───────────┼────────────┼─────────────┼───────────┼──────────────────────
    1 (50%)    │ 30 Mar 2026│ ₹ 10,030   │ ✅ PAID   │ TCC-RCP-2026-0842
               │            │             │ 30 Mar AM │ UPI: UTR 306140XXXXX
    2 (50%)    │ 01 Aug 2026│ ₹ 10,030   │ ⏳ Upcoming│ —
    ───────────┴────────────┴─────────────┴───────────┴──────────────────────
    BALANCE:   ₹ 10,030 (due 1 Aug 2026)

  REMINDERS SCHEDULED:
    Jul 18 (2 weeks before):   WhatsApp reminder — auto ✅
    Jul 28 (3 days before):    SMS reminder — auto ✅
    Aug 1 (due date):          WhatsApp + SMS — auto ✅
    Aug 5 (+4 days overdue):   Call by Accounts team — if not paid

  [Modify Schedule]   [Send Early Reminder]   [Mark as Scholarship (waive)]
```

---

## 3. Overdue Collection Workflow

```
OVERDUE MANAGEMENT — Active Cases (> 30 days)

  Student          │ ID      │ Batch          │ Amount  │ Overdue │ Last Contact  │ Action
  ─────────────────┼─────────┼────────────────┼─────────┼─────────┼───────────────┼────────────────
  Mohammed R.      │ TCC-2406│ SSC CGL Morn.  │ ₹ 9,000 │ 45 days │ Mar 22 (call) │ 🔴 Escalated
  Sravya Rao       │ TCC-2418│ SSC CGL Morn.  │ ₹ 9,000 │ 38 days │ Mar 25 (SMS)  │ 🔴 Escalated
  Pavan Reddy      │ TCC-2428│ SSC CGL Morn.  │ ₹ 9,000 │ 60 days │ Mar 10 (call) │ 🔴 Final notice
  Kiran Naidu      │ TCC-2419│ SSC CGL Morn.  │ ₹ 9,000 │ 32 days │ Mar 28 (SMS)  │ 🔴 Escalated

  PAVAN REDDY (60 days overdue) — Final Notice:
    Final notice letter sent: 29 Mar 2026 (registered post + WhatsApp)
    Content: "Pay ₹9,000 by Apr 7 or access restricted"
    Branch Manager approved the final notice ✅
    Next step: Portal access restriction from Apr 8 if unpaid

  COLLECTION SLA:
    Day 1–7:   Auto SMS (2 reminders)
    Day 8–15:  Auto WhatsApp + personal SMS from Accounts
    Day 16–30: Counsellor call (personal follow-up)
    Day 31–60: Branch Manager escalation + written notice
    Day 61+:   Access restriction pending Branch Manager decision
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/finance/installments/?status=upcoming&month=2026-04` | Upcoming instalments |
| 2 | `GET` | `/api/v1/coaching/{id}/finance/installments/student/{sid}/` | Student's instalment schedule |
| 3 | `GET` | `/api/v1/coaching/{id}/finance/installments/overdue/` | All overdue instalments |
| 4 | `POST` | `/api/v1/coaching/{id}/finance/installments/{iid}/reminder/` | Send manual reminder |
| 5 | `POST` | `/api/v1/coaching/{id}/finance/installments/{iid}/restrict-access/` | Restrict portal access (escalated overdue) |
| 6 | `PATCH` | `/api/v1/coaching/{id}/finance/installments/{iid}/reschedule/` | Reschedule instalment (Branch Manager) |

---

## 5. Business Rules

- The standard instalment plan (2 equal instalments: at enrollment and at batch midpoint) is TCC's default; no other instalment split (3 parts, 4 parts, monthly EMI) is offered without explicit Branch Manager approval; the 2-instalment model simplifies accounts reconciliation and creates a clear midpoint checkpoint for the student's commitment — a student who hasn't paid the second instalment by midpoint is likely at risk of dropping out, and the fee follow-up serves as a retention trigger
- Instalment due dates are calculated from the batch start date, not the enrollment date; the second instalment is due at the batch's midpoint (5 months in for a 10-month course); this means students who enroll late (2 months after batch start) have a shorter window before their second instalment is due; the system calculates and displays this at enrollment so the student is aware; counsellors must not manually push the second instalment date beyond the batch midpoint without Accounts approval
- Access restriction for overdue fees is the last resort before withdrawal; before access restriction, the student must receive: (1) auto-reminders, (2) a personal call from the Accounts team, (3) a written final notice, and (4) a Branch Manager review; the access restriction is not punitive — it is a practical measure to prevent the student from consuming services (tests, materials) while not paying; the restriction is lifted immediately upon payment; a student can attend physical classes during the restriction period (access restriction is portal-only)
- Instalment rescheduling (moving the second instalment date) requires Branch Manager written approval and must be logged with the reason (medical emergency, exam postponement, economic hardship); a rescheduled instalment cannot be moved more than 30 days from the original due date; if a student's hardship requires more than 30 days of extension, the Branch Manager can escalate to the Director for a longer deferral, documented with a formal agreement; this flexibility prevents student dropout while maintaining financial accountability
- Overdue fee data (amount, how long overdue) is visible to the Batch Coordinator in their batch student list (D-03) so they can be aware of at-risk students; however, the Batch Coordinator cannot take any fee action (cannot send reminders, cannot restrict access, cannot reschedule); their role is academic, not financial; the separation ensures a student's fee situation does not bias the coordinator's academic treatment of the student; the coordinator is only notified when a student's fee situation reaches the "access restriction" stage

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division G*
