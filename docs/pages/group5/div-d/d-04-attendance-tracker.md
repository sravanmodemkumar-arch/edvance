# D-04 — Attendance Tracker

> **URL:** `/coaching/batches/attendance/`
> **File:** `d-04-attendance-tracker.md`
> **Priority:** P1
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6)

---

## 1. Daily Attendance Summary

```
ATTENDANCE TRACKER — SSC CGL MORNING BATCH
Date: 30 March 2026 (Monday) | Coordinator: Ms. Priya Nair

  SESSION 1 — Quantitative Aptitude (06:00–07:00)
    Faculty: Mr. Suresh Kumar | Submitted: 06:08 ✅
    Present: 214  |  Absent: 18  |  Late: 8  |  Total: 240
    Rate: 89.2%

  SESSION 2 — Reasoning (08:00–09:00)
    Faculty: Mr. Mohan Rao | Submitted: 08:12 ✅
    Present: 208  |  Absent: 24  |  Late: 8  |  Total: 240
    Rate: 86.7%

  DAY SUMMARY:
    Present all sessions:  196 (81.7%) ✅
    Present some sessions:  26 (10.8%) ⚠️
    Absent all sessions:    18  (7.5%) 🔴

  AUTO-ACTIONS TRIGGERED TODAY:
    • 18 unexplained absences → SMS to students (sent 06:25 AM) ✅
    • Mohammed R. (TCC-2406): 3rd absence this week → Counsellor flagged ✅
    • Sravya R. (TCC-2418): Attendance dropped to 64% → Watch list added ⚠️
```

---

## 2. Monthly Attendance Report

```
MONTHLY REPORT — MARCH 2026 (SSC CGL MORNING)
Working days: 26  |  Avg batch attendance: 85.4%

  ATTENDANCE DISTRIBUTION:
    Band          │ Students │ % Batch │ Action
    ──────────────┼──────────┼─────────┼──────────────────────────────────
    > 90%         │   142    │  59.2%  │ ✅ Good standing
    80% – 90%     │    56    │  23.3%  │ ✅ Acceptable
    70% – 80%     │    24    │  10.0%  │ ⚠️ Warning SMS sent
    60% – 70%     │    10    │   4.2%  │ 🟡 Counsellor flagged
    < 60%         │     8    │   3.3%  │ 🔴 Access restriction warning
    ──────────────┴──────────┴─────────┴──────────────────────────────────
    Total:            240

  WEEKLY TREND (March):
    W1 (Mar 2–7):   88.4%
    W2 (Mar 9–14):  86.2%
    W3 (Mar 16–21): 83.1% ← dip (SSC admit card release day — 22 left early)
    W4 (Mar 23–28): 84.8%

  MOST ABSENT STUDENTS (this month):
    1. Mohammed R. (TCC-2406) — 43% — 15 absences / 26 sessions
    2. Pavan Reddy (TCC-2428) — 51% — 13 absences / 26 sessions
    3. Sravya Rao  (TCC-2418) — 64% —  9 absences / 26 sessions
```

---

## 3. Attendance Correction (Dispute Resolution)

```
ATTENDANCE CORRECTION REQUEST
Raised by: Ravi Singh (TCC-2403) | Date: 29 March 2026

  Dispute:
    Session:  28 March 2026, Quantitative Aptitude (06:00)
    Marked:   ABSENT
    Claim:    "I was present but seated at the back — faculty may have missed me"
    Evidence: WhatsApp screenshot showing discussion of Q3 from that day's class

  COORDINATOR REVIEW:
    Faculty (Mr. Suresh Kumar) confirms: "Yes, Ravi came late (~06:18),
    I had already marked attendance. He should be marked Late, not Absent."

    Correction: ABSENT → LATE  (attendance change: -1 absent, +1 late)
    Attendance month %: 82.1% → 84.6% (net impact: +2.5%)

    [Approve Correction]   [Reject]   [Escalate to Branch Manager]

  AUDIT:
    Original mark by: Mr. Suresh Kumar (06:08 AM, Mar 28)
    Correction by:    Ms. Priya Nair (Coordinator) — if approved
    Reason logged:    Faculty confirmation of late arrival
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/attendance/?date=2026-03-30` | Daily attendance summary for coordinator |
| 2 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/attendance/monthly/?month=2026-03` | Monthly attendance report |
| 3 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/attendance/student/{sid}/?month=2026-03` | One student's monthly record |
| 4 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/attendance/correction/` | Raise or approve an attendance correction |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/attendance/alerts/?month=2026-03` | Students who triggered auto-alerts |

---

## 5. Business Rules

- Attendance corrections are a high-fraud-risk operation; the system logs every correction with the original value, the new value, the person who made the change, the timestamp, and the stated reason; corrections are visible to the Branch Manager in their audit report; a coordinator who makes more than 10 attendance corrections per month is flagged for review — this could indicate genuine errors or systematic manipulation to inflate attendance percentages for fee-defaulter retention
- A student's attendance percentage directly determines their access to study material and mock tests on the platform; when attendance drops below 60%, the student's test access is restricted to one test per week (instead of the standard unlimited access) and a warning banner appears on their student dashboard; this creates a direct consequence for poor attendance without the more drastic step of removing them from the batch
- The "late" designation has a meaningful boundary: students arriving within the first 15 minutes of class are marked late; students arriving after 15 minutes but within the first 45 minutes are marked late + note; students arriving after 45 minutes are marked absent for that session regardless of their presence; this 45-minute rule prevents students from using a 5-minute appearance at end of class to claim attendance
- Automated SMS alerts for absences must use the student's own registered number for adult students (18+); for minor students, the alert goes to the parent's registered WhatsApp number; coordinators cannot override this routing — the contact field in the student profile determines alert destination; changing the registered contact number requires the student's physical signature (in-branch) or an OTP confirmation, preventing students from changing their parent's number to their own
- Monthly attendance reports are shared with the Branch Manager by the 3rd of the following month as part of the standard MIS pack; coordinators who do not submit the monthly report by the 3rd face a process violation note in their performance log; the attendance data feeds into the franchise performance dashboard (A-05) for franchise branches, making timely submission a contractual obligation with franchisees

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
