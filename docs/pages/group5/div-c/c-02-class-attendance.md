# C-02 — Class Attendance

> **URL:** `/coaching/faculty/attendance/`
> **File:** `c-02-class-attendance.md`
> **Priority:** P1
> **Roles:** Faculty (K2) · Batch Coordinator (K3)

---

## 1. Take Attendance

```
TAKE ATTENDANCE — SSC CGL MORNING BATCH
30 March 2026 (Monday) | 06:00–08:00 | Hall A
Faculty: Mr. Suresh Kumar | Subject: Quantitative Aptitude

  Attendance window:  06:00 – 06:15  (late mark after 06:15)
  Students registered: 236 | Submitted: 0 | Time remaining: 8 min

  QUICK MARK:  [✅ Mark All Present]  [Clear All]

  #    Student Name           Roll No   Status         Late?
  ──────────────────────────────────────────────────────────
  1    Akhil Kumar            TCC-2401  ( ) P  (●) A    [ ]
  2    Priya Reddy            TCC-2402  (●) P  ( ) A    [ ]
  3    Ravi Singh             TCC-2403  (●) P  ( ) A    [✓] Late
  4    Divya Sharma           TCC-2404  (●) P  ( ) A    [ ]
  5    Karthik M.             TCC-2405  (●) P  ( ) A    [ ]
  6    Mohammed R.            TCC-2406  ( ) P  (●) A    [ ]  ← 3rd absence this week
  7    Suresh P.              TCC-2407  (●) P  ( ) A    [ ]
  8    Anitha K.              TCC-2408  (●) P  ( ) A    [ ]
  9    Lakshmi T.             TCC-2409  (●) P  ( ) A    [ ]
  10   Rajesh Kumar           TCC-2410  (●) P  ( ) A    [ ]
  ...  (226 more students)

  Showing 10 of 236 | [Load All] | Search: [________________]

  CURRENT COUNT: Present: 198 | Absent: 14 | Unmarked: 24
  [Save Attendance]   ⚠️ 24 students unmarked — save will mark them absent

  ── AUTO-ALERTS TRIGGERED ───────────────────────────────────────────────────
  Mohammed R. (TCC-2406): 3rd absence this week → Counsellor flagged ✅
  Akhil Kumar (TCC-2401): Today absent (1st this month) → No alert (threshold: 3)
```

---

## 2. Attendance History — Monthly View

```
ATTENDANCE CALENDAR — Mohammed R. (TCC-2406)
Batch: SSC CGL Morning | Month: March 2026

  Week │ Mon  │ Tue  │ Wed  │ Thu  │ Fri  │ Sat  │ Monthly %
  ─────┼──────┼──────┼──────┼──────┼──────┼──────┼──────────
  W1   │  P   │  P   │  A   │  P   │  P   │  P   │
  W2   │  P   │  A   │  P   │  P   │  A   │  P   │
  W3   │  A   │  P   │  P   │  A   │  P   │  P   │
  W4   │  A   │  —   │  —   │  —   │  —   │  —   │
  ─────────────────────────────────────────────────────────
  Total: 18P + 5A + 3 remaining = 18/21 = 57.1% 🔴 BELOW CUTOFF

  ⚠️ 60% cutoff for counsellor action → Mohammed already flagged
  Parent notified (minor? No — Mohammed is 22, adult student): SMS to student only
  Counsellor: Ms. Ananya Roy — session scheduled 1 Apr 2026
```

---

## 3. Batch Attendance Summary

```
BATCH ATTENDANCE SUMMARY — SSC CGL MORNING (March 2026)

  Attendance Band   │ Students │ % of Batch │ Action
  ──────────────────┼──────────┼────────────┼─────────────────────────────────
  > 90%             │   142    │   60.2%    │ ✅ Good standing
  75% – 90%         │    68    │   28.8%    │ ⚠️ Reminder SMS sent
  60% – 75%         │    18    │    7.6%    │ 🟡 Counsellor flagged
  < 60%             │     8    │    3.4%    │ 🔴 Parent alert + access warning
  ──────────────────┴──────────┴────────────┴─────────────────────────────────
  Batch average:    85.2%   Target: 85%   ✅

  WEEKLY TREND (March):
    Week 1: 88.4% | Week 2: 86.2% | Week 3: 83.1% | Week 4: 84.2% (partial)
    ⚠️ Declining trend — investigate Week 3 dip (SSC CGL admit card release day — many left early)
```

---

## 4. API Endpoints

| # | Method | Endpoint | Description |
|---|---|---|---|
| 1 | `GET` | `/api/v1/coaching/{id}/attendance/?batch={id}&date=2026-03-30` | Today's attendance sheet |
| 2 | `POST` | `/api/v1/coaching/{id}/attendance/` | Submit attendance for a session |
| 3 | `GET` | `/api/v1/coaching/{id}/attendance/student/{sid}/?month=2026-03` | Monthly calendar for one student |
| 4 | `GET` | `/api/v1/coaching/{id}/attendance/batch/{bid}/summary/?month=2026-03` | Batch monthly summary |
| 5 | `GET` | `/api/v1/coaching/{id}/attendance/alerts/` | Students below threshold (auto-flagged) |

---

## 5. Business Rules

- Attendance must be submitted within 30 minutes of class start; submissions after 30 minutes are flagged as "late submission" and are visible to the Batch Coordinator; chronic late attendance submission (>3 times/month) is a faculty performance issue — it suggests the faculty is not tracking attendance seriously or is marking attendance retrospectively from memory, which introduces errors
- The 15-minute late-mark window is enforced by the system; a student marked present after 06:15 is automatically tagged as "Late"; 3 late-marks in a week count as 1 absence for attendance calculation purposes; this prevents students from gaming attendance by arriving 45 minutes late and claiming they were "present"
- For minor students (Foundation batch, students under 18): any single absence triggers an immediate WhatsApp alert to the registered parent number; this is a POCSO duty-of-care requirement and a parent service commitment; parents who pay ₹12,000/year have a legitimate expectation of being notified when their child doesn't attend; failure to notify is a customer service failure and a potential POCSO liability
- Unmarked students at attendance save are automatically marked absent; this design choice (absent-by-default) is intentional — it prevents attendance inflation where unmarked students are treated as present; faculty who habitually save with many unmarked students are creating unreliable attendance records; the system shows the count of unmarked before save to prompt completion
- The attendance data owned by TCC is personal data under DPDPA 2023; it can only be shared with the student, their parent (if minor), their Batch Coordinator, and the Branch Manager; it cannot be exported in bulk or shared with third parties without explicit consent; TCC's privacy policy must state how long attendance records are retained (TCC policy: 3 years post-batch end) and the student's right to request correction of incorrectly marked absences

---

*Last updated: 2026-03-30 · Group 5 — Coaching Portal · Division C*
