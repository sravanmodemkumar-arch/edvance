# D-01 — Batch Dashboard

> **URL:** `/coaching/batches/dashboard/`
> **File:** `d-01-batch-dashboard.md`
> **Priority:** P1
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6) · Faculty (K3)

---

## 1. My Assigned Batches — Summary Cards

```
BATCH DASHBOARD — Toppers Coaching Centre (TCC), Hyderabad
Coordinator: Ms. Priya Nair   |   As of 30 March 2026

╔══════════════════════════════════╦══════════════════════════════════╗
║  SSC CGL Morning Batch           ║  Banking Morning Batch           ║
║  Mon–Sat  6:00–9:00 AM           ║  Mon–Sat  6:30–9:00 AM           ║
║  Strength: 240 students          ║  Strength: 200 students          ║
║  Today's class: ✅ IN PROGRESS   ║  Today's class: ✅ COMPLETED     ║
║  Attendance today: 212/240 (88%) ║  Attendance today: 178/200 (89%) ║
║  Next test: SSC Full Mock #25    ║  Next test: Banking Mock #14     ║
║              (Apr 5, Sunday)     ║              (Apr 4, Saturday)   ║
║  At-risk students:  14           ║  At-risk students:   9           ║
║  Fee defaulters:    18           ║  Fee defaulters:     11          ║
╚══════════════════════════════════╩══════════════════════════════════╝
```

---

## 2. Today's Class Status

```
TODAY — Monday, 30 March 2026

SSC CGL MORNING BATCH  |  Hall A, Main Campus
─────────────────────────────────────────────────────────────────
  Time:      6:00 AM – 9:00 AM
  Subject:   Quantitative Aptitude
  Faculty:   Mr. Ravi Kumar (Primary)
  Topic:     Percentage & Profit-Loss (Chapter 7)
  Status:    IN PROGRESS  (started 6:02 AM)
  Present:   212 / 240   (88.3%)
  Late:       8 students (marked late, arrived 6:05–6:22 AM)
  Absent:    28 students
    ↳  Prior-notified absences:  11
    ↳  Unexplained absences:     17  ⚠️  Auto-SMS sent to guardians

BANKING MORNING BATCH  |  Hall B, Main Campus
─────────────────────────────────────────────────────────────────
  Time:      6:30 AM – 9:00 AM
  Subject:   Reasoning
  Faculty:   Ms. Deepa Sharma (Primary)
  Topic:     Seating Arrangement & Puzzles (Chapter 11)
  Status:    COMPLETED  (ended 8:58 AM)
  Present:   178 / 200   (89.0%)
  Late:        4 students
  Absent:    22 students
    ↳  Prior-notified absences:   9
    ↳  Unexplained absences:     13  ⚠️  Auto-SMS sent to guardians
```

---

## 3. Upcoming Tests (Next 14 Days)

```
UPCOMING TESTS — SSC CGL MORNING + BANKING MORNING
─────────────────────────────────────────────────────────────────
  Date       Test Name                     Batch           Mode
  ─────────  ────────────────────────────  ──────────────  ──────
  Apr 3 Fri  RRB NTPC Sprint #8            Cross-batch     Online
  Apr 4 Sat  Banking Full Mock #14         Banking Morn.   Online
  Apr 5 Sun  SSC CGL Full Mock #25         SSC CGL Morn.   Online
  Apr 12 Sun SSC CHSL Evening Full Mock    SSC CHSL Eve.   Online
  Apr 13 Mon Chapter Test — Maths Ch 8     SSC CGL Morn.   Offline
  Apr 18 Sat Banking Sectional — GA/GK     Banking Morn.   Online

  [View Full Test Calendar →]
```

---

## 4. At-Risk Students Alert Panel

```
AT-RISK STUDENTS — SSC CGL MORNING BATCH (14 flagged)
─────────────────────────────────────────────────────────────────
  Criteria: Attendance < 70%  OR  Last 3 test avg < 35%  OR  Fee overdue > 30 days

  #   Student Name        Attend%  Avg Score  Fee Status   Risk Factor
  ─   ─────────────────   ───────  ─────────  ───────────  ────────────
  1   Pavan Reddy          58.3%    38.2%      Overdue 45d  Multiple
  2   Sravya Rao           64.1%    42.5%      OK           Attendance
  3   Kiran Naidu          62.0%    31.8%      Overdue 32d  Multiple
  4   Lakshmi Devi         69.5%    33.0%      OK           Score
  5   Mohammed Arif        55.2%    28.7%      Overdue 60d  Multiple ⚠️
  …   (9 more — [View All →])

  [Schedule Counselling]   [Send Group SMS]   [Export List]
```

---

## 5. Fee Defaulters Summary (Batch Level)

```
FEE DEFAULTERS — SSC CGL MORNING BATCH (18 students)
─────────────────────────────────────────────────────────────────
  Overdue 1–30 days:    7 students   ₹  42,000 pending
  Overdue 31–60 days:   6 students   ₹  54,000 pending
  Overdue > 60 days:    5 students   ₹  62,000 pending  ⚠️

  TOTAL PENDING (this batch):  ₹ 1,58,000

  [Notify Finance Team]   [Send Reminder SMS]   [View Individual Records →]

FEE DEFAULTERS — BANKING MORNING BATCH (11 students)
─────────────────────────────────────────────────────────────────
  Overdue 1–30 days:    5 students   ₹  28,000 pending
  Overdue 31–60 days:   4 students   ₹  32,000 pending
  Overdue > 60 days:    2 students   ₹  20,000 pending  ⚠️

  TOTAL PENDING (this batch):  ₹  80,000
```

---

## 6. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/dashboard/?coordinator={uid}` | Coordinator's batch summary cards |
| 2 | `GET` | `/api/v1/coaching/{id}/batches/{batch_id}/today-class/` | Today's class status and attendance snapshot |
| 3 | `GET` | `/api/v1/coaching/{id}/batches/{batch_id}/upcoming-tests/?days=14` | Upcoming tests for the batch |
| 4 | `GET` | `/api/v1/coaching/{id}/batches/{batch_id}/at-risk-students/` | At-risk student list with criteria flags |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{batch_id}/fee-defaulters/` | Fee defaulter summary by aging bucket |

---

## 7. Business Rules

- A student is flagged as "at-risk" when any one of three criteria is met: attendance below 70% for the current month, average score across the last three tests below 35%, or a fee outstanding beyond 30 days; when all three are true simultaneously, the student is escalated to the Branch Manager's queue for direct intervention rather than remaining only with the Batch Coordinator.
- Unexplained absences trigger an automated SMS to the registered guardian within 30 minutes of the attendance cut-off time (one hour after class start); if the student is a minor (under 18), a WhatsApp message is also sent to the POCSO-designated guardian contact, ensuring duty-of-care obligations are met even before the coordinator manually reviews the list.
- The Batch Dashboard is personalized to show only the batches assigned to the logged-in coordinator; a Branch Manager sees all batches across their branch in a consolidated view, while the Director sees a centre-wide rollup without student-level detail, enforcing a least-privilege data access pattern across roles.
- Fee defaulter counts on the dashboard are read-only for the Batch Coordinator — they can trigger reminder SMSs but cannot modify fee records; only the Accounts team (K5) and Branch Manager (K6) can mark dues as paid, waived, or rescheduled, preventing coordinators from making unauthorized fee adjustments.
- Today's class status auto-refreshes every five minutes during active class hours (5:30 AM to 9:30 AM for morning batches, 4:30 PM to 9:30 PM for evening batches); outside these windows the dashboard shows static data from the last refresh to avoid unnecessary API load during off-hours.

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
