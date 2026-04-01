# D-03 — Student List (per Batch)

> **URL:** `/coaching/batches/students/`
> **File:** `d-03-student-list.md`
> **Priority:** P1
> **Roles:** Batch Coordinator (K4) · Branch Manager (K6)

---

## 1. Batch Student Roster

```
STUDENT LIST — SSC CGL MORNING BATCH
As of 30 March 2026  |  Coordinator: Ms. Priya Nair

  Filter: [All ▼]  [Status: All ▼]  [Fee: All ▼]  [Risk: All ▼]  [Search: _____]

  #    Student Name        Roll No   Joined    Attend%  Avg/100  Fee      Status
  ────────────────────────────────────────────────────────────────────────────────
  1    Akhil Kumar         TCC-2401  Aug 2025   95.4%    91.2    Paid     ✅ Active
  2    Priya Reddy         TCC-2402  Aug 2025   88.2%    78.6    Paid     ✅ Active
  3    Ravi Singh          TCC-2403  Sep 2025   82.1%    66.4    Paid     ✅ Active
  4    Divya Sharma        TCC-2404  Aug 2025   90.8%    84.3    Paid     ✅ Active
  5    Karthik M.          TCC-2405  Aug 2025   86.5%    72.1    Paid     ✅ Active
  6    Mohammed R.         TCC-2406  Aug 2025   57.1%    48.2    Paid     🔴 At-Risk
  7    Suresh P.           TCC-2407  Oct 2025   78.4%    62.8    Overdue  🟡 Watch
  8    Anitha K.           TCC-2408  Aug 2025   92.1%    80.4    Paid     ✅ Active
  9    Lakshmi T.          TCC-2409  Nov 2025   70.2%    55.6    Paid     🟡 Watch
  10   Rajesh Kumar        TCC-2410  Aug 2025   93.6%    88.9    Paid     ✅ Active
  ...  (230 more students)

  Showing 10 of 240  |  [Load All]  |  [Export CSV]

  SUMMARY:
    ✅ Active:    208 (86.7%)   🟡 Watch:  18 (7.5%)
    🔴 At-Risk:   14 (5.8%)    ⬛ Inactive:  0 (0%)

  [Send Batch SMS]  [Schedule Counselling (14 at-risk)]  [Fee Reminder (18)]
```

---

## 2. Student Detail Card (Coordinator View)

```
STUDENT PROFILE — Mohammed R. (TCC-2406)
Batch: SSC CGL Morning | Coordinator: Ms. Priya Nair

  PERSONAL:
    Full Name:    Mohammed Riyaz Ahmed
    Phone:        +91-98765-12340   (SMS enabled)
    Email:        mohammed.riyaz@gmail.com
    Age:          22 (adult — no POCSO guardian requirement)
    Joined:       18 Aug 2025

  ACADEMIC STATUS:
    Attendance:   57.1% — 🔴 BELOW 60% CUTOFF
    Scores:       Last 5 tests avg: 48.2/100
      Full Mock #23: 44  | Quant Sprint #17: 52 | Full Mock #22: 46
      Quant Sprint #16: 50 | Full Mock #21: 48
    Weak areas:   Caselet DI (32%), Data Interpretation (41%)

  FEE STATUS:
    Course fee:   ₹18,000 (SSC CGL — 10 months)
    Paid:         ₹12,000 (Installment 1: Aug, Installment 2: Oct)
    Due:          ₹6,000 (Installment 3 — overdue 0 days, due Apr 1)
    Next due:     01 Apr 2026

  COUNSELLING HISTORY:
    15 Mar 2026 — Counsellor: Ms. Ananya Roy — attendance discussion
    Session notes: [view — restricted to coordinator and above]

  ACTIONS:
    [Send SMS]  [Schedule Counselling]  [Mark as Inactive]  [View Full Profile →]
```

---

## 3. Batch Composition Analytics

```
BATCH ANALYTICS — SSC CGL MORNING (240 students)
As of 30 March 2026

  BY JOINING MONTH:
    Aug 2025 (batch start):  186 students  (77.5%)
    Sep–Oct 2025 (late):      38 students  (15.8%)
    Nov 2025 onward:          16 students   (6.7%) ← performance gap expected

  BY SCORE BAND (last full mock):
    Band         │ Range    │ Students │ %
    ─────────────┼──────────┼──────────┼──────
    Excellent    │ 80–100   │    42    │ 17.5%
    Good         │ 60–79    │    88    │ 36.7%
    Average      │ 40–59    │    76    │ 31.7%
    Weak         │ 20–39    │    28    │ 11.7%
    Critical     │ 0–19     │     6    │  2.5%

  BY ATTENDANCE BAND:
    > 90%:   142 students  (59.2%)
    75–90%:   68 students  (28.3%)
    60–75%:   16 students   (6.7%)
    < 60%:    14 students   (5.8%) ← counsellor-flagged

  GENDER:
    Male: 158 (65.8%)  |  Female: 82 (34.2%)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/students/` | Full student roster with filters |
| 2 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/students/{sid}/` | One student's coordinator-view profile |
| 3 | `POST` | `/api/v1/coaching/{id}/batches/{bid}/students/{sid}/sms/` | Send SMS to a student |
| 4 | `PATCH` | `/api/v1/coaching/{id}/batches/{bid}/students/{sid}/status/` | Update student status (active/inactive) |
| 5 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/students/analytics/` | Batch composition analytics |
| 6 | `GET` | `/api/v1/coaching/{id}/batches/{bid}/students/export/` | Export roster as CSV (role-gated) |

---

## 5. Business Rules

- The student list visible to a Batch Coordinator is limited to their assigned batches; a coordinator for SSC CGL Morning cannot view students in the Banking Batch; within their batch, coordinators see academic performance (attendance, scores), fee status (paid/overdue amounts), and counselling history summaries; they do not see personal documents (Aadhaar, PAN), health information, or full admission records — those remain in the Admissions division
- "Inactive" status can be set by the Coordinator for students who have formally withdrawn or been removed for non-payment after the grace period; inactivation is irreversible by the coordinator — reactivation requires Branch Manager approval; this prevents coordinators from accidentally inactivating active students who are temporarily absent
- The CSV export of student data (Roll No, Name, Phone, Scores) is restricted to Batch Coordinator and above; the exported file is watermarked with the coordinator's name and timestamp; bulk exports are logged in the audit trail; this prevents mass export of student data for misuse (selling contact lists to competitors, which is a documented problem in the coaching industry)
- Late joiners (students who enrolled more than 6 weeks after batch start) are flagged with a "late join" tag in the roster; coordinators must schedule a one-time catch-up plan for late joiners; students who join late without a catch-up plan consistently score in the bottom quartile; the system auto-generates a suggested catch-up schedule based on the missed topics in the curriculum tracker
- Student phone numbers are the primary communication channel; TCC uses a registered business sender ID for all batch SMS to avoid being marked as spam; coordinators cannot use personal phones or WhatsApp for official batch communications — all communication must go through the platform to maintain audit trails; a coordinator who uses a personal phone to share test dates, fee reminders, or results with students is creating an unauditable record

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division D*
